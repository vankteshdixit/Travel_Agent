from typing import Optional, List
from datetime import date
from pydantic import BaseModel, Field


class Flight(BaseModel):
    airline: str
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure: Optional[str] = None
    arrival: Optional[str] = None
    duration_minutes: Optional[int] = None
    stops: Optional[int] = None
    price: Optional[float] = None
    currency: Optional[str] = None


class Hotel(BaseModel):
    name: str
    rating: Optional[float] = None
    reviews: Optional[int] = None
    stars: Optional[int] = None
    price: Optional[float] = None
    currency: Optional[str] = None


class TripRequest(BaseModel):
    origin: str = Field(..., example="Bengaluru")
    destination: str = Field(..., example="Lucknow")
    travel_date: date = Field(..., example="2026-06-10")
    days: int = Field(3, ge=1, le=30)
    budget: Optional[str] = Field("medium", example="medium")


class TripResponse(BaseModel):
    origin: str
    destination: str
    travel_date: date
    days: int
    budget: Optional[str]

    plan: Optional[str] = None
    flights: Optional[List[Flight]] = None
    hotels: Optional[List[Hotel]] = None
    itinerary: Optional[str] = None