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
        print(user_driver_dict)
        if driver:
            try :
                user = CustomUser.objects.filter(id=user_id).first()
                i_bot = Bot(user=user)
                if i_bot.TestRunDriver(driver) == False :
                    driver,keys,value = self.give_driver(CreateNew=True)
                    
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
                    
                    SearchedHistory.objects.create(
                        user = user,
                        hashtag = request.data['hashtag'],
                        platform = 'Instagram',
                        result = json.dumps(Hastag)
                    )
                    return Response({"Hashtag": Hastag, "Message": msg},status=status.HTTP_200_OK)
                else:
                    msg = 'Failed to scrape the hashtag'
                    return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)
            except :
                msg = 'Failed to scrape the hashtag'
            finally :
                value['status'] = True
                if msg == "Hashtag scraped successfully" :
                    return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_200_OK)
                return Response({"Hashtag": Hastag, "Message": msg}, status=status.HTTP_400_BAD_REQUEST)

        else:
            msg = 'All drivers are busy!'
            return Response({"Message": msg}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class start_drivers(APIView):

    def post(self, request, format=None):
        try :
            return JsonResponse({"Hastag" : "hashtag"})
        except Exception as e :
            return JsonResponse({"Hastag" : "hashtag"})
        
