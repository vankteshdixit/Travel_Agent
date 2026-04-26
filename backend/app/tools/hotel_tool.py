from datetime import date
from app.services.booking_service import fetch_hotel


def search_hotels(
    destination: str,
    checkin_date: date,
    checkout_date: date
):
    return fetch_hotel(
        destination,
        checkin_date,
        checkout_date
    )