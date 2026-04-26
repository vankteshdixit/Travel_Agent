from app.services.weather_service import fetch_weather


def get_weather(destination: str) -> str:
    return fetch_weather(destination)