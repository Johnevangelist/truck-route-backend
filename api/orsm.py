import requests

def get_route(start_coords, end_coords):
    lon1, lat1 = start_coords
    lon2, lat2 = end_coords

    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}"
        f"?overview=false"
    )

    r = requests.get(url, timeout=10)
    r.raise_for_status()

    data = r.json()

    if data["code"] != "Ok":
        raise Exception("OSRM routing failed")

    return data["routes"][0]
