import requests

# Replace 'USER_ACCESS_TOKEN' with the actual user access token
access_token = 'IGQWRQVUNSQlVJVUYwdDBaTWNYSk91bUg5SC1VZADlvQkgyTVdpUUplR1QtRGVhNUhPb3VqNFNUZAlBLdWFSeF9kNl9WTlRhd2tUdFY0ckpvQjk1YTd1QXFVQ2U2SzVYaUttTkZAHOFo0QXE3Yl9veTNmWE53b3dUNjAZD'


# Replace 'ACCESS_TOKEN' and 'HASHTAG' with your actual access token and hashtag
hashtag = '17841516322080859'

api_endpoint = f'https://graph.instagram.com/v12.0/{hashtag}/recent_media'

# Make the API request
response = requests.get(api_endpoint, params={'access_token': access_token})

# Print the response
print(response.json())

