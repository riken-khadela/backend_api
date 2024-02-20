from .models import instagram_accounts
from .bot import Bot
from dotenv import load_dotenv
from datetime import timedelta, datetime
import random, time, os, json, pytz
from home.models import CustomUser, SearchedHistory, instagram_accounts, DepositeMoney


from pytrends.request import TrendReq
import pandas as pd, random, json, os

def generate_interest_trends(csv_path,keyword):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Convert the 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Set the 'date' column as the index
    df.set_index('date', inplace=True)

    # Resample the data to get weekly, monthly, and yearly sums
    weekly_data = df[keyword].resample('W').sum()
    monthly_data = df[keyword].resample('M').sum()
    yearly_data = df[keyword].resample('Y').sum()

    # Convert the results to JSON format with the desired date format
    weekly_json = weekly_data.reset_index().to_json(orient='records', date_format='iso')
    monthly_json = monthly_data.reset_index().to_json(orient='records', date_format='iso')
    yearly_json = yearly_data.reset_index().to_json(orient='records', date_format='iso')

    # Modify the date format in the JSON strings
    weekly_json = weekly_json.replace('T00:00:00.000', '')
    monthly_json = monthly_json.replace('T00:00:00.000', '')
    yearly_json = yearly_json.replace('T00:00:00.000', '')

    # Create a dictionary to store the results
    result_dict = {
        "weekly_interest": json.loads(weekly_json),
        "monthly_interest": json.loads(monthly_json),
        "yearly_interest": json.loads(yearly_json)
    }

    return result_dict

def csv_to_json(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Convert the DataFrame to JSON format
    json_data = df.to_json(orient='records')

    return json.loads(json_data)

def get_yt_trend_data(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)  # Set your desired language and timezone

    # Build payload for the given keyword
    pytrends.build_payload([keyword], cat=0, timeframe='today 5-y', geo='', gprop='youtube')
    file_name = f'{random.randint(10000,10000000)}.csv'
    pytrends.interest_over_time().to_csv(file_name)
    interest_over_time_data = generate_interest_trends(file_name,keyword)
    pytrends.interest_by_region().to_csv(file_name)
    interest_by_region_data = csv_to_json(file_name)
    if type(interest_by_region_data) == str:
        interest_by_region_data = json.loads(interest_by_region_data)
    
    if os.path.exists(os.path.join(os.getcwd(),file_name)) : 
        os.remove(os.path.join(os.getcwd(),file_name))
        
    return {
        "interest_by_time" : interest_over_time_data,
        "interest_by_region" : interest_by_region_data
    }

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

        print("start_of_week------------->4444444444444444444444444444444444444",end_of_week)
        print("start_of_week------------->4444444444444444444444444444444444444",start_of_week)

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
            #print("Week data 281787234782348747",week)
            #print("search_his------->8723t72t4t8234",search_his)
            main_weekly_search.append( {
                Weekly_search.index(week)+1 : {
                    "total_search" : len(search_his),
                    'weekly_search' :  search_his
                }
            })
    return main_weekly_search

def get_search_history_(platform_: str, start_date: datetime = None, end_date: datetime = None):
    tz = pytz.timezone('UTC')
    now = datetime.now().astimezone(tz)
    Weekly_search = []    
    if end_date ==None:

        week_data = SearchedHistory.objects.filter(created__gte=start_date,  created__lte=now, platform=platform_)
        Weekly_search.append(week_data)
            # Add the query results to the list
    elif end_date !=None and start_date !=None:
        
        week_data = SearchedHistory.objects.filter(created__gte=start_date,  created__lte=end_date, platform=platform_)
        Weekly_search.append(week_data)
    else:
        print("Provide valid Date Range")
        week_data=None

        Weekly_search.append(week_data)
            
    main_weekly_search = []
    for week in Weekly_search :
        if not week :
            main_weekly_search.append({
                Weekly_search.index(week)+1 : {
                    "total_search_count" : 0,
                    'search_history' : []
                }
            })
        else :
            search_his = [ {src.id : { "hashtag" : src.hashtag, "user" : src.user.email} } for src in week]
            #print("search_his------->8723t72t4t8234",search_his)
            main_weekly_search.append( {
                Weekly_search.index(week)+1 : {
                    "total_search_count" : len(search_his),
                    'search_history' :  search_his
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

