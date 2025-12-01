# TODO: FastAPI app initialization, include routers, CORS middleware, create DB tables

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import auth_routes, user_routes, portfolio_routes


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Stock Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(portfolio_routes.router)

@app.get("/")
async def root():
    return {"message": "Backend is running"}



