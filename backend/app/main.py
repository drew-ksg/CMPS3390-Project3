# TODO: FastAPI app initialization, include routers, CORS middleware, create DB tables

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import auth_routes, user_routes, portfolio_routes


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Stock Tracker API", version="1.0.0")

templates = Jinja2Templates(directory="backend/app/templates")

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

@app.get("/status")
async def root():
    return {"message": "Backend is running"}

#Views
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})   




