import os
import requests
from dotenv import load_dotenv

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")

def geocode(city):
    r = requests.get(
        "https://api.openrouteservice.org/geocode/search",
        params={"text": city, "size": 1},
        headers={
            "Authorization": ORS_API_KEY,
            "Accept": "application/json"
        },
        timeout=10
    )
    r.raise_for_status()

    data = r.json()
    return data["features"][0]["geometry"]["coordinates"]  # [lon, lat]
