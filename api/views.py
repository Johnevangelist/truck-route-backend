import csv
import json
from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .ors import geocode, get_route

# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "fuel-prices-for-be-assessment.csv"

# ---------- Load fuel stations ONCE ----------
STATIONS = []
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        STATIONS.append({
            "id": r["OPIS Truckstop ID"],
            "name": r["Truckstop Name"],
            "address": r["Address"],
            "city": r["City"],
            "state": r["State"],
            "price": float(r["Retail Price"]),
        })


@csrf_exempt
def fuel_plan(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        data = json.loads(request.body)
        start_city = data["start"]
        end_city = data["end"]
    except Exception:
        return JsonResponse(
            {"error": "Body must contain { start, end }"},
            status=400
        )

    # ---------- Geocode ----------
    start_coords = geocode(start_city)
    end_coords = geocode(end_city)

    # ---------- Get route (ONE ORS CALL) ----------
    route_data = get_route(start_coords, end_coords)

    summary = route_data["features"][0]["properties"]["summary"]

    distance_miles = round(summary["distance"] / 1609.34, 2)
    duration_hours = round(summary["duration"] / 3600, 2)

    # ---------- Fuel math ----------
    MPG = 10
    MAX_RANGE = 500

    gallons_used = distance_miles / MPG
    avg_price = sum(s["price"] for s in STATIONS) / len(STATIONS)
    estimated_fuel_cost = round(gallons_used * avg_price, 2)

    stops_required = max(1, int(distance_miles // MAX_RANGE))

    recommended_stops = sorted(
        STATIONS, key=lambda x: x["price"]
    )[:stops_required]

    # ---------- FINAL RESPONSE ----------
    return JsonResponse({
        "start": start_city,
        "end": end_city,
        "distance_miles": distance_miles,
        "estimated_fuel_cost": estimated_fuel_cost,
        "route": {
            "distance_miles": distance_miles,
            "duration_hours": duration_hours,
        },
        "fuel_stops": recommended_stops,
    })
