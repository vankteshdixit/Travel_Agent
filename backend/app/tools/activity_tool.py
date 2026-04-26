from typing import List

def get_activities(destination: str) -> List[str]:
    data = {
        "Goa": [
            "Beach hopping",
            "Water sports",
            "Night market",
            "Seafood dining",
        ],
        "Tokyo": [
            "Shibuya Crossing",
            "Temple visit",
            "Anime district",
            "Sushi experience",
        ],
    }

    return data.get(destination, ["City exploration"])