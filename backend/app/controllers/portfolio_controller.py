from sqlalchemy import func
from ..models import Transaction, Holding, TransactionType
from ..services.paper_trading_service import PaperTradingService


class PortfolioController:
    """Handles portfolio business logic"""

    # =============================================================================
    @staticmethod
    def get_portfolio_summary(db, user_id: int):
        """Return cash balance, portfolio value, and detailed positions."""

        cash_balance = PaperTradingService.get_cash_balance(db, user_id)

        holdings = (
            db.query(Holding)
            .filter(Holding.user_id == user_id)
            .all()
        )

        total_portfolio_value = 0.0
        detailed_positions = []

        for h in holdings:
            # latest price = latest transaction price
            latest_price = (
                db.query(Transaction.price)
                .filter(Transaction.user_id == user_id, Transaction.symbol == h.symbol)
                .order_by(Transaction.date.desc())
                .first()
            )
            current_price = latest_price[0] if latest_price else 0
            position_value = h.quantity * current_price

            detailed_positions.append({
                "symbol": h.symbol,
                "quantity": h.quantity,
                "current_price": current_price,
                "position_value": position_value,
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
        """Return daily trade activity (placeholder for real performance)."""

        results = (
            db.query(
                func.date(Transaction.date).label("day"),
                func.sum(Transaction.quantity * Transaction.price).label("trade_value"),
            )
            .filter(Transaction.user_id == user_id)
            .group_by(func.date(Transaction.date))
            .order_by("day")
            .all()
        )

        return [
            {"date": str(day), "value": value}
            for day, value in results
        ]

    # =============================================================================
    @staticmethod
    def get_position_details(db, user_id: int, symbol: str):
        """Return avg cost, quantity, and P/L for a given stock."""

        # Query holdings table
        holding = (
            db.query(Holding)
            .filter(Holding.user_id == user_id, Holding.symbol == symbol)
            .first()
        )

        if not holding:
            return {
                "symbol": symbol,
                "shares_owned": 0,
                "avg_cost_basis": 0,
                "current_price": 0,
                "position_value": 0,
                "total_profit_loss": 0,
            }

        qty_owned = holding.quantity

        # Compute average cost from transactions
        total_bought_value = (
            db.query(func.sum(Transaction.quantity * Transaction.price))
            .filter(
                Transaction.user_id == user_id,
                Transaction.symbol == symbol,
                Transaction.type == TransactionType.BUY
            )
            .scalar() or 0
        )

        total_bought_qty = (
            db.query(func.sum(Transaction.quantity))
            .filter(
                Transaction.user_id == user_id,
                Transaction.symbol == symbol,
                Transaction.type == TransactionType.BUY
            )
            .scalar() or 0
        )

        avg_cost = total_bought_value / total_bought_qty if total_bought_qty > 0 else 0

        # latest price
        latest_price = (
            db.query(Transaction.price)
            .filter(Transaction.user_id == user_id, Transaction.symbol == symbol)
            .order_by(Transaction.date.desc())
            .first()
        )
        current_price = latest_price[0] if latest_price else 0

        position_value = qty_owned * current_price
        profit_loss = qty_owned * (current_price - avg_cost)

        return {
            "symbol": symbol,
            "shares_owned": qty_owned,
            "avg_cost_basis": avg_cost,
            "current_price": current_price,
            "position_value": position_value,
            "total_profit_loss": profit_loss,
        }
