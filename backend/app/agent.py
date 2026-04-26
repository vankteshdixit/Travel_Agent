from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from datetime import date, timedelta
import asyncio

from app.cache import get_cache, set_cache
from app.db import save_trip
from app.tools.flight_tool import search_flights
from app.tools.hotel_tool import search_hotels
from app.tools.weather_tool import get_weather
from app.tools.activity_tool import get_activities

load_dotenv()


# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)


class State(TypedDict, total=False):
    origin: str
    destination: str
    travel_date: date
    days: int
    budget: str

    plan: str
    flights: List[Dict[str, Any]]
    hotels: List[Dict[str, Any]]
    weather: str
    activities: List[str]
    itinerary: str


# Node 1
def plan_trip(state: State):
    state["plan"] = (
        f"{state['days']}-day trip "
        f"from {state['origin']} "
        f"to {state['destination']}"
    )
    return state


# Node 2 -> Parallel execution
def fetch_all_data(state: State):
    checkout_date = (
        state["travel_date"] +
        timedelta(days=state["days"])
    )

    async def run_parallel():
        flights_task = search_flights(
            state["origin"],
            state["destination"],
            state["travel_date"],
            state["days"],
            state["budget"]
        )

        hotels_task = search_hotels(
            state["destination"],
            state["travel_date"],
            checkout_date
        )

        weather_task = get_weather(
            state["destination"]
        )

        activities_task = get_activities(
            state["destination"]
        )

        return await asyncio.gather(
            flights_task,
            hotels_task,
            weather_task,
            activities_task
        )

    flights, hotels, weather, activities = asyncio.run(
        run_parallel()
    )

    state["flights"] = flights
    state["hotels"] = hotels
    state["weather"] = weather
    state["activities"] = activities

    return state


# Node 3 -> Generate itinerary
def generate_itinerary(state: State):

    # FINAL TRIP CACHE
    trip_cache_key = (
        f"trip:"
        f"{state['origin']}:"
        f"{state['destination']}:"
        f"{state['travel_date']}:"
        f"{state['days']}:"
        f"{state['budget']}"
    )

    cached_trip = get_cache(trip_cache_key)

    if cached_trip:
        state["itinerary"] = cached_trip
        return state

    # Flights formatting
    if state.get("flights"):
        flight_text = "\n".join([
            (
                f"{f.get('airline')} | "
                f"{f.get('origin')} → {f.get('destination')} | "
                f"₹{f.get('price')} {f.get('currency')} | "
                f"Stops: {f.get('stops')} | "
                f"Departure: {f.get('departure')}"
            )
            for f in state["flights"]
        ])
    else:
        flight_text = "No flights available"

    # Hotels formatting
    if state.get("hotels"):
        hotel_text = "\n".join([
            (
                f"{h.get('name')} | "
                f"⭐ {h.get('rating')} | "
                f"Reviews: {h.get('reviews')} | "
                f"Stars: {h.get('stars') or 'N/A'} | "
                f"₹{h.get('price')} {h.get('currency')}"
            )
            for h in state["hotels"]
        ])
    else:
        hotel_text = "No hotels available"

    # Activities formatting
    if state.get("activities"):
        activity_text = "\n".join([
            f"- {activity}"
            for activity in state["activities"]
        ])
    else:
        activity_text = "No activities available"

    prompt = f"""
You are an expert AI travel planner.

Create a detailed itinerary.

Origin: {state['origin']}
Destination: {state['destination']}
Travel Date: {state['travel_date']}
Days: {state['days']}
Budget: {state['budget']}
Weather: {state['weather']}

Flights:
{flight_text}

Hotels:
{hotel_text}

Activities:
{activity_text}

Return format:

Day 1:
- activities
- food suggestions
- travel tips

Day 2:
- activities
- food suggestions
- travel tips

Continue for all days.

At end give:
1. Budget summary
2. Best hotel recommendation
3. Best flight recommendation
4. Important travel notes
"""

    response = llm.invoke(prompt)

    itinerary = response.content

    state["itinerary"] = itinerary

    # SAVE TO MONGODB
    save_trip({
        "origin": state["origin"],
        "destination": state["destination"],
        "travel_date": str(state["travel_date"]),
        "days": state["days"],
        "budget": state["budget"],
        "flights": state["flights"],
        "hotels": state["hotels"],
        "weather": state["weather"],
        "activities": state["activities"],
        "itinerary": itinerary
    })

    # SAVE FINAL TRIP CACHE
    set_cache(
        trip_cache_key,
        itinerary,
        ttl=3600
    )

    return state


# Build graph
builder = StateGraph(State)

builder.add_node("plan", plan_trip)
builder.add_node("fetch_all", fetch_all_data)
builder.add_node("itinerary", generate_itinerary)

builder.set_entry_point("plan")

builder.add_edge("plan", "fetch_all")
builder.add_edge("fetch_all", "itinerary")

graph = builder.compile()