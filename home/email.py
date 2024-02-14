from django.core.mail import send_mail
import random
from django.conf import settings
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

# def send_otp_via_email(email):
#     subject = "Your Account Verification Email"
#     otp = random.randint(100000,999999)
#     message = f'Your otp is {otp}'
#     email_from = settings.EMAIL_HOST
#     send_mail(subject,message,email_from,[email])
#     user_obj = CustomUser.objects.get(email = email)
#     user_obj.otp = otp
#     user_obj.save()



def send_otp_via_email(email):
    try:
        user_obj = CustomUser.objects.get(email=email)
        # Now you can send the OTP email to the user
        # Example code for sending email...
        subject = 'Verification code is here'
        message = f'Your verification code is: {user_obj.verification_code}'
        from_email = 'info@keywordlit.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
    except ObjectDoesNotExist:
        # Handle the case where the user does not exist
        # For example, you can log the error or return a response indicating the error
        print(f"User with email {email} does not exist")

