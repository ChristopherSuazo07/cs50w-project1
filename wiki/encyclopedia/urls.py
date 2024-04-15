from django.urls import path
from django.conf.urls import handler404
from . import util
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name = "wiki"),
    path("new", views.new, name="new"),
    path("random", views.Random, name="random"),
    path("search", views.search, name="search"),
    path("edit/<str:title>",views.edit, name = "edit")
    
]