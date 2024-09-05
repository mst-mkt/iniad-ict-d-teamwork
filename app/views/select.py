import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from config.settings import HOT_PEPPER_API_KEY

from ..constants import HOT_PEPPER_API_BASEURL


def select_view(request: HttpRequest) -> HttpResponse:
    shop_ids = request.GET.getlist("shop_ids")
    request_url = HOT_PEPPER_API_BASEURL

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
