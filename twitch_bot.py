#For access token :  https://twitchapps.com/tmi
#Sources: https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8
#https://twitchio.readthedocs.io/en/rewrite/twitchio.html


#run in virtual environment: pipenv shell python twitch_bot.py
import os
import xml.etree.ElementTree as ET
import json
from twitchio.ext import commands
import global_constants as gc
#import controller_message as cm
#import controller_database as dbc
import linecache
import random
import re
import sys
import time
from time import sleep
from datetime import date
from datetime import datetime
from datetime import timedelta
from string import ascii_lowercase


# Function: print_exception
# Prints exception messages
# Parameters:
#   ex      -- the exception to print
#   unique  -- a unique value to track the location of the exception
def print_exception(ex, unique=''):
    # Get the exception information
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    # Print the exception
    print('')
    print(gc.PRINT_LINE_BREAK)
    print('~ ' + str(exc_type))
    print('~ ' + str(filename))
    print('~ LINE: ' + str(lineno))
    print('~ CODE: ' + str(line.strip()))
    print('~ ERROR: ' + str(exc_obj))
    print('~ TIME: ' + str(datetime.now()))
    if unique != '':
        unique_list = str(unique).split('\r\n')
        if len(unique_list) > 0:
            print('~ REFERENCE:')
            for strings in unique_list:
                print('~ ' + strings.replace('\r\n', ''))    
        else:
            print('~ REFERENCE: ' + str(unique))        
    print(gc.PRINT_LINE_BREAK)
    print(gc.PRINT_LINE_BREAK)
    print('')



def write_to_xml(mes, twitch_data, myfile):

    


    message = ET.SubElement(twitch_data, 'message')

        # set the name with a counter and increment after we append

    message.set('name','message' + str(mes.timestamp))


    message.text = mes.content



    # Create a new XML file with the results

    mydata = ET.tostring(twitch_data, encoding = "unicode")

    myfile.write(mydata)



def message_to_db(message):

    message_data = {}

    

    message_data['linq_username'] = 'lambda'

    message_data['message'] = message.content

    message_data['twitch_username'] = message.author.name

    message_data['twitch_userId'] = message.author.id

    message_data['timestamp'] = message.timestamp




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
    ws = testbot._ws 
    #turn the mode off
    await ws.send_privmsg(os.environ['channel'],f"/emoteonlyoff")
    await ws.send_privmsg(os.environ['channel'],f"/followersoff")
    await ws.send_privmsg(os.environ['channel'],f"/subscribersoff")
    await ws.send_privmsg(os.environ['channel'],f"/slowoff")
    await ws.send_privmsg(os.environ['channel'],f"/unhost")
    #show the bot is connected
    await ws.send_privmsg(os.environ['channel'],f"twitch chat bot started!")

   

@testbot.event
async def event_message(mes):
    #d = dbc.ControllerDatabase()
    #c = cm.ControllerHUB(dbc= d, tbot = testbot, event = testbot.event)
    myfile = open(r"twitch_messages.xml", 'a')
    print('chat-bot: Received message from @' + mes.author.name + ':')
    print (mes.content)
    #c.message_list.append(mes)
    message_to_db(mes)
    write_to_xml(mes, twitch_data, myfile)
    await testbot.handle_commands(mes)
  
    myfile.close()
    sleep(0.01)


#Commands from Dallas's code.

@testbot.command(name= "game")
async def game(mes):
    message = mes.content
    if message.startswith('!game'):
        await mes.channel.send(f'@{mes.author.name} I lost "the game" (and now you did too)')

@testbot.command(name = "get_time")
async def get_time(mes):
    message = mes.content
    if message.startswith('!time') :
        await mes.channel.send(f'@{mes.author.name}  It is currently ' + time.strftime("%I:%M %p %Z on %A, %B %d, %Y."))

@testbot.command(name= "help")
async def help(mes):
    message = mes.content
    if message.startswith('!help'):
        await mes.channel.send(f'@{mes.author.name}  What would make this more fun for you? Also, try the !question command')

@testbot.command(name = "command")
async def command(mes):
    message = mes.content
    if message.startswith('!command'):
        await mes.channel.send(f'@{mes.author.name} There are lots of commands, but part of the fun is trying to figure out what they are, so I am not going to tell you. You will have to ask others. You can find some (but not all) of them here: https://StreamElements.com/twitchcatplays/commands')

@testbot.command(name = "think")
async def think(mes):
    message = mes.content
    if message == '!think':
        await mes.channel.send(f'@{mes.author.name} What do you think?')
    elif message.startswith('!think'):
        await mes.channel.send(f'@{mes.author.name} Thank you for sharing what you !think')

@testbot.command(name = "rules")
async def rules(mes):
    message = mes.content
    if message.startswith('!rules'):
        await mes.channel.send(f'@{mes.author.name} Most rules are hidden as part of the fun, but you can try !supporter or !troll')

@testbot.command(name = "spam")
async def spam(mes):
    message = mes.content
    if message.startswith('!spam'):
        await mes.channel.send(f'@{mes.author.name} Spamming is permitted')

@testbot.command(name = "story")
async def story(mes):
    message = mes.content
    if message == '!story':
        await mes.channel.send(f'@{mes.author.name}  Please share your story with me, or any story for that matter')
    elif message.startswith('!story'):
        await mes.channel.send(f'@{mes.author.name}  Thank you for sharing a story with me')

@testbot.command(name = "question")
async def question(mes):
    message = mes.content
    if message == '!question':
        await mes.channel.send(f'@{mes.author.name} Ask me a question. If I have an answer I will give it, otherwise I will process it and have an answer for the next time it is asked.')




    
@testbot.event
async def event_error(error, data):
    print_exception(error, data)
               


if __name__ == "__main__":
    twitch_data = ET.Element('twitch_data')
    testbot.run()

