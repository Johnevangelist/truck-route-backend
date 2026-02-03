import os
import requests

ORS_KEY = os.getenv("ORS_API_KEY")
BASE_URL = "https://api.openrouteservice.org"

def geocode(city):
    url = f"{BASE_URL}/geocode/search"
    params = {
        "api_key": ORS_KEY,
        "text": city,
        "size": 1,
        "boundary.country": "US",
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    coords = r.json()["features"][0]["geometry"]["coordinates"]
    return coords  # [lon, lat]

def get_route(start_coords, end_coords):
    url = f"{BASE_URL}/v2/directions/driving-car/geojson"
    headers = {
        "Authorization": ORS_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "coordinates": [start_coords, end_coords],
        "geometry_simplify": True,
    }
    r = requests.post(url, json=body, headers=headers)
    r.raise_for_status()
    return r.json()
