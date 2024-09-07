import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import importlib

from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

API_PREFIX = "/api"


app = FastAPI(openapi_prefix=API_PREFIX)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

backend_path = os.path.split(__file__)[0]
routes_path = os.path.join(backend_path, "api", "route")

routes = [x.rstrip(".py") for x in os.listdir(routes_path) if x.endswith(".py") and not x.startswith("_")]


for route in routes:
    # dynamically import all routes which are defined in "backend/api/route/"
    print("Importing route from:", os.path.join(routes_path, route))
    try:
        importlib.util.spec_from_file_location(route, os.path.join(routes_path, route))
        module = importlib.import_module(f"api.route.{route}")
        module.setup(app)
        print("Added Route:", route)
    except Exception as e:
        print("Failed:", type(e).__name__)
        print(e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)