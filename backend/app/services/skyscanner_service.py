import os
import time
import requests
from dotenv import load_dotenv
from app.cache import get_cache, set_cache

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = os.getenv("RAPIDAPI_HOST")

BASE_URL = f"https://{API_HOST}"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}


def search_airport(query: str):
    try:
        url = f"{BASE_URL}/flights/searchAirport"

        response = requests.get(
            url,
            headers=HEADERS,
            params={
                "query": query,
                "market": "IN",
                "locale": "en-US"
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()
        places = data.get("places", [])

        if not places:
            return None

        first = places[0]

        return {
            "skyId": first["skyId"],
            "entityId": first["entityId"],
            "iataCode": first.get("iataCode"),
            "name": first["name"]
        }

    except Exception as e:
        print("[Airport Search Error]", e)
        return None


def fetch_flights(origin: str, destination: str, travel_date):
    try:
        travel_date_str = travel_date.isoformat()

        # Redis cache key
        cache_key = (
            f"flight:"
            f"{origin}:"
            f"{destination}:"
            f"{travel_date_str}"
        )

        # Try cache first
        cached = get_cache(cache_key)
        if cached:
            return cached

        origin_data = search_airport(origin)
        destination_data = search_airport(destination)

        if not origin_data or not destination_data:
            flights = [
                {
                    "airline": "No flights available",
                    "origin": origin,
                    "destination": destination,
                    "departure": None,
                    "arrival": None,
                    "duration_minutes": None,
                    "stops": None,
                    "price": None,
                    "currency": None
                }
            ]

            set_cache(cache_key, flights)
            return flights

        url = f"{BASE_URL}/flights/searchFlights"

        params = {
            "originSkyId": origin_data["skyId"],
            "originEntityId": origin_data["entityId"],
            "destinationSkyId": destination_data["skyId"],
            "destinationEntityId": destination_data["entityId"],
            "date": travel_date_str,
            "adults": 1,
            "children": 0,
            "infants": 0,
            "cabinClass": "economy",
            "currency": "INR",
            "market": "IN",
            "countryCode": "IN"
        }

        for attempt in range(3):
            try:
                response = requests.get(
                    url,
                    headers=HEADERS,
                    params=params,
                    timeout=30
                )

                print("\n===== FLIGHT API DEBUG =====")
                print("Attempt:", attempt + 1)
                print("Status:", response.status_code)
                print("Body:", response.text[:1000])
                print("============================\n")

                response.raise_for_status()

                data = response.json()
                itineraries = data.get("itineraries", [])

                if not itineraries:
                    break

                flights = []

                for itinerary in itineraries[:5]:
                    try:
                        price = itinerary.get("price", {})
                        legs = itinerary.get("legs", [])

                        if not legs:
                            continue

                        leg = legs[0]

                        carrier = "Unknown"
                        carriers = leg.get("carriers", [])

                        if carriers:
                            carrier = carriers[0].get("name", "Unknown")

                        flights.append({
                            "airline": carrier,
                            "origin": leg.get("origin"),
                            "destination": leg.get("destination"),
                            "departure": leg.get("departure"),
                            "arrival": leg.get("arrival"),
                            "duration_minutes": leg.get("durationMinutes"),
                            "stops": leg.get("stopCount"),
                            "price": price.get("amount"),
                            "currency": price.get("currency")
                        })

                    except Exception as parse_error:
                        print("[Flight Parse Error]", parse_error)
                        continue

                if flights:
                    set_cache(cache_key, flights)
                    return flights

            except Exception as e:
                print(f"[Retry {attempt + 1} Failed]", e)
                time.sleep(1)

        flights = [
            {
                "airline": "No flights available",
                "origin": origin,
                "destination": destination,
                "departure": None,
                "arrival": None,
                "duration_minutes": None,
                "stops": None,
                "price": None,
                "currency": None
            }
        ]

        set_cache(cache_key, flights)
        return flights

    except Exception as e:
        print("[Flight Search Error]", e)

        flights = [
            {
                "airline": "Flight service unavailable",
                "origin": origin,
                "destination": destination,
                "departure": None,
                "arrival": None,
                "duration_minutes": None,
                "stops": None,
                "price": None,
                "currency": None
            }
        ]

        return flights