from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..services.grourmet import get_restaurants
from ..services.maps import get_location, get_places
from ..services.weather import get_weather


def select_view(request: HttpRequest) -> HttpResponse:
    area = request.GET.get("area")
    genre = request.GET.get("genre")

    restaurant_param = {"address": area, **({"genre": genre} if genre else {})}
    restaurants = get_restaurants(restaurant_param)

    location = get_location(area)
    spots = get_places(location, 5000, "デートスポット")
    weather = get_weather(location)

    return render(
        request,
        "pages/select.html",
        {
            "area": area,
            "restaurants": restaurants,
            "spots": spots,
            "weather": weather["weather"][0],
        },
    )
