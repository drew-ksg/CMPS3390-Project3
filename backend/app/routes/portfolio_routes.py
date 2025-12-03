# backend/app/routes/portfolio_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user
from ..models import User
from ..controllers.portfolio_controller import PortfolioController
from ..services.paper_trading_service import PaperTradingService
from ..services.stock_api import API
from ..schemas import Trade


router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])

# =============================================================================
@router.get("/summary")
def get_portfolio_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """GET /api/portfolio/summary. Returns: total value, cash balance, profit/loss"""
    result = PortfolioController.get_portfolio_summary(db, current_user.id)
    return result

# =============================================================================
@router.get("/performance")
def get_portfolio_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """GET /api/portfolio/performance. Returns: historical performance data for charts"""
    result = PortfolioController.get_portfolio_performance(db, current_user.id)
    return result

# =============================================================================
@router.get("/positions")
def get_positions(
    symbol: str | None = None,  # Optional — allows all positions OR single position
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    GET /api/portfolio/positions
    Returns either:
        - all positions (if no symbol is provided)
        - or details for a specific position (if symbol is provided)
    """
    if symbol:
        return PortfolioController.get_position_details(db, current_user.id, symbol)
    else:
        return PortfolioController.get_portfolio_summary(db, current_user.id) 

# =============================================================================
@router.get("/cash")
def get_cash_balance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """GET /api/portfolio/cash. Returns: user's available cash balance"""
    cash = PaperTradingService.get_cash_balance(db, current_user.id)
    return {"cash_balance": cash}

# =============================================================================
@router.post("/validate-trade")
def validate_trade(
    symbol: str,
    trade_type: str,
    quantity: float,
    price: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """POST /api/portfolio/validate-trade. Check if a trade is valid before executing"""
    cash_balance = PaperTradingService.get_cash_balance(db, current_user.id)

    if trade_type.upper() == "BUY":
        valid = PaperTradingService.validate_buy_order(
            cash_balance, quantity, price
        )

    elif trade_type.upper() == "SELL":
        valid = PaperTradingService.validate_sell_order(
            db, current_user.id, symbol, quantity
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid trade type. Use BUY or SELL.")

    return {"valid": valid}
# =============================================================================
@router.post("/trade")
def execute_trade(
    trade: Trade,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """POST /api/portfolio/execute-trade"""
    result = PaperTradingService.execute_trade(db, current_user.id, trade.symbol, trade.trade_type, trade.quantity)
    return result
