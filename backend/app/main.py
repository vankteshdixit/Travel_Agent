from fastapi import FastAPI, HTTPException
from app.agent import graph
from app.schema import TripRequest, TripResponse

app = FastAPI(title="AI Travel Planner API")

@app.post("/trip-request", response_model=TripResponse)
def trip_request(request: TripRequest):
    try:
        result = graph.invoke(request.dict())
        return result
    
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def root():
    return {"message": "Travel AI Agent Running"}
