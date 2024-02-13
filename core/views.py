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



#  < -- SIGN UP --->
def signup(request):
    context={}
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

#  < -- Dashboard --->
def dashboard(request):
    return render(request, 'pages/dashboard.html')

#  < -- User Settings --->
def user_settings(request):
    print("Request Method is:" + request.method)
    
    if request.method == 'GET':
        return render(request, 'pages/settings.html')
    elif request.method == 'POST':
        zerodha_api_key = request.data.get('zerodha_api_key')
        zerodha_secret_key = request.data.get('zerodha_secret_key')
        return Response({"message": "This is a POST request"})

def market_data(request):
    return render(request, 'pages/market-data.html')

def reports(request):
    return render(request, 'pages/comingsoon.html')

def alerts(request):
    return render(request, 'pages/comingsoon.html')
    

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



@receiver(post_save, sender=User)
def create_userdetails(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)
