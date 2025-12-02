# TODO: Business logic - create_user, get_user_by_username, add_transaction, get_user_transactions, get_user_holdings (aggregate BUY/from
from sqlalchemy.orm import Session
from ..models import User, Transaction, TransactionType
from ..schemas import UserCreate, TransactionCreate, HoldingResponse
from ..auth import get_password_hash
from typing import List

class UserController:

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        hashed_user_password = get_password_hash(user.password)
        db_user = User(
            username=user.username, 
            email=user.email, 
            hashed_password=hashed_user_password
            )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def add_transaction(db: Session, username: str, transaction: TransactionCreate) -> Transaction:
        user = UserController.get_user_by_username(db, username)
        if not user:
            raise ValueError("User not found")
        db_transaction = Transaction(
            user_id=user.id,
            symbol=transaction.symbol,
            type=transaction.type,
            quantity=transaction.quantity,
            price=transaction.price
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    
    @staticmethod
    def get_user_transactions(db: Session, user_id: int) -> List[Transaction]:
        return db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    
    @staticmethod
    def get_user_holdings(db: Session, user_id: int) -> List[HoldingResponse]:
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
        holdings = {}

        for transaction in transactions:
            symbol=  transaction.symbol

            if symbol not in holdings:
                holdings[symbol] = {
                    "quantity": 0,
                    "cost": 0.0
                }

            if transaction.type == TransactionType.BUY:
                holdings[symbol]["quantity"] += transaction.quantity
                holdings[symbol]["cost"] += transaction.quantity * transaction.price

            elif transaction.type == TransactionType.SELL:
                holdings[symbol]["quantity"] -= transaction.quantity
                if holdings[symbol]["quantity"] > 0:
                    avg_cost = holdings[symbol]["cost"] / (holdings[symbol]["quantity"] + transaction.quantity)
                    holdings[symbol]["cost"] -= avg_cost * transaction.quantity
                else:
                    holdings[symbol]["cost"] = 0
        return [
            HoldingResponse(
                    symbol=symbol,
                    total_quantity=data["quantity"],
                    average_price=(data["cost"] / data["quantity"]) if data["quantity"] > 0 else 0.0,
                    total_cost=data["cost"]
                )
                for symbol, data in holdings.items()
                if data["quantity"] > 0
            ]
                    

                    

        