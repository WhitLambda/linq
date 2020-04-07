# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    #Download json file from the google project
    client_secrets_file = ""

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    #gets information for dummy youtube channel
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()

    print(response)

    #Download from the google project
    DEVELOPER_KEY = ""
    
    #access developer's account
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.comments().list(
        part="snippet",
        parentId="UgzDE2tasfmrYLyNkGt4AaABAg"
    )
    response = request.execute()

    #prints comment text
    for dictionary in response['items']:
        for key, value in dictionary.items():
            if key  == 'snippet':
                newDict = dictionary[key]
                print(newDict['textDisplay'])
    #prints all data
    print(response)
   
if __name__ == "__main__":
    main()

