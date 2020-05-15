# message_controller.py
# Manages chat messages
import global_constants as gc
import random
import threading
import time
import utils
from time import sleep
import the_dictionary
from twitchio.ext import commands


class ControllerHUB():
    # Class Variables
    #pyg_control_ref = ''  # ControllerPyglet
    dbc_ref = ''  # ControllerDatabase
    twitch_bot_ref = ''  # ControllerTwitch
    message_list = list([])
   
    # Function: __init__
    # Sets up the class
    def __init__(self, dbc, tbot, event):
        # Assign references
        self.dbc_ref = dbc
        self.bot_ref = tbot
        self.event_control_ref = event
                
                    
    def handle_message(self, dbc, message_to_process):
        # Get the username
        message = message_to_process
        sender_username = message.author.name
        # Get the message
        # Check the sender/message        
        if ':jtv!jtv@jtv.tmi.twitch.tv privmsg ' + self.bot_ref.initial_channels[0] + ' :' in message.lower():
            # Handle PRIVMSG
            self.handle_privmsg_message( message)
        elif sender_username == 'tmi':
            # Handle twitch's message
            self.handle_twitch_message( message)
        elif sender_username == 'streamlabs' or sender_username == 'streamelements':
            # Handle stream message
            self.handle_stream_message( message)  
        elif sender_username != self.bot_ref.initial_channels[0]:
            # Handle a user's message
            self.handle_user_message(message)                   
        else: # Bot sent a message
            # Handle a program's message
            self.handle_program_message(message)        
    
    async def handle_user_message(self, message_ref):
        original_content = message_ref.content
        username = message_ref.author.name
        # Print the function call
        print("handle_user_message: username=" + str(username), True)
        # Wrap the function in a try statement
        try:
            # Save message to datatable
            self.dbc_ref.message_to_db(message_ref)
            # Check for banned words
            
            if utils.contains_profanity(message_ref):
                # Print the message contains profanity
                print("message has triggered 'contains profanity' -> timeout_user_yes_ban()")
                # Timeout or ban the user, timeout process deletes their messages
                #self.timeout_user_yes_ban(username)
                # Tell the user
                await message_ref.channel.send.send(f"@ {username} Please do not use profanity in chat. Do it enough times an you will be banned.")
            elif utils.contains_timeout_word(message_ref):
                # Print the message contains timeout words
                print("message has triggered 'contains timeout word' -> timeout_user_no_ban()")
                # Timeout or ban the user, timeout process deletes their messages
                #self.timeout_user_no_ban(username)
                # Tell the user
                await message_ref.channel.send.send(f"@{username}Please take care with what words you use. Certain topics are better suited for other places.")                       
            elif utils.contains_self_promo(message_ref):
                # Print the message contains self promotion
                print("message has triggered 'contains self promotion' -> timeout_user_yes_ban()")
                # Timeout or ban the user, timeout process deletes their messages
                #self.timeout_user_yes_ban(username)
                # Tell the user
                await message_ref.channel.send(f"@{username} Please do not promote other channels/products/etc. in chat.")                       
            else:
                message_ref.content = original_content
                reply = self.check_for_message_trigger( message_ref)
                if len(reply) > 0:
                    await message_ref.channel.send(f'@{username}  {reply}')
    
            #c.handle_user_command( message)
        except KeyboardInterrupt as ki:
            utils.print_exception( 'handle_user_message')
        except Exception as e:
            utils.print_exception( 'handle_user_message')

      
    
    async def handle_program_message(self, message_ref):
        # Print the function call
       
        print('handle_program_message: ' + str(message_ref), True)    
        # Save message to datatable
        message = message_ref.content
        if message != gc.TWITCH_STARTUP_MESSAGE:
            if not message.startswith('/'):
                self.dbc_ref.message_to_db( message_ref)
        # Make the message lowercase
        message = message.lower().strip()
        # Wrap the function in a try statement
        try:
            # Check the message
            #if message == '!merge':
                #self.dbc_ref.merge_databases()
            #elif message == '!data' or message == '!backupdata' or message == '!backup':
                #self.dbc_ref.update_backup_database()
            if message == '!cleantmi' or message == '!cleartmi' or message == '!clean_tmi' or message == '!clear_tmi':
                await utils.clean_database_user_messages_with_trigger('tmi')
            elif message == '!cleandts' or message == '!cleardts' or message == '!clean_dts' or message == '!clear_dts':
                await utils.clean_database_user_messages_with_trigger('dtscrockett')
            elif message == '!cleantcp' or message == '!cleartcp' or message == '!clean_tcp' or message == '!clear_tcp':
                await utils.clean_database_user_messages_with_trigger(self.bot_ref.initial_channels[0])
            elif message == '!cleancmd' or message == '!clearcmd' or message == '!clean_cmd' or message == '!clear_cmd':
                await utils.clean_database_user_commands_with_trigger()
            elif message == '!c' or message == '!k3' or message == '!c30':  # Run a 30 second commercial
                await utils.send_chat_message_with_trigger('/commercial 30')
            elif message == '!c6' or message == '!c60':  # Run a 60 second commercial
                await utils.send_chat_message_with_trigger('/commercial 60')
            elif message == '!c9' or message == '!c90':  # Run a 90 second commercial
                await utils.send_chat_message_with_trigger('/commercial 90')
            elif message == '!k' or message == '!k3' or message == '!k30':  # Run a 30 second commercial
                await utils.send_chat_message_with_trigger('/commercial 30')
            elif message == '!k6' or message == '!k60':  # Run a 60 second commercial
                await utils.send_chat_message_with_trigger('/commercial 60')
            elif message == '!k9' or message == '!k90':  # Run a 90 second commercial
                await utils.send_chat_message_with_trigger('/commercial 90')
            elif message == '!smoff':  # System Messages Off
                await utils.set_system_message_visible_with_trigger(False)
            elif message == '!smon':  # System Messages On
                await utils.set_system_message_visible_with_trigger(True)
            elif message.startswith('!alert '):
                await utils.send_alert_message_with_trigger(message.replace('!alert ', ''), 2, gc.ALERT_TYPE_WS_BB)
            elif message.startswith('!hms'):  # Health Messages
                # Check for a value
                try:
                    messages = int(message.replace('!hms', '').strip())
                except:
                    messages = 200
                # Sent the messages
                #utils.send_multiple_chat_messages(utils.get_filled_list_str(messages, 'iah-'))
            # Check if the avatar's health should be affected
            if message.startswith('!reset_to'):  # Reset timeout counters
                # Get the username
                username = message_ref.author.name
                # Check if the username is in the database
                if self.dbc_ref.username_exists(username, self.dbc_ref.DBNAME):
                    # Reset the timeout counters
                    self.dbc_ref.set_user_value(username, gc.TWITCH_USER_VALUE_TIMEOUT_COUNT_BAN, 0, self.dbc_ref.DBNAME)
                    self.dbc_ref.set_user_value(username, gc.TWITCH_USER_VALUE_TIMEOUT_COUNT_NO_BAN, 0, self.dbc_ref.DBNAME)            
        except KeyboardInterrupt as ki:
           print( 'handle_program_message')
        except Exception as e:
            print('handle_program_message')
    
    async def handle_twitch_message(self, message_ref):
        #username = message_ref.author.name
        message = message_ref.content
       
        # Wrap the function in a try statement
        try:
            # Log username
            #self.save_username_to_db(message.author.name)
            # Check for non-loading message
            if not 'This server is rather new' in message.content:
                # Save message to datatable
                self.dbc_ref.message_to_db(message_ref)
        except KeyboardInterrupt as ki:
            utils.print_exception( 'handle_twitch_message')
        except Exception as e:
            utils.print_exception( 'handle_twitch_message')
    
    async def handle_privmsg_message(self, message_ref):
        username = message_ref.author.name
        message = message_ref.content
      
        # Wrap the function in a try statement
        try:
            message.content = ""
            self.dbc_ref.message_to_db(message_ref)
            # Check for host
            if ' is now hosting you' in message.content:
                print('message-controller: handle_privmsg_message(): @' + username + ' is now hosting the channel', False)
                # Thank the host
                await message_ref.channel.send(f"@{username} Thanks for hosting!") 
        except KeyboardInterrupt as ki:
            utils.print_exception( ki,'handle_privmsg_message')
        except Exception as e:
            utils.print_exception( e,'handle_privmsg_message')
    
    def handle_stream_message(self, message_ref):
        username = message_ref.author.name
        message = message_ref.content
       
        # Make the message lowercase
        message = message.lower()
        # Wrap the function in a try statement
        try:
            # Save message to datatable
            self.dbc_ref.message_to_db(message_ref)
            # Check the message for needed updates
            if 'thank you for following' in message:
                # Strip the username from message
                username = utils.strip_non_alphanumeric(str(message.replace('thank you for following', ''))[:-1], True, True).lower()                
        except KeyboardInterrupt as ki:
            utils.print_exception( ki, 'handle_stream_message')
        except Exception as e:
            utils.print_exception(e, 'handle_stream_message')
    
    async def handle_user_command(self, message_ref):
        username = message_ref.author.name
        message = message_ref.content
        # Wrap the function in a try statement
        try:
            # Get the user's values
            #utils.o_print("message-controller: handle_user_command(): @" + username)
            # Replace commands with base version
            message = utils.replace_base_commands(message)
            # Strip the message
            message = utils.reduce_text_to_minimum(message_ref, False)
           
            # Check the command
           
            # Track the user's comment count
            self.dbc_ref.increment_user_value_int(username, gc.TWITCH_USER_VALUE_COMMENT_COUNT, 1, self.dbc_ref.DBNAME)
            # Get the date of the user's last message
            last_message = self.dbc_ref.get_user_most_recent_message_date_submitted(username)
            # Check if it has been a while since the user's last message
            if last_message != 'None':
                if last_message < utils.get_datetime_now_add_days(-1):
                    # Send a welcome back message
                    await message_ref.channel.send(f"@{username} Welcome back!") 
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'handle_user_command')
        except Exception as e:
            utils.print_exception(e, 'handle_user_command')
    
    
    
    def get_user_timeout_count(self, username, ban_count=True):
        # Get the count
        if ban_count:
            count = self.dbc_ref.get_user_value(username, gc.TWITCH_USER_VALUE_TIMEOUT_COUNT_BAN, self.dbc_ref.DBNAME)
        else:
            count = self.dbc_ref.get_user_value(username, gc.TWITCH_USER_VALUE_TIMEOUT_COUNT_NO_BAN, self.dbc_ref.DBNAME)
        # Check for none
        if count == 'None':
            return 0
        # Return the count
        try:
            return int(count)
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'get_user_timeout_count')
            return 0
        except Exception as e:
            utils.print_exception(e, 'get_user_timeout_count')
            return 0
    
    def get_user_comment_ratio(self, username):
        # Wrap the function in a try statement
        try:
            # Get the number of comments
            comment_count = self.dbc_ref.get_user_value(username, gc.TWITCH_USER_VALUE_COMMENT_COUNT, self.dbc_ref.DBNAME)
            # Validate values
            if comment_count == 'None':
                comment_count = 0
            # Get the total number of comments
            total_count = int(comment_count)
            # Get the player_type ratio
            if total_count == 0:
                ratio = 0
            else:
                ratio = float(comment_count) / float(total_count)
            # Convert ratio to 2 digit int
            ratio = int(round(ratio, 2) * 100)
            # Return the ratio
            return ratio
        except KeyboardInterrupt as ki:
            utils.print_exception(ki, 'get_user_comment_ratio')
            return 0
        except Exception as e:
            utils.print_exception(e, 'get_user_comment_ratio')
            return 0

    #def get_reply(self, keywords, message_ref):
        #reply_list = []
        #random.seed()
        #username = message_ref.author.name
        #if '((' in keywords[message_ref.content]:
                        # Check the special case
                #if '((ban))' in keywords[message_ref.content].lower():
                            #self.bot_ref.ban_user(username) 
                    #self.bot_ref.intial_channels[0].ban(username)                           
                #elif '((timeout_noban))' in keywords[message_ref.content].lower():
                    #self.timeout_user_no_ban(username)
                #elif '((timeout_ban))' in keywords[message_ref.content].lower():
                    #self.timeout_user_yes_ban(username)
                #elif '((timeout_free))' in keywords[message_ref.content].lower():
                            #self.timeout_user_no_counter(username, 30)
                    #self.bot_ref.initial_channels[0].timeout(username, 30)
                #elif '((timeout_free_30))' in keywords[message_ref.content].lower():
                            #self.timeout_user_no_counter(username, 30)
                    #self.bot_ref.initial_channels[0].timeout(username, 30)
                #elif '((timeout_free_60))' in keywords[message_ref.content].lower():
                            #self.timeout_user_no_counter(username, 60)
                    #self.bot_ref.initial_channels[0].timeout(username, 60)
                #elif '((timeout_free_90))' in keywords[message_ref.content].lower():
                            #self.timeout_user_no_counter(username, 90)
                    #self.bot_ref.initial_channels[0].timeout(username, 90)
                #elif '((timeout_free_300))' in keywords[message_ref.content].lower():
                            #self.timeout_user_no_counter(username, 300)
                    #self.bot_ref.initial_channels[0].timeout(username, 300)
                #elif '((timeout_free_600))' in keywords[message_ref.content].lower():
                            #self.timeout_user_no_counter(username, 600)
                    #self.bot_ref.initial_channels[0].timeout(username, 600)
        #for value in keywords[message_ref.content]:
            #reply_list.append(value)
        #index = random.randint(0, len(reply_list) - 1)
        #message_ref.content = reply_list[index]
        #reply = utils.convert_response_keywords(message_ref)
        #return reply

    #def check_for_message_trigger(self, keywords, message_ref):
        #message = message_ref.content
        #if message in keywords.keys():
            #reply = self.get_reply(keywords, message_ref).content
            #await self.get_send_message_trigger_response(message_ref.author.name, message_ref)
            #return reply
        #else:
            #message_ref.content = utils.reduce_text_to_minimum(message_ref).content
            #if message_ref.content in keywords.keys():
                #reply = self.get_reply(keywords, message).content
                #self.get_send_message_trigger_response(message_ref.author.name, message_ref)
                #return reply
            #else:
                #message_ref.content = utils.translate_text_to_minimum(message_ref).content
                #if message_ref.content in keywords.keys():
                    #reply = self.get_reply(keywords, message).content
                    #self.get_send_message_trigger_response(message_ref.author.name, message_ref)
                    #return reply
                #else:
                    #return ""


    
    def check_for_message_trigger(self, message_ref):
        # Check for exact triggers
        username = message_ref.author.name
        message = message_ref.content
        response = self.get_send_message_trigger_response(username,message_ref)
        # Check if a response was found
        if response == '':
            # Check for reduced triggers next
            response = self.check_for_message_trigger_reduced(username,message_ref)
        # Check if a response was found
        if response == '':
            # Check for translated triggers
            response = self.check_for_message_trigger_translated(username,message_ref)
        # Check if a response was found
        if response == '':
            # Remove common sentence starts
            message_ref.content = utils.remove_common_sentence_starts(message_ref.content)
            # Check for exact triggers
            response = self.get_send_message_trigger_response(username, message_ref)
            return response
        # Check if a response was found
        if response == '':
            # Check for reduced triggers next
            response = self.check_for_message_trigger_reduced(username, message_ref)
        # Check if a response was found
        if response == '':
            # Check for translated triggers
            response = self.check_for_message_trigger_translated(username, message_ref)
        # Check if a response was found
        if response == '':
            # Remove common sentence ends
           message_ref.content = utils.remove_common_sentence_ends(message_ref.content)
            # Check for exact triggers
           response = self.get_send_message_trigger_response(username, message_ref)
        # Check if a response was found
        if response == '':
            # Check for reduced triggers next
            response = self.check_for_message_trigger_reduced(username, message_ref)
        # Check if a response was found
        if response == '':
            # Check for translated triggers
            response = self.check_for_message_trigger_translated(username, message_ref)
        
    def check_for_message_trigger_reduced(self, username, message_ref):
        # Get the reduced version of the message
        username = message_ref.author.name
        message_reduced = utils.reduce_text_to_minimum(message_ref)
        # Print the translated message
        print('    reduced message:')
        print('        ' + str(message_reduced.content).replace('\r\n', '\r\n        '))
        # Return the response
        return self.get_send_message_trigger_response(username, message_reduced)
    
    def check_for_message_trigger_translated(self, username, message_ref):
        # Get the translated version of the message
        message_translated = utils.translate_text_to_minimum(message_ref)
        # Print the translated message
        print('    translated message:')
        print('        ' + str(message_translated.content).replace('\r\n', '\r\n        '))
        # Return the response
        return self.get_send_message_trigger_response(username, message_translated)
    
    async def get_send_message_trigger_response(self, username, message_ref):
        message = message_ref.content
        # Wrap the function in a try statement
        try:
            # Set initial value
            response_to_send = ''
            available_responses = list([])
            # Make message lowercase
            message = message.lower()
            # Check if there is a trigger
            mt_id = self.dbc_ref.get_table_row_column('messages_triggers', 'mt_id', 'message_text', message, self.dbc_ref.DBNAME)
            # Check for an id
            if str(mt_id) != 'None':
                # Create a list of potential responses
                responses = self.dbc_ref.get_table_rows('messages_triggers_responses', 'mt_id', mt_id, '', self.dbc_ref.DBNAME)
            #reply = self.get_reply(the_dictionary.keywords, message_ref)
                # Cycle through all of the responses that match the username's player_type
                for row in responses:
                    # Get variables
                    response_text = str(row[1]).strip()
                    # Check for special case responses
            if '((' in response_text:
                        # Check the special case
                if '((ban))' in response_text.lower():
                            #self.bot_ref.ban_user(username) 
                    self.bot_ref.intial_channels[0].ban(username)                           
                elif '((timeout_noban))' in response_text.lower():
                    self.timeout_user_no_ban(username)
                elif '((timeout_ban))' in response_text.lower():
                    self.timeout_user_yes_ban(username)
                elif '((timeout_free))' in response_text.lower():
                            #self.timeout_user_no_counter(username, 30)
                    self.bot_ref.initial_channels[0].timeout(username, 30)
                elif '((timeout_free_30))' in response_text.lower():
                            #self.timeout_user_no_counter(username, 30)
                    self.bot_ref.initial_channels[0].timeout(username, 30)
                elif '((timeout_free_60))' in response_text.lower():
                            #self.timeout_user_no_counter(username, 60)
                    self.bot_ref.initial_channels[0].timeout(username, 60)
                elif '((timeout_free_90))' in response_text.lower():
                            #self.timeout_user_no_counter(username, 90)
                    self.bot_ref.initial_channels[0].timeout(username, 90)
                elif '((timeout_free_300))' in response_text.lower():
                            #self.timeout_user_no_counter(username, 300)
                    self.bot_ref.initial_channels[0].timeout(username, 300)
                elif '((timeout_free_600))' in response_text.lower():
                            #self.timeout_user_no_counter(username, 600)
                    self.bot_ref.initial_channels[0].timeout(username, 600)
                    # Remove text in case
                response_text = response_text.replace('((Ban))', '')
                response_text = response_text.replace('((ban))', '')
                response_text = response_text.replace('((Timeout_NoBan))', '')
                response_text = response_text.replace('((timeout_noban))', '')
                response_text = response_text.replace('((Timeout_Ban))', '')
                response_text = response_text.replace('((timeout_ban))', '')
                response_text = response_text.replace('((Timeout_Free))', '')
                response_text = response_text.replace('((timeout_free))', '')
                response_text = response_text.replace('((Timeout_Free_30))', '')
                response_text = response_text.replace('((timeout_free_30))', '')
                response_text = response_text.replace('((Timeout_Free_60))', '')
                response_text = response_text.replace('((timeout_free_60))', '')
                response_text = response_text.replace('((Timeout_Free_90))', '')
                response_text = response_text.replace('((timeout_free_90))', '')
                response_text = response_text.replace('((Timeout_Free_300))', '')
                response_text = response_text.replace('((timeout_free_300))', '')
                response_text = response_text.replace('((Timeout_Free_600))', '')
                response_text = response_text.replace('((timeout_free_600))', '')
                response_text = response_text.strip()
    
                if response_text != '':
                    available_responses.append(response_text)
                # Check for a response
                #if len(reply) > 0:
                    # Print the available responses
    
                    # Select a random response
                    response_index = (random.randint(1, len(available_responses)) - 1)
                    # Print the response index
                
                    # Pull the response from the list
                    message_ref.content = str(available_responses[response_index])
                    # Print the response text
                    #utils.o_print('        response_to_send: ' + str(response_to_send), False)
                    # Print the number of available responses to logs
                    #utils.o_print('message-controller: available_responses: ' + str(available_responses), True, True)
                    # Send the response as a chat message
                #await message.channel.send(f'@ {username} {utils.convert_response_keywords(message_ref)}')
        except KeyboardInterrupt as ki:
            utils.print_exception( ki,'get_send_message_trigger_response: username=' + str(username) + ', message=' + str(message))
        except Exception as e:
            utils.print_exception(e,'get_send_message_trigger_response: username=' + str(username) + ', message=' + str(message))
        # Return the response to send, empty if none found
        return utils.convert_response_keywords(message_ref)
    
    def timeout_user_yes_ban(self, username):
        # Get the timeout count
        timeout_count = int(self.get_user_timeout_count(username, True)) + 1
        # Get the number of times the user has been timed out
        if timeout_count <= gc.TWITCH_USER_MAX_TIMEOUT_COUNT:
            # Timeout the user
            self.bot_ref.timeout_user(username, int(timeout_count * 30))
        else:
            # Ban the user
            self.bot_ref.ban_user(username)
        # Increment the timeout count
        self.dbc_ref.set_user_value(username, gc.TWITCH_USER_VALUE_TIMEOUT_COUNT_BAN, int(timeout_count), self.dbc_ref.DBNAME)
            
    def timeout_user_no_ban(self, username):
        # Get the timeout count
        timeout_count = int(self.get_user_timeout_count(username, False)) + 1
        # Timeout the user
        self.bot_ref.timeout_user(username, int(timeout_count * 30))
        # Increase counter
        self.dbc_ref.set_user_value(username, gc.TWITCH_USER_VALUE_TIMEOUT_COUNT_NO_BAN, int(timeout_count), self.dbc_ref.DBNAME)
            
    #def timeout_user_no_counter(self, username, seconds):
        # Timeout the user
        #self.bot_ref.timeout_user(username, int(seconds))
        
    def set_chat_mode_based_on_message_list(self):
        # Wrap the function in a try statement
        try:
            # Get the length of the message list
            length = len(self.message_list)
            # Check the length
            if length >= gc.TWITCH_CHAT_MODE_THRESHOLD:
                # Subs only mode
                self.bot_ref.set_subs_only_mode_on()
                # Slow mode
                #self.bot_ref.set_slow_mode_on(30)
                self.bot_ref.get_initial_channels[0].slow()
                # Print the status
                #utils.o_print('message-controller: Messages(' + str(len(self.message_list)) + '/' + str(gc.TWITCH_CHAT_MODE_THRESHOLD) + ', ' + str(round(float(len(self.message_list)) / float(gc.TWITCH_CHAT_MODE_THRESHOLD), 2)) + '): engaging static game state, subs only chat mode, slow mode 30')
            else:  # Below threshold
                # Print the status
                #utils.o_print('message-controller: Messages(' + str(len(self.message_list)) + '/' + str(gc.TWITCH_CHAT_MODE_THRESHOLD) + ', ' + str(round(float(len(self.message_list)) / float(gc.TWITCH_CHAT_MODE_THRESHOLD), 2)) + ')')
                # Check the message list length
                if length < self.get_threshold_percentile(8):
                    # Set the chat mode
                    self.bot_ref.remove_all_chat_modes()
                elif length >= self.get_threshold_percentile(0.25):
                    # Set the chat mode
                    self.bot_ref.set_subs_only_mode_on()
                    # Slow mode
                    #self.bot_ref.set_slow_mode_on(15)
                    self.bot_ref.get_initial_channels[0].slow()
                elif length >= self.get_threshold_percentile(0.5):
                    # Set the chat mode
                    self.bot_ref.set_subs_only_mode_on()
                    # Slow mode
                    #self.bot_ref.set_slow_mode_on(10)
                    self.bot_ref.get_initial_channels[0].slow()
                elif length >= self.get_threshold_percentile(1):
                    # Set the chat mode
                    self.bot_ref.set_subs_only_mode_on()
                    # Slow mode
                    #self.bot_ref.set_slow_mode_on(5)
                    self.bot_ref.get_initial_channels.slow(0)
                elif length >= self.get_threshold_percentile(1.5):
                    # Set the chat mode
                    self.bot_ref.set_subs_only_mode_on()
                    # Slow mode
                    self.bot_ref.set_slow_mode_on(1)
                elif length >= self.get_threshold_percentile(2):
                    # Set the chat mode
                    self.bot_ref.set_follower_only_mode_on(1, 'week')
                    # Slow mode
                    self.bot_ref.set_slow_mode_on(5)
                elif length >= self.get_threshold_percentile(2.5):
                    # Set the chat mode
                    self.bot_ref.set_follower_only_mode_on(1, 'day')
                    # Slow mode
                    self.bot_ref.set_slow_mode_on(5)
                elif length >= self.get_threshold_percentile(4):
                    # Set the chat mode
                    self.bot_ref.set_follower_only_mode_on(1, 'hour')
                    # Slow mode
                    #self.bot_ref.set_slow_mode_on(5)
                    self.bot_ref.initial_channels[0].slow(0)
                elif length >= self.get_threshold_percentile(4):
                    # Set the chat mode
                    self.bot_ref.set_follower_only_mode_on(1, 'minute')
                    # Slow mode
                    self.bot_ref.set_slow_mode_on(15)
                elif length >= self.get_threshold_percentile(5):
                    # Set the chat mode
                    self.bot_ref.set_follower_only_mode_on(1, 'minute')
                    # Slow mode
                    #self.bot_ref.set_slow_mode_on(10)
                    self.bot_ref.initial_channels[0].slow()
                elif length >= self.get_threshold_percentile(6):
                    # Set the chat mode
                    self.bot_ref.set_follower_only_mode_on(1, 'minute')
                    # Slow mode
                    #self.bot_ref.set_slow_mode_on(5)
                    self.bot_ref.initial_channels[0].slow()
                elif length >= self.get_threshold_percentile(7):
                    # Set the chat mode
                    self.bot_ref.set_follower_only_mode_on(1, 'minute')
                    # Slow mode
                    #self.bot_ref.set_slow_mode_on(3)
                    self.bot_ref.initial_channels[0].slow()
                elif length >= self.get_threshold_percentile(8):
                    # Set the chat mode
                    self.bot_ref.set_follower_only_mode_on(1, 'minute')
                    # Slow mode
                    #self.bot_ref.set_slow_mode_on(1)
                    self.bot_ref.initial_channels[0].slow()
                else:
                    # All viewers mode
                    self.bot_ref.remove_all_chat_modes()
        except KeyboardInterrupt as ki:
            utils.print_exception( ki, 'set_chat_mode_based_on_message_list: len(self.message_list)=' + str(len(self.message_list)))
        except Exception as e:
            utils.print_exception(e, 'set_chat_mode_based_on_message_list: len(self.message_list)=' + str(len(self.message_list)))
    
    def get_threshold_percentile(self, multiplier):
        return int(gc.TWITCH_CHAT_MODE_THRESHOLD - int(float(multiplier) * gc.TWITCH_CHAT_MODE_THRESHOLD))
    
    def make_user_vip(self, username, player_type):
        # Get the VIP count
        vip_count = self.dbc_ref.exec_db_query_return_single_value("SELECT COUNT username FROM users_values WHERE value_type='" + gc.TWITCH_USER_VALUE_IS_VIP + "' AND value_reference='True'", self.dbc_ref.DBNAME)
        # Check if there is room for another VIP
        if int(vip_count) < gc.TWITCH_CONTROLLER_MAX_VIP:
            # Make the user VIP
            self.bot_ref.make_vip(username)
            # Save the VIP status
            self.dbc_ref.set_user_value(username, gc.TWITCH_USER_VALUE_IS_VIP, 'True', self.dbc_ref.DBNAME)
    
    def remove_user_vip(self, username):
        # Make the user VIP
        self.bot_ref.make_vip(username, False)
        # Save the VIP status
        self.dbc_ref.set_user_value(username, gc.TWITCH_USER_VALUE_IS_VIP, 'False', self.dbc_ref.DBNAME)


