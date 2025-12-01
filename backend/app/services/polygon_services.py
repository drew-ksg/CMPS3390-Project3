import requests
from functools import lru_cache  # caching to prevent rate limits
from ..config import get_settings

settings = get_settings()

class PolygonService:
    BASE_URL = "https://api.polygon.io"

    # ========================= REAL-TIME QUOTE =========================
    @staticmethod
    @lru_cache(maxsize=128)  # Cache response (prevents rate limits)
    def get_stock_quote(symbol: str):
        """Get real-time stock quote."""
        url = f"{PolygonService.BASE_URL}/v2/last/nbbo/{symbol.upper()}"
        params = {"apiKey": settings.API_KEY}

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {"error": "Failed to fetch stock quote"}
        
        data = response.json()
        if "results" not in data:
            return {"error": "No quote data found"}

        return {
            "symbol": symbol.upper(),
            "price": data["results"]["p"],  # last trade price
            "timestamp": data["results"]["t"]
        }

    # ====================== HISTORICAL PRICES ==========================
    @staticmethod
    @lru_cache(maxsize=128)
    def get_historical_data(symbol: str, from_date: str, to_date: str):
        """Get OHLC historical data (candlesticks)."""
        url = f"{PolygonService.BASE_URL}/v2/aggs/ticker/{symbol.upper()}/range/1/day/{from_date}/{to_date}"
        params = {"apiKey": settings.API_KEY}

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {"error": "Failed to fetch historical data"}

        data = response.json()
        if "results" not in data:
            return {"error": "No historical data found"}

        # Format for charting
        candles = [
            {
                "date": result["t"],  # timestamp
                "open": result["o"],
                "high": result["h"],
                "low": result["l"],
                "close": result["c"],
                "volume": result["v"],
            }
            for result in data["results"]
        ]

        return candles
