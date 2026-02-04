import csv
import json
from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .ors import geocode
from .orsm import get_route

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "fuel-prices-for-be-assessment.csv"

# Load fuel stations once
STATIONS = []
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        STATIONS.append({
            "id": r["OPIS Truckstop ID"],
            "name": r["Truckstop Name"],
            "city": r["City"],
            "state": r["State"],
            "price": float(r["Retail Price"]),
        })


@csrf_exempt
def fuel_plan(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = json.loads(request.body)
        start_city = body["start"]
        end_city = body["end"]
    except Exception:
        return JsonResponse(
            {"error": "Body must contain { start, end }"},
            status=400
        )

    try:
        # 1️⃣ Geocode
        start_coords = geocode(start_city)
        end_coords = geocode(end_city)

        # 2️⃣ Route via OSRM
        route = get_route(start_coords, end_coords)

    except Exception as e:
        return JsonResponse(
            {"error": "Routing failed", "details": str(e)},
            status=400
        )

    # Distance & duration
    distance_miles = round(route["distance"] / 1609.34, 2)
    duration_hours = round(route["duration"] / 3600, 2)

    # Fuel calculation
    MPG = 10
    MAX_RANGE = 500

    gallons_used = distance_miles / MPG
    avg_price = sum(s["price"] for s in STATIONS) / len(STATIONS)
    estimated_fuel_cost = round(gallons_used * avg_price, 2)

    stops_required = max(1, int(distance_miles // MAX_RANGE))
    cheapest_stops = sorted(STATIONS, key=lambda x: x["price"])[:stops_required]

    return JsonResponse({
        "start": start_city,
        "end": end_city,
        "distance_miles": distance_miles,
        "duration_hours": duration_hours,
        "estimated_fuel_cost": estimated_fuel_cost,
        "fuel_stops": cheapest_stops,
    })
