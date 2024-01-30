import instaloader
import requests
import json

def get_hashtag_details_by_id(hashtag_id):
    try:
        # Create a session and load it
        L = instaloader.Instaloader()
        USERNAME = 'keywordlit7'
        PASSWORD = 'Keywordlit-01'
        
        L.login(USERNAME,PASSWORD)
        # L.load_session_from_file(USERNAME)
        # Define the GraphQL query
        graphql_query__ = {
            "id": hashtag_id,
            "first": 1,
        }
        print(graphql_query__)
        # Send a request to Instagram's GraphQL API
        instaloader.
        response = L.context.graphql_query('hashtag', graphql_query__)
        
        # Parse the response and extract hashtag details
        hashtag_data = response['data']['hashtag']
        if hashtag_data:
            print("Hashtag Name:", hashtag_data['name'])
            print("Number of Posts:", hashtag_data['edge_hashtag_to_media']['count'])
            return hashtag_data

    except instaloader.exceptions.InstaloaderException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Replace '17841562783108532' with the actual ID of the hashtag you want to get details for
    hashtag_id = '17841562783108532'
    hashtag_details = get_hashtag_details_by_id(hashtag_id)
