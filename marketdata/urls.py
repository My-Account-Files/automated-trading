from django.urls import path, include
from .views import *

urlpatterns = [
    path('market_data/', market_data, name="market_data"),
]
