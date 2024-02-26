from django.urls import path, include
from .views import *

urlpatterns = [
    path('market_data/', market_data, name="market_data"),
    path('market_data_form/', market_data_form, name="market_data_form"),
]
