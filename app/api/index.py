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
    shop_ids = [f"shop_ids={shop["id"]}" for shop in shops]

    redirect_url = f"/select/?{'&'.join(shop_ids)}"

    return redirect(redirect_url)
