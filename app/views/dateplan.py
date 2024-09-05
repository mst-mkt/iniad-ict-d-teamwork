from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from langchain_openai import ChatOpenAI

from ..constants import OPENAI_API_BASEURL
from ..services.grourmet import get_restaurants
from ..services.maps import get_place_detail


def dateplan_view(request: HttpRequest) -> HttpResponse:
    restaurant_ids = request.GET.getlist("restaurant_id")
    spot_ids = request.GET.getlist("spot_id")

    restaurants = get_restaurants({"id": restaurant_ids})
    spots = [get_place_detail(spot_id) for spot_id in spot_ids]

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        streaming=True,
        openai_api_base=OPENAI_API_BASEURL,
    )

    prompt = f"""
あなたはデートプランナーです。
以下のレストランとスポットを使ってデートプランを作成してください。

レストラン:
{"\n\n".join([f"{r['name']} ({r['address']})" for r in restaurants])}

スポット:
{"\n\n".join([f"{s['name']} ({s['vicinity']})" for s in spots])}
"""

    response = model.invoke(prompt)
    print(response)

    context = {
        "shops": restaurants,
        "message": response,
    }

    return render(request, "pages/dateplan.html", context)
