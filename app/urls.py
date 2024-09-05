from django.urls import path

import app.api.index as index_api
import app.views as views

urlpatterns = [
    path("", views.index.index_view, name="index"),
    path("api/", index_api.index_api, name="index_api"),
    path("select/", views.select.select_view, name="select"),
    path("dateplan/", views.dateplan.dateplan_view, name="dateplan"),
]
