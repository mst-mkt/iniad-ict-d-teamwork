from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..services.dateplan import create_date_plan_with_rag
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

    date_plan = create_date_plan_with_rag(
        spots, restaurants, weather_info, "デートプラン"
    )

    print(date_plan)

    context = {"shops": restaurants, "message": date_plan}

    return render(request, "pages/dateplan.html", context)
