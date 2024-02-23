from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('signin/', signin, name="signin"),
    path('signup/', signup, name="signup"),
    path('verify_otp/', verify_otp, name="verify_otp"),
    path('trade/', include('marketdata.urls')),

]
