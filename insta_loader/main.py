import instaloader
def get_hashtags_from_search(L, query):
    try:
        # Perform a hashtag search
        search_results = instaloader.TopSearchResults(L.context, query)
        search_results = instaloader.TopSearchResults.get_hashtags(query)
        # Extract hashtags from the search results
        hashtags = [result.hashtag for result in search_results]

        # Print or process the list of hashtags
        print("List of Hashtags:")
        for hashtag in hashtags:
            print(hashtag)

        return hashtags

    except instaloader.exceptions.InstaloaderException as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    L = instaloader.Instaloader()
    USERNAME = 'keywordlit7'
    PASSWORD = 'Keywordlit-01'
    # Replace 'shiva' with the hashtag you want to search for
    hashtag_query = '#shiva'
    L.load_session_from_file(USERNAME)
    # Call the function to get a list of hashtags
    hashtag_list = get_hashtags_from_search(L, hashtag_query)
