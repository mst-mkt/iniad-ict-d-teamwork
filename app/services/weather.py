import requests

from config.settings import OPENWEATHER_API_KEY

from ..constants import OPENWEATHER_API_BASEURL


def get_weather(location: dict) -> dict:
    params = {
        "lat": location["lat"],
        "lon": location["lng"],
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ja",
    }

    res = requests.get(OPENWEATHER_API_BASEURL, params=params)
    res_json = res.json()

    return res_json
