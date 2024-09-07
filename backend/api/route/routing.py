from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from opencage.geocoder import OpenCageGeocode

from backend.api.service.models import Factors, Locations
import os
from dotenv import load_dotenv

router = APIRouter()

prefix = "/routing"

factors_storage = {}
locations_storage = {}

load_dotenv()
API_KEY = os.getenv("API_KEY")

geocoder = OpenCageGeocode(API_KEY)


@router.get("/get-factors")
async def get_factors():
    return factors_storage


@router.get("/get-locations")
async def get_locations():
    return locations_storage


@router.post("/save-factors")
async def save_factors(factors: Factors):
    factors_storage.update(factors.model_dump())
    return {"message": "Factors saved successfully!"}


@router.post("/save-locations")
async def save_locations(locations: Locations):
    try:
        if locations.from_location:
            results_from = geocoder.geocode(locations.from_location)
            if results_from:
                coordinates_from = results_from[0]['geometry']
                locations_storage.update(
                    {"from": {"latitude": coordinates_from["lat"], "longitude": coordinates_from['lng']}})
            else:
                locations_storage.pop("from", None)
        if locations.to_location:
            results_to = geocoder.geocode(locations.to_location)
            if results_to:
                coordinates_to = results_to[0]['geometry']
                locations_storage.update(
                    {"to": {"latitude": coordinates_to["lat"], "longitude": coordinates_to['lng']}})
            else:
                locations_storage.pop("to", None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Locations identified and passed!", "from_coords": coordinates_from, "to_coords": coordinates_to}


def setup(app):
    app.include_router(router, prefix=prefix)
