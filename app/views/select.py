from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..services.grourmet import get_shops


def select_view(request: HttpRequest) -> HttpResponse:
    area = request.GET.get("area")
    shops = get_shops({"address": area})

    return render(request, "pages/select.html", {"shops": shops})
