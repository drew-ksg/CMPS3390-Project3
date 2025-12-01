# TODO: POST /api/user/transactions - add transaction (requires auth)
# TODO: GET /api/user/transactions - list all user transactions (requires auth)
# TODO: GET /api/user/holdings - calculate current holdings (requires auth)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas import TransactionCreate, TransactionResponse, HoldingResponse
from ..controllers.user_controller import UserController
from ..dependencies import get_current_user
from ..models import User

router = APIRouter(prefix="/api/user", tags=["user"])

# Add transaction
@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def add_transaction(
    transaction: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return UserController.add_transaction(db, current_user.username, transaction)


# Get all user transactions
@router.get("/transactions", response_model=List[TransactionResponse])
def list_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return UserController.get_user_transactions(db, current_user.id)


# Get holdings
@router.get("/holdings", response_model=List[HoldingResponse])
def get_holdings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return UserController.get_user_holdings(db, current_user.id)
