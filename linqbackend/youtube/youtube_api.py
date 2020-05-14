# -*- coding: utf-8 -*-
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python
import os
import json
import requests
import google.oauth2.credentials 
import xml.etree.ElementTree as ET
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# API settings and access type
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"

# Get the user's permission for the app to access their YouTube account. Save credentials to save time on rerun.
def get_authenticated_service():
    # Secret file from the Google Cloud Credentials landing. WARNING: DO NOT POST TO GITHUB
    flow = InstalledAppFlow.from_client_secrets_file("./client_secrets_file.json", scopes)
    credentials = flow.run_console()

    # Return the API client using api version and user credentials
    return build(api_service_name, api_version, credentials = credentials)

# Retrieve the videos from the user's profile in pages. Specify the max number of pages.
def get_videos(service, **kwargs):
    final_results = []
    results = service.search().list(**kwargs).execute()

    i = 0
    max_pages = 5
    while results and i < max_pages and len(final_results) < 20:
        final_results.extend(results['items'])

        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.search().list(**kwargs).execute()
            i += 1
        else:
            break

    return final_results

# Get 'parent comments' from each video
def get_video_comments(service, **kwargs):
    comments = []
    results = service.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            commenter_name = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            commenter_id = item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
            last_updated_at = item['snippet']['topLevelComment']['snippet']['updatedAt']
            comments.extend([(comment, commenter_name, commenter_id, last_updated_at)])

        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    return comments

# Taking the final comment array and writing it to a 
def write_to_xml(comments):
    # Create the file structure
    data = ET.Element('data')
    count = 1
    for item in comments:
        comment = ET.SubElement(data, 'comment')
        # set the name with a counter and increment after we append
        comment.set('name','comment' + str(count))
        count += 1
        comment.text = item

    # Create a new XML file with the results
    mydata = ET.tostring(data, encoding = "unicode")
    myfile = open(r"comments.xml", 'w')
    myfile.write(mydata)
    myfile.close()

# Creates the HTTP post request for the comments
def make_post_request(json_request_data):
    header = {'Content-type':'application/json', 'Accept':'application/json'}
    r = requests.post('http://127.0.0.1:8000/api/v1/youtube_comments/', json=json_request_data, headers=header)
    print(r.status_code)

# Stores the comments in the database
def comments_to_db(final_result):
    comment_data = {}
    for idx, result in enumerate(final_result):
        comment_data['linq_username'] = 'lambda'
        comment_data['message'] = result[3][0]
        comment_data['YT_username'] = result[3][1]
        comment_data['YT_userId'] = result[3][2]
        comment_data['timestamp'] = result[3][3]
        comment_data['video_id'] = result[idx]
        # Post to the DB now
        json_request = json.dumps(comment_data)
        print(json_request)
        make_post_request(comment_data)

# Gets all the comments from every video and saves them to an XML file called 'comments.xml'
def save_comments(service, **kwargs):
    # Get videos and then search each video for 'parent comments'
    results = get_videos(service, **kwargs)
    final_result = []
    for item in results:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        channel_id = item['snippet']['channelId']
        comments = get_video_comments(service, part='snippet', videoId=video_id, textFormat='plainText')

        newComments = []
        if len(comments) > 20:
            #get latest 20 comments
            for c in range(0, 20):
                newComments.append(comments[c])
            comments = newComments
    
        # Append comments to a list for the XML writing
        final_result.extend([(video_id, title, channel_id, comment) for comment in comments])
        # test code
        #print(comments)
        
    comments_to_db(final_result)
   # write_to_xml(comments)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # When running in production, *DO NOT* leave this option enabled.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    service = get_authenticated_service()
    save_comments(service, part="snippet", forMine=True, type="video")

if __name__ == "__main__":
    main()



def yt_test_func():
    print("hiiiiiiiiii............")