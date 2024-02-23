from django.urls import path, include
from .views import *

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('user_settings/', user_settings, name="user_settings"),
    path('market_data/', market_data, name="market_data"),
    path('reports/', reports, name="reports"),
    path('alerts/', alerts, name="alerts"),
]
