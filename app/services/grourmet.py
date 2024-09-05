import requests

from config.settings import HOT_PEPPER_API_KEY

from ..constants import HOT_PEPPER_API_BASEURL


def get_restaurants(params: dict) -> list:
    request_url = HOT_PEPPER_API_BASEURL + "gourmet/v1/"
    params = {
        **params,
        "key": HOT_PEPPER_API_KEY,
        "count": 20,
        "format": "json",
    }

    res = requests.get(request_url, params=params)
    res_json = res.json()

    shops = res_json["results"]["shop"]

    return shops


def get_gourmet_genres() -> list:
    request_url = HOT_PEPPER_API_BASEURL + "genre/v1/"
    params = {
        "key": HOT_PEPPER_API_KEY,
        "format": "json",
    }

    res = requests.get(request_url, params=params)
    res_json = res.json()

    genres = res_json["results"]["genre"]

    return genres


def generate_gourmet_info(shop: dict) -> str:
    name = shop["name"]
    catch = shop["catch"]
    id = shop["id"]
    address = shop["address"]
    station = shop["station_name"]
    genre = shop["genre"]["name"]

    return f"""
    {name} (ID: {id})
    {catch}
    {genre} / 最寄り:{station}
    {address}
    """
