# backend/app/controllers/portfolio_controller.py

from sqlalchemy import func
from app.models import Transaction
from app.services.paper_trading_service import PaperTradingService


class PortfolioController:
    """Handles portfolio business logic"""

    @staticmethod
    def get_portfolio_summary(db, user_id: int):
        """Calculate total portfolio value, cash balance, and overall profit/loss."""

        # 1. Get cash balance using the PaperTradingService
        cash_balance = PaperTradingService.get_cash_balance(db, user_id)

        # 2. Get net position per stock:
        # SUM(BUY qty) - SUM(SELL qty) → shares currently owned
        positions = (
            db.query(
                Transaction.symbol,
                func.sum(
                    func.case([(Transaction.type == "BUY", Transaction.quantity)], else_=0)
                ).label("bought"),
                func.sum(
                    func.case([(Transaction.type == "SELL", Transaction.quantity)], else_=0)
                ).label("sold")
            )
            .filter(Transaction.user_id == user_id)
            .group_by(Transaction.symbol)
            .all()
        )

        total_portfolio_value = 0.0
        detailed_positions = []

        # We need real-time prices (We can add API later)
        # For now, assume current price == latest transaction price
        for pos in positions:
            owned = (pos.bought or 0) - (pos.sold or 0)
            if owned <= 0:
                continue  # user no longer owns this stock

            # Get latest transaction price
            latest_price = (
                db.query(Transaction.price)
                .filter(Transaction.user_id == user_id, Transaction.symbol == pos.symbol)
                .order_by(Transaction.date.desc())
                .first()
            )
            current_price = latest_price[0] if latest_price else 0
            position_value = owned * current_price

            detailed_positions.append({
                "symbol": pos.symbol,
                "quantity": owned,
                "current_price": current_price,
                "position_value": position_value
            })

            total_portfolio_value += position_value

        total_value = cash_balance + total_portfolio_value

        return {
            "cash_balance": cash_balance,
            "portfolio_value": total_portfolio_value,
            "total_value": total_value,
            "positions": detailed_positions,
        }

    # =============================================================================
    @staticmethod
    def get_portfolio_performance(db, user_id: int):
        """Returns daily total portfolio value history — e.g. for charts."""

        # Sum portfolio value per day:
        results = (
            db.query(
                func.date(Transaction.date).label("day"),
                func.sum(Transaction.quantity * Transaction.price).label("value_change"),
            )
            .filter(Transaction.user_id == user_id)
            .group_by(func.date(Transaction.date))
            .order_by("day")
            .all()
        )

        # Convert into chart-ready format
        chart_data = [{"date": str(day), "value": value} for day, value in results]
        return chart_data

    # =============================================================================
    @staticmethod
    def get_position_details(db, user_id: int, symbol: str):
        """
        For a specific stock:
        - net shares owned
        - avg cost
        - total profit/loss
        """

        total_bought = (
            db.query(func.sum(Transaction.quantity * Transaction.price))
            .filter(Transaction.user_id == user_id, Transaction.symbol == symbol, Transaction.type == "BUY")
            .scalar() or 0.0
        )

        total_qty_bought = (
            db.query(func.sum(Transaction.quantity))
            .filter(Transaction.user_id == user_id, Transaction.symbol == symbol, Transaction.type == "BUY")
            .scalar() or 0.0
        )

        total_sold = (
            db.query(func.sum(Transaction.quantity * Transaction.price))
            .filter(Transaction.user_id == user_id, Transaction.symbol == symbol, Transaction.type == "SELL")
            .scalar() or 0.0
        )

        total_qty_sold = (
            db.query(func.sum(Transaction.quantity))
            .filter(Transaction.user_id == user_id, Transaction.symbol == symbol, Transaction.type == "SELL")
            .scalar() or 0.0
        )

        owned = total_qty_bought - total_qty_sold

        # Compute average cost basis
        avg_cost = total_bought / total_qty_bought if total_qty_bought > 0 else 0.0

        # Get current price = latest transaction price
        latest_price = (
            db.query(Transaction.price)
            .filter(Transaction.user_id == user_id, Transaction.symbol == symbol)
            .order_by(Transaction.date.desc())
            .first()
        )
        current_price = latest_price[0] if latest_price else 0

        # Current position value & profit/loss
        position_value = owned * current_price
        profit_loss = position_value - (owned * avg_cost)

        return {
            "symbol": symbol,
            "shares_owned": owned,
            "avg_cost_basis": avg_cost,
            "current_price": current_price,
            "position_value": position_value,
            "total_profit_loss": profit_loss,
        }