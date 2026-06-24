import requests


def get_coordinates(city):

    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"

    headers = {
        "User-Agent": "SmartTourismProject"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    if len(data) > 0:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])

        return lat, lon

    return None


def get_route_details(start_city, end_city):

    start = get_coordinates(start_city)
    end = get_coordinates(end_city)

    if not start or not end:
        return None

    start_lat, start_lon = start
    end_lat, end_lon = end

    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
        f"?overview=full&steps=true"
    )

    response = requests.get(url)

    data = response.json()

    if data["code"] != "Ok":
        return None

    route = data["routes"][0]

    distance = route["distance"] / 1000
    duration = route["duration"] / 60

    roads = []
    seen = set()

    for leg in route["legs"]:
        for step in leg["steps"]:

            road = step.get("name", "").strip()

            if road and road not in seen:
                roads.append(road)
                seen.add(road)

    return {
        "distance": distance,
        "duration": duration,
        "roads": roads
    }