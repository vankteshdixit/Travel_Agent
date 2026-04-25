from typing import Optional, List
from pydantic import BaseModel, Field

class TripRequest(BaseModel):
    destination: str = Field(..., examples="Goa")
    days: int = Field(3, ge=1, le=30)
    budget: Optional[str] = Field(None, examples="Budget")

class TripResponse(BaseModel):
    destination: str
    days: int
    budget: Optional[str]

    plan: Optional[str] = None
    flights: Optional[List[str]] = None
    hotels: Optional[List[str]] = None
    itinerary: Optional[str] = None