from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.hashers import check_password
from .jwtauth import *

@api_view(['POST'])
def signup(request):
    email  = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    
    if not email or not password or not first_name:
        json_response = {"message":"Email and password are required"}
        return Response(json_response, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.filter(email=email)
    if user.exists():
        json_response = {"message":"Email already registered"}
        return Response(json_response, status=status.HTTP_409_CONFLICT)
    else:
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, is_active=False)
        send_verification_code(user)

        json_response = {"message":"User registered succesfully. OTP sent!"}
        return Response(json_response, status=status.HTTP_200_OK)


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



@api_view(['POST'])
def verify_and_login(request):
    otp = request.data.get('otp')
    email = request.data.get('email')
    user = User.objects.get(email=email)
    user_details = UserDetail.objects.get(user=user)

    if otp:
        if user_details.otp == otp:
            user_details.otp=''
            user.is_active = True
            user_details.save()
            user.save()
            login(request, user)
            jwt_token = generate_access_token(user.id)
            json_response = {"message":"User login succesfully!","jwt_token":jwt_token}
            return Response(json_response, status=status.HTTP_200_OK)
        else:
            json_response = {"message":"Invalid OTP!"}
            return Response(json_response, status=status.HTTP_401_UNAUTHORIZED)
        


@api_view(['POST'])
def signin(request):
    email  = request.data.get('email')
    password = request.data.get('password')

    # token = request.data.get('token')
    # user = get_current_user(token)
    # if not user:
    #     json_response = {"message":"InValid token!"}
    #     return Response(json_response, status=status.HTTP_401_UNAUTHORIZED)
    # else:
    #     json_response = {"message":"Valid token!","email":user.email}
    #     return Response(json_response, status=status.HTTP_200_OK)

    if not email or not password:
        json_response = {"message":"Email and password are required"}
        return Response(json_response, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=email, password=password)
    user = User.objects.get(username=email)
    user_verified = check_password(password, user.password) 
    if not user_verified:
        json_response = {"message":"Invalid username or password"}
        return Response(json_response, status=status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        json_response = {"message":"User not verified!"}
        return Response(json_response, status=status.HTTP_403_FORBIDDEN)
    else:
        send_verification_code(user)
        json_response = {"message":"User authenticated. OTP sent!"}
        return Response(json_response, status=status.HTTP_200_OK)
    