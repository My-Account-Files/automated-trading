from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

        
def market_data(request):
    return render(request, 'pages/market-data.html')


    