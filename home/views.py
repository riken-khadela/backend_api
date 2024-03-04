import random, requests, json
from rest_framework import status
from .renderers import UserRenderer
from home.models import CustomUser, SearchedHistory, instagram_accounts, DepositeMoney
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from .serializers import  UserChangePasswordSerializer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
import random, dotenv
from django.http import JsonResponse
from .utils import GetActiveChromeSelenium, get_yt_trend_data, scrape_hashtags,get_user_id_from_token, generate_random_string, get_search_history, get_search_history_
import random, time, os, json, pytz
from .bot import Bot
from datetime import timedelta, datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from urllib.parse import unquote
from django.db.models import Sum
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .insta import main_call, get_hashtags
import time
import re
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import AllowAny
from .serializers import UserChangePasswordSerializer
from .models import CustomUser
from .email import send_otp_via_email
from .email import *
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
import concurrent.futures
import yaml
import urllib.parse
import langdetect
from django.db.models import Q


user_driver_dict = {}

from rest_framework.permissions import BasePermission

def IsSuperUser(user_id):
    user = CustomUser.objects.filter(id=user_id)
    if not user : return False, False
    user = user.first()
    return user , user.is_superuser
    
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
        if not 'username' in request.data :
            while True :
                genrated_random_username =  generate_random_string(15)
                if CustomUser.objects.filter(username=genrated_random_username).count() == 0 :
                    request.data['username'] = genrated_random_username
                    break
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.data['email'] :
            return Response({'Message':'email field is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        if 'super' in request.data and request.data['super'] == True : 
            user.is_superuser = True
            user.save()
        #token = get_tokens_for_user(user)
        verification_code = random.randint(100000,999999)
        user.verification_code = verification_code
        user.save()
        subject = 'Verification code is here'
        message = f'verification code : {verification_code}'
        from_email = 'info@keywordlit.com'
        recipient_list = [user.email]   
        send_mail(subject, message, from_email, recipient_list)            
        #return Response({'token':token, "email" : 'email verification code has been set' ,'msg':'Registration succesful'}, status=status.HTTP_201_CREATED)
        return Response({"email" : 'Email verification code has been set' ,'Message':'Verify your account'}, status=status.HTTP_201_CREATED)

#---------------------------------------------------------UserEmailVerification By Riken--------------------------------------------------------

# class UserEmailVerificationView(APIView):
#     """ 
#     To verify user needs to send email and verification 
#     """
#     def post(self, request):
#         email = request.data.get('email')
#         verification_code = request.data.get('verification_code')

#         user = CustomUser.objects.filter(email=email, verification_code=verification_code).first()
#         if user :
#             user.is_user_verified = True
#             user.save()
#             return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
#         else :
#             try :
#                 verification_code = random.randint(100000,999999)
#                 user.verification_code = verification_code
#                 user.save()
#                 subject = 'Verification code is here'
#                 message = f'verification code : {verification_code}'
#                 from_email = 'info@keywordlit.com'
#                 recipient_list = [email]   
#                 send_mail(subject, message, from_email, recipient_list) 
#                 send_verification_code = True
#             except : 
#                 send_verification_code = False

#             return Response({'message': 'Invalid verification code.','ResendVerificationCode' : send_verification_code}, status=status.HTTP_400_BAD_REQUEST)
#---------------------------------------------------------UserEmailVerification By Riken--------------------------------------------------------

#---------------------------------------------------------UserEmailVerification By Adil--------------------------------------------------------
    
class UserEmailVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        # Check if required fields are provided
        if not email or not verification_code:
            return Response({'Message': 'Please provide the following details', 'details': {'email': 'Email', 'verification_code': 'Verification code'}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)

            if user.is_user_verified == True:
                # If user is already verified, return a message indicating so
                return Response({'Message': 'User is already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            
             # Check if verification code is a valid number
            if not verification_code.isdigit():
                return Response({'Message': 'Invalid Verification Code.'}, status=status.HTTP_400_BAD_REQUEST)

            if str(user.verification_code) == verification_code:
                user.is_user_verified = True
                token = get_tokens_for_user(user)
                verification_code = random.randint(100000, 999999)# Extra Code added to change the code after Process because same code will be used multiple times ex- same code will be used to chnage password.
                user.verification_code = verification_code# Extra Code added to change the code after Process because same code will be used multiple times ex- same code will be used to chnage password.
                user.save()
                return Response({'token':token,'Message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
            else:
                # If verification code is incorrect, resend verification code
                #verification_code = random.randint(100000, 999999)
                #user.verification_code = verification_code
                #user.save()
                #send_otp_via_email(email)  # Now Resend verification code via email will not be send Instaed call Resend OTP API
                return Response({'Message': 'Verification code is incorrect. Resent verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            # If email is not in records, prompt user to register first
            return Response({'Message': 'Email not in records. Please register first.'}, status=status.HTTP_400_BAD_REQUEST)

#---------------------------------------------------------UserEmailVerification By Adil--------------------------------------------------------
 
#---------------------------------------------------------Resend OTP API by ADIL----------------------------------------------------------------

class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'Message':  {"email": 'Please provide an email address.'}}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            verification_code = random.randint(100000, 999999)
            user.verification_code = verification_code
            user.save()
            # Call the function to send OTP via email
            send_otp_via_email(email)
            return Response({'Message': 'New verification code sent successfully.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'Message': 'Email not found in records. Register First'}, status=status.HTTP_404_NOT_FOUND)


#---------------------------------------------------------Resend OTP APY by ADIL---------------------------------------------------------------




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
        #user = CustomUser.objects.get(email = email)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # If the email is not found in records, return a 404 NotFound response
            return Response({'Message': {'non_field_errors': ['Email not in record. Register First!']}}, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password)  :
            token = get_tokens_for_user(user)
            if user.is_user_verified:
                return Response({'token':token,'verified' : user.is_user_verified, 'Message':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'verified' : user.is_user_verified, 'Message':'Verify your account First!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Message':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class RefreshTokenView(APIView):
    """
    Send a refresh token to get a new access token.
    """
    def post(self, request, format=None):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'Message': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = refresh_token.access_token
        except Exception as e:
            return Response({'Message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'access_token': str(access_token)}, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):
    """ 
    Get a user profile data with email and password
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        search_history = []
        user_id = get_user_id_from_token(request)
        user = CustomUser.objects.filter(id=user_id).first()
        
        for history in SearchedHistory.objects.filter(user=user) :
#-------------------------Code to fetch the error in the section---------------------------------------------------
            try:
                # Attempt to load the JSON data, replacing single quotes with double quotes
                result_json = json.loads(history.result.replace("'", '"'))
            except json.JSONDecodeError as e:
                # Handle JSON decoding errors, for example by skipping the problematic entry
                print(f"Error decoding JSON for history ID {history.id}: {e}")
                print(f"Error decoding JSON for history platform {history.platform}: {e}")
                print(f"Error decoding JSON for history hashtag {history.hashtag}: {e}")
                print(f"Error decoding JSON for history date {history.created}: {e}")
                continue
#-------------------------Code to fetch the error in the section---------------------------------------------------
            tmp = {
                'platform' : history.platform,
                'hashtag' : history.hashtag,
                'date' : history.created.strftime("%d/%m/%Y"),
                'result' : json.loads(history.result.replace("'", "\"")
            ),
            }
            search_history.append(tmp)
        
        diposit_history = []
        for MoneyHistory in DepositeMoney.objects.filter(user=user):
            tmp = {
                'deposit_id' : MoneyHistory.id,
                'date' : MoneyHistory.created.strftime("%d/%m/%Y"),
                'amount' : MoneyHistory.Amount,
                'transection_id' : MoneyHistory.TransactionId,
                'method' : MoneyHistory.method,
                'status' : MoneyHistory.status
            }
            diposit_history.append(tmp)
        
        jsonn_response = {
            'personal_data' : serializer.data,
            'searched_history' : search_history,
            'deposit_history' : diposit_history
        }
        response = Response(jsonn_response, status=status.HTTP_200_OK)
        
        # Set the Referrer Policy header
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        return response

#----------------------------------------------------UserChangePAssword by Riken------------------------------------------------------------

# class UserChangePasswordView(APIView):
#     """ 
#     Change user password
#     """
#     renderer_classes = [UserRenderer]
#     permission_classes = [IsAuthenticated]
#     def post(self, request, format=None):
#         serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
#         serializer.is_valid(raise_exception=True)
#         return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
    
#--------------------------------------------------UserChangePassword by Riken---------------------------------------------------------------


#---------------------------------------------Change Password by Adil------------------------------------------------------------

class UserChangePasswordView(APIView):
    """ 
    Change user password
    """
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]  # Allow any user to access this endpoint

    def post(self, request, format=None):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')
        new_password = request.data.get('new_password')

        # Check if required fields are provided
        if not email or not verification_code or not new_password:
            return Response({'Message': 'Please provide the following details', 'details': {'email': 'Email', 'verification_code': 'Verification code', 'new_password': 'New Password'}}, status=status.HTTP_400_BAD_REQUEST)

         # Check if verification code is a valid number
        if not verification_code.isdigit():
            return Response({'Message': 'Invalid Verification Code.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email, verification_code=verification_code)
            verification_code = random.randint(100000, 999999)# Extra Code added to change the code after Process because same code will be used multiple times.
            user.verification_code = verification_code# Extra Code added to change the code after Process because same code will be used multiple times.
            user.save()# Extra Code added to change the code after Process because same code will be used multiple times.
        except CustomUser.DoesNotExist:
            return Response({'Message': 'Invalid email or verification code.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserChangePasswordSerializer(instance=user, data={'password': new_password, 'password2': new_password})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'Message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            # Handle validation errors
            return Response({'Message': e.detail}, status=status.HTTP_400_BAD_REQUEST)


#---------------------------------------------Change Password by Adil------------------------------------------------------------









from django.core.mail import send_mail

class send_email(APIView):

    def post(self, request, format=None):
        user_id = get_user_id_from_token(request)
        user = CustomUser.objects.filter(id=user_id).first()
        if not user :
            msg = 'could not find the user'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        EMAIL_HOST = 'mail.keywordlit.com'
        EMAIL_PORT = 465
        EMAIL_HOST_USER = 'donotreply@keywordlit.com'
        EMAIL_HOST_PASSWORD = 'keywordlit'
        from_email = 'donotreply@keywordlit.com'
        subject = 'This mail to verify the user via OTP'
        recipient_list = user.email
        
        if not user.verification_code :
            msg = 'Could not get the userverified'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
            
        # Email body
        body = 'Here is the OTP to verify the account : '+ str(user.verification_code) +'\nThanks'
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = recipient_list
        msg['Subject'] = subject
        
        # Attach the email body
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT)
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.sendmail(from_email, recipient_list, msg.as_string())
        server.quit()
        return Response({"Email sent successfully."},status=status.HTTP_200_OK)
    
class HashTagHistory(APIView):
    """ 
    Get a user profile data with email and password
    """
    def post(self, request, format=None):
        search_history = []
        user_id = get_user_id_from_token(request)
        user = CustomUser.objects.filter(id=user_id).first()
        if not user :
            msg = 'could not found the user'
            return Response({ "search_history":search_history, "Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        for history in SearchedHistory.objects.filter(user=user) :
            tmp = {
                'platform' : history.platform,
                'hashtag' : history.hashtag,
                'result' : json.loads(history.result.replace("'", "\""))
            }
            search_history.append(tmp)
        msg = 'successfully searched userhistory !'
        return Response({ "search_history":search_history, "Message": msg}, status=status.HTTP_200_OK)
    
class DepositeMoneyAPI(APIView):
    """ 
    Get a user profile data with email and password
    """
    def post(self, request, format=None):
        transection_id = 0
        user_id = get_user_id_from_token(request)
        user = CustomUser.objects.filter(id=user_id).first()
        if not user :
            msg = 'could not diposite in the user account'
            return Response({ "transection_id":transection_id, "Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not 'money' in request.data and not request.data['money']:
            msg = 'could not found the money'
            return Response({ "transection_id":transection_id, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
        transection_id = random.randint(100000000,99999999999)
        DepositeMoney.objects.create(user=user,Amount= request.data['money'],TransactionId = str(transection_id), method = "CREDIT_CARD", status = "COMPLETE" )
        
        msg = 'successfully transection completed !'
        return Response({ "transection_id":transection_id, "Message": msg}, status=status.HTTP_200_OK)

class InstaHashTag(APIView):
    """ 
    Get a user profile data with email and password
    """
    def get_ranking(self,data) :
        for item in data["Hashtag"].values():
            # breakpoint()
            item["total_post"] = int(str(item["total_post"]).replace(",", ""))

        # Calculate maximum number of posts
        max_posts = max(item["total_post"] for item in data["Hashtag"].values())

        referanceposts = sum(item["total_post"] for item in data["Hashtag"].values())
        referance_cpc = 5
        referance_total_post = 1000000000
        total_post_ration = referanceposts/referance_total_post
        estimated_base_cpc = referance_cpc * total_post_ration
        
        # Perform normalization and scoring calculations
        total_hashtags = len(data["Hashtag"])  # Total number of hashtags
        normalized_data = []
        for index, item in enumerate(data["Hashtag"].values()):
            normalized_rank = 1 - ((index + 1) / total_hashtags)  # Rank normalization
            normalized_posts = item["total_post"] / max_posts
            combined_score = (0.4 * normalized_rank) + (0.6 * normalized_posts)  # Example weights

            item_data = {
                "hashtag": item["hastag"],
                "total_post": item["total_post"],
                "rank" : index,
                "combined_score": combined_score
            }
            if 'likes' in item : item_data['likes'] = item['likes']
            if 'comment' in item : item_data['comment'] = item['comment']
            if 'reels' in item : item_data['reels'] = item['reels']
            normalized_data.append(item_data)

        # Set thresholds for competition levels
        low_comp_threshold = 0.3
        med_comp_threshold = 0.6

        # Categorize based on competition levels
        for item in normalized_data:
            item['rank'] += 1
            if item["combined_score"] <= low_comp_threshold:
                item["competition_level"] = "Low Competition"
                item["CPC"] = round(estimated_base_cpc*0.8,3)
            elif low_comp_threshold < item["combined_score"] <= med_comp_threshold:
                item["competition_level"] = "Medium Competition"
                item["CPC"] = round(estimated_base_cpc*1.0,3)
            else:
                item["CPC"] = round(estimated_base_cpc*1.2,3)
                item["competition_level"] = "High Competition"
                
            
        return normalized_data

    def get_ranking2(self, data):
        data = data['Hashtag']
        for item in data:
            item["total_post"] = int(str(item["total_post"]).replace(",", ""))

        # Calculate maximum number of posts
        max_posts = max(item["total_post"] for item in data)

        referanceposts = sum(item["total_post"] for item in data)
        referance_cpc = 5
        referance_total_post = 1000000000
        total_post_ration = referanceposts / referance_total_post
        estimated_base_cpc = referance_cpc * total_post_ration

        # Perform normalization and scoring calculations
        total_hashtags = len(data)  # Total number of hashtags
        normalized_data = []
        for index, item in enumerate(data):
            normalized_rank = 1 - ((index + 1) / total_hashtags)  # Rank normalization
            normalized_posts = item["total_post"] / max_posts
            combined_score = (0.4 * normalized_rank) + (0.6 * normalized_posts)  # Example weights

            item_data = {
                "hashtag": item["hashtag"],
                "total_post": item["total_post"],
                "rank": index,
                "combined_score": combined_score
            }
            normalized_data.append(item_data)

        # Set thresholds for competition levels
        low_comp_threshold = 0.3
        med_comp_threshold = 0.6

        # Categorize based on competition levels
        for item in normalized_data:
            if item["combined_score"] <= low_comp_threshold:
                item["competition_level"] = "Low Competition"
                item["CPC"] = round(estimated_base_cpc * 0.8, 3)
            elif low_comp_threshold < item["combined_score"] <= med_comp_threshold:
                item["competition_level"] = "Medium Competition"
                item["CPC"] = round(estimated_base_cpc * 1.0, 3)
            else:
                item["competition_level"] = "High Competition"
                item["CPC"] = round(estimated_base_cpc * 1.2, 3)

        return normalized_data
    
    def give_driver(self,CreateNew = False):
        driver = ''
        global user_driver_dict
        if user_driver_dict == {} or CreateNew == True:
            user_driver_dict = GetActiveChromeSelenium()
        for keys,value in user_driver_dict.items():
            if value['status'] == True :
                driver = value['driver']
            if driver : 
                value['status'] = False

                return driver, keys, value
        return '','',''
    
    def convert_dict(self,original_list):
        converted_dict = {}

        for item in original_list:
            converted_dict[item['rank']] = {
                'hashtag': item['hashtag'],
                'total_post': f"{item['total_post']:,}",
                'link': item['link'],
                'likes': 0,  # You can add more fields here if needed
                'comment': 0,
                'reels': '42%'  # Example value, replace with actual data if available
            }
        return converted_dict
    def post(self, request, format=None):
        Hastag = []
        user_id = get_user_id_from_token(request)
        user = CustomUser.objects.filter(id=user_id).first()
        
        if not user :
            msg = 'could not found the user'
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        if user.credit < 10 :
            msg = 'Insufficient credit to perform this action.'
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        try :
            user = CustomUser.objects.filter(id=user_id).first()
            i_bot = Bot(user=user)
            twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
            past_searched_hashtag = SearchedHistory.objects.filter(hashtag=request.data['hashtag'],created__gte=twenty_four_hours_ago,platform="Instagram")
            
            if not past_searched_hashtag :
                for _ in range(3) :
                    Hastag = main_call(request.data['hashtag'])
                    if len(Hastag) > 5: break
                else:
                    msg = 'Failed to scrape the hashtag'
                    return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
            else :
                try :
                    Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['hashtag'],created__gte=twenty_four_hours_ago,platform="Instagram").first().result.replace("'", "\""))
                except :
                    try :
                        Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['hashtag'],created__gte=twenty_four_hours_ago,platform="Instagram").first().result)
                    except :
                        msg = 'Failed to scrape the hashtag'
                        return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

            if Hastag:
                msg = 'Hashtag scraped successfully'
                if not past_searched_hashtag :
                    SearchedHistory.objects.create(
                        user = user,
                        hashtag = request.data['hashtag'],
                        platform = 'Instagram',
                        result = json.dumps(Hastag)
                    )
                    user.credit= user.credit - 10
                    user.save()
                if type(Hastag) == str : 
                    Hastag = json.loads(Hastag.replace("'", "\""))
                return Response({"Hashtag": Hastag, "Message": msg},status=status.HTTP_200_OK)
                # return Response({"Hashtag": self.get_ranking2({"Hashtag": Hastag}), "Message": msg},status=status.HTTP_200_OK)
            else:
                msg = 'Failed to scrape the hashtag'
                return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
        except :
            msg = 'Failed to scrape the hashtag'
        finally :
            if msg == "Hashtag scraped successfully" :
                return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_200_OK)
                # return Response({"Hashtag": self.get_ranking2({"Hashtag": Hastag}), "Message": msg}, status=status.HTTP_200_OK)
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

        
        
    # def post(self, request, format=None):
    #     Hastag = []
    #     user_id = get_user_id_from_token(request)
    #     user = CustomUser.objects.filter(id=user_id).first()
        
    #     if not user :
    #         msg = 'could not found the user'
    #         return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
    #     if user.credit < 10 :
    #         msg = 'Insufficient credit to perform this action.'
    #         return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_402_PAYMENT_REQUIRED)
        
    #     driver,keys,value = self.give_driver()
        
    #     global user_driver_dict
    #     if driver:
    #         try :
    #             user = CustomUser.objects.filter(id=user_id).first()
    #             i_bot = Bot(user=user)
    #             twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    #             past_searched_hashtag = SearchedHistory.objects.filter(hashtag=request.data['hashtag'],created__gte=twenty_four_hours_ago,platform="Instagram")
    #             # if past_searched_hashtag : 
    #             #     Hastag = json.loads(past_searched_hashtag.first().result.replace("'", "\""))
    #             # if not past_searched_hashtag :
    #             #     Hastag = self.get_related_keywords(request.data['hashtag'])
                
    #             if i_bot.TestRunDriver(driver) == False :
    #                 driver,keys,value = self.give_driver(CreateNew=True)
    #             if not past_searched_hashtag :
    #                 for _ in range(3) :
    #                     Hastag = scrape_hashtags(keys,request.data['hashtag'], driver)
    #                     if len(Hastag) > 5: break
    #                 else:
    #                     msg = 'Failed to scrape the hashtag'
    #                     return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
    #             else :
    #                 try :
    #                     Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['hashtag'],created__gte=twenty_four_hours_ago,platform="Instagram").first().result.replace("'", "\""))
    #                 except :
    #                     try :
    #                         Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['hashtag'],created__gte=twenty_four_hours_ago,platform="Instagram").first().result)
    #                     except :
    #                         msg = 'Failed to scrape the hashtag'
    #                         return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

    #             if Hastag:
    #                 msg = 'Hashtag scraped successfully'
    #                 if not past_searched_hashtag :
    #                     SearchedHistory.objects.create(
    #                         user = user,
    #                         hashtag = request.data['hashtag'],
    #                         platform = 'Instagram',
    #                         result = json.dumps(Hastag)
    #                     )
    #                     user.credit= user.credit - 10
    #                     user.save()
    #                 if type(Hastag) == str : 
    #                     Hastag = json.loads(Hastag.replace("'", "\""))
    #                 breakpoint()
    #                 return Response({"Hashtag": self.get_ranking({"Hashtag": Hastag}), "Message": msg},status=status.HTTP_200_OK)
    #             else:
    #                 msg = 'Failed to scrape the hashtag'
    #                 return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
    #         except :
    #             msg = 'Failed to scrape the hashtag'
    #         finally :
    #             value['status'] = True
    #             if msg == "Hashtag scraped successfully" :
    #                 return Response({"Hashtag": self.get_ranking({"Hashtag": Hastag}), "Message": msg}, status=status.HTTP_200_OK)
    #             return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

    #     else:
    #         msg = 'All drivers are busy!'
    #         return Response({"Message": msg}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class YouTubeHashTag(APIView):
    def post(self, request, format=None):
        Hastag = []
        user_id = get_user_id_from_token(request)
        user = CustomUser.objects.filter(id=user_id).first()
        if not user :
            msg = 'could not found the user'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        if user.credit < 10 :
            Hastag=request.data['tag']
            msg = 'Insufficient credit to perform this action.'
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        if not 'tag' in request.data and not request.data['tag']:
            msg = 'could not found the tag'
            return Response({'Message' : msg}, status=status.HTTP_400_BAD_REQUEST)
        
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        past_searched_hashtag = SearchedHistory.objects.filter(hashtag=request.data['tag'],created__gte=twenty_four_hours_ago,platform="Youtube")
        # breakpoint()
        if not past_searched_hashtag :
            if 'language' in request.data and request.data['language']:
                lang = request.data['language']# en or ko else lang=None
                Hastag = self.get_related_keywords(request.data['tag'],lang)
            else:
                Hastag = self.get_related_keywords(request.data['tag'])
            print("The Hashtag Is",Hastag)
            # if len(Hastag)>=15:
            #     Hastag=Hastag[:15]
        else :
            try :
                Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['tag'],created__gte=twenty_four_hours_ago,platform="Youtube").first().result.replace("'", "\""))
            except :
                try :
                    Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['tag'],created__gte=twenty_four_hours_ago,platform="Youtube").first().result)
                except :
                    msg = 'Failed to scrape the hashtag'
                    return Response({"Hashtag": request.data['tag'], "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

        if Hastag:
            if not past_searched_hashtag :
                SearchedHistory.objects.create(
                    user = user,
                    hashtag = request.data['tag'],
                    platform = 'Youtube',
                    result = json.dumps(Hastag)
                )
                user.credit= user.credit - 10
                user.save()
            
            if type(Hastag) == str : 
                Hastag = json.loads(Hastag.replace("'", "\""))
            msg = 'Hashtag scraped successfully'

            try:
                TREND = get_yt_trend_data(request.data['tag'])
                return Response({"Hashtag":  Hastag, "trend" : TREND, "Message": msg},status=status.HTTP_200_OK) # If we get trends
            except:
                return Response({"Hashtag":  Hastag,  "Message": msg},status=status.HTTP_200_OK) # If we don't get trends
        else:
            msg = 'Failed to scrape the hashtag'
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
        
    #---------------------New code to refresh token automatically By ADIL--------------------------------------------------------
    def read_token_from_file(self,file_path):
        with open(file_path, 'r') as file:
            token_data = json.load(file)
        return token_data

    def write_token_to_file(self,file_path, token_data):
        with open(file_path, 'w') as file:
            json.dump(token_data, file)

    def refresh_access_token(self,client_id, client_secret, refresh_token, token_uri):
        token_data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        try:
            response = requests.post(token_uri, data=token_data)
            response_data = response.json()
            if 'access_token' in response_data and 'expires_in' in response_data:
                access_token = response_data['access_token']
                refresh_token = response_data.get('refresh_token', refresh_token)
                expiry_seconds = response_data['expires_in']
                return access_token, refresh_token, expiry_seconds
            else:
                print("Failed to refresh access token.")
                return None, None, None
        except Exception as e:
            print("Error occurred during token refresh:", e)
            return None, None, None

    def update_config_yaml(self,config_file, refresh_token):
        with open(config_file, 'r') as file:
            config_data = yaml.safe_load(file)
        config_data['refresh_token'] = refresh_token
        with open(config_file, 'w') as file:
            yaml.dump(config_data, file)

    def refresh_token_flow(self,config_file, token_file):
        # Read token data from file
        token_data = self.read_token_from_file(token_file)
        client_id = token_data['client_id']
        client_secret = token_data['client_secret']
        refresh_token = token_data['refresh_token']
        token_uri = token_data['token_uri']

        # Check if token is expired
        expiry_datetime = datetime.strptime(token_data['expiry'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if datetime.utcnow() >= expiry_datetime:
            # Token is expired, get a new one
            new_access_token, new_refresh_token, expiry_seconds = self.refresh_access_token(client_id, client_secret, refresh_token, token_uri)
            if new_refresh_token:
                expiry_datetime = datetime.utcnow() + timedelta(seconds=expiry_seconds)
                # Update token data
                token_data['refresh_token'] = new_refresh_token
                token_data['expiry'] = expiry_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                # Write updated token data to file
                self.write_token_to_file(token_file, token_data)
                # Update config.yaml with new refresh token
                self.update_config_yaml(config_file, new_refresh_token)
                print("Refreshed token and updated config.yaml.")
            else:
                print("Failed to refresh token.")
        else:
            print("Token is still valid.")
#-------------------- To Detect the language of keyword given by user --------------------------------------------------------------
    def detect_language(self,text):
        try:
            detected_lang = langdetect.detect(text)
            return detected_lang
        except:
            return "ko" # If it failed to detect language then by default --> KOREAN

#-------------------- To Detect the language of keyword given by user --------------------------------------------------------------


    #---------------------New code to refresh token automatically By ADIL--------------------------------------------------------
        
    def get_related_keywords(self, keyword_text, lang=None):
        
        #---------------------New code to refresh token automatically By ADIL--------------------------------------------------------
        config_file = './conf.yaml'    # Riken Bhai Please check this
        token_file = './ref-token.json' # Riken Bhai Please check this
        self.refresh_token_flow(config_file, token_file) # Riken Bhai Please check this
        #---------------------New code to refresh token automatically By ADIL--------------------------------------------------------
        hashtags = []
        # Initialize the Google Ads client.
        client = GoogleAdsClient.load_from_storage("./conf.yaml")

        # Get the service.
        keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

        #------------------------------- Hard Coded Values Used Before--------------------------------------------------------------
        # Set up the query parameters.
        #language = client.get_type("StringValue")
        #language = "1000" # For English
        #language_criterion_id = "1000"  # Criterion ID for English
        #geo_target_criterion_id = "2840"  # Criterion ID for United States

        #------------------------------- Hard Coded Values Used Before--------------------------------------------------------------
        
        
        #--------------------------------------New Code that detect the Lnaguage of user input and region set to South Korea -------------------------------------
        
        if lang is not None:
            if lang == 'ko':  # Korean
                language = "1012"
                language_criterion_id = "1012"
                # Update geo target criterion for South Korea
                geo_target_criterion_id = "2410"
            elif lang == 'en':  # English
                language = "1000"
                language_criterion_id = "1000"
                # Update geo target criterion for South Korea
                geo_target_criterion_id = "2410"
            else:
                pass
        
        
        else:
        
            
            # if lang is None
            user_input_language = self.detect_language(keyword_text)
            print("UserInput Langauge is :",user_input_language)
            if user_input_language == 'ko':  # Korean
                language = "1012"
                language_criterion_id = "1012"
                # Update geo target criterion for South Korea
                geo_target_criterion_id = "2410"
            elif user_input_language == 'en':  # English
                language = "1000"
                language_criterion_id = "1000"
                # Update geo target criterion for South Korea
                geo_target_criterion_id = "2410"
            else:
                # Default to Korean if language detection fails or unknown language
                language = "1012"
                language_criterion_id = "1012"
                # Update geo target criterion for South Korea
                geo_target_criterion_id = "2410"

    #--------------------------------------New Code that detect the Lnaguage of user input and region set to South Korea -------------------------------------

        keyword = keyword_text

        # Create the request.
        request = client.get_type("GenerateKeywordIdeasRequest")
        request.customer_id = '5227482652'
        request.language = f"languageConstants/{language_criterion_id}"
        request.geo_target_constants.append(f"geoTargetConstants/{geo_target_criterion_id}")
        request.keyword_plan_network = client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
        request.keyword_seed.keywords.append(keyword)

        try:
            # Execute the request.
            response = keyword_plan_idea_service.generate_keyword_ideas(request=request)

            # Iterate through the results and print them.
            for idea in response.results:
                metric = idea.keyword_idea_metrics
                print(f"Keyword: {idea.text}, Search Volume: {metric.avg_monthly_searches}, Competition: {metric.competition.name}")
                hashtags.append({
                    "Keyword" : idea.text,
                    "Search_Volume" : metric.avg_monthly_searches,
                    "Competition" : metric.competition.name
                })

            return hashtags

        except GoogleAdsException as ex:
            print(f"Request with ID '{ex.request_id}' failed with status '{ex.error.code().name}' and includes the following errors:")
            for error in ex.failure.errors:
                print(f"\tError with message '{error.message}'.")
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")

        return hashtags


class start_drivers(APIView):

    def post(self, request, format=None):
        try :
            return JsonResponse({"Hastag" : "hashtag"})
        except Exception as e :
            return JsonResponse({"Hastag" : "hashtag"})
        

class GetUserList(APIView):
    """ 
    Get-all-user if token is of super user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user_id = get_user_id_from_token(request)
        user, is_superuser = IsSuperUser(user_id)
        if not user or not is_superuser:
            msg = 'could not found the super user'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        if 'email' in request.data:
            all_user = CustomUser.objects.filter(is_superuser=False,email=request.data['email'])
            if not all_user :
                return Response({'Message' : 'counld not got the user list', 'email' : request.data['email']}, status=status.HTTP_204_NO_CONTENT)
                
        else :
            all_user = CustomUser.objects.filter(is_superuser=False)
        user_list = [ 
                     {
                         c_user.id : { 
                             'email' : c_user.email, 
                             'credit' : c_user.credit, 
                             'fname' : c_user.first_name, 
                             "Total_diposite" :DepositeMoney.objects.filter(status="COMPLETE",user=c_user).aggregate(total_amount=Sum('Amount'))['total_amount'] if DepositeMoney.objects.filter(status="COMPLETE",user=c_user).aggregate(total_amount=Sum('Amount'))['total_amount'] else 0, 
                             "search_history" : [ {"hashtag" : search.hashtag, "platform" : search.platform } for search in SearchedHistory.objects.filter(user=c_user)] }} for c_user in all_user 
                     ]
        if user_list :
            return Response({'Message' : 'successfully got the user list','userlist' : user_list}, status=status.HTTP_200_OK)
        return Response({'Message' : 'counld not got the user list', 'userlist' : user_list}, status=status.HTTP_204_NO_CONTENT)

class GetDipositeList(APIView):
    """ 
    Get-all-user if token is of super user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user_id = get_user_id_from_token(request)
        user, is_superuser = IsSuperUser(user_id)
        if not user or not is_superuser:
            msg = 'could not found the super user'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        if 'TransactionId' in request.data:
            all_diposite = DepositeMoney.objects.filter(TransactionId=request.data['TransactionId'])
            if not all_diposite :
                return Response({'Message' : 'counld not got the diposite', 'TransactionId' : request.data['TransactionId']}, status=status.HTTP_204_NO_CONTENT)
                
        else :
            all_diposite = DepositeMoney.objects.filter()
            
        diposite_list = [ 
                     {
                         dp.TransactionId : {
                             "amount" : dp.Amount,
                             "method" : dp.method,
                             "status" : dp.status,
                             "user" : dp.user.email,
                         } 
                         } 
                     for dp in all_diposite ]
        
        
        # diposite_list = [ {c_user.id : { 'email' : c_user.email, 'credit' : c_user.credit, 'fname' : c_user.first_name, "Diposited_balance" : sum([dp_obj.Amount for dp_obj in DepositeMoney.objects.filter(user=c_user)]) if  sum([dp_obj.Amount for dp_obj in DepositeMoney.objects.filter(user=c_user)]) else 0, "search_history" : [ {"hashtag" : search.hashtag, "platform" : search.platform } for search in SearchedHistory.objects.filter(user=c_user)] }} for c_user in all_diposite ]
        if diposite_list :
            return Response({'Message' : 'successfully got the user list','userlist' : diposite_list}, status=status.HTTP_200_OK)
        return Response({'Message' : 'counld not got the user list', 'userlist' : diposite_list}, status=status.HTTP_204_NO_CONTENT)

class EditUser(APIView):
    """ 
    Get-all-user if token is of super user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):

        user_id = get_user_id_from_token(request)
        user, is_superuser = IsSuperUser(user_id)
        if not user or not is_superuser:
            msg = 'could not found the super user'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_found = False
        if not 'email' in request.data and not request.data['email']:
            msg = 'could not found the email'
            return Response({'Message' : msg}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'feild' in request.data and not request.data['feild']:
            msg = 'could not found the feild which needs to be edited'
            return Response({'Message' : msg}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'new_value' in request.data and not request.data['new_value']:
            msg = 'could not found the new value which needs to be replaced with old values'
            return Response({'Message' : msg}, status=status.HTTP_400_BAD_REQUEST)
            
        found_user = CustomUser.objects.filter(is_superuser=False,email=request.data['email'])
        if not found_user :
            return Response({'Message' : 'could not got the user'}, status=status.HTTP_204_NO_CONTENT)

        found_user = found_user.first()
        field_name = request.data['feild']
        new_value = request.data['new_value']
        
        if type(field_name) == list :
            try: 
                for fl in range(len(field_name)) :
                    fl_name = field_name[fl]                    
                    nv_name = new_value[fl]     
                    setattr(found_user, fl_name, nv_name)
                    found_user.save()               
                msg = 'Successfully edited the user data'
                status_code = status.HTTP_200_OK
            except : 
                msg = f'Error editing user data: {str(e)}'
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        elif type(field_name) == str :
            
            try:
                setattr(found_user, field_name, new_value)
                found_user.save()
                msg = 'Successfully edited the user data'
                status_code = status.HTTP_200_OK
                
            except Exception as e:
                msg = f'Error editing user data: {str(e)}'
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # foundus

        
        return Response({'Message' : msg}, status=status_code)


class DeleteUser(APIView):
    """ 
    Get-all-user if token is of super user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):

        user_id = get_user_id_from_token(request)
        user, is_superuser = IsSuperUser(user_id)
        if not user or not is_superuser:
            msg = 'could not found the super user'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        user_deleted = False
        if 'email' in request.data and request.data['email']:
            del_user = CustomUser.objects.filter(is_superuser=False,email=request.data['email'])
            if not del_user :
                return Response({'Message' : 'successfully got the user list','user_deleted' : user_deleted}, status=status.HTTP_204_NO_CONTENT)

            del_user = del_user.first()
            if del_user.delete() :
                user_deleted = True

        if user_deleted :
            return Response({'Message' : 'successfully deleted the user list','user_deleted' : user_deleted}, status=status.HTTP_200_OK)
        return Response({'Message' : 'counld not delete the user', 'user_deleted' : user_deleted}, status=status.HTTP_204_NO_CONTENT)


class InstaHashTagHistory(APIView):
    """ 
    Get-all-user if token is of super user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        tz = pytz.timezone('UTC')
        now = datetime.now().astimezone(tz)
        user_id = get_user_id_from_token(request)
        user, is_superuser = IsSuperUser(user_id)
        if not user or not is_superuser:
            msg = 'could not found the super user'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
                    
        return Response({'Message' : 'successfully get the data', 'data' : get_search_history(6,"Instagram")}, status=status.HTTP_200_OK)


class YoutubeHashTagHistory(APIView):
    """ 
    Get-all-user if token is of super user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        tz = pytz.timezone('UTC')
        now = datetime.now().astimezone(tz)
        user_id = get_user_id_from_token(request)
        user, is_superuser = IsSuperUser(user_id)
        if not user or not is_superuser:
            msg = 'could not found the super user'
            return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        

        # Get search history for "Youtube"
        youtube_history = get_search_history_(start_date=now - timedelta(days=6), end_date=now, platform_="Youtube")
        
        # Get search history for "Youtube1"
        youtube1_history = get_search_history_(start_date=now - timedelta(days=6), end_date=now, platform_="Youtube1")
        
        # Combine the histories into a single response
        combined_response = {
            "Youtube_search_history": youtube_history,
            "Youtube_average_search_history": youtube1_history
        }
        
        return Response({'Message': 'Successfully get the data', 'data': combined_response}, status=status.HTTP_200_OK)
                    
        #return Response({'msg' : 'successfully get the data', 'data' : get_search_history(6,"Youtube")}, status=status.HTTP_200_OK)



class SuperuserDashboard(APIView):
    """ 
    Get-all-user if token is of super user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request, format=None):
        try :
            tz = pytz.timezone('UTC')

            now = datetime.now().astimezone(tz)
            user_id = get_user_id_from_token(request)
            user, is_superuser = IsSuperUser(user_id)
            if not user or not is_superuser:
                msg = 'could not found the super user'
                return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)



            #Dash board
            # all_user = CustomUser.objects.filter(is_superuser=False)
            weekly_data = []

            for i in range(6):
                # Calculate the start and end of the week
                end_of_week = now - timedelta(days= 6*i  )
                start_of_week = end_of_week - timedelta(days=6)

                # Query to get data created in this week
                week_data = CustomUser.objects.filter(created__gte=start_of_week,  created__lte=end_of_week,is_superuser=False)

                # Add the query results to the list
                weekly_data.append(week_data)
                
            main_weekly_data = []
            for week in weekly_data :
                main_weekly_data.append( {
                    weekly_data.index(week)+1 : {
                        'weekly_total_user' : len(week)
                    }
                })
            
            
            Weekly_income = []
            for i in range(6):
                # Calculate the start and end of the week
                end_of_week = now - timedelta(days= 6*i  )
                start_of_week = end_of_week - timedelta(days=6)

                # Query to get data created in this week
                week_data = DepositeMoney.objects.filter(created__gte=start_of_week,  created__lte=end_of_week)

                # Add the query results to the list
                Weekly_income.append(week_data)
            main_weekly_income = []
            for week in Weekly_income :
                if not week :
                    main_weekly_income.append({
                        Weekly_income.index(week)+1 : {
                            'weekly_total_income' : 0
                        }
                    })
                else :
                    main_weekly_income.append( {
                        Weekly_income.index(week)+1 : {
                            'weekly_total_income' : sum([ dp.Amount for dp in week]),
                            "weekly_total_diposite" : len(week)
                        }
                    })
                    
                    
            Weekly_search = []
            for i in range(6):
                # Calculate the start and end of the week
                end_of_week = now - timedelta(days= 6*i  )
                start_of_week = end_of_week - timedelta(days=6)

                # Query to get data created in this week
                week_data = SearchedHistory.objects.filter(created__gte=start_of_week,  created__lte=end_of_week)

                # Add the query results to the list
                Weekly_search.append(week_data)
            main_weekly_search = []
            for week in Weekly_search :
                if not week :
                    main_weekly_search.append({
                        Weekly_search.index(week)+1 : {
                            'weekly_total_search' : 0
                        }
                    })
                else :
                    main_weekly_search.append( {
                        Weekly_search.index(week)+1 : {
                            'weekly_total_search' : len(week)
                        }
                    })
            msg = 'get the data successfully'            
        except :
            msg = 'could not get the data successfully'    
                    
        responsee = {
            "total_user" : CustomUser.objects.filter(is_superuser=False).count(),
            "total_Instagram_search" : SearchedHistory.objects.filter(platform="Instagram").count(),
            "Instagram_search_history" : get_search_history(6,"Instagram"),
            "total_Youtube_search" : SearchedHistory.objects.filter(platform="Youtube").count(),
            "Youtube_search_history" : get_search_history(6,"Youtube"),
            "total_diposite_amount" : DepositeMoney.objects.filter(status="COMPLETE").aggregate(total_amount=Sum('Amount'))['total_amount'],
            "total_diposite" : DepositeMoney.objects.filter(status="COMPLETE").count(),
            "weekly_user" : main_weekly_data,
            "weekly_income" : main_weekly_income,
            "weekly_search" : main_weekly_search
        }
        
        return Response({'Message' : msg, 'data' : responsee}, status=status.HTTP_200_OK)
    

from dateutil.relativedelta import relativedelta       
#---------------------------------------------------------New code for SuperUSerDashboard---------------------------------------
class SuperuserDashboardNew(APIView):
    """ 
    Get-all-user if token is of super user
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    
    def post(self, request, format=None):
        try :
            tz = pytz.timezone('UTC')
            now = datetime.now().astimezone(tz)
            user_id = get_user_id_from_token(request)
            user, is_superuser = IsSuperUser(user_id)
            if not user or not is_superuser:
                msg = 'could not found the super user'
                return Response({"Message": msg}, status=status.HTTP_401_UNAUTHORIZED)


            if request.method == 'POST':
                data = request.data
                date_filter = data.get('date_filter')
                start_date_str = data.get('start_date')
                end_date_str = data.get('end_date')
                periods_str = data.get('periods')
            
                # Convert start_date and end_date strings to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').astimezone(tz) if start_date_str else None
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').astimezone(tz) if end_date_str else None

                # Convert periods string to integer
                periods = int(periods_str) if periods_str else None


            if date_filter==None:
                msg={
                        "date_filter": "Missing"
                    }

                return Response({"Message": msg}, status=status.HTTP_400_BAD_REQUEST)
            

            if start_date == None and periods == None:
                msg={"Please Provide either of  the value":{
                        "start_date": "Missing",
                        "periods":"Missing"
                    }}

                return Response({"Message": msg}, status=status.HTTP_400_BAD_REQUEST)

        
            if date_filter == 'month' or date_filter == 'week' or date_filter == 'year':
                if date_filter == 'week':
                    end_date = now
                    start_date = now - timedelta(weeks=periods)
                elif date_filter == 'month':
                    end_date = now
                    start_date = now - relativedelta(months=periods)
                elif date_filter == 'year':
                    end_date = now
                    start_date = now - relativedelta(years=periods)
            else:
                start_date=start_date
                end_date=end_date


            msg = 'get the data successfully'            
        except :
            msg = 'could not get the data successfully'    
                    
        responsee = {
            "date_filter":date_filter,
            "date_range":{"Start_date":str(start_date), "End_date":str(end_date)},
            "total_user" : CustomUser.objects.filter(is_superuser=False,created__gte=start_date,  created__lte=end_date).count(),
            "total_Instagram_search" : SearchedHistory.objects.filter(platform="Instagram",created__gte=start_date,  created__lte=end_date).count(),
            "Instagram_search_history" : get_search_history_(start_date=start_date,end_date=end_date,platform_="Instagram"),
            #"total_Youtube_search" : SearchedHistory.objects.filter(platform="Youtube",created__gte=start_date,  created__lte=end_date).count(),
            "total_Youtube_search" : SearchedHistory.objects.filter(Q(platform="Youtube") | Q(platform="Youtube1"),created__gte=start_date,created__lte=end_date).count(),
            "Youtube_search_history" : get_search_history_(start_date=start_date,end_date=end_date,platform_="Youtube"),
            "Youtube_average_search_history" : get_search_history_(start_date=start_date,end_date=end_date,platform_="Youtube1"),
            "total_deposit_amount" : DepositeMoney.objects.filter(status="COMPLETE",created__gte=start_date,  created__lte=end_date).aggregate(total_amount=Sum('Amount'))['total_amount'],
            "total_deposit" : DepositeMoney.objects.filter(status="COMPLETE",created__gte=start_date,  created__lte=end_date).count(),

        }
        
        return Response({'Message' : msg, 'data' : responsee}, status=status.HTTP_200_OK)
#---------------------------------------------------------New code for SuperUSerDashboard---------------------------------------



#---------------------------------Forgot Password by Adil--------------------------------------------------------------------

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'Message': 'Please provide the following details', 'details': {'email': 'Email'}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Check if user exists in records
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # If user is not in records, prompt user to register first
            return Response({'Message': 'User not in records. Register first.'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a verification code
        verification_code = random.randint(100000, 999999)
        user.verification_code = verification_code
        user.save()

        # Send verification code via email
        send_otp_via_email(email)

        return Response({'Message': 'Password Reset code sent successfully. Use it to reset your password.'}, status=status.HTTP_200_OK)

#------------------------------------Forgot Password by Adil---------------------------------------------------------------
    





#-------------------------------Youtube Hashtag Search By Adil---------------------------------------------------------------

class YoutubeHashTag_new(APIView):
    """
    This function takes Query as Input and returns top_five_video_titles, avg_views,avg_likes & avg_comments as Output.

    """

    def search_youtube(self,query):
        lst = []
        url = "https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"

        encoded_query = urllib.parse.quote(query)
        
        headers = {
            "Accept": "*/*",
            #"Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
            "Authorization": "SAPISIDHASH 1707374253_db06ff3c4865646cc7e60b0d91fb6343a057d70e",
            "Content-Type": "application/json",
            "Origin": "https://www.youtube.com",
            #"Referer": f"https://www.youtube.com/results?search_query={query}",
            "Referer": f"https://www.youtube.com/results?search_query={encoded_query}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "same-origin",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-Goog-Authuser": "0",
            "X-Goog-Visitor-Id": "CgtRVDBNZC10YjhiRSiB7ZGuBjIKCgJJThIEGgAgTg%3D%3D",
            "X-Origin": "https://www.youtube.com",
            "X-Youtube-Client-Name": "1",
            "X-Youtube-Client-Version": "2.20240207.01.00"
        }
        
        cookies = {
            "SID": "g.a000gAhJjhQVJKHBBXaBY68i4nfoaCao9dHK-af3mg-T17NLt9H6hA1IUadg7WYJqCo2PIRShwACgYKAT4SAQASFQHGX2MifPyGJryV-pdKdPFnkApENRoVAUF8yKrr1PZ4ObLLCQk2WaxO23VE0076",
            "__Secure-1PSID": "g.a000gAhJjhQVJKHBBXaBY68i4nfoaCao9dHK-af3mg-T17NLt9H6CMWiFbLxypOOiClxT_twBQACgYKAfISAQASFQHGX2Mi6EPKJiUX9_H8aPGnd-nznxoVAUF8yKq7u_T5cA3_6jyJSv-31vlM0076",
            "__Secure-3PSID": "g.a000gAhJjhQVJKHBBXaBY68i4nfoaCao9dHK-af3mg-T17NLt9H6E8djN5wlekq077HtCM5KgAACgYKAeoSAQASFQHGX2MiCQeBFS35eAkJDAWqvNjQqBoVAUF8yKopgrg-BBHgqyMpmb9Fukje0076",
            "HSID": "ANRZYhMwnKWC1VV1A",
            "SSID": "AW9hnKacmAvmNmqbm",
            "APISID": "qx3YOrlTqUDgwkNo/AAEstHL4MHVmHg4TQ",
            "SAPISID": "A2WA-2epk6mIVn3n/A_l7GS8mEQOL_xPZw",
            "__Secure-1PAPISID": "A2WA-2epk6mIVn3n/A_l7GS8mEQOL_xPZw",
            "__Secure-3PAPISID": "A2WA-2epk6mIVn3n/A_l7GS8mEQOL_xPZw",
            "YSC": "1AybS0LaEtQ",
    #         "LOGIN_INFO": "AFmmF2swRQIgQfv7fKfpigXRDNRNo1bJ3_wIcCmGNP4HPM37gVcLa_kCIQDd7_sCH30rUCvuK4bJermQfdiVf-j6lC8odTfUQFhVMQ:QUQ3MjNmeVh0bUk3MnpIUXhIUWdieFFVVThNODdTZFdncEIwTW82Q0J4aVdDaEZaSUMxZTZ0Z0dIOERQbGJpdHpQUTJMVGZmbzdJSGdKT3l0Zk9hQjBsQlNwMGR5MUJpUTNwYVRVWHZ2UjEtc0JqVUtOS094WVNBdDV0R0tKS1lhLVNoTnFnV0ljUVo5SUEwZE1sM0hOTm1WLVFwSFRqcHpB",
    #         "VISITOR_PRIVACY_METADATA": "CgJJThIEGgAgTg%3D%3D",
    #         "VISITOR_INFO1_LIVE": "QT0Md-tb8bE",
            "PREF": "f7=4100&tz=Asia.Calcutta&f4=4000000&f5=30000",
            "__Secure-1PSIDTS": "sidts-CjEBPVxjSq7fPfKFm5cRqLqj1lg8e_LgpP5FczWUN5nrjebICE7aPkikLpbm6z4LzdpIEAA",
            "__Secure-3PSIDTS": "sidts-CjEBPVxjSq7fPfKFm5cRqLqj1lg8e_LgpP5FczWUN5nrjebICE7aPkikLpbm6z4LzdpIEAA",
            "CONSISTENCY": "AKreu9sWrLkdroQecNvyq9hIFL1SiHNDNQlbqEHaoJHpdH2lJRZ7rFsxkkQ9r9VhvnzAeqWqMjVQQIKk5hYSOTFyabobaWmEWLIVKByKfoBmMfg1xObtHpJM0JLU8TAJoCrCdrnU8d_zOVmoli3E0NBa",
            "SIDCC": "ABTWhQFist3oSOwEusHXhFerSf_BPZUaf7W7zHIJk8_Zf35u-343J6qznSIDkbSYM2_sz91oCA",
            "__Secure-1PSIDCC": "ABTWhQHC4whbeFvJKxTgPWH46on1CTAUbm2YmPFfXzN9wZ1xmp6kja80vpKRqfg1XQBBXNhumA",
            "__Secure-3PSIDCC": "ABTWhQGEzHWCQMtrZuVFsk91tvIK-X61Yg11c3BUO4Rbdc7Z_orv9JGYHraKn59SB5C2A-TZ2A",
            "ST-vhwkpf": "oq=%23bike&gs_l=youtube.3..0i71k1l9.0.0.2.13127.0.0.0.0.0.0.0.0..0.0.ytpnlt_c...0...1ac..64.youtube..0.0.0....0.1V7XxGFYavk&itct=CBMQ7VAiEwiF1-HYkJuEAxUp0XMBHWRaAtY%3D&csn=MC4xODU4MTUyMjM4OTE0NDIzNA..&endpoint=%7B%22clickTrackingParams%22%3A%22CBMQ7VAiEwiF1-HYkJuEAxUp0XMBHWRaAtY%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fresults%3Fsearch_query%3D%2523bike%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_SEARCH%22%2C%22rootVe%22%3A4724%7D%7D%2C%22searchEndpoint%22%3A%7B%22query%22%3A%22%23bike%22%7D%7D"
        }
        
        payload = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20240207.01.00",
                    "hl": "en",
                    "gl": "US",
                    "experimentIds": [],
                },
                "request": {
                    "sessionId": "None",
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": [],
                },
            },
            "query": query,
            "params": "Eg-KA3gC",
        }
        
        response = requests.post(url, headers=headers, cookies=cookies, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            link_extra='https://www.youtube.com/watch?v='
            #count=0
            for j in range(len(data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'])):
                try:
                    video_title=data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][j]['videoRenderer']['title']['runs'][0]['text']
                    views_count=int(data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][j]['videoRenderer']['viewCountText']['simpleText'].split()[0].replace(',',''))
                    link=link_extra+data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][j]['videoRenderer']['videoId']
                    #count+=1
                    #print(count)
                    dct={
                            'video_title':video_title,
                            'views_count':views_count,
                            'link':link
                        }
                    
                    
                    lst.append(dct)
                    
                except:
                        pass
            return lst
            
            
        else:
            print("Error:", response.status_code)
            return None
    
    def get_youtube_videos(self,query):
        response = self.search_youtube(query)
        response=response[:5]
        return response



    def get_youtube_video_data(self,query):
        videos = self.get_youtube_videos(query)
        video_titles=[i['video_title'] for i in videos]
        links=[i['link'] for i in videos]
        view_tmp=[int(i['views_count']) for i in videos]
        avg_view=round(sum(view_tmp)/len(view_tmp))
        return video_titles, links, avg_view

#----------------------------------------Extract Video ID----------------------------------------------------------------------
    def extract_video_id(self,url):
        try: 
            v_id=url.split('=')[-1]
        #     match = re.search(r"watch\?v=(\w+)", url)
            return v_id
        except:
            print('Invalid URL')


#----------------------------------------Extract Video ID----------------------------------------------------------------------


    #----------------------------------------LIKE----------------------------------------------------------------------

    def get_youtube_like_counts(self,video_url):
        video_id = self.extract_video_id(video_url)

        # Check if video ID exists
        if video_id:
            # API endpoint URL with updated video ID
            url = f"https://www.youtube.com/youtubei/v1/updated_metadata?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false&videoId={video_id}"

            # Request headers
            headers = {
                "Accept": "*/*",
                #"Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
                # Add your authorization headers here if needed
            }

            # Payload containing the video ID
            payload = {
                "context": {
                    "client": {
                        "clientName": "WEB",
                        "clientVersion": "2.20240207.01.00",
                        "hl": "en",
                        "gl": "IN",
                        "experimentIds": [],
                        "experimentsToken": "",
                        "utcOffsetMinutes": 330,
                        "browserName": "Chrome",
                        "browserVersion": "121.0.0",
                        "osName": "Windows",
                        "osVersion": "10.0",
                        "mobile": False,
                        "screenWidthPoints": 1920,
                        "screenHeightPoints": 1080,
                        "screenPixelDensity": 1,
                        "platform": "DESKTOP",
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                        "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                        "browserIsBots": False
                    },
                    "request": {},
                    "user": {}
                },
            }

            # Make the POST request
            response = requests.post(url, json=payload, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                try:
                    # Extract like counts from the response JSON
                    like_counts = int(response.json()['frameworkUpdates']['entityBatchUpdate']['mutations'][0]['payload']['likeCountEntity']['expandedLikeCountIfLiked']['content'].replace(',',''))
                    return like_counts
                except (KeyError, IndexError):
                    #print("Failed to extract like counts from the response.")
                    return None
            else:
                #print("Request failed with status code:", response.status_code)
                return None
        else:
            print("Failed to extract video ID from the URL.")
            return None
        

    #----------------------------------------------LIKE------------------------------------------------------
        


    #------------------------------------------COMMENTS-----------------------------------------------------------
        
# -------------------------------Extract The Continous Token From Pattern----------------------------------------------------
    def extract_continuation(self,response_text):
        pattern = r'"token":"([^"]*)"'
        match = re.search(pattern, response_text)
        if match:
            return match.group(1)
        else:
            return None


# -------------------------------Extract The Continous Token From Pattern----------------------------------------------------
        
    #-----------------------------------------Get Continuous Token----------------------------------------------------------#
    def get_youtube_continuation(self,video_url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        }

        try:
            response = requests.get(video_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            response_text = response.text
            # Extract continuation from the response text
            continuation = self.extract_continuation(response_text)
            return continuation
        except Exception as e:
            print("Error:", e)
            return None
        
    #-----------------------------------------Get Comments----------------------------------------------------------#

    def get_video_metadata(self,continuation_token):
        url = "https://www.youtube.com/youtubei/v1/next?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"

        headers = {
            "Accept": "*/*",
            #"Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
            "Content-Type": "application/json",
            "Origin": "https://www.youtube.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        }

        payload = {
            "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
            "prettyPrint": False,
            "context": {
                "client": {
                    "hl": "en-GB",
                    "gl": "IN",
                    "remoteHost": "103.219.216.157",
                    "deviceMake": "",
                    "deviceModel": "",
                    "browserName": "Chrome",
                    "browserVersion": "121.0.0",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "mobile": False,
                    "screenWidthPoints": 1920,
                    "screenHeightPoints": 1080,
                    "screenPixelDensity": 1,
                    "platform": "DESKTOP",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    "clientName": "WEB",
                    "clientVersion": "2.20240207.01.00",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "browserIsBots": False
                },
                "user": {},
                "request": {}
            },             
            "continuation": continuation_token,
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            tmp= response.json()
            return int(tmp['onResponseReceivedEndpoints'][0]['reloadContinuationItemsCommand']['continuationItems'][0]['commentsHeaderRenderer']['countText']['runs'][0]['text'].replace(',',''))
        except requests.exceptions.HTTPError as err:
            print("HTTP Error:", err)
        except requests.exceptions.RequestException as err:
            print("Request Exception:", err)

            
    def get_youtube_comment_counts(self,video_url):
        continuation_token=self.get_youtube_continuation(video_url)
        comment=self.get_video_metadata(continuation_token)
        return comment

    #------------------------------------------COMMENTS-----------------------------------------------------------


    #---------------------------------------------MAIN------------------------------------------------------------

    # def get_youtube_result(self,query):
    #     video_titles_lst, link_lst, avg_views = self.get_youtube_video_data(query)
    #     #time.sleep(1)

    #     # -------------------Average Likes-----------------------------------
    #     like_lst=[int(self.get_youtube_like_counts(url)) if self.get_youtube_like_counts(url) is not None else 0 for url in link_lst]
    #     avg_likes=round(sum(like_lst)/len(like_lst))

    #     # ------------------Average Comment---------------------------------
    #     comment_lst=[int(self.get_youtube_comment_counts(url)) if self.get_youtube_comment_counts(url) is not None else 0 for url in link_lst]
    #     avg_comment=round(sum(comment_lst)/len(comment_lst))
        
    #     # # -------------------Average Likes-----------------------------------
    #     # like_lst=[int(self.get_youtube_like_counts(url)) if self.get_youtube_like_counts(url) is not None else 0 for url in link_lst]
    #     # avg_likes=round(sum(like_lst)/len(like_lst))
        
    #     main={
    #     'top_five_video_titles':video_titles_lst,
    #     'avg_views':avg_views,
    #     'avg_likes':avg_likes,
    #     'avg_comments':avg_comment
    #     }
    #     return main
    
    def get_youtube_result(self, query):
        #print(time.localtime())
        video_titles_lst, link_lst, avg_views = self.get_youtube_video_data(query)
        #print('Video Link EXtracted')
        #print(time.localtime())
        # Fetch like counts and comment counts concurrently
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            like_counts = list(executor.map(self.get_youtube_like_counts, link_lst))
            #print('likes count Extracted')
            #print(time.localtime())
            comment_counts = list(executor.map(self.get_youtube_comment_counts, link_lst))
            #print('Comment Count Extracted')
            #print(time.localtime())

        # Calculate average likes and comments
        like_lst = [int(count) if count is not None else 0 for count in like_counts]
        avg_likes = round(sum(like_lst) / len(like_lst))
        #print('Avg Like DONE')
        #print(time.localtime())

        comment_lst = [int(count) if count is not None else 0 for count in comment_counts]
        avg_comment = round(sum(comment_lst) / len(comment_lst))
        #print("Avg Comment Done")
        #print(time.localtime())

        main = {
            'top_five_video_titles': video_titles_lst,
            'avg_views': avg_views,
            'avg_likes': avg_likes,
            'avg_comments': avg_comment
        }
        return main


    #---------------------------------------------MAIN-------------------------------------------------------------



# # -------------------------------Main Calling Class For youtube API call----------------------------------------------------#

#------------------------Get Youtube Tags and Save Search History Code----------------------------------------------------------

class GetYouTubeTagsView(APIView):
    """
    Search any query that you want and it provide you with relevant Top 5 Video tiles, avg count, avg likes etc...
    """
    def post(self, request):
        # Get the query from the request
        data = request.data
        query = data.get('query')
        #query = request.POST.get('query')
        
        #-----------------------------------------------------New Code---------------------------------------
        
        user_id = get_user_id_from_token(request)

        # Create an instance of your InstaHashTag_new class
        youtube_instance = YoutubeHashTag_new()
        
        
        try:
            # Call the get_hashtags method to get the desired data
            user = CustomUser.objects.filter(id=user_id).first()
            if user.credit < 10 :
                msg = 'Insufficient credit to perform this action.'
                return Response({"Hashtag": query, "Message": msg}, status=status.HTTP_402_PAYMENT_REQUIRED)
            
            if not 'query' in request.data and not request.data['query']:
                msg = 'could not found the query'
                return Response({'Message' : msg}, status=status.HTTP_400_BAD_REQUEST)


            i_bot = Bot(user=user)
            twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
            past_searched_hashtag = SearchedHistory.objects.filter(hashtag=query, created__gte=twenty_four_hours_ago, platform="Youtube1")
            # Check if the hashtag/query is in past_searched_hashtag
            
            if not past_searched_hashtag :
                #Hastag = self.get_related_keywords(request.data['tag'])
                Hastag = youtube_instance.get_youtube_result(f'{query}')
            else :
                try :
                    Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['query'],created__gte=twenty_four_hours_ago,platform="Youtube1").first().result.replace("'", "\""))
                except :
                    try :
                        Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['query'],created__gte=twenty_four_hours_ago,platform="Youtube1").first().result)
                    except :
                        msg = 'Failed to scrape the hashtag'
                        return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
                

        except Exception as e:
            error_message = str(e)
            if "max() arg is an empty sequence" in error_message:
                return JsonResponse({'Message': 'Please enter a valid query.'}, status=400)
            else:
                return JsonResponse({'Message': f'Error occurred: {error_message}'}, status=400)

        # Check if hashtag_data is retrieved successfully
        if Hastag:
            msg = 'Hashtag scraped successfully'
            # Save to history if not found in past_searched_hashtag
            if Hastag:
                if not past_searched_hashtag :
                    SearchedHistory.objects.create(
                        user = user,
                        hashtag = request.data['query'],
                        platform = "Youtube1",
                        result = json.dumps(Hastag)
                    )
                    user.credit= user.credit - 10
                    user.save()
            # Convert to JSON if it's a string
            if isinstance(Hastag, str): 
                Hastag = json.loads(Hastag.replace("'", "\""))
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_200_OK)
        else:
            msg = 'Failed to scrape the hashtag'
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)



#------------------------Get Youtube Tags and Save Search History Code----------------------------------------------------------


#--------------------------------Instagram Hashtag Search By Adil--------------------------------------------------------------

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
class InstaHashTag_new(APIView):
    # ------------------------------------ First Block  Start-----------------------------------------------------------------------------------------------

    def get_instagram_cookies(self, username, password):
        # Use the Instagram login URL
        login_url = 'https://www.instagram.com/accounts/login/'

        # Create a headless browser (you may need to install the appropriate driver)
        driver = webdriver.Chrome()

        # Navigate to the Instagram login page
        driver.get(login_url)

        # Wait for the page to load
        time.sleep(2)

        # Find the username and password fields and fill them with your credentials
        username_field = driver.find_element(By.NAME, 'username')
        username_field.send_keys(username)

        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)

        # Submit the login form
        login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()

        # Wait for the login process to complete
        time.sleep(5)

    

        response_cookie=driver.get_cookies()

        return response_cookie
    

    def check_login(self, username, password):
        driver = None  # Initialize driver variable
        try:            
            if os.path.exists(f'cookies/cookies_{username}.txt'):
                with open(f'cookies/cookies_{username}.txt', 'r') as file:
                    cookies_data = json.load(file)  # Assuming the cookies data is stored as a Python list

                    sessionid = None
                    csrftoken = None

                    for cookie in cookies_data:
                        if cookie.get('name') == 'sessionid':
                            sessionid = cookie.get('value')
                        elif cookie.get('name') == 'csrftoken':
                            csrftoken = cookie.get('value')

                    # Check if cookies are expired or used for 30 times
                    if self.are_cookies_expired(cookies_data) or self.cookies_used_too_many_times(username):
                        print("Cookies are expired or used too many times. Obtaining new cookies.")
                        raise Exception("Cookies expired or used too many times")

                    print('Cookies file exists')
                return driver, csrftoken, sessionid

        except Exception as e:
            print(e)
            print("An error occurred while loading cookies file")

        try:
            response_cookie = self.get_instagram_cookies(username, password)
            # response_cookie = json.loads(response_cookie)
            sessionid = None
            csrftoken = None

            for cookie in response_cookie:
                if cookie.get('name') == 'sessionid':
                    sessionid = cookie.get('value')
                elif cookie.get('name') == 'csrftoken':
                    csrftoken = cookie.get('value')

            # sessionid = response_cookie['sessionid']
            # csrftoken = response_cookie['csrftoken']
            cookies = response_cookie
            with open(f'cookies/cookies_{username}.txt', 'w') as file:
                json.dump(cookies, file)
            print('User has been logged in')
            return driver, csrftoken, sessionid

        except Exception as e:
            print(e)
            print("An error occurred while obtaining new cookies")
            return None, None, None


    def are_cookies_expired(self, cookies_data):
        if not cookies_data:
            return True
        
        for cookie in cookies_data:
            if 'expiry' in cookie:
                if cookie['expiry'] < int(time.time()):
                    return True
        
        return False


    def cookies_used_too_many_times(self, username):
        # Implement logic to check if the cookies in the file have been used too many times
        # For example, you can keep track of the number of times the cookies have been used in a separate file or database
        # Here's a simplified example assuming you have a counter stored in a file
        counter_file = f'cookies/counter_{username}.txt'
        if os.path.exists(counter_file):
            with open(counter_file, 'r') as file:
                counter = int(file.read().strip())
            if counter >= 10:
                # Reset the counter to 1
                with open(counter_file, 'w') as file:
                    file.write('1')
                return True
            else:
                # Increment the counter
                counter += 1
                with open(counter_file, 'w') as file:
                    file.write(str(counter))
        else:
            # Initialize the counter file if it doesn't exist
            with open(counter_file, 'w') as file:
                file.write('1')
        return False


    
    def get_hashtags(self,query,csrftoken,sessionid):
        # RIGHT NOW i HAVE JUST HARD CODED THESE VALUES
        csrftoken= csrftoken
        sessionid= sessionid

        url = "https://www.instagram.com/api/graphql"
        dct={}

        headers = {
            "Accept": "*/*",
            #"Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.instagram.com",
            "Referer": "https://www.instagram.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "X-Asbd-Id": "129477",
            "X-Csrftoken": csrftoken,
            "X-Fb-Friendly-Name": "PolarisSearchBoxRefetchableQuery",
            "X-Fb-Lsd": "NFayaAYxCIr2sjmcgk81Be",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
            "Sec-Ch-Ua-Full-Version-List": '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.83", "Chromium";v="121.0.6167.85"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Model": '""',
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Ch-Prefers-Color-Scheme": "light",
        "Origin-Agent-Cluster": "?0",
        "Permissions-Policy": "accelerometer=(self), ambient-light-sensor=(), bluetooth=(), camera=(self), display-capture=(), fullscreen=(self), gamepad=(), geolocation=(self), gyroscope=(self), hid=(), idle-detection=(), keyboard-map=(), local-fonts=(), magnetometer=(), microphone=(self), midi=(), otp-credentials=(), payment=(), picture-in-picture=(self), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), window-management=()",
        "Permissions-Policy-Report-Only": "autoplay=(), clipboard-read=(), clipboard-write=(), encrypted-media=(), xr-spatial-tracking=()",
        "Pragma": "no-cache",
        "Priority": "u=1,i",
        "Report-To": "{\"max_age\":2592000,\"endpoints\":[{\"url\":\"https://www.facebook.com/browser_reporting/coop/?minimize=0\"}],\"group\":\"coop_report\",\"include_subdomains\":true}, {\"max_age\":86400,\"endpoints\":[{\"url\":\"https://www.facebook.com/browser_reporting/coep/?minimize=0\"}],\"group\":\"coep_report\"}, {\"max_age\":259200,\"endpoints\":[{\"url\":\"https://www.instagram.com/error/ig_web_error_reports/?device_level=unknown\"}]}",
        "Reporting-Endpoints": "coop_report=\"https://www.facebook.com/browser_reporting/coop/?minimize=0\", coep_report=\"https://www.facebook.com/browser_reporting/coep/?minimize=0\", default=\"https://www.instagram.com/error/ig_web_error_reports/?device_level=unknown\"",
        "Strict-Transport-Security": "max-age=31536000; preload; includeSubDomains",
        "Vary": "Origin, Accept-Encoding",
        "X-Content-Type-Options": "nosniff",
        "X-Fb-Debug": "1JRBkBdBnQsRcYj130p54bbE2I5021ciwlckKMYy9bLVarSQOQyzuLgq8TUN9fjXFHP0JLrvHPW1RkY8O3BjCA==",
        "X-Frame-Options": "DENY",
        "X-Xss-Protection": "0",
        }

        payload = {
            "av": 17841432819377428,
            "__d": "www",
            "__user": 0,
            "__a": 1,
            "__req": "1p",
            "__hs": "19754.HYP:instagram_web_pkg.2.1..0.1",
            "dpr": 1.5,
            "__ccg": "UNKNOWN",
            "__rev": 1011158543,
            "__s": "f5eww0:cx3okz:ike52g",
            "__hsi": 7330629208565479708,
            "__dyn": "7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2iyovw8OfK0EUjwGzEaE7622362W2K0zK5o4q3y1Sx-0iS2Sq2-azqwt8dUaob82cwMwrUdUbGwmk1xwmo6O1FwlE6PhA6bxy4UjK5V8",
            "__csr": "gvMCx5gH9sLEIzti9QhiH8LH_898yqZaVZvmAuVrAmFqzqF3EJalyEFVIyt4Gaauy3bXx0xemqlaBGECeF3ryWAh-H-WjCKcVoV3aAxucyeEjwCg9e4po5G2qbw05dUwur9w9ro1U404mE0mTPF6OF1fgO0X898owo81cpU1PO05Sw9SOm0KU1qK0ia0qS1_wtUgwzg9EV00aAa",
            "__comet_req": 7,
            "fb_dtsg": "NAcMv12OeUaZP1Y9tFln7RbaZZUwyZiFL5xvz3ucV--Nvwadj5zfDgA:17864970403026470:1706794861",
            "jazoest": 26361,
            "lsd": "NFayaAYxCIr2sjmcgk81Be",
            "__spin_r": 1011158543,
            "__spin_b": "trunk",
            "__spin_t": 1706795117,
            "fb_api_caller_class": "RelayModern",
            "fb_api_req_friendly_name": "PolarisSearchBoxRefetchableQuery",
            "variables": f'{{"data":{{"context":"blended","include_reel":"true","query":"#{query}","rank_token":"","search_surface":"web_top_search"}},"hasQuery":true}}',
            "server_timestamps": True,
            "doc_id": 6901177919928333,
        }

        response = requests.post(url, headers=headers, data=payload)
        
        hashtag_list = []
        for i in range(len(response.json()['data']['xdt_api__v1__fbsearch__topsearch_connection']['hashtags'])):
            hashtag_info = {
                "hashtag": response.json()['data']['xdt_api__v1__fbsearch__topsearch_connection']['hashtags'][i]['hashtag']['name'],
                "total_post": response.json()['data']['xdt_api__v1__fbsearch__topsearch_connection']['hashtags'][i]['hashtag']['media_count'],
                "rank": 1 + i,
                "link": f'https://www.instagram.com/explore/tags/{response.json()["data"]["xdt_api__v1__fbsearch__topsearch_connection"]["hashtags"][i]["hashtag"]["name"]}/'
            }
            hashtag_list.append(hashtag_info)
        
        return hashtag_list

    # ------------------------------------ First Block End -----------------------------------------------------------------------------------------------



#     -------------------------- Average Calculation Block-------------------------------------------------------------
    def count_reel_tag(self,json_data):
        target_tag='video_length'
        count = 0

        if isinstance(json_data, list):
            for item in json_data:
                count += self.count_reel_tag(item)
        elif isinstance(json_data, dict):
            for key, value in json_data.items():
                if key == target_tag:
                    count += 1
                count += self.count_reel_tag(value)

        return count

    
    
    def get_average_like_count(self,json_object):
        total_like_count = 0
        total_items = 0

        if isinstance(json_object, dict):
            for key, value in json_object.items():
                if key == 'like_count':
                    total_like_count += value
                    total_items += 1
                elif isinstance(value, (dict, list)):
                    count, items = self.get_average_like_count(value)
                    total_like_count += count
                    total_items += items

        elif isinstance(json_object, list):
            for item in json_object:
                count, items = self.get_average_like_count(item)
                total_like_count += count
                total_items += items

        if total_items > 0:
            return total_like_count, total_items
        else:
            return 0, 0  # Return 0 for both total_like_count and total_items if there are no items

    
    def get_average_comment_count(self,json_object):
        total_comment_count = 0
        total_items = 0

        if isinstance(json_object, dict):
            for key, value in json_object.items():
                if key == 'comment_count':
                    total_comment_count += value
                    total_items += 1
                elif isinstance(value, (dict, list)):
                    count, items = self.get_average_comment_count(value)
                    total_comment_count += count
                    total_items += items

        elif isinstance(json_object, list):
            for item in json_object:
                count, items = self.get_average_comment_count(item)
                total_comment_count += count
                total_items += items

        return total_comment_count, total_items
    
    
    
#     -------------------------- Average Calculation Block-------------------------------------------------------------




    # ------------------------------------ Second Block Start -----------------------------------------------------------------------------------------------


    def count_tags_all(self,tag_list,csrftoken,sessionid):
        # RIGHT NOW i HAVE JUST HARD CODED THESE VALUES
        csrftoken= csrftoken
        sessionid= sessionid


        lst=[]
        main={}
        
        
        # Define the API endpoint
        url = "https://www.instagram.com/api/v1/tags/web_info/"
        for i in range(len(tag_list)):
#             print(i)
            if i==0:
                query=tag_list[i]['hashtag']
                ranking=tag_list[i]['rank']
                total_post=tag_list[i]['total_post']
                # Define the query parameters
                params = {"tag_name": f"{query}"}

                # Define the headers
                # Define headers
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                    "Accept": "*/*",
                    "Accept-Language": "en-US,en;q=0.9,ko;q=0.8",
                    "Referer": "https://www.instagram.com",
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "Dpr": "1.25",
                    "Sec-Ch-Prefers-Color-Scheme": "light",
                    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
                    "Sec-Ch-Ua-Full-Version-List": '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.128", "Chromium";v="121.0.6167.184"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Model": '""',
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
                    "Sec-Fetch-Dest": "empty",
                    "Sec-Fetch-Mode": "cors",
                    "Sec-Fetch-Site": "same-origin",
                    "Viewport-Width": "744",
                    "X-Asbd-Id": "129477",
                    "X-Csrftoken": csrftoken,  # Replace with your actual csrftoken
                    "X-Ig-App-Id": "936619743392459",
                    "X-Ig-Www-Claim": "hmac.AR2aC1xHaqmnod4qoRG9Dil2v4H1H21pxuX_IGEyaetED4Fv",
                    "X-Requested-With": "XMLHttpRequest",
                }

                cookies = {
                    "csrftoken": csrftoken,
                    "sessionid": sessionid,
                }
                # print({
                #     "csrftoken": csrftoken,
                #     "sessionid": sessionid,
                # })
                # Make the GET request
                response = requests.get(url, params=params, headers=headers, cookies=cookies)

                #total_post=response.json()['count']
                hashtag_name=query
                kk=response.json()

                #-------------------------------------------------- Avg_comment -------------------------------------------------#
                
                comment_count, total_items = self.get_average_comment_count(kk)
                if total_items > 0:
                    average_comment_count = comment_count / total_items
                average_comment_count= round(average_comment_count)

                #------------------------------------------------ Reel_percentage -----------------------------------------------#
                reel_percentage=round((self.count_reel_tag(kk)/total_items)*100)


                #------------------------------------------------- Avg_likes ----------------------------------------------------#
                total_like_count, total_items = self.get_average_like_count(kk)
                if total_items > 0:
                    average_like_counts = total_like_count / total_items
                else:
                    average_like_counts = 0
                average_like_count=round(average_like_counts)



                main_second={
                        "hashtag": hashtag_name,
                        "total_post": total_post,
                        "rank": ranking,
                        "likes": average_like_count,
                        "comment": average_comment_count,
                        "reels": f"{reel_percentage} %",


                    }


                lst.append(main_second)
#                 print(main_second)
            else:
                query=tag_list[i]['hashtag']
                ranking=tag_list[i]['rank']
                total_post=tag_list[i]['total_post']
                
                main_second={
                        "hashtag": query,
                        "total_post": total_post,
                        "rank": ranking
                    }
                lst.append(main_second)
                
                

        main['Hashtag']=lst
        
        return main
        
        
    # ------------------------------------ Second Block End -----------------------------------------------------------------------------------------------     


    # ---------------------------------------CPC Function Start--------------------------------------------------------------------------------------------


    def get_ranking(self,data) :
            for item in data["Hashtag"]:
                item["total_post"] = int(str(item["total_post"]).replace(",", ""))

            max_posts = max([item['total_post'] for item in data["Hashtag"]])

            referanceposts = sum([item['total_post'] for item in data["Hashtag"]])
            
            referance_cpc = 5
            referance_total_post = 1000000000
            total_post_ration = referanceposts/referance_total_post
            estimated_base_cpc = referance_cpc * total_post_ration

            # Perform normalization and scoring calculations
            total_hashtags = len(data["Hashtag"])  # Total number of hashtags
            normalized_data = []
            for index, item in enumerate(data["Hashtag"]):
                normalized_rank = 1 - ((index + 1) / total_hashtags)  # Rank normalization
                normalized_posts = item["total_post"] / max_posts
                combined_score = (0.4 * normalized_rank) + (0.6 * normalized_posts)  

                item_data = {
                    "hashtag": item["hashtag"],
                    "total_post": item["total_post"],
                    "rank" : index,
                    "combined_score": combined_score
                }
                if 'likes' in item : item_data['likes'] = item['likes']
                if 'comment' in item : item_data['comment'] = item['comment']
                if 'reels' in item : item_data['reels'] = item['reels']
                normalized_data.append(item_data)

            # Set thresholds for competition levels
            low_comp_threshold = 0.3
            med_comp_threshold = 0.6

            # Categorize based on competition levels
            for item in normalized_data:
                item['rank'] += 1
                if item["combined_score"] <= low_comp_threshold:
                    item["competition_level"] = "Low Competition"
                    item["CPC"] = round(estimated_base_cpc*0.8,3)
                elif low_comp_threshold < item["combined_score"] <= med_comp_threshold:
                    item["competition_level"] = "Medium Competition"
                    item["CPC"] = round(estimated_base_cpc*1.0,3)
                else:
                    item["CPC"] = round(estimated_base_cpc*1.2,3)
                    item["competition_level"] = "High Competition"


            return normalized_data
    


    # ---------------------------------------CPC Function Start--------------------------------------------------------------------------------------------

    
# -------------------------------Main Class For Instagram API call----------------------------------------------------#
    
            


class GetInstaTagsView(APIView):
    def post(self, request):
        # Get the query from the request
        insta_user_list = instagram_accounts.objects.filter(status='ACTIVE')
        if not insta_user_list:
            return JsonResponse({'Message': "No User is Active"}, status=400)
        
        insta_user = insta_user_list.first()

        # Parse JSON data from request body
        data = request.data
        query = data.get('query')

        username = insta_user.username
        password = insta_user.password
        
        user_id = get_user_id_from_token(request)
        
        #user_id = insta_user.id  # Update to get user_id from insta_user

        # Create an instance of your InstaHashTag_new class
        insta_instance = InstaHashTag_new()
        
        # Call the check_login method to ensure the user is logged in
        drivers, csrftoken, sessionid = insta_instance.check_login(username, password)
        
        try:
            # Call the get_hashtags method to get the desired data
            user = CustomUser.objects.filter(id=user_id).first()

            if user.credit < 10 :
                msg = 'Insufficient credit to perform this action.'
                return Response({"Hashtag": query, "Message": msg}, status=status.HTTP_402_PAYMENT_REQUIRED)
            
            if not 'query' in request.data and not request.data['query']:
                msg = 'could not found the query'
                return Response({'Message' : msg}, status=status.HTTP_400_BAD_REQUEST)

            i_bot = Bot(user=user)
            twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
            past_searched_hashtag = SearchedHistory.objects.filter(hashtag=query, created__gte=twenty_four_hours_ago, platform="Instagram")
            # Check if the hashtag/query is in past_searched_hashtag
            if not past_searched_hashtag:
                for _ in range(3):
                    json_data = insta_instance.get_hashtags(query, csrftoken, sessionid)
                    response_json = insta_instance.count_tags_all(json_data, csrftoken, sessionid)
                    hashtag_data = insta_instance.get_ranking(response_json)
                    if len(hashtag_data) > 5:
                        break
                else:
                    msg = 'Failed to scrape the hashtag'
                    return Response({"Hashtag": hashtag_data, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

            else:
                try:
                    hashtag_data = json.loads(SearchedHistory.objects.filter(hashtag=query, created__gte=twenty_four_hours_ago, platform="Instagram").first().result.replace("'", "\""))
                except:
                    try:
                        hashtag_data = json.loads(SearchedHistory.objects.filter(hashtag=query, created__gte=twenty_four_hours_ago, platform="Instagram").first().result)
                    except:
                        msg = 'Failed to scrape the hashtag'
                        return Response({"Hashtag": hashtag_data, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
                

        except Exception as e:
            error_message = str(e)
            if "max() arg is an empty sequence" in error_message:
                return JsonResponse({'Message': 'Please enter a valid query.'}, status=400)
            else:
                return JsonResponse({'Message': f'Error occurred: {error_message}'}, status=400)

        # Check if hashtag_data is retrieved successfully
        if hashtag_data:
            msg = 'Hashtag scraped successfully'
            # Save to history if not found in past_searched_hashtag
            if not past_searched_hashtag:
                SearchedHistory.objects.create(
                    user=user,
                    hashtag=query,
                    platform='Instagram',
                    result=json.dumps(hashtag_data)
                )
                user.credit -= 10  # Deduct credits from the user
                user.save()
            # Convert to JSON if it's a string
            if isinstance(hashtag_data, str): 
                hashtag_data = json.loads(hashtag_data.replace("'", "\""))
            return Response({"Hashtag": hashtag_data, "Message": msg}, status=status.HTTP_200_OK)
        else:
            msg = 'Failed to scrape the hashtag'
            return Response({"Hashtag": hashtag_data, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
        


# -------------------------------Main Class For Instagram API call----------------------------------------------------#


#--------------------------------Instagram Hashtag Search By Adil--------------------------------------------------------------