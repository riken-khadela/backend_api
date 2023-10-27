from django.urls import path, include
from .views import *

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path('api/register/', UserRegistrationView.as_view(), name='api-register'),
    path('api/verification/', UserEmailVerificationView.as_view(), name='api-register'),
    path('api/login/', UserLoginView.as_view(), name='api-login'),
    path('api/profile/', UserProfileView.as_view(), name='api-profile'),
    path('api/changepassword/', UserChangePasswordView.as_view(), name='api-changepassword'),
    path('api/send-email/', send_email.as_view(), name='api-send-email'),
]