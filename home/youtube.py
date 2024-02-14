# -------------------------------Main Class For Instagram API call----------------------------------------------------#


class YoutubeHashTag_new(APIView):
    """
    This function takes Query as Input and returns top_five_video_titles, avg_views,avg_likes & avg_comments as Output.

    """

    def search_youtube(self,query):
        lst = []
        url = "https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"
        
        headers = {
            "Accept": "*/*",
            #"Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "SAPISIDHASH 1707374253_db06ff3c4865646cc7e60b0d91fb6343a057d70e",
            "Content-Type": "application/json",
            "Origin": "https://www.youtube.com",
            "Referer": f"https://www.youtube.com/results?search_query={query}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "same-origin",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-Goog-Authuser": "0",
            "X-Goog-Visitor-Id": "CgtRVDBNZC10YjhiRSiB7ZGuBjIKCgJJThIEGgAgTg%3D%3D",
            "X-Origin": "https://www.youtube.com",
            "X-Youtube-Client-Name": "1",
            "X-Youtube-Client-Version": "2.20240207.01.00"
        }
        
        cookies = {
            "SID": "g.a000gAhJjhQVJKHBBXaBY68i4nfoaCao9dHK-af3mg-T17NLt9H6hA1IUadg7WYJqCo2PIRShwACgYKAT4SAQASFQHGX2MifPyGJryV-pdKdPFnkApENRoVAUF8yKrr1PZ4ObLLCQk2WaxO23VE0076",
            "__Secure-1PSID": "g.a000gAhJjhQVJKHBBXaBY68i4nfoaCao9dHK-af3mg-T17NLt9H6CMWiFbLxypOOiClxT_twBQACgYKAfISAQASFQHGX2Mi6EPKJiUX9_H8aPGnd-nznxoVAUF8yKq7u_T5cA3_6jyJSv-31vlM0076",
            "__Secure-3PSID": "g.a000gAhJjhQVJKHBBXaBY68i4nfoaCao9dHK-af3mg-T17NLt9H6E8djN5wlekq077HtCM5KgAACgYKAeoSAQASFQHGX2MiCQeBFS35eAkJDAWqvNjQqBoVAUF8yKopgrg-BBHgqyMpmb9Fukje0076",
            "HSID": "ANRZYhMwnKWC1VV1A",
            "SSID": "AW9hnKacmAvmNmqbm",
            "APISID": "qx3YOrlTqUDgwkNo/AAEstHL4MHVmHg4TQ",
            "SAPISID": "A2WA-2epk6mIVn3n/A_l7GS8mEQOL_xPZw",
            "__Secure-1PAPISID": "A2WA-2epk6mIVn3n/A_l7GS8mEQOL_xPZw",
            "__Secure-3PAPISID": "A2WA-2epk6mIVn3n/A_l7GS8mEQOL_xPZw",
            "YSC": "1AybS0LaEtQ",
    #         "LOGIN_INFO": "AFmmF2swRQIgQfv7fKfpigXRDNRNo1bJ3_wIcCmGNP4HPM37gVcLa_kCIQDd7_sCH30rUCvuK4bJermQfdiVf-j6lC8odTfUQFhVMQ:QUQ3MjNmeVh0bUk3MnpIUXhIUWdieFFVVThNODdTZFdncEIwTW82Q0J4aVdDaEZaSUMxZTZ0Z0dIOERQbGJpdHpQUTJMVGZmbzdJSGdKT3l0Zk9hQjBsQlNwMGR5MUJpUTNwYVRVWHZ2UjEtc0JqVUtOS094WVNBdDV0R0tKS1lhLVNoTnFnV0ljUVo5SUEwZE1sM0hOTm1WLVFwSFRqcHpB",
    #         "VISITOR_PRIVACY_METADATA": "CgJJThIEGgAgTg%3D%3D",
    #         "VISITOR_INFO1_LIVE": "QT0Md-tb8bE",
            "PREF": "f7=4100&tz=Asia.Calcutta&f4=4000000&f5=30000",
            "__Secure-1PSIDTS": "sidts-CjEBPVxjSq7fPfKFm5cRqLqj1lg8e_LgpP5FczWUN5nrjebICE7aPkikLpbm6z4LzdpIEAA",
            "__Secure-3PSIDTS": "sidts-CjEBPVxjSq7fPfKFm5cRqLqj1lg8e_LgpP5FczWUN5nrjebICE7aPkikLpbm6z4LzdpIEAA",
            "CONSISTENCY": "AKreu9sWrLkdroQecNvyq9hIFL1SiHNDNQlbqEHaoJHpdH2lJRZ7rFsxkkQ9r9VhvnzAeqWqMjVQQIKk5hYSOTFyabobaWmEWLIVKByKfoBmMfg1xObtHpJM0JLU8TAJoCrCdrnU8d_zOVmoli3E0NBa",
            "SIDCC": "ABTWhQFist3oSOwEusHXhFerSf_BPZUaf7W7zHIJk8_Zf35u-343J6qznSIDkbSYM2_sz91oCA",
            "__Secure-1PSIDCC": "ABTWhQHC4whbeFvJKxTgPWH46on1CTAUbm2YmPFfXzN9wZ1xmp6kja80vpKRqfg1XQBBXNhumA",
            "__Secure-3PSIDCC": "ABTWhQGEzHWCQMtrZuVFsk91tvIK-X61Yg11c3BUO4Rbdc7Z_orv9JGYHraKn59SB5C2A-TZ2A",
            "ST-vhwkpf": "oq=%23bike&gs_l=youtube.3..0i71k1l9.0.0.2.13127.0.0.0.0.0.0.0.0..0.0.ytpnlt_c...0...1ac..64.youtube..0.0.0....0.1V7XxGFYavk&itct=CBMQ7VAiEwiF1-HYkJuEAxUp0XMBHWRaAtY%3D&csn=MC4xODU4MTUyMjM4OTE0NDIzNA..&endpoint=%7B%22clickTrackingParams%22%3A%22CBMQ7VAiEwiF1-HYkJuEAxUp0XMBHWRaAtY%3D%22%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fresults%3Fsearch_query%3D%2523bike%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_SEARCH%22%2C%22rootVe%22%3A4724%7D%7D%2C%22searchEndpoint%22%3A%7B%22query%22%3A%22%23bike%22%7D%7D"
        }
        
        payload = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20240207.01.00",
                    "hl": "en",
                    "gl": "US",
                    "experimentIds": [],
                },
                "request": {
                    "sessionId": "None",
                    "internalExperimentFlags": [],
                    "consistencyTokenJars": [],
                },
            },
            "query": query,
            "params": "Eg-KA3gC",
        }
        
        response = requests.post(url, headers=headers, cookies=cookies, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            link_extra='https://www.youtube.com/watch?v='
            #count=0
            for j in range(len(data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'])):
                try:
                    video_title=data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][j]['videoRenderer']['title']['runs'][0]['text']
                    views_count=int(data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][j]['videoRenderer']['viewCountText']['simpleText'].split()[0].replace(',',''))
                    link=link_extra+data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][j]['videoRenderer']['videoId']
                    #count+=1
                    #print(count)
                    dct={
                            'video_title':video_title,
                            'views_count':views_count,
                            'link':link
                        }
                    
                    
                    lst.append(dct)
                    
                except:
                        pass
            return lst
            
            
        else:
            print("Error:", response.status_code)
            return None
    
    def get_youtube_videos(self,query):
        response = self.search_youtube(query)
        response=response[:5]
        return response



    def get_youtube_video_data(self,query):
        videos = self.get_youtube_videos(query)
        video_titles=[i['video_title'] for i in videos]
        links=[i['link'] for i in videos]
        view_tmp=[int(i['views_count']) for i in videos]
        avg_view=round(sum(view_tmp)/len(view_tmp))
        return video_titles, links, avg_view

