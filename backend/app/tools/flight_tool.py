from app.services.skyscanner_service import fetch_flights


def search_flights(
    origin: str,
    destination: str,
    travel_date,
    days: int,
    budget: str
):
    return fetch_flights(
        origin,
        destination,
        travel_date
    )