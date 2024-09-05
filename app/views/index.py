from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from ..services.grourmet import get_gourmet_genres


def index_view(request: HttpRequest) -> HttpResponse:
    restaurant_genres = get_gourmet_genres()
    return render(request, "pages/index.html", {"genres": restaurant_genres})
