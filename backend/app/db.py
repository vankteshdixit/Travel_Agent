from pymongo import MongoClient
from datetime import datetime


# Mongo connection
client = MongoClient(
    "mongodb://localhost:27017"
)

db = client["travel_ai"]

trips_collection = db["trips"]
users_collection = db["users"]


def save_trip(data: dict):
    try:
        data["created_at"] = datetime.utcnow()

        result = trips_collection.insert_one(
            data
        )

        print(
            f"[Mongo Saved] {result.inserted_id}"
        )

        return str(result.inserted_id)

    except Exception as e:
        print(
            "[Mongo Save Error]",
            e
        )
        return None


def get_user_trips(user_id: str):
    try:
        trips = list(
            trips_collection.find(
                {"user_id": user_id},
                {"_id": 0}
            ).sort(
                "created_at",
                -1
            )
        )

        return trips

    except Exception as e:
        print(
            "[Mongo Read Error]",
            e
        )
        return []


def get_user_by_email(email: str):
    try:
        return users_collection.find_one(
            {"email": email.lower()}
        )

    except Exception as e:
        print(
            "[Mongo User Error]",
            e
        )
        return None