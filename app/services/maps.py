import googlemaps

from config.settings import GOOGLE_API_KEY

mapsClient = googlemaps.Client(key=GOOGLE_API_KEY)


def get_location(address: str) -> dict:
    geocode_result = mapsClient.geocode(address)
    location = geocode_result[0]["geometry"]["location"]

    return location


def get_places(location: dict, radius: int, keyword: str) -> list:
    places = mapsClient.places_nearby(
        location=location, radius=radius, keyword=keyword, language="ja"
    )

    return places["results"]


def generate_place_info(place: dict) -> str:
    name = place["name"]
    id = place["place_id"]
    address = place["vicinity"]

    return f"""
    {name} (ID: {id})
    {address}
    """


def get_place_detail(place_id: str) -> dict:
    place = mapsClient.place(place_id=place_id, language="ja")

    return place["result"]
