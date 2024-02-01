from .models import instagram_accounts
from .bot import Bot
from dotenv import load_dotenv
from datetime import timedelta, datetime
import random, time, os, json, pytz
from home.models import CustomUser, SearchedHistory, instagram_accounts, DepositeMoney

load_dotenv()
import subprocess

def get_search_history(week_num : int, platform_ : str) :
    tz = pytz.timezone('UTC')
    now = datetime.now().astimezone(tz)
    
    Weekly_search = []
    for i in range(week_num):
        # Calculate the start and end of the week
        end_of_week = now - timedelta(days= 6*i  )
        start_of_week = end_of_week - timedelta(days=6)

        # Query to get data created in this week
        week_data = SearchedHistory.objects.filter(created__gte=start_of_week,  created__lte=end_of_week,platform=platform_)

        # Add the query results to the list
        Weekly_search.append(week_data)
        
    main_weekly_search = []
    for week in Weekly_search :
        if not week :
            main_weekly_search.append({
                Weekly_search.index(week)+1 : {
                    "total_search" : 0,
                    'weekly_search' : []
                }
            })
        else :
            search_his = [ {src.id : { "hashtag" : src.hashtag, "user" : src.user.email} } for src in week]
            main_weekly_search.append( {
                Weekly_search.index(week)+1 : {
                    "total_search" : len(search_his),
                    'weekly_search' :  search_his
                }
            })
    return main_weekly_search
                

def generate_random_string(length=10):
    import random, string
    # Define the characters you want to include in the random string
    characters = string.ascii_letters 

    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string

def GetActiveChromeSelenium():
    # subprocess.run(['pkill', 'chrome'])

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

