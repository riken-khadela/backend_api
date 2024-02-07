import requests

# ------------------------------------ First Block  Start-----------------------------------------------------------------------------------------------



def get_hashtags(query):
    # RIGHT NOW i HAVE JUST HARD CODED THESE VALUES
    csrftoken= 'mjnA9xvme3pd667Gpi3Dyn3nbSxDarMZ'
    sessionid= '64657101601%3AkYle40OMub6KP9%3A25%3AAYfUSWzek8QWNntjVwDhe_ehkuE51fSA6DutGZw62w'


    url = "https://www.instagram.com/api/graphql"
    dct={}

    headers = {
        "Accept": "*/*",
        #"Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.instagram.com",
        "Referer": "https://www.instagram.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "X-Asbd-Id": "129477",
        "X-Csrftoken": csrftoken,
        "X-Fb-Friendly-Name": "PolarisSearchBoxRefetchableQuery",
        "X-Fb-Lsd": "NFayaAYxCIr2sjmcgk81Be",
        "Sec-Ch-Ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        "Sec-Ch-Ua-Full-Version-List": '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.83", "Chromium";v="121.0.6167.85"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Model": '""',
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Ch-Prefers-Color-Scheme": "light",
    "Origin-Agent-Cluster": "?0",
    "Permissions-Policy": "accelerometer=(self), ambient-light-sensor=(), bluetooth=(), camera=(self), display-capture=(), fullscreen=(self), gamepad=(), geolocation=(self), gyroscope=(self), hid=(), idle-detection=(), keyboard-map=(), local-fonts=(), magnetometer=(), microphone=(self), midi=(), otp-credentials=(), payment=(), picture-in-picture=(self), publickey-credentials-get=(), screen-wake-lock=(), serial=(), usb=(), window-management=()",
    "Permissions-Policy-Report-Only": "autoplay=(), clipboard-read=(), clipboard-write=(), encrypted-media=(), xr-spatial-tracking=()",
    "Pragma": "no-cache",
    "Priority": "u=1,i",
    "Report-To": "{\"max_age\":2592000,\"endpoints\":[{\"url\":\"https://www.facebook.com/browser_reporting/coop/?minimize=0\"}],\"group\":\"coop_report\",\"include_subdomains\":true}, {\"max_age\":86400,\"endpoints\":[{\"url\":\"https://www.facebook.com/browser_reporting/coep/?minimize=0\"}],\"group\":\"coep_report\"}, {\"max_age\":259200,\"endpoints\":[{\"url\":\"https://www.instagram.com/error/ig_web_error_reports/?device_level=unknown\"}]}",
    "Reporting-Endpoints": "coop_report=\"https://www.facebook.com/browser_reporting/coop/?minimize=0\", coep_report=\"https://www.facebook.com/browser_reporting/coep/?minimize=0\", default=\"https://www.instagram.com/error/ig_web_error_reports/?device_level=unknown\"",
    "Strict-Transport-Security": "max-age=31536000; preload; includeSubDomains",
    "Vary": "Origin, Accept-Encoding",
    "X-Content-Type-Options": "nosniff",
    "X-Fb-Debug": "1JRBkBdBnQsRcYj130p54bbE2I5021ciwlckKMYy9bLVarSQOQyzuLgq8TUN9fjXFHP0JLrvHPW1RkY8O3BjCA==",
    "X-Frame-Options": "DENY",
    "X-Xss-Protection": "0",
    }

    payload = {
        "av": 17841432819377428,
        "__d": "www",
        "__user": 0,
        "__a": 1,
        "__req": "1p",
        "__hs": "19754.HYP:instagram_web_pkg.2.1..0.1",
        "dpr": 1.5,
        "__ccg": "UNKNOWN",
        "__rev": 1011158543,
        "__s": "f5eww0:cx3okz:ike52g",
        "__hsi": 7330629208565479708,
        "__dyn": "7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJxS0k24o0B-q1ew65xO2O1Vw8G1nzUO0n24oaEd86a3a1YwBgao6C0Mo2iyovw8OfK0EUjwGzEaE7622362W2K0zK5o4q3y1Sx-0iS2Sq2-azqwt8dUaob82cwMwrUdUbGwmk1xwmo6O1FwlE6PhA6bxy4UjK5V8",
        "__csr": "gvMCx5gH9sLEIzti9QhiH8LH_898yqZaVZvmAuVrAmFqzqF3EJalyEFVIyt4Gaauy3bXx0xemqlaBGECeF3ryWAh-H-WjCKcVoV3aAxucyeEjwCg9e4po5G2qbw05dUwur9w9ro1U404mE0mTPF6OF1fgO0X898owo81cpU1PO05Sw9SOm0KU1qK0ia0qS1_wtUgwzg9EV00aAa",
        "__comet_req": 7,
        "fb_dtsg": "NAcMv12OeUaZP1Y9tFln7RbaZZUwyZiFL5xvz3ucV--Nvwadj5zfDgA:17864970403026470:1706794861",
        "jazoest": 26361,
        "lsd": "NFayaAYxCIr2sjmcgk81Be",
        "__spin_r": 1011158543,
        "__spin_b": "trunk",
        "__spin_t": 1706795117,
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "PolarisSearchBoxRefetchableQuery",
        "variables": f'{{"data":{{"context":"blended","include_reel":"true","query":"#{query}","rank_token":"","search_surface":"web_top_search"}},"hasQuery":true}}',
        "server_timestamps": True,
        "doc_id": 6901177919928333,
    }

    response = requests.post(url, headers=headers, data=payload)
    
    hashtag_list = []
    for i in range(len(response.json()['data']['xdt_api__v1__fbsearch__topsearch_connection']['hashtags'])):
        hashtag_info = {
            "hashtag": response.json()['data']['xdt_api__v1__fbsearch__topsearch_connection']['hashtags'][i]['hashtag']['name'],
            "total_post": response.json()['data']['xdt_api__v1__fbsearch__topsearch_connection']['hashtags'][i]['hashtag']['media_count'],
            "rank": 1 + i,
            "link": f'https://www.instagram.com/explore/tags/{response.json()["data"]["xdt_api__v1__fbsearch__topsearch_connection"]["hashtags"][i]["hashtag"]["name"]}/'
        }
        hashtag_list.append(hashtag_info)
    
    return hashtag_list

# ------------------------------------ First Block End -----------------------------------------------------------------------------------------------



# ------------------------------------ Second Block Start -----------------------------------------------------------------------------------------------


def count_tags_all(tag_list):
    # RIGHT NOW i HAVE JUST HARD CODED THESE VALUES
    csrftoken= 'mjnA9xvme3pd667Gpi3Dyn3nbSxDarMZ'
    sessionid= '64657101601%3AkYle40OMub6KP9%3A25%3AAYfUSWzek8QWNntjVwDhe_ehkuE51fSA6DutGZw62w'

    lst=[]
    main={}
#     -------------------------- Average Calculation Block-------------------------------------------------------------
    def count_reel_tag(json_data):
        target_tag='video_length'
        count = 0

        if isinstance(json_data, list):
            for item in json_data:
                count += count_reel_tag(item)
        elif isinstance(json_data, dict):
            for key, value in json_data.items():
                if key == target_tag:
                    count += 1
                count += count_reel_tag(value)

        return count

    
    
    def get_average_like_count(json_object):
        total_like_count = 0
        total_items = 0

        if isinstance(json_object, dict):
            for key, value in json_object.items():
                if key == 'like_count':
                    total_like_count += value
                    total_items += 1
                elif isinstance(value, (dict, list)):
                    count, items = get_average_like_count(value)
                    total_like_count += count
                    total_items += items

        elif isinstance(json_object, list):
            for item in json_object:
                count, items = get_average_like_count(item)
                total_like_count += count
                total_items += items

        if total_items > 0:
            return total_like_count, total_items
        else:
            return 0, 0  # Return 0 for both total_like_count and total_items if there are no items

    
    def get_average_comment_count(json_object):
        total_comment_count = 0
        total_items = 0

        if isinstance(json_object, dict):
            for key, value in json_object.items():
                if key == 'comment_count':
                    total_comment_count += value
                    total_items += 1
                elif isinstance(value, (dict, list)):
                    count, items = get_average_comment_count(value)
                    total_comment_count += count
                    total_items += items

        elif isinstance(json_object, list):
            for item in json_object:
                count, items = get_average_comment_count(item)
                total_comment_count += count
                total_items += items

        return total_comment_count, total_items
    
    
    
