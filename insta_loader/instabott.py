from instabot import Bot
import time
import os 
import glob
cookie_del = glob.glob("config/*cookie.json")
try:
    # Your code here
    os.remove(cookie_del[0])
except Exception as e:
    print(f'Error: {e}')
# Initialize the Instabot
bot = Bot()

# Log in to your Instagram account
bot.login(username="keywordlit7", password="Keywordlit-01")
breakpoint()

# Specify the hashtag you want to explore
hashtag = "shiva"

# Get the media IDs associated with the hashtag
media_ids = bot.get_hashtag_medias(hashtag)
bot.get_total_hashtag_medias(hashtag)
# bot.

# Iterate through the media IDs and retrieve details
for media_id in media_ids:
    # Get media details
    media_info = bot.get_media_info(media_id)
    
    # Extract relevant information (e.g., caption, likes, comments, etc.)
    caption = media_info[0]['caption']['text']
    likes = media_info[0]['like_count']
    comments = media_info[0]['comment_count']

    # Print or store the information as needed
    print(f"Caption: {caption}")
    print(f"Likes: {likes}")
    print(f"Comments: {comments}")
    print("\n")

# Logout from the Instagram account
bot.logout()
