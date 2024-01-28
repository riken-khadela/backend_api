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
            print(result.hashtagid)
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
    # Replace 'shiva' with the hashtag you want to search for
    hashtag_query = '#shiva'
    L.load_session_from_file(USERNAME)
    breakpoint()
    # query = '''query {viewer {idusername}}'''
    # L.context.get_json('/explore/tags/ram/',{"data":{"context":"blended","include_reel":"true","query":"#ram","rank_token":"1706334500509|79b9410e350d9f58c3d36cd96fa9f6fa4e0b58b2560355dc4ac3934edcd4670f","search_surface":"web_top_search"},"hasQuery":True})
    # L.context.graphql_query(query,{"context":"blended","include_reel":"true","query":"#ram","rank_token":"1706334500509|79b9410e350d9f58c3d36cd96fa9f6fa4e0b58b2560355dc4ac3934edcd4670f","search_surface":"web_top_search"})
    # Call the function to get a list of hashtags
    hashtag_list = get_hashtags_from_search(L, hashtag_query)
