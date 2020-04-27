#For access token :  https://twitchapps.com/tmi
#Sources: https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8
#https://twitchio.readthedocs.io/en/rewrite/twitchio.html


#run in virtual environment: pipenv shell python twitch_bot.py
import os
import xml.etree.ElementTree as ET
import json
from twitchio.ext import commands



def message_to_db(message):

    message_data = {}

    

    message_data['linq_username'] = 'lambda'

    message_data['message'] = message.content

    message_data['twitch_username'] = message.author.name

    message_data['twitch_userId'] = message.author.id



        # Post to the DB now

        json_request = json.dumps(message_data)

        print(json_request)





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
        
    print(comments)



    comments_to_db(final_result)

   # write_to_xml(comments)





testbot = commands.Bot(
    irc_token = os.environ['token'],
    client_id = os.environ['client_id'],
    nick = os.environ['nick'],
    prefix = '!',
    initial_channels = [os.environ['channel']]
)

@testbot.event
async def event_ready():
    print(f"twitch chat bot started!")
    ws = testbot._ws
   

@testbot.event
async def event_message(mes):
    print (mes.content)
    message_to_db(mes)
    await testbot.handle_commands(mes)
    
    


    




if __name__ == "__main__":
    twitch_data = ET.Element('twitch_data')
    testbot.run()
