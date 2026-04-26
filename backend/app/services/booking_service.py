import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
BOOKING_HOST = os.getenv("BOOKING_API_HOST")

BASE_URL = f"https://{BOOKING_HOST}"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": BOOKING_HOST
}


def search_hotel_destination(city: str):
    try:
        url = f"{BASE_URL}/api/v1/hotels/searchDestination"

        params = {
            "query": city
        }

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()
        destinations = data.get("data", [])

        if not destinations:
            print(f"[Hotel Destination] No destination found for {city}")
            return None

        first = destinations[0]

        return {
            "dest_id": first.get("dest_id"),
            "search_type": first.get("dest_type")
        }

    except requests.exceptions.Timeout:
        print("[Hotel Destination Error] Request timed out")
        return None

    except requests.exceptions.HTTPError as e:
        print("[Hotel Destination HTTP Error]", e)
        return None

    except requests.exceptions.ConnectionError:
        print("[Hotel Destination Connection Error]")
        return None

    except Exception as e:
        print("[Hotel Destination Error]", e)
        return None


def fetch_hotel(destination: str, checkin_date, checkout_date):
    try:
        dest = search_hotel_destination(destination)

        if not dest:
            return [{
                "name": "No hotels found",
                "rating": None,
                "reviews": None,
                "stars": None,
                "price": None,
                "currency": None
            }]

        url = f"{BASE_URL}/api/v1/hotels/searchHotels"

        params = {
            "dest_id": dest["dest_id"],
            "search_type": dest["search_type"],
            "arrival_date": checkin_date.isoformat(),
            "departure_date": checkout_date.isoformat(),
            "adults": 1,
            "room_qty": 1,
            "page_number": 1,
            "units": "metric",
            "temperature_unit": "c",
            "languagecode": "en-us",
            "currency_code": "INR"
        }

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        hotels_data = data.get("data", {}).get("hotels", [])

        if not hotels_data:
            return [{
                "name": "No hotels available",
                "rating": None,
                "reviews": None,
                "stars": None,
                "price": None,
                "currency": None
            }]

        hotels = []

        for hotel in hotels_data[:5]:
            try:
                prop = hotel.get("property", {})

                price_breakdown = (
                    prop.get("priceBreakdown")
                    or hotel.get("priceBreakdown")
                    or {}
                )

                gross_price = price_breakdown.get("grossPrice", {})
                excluded_price = price_breakdown.get("excludedPrice", {})
                display_price = price_breakdown.get("priceDisplay", {})

                price = (
                    gross_price.get("value")
                    or excluded_price.get("value")
                    or display_price.get("amount")
                    or display_price.get("price")
                    or None
                )

                currency = (
                    gross_price.get("currency")
                    or excluded_price.get("currency")
                    or "INR"
                )

                stars = (
                    prop.get("propertyClass")
                    or prop.get("accuratePropertyClass")
                    or None
                )

                if stars == 0:
                    stars = None

                hotels.append({
                    "name": prop.get("name", "Unknown Hotel"),
                    "rating": prop.get("reviewScore"),
                    "reviews": prop.get("reviewCount"),
                    "stars": stars,
                    "price": price,
                    "currency": currency
                })

            except Exception as parse_error:
                print("[Hotel Parse Error]", parse_error)
                continue

        if not hotels:
            return [{
                "name": "No hotels available",
                "rating": None,
                "reviews": None,
                "stars": None,
                "price": None,
                "currency": None
            }]

        return hotels

    except requests.exceptions.Timeout:
        print("[Hotel Search Error] Request timed out")
        return [{
            "name": "Hotel service timeout",
            "rating": None,
            "reviews": None,
            "stars": None,
            "price": None,
            "currency": None
        }]

    except requests.exceptions.HTTPError as e:
        print("[Hotel Search HTTP Error]", e)
        return [{
            "name": "Hotel service unavailable",
            "rating": None,
            "reviews": None,
            "stars": None,
            "price": None,
            "currency": None
        }]

    except requests.exceptions.ConnectionError:
        print("[Hotel Search Connection Error]")
        return [{
            "name": "Hotel service unavailable",
            "rating": None,
            "reviews": None,
            "stars": None,
            "price": None,
            "currency": None
        }]

    except Exception as e:
        print("[Hotel Search Error]", e)
        return [{
            "name": "Hotel service unavailable",
            "rating": None,
            "reviews": None,
            "stars": None,
            "price": None,
            "currency": None
        }]