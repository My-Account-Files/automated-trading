from django.urls import path
from .views import *

urlpatterns = [
    path('api/signin/',  signin , name="signin"),
    path('api/signup/',  signup , name="signup"),
    path('api/verify_otp/', verify_and_login, name="verify_otp"),
]
