from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from config.settings import GOOGLE_API_KEY

from ..services.dateplan import create_date_plan_with_rag
from ..services.grourmet import get_restaurants
from ..services.maps import get_location, get_place_detail, get_places
from ..services.weather import get_weather


def dateplan_view(request: HttpRequest) -> HttpResponse:
    area = request.GET.get("area")
    genre = request.GET.get("genre")
    restaurant_ids = request.GET.getlist("restaurant_id")
    spot_ids = request.GET.getlist("spot_id")
    query = request.GET.get("query")

    restaurants = get_restaurants({"id": restaurant_ids})
    all_restaurants = get_restaurants(
        {"address": area, **({"genre": genre} if genre else {})}
    )
    spots = [get_place_detail(spot_id) for spot_id in spot_ids]
    all_spots = get_places(get_location(area), 5000, "デートスポット")

    location = get_location(area)
    weather_info = get_weather(location)

    date_plan = create_date_plan_with_rag(
        spots, restaurants, all_spots, all_restaurants, weather_info, query
    )

    date_plan_info = {
        "title": date_plan.title,
        "message": date_plan.message,
        "steps": [
            {
                "type": step.type,
                "id": step.id,
                "from_time": step.from_time,
                "to_time": step.to_time,
                "comment": step.comment,
                "data": get_place_detail(step.id)
                if step.type == "spot"
                else get_restaurants({"id": [step.id]})[0],
            }
            for step in date_plan.steps
        ],
        "advice": date_plan.advice,
    }

    return render(
        request,
        "pages/dateplan.html",
        {"date_plan": date_plan_info, "maps_api_key": GOOGLE_API_KEY},
    )
