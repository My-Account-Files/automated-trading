from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from core.models import *
# Create your views here.

#  < -- Market Data --->
@login_required(login_url='/signin')
def market_data(request):
    return render(request, 'pages/market-data.html')

@login_required(login_url='/signin')
def market_data_form(request):
    context = {}
    broker_setting = BrokerSetting.objects.filter(user=request.user, broker_name="Zerodha")
    if not broker_setting.exists():
        messages.error(request, "Please add API KEYS in settings")
        return redirect('/trade/market_data')    
    broker_list = [instance.broker_name for instance in broker_setting]
    broker_setting = broker_setting.first()
    try:
        master_instrument_list = MasterInstrumentList.objects.get(broker_setting=broker_setting)
        context['master_instrument_list']=master_instrument_list
    except Exception as e:
        # Call for fetching master_instrument_list
        pass

    context = {'brokers_list':broker_list}
    return render(request, 'pages/market_data_form.html')


def fetch_ohlcv_data(request):
    if request.method == "POST":
        pass
    