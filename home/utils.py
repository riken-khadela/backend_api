from .models import instagram_accounts
from .bot import Bot
from dotenv import load_dotenv
load_dotenv()
import subprocess


def generate_random_string(length=10):
    import random, string
    # Define the characters you want to include in the random string
    characters = string.ascii_letters 

    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

def GetActiveChromeSelenium():
    subprocess.run(['pkill', 'chrome'])

    user_driver_dict = {}
    all_active_user = instagram_accounts.objects.filter(status='ACTIVE')
    for user in all_active_user : 
        i_bot = Bot(user=user)
        driver = i_bot.return_driver()
        if driver != False :
            user_driver_dict[user.username] = {
                'driver' : driver,
                'status' : True
                }
        
    return user_driver_dict

def scrape_hashtags(username,hashtag, driver):
    user = instagram_accounts.objects.filter(username=username).first()
    i_bot = Bot(user=user)
    return  i_bot.extract_tag(hashtag,driver)


from rest_framework_simplejwt.tokens import AccessToken

def get_user_id_from_token(request):
    # Assuming the token is present in the Authorization header
    authorization_header = request.headers.get('Authorization')

    if authorization_header:
        try:
            # Extracting the token part from the header
            token = authorization_header.split(' ')[1]
            # Decoding the token to retrieve the payload
            access_token = AccessToken(token)
            # Accessing the user ID from the decoded token payload
            user_id = access_token.payload.get('user_id')
            return user_id
        except Exception as e:
            print(f"Error decoding token: {e}")
    return None 