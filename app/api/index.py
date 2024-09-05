import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from config.settings import HOT_PEPPER_API_KEY


def index_api(request: HttpRequest) -> HttpResponse:
    if not request.method == "POST":
        return redirect("index")

    area = request.POST.get("area")

    url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

    params = {
        "key": HOT_PEPPER_API_KEY,
        "address": area,
        "count": 20,
        "format": "json",
    }

    res = requests.get(url, params=params)
    res_json = res.json()

    shops = res_json["results"]["shop"]
    shop_ids = [shop["id"] for shop in shops]
    shop_id_queries = "&".join([f"shop_ids={shop_id}" for shop_id in shop_ids])

    redirect_url = f"/select/?{shop_id_queries}"

    return redirect(redirect_url)
