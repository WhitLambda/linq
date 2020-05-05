#For access token :  https://twitchapps.com/tmi
#Sources: https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8
#https://twitchio.readthedocs.io/en/rewrite/twitchio.html


#run in virtual environment: pipenv shell python twitch_bot.py
import os
import xml.etree.ElementTree as ET
import json
from twitchio.ext import commands
import utils
import global_constants as gc
import controller_message as cm
import controller_database as dbc
import utils
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



async def handle_user_message(c, db, message_ref):
    username = message_ref.author.name
    message = message_ref
        # Print the function call
        #utils.o_print("handle_user_message: username=" + str(username), True)
        # Check for a ghost user
        #if username.startswith(gc.TWITCH_CONTROLLER_GHOST_USERNAME):
            # Check for a message trigger
            #self.check_for_message_trigger( message)
            # Check for custom commands
            #self.handle_user_command( message)
            # Do nothing else with ghost users
            #return
    db.insert_user_message(message.author.name, message.content)
        # Wrap the function in a try statement
    try:
            # Log username
            #self.save_username_to_db(username)
            # Save message to datatable
        message_to_db(message)
            # Check for banned words
        if utils.contains_profanity(message.content):
                # Print the message contains profanity
                #utils.o_print("message has triggered 'contains profanity' -> timeout_user_yes_ban()")
                # Timeout or ban the user, timeout process deletes their messages
                #self.timeout_user_yes_ban(username)
                # Tell the user
            await message_ref.channel.send.send(f"@ {username} Please do not use profanity in chat. Do it enough times an you will be banned.")
        elif utils.contains_timeout_word(message.content):
                # Print the message contains timeout words
                #utils.o_print("message has triggered 'contains timeout word' -> timeout_user_no_ban()")
                # Timeout or ban the user, timeout process deletes their messages
                #self.timeout_user_no_ban(username)
                # Tell the user
            await message_ref.channel.send.send(f"@{username}Please take care with what words you use. Certain topics are better suited for other places.")                       
        elif utils.contains_self_promo(message.content):
                # Print the message contains self promotion
                #utils.o_print("message has triggered 'contains self promotion' -> timeout_user_yes_ban()")
                # Timeout or ban the user, timeout process deletes their messages
                #self.timeout_user_yes_ban(username)
                # Tell the user
            await message_ref.channel.send(f"@{username} Please do not promote other channels/products/etc. in chat.")                       
        else:
                # Check for a message trigger
            c.check_for_message_trigger(message)
                # Check for custom commands
            c.handle_user_command( message)
    except KeyboardInterrupt as ki:
        utils.print_exception( 'handle_user_message')
    except Exception as e:
        utils.print_exception( 'handle_user_message')


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

    #json_request = json.dumps(message_data)

    #print(json_request)







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
    d = dbc.ControllerDatabase()
    c = cm.ControllerHUB(dbc= d, tbot = testbot, event = testbot.event)
    myfile = open(r"twitch_messages.xml", 'a')
    #c.start_managing_messages()
    await handle_user_message(c,d, mes)
    print('chat-bot: Received message from @' + mes.author.name + ':')
    print (mes.content)
    c.message_list.append(mes)
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
    utils.print_exception(error, data)
               


if __name__ == "__main__":
    twitch_data = ET.Element('twitch_data')
    testbot.run()

