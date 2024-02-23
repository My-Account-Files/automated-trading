from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

#  < -- Dashboard --->
def dashboard(request):
    return render(request, 'pages/dashboard.html')

#  < -- User Settings --->
@login_required(login_url='/signin')
def user_settings(request):
    
    if request.method == 'GET':
        return render(request, 'pages/settings.html')
    elif request.method == 'POST':
        current_user = request.user
        print(request.user)
        user_broker_settings = BrokerSetting.objects.filter(user=current_user)

        if not user_broker_settings.exists():
            user_broker_settings = BrokerSetting.objects.create(user=current_user)
        zerodha_api_key = request.POST.get('zerodha_api_key')
        zerodha_secret_key = request.POST.get('zerodha_secret_key')

        if zerodha_api_key is not None and zerodha_secret_key is not None:
          zerodha_broker_settings = BrokerSetting.objects.filter(user=current_user, broker_name="zerodha")
        if not zerodha_broker_settings.exists():
          zerodha_broker_settings = BrokerSetting.objects.create(user=current_user, api_key=zerodha_api_key, api_secret=zerodha_secret_key)
        else:
            zerodha_broker_settings.update()

    return render(request, 'pages/settings.html')
        

def market_data(request):
    return render(request, 'pages/market-data.html')

def reports(request):
    return render(request, 'pages/comingsoon.html')

def alerts(request):
    return render(request, 'pages/comingsoon.html')
    