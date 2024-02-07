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
from .utils import GetActiveChromeSelenium, get_yt_trend_data, scrape_hashtags,get_user_id_from_token, generate_random_string, get_search_history
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
            return Response({'msg':'email field is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        if 'super' in request.data and request.data['super'] == True : 
            user.is_superuser = True
            user.save()
        token = get_tokens_for_user(user)
        verification_code = random.randint(100000,999999)
        user.verification_code = verification_code
        user.save()
        subject = 'Verification code is here'
        message = f'verification code : {verification_code}'
        from_email = 'info@keywordlit.com'
        recipient_list = [user.email]   
        send_mail(subject, message, from_email, recipient_list)            
        return Response({'token':token, "email" : 'email verification code has been set' ,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserEmailVerificationView(APIView):
    """ 
    To verify user needs to send email and verification 
    """
    def post(self, request):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')

        user = CustomUser.objects.filter(email=email, verification_code=verification_code).first()
        if user :
            user.is_user_verified = True
            user.save()
            return Response({'message': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        else :
            try :
                verification_code = random.randint(100000,999999)
                user.verification_code = verification_code
                user.save()
                subject = 'Verification code is here'
                message = f'verification code : {verification_code}'
                from_email = 'info@keywordlit.com'
                recipient_list = [email]   
                send_mail(subject, message, from_email, recipient_list) 
                send_verification_code = True
            except : 
                send_verification_code = False

            return Response({'message': 'Invalid verification code.','ResendVerificationCode' : send_verification_code}, status=status.HTTP_400_BAD_REQUEST)

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

            return Response({'token':token,'verified' : user.is_user_verified, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class RefreshTokenView(APIView):
    """
    Send a refresh token to get a new access token.
    """
    def post(self, request, format=None):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = RefreshToken(refresh_token)
            access_token = refresh_token.access_token
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

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
                    breakpoint()
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
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_401_UNAUTHORIZED)
        if user.credit < 10 :
            msg = 'Insufficient credit to perform this action.'
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        if not 'tag' in request.data and not request.data['tag']:
            msg = 'could not found the tag'
            return Response({'msg' : msg}, status=status.HTTP_400_BAD_REQUEST)
        
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        past_searched_hashtag = SearchedHistory.objects.filter(hashtag=request.data['tag'],created__gte=twenty_four_hours_ago,platform="Youtube")
        # breakpoint()
        if not past_searched_hashtag :
            Hastag = self.get_related_keywords(request.data['tag'])
        else :
            try :
                Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['tag'],created__gte=twenty_four_hours_ago,platform="Youtube").first().result.replace("'", "\""))
            except :
                try :
                    Hastag = json.loads(SearchedHistory.objects.filter(hashtag=request.data['tag'],created__gte=twenty_four_hours_ago,platform="Youtube").first().result)
                except :
                    msg = 'Failed to scrape the hashtag'
                    return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"Hashtag":  Hastag, "trend" : get_yt_trend_data(request.data['tag']), "Message": msg},status=status.HTTP_200_OK)
        else:
            msg = 'Failed to scrape the hashtag'
            return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_related_keywords(self, keyword_text):
        hashtags = []
        # Initialize the Google Ads client.
        client = GoogleAdsClient.load_from_storage("./conf.yaml")

        # Get the service.
        keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")

        # Set up the query parameters.
        #language = client.get_type("StringValue")
        language = "1000" # For English
        language_criterion_id = "1000"  # Criterion ID for English
        geo_target_criterion_id = "2840"  # Criterion ID for United States

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
                return Response({'msg' : 'counld not got the user list', 'email' : request.data['email']}, status=status.HTTP_204_NO_CONTENT)
                
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
            return Response({'msg' : 'successfully got the user list','userlist' : user_list}, status=status.HTTP_200_OK)
        return Response({'msg' : 'counld not got the user list', 'userlist' : user_list}, status=status.HTTP_204_NO_CONTENT)

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
                return Response({'msg' : 'counld not got the diposite', 'TransactionId' : request.data['TransactionId']}, status=status.HTTP_204_NO_CONTENT)
                
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
            return Response({'msg' : 'successfully got the user list','userlist' : diposite_list}, status=status.HTTP_200_OK)
        return Response({'msg' : 'counld not got the user list', 'userlist' : diposite_list}, status=status.HTTP_204_NO_CONTENT)

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
            return Response({'msg' : msg}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'feild' in request.data and not request.data['feild']:
            msg = 'could not found the feild which needs to be edited'
            return Response({'msg' : msg}, status=status.HTTP_400_BAD_REQUEST)
        
        if not 'new_value' in request.data and not request.data['new_value']:
            msg = 'could not found the new value which needs to be replaced with old values'
            return Response({'msg' : msg}, status=status.HTTP_400_BAD_REQUEST)
            
        found_user = CustomUser.objects.filter(is_superuser=False,email=request.data['email'])
        if not found_user :
            return Response({'msg' : 'could not got the user'}, status=status.HTTP_204_NO_CONTENT)

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

        
        return Response({'msg' : msg}, status=status_code)


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
                return Response({'msg' : 'successfully got the user list','user_deleted' : user_deleted}, status=status.HTTP_204_NO_CONTENT)

            del_user = del_user.first()
            if del_user.delete() :
                user_deleted = True

        if user_deleted :
            return Response({'msg' : 'successfully deleted the user list','user_deleted' : user_deleted}, status=status.HTTP_200_OK)
        return Response({'msg' : 'counld not delete the user', 'user_deleted' : user_deleted}, status=status.HTTP_204_NO_CONTENT)


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
                    
        return Response({'msg' : 'successfully get the data', 'data' : get_search_history(6,"Instagram")}, status=status.HTTP_200_OK)


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
                    
        return Response({'msg' : 'successfully get the data', 'data' : get_search_history(6,"Youtube")}, status=status.HTTP_200_OK)



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
        
        return Response({'msg' : msg, 'data' : responsee}, status=status.HTTP_200_OK)
        