#For access token :  https://twitchapps.com/tmi
#Sources: https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8
#https://twitchio.readthedocs.io/en/rewrite/twitchio.html


#run in virtual environment: pipenv shell python twitch_bot.py
import os
import xml.etree.ElementTree as ET
import json
from twitchio.ext import commands

def write_to_xml(mes, twitch_data, count, myfile):

    


    message = ET.SubElement(twitch_data, 'message')

        # set the name with a counter and increment after we append

    message.set('name','message' + str(count))

    count += 1

    message.text = mes



    # Create a new XML file with the results

    mydata = ET.tostring(twitch_data, encoding = "unicode")

    myfile.write(mydata)
    return count

    


def message_to_db(message):

    message_data = {}

    

    message_data['linq_username'] = 'lambda'

    message_data['message'] = message.content

    message_data['twitch_username'] = message.author.name

    message_data['twitch_userId'] = message.author.id



        # Post to the DB now

    json_request = json.dumps(message_data)

    print(json_request)







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
    count = write_to_xml(mes, twitch_data, count, myfile)
    await testbot.handle_commands(mes)
    
    


    




if __name__ == "__main__":
    twitch_data = ET.Element('twitch_data')
    count = 1
    myfile = open(r"twitch_messages.xml", 'a')
    testbot.run()
    myfile.close()
