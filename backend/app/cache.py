import json
import redis

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def get_cache(key: str):
    try:
        data = redis_client.get(key)

        if data:
            print(f"[CACHE HIT] {key}")
            return json.loads(data)

        print(f"[CACHE MISS] {key}")
        return None

    except Exception as e:
        print("[Redis GET Error]", e)
        return None


def set_cache(key: str, value, ttl=1800):
    try:
        redis_client.setex(
            key,
            ttl,
            json.dumps(value)
        )

        print(f"[CACHE SET] {key}")

    except Exception as e:
        print("[Redis SET Error]", e)