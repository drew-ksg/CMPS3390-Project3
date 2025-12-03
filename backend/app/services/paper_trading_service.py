from sqlalchemy import func
from ..models import Transaction, Holding, TransactionType


class PaperTradingService:
    """Handles paper trading validation and execution"""

    INITIAL_CASH = 100000.0  # Users start with $100k virtual cash

    @staticmethod
    def get_cash_balance(db, user_id: int):
        """Calculate available cash."""

        buy_total = (
            db.query(func.sum(Transaction.quantity * Transaction.price))
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.BUY
            )
            .scalar()
        ) or 0.0

        sell_total = (
            db.query(func.sum(Transaction.quantity * Transaction.price))
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.SELL
            )
            .scalar()
        ) or 0.0

        return PaperTradingService.INITIAL_CASH - buy_total + sell_total

    @staticmethod
    def validate_buy_order(cash_balance: float, quantity: float, price: float):
        return cash_balance >= quantity * price

    @staticmethod
    def validate_sell_order(db, user_id: int, symbol: str, quantity: float):
        holding = (
            db.query(Holding)
            .filter(Holding.user_id == user_id, Holding.symbol == symbol)
            .first()
        )
        return holding is not None and holding.quantity >= quantity

    @staticmethod
    def execute_trade(db, user_id: int, symbol: str, trade_type: str, quantity: float, price: float):
        """Executes a trade, updates transactions + holdings."""

        cash_balance = PaperTradingService.get_cash_balance(db, user_id)

        # Validate buy
        if trade_type == "BUY":
            if not PaperTradingService.validate_buy_order(cash_balance, quantity, price):
                return {"success": False, "message": "Insufficient cash."}
            tx_type = TransactionType.BUY

        # Validate sell
        elif trade_type == "SELL":
            if not PaperTradingService.validate_sell_order(db, user_id, symbol, quantity):
                return {"success": False, "message": "Not enough shares."}
            tx_type = TransactionType.SELL

        # Record transaction
        new_tx = Transaction(
            user_id=user_id,
            symbol=symbol,
            type=tx_type,
            quantity=quantity,
            price=price
        )
        db.add(new_tx)

        # Update holdings
        holding = (
            db.query(Holding)
            .filter(Holding.user_id == user_id, Holding.symbol == symbol)
            .first()
        )

        if tx_type == TransactionType.BUY:
            if holding:
                holding.quantity += quantity
            else:
                db.add(Holding(user_id=user_id, symbol=symbol, quantity=quantity))
        else:  # SELL
            holding.quantity -= quantity
            if holding.quantity <= 0:
                db.delete(holding)

        db.commit()

        return {
            "success": True,
            "message": f"{trade_type} executed successfully.",
            "transaction_id": new_tx.id
        }
