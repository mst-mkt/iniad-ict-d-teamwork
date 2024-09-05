from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..services.grourmet import get_shops


def select_view(request: HttpRequest) -> HttpResponse:
    area = request.GET.get("area")
    genre = request.GET.get("genre")
    params = {"address": area, **({"genre": genre} if genre else {})}
    shops = get_shops(params)

    return render(request, "pages/select.html", {"shops": shops})
