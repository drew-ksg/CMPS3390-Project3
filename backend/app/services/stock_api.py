import requests
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from ..config import get_settings

settings = get_settings()


last_request: datetime | None = None

class API:
    Base_URL = "https://api.massive.com/v1"
    API_Key = settings.API_KEY
    
    @staticmethod
    def get_stock_price(symbol: str) -> dict:
        global last_request
        now = datetime.now(timezone.utc)
        
        if last_request and (now - last_request) < timedelta(minutes=1):
            seconds_left = int((timedelta(minutes=1) - (now - last_request)).total_seconds())
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Try again in {seconds_left} seconds."
            )
        
        url = f"{API.Base_URL}/open-close/{symbol}/{now.strftime('%Y-%m-%d')}?adjusted=true&apiKey={API.API_Key}"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Massive API error: {response.text}"
            )

        last_request = now

        return response.json()
