from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.views.generic.base import TemplateView
import random, requests, json
from rest_framework import status
from .renderers import UserRenderer
from home.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from .serializers import  UserChangePasswordSerializer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
import random

    
def get_or_createToken(request):
    """ 
    Create a user access token for already logged in user
    """
    if request.user.is_authenticated  :
        user = CustomUser.objects.get(email = request.user.email)
        token = get_tokens_for_user(user)
        request.session['access_token'] = token['access']
        return request.session['access_token']
    else:
        return False

def get_tokens_for_user(user):
    """ 
    Get a token access for already logged in user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
      

class UserRegistrationView(APIView):
    """ 
    An api view for user registration and return error if these is any error or not provided insufficient data
    """
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if not request.data['email'] :
                return Response({'msg':'email field is required'}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    """ 
    send an username and exist user's password to get user's accesstoken.
    """
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = CustomUser.objects.get(email = email)
        if user.check_password(password)  :
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    """ 
    Get a user profile data with email and password
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    """ 
    Change user password
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

    

from django.core.mail import send_mail

class send_email(APIView):

    def post(self, request, format=None):

        subject = 'Hello, Django Email'
        message = 'This is a test email sent from a Django application.'
        from_email = 'info@keywordlit.com'
        recipient_list = ['rikenkhadela85@gmail.com']   

        send_mail(subject, message, from_email, recipient_list)
        return Response({"Email sent successfully."},status=status.HTTP_200_OK)