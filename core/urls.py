from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('signin/', signin, name="signin"),
    path('signup/', signup, name="signup"),
    path('verify_otp/', verify_otp, name="verify_otp"),
    path('dashboard/', dashboard, name="dashboard"),
    path('user_settings/', user_settings, name="user_settings"),
    path('market_data/', market_data, name="market_data"),
    path('reports/', reports, name="reports"),
    path('alerts/', alerts, name="alerts"),
]
