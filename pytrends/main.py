from pytrends.request import TrendReq
import pandas as pd, random, json, os

def generate_interest_trends(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Convert the 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Set the 'date' column as the index
    df.set_index('date', inplace=True)

    # Resample the data to get weekly, monthly, and yearly sums
    weekly_data = df['ram'].resample('W').sum()
    monthly_data = df['ram'].resample('M').sum()
    yearly_data = df['ram'].resample('Y').sum()

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
        "weekly_interest": weekly_json,
        "monthly_interest": monthly_json,
        "yearly_interest": yearly_json
    }

    return result_dict

def csv_to_json(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Convert the DataFrame to JSON format
    json_data = df.to_json(orient='records')

    return json_data

def get_trend_data(keyword):
    pytrends = TrendReq(hl='en-US', tz=360)  # Set your desired language and timezone

    # Build payload for the given keyword
    pytrends.build_payload([keyword], cat=0, timeframe='today 5-y', geo='', gprop='youtube')
    file_name = f'{random.randint(10000,10000000)}.csv'
    pytrends.interest_over_time().to_csv(file_name)
    interest_over_time_data = generate_interest_trends(file_name)
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


if __name__ == "__main__":
    keyword = "ram"
    trend_data = get_trend_data(keyword)

    # Display the trend data
    print(trend_data,'----')