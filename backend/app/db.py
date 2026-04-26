from pymongo import MongoClient
from datetime import datetime


# Mongo connection
client = MongoClient(
    "mongodb://localhost:27017"
)

db = client["travel_ai"]

trips_collection = db["trips"]


def save_trip(data: dict):
    try:
        data["created_at"] = datetime.utcnow()

        result = trips_collection.insert_one(data)

        print(
            f"[Mongo Saved] {result.inserted_id}"
        )

        return str(result.inserted_id)

    except Exception as e:
        print("[Mongo Save Error]", e)
        return