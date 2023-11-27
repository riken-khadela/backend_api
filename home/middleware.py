# home/middleware.py
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Get the token from the request headers
            token = request.headers.get('Authorization').split()[1]
            # Decode and validate the token
            decoded_token = AccessToken(token, verify=False)
            decoded_token.verify()

            # Attach the user to the request object
            request.user = decoded_token.payload.get('user')
        except (InvalidToken, AttributeError, IndexError):
            # If the token is invalid or not present, set the user to AnonymousUser
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response
