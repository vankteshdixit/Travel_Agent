import asyncio
from app.services.skyscanner_service import fetch_flights


async def search_flights(
    origin: str,
    destination: str,
    travel_date,
    days: int,
    budget: str
):
    return await asyncio.to_thread(
        fetch_flights,
        origin,
        destination,
        travel_date
    )