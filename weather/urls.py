from django.urls import path
from . import views


urlpatterns = [
    path('search-geo/', views.search_geo),
    path('get-weather/', views.get_weather),
    path('get-stats/', views.get_stats),
]