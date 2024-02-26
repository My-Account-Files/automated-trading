from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.decorators import api_view
from rest_framework.response import Response

#  < -- User Settings --->
@login_required(login_url='/signin')
def user_settings(request):

    context={ "brokersData": [], "disableBrokersName": [] }
    current_user = request.user
    if request.method == 'GET':
        broker_setting_enabled("zerodha", current_user, context)
        broker_setting_enabled("icici", current_user, context)
        return render(request, 'pages/settings.html', context)
    elif request.method == 'POST':
        setting_updated = False
        broker_name = request.POST.get('broker_name')
        broker_settings = BrokerSetting.objects.filter(user=current_user, broker_name=broker_name).first()

        api_key = request.POST.get('api_key')
        secret_key = request.POST.get('secret_key')

        if broker_settings is None and api_key is not None and secret_key is not None:
          broker_settings = BrokerSetting.objects.create(user=current_user, broker_name=broker_name, api_key=api_key, api_secret=secret_key)
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


# <---- Dashboard --->
def dashboard(request):
    return render(request, 'pages/dashboard.html')

#  < -- SIGN UP --->
def signup(request):
    context={ }
    if request.method == 'POST':
        email = request.POST.get('email')
        username = email.split('@')[0]
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        password = request.POST.get('password')

        if email_exist(email):
            messages.error(request, "Email already exists!")
            return render(request, 'pages/signup.html')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
        send_verification_code(user)
        context['code_send'] = True
        context['hidden_email'] = email
        messages.success(request, "Verification code has been sent")
            
    return render(request, 'pages/signup.html', context)



def email_exist(email):
    return User.objects.filter(email=email).exists()


def send_verification_code(user):
    verification_code = ''.join(random.choices('1234567890', k=6))
    user_details = UserDetail.objects.get(user=user)
    user_details.otp = verification_code
    user_details.save()
    subject = "Verification Code"
    message = f'Your verification code is: {verification_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(e)

#  < -- SIGN IN --->

def signin(request):
    context={}
    if request.method == "POST":
        email  = request.POST.get('email')
        password = request.POST.get('password')
        username = email.split('@')[0]
        current_user = User.objects.filter(username=username)
        if current_user.exists():
            current_user = current_user.first()
            auth_user = authenticate(username=current_user.username, password=password)
            if auth_user is None:
                messages.error(request, "Invalid username or password")
            else:
                send_verification_code(auth_user)
                context['code_send'] = True
                context['hidden_email'] = email
                messages.success(request, "Verification code has been sent")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'pages/signin.html', context)



def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get('hidden_email')
        current_user = User.objects.get(email=email)
        current_user_details = UserDetail.objects.get(user=current_user)
        if request.method == 'POST':
            otp = request.POST.get('code')
            if current_user_details.otp == otp:
                messages.success(request, "User verified!")
                if current_user_details.is_verified == False:
                    current_user_details.is_verified = True
                current_user_details.otp = ''
                current_user_details.save()
                login(request, current_user)
                return redirect('/dashboard/')
            else:
                current_user_details.otp = ''
                current_user_details.save()
                messages.error(request, "Invalid OTP! Login again")
                return redirect('/signin/')


def index(request):
    return render(request, 'pages/landing.html')


def broker_setting_enabled(broker_name, current_user, context):
    broker_setting = BrokerSetting.objects.filter(user=current_user, broker_name=broker_name).first()
    if broker_setting is not None:
        broker_setting.api_key = BrokerSetting.decrypt_data(broker_setting.api_key, b'g6stRwKJ9xVVWhmUh8p8AuyCJdPS8XrTXqfcYG9DEOQ=')
        broker_setting.api_secret = BrokerSetting.decrypt_data(broker_setting.api_secret, b'g6stRwKJ9xVVWhmUh8p8AuyCJdPS8XrTXqfcYG9DEOQ=')
        context["brokersData"].append(broker_setting)
    else:
        context["disableBrokersName"].append(broker_name)

@receiver(post_save, sender=User)
def create_userdetails(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)
