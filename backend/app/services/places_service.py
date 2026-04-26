# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("RAPIDAPI_KEY")
# PLACES_HOST = os.getenv("PLACES_API_HOST")

# BASE_URL = f"https://{PLACES_HOST}"

# HEADERS = {
#     "x-rapidapi-key": API_KEY,
#     "x-rapidapi-host": PLACES_HOST
# }


# def fetch_places(destination: str):
#     try:
#         url = f"{BASE_URL}/FindPlaceByText"

#         params = {
#             "text": f"tourist attractions in {destination}",
#             "language": "en"
#         }

#         response = requests.get(
#             url,
#             headers=HEADERS,
#             params=params,
#             timeout=20
#         )

#         response.raise_for_status()

#         data = response.json()

#         results = data.get("results", [])

#         if not results:
#             return ["City exploration"]

#         activities = []

#         for place in results[:5]:
#             name = place.get("name")
#             if name:
#                 activities.append(name)

#         return activities if activities else ["City exploration"]

#     except Exception as e:
#         print("[Places Error]", e)
#         return ["City exploration"]

import os
import requests
from dotenv import load_dotenv
from app.cache import get_cache, set_cache

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
PLACES_HOST = os.getenv("PLACES_API_HOST")

BASE_URL = f"https://{PLACES_HOST}"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": PLACES_HOST
}


def fetch_places(destination: str):
    try:
        cache_key = f"places:{destination}"

        # Try cache first
        cached = get_cache(cache_key)
        if cached:
            return cached

        url = f"{BASE_URL}/FindPlaceByText"

        params = {
            "text": f"tourist attractions in {destination}",
            "language": "en"
        }

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()
        results = data.get("results", [])

        if not results:
            activities = ["City exploration"]
            set_cache(cache_key, activities)
            return activities

        activities = []

        for place in results[:5]:
            name = place.get("name")
            if name:
                activities.append(name)

        if not activities:
            activities = ["City exploration"]

        # Save cache
        set_cache(cache_key, activities, ttl=3600)

        return activities

    except requests.exceptions.Timeout:
        print("[Places Error] Request timed out")
        return ["City exploration"]

    except requests.exceptions.HTTPError as e:
        print("[Places HTTP Error]", e)
        return ["City exploration"]

    except requests.exceptions.ConnectionError:
        print("[Places Connection Error]")
        return ["City exploration"]

    except Exception as e:
        print("[Places Error]", e)
        return ["City exploration"]