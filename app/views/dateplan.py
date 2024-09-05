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
    query = request.GET.get("query")

    restaurants = get_restaurants({"id": restaurant_ids})
    spots = [get_place_detail(spot_id) for spot_id in spot_ids]

    location = get_location(area)
    weather_info = get_weather(location)

    date_plan = create_date_plan_with_rag(spots, restaurants, weather_info, query)

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

    return render(request, "pages/dateplan.html", {"date_plan": date_plan_info})
