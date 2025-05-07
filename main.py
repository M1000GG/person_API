from fastapi import FastAPI
from controller.location_controller import location_router, set_location_service
from service.location_service import LocationService

app = FastAPI()

# Create instance of service
location_service = LocationService("data/DIVIPOLA.csv")
set_location_service(location_service)

app.include_router(location_router)

@app.get("/")
async def root():
    return {"message": "Person API V1"}


