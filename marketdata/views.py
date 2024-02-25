from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        context={}
        setting_updated = False
        current_user = request.user
        broker_name = request.POST.get('broker_name')
        broker_settings = BrokerSetting.objects.filter(user=current_user, broker_name=broker_name).first()

        api_key = request.POST.get('api_key')
        secret_key = request.POST.get('secret_key')

        if broker_settings is None and api_key is not None and secret_key is not None:
          zerodha_broker_settings = BrokerSetting.objects.create(user=current_user, broker_name=broker_name, api_key=api_key, api_secret=secret_key)
          setting_updated = True
        elif broker_settings is not None and api_key is not None and secret_key is not None:
            broker_settings.api_key=api_key
            broker_settings.api_secret=secret_key
            broker_settings.save()
            setting_updated = True

        if bool(setting_updated):
            messages.success(request, "Setting has been updated")

        zerodha_broker_settings = BrokerSetting.objects.filter(user=current_user, broker_name="zerodha").first()
        icici_broker_settings = BrokerSetting.objects.filter(user=current_user, broker_name="icici").first()
        context= {'zerodha_broker_settings': zerodha_broker_settings, 'icici_broker_settings': icici_broker_settings}

    return render(request, 'pages/settings.html', context)
        

def market_data(request):
    return render(request, 'pages/market-data.html')

def reports(request):
    return render(request, 'pages/comingsoon.html')

def alerts(request):
    return render(request, 'pages/comingsoon.html')



def enable_broker_settings(broker_settings):
    if broker_settings is None:
        return False

    if broker_setting.broker_name == "zerodha":
        return bool(broker_settings.enable_zerodha)
    elif broker_setting.broker_name == "icici":
        return bool(broker_settings.enable_icici)

    