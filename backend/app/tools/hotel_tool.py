import asyncio
from datetime import date
from app.services.booking_service import fetch_hotel


async def search_hotels(
    destination: str,
    checkin_date: date,
    checkout_date: date
):
    return await asyncio.to_thread(
        fetch_hotel,
        destination,
        checkin_date,
        checkout_date
    )