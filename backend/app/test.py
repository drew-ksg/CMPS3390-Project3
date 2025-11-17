from config import get_settings

settings = get_settings()
print(f" SECRET_KEY: {settings.SECRET_KEY[:10]}...")
print(f" DATABASE_URL: {settings.DATABASE_URL}")
print(f" ALGORITHM: {settings.ALGORITHM}")
print(f" Token expires in: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} min")