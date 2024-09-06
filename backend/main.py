# import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from opencage.geocoder import OpenCageGeocode
from dotenv import load_dotenv
import os
from route_gen import get_optimal_route

# Did not gitignore .env since repo is private.
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Factors(BaseModel):
    slider1: int
    slider2: int
    slider3: int
    slider4: int
    slider5: int

class Locations(BaseModel):
    from_location: str
    to_location: str
    
factors_storage = {}
locations_storage = {}

@app.post("/api/save-factors")
async def save_factors(factors: Factors):
    factors_storage.update(factors.model_dump())
    return {"message": "Factors saved successfully!"}

@app.post("/api/save-locations")
async def save_locations(locations: Locations):
    geocoder = OpenCageGeocode(API_KEY)
    try:
        if locations.from_location:
            results_from = geocoder.geocode(locations.from_location)
            if results_from:
                coordinates_from = results_from[0]['geometry']
                locations_storage.update({"from": {"latitude": coordinates_from["lat"], "longitude": coordinates_from['lng']}})
            else:
                locations_storage.pop("from", None)
        if locations.to_location:
            results_to = geocoder.geocode(locations.to_location)
            if results_to:
                coordinates_to = results_to[0]['geometry']
                locations_storage.update({"to": {"latitude": coordinates_to["lat"], "longitude": coordinates_to['lng']}})
            else:
                locations_storage.pop("to", None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Locations saved successfully!", "from_coords": coordinates_from, "to_coords": coordinates_to}

@app.get("/api/get-factors")
async def get_factors():
    return factors_storage

@app.get("/api/get-locations")
async def get_locations():
    return locations_storage

@app.get("/api/get-ship-route")
async def get_ship_route():
    get_optimal_route(locations_storage)
    return FileResponse(path="route.png", media_type="image/png", filename="route.png")