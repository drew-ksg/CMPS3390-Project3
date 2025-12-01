""" Testing config file
from config import get_settings

settings = get_settings()
print(f" SECRET_KEY: {settings.SECRET_KEY[:10]}...")
print(f" DATABASE_URL: {settings.DATABASE_URL}")
print(f" ALGORITHM: {settings.ALGORITHM}")
print(f" Token expires in: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} min")
"""
""" Testing database file 
from backend.app.database import engine, Base, SessionLocal, get_db
from backend.app.config import get_settings

settings = get_settings()
print(f"Database URL: {settings.DATABASE_URL}")
print(f"Engine: {engine}")
print(f"Base class: {Base}")
print(f"SessionLocal: {SessionLocal}")
print(f"get_db function: {get_db}") 
"""
"""Testing models file
from backend.app.models import User, Transaction, TransactionType
print(f"\n User table name: {User.__tablename__}")
print(f" Transaction table name: {Transaction.__tablename__}")

print(f"\n TransactionType.BUY: {TransactionType.BUY}")
print(f" TransactionType.SELL: {TransactionType.SELL}")
"""
""" Testing schemas file
from backend.app.schemas import (
    UserCreate, UserResponse, Token, LoginRequest,
    TransactionCreate, TransactionResponse, HoldingResponse
)
print(f"UserCreate fields: {UserCreate.model_fields.keys()}")
print(f"TransactionCreate fields: {TransactionCreate.model_fields.keys()}")
"""
""" Testing auth file 
from backend.app.auth import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    decode_access_token
)
# Test password hashing
password = "mypassword123"
hashed = get_password_hash(password)
print(f"Original password: {password}")
print(f"Hashed password: {hashed[:30]}...")
print(f"Verify correct password: {verify_password(password, hashed)}")
print(f"Verify wrong password: {verify_password('wrongpass', hashed)}")

# Test JWT token
token = create_access_token(data={"sub": "testuser"})
print(f"JWT Token: {token[:50]}...")
username = decode_access_token(token)
print(f"Decoded username: {username}")
print(f" Type: {type(username)}")

"""
""" Testing dependencies file 
from backend.app.dependencies import get_current_user, security
print(f"Security object: {security}")
print(f"get_current_user function: {get_current_user}")
"""
""" Testing user controller file 
from backend.app.controllers.user_controller import UserController
print(f"UserController class: {UserController}")    
methods = [
    'create_user',
    'get_user_by_username',
    'get_user_by_email',
    'add_transaction',
    'get_user_transactions',
    'get_user_holdings'
]
print("Methods:")
for method in methods:
    if hasattr(UserController, method):
        print(f"{method}")
    else:
        print(f"{method} - MISSING!")
"""
""" Testing auth routes file 
from backend.app.routes.auth_routes import router
print(f"Router: {router}")
print(f"Prefix: {router.prefix}")
print(f"Tags: {router.tags}")
print(f"Routes: {[route.path for route in router.routes]}")
"""
""" Testing user routes file 
from backend.app.routes.user_routes import router
print(f"\n Router: {router}")
print(f"Prefix: {router.prefix}")
print(f"Tags: {router.tags}")
print(f"Routes: {[f'{route.methods} {route.path}' for route in router.routes]}")
"""