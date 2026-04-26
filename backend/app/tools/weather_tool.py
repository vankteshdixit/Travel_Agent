import asyncio
from app.services.weather_service import fetch_weather


async def get_weather(destination: str) -> str:
    return await asyncio.to_thread(
        fetch_weather,
        destination
    )