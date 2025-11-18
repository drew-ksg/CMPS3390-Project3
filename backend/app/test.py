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