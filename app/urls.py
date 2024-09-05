from django.urls import path

import app.views as views

urlpatterns = [
    path("", views.index.index_view, name="index"),
    path("select/", views.select.select_view, name="select"),
    path("dateplan/", views.dateplan.dateplan_view, name="dateplan"),
]
