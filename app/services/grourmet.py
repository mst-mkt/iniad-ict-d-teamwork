import requests

from config.settings import HOT_PEPPER_API_KEY

from ..constants import HOT_PEPPER_API_BASEURL


def get_shops(params: dict) -> list:
    request_url = HOT_PEPPER_API_BASEURL
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
