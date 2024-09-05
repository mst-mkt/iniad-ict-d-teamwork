import requests
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from langchain_openai import ChatOpenAI

from config.settings import HOT_PEPPER_API_KEY


def dateplan_view(request: HttpRequest) -> HttpResponse:
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

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        streaming=True,
        openai_api_base="https://api.openai.iniad.org/api/v1/",
    )

    prompt = f"あなたはデートプランナーです。以下のお店を参考にして、デートプランを提案してください。\n\n - {shops[0]['name']} - {shops[0]['address']}\n - {shops[1]['name']} - {shops[1]['address']}\n - {shops[2]['name']} - {shops[2]['address']}\n\nデートプラン："

    response = model.invoke(prompt)
    print(response)

    context = {
        "shops": shops,
        "message": response,
    }

    return render(request, "pages/dateplan.html", context)
