from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

class State(TypedDict, total = False):
    destination:str
    days: int
    budget: str

    plan: str
    flights: List[str]
    hotels: List[str]
    itinerary: str

# graph node 1
def plan_trip(state: State):
    destination = state["destination"]
    days = state["days"]

    state["plan"] = f"{days}-day trip to {destination}"
    return state

# graph node 2
def search_flights(state: State):
    destination = state["destination"]

    state["flights"] = [
        f"Flight to {destination} - ₹5000",
        f"Flight to {destination} - ₹6500",
        f"Flight to {destination} - ₹8500",
    ]
    return state

# graph node 3
def search_hotels(state:State):
    destination = state["destination"]

    state["hotels"] = [
        f"{destination} Luxury Stay - ₹6000/night",
        f"{destination} Beach Resort - ₹4500/night",
        f"{destination} Budget Inn - ₹2500/night",
    ]
    return state

# the actual prompt to get the travel easy
def generate_itinerary(state: State):
    prompt = f"""
You are an expert AI travel planner. Generate a structured itinerary.

Destination: {state['destination']}
Days: {state['days']}
Budget: {state['budget']}

Flights: {state['flights']}

Hotels: {state['hotels']}

Return format:

Day 1:
- activities
- food recommendation
- travel tip

Day 2:
...

Estimated budget summary
"""
    response = llm.invoke(prompt)
    state["itinerary"] = response.content
    return state

# Build graph
builder = StateGraph(State)

builder.add_node("plan", plan_trip)
builder.add_node("flights", search_flights)
builder.add_node("hotels", search_hotels)
builder.add_node("itinerary", generate_itinerary)

builder.set_entry_point("plan")

builder.add_edge("plan", "flights")
builder.add_edge("flights", "hotels")
builder.add_edge("hotels", "itinerary")

graph = builder.compile()