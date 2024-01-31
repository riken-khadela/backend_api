import instaloader
def get_hashtags_from_search(L, query):
    try:
        # Perform a hashtag search
        # search_results = instaloader.Hashtag.from_name(L.context, query)
        search_results = instaloader.TopSearchResults(L.context, query)
        
        # Extract hashtags from the search results
        
        # hashtags = [result.name for result in search_results.get_hashtags()]
        for result in search_results.get_hashtags() : 
            print(result.name)
            try : print(result.description)
            except : ...
            try : print(result.mediacount)
            except : ...
            # for post in result.get_top_posts():
            #     print(f"Post URL: {post.url}")
            #     print(f"Likes: {post.likes}")
            #     print(f"Comments: {post.comments}")
            #     print(f"Caption: {post.caption}")
            #     print("------")
        # Print or process the list of hashtags
        print("List of Hashtags:")
        # for hashtag in hashtags:
        #     print(hashtag)

        # return hashtags

    except instaloader.exceptions.InstaloaderException as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    L = instaloader.Instaloader()
    USERNAME = 'keywordlit7'
    PASSWORD = 'Keywordlit-01'
    hashtag_query = '#shiva'
    L.load_session_from_file(USERNAME)
    hashtag_list = get_hashtags_from_search(L, hashtag_query)
