from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from langchain_openai import ChatOpenAI

from ..constants import OPENAI_API_BASEURL
from ..services.grourmet import get_restaurants
from ..services.maps import get_location, get_place_detail
from ..services.weather import get_weather


def dateplan_view(request: HttpRequest) -> HttpResponse:
    area = request.GET.get("area")
    restaurant_ids = request.GET.getlist("restaurant_id")
    spot_ids = request.GET.getlist("spot_id")

    restaurants = get_restaurants({"id": restaurant_ids})
    spots = [get_place_detail(spot_id) for spot_id in spot_ids]

    location = get_location(area)
    weather_info = get_weather(location)
    weather = weather_info["weather"][0]["description"]
    temperature = weather_info["main"]["temp"]
    humidity = weather_info["main"]["humidity"]

    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        streaming=True,
        openai_api_base=OPENAI_API_BASEURL,
    )

    prompt = f"""
あなたはデートプランナーです。
以下のレストランとスポット、天気情報を使ってデートプランを作成してください。

天気情報:
{weather}: 気温は{temperature}度, 湿度は{humidity}%です。

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
        "weather": weather,
    }

    return render(request, "pages/dateplan.html", context)
