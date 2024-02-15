from django.urls import path, include
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('api/register/', UserRegistrationView.as_view(), name='api-register'),
    path('api/verification/', UserEmailVerificationView.as_view(), name='api-register'),
    path('api/login/', UserLoginView.as_view(), name='api-login'),
    path('api/refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('api/profile/', UserProfileView.as_view(), name='api-profile'),
    path('api/forgotpassword/', ForgotPasswordView.as_view(), name='api-forgotpassword'), #Adil
    path('api/changepassword/', UserChangePasswordView.as_view(), name='api-changepassword'),
    path('api/send-email/', send_email.as_view(), name='api-send-email'), # email is not sending
    path('api/diposite-money/', DepositeMoneyAPI.as_view(), name='diposite-money'), # email is not sending
    #path('api/get-insta-tags/', InstaHashTag.as_view(), name='get-insta-tags'), # Function changed By Adil
    path('api/get-insta-tags/', GetInstaTagsView.as_view(), name='get-insta-tags'), # Function changed By Adil
    path('api/get-insta-history/', InstaHashTagHistory.as_view(), name='get-insta-history'),
    path('api/get-youtube-tags/', YouTubeHashTag.as_view(), name='get-youtube-tags'), 
    path('api/get-youtube-tags-new/', GetYouTubeTagsView.as_view(), name='get-youtube-tags-new'), # Function Added By Adil
    path('api/get-youtube-history/', YoutubeHashTagHistory.as_view(), name='get-youtube-history'),
    path('api/get-users-list/', GetUserList.as_view(), name='get-users-list'),
    path('api/get-diposite-list/', GetDipositeList.as_view(), name='get-diposite-list'),
    path('api/edit-user/', EditUser.as_view(), name='user-edit'),
    path('api/user-delete/', DeleteUser.as_view(), name='user-delete'),
    path('api/superuser-dashboard/', SuperuserDashboard.as_view(), name='superuser-dashboard'),
]