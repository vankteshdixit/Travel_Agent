# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("OPENWEATHER_API_KEY")


# def fetch_weather(city: str) -> str:
#     try:
#         url = "https://api.openweathermap.org/data/2.5/weather"

#         params = {
#             "q": city,
#             "appid": API_KEY,
#             "units": "metric"
#         }

#         response = requests.get(url, params=params, timeout=10)
#         response.raise_for_status()

#         data = response.json()

#         weather = data["weather"][0]["main"]
#         temp = data["main"]["temp"]

#         return f"{weather}, {temp}°C"

#     except Exception as e:
#         print("Weather API error:", e)
#         return "Weather unavailable"

import os
import requests
from dotenv import load_dotenv
from app.cache import get_cache, set_cache

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def fetch_weather(city: str) -> str:
    try:
        cache_key = f"weather:{city}"

        # Try cache first
        cached = get_cache(cache_key)
        if cached:
            return cached

        url = "https://api.openweathermap.org/data/2.5/weather"

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        weather = data["weather"][0]["main"]
        temp = data["main"]["temp"]

        result = f"{weather}, {temp}°C"

        # Save cache
        set_cache(cache_key, result, ttl=1800)

        return result

    except requests.exceptions.Timeout:
        print("[Weather Error] Request timed out")
        return "Weather unavailable"

    except requests.exceptions.HTTPError as e:
        print("[Weather HTTP Error]", e)
        return "Weather unavailable"

    except requests.exceptions.ConnectionError:
        print("[Weather Connection Error]")
        return "Weather unavailable"

    except Exception as e:
        print("[Weather Error]", e)
        return "Weather unavailable"