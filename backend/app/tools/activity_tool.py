import asyncio
from typing import List
from app.services.places_service import fetch_places


async def get_activities(destination: str) -> List[str]:
    return await asyncio.to_thread(
        fetch_places,
        destination
    )

