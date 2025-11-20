# TODO: Simulate order execution, validate buying power, manage virtual cash balance, check if user can afford trade
# backend/app/services/paper_trading_service.py

from sqlalchemy import func
from app.models import Transaction
from app.models import Holding 

class PaperTradingService:
    """Handles paper trading validation and execution"""

    INITIAL_CASH = 100000.0  # Users start with $100k virtual cash

    @staticmethod
    def get_cash_balance(db, user_id: int):
        """
        Calculate user's available cash.
        Starts with INITIAL_CASH and subtracts/credits all past trades.
        """

        # Total spent on buys
        buy_total = (
            db.query(func.sum(Transaction.quantity * Transaction.price))
            .filter(Transaction.user_id == user_id, Transaction.type == "BUY")
            .scalar()
        ) or 0.0

        # Total gained from sells
        sell_total = (
            db.query(func.sum(Transaction.quantity * Transaction.price))
            .filter(Transaction.user_id == user_id, Transaction.type == "SELL")
            .scalar()
        ) or 0.0

        return PaperTradingService.INITIAL_CASH - buy_total + sell_total

    @staticmethod
    def validate_buy_order(cash_balance: float, quantity: float, price: float):
        """Return True only if user can afford this trade."""
        total_cost = quantity * price
        return cash_balance >= total_cost

    @staticmethod
    def validate_sell_order(db, user_id: int, symbol: str, quantity: float):
        """
        Check if user owns enough shares to sell.
        Assumes 'Holding' model stores total shares per symbol.
        """
        holding = (
            db.query(Holding)
            .filter(Holding.user_id == user_id, Holding.symbol == symbol)
            .first()
        )

        if not holding:
            return False

        return holding.quantity >= quantity

    @staticmethod
    def execute_trade(db, user_id: int, symbol: str, trade_type: str, quantity: float, price: float):
        """
        Execute a paper trade:
        - Validates trade
        - Creates a transaction record
        - Updates holdings
        - Returns success/failure dict
        """

        cash_balance = PaperTradingService.get_cash_balance(db, user_id)

        # Validate BUY
        if trade_type == "BUY":
            if not PaperTradingService.validate_buy_order(cash_balance, quantity, price):
                return {"success": False, "message": "Insufficient cash."}

        # Validate SELL
        if trade_type == "SELL":
            if not PaperTradingService.validate_sell_order(db, user_id, symbol, quantity):
                return {"success": False, "message": "Not enough shares to sell."}

        # --- Record transaction ---
        new_tx = Transaction(
            user_id=user_id,
            symbol=symbol,
            type=trade_type,
            quantity=quantity,
            price=price,
        )
        db.add(new_tx)

        # --- Update holdings ---
        holding = (
            db.query(Holding)
            .filter(Holding.user_id == user_id, Holding.symbol == symbol)
            .first()
        )

        if trade_type == "BUY":
            if holding:
                holding.quantity += quantity
            else:
                db.add(Holding(user_id=user_id, symbol=symbol, quantity=quantity))

        elif trade_type == "SELL":
            holding.quantity -= quantity
            if holding.quantity == 0:
                db.delete(holding)

        db.commit()
        return {"success": True, "message": f"{trade_type} executed successfully."}
