from typing import TypedDict, List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from datetime import date, timedelta

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


# Node 1 -> basic trip plan
def plan_trip(state: State):
    state["plan"] = (
        f"{state['days']}-day trip "
        f"from {state['origin']} "
        f"to {state['destination']}"
    )
    return state


# Node 2 -> real flights
def search_flights_node(state: State):
    state["flights"] = search_flights(
        state["origin"],
        state["destination"],
        state["travel_date"],
        state["days"],
        state["budget"]
    )
    return state


# Node 3 -> real hotels
def search_hotels_node(state: State):
    checkout_date = state["travel_date"] + timedelta(days=state["days"])

    state["hotels"] = search_hotels(
        state["destination"],
        state["travel_date"],
        checkout_date
    )

    return state


# Node 4 -> weather
def weather_node(state: State):
    state["weather"] = get_weather(state["destination"])
    return state


# Node 5 -> activities
def activity_node(state: State):
    state["activities"] = get_activities(state["destination"])
    return state


# Node 6 -> final itinerary generation
def generate_itinerary(state: State):

    # format flights nicely
    if state.get("flights"):
        flight_text = "\n".join(
            [
                (
                    f"{f['airline']} | "
                    f"{f['origin']} → {f['destination']} | "
                    f"₹{f['price']} {f['currency']} | "
                    f"Stops: {f['stops']} | "
                    f"Departure: {f['departure']}"
                )
                for f in state["flights"]
            ]
        )
    else:
        flight_text = "No flights available"

    # format hotels nicely
    if state.get("hotels"):
        hotel_text = "\n".join(
            [
                (
                    f"{h['name']} | "
                    f"⭐ {h['rating']} | "
                    f"Reviews: {h['reviews']} | "
                    f"Stars: {h['stars']} | "
                    f"₹{h['price']} {h['currency']}"
                )
                for h in state["hotels"]
            ]
        )
    else:
        hotel_text = "No hotels available"

    # format activities nicely
    if state.get("activities"):
        activity_text = "\n".join(
            [f"- {activity}" for activity in state["activities"]]
        )
    else:
        activity_text = "No activities available"

    prompt = f"""
You are an expert travel planner.

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
Budget summary
Best hotel recommendation
Best flight recommendation
"""

    response = llm.invoke(prompt)

    state["itinerary"] = response.content

    return state


# Build graph
builder = StateGraph(State)

builder.add_node("plan", plan_trip)
builder.add_node("flights", search_flights_node)
builder.add_node("hotels", search_hotels_node)
builder.add_node("weather", weather_node)
builder.add_node("activities", activity_node)
builder.add_node("itinerary", generate_itinerary)

builder.set_entry_point("plan")

builder.add_edge("plan", "flights")
builder.add_edge("flights", "hotels")
builder.add_edge("hotels", "weather")
builder.add_edge("weather", "activities")
builder.add_edge("activities", "itinerary")

graph = builder.compile()