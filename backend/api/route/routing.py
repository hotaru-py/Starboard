import os

from dotenv import load_dotenv
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import FileResponse
from opencage.geocoder import OpenCageGeocode
try:
    from backend.api.service.models import Factors, Locations
    from backend.api.service.route_gen import get_optimal_route
except ModuleNotFoundError:
    # we wont reach this block when running in a venv
    # but we're sometimes not able to import backend.api.{something}, for some reason
    # importing api.{something} works, though
    from api.service.models import Factors, Locations
    from api.service.route_gen import get_optimal_route

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


@router.get("/get-ship-route")
async def get_ship_route():
    save_directory = os.path.split(os.path.abspath(__file__))[0]
    save_path = os.path.join(save_directory, "route.png")
    get_optimal_route(locations_storage, save_path)
    return FileResponse(path=save_path, media_type="image/png", filename="route.png")


def setup(app):
    app.include_router(router, prefix=prefix)
