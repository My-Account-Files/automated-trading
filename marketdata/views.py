from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
# Create your views here.

#  < -- User Settings --->
@login_required(login_url='/signin')
        
def market_data(request):
    return render(request, 'pages/market-data.html')

def market_data_form(request):
    return render(request, 'pages/market_data_form.html')

def alerts(request):
    return render(request, 'pages/comingsoon.html')

    