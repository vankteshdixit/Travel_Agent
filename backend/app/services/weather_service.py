import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_weather(city: str) -> str:
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]

        return f"{weather}, {temp}°C"

    except Exception as e:
        print("Weather API error:", e)
        return "Weather unavailable"