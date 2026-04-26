from fastapi import (
    FastAPI,
    HTTPException,
    Header,
    Depends
)

from app.agent import graph
from app.schema import TripRequest, TripResponse
from app.routes.auth_routes import router as auth_router
from app.auth import verify_token
from app.db import get_user_trips


app = FastAPI(
    title="AI Travel Planner API"
)

# Register auth routes
app.include_router(auth_router)


def get_current_user(
    authorization: str = Header(None)
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    if not authorization.startswith(
        "Bearer "
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid token format"
        )

    token = authorization.split(" ")[1]

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload


@app.post(
    "/trip-request",
    response_model=TripResponse
)
def trip_request(
    request: TripRequest,
    user=Depends(get_current_user)
):
    try:
        request_data = request.dict()

        request_data["user_id"] = user["sub"]
        request_data["email"] = user["email"]

        result = graph.invoke(
            request_data
        )

        return result

    except Exception as e:
        print("ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/my-trips")
def my_trips(
    user=Depends(get_current_user)
):
    trips = get_user_trips(
        user["sub"]
    )

    return {
        "count": len(trips),
        "trips": trips
    }


@app.get("/")
def root():
    return {
        "message": "Travel AI Agent Running"
    }