from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('signin/', signin, name="signin"),
    path('signup/', signup, name="signup"),
    path('verify_otp/', verify_otp, name="verify_otp"),
    path('user_settings/', user_settings, name="user_settings"),
    path('dashboard/', dashboard, name="dashboard"),
    path('trade/', include('marketdata.urls')),

]
