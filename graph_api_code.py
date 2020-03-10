#sources: https://stackoverflow.com/questions/3058723/programmatically-getting-an-access-token-for-using-the-facebook-graph-api
#https://towardsdatascience.com/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999
#https://medium.com/@DrGabrielHarris/python-how-making-facebook-api-calls-using-facebook-sdk-ea18bec973c8


import requests
import urllib3
import facebook
import subprocess
import warnings
import urllib

FACEBOOK_APP_ID     = '2617245555263180'
FACEBOOK_APP_SECRET = '530a5205ccd4f1fd35bdb53301d532a6'
FACEBOOK_PROFILE_ID = '108490387437190'
USER_SHORT_TOKEN = 'EAAlMXvechswBACL8ZBGkfnAnAZCMo2vuEfX1QnCDK9aVRyVggqoZBMY0iU8fudZC5ciu5ZAHEpUDJXBinps7SbQzCW6bbLZBwFBgZA48g5Wt2E4VR1iULU7Ygtk3zxajWHaZCRgKObHX1Qep1O4IIafqxD67zz5ZA2YgtfylBiSukV2FoZAp1wPFdaZAVU3J1yykGiJKgtbyEdJQ309iHhhbdZAH'

#get long term access token
access_token_url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}".format(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, USER_SHORT_TOKEN)
r = requests.get(access_token_url)
access_token_info = r.json()
try:
    user_long_token = access_token_info['access_token']
except KeyError:
    print('Could not get access token')



  #Get info from Graph API
graph = facebook.GraphAPI(access_token=user_long_token, version = 3.1)
pages_data = graph.get_object("/me/accounts")
user = graph.request('/me?fields=id,name')

#need more permissions to get posts
comments = graph.request('/me?fields=id,posts')
print(user)