#----------------------------------------Extract Video ID----------------------------------------------------------------------
    def extract_video_id(self,url):
        try: 
            v_id=url.split('=')[-1]
        #     match = re.search(r"watch\?v=(\w+)", url)
            return v_id
        except:
            print('Invalid URL')


#----------------------------------------Extract Video ID----------------------------------------------------------------------


    #----------------------------------------LIKE----------------------------------------------------------------------

    def get_youtube_like_counts(self,video_url):
        # Function to extract video ID from YouTube URL
        # def extract_video_id(self,url):
        #     try: 
        #         v_id=url.split('=')[-1]
        #     #     match = re.search(r"watch\?v=(\w+)", url)
        #         return v_id
        #     except:
        #         print('Invalid URL')

        # Extract video ID from the URL
        video_id = self.extract_video_id(video_url)

        # Check if video ID exists
        if video_id:
            # API endpoint URL with updated video ID
            url = f"https://www.youtube.com/youtubei/v1/updated_metadata?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false&videoId={video_id}"

            # Request headers
            headers = {
                "Accept": "*/*",
                #"Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                # Add your authorization headers here if needed
            }

            # Payload containing the video ID
            payload = {
                "context": {
                    "client": {
                        "clientName": "WEB",
                        "clientVersion": "2.20240207.01.00",
                        "hl": "en",
                        "gl": "IN",
                        "experimentIds": [],
                        "experimentsToken": "",
                        "utcOffsetMinutes": 330,
                        "browserName": "Chrome",
                        "browserVersion": "121.0.0",
                        "osName": "Windows",
                        "osVersion": "10.0",
                        "mobile": False,
                        "screenWidthPoints": 1920,
                        "screenHeightPoints": 1080,
                        "screenPixelDensity": 1,
                        "platform": "DESKTOP",
                        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                        "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                        "browserIsBots": False
                    },
                    "request": {},
                    "user": {}
                },
            }

            # Make the POST request
            response = requests.post(url, json=payload, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                try:
                    # Extract like counts from the response JSON
                    like_counts = int(response.json()['frameworkUpdates']['entityBatchUpdate']['mutations'][0]['payload']['likeCountEntity']['expandedLikeCountIfLiked']['content'].replace(',',''))
                    return like_counts
                except (KeyError, IndexError):
                    #print("Failed to extract like counts from the response.")
                    return None
            else:
                #print("Request failed with status code:", response.status_code)
                return None
        else:
            print("Failed to extract video ID from the URL.")
            return None
        

    #----------------------------------------------LIKE------------------------------------------------------
        


    #------------------------------------------COMMENTS-----------------------------------------------------------
        
# -------------------------------Extract The Continous Token From Pattern----------------------------------------------------
    def extract_continuation(self,response_text):
        pattern = r'"token":"([^"]*)"'
        match = re.search(pattern, response_text)
        if match:
            return match.group(1)
        else:
            return None


# -------------------------------Extract The Continous Token From Pattern----------------------------------------------------
        
    #-----------------------------------------Get Continuous Token----------------------------------------------------------#
    def get_youtube_continuation(self,video_url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        }

        try:
            response = requests.get(video_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

            response_text = response.text

            # # Function to extract continuation from response text
            # def extract_continuation(self,response_text):
            #     pattern = r'"token":"([^"]*)"'
            #     match = re.search(pattern, response_text)
            #     if match:
            #         return match.group(1)
            #     else:
            #         return None

            # Extract continuation from the response text
            continuation = self.extract_continuation(response_text)
            return continuation
        except Exception as e:
            print("Error:", e)
            return None
        
    #-----------------------------------------Get Comments----------------------------------------------------------#

    def get_video_metadata(self,continuation_token):
        url = "https://www.youtube.com/youtubei/v1/next?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false"

        headers = {
            "Accept": "*/*",
            #"Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://www.youtube.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        }

        payload = {
            "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
            "prettyPrint": False,
            "context": {
                "client": {
                    "hl": "en-GB",
                    "gl": "IN",
                    "remoteHost": "103.219.216.157",
                    "deviceMake": "",
                    "deviceModel": "",
                    "browserName": "Chrome",
                    "browserVersion": "121.0.0",
                    "osName": "Windows",
                    "osVersion": "10.0",
                    "mobile": False,
                    "screenWidthPoints": 1920,
                    "screenHeightPoints": 1080,
                    "screenPixelDensity": 1,
                    "platform": "DESKTOP",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                    "clientName": "WEB",
                    "clientVersion": "2.20240207.01.00",
                    "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                    "browserIsBots": False
                },
                "user": {},
                "request": {}
            },              # Eg0SC2VkcDNjZ2lqZHZJGAYyJSIRIgtlZHAzY2dpamR2STAAeAJCEGNvbW1lbnRzLXNlY3Rpb24%3D
            "continuation": continuation_token,#"Eg0SC1R5NTlYZUJHVnd3GAYyJSIRIgtUeTU5WGVCR1Z3dzAAeAJCEGNvbW1lbnRzLXNlY3Rpb24%3D",
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            #print("Status Code:", response.status_code)
            tmp= response.json()
            return int(tmp['onResponseReceivedEndpoints'][0]['reloadContinuationItemsCommand']['continuationItems'][0]['commentsHeaderRenderer']['countText']['runs'][0]['text'].replace(',',''))
        except requests.exceptions.HTTPError as err:
            print("HTTP Error:", err)
        except requests.exceptions.RequestException as err:
            print("Request Exception:", err)

            
    def get_youtube_comment_counts(self,video_url):
        continuation_token=self.get_youtube_continuation(video_url)
        comment=self.get_video_metadata(continuation_token)
        return comment

    #------------------------------------------COMMENTS-----------------------------------------------------------


    #---------------------------------------------MAIN------------------------------------------------------------

    def get_youtube_result(self,query):
        video_titles_lst, link_lst, avg_views = self.get_youtube_video_data(query)
        #print(video_titles_lst)
        #print(avg_views)
        #print(link_lst)
        time.sleep(1)
        # ------------------Average Comment---------------------------------
        #comment_lst=[int(get_youtube_comment_counts(url)) for url in link_lst]
        comment_lst=[int(self.get_youtube_comment_counts(url)) if self.get_youtube_comment_counts(url) is not None else 0 for url in link_lst]
        avg_comment=round(sum(comment_lst)/len(comment_lst))
        #print(comment_lst)
        #print(avg_comment)
        
        # -------------------Average Likes-----------------------------------
        like_lst=[int(self.get_youtube_like_counts(url)) if self.get_youtube_like_counts(url) is not None else 0 for url in link_lst]
        avg_likes=round(sum(like_lst)/len(like_lst))
        
        main={
        'top_five_video_titles':video_titles_lst,
        'avg_views':avg_views,
        'avg_likes':avg_likes,
        'avg_comments':avg_comment
        }
        return main


    #---------------------------------------------MAIN-------------------------------------------------------------


# -------------------------------Main Calling Class For youtube API call----------------------------------------------------#
class GetYouTubeTagsView(APIView):
    def post(self, request):
        # Get the query from the request
        query = request.POST.get('query')

        # Create an instance of your YoutubeHashTag_new class
        youtube_instance = YoutubeHashTag_new()
        
        # Call the get_youtube_result method to get the desired data
        result = youtube_instance.get_youtube_result(f'{query}')
        
        # Return the result as a JSON response
        return JsonResponse(result)
# -------------------------------Main Calling Class For youtube API call----------------------------------------------------#

# -------------------------------Main Class For youtube API call----------------------------------------------------#