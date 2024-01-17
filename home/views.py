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
from .utils import GetActiveChromeSelenium, scrape_hashtags,get_user_id_from_token, generate_random_string
import random, time, os, json
from .bot import Bot
from datetime import timedelta, datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from urllib.parse import unquote

user_driver_dict = {}
    
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
                'result' : json.loads(history.result),
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
        
        return Response(jsonn_response, status=status.HTTP_200_OK)

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

        subject = 'Hello, Django Email111'
        message = 'This is a test email sent from a Django application.'
        from_email = 'info@keywordlit.com'
        recipient_list = [request.data['email']]   
        aa = send_mail(subject, message, from_email, recipient_list)
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
                'result' : json.loads(history.result)
            }
            search_history.append(tmp)
        msg = 'successfully searched userhistory !'
        return Response({ "search_history":search_history, "Message": msg}, status=status.HTTP_200_OK)

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
        
        driver,keys,value = self.give_driver()
        
        global user_driver_dict
        if driver:
            try :
                user = CustomUser.objects.filter(id=user_id).first()
                i_bot = Bot(user=user)

                twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
                past_searched_hashtag = SearchedHistory.objects.filter(hashtag=request.data['hashtag'],created__gte=twenty_four_hours_ago)
                if past_searched_hashtag : 
                    Hastag = json.loads(past_searched_hashtag.first().result)
                if i_bot.TestRunDriver(driver) == False :
                    driver,keys,value = self.give_driver(CreateNew=True)
                if not past_searched_hashtag :
                    for _ in range(3) :
                        Hastag = scrape_hashtags(keys,request.data['hashtag'], driver)
                        if len(Hastag) > 5: break
                    else:
                        msg = 'Failed to scrape the hashtag'
                        return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
                
                if Hastag:
                    user.credit= user.credit - 10
                    user.save()
                    msg = 'Hashtag scraped successfully'
                    if not past_searched_hashtag :
                        SearchedHistory.objects.create(
                            user = user,
                            hashtag = request.data['hashtag'],
                            platform = 'Instagram',
                            result = json.dumps(Hastag)
                        )
                    return Response({"Hashtag": self.get_ranking({"Hashtag": Hastag}), "Message": msg},status=status.HTTP_200_OK)
                else:
                    msg = 'Failed to scrape the hashtag'
                    return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
            except :
                msg = 'Failed to scrape the hashtag'
            finally :
                value['status'] = True
                if msg == "Hashtag scraped successfully" :
                    return Response({"Hashtag": self.get_ranking({"Hashtag": Hastag}), "Message": msg}, status=status.HTTP_200_OK)
                return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

        else:
            msg = 'All drivers are busy!'
            return Response({"Message": msg}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


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
        
        Hastag = self.get_related_keywords()
        if Hastag:
            user.credit= user.credit - 10
            user.save()
            msg = 'Hashtag scraped successfully'
            return Response({"Hashtag": self.get_ranking({"Hashtag": Hastag}), "Message": msg},status=status.HTTP_200_OK)
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
        
