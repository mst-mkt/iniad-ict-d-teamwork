import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from config.settings import HOT_PEPPER_API_KEY


def select_view(request: HttpRequest) -> HttpResponse:
    shop_ids = request.GET.getlist("shop_ids")
    request_url = "https://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

    print(shop_ids)

    params = {
        "key": HOT_PEPPER_API_KEY,
        "id": shop_ids,
        "count": 20,
        "format": "json",
    }

    res = requests.get(request_url, params=params)
    res_json = res.json()

    shops = res_json["results"]["shop"]

    return render(request, "pages/select.html", {"shops": shops})