#     -------------------------- Average Calculation Block-------------------------------------------------------------
    
    
    
    # Define the API endpoint
    url = "https://www.instagram.com/api/v1/tags/web_info/"
    for i in range(len(tag_list)):
        query=tag_list[i]['hashtag']
        ranking=tag_list[i]['rank']

        if i ==0:
            # Define the query parameters
            params = {"tag_name": f"{query}"}

            # Define the headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.instagram.com/explore/tags/rammandirayodhya/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Dpr": "1.25",
                "Sec-Ch-Prefers-Color-Scheme": "light",
                "Sec-Ch-Ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
                "Sec-Ch-Ua-Full-Version-List": '"Not A(Brand";v="99.0.0.0", "Microsoft Edge";v="121.0.2277.83", "Chromium";v="121.0.6167.85"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Model": '""',
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Ch-Ua-Platform-Version": '"15.0.0"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Viewport-Width": "934",
                "X-Asbd-Id": "129477",
                "X-Csrftoken": csrftoken,
                "X-Ig-App-Id": "936619743392459",
                "X-Ig-Www-Claim": "hmac.AR2V8u0CfqOPW5C_C1-_H6dEcSPRweDaHL6E554mdkqC_80b",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.instagram.com",
                "Host": "www.instagram.com",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "TE": "Trailers",
            }

            cookies = {
                "csrftoken": csrftoken,
                "sessionid": sessionid,
            }

            # Make the GET request
            response = requests.get(url, params=params, headers=headers, cookies=cookies)

            total_post=response.json()['count']
            hashtag_name=query
            kk=response.json()

            #-------------------------------------------------- Avg_comment -------------------------------------------------#
            comment_count, total_items = get_average_comment_count(kk)
            if total_items > 0:
                average_comment_count = comment_count / total_items
            average_comment_count= round(average_comment_count)

            #------------------------------------------------ Reel_percentage -----------------------------------------------#
            reel_percentage=round((count_reel_tag(kk)/total_items)*100)


            #------------------------------------------------- Avg_likes ----------------------------------------------------#
            total_like_count, total_items = get_average_like_count(kk)
            if total_items > 0:
                average_like_count = total_like_count / total_items
            else:
                average_like_count = 0
            average_like_count=round(average_like_count)



            main_second={
                    "hashtag": hashtag_name,
                    "total_post": total_post,
                    "rank": ranking,
                    "likes": average_like_count,
                    "comment": average_comment_count,
                    "reels": f"{reel_percentage} %",


                }
            lst.append(main_second)
        else:
            main_second={
                    "hashtag": hashtag_name,
                    "total_post": total_post,
                    "rank": ranking,

                }

            lst.append(main_second)
    
    main['Hashtag']=lst
    
    return main
    
    
# ------------------------------------ Second Block End -----------------------------------------------------------------------------------------------     


# ---------------------------------------CPC Function Start--------------------------------------------------------------------------------------------


def get_ranking(data) :
        for item in data["Hashtag"]:
            item["total_post"] = int(str(item["total_post"]).replace(",", ""))

        max_posts = max([item['total_post'] for item in data["Hashtag"]])

        referanceposts = sum([item['total_post'] for item in data["Hashtag"]])
        
        referance_cpc = 5
        referance_total_post = 1000000000
        total_post_ration = referanceposts/referance_total_post
        estimated_base_cpc = referance_cpc * total_post_ration

        # Perform normalization and scoring calculations
        total_hashtags = len(data["Hashtag"])  # Total number of hashtags
        normalized_data = []
        for index, item in enumerate(data["Hashtag"]):
            normalized_rank = 1 - ((index + 1) / total_hashtags)  # Rank normalization
            normalized_posts = item["total_post"] / max_posts
            combined_score = (0.4 * normalized_rank) + (0.6 * normalized_posts)  

            item_data = {
                "hashtag": item["hashtag"],
                "total_post": item["total_post"],
                "rank" : index,
                "combined_score": combined_score
            }
            if 'likes' in item : item_data['likes'] = item['likes']
            if 'comment' in item : item_data['comment'] = item['comment']
            if 'reels' in item : item_data['reels'] = item['reels']
            normalized_data.append(item_data)

        # Set thresholds for competition levels
        low_comp_threshold = 0.3
        med_comp_threshold = 0.6

        # Categorize based on competition levels
        for item in normalized_data:
            item['rank'] += 1
            if item["combined_score"] <= low_comp_threshold:
                item["competition_level"] = "Low Competition"
                item["CPC"] = round(estimated_base_cpc*0.8,3)
            elif low_comp_threshold < item["combined_score"] <= med_comp_threshold:
                item["competition_level"] = "Medium Competition"
                item["CPC"] = round(estimated_base_cpc*1.0,3)
            else:
                item["CPC"] = round(estimated_base_cpc*1.2,3)
                item["competition_level"] = "High Competition"


        return normalized_data
# ---------------------------------------CPC Function Start--------------------------------------------------------------------------------------------




# ---------------------------------------- Main Call Function -----------------------------------------------------------------------------------------
def main_call(tag_to_search):
    tags_list=get_hashtags(tag_to_search)
    json_data=count_tags_all(tags_list)
    result=get_ranking(json_data) 
    return result



