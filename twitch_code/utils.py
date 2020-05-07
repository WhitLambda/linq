# utils.py
# Contains common functions
import word_lists as wl
import word_lists_unwanted as wlu
import response_lists as rl
import global_constants as gc
import linecache
import math
#import pyglet
import random
import re
import sys
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from string import ascii_lowercase
from twitchio.ext import commands

# Global variable
util_trigger_list = list([])  # Keeps track of utility triggers


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
    print(gc.PRINT_LINE_BREAK)
    print('~ ' + str(exc_type))
    print('~ ' + str(filename))
    print('~ LINE: ' + str(lineno))
    print('~ CODE: ' + str(line.strip()))
    print('~ ERROR: ' + str(exc_obj))
    print('~ TIME: ' + str(datetime.now()))
    if unique !='':
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


# Function: print_alert
# Prints alert messages
# Parameters:
#   message  -- the message to display
def print_alert(message=''):
    # Print the exception
    print('')
    print(gc.PRINT_LINE_BREAK)
    print(gc.PRINT_LINE_BREAK)
    print('~ ' + str(message))
    print(gc.PRINT_LINE_BREAK)
    print(gc.PRINT_LINE_BREAK)
    print('')


# Function: print_to_file
# Prints the message to the parameter file
def print_to_file(print_file_in, mb):
    print_file = open(print_file_in, "a")
    if '\r\n' in mb:
        for line in mb.split('\r\n'):
            if line != '':
                print >> print_file, str(line).replace('\r\n', '')
    else:
        print >> print_file, str(mb)
    print_file.close()


# Function: print_chat
# Prints the message to the parameter file
def print_chat(message, username):
    try:
        # Print simple chat
        chat_file = 'logs\chat-' + str(gc.PROGRAM_PRINT_OUT)
        print_to_file(chat_file, '@' + str(username) + ': ' + str(message))
        print_to_file(chat_file, ' ')
        # Print extended chat information
        chat_file_info = 'logs\chat-' + str(gc.PROGRAM_PRINT_OUT).replace('.txt', '') + '-info.txt'
        print_to_file(chat_file_info, '@' + str(username) + ' {' + str(datetime.now()) + '}')
        print_to_file(chat_file_info, '    o: ' + str(message))
        print_to_file(chat_file_info, '    r: ' + reduce_text_to_minimum(message))
        print_to_file(chat_file_info, '    m: ' + translate_text_to_minimum(message))
        print_to_file(chat_file_info, ' ')
    except Exception as e:
        print_exception(e, 'print_chat')


# Function: pull_utils_triggers
# Gets a list of triggers created within utils.py
def pull_utils_triggers():
    # Reference global variables
    global util_trigger_list
    # Make a copy of the trigger list
    return_list = list(util_trigger_list)
    # Empty the trigger list
    util_trigger_list = list([])
    # Return a copy of the list
    return return_list


# Function: add_trigger
# Keeps track of triggers
# Parameters:
#   trigger -- the trigger to add
def add_utils_trigger(trigger):
    # Check for an existing trigger
    if trigger == '':
        return
    # Add the trigger to the list
    util_trigger_list.append(str(trigger))


# Function: get_full_trigger_reference
# Creates the full reference string for a trigger
# Parameters:
#   trigger -- the trigger reference string
#   values  -- the number of values the trigger requires
def get_full_trigger_reference(trigger, value_list):
    # Check for an existing trigger
    if trigger == '':
        return ''
    values = len(value_list)
    # Validate the values type
    try:
        values = int(values)
    except KeyboardInterrupt as ki:
        print_exception(ki, 'get_full_trigger_reference 1b')
    except Exception as e:
        print_exception(e, 'get_full_trigger_reference 1')
    # Validate the number count
    if values < 0:
        values = 0
    # Add the value places
    if values > 0:
        for n in range(1, values + 1):
            # Add the value wrap
            trigger = trigger + (str(gc.REPLACE_FULL).replace('.#**', '.' + str(n) + '**'))
    # Return the update trigger reference
    return trigger


# Function: replace_trigger_value
# Replaces trigger values
# Parameters:
#   trigger -- the trigger reference string
#   index   -- the 1-based value index to replace
#   value   -- the value to assign
def replace_trigger_value(trigger, index, value):
    # Check for an existing trigger
    if trigger == '':
        return ''
    # Check the index type
    try:
        index = int(index)
    except KeyboardInterrupt as ki:
        print_exception(ki, 'replace_trigger_value (' + str(index) + ')')
    except Exception as e:
        print_exception(e, 'replace_trigger_value (' + str(index) + ')')
    # Replace the value
    trigger = str(trigger).replace(str(gc.REPLACE_FULL).replace('.#**', '.' + str(index) + '**'), gc.REF_VALUE_S + str(value) + gc.REF_VALUE_E)
    # Return the update trigger reference
    return trigger


# Function: get_trigger_values
# Strips a trigger string and returns the values
# Parameters:
#   trigger -- the trigger reference string
def get_trigger_values(trigger):
    # Create an empty list to fill with values
    values = list([])
    # Cycle through the values, put them in a list
    for value in trigger.split(gc.REF_VALUE_S):
        # Strip the reference characters wrapping the value
        value = str(value[0:len(str(value)) - 1])
        # Put the value in a list
        values.append(value)
    # Remove the first item
    values.pop(0)
    # Return the list of values
    return values


# Function: set_system_message
# Sends a system message to the screen
# Parameters:
#   message -- the message string to display
def set_system_message(message):
    value_list = []
    # Check for an existing message
    if message == '':
        return
    value_list.append(message)
    # Print function use
    print('utils: set_system_message(' + str(message) + ')')
    # Add the trigger to the list, replacing the message within the trigger
    create_add_trigger_value(gc.SMS_MESSAGE_SYSTEM, value_list)    


def print_dictionary(dict_to_print, name=''):
    # Show start of print
    if name != '':
        print(name + ' Key/Value Pairs (' + str(len(dict_to_print)) + '):', True)
    else:
        print('Dictionary Key/Value Pairs (' + str(len(dict_to_print)) + '):', True)
    # Cycle through dictionary items
    for k in dict_to_print:
        print('    ' + str(k) + ': ' + str(dict_to_print[k]), True)


def print_list(list_to_print, name=''):
    # Show start of print
    if name != '':
        print(name + ' values (' + str(len(list_to_print)) + '):')
    else:
        print('List Values (' + str(len(list_to_print)) + '):')
    # Cycle through list
    for x in range(len(list_to_print)): 
        print(list_to_print[x])





def translate_text_to_minimum(text_to_translate_ref):
    # Make the text lowercase

    text_to_translate = text_to_translate_ref.content.lower().strip()
    # Check for text
    if text_to_translate == '':
        return ''
    # Remove tagged user
    text_to_translate = text_to_translate.replace('@' + gc.TWITCH_CONTROLLER_CHAN.lower(), '').strip()
    text_to_translate = text_to_translate.replace(gc.TWITCH_CONTROLLER_CHAN.lower(), '').strip()
    # Replace min/reduce dictionary key/value pairs
    text_to_translate = replace_key_value(text_to_translate, wl.min_reduce_dict)
    # Check for text
    if text_to_translate == '':
        return ''
    # Cleanup repeating characters
    text_to_translate = replace_double_lowercase_characters(text_to_translate).strip()
    # Cycle through replace key/value pairs
    for key in wl.minimize_dict_1.keys():
        text_to_translate = text_to_translate.replace(str(key), str(wl.minimize_dict_1[key]))
    # Check for text
    if text_to_translate == '':
        return ''
    # Replace common mispellings
    text_to_translate = replace_common_misspellings(text_to_translate)
    # Replace numbers
    #text_to_translate = replace_numbers(text_to_translate, ' number ')
    # Strip non-alpha characters
    text_to_translate = strip_non_alpha(text_to_translate, False, False)
    # Check for text
    if text_to_translate == '':
        return ''
    # Check if the text ends in a space, if not add it
    if not text_to_translate.endswith(' '):
        text_to_translate = text_to_translate + ' '
    # Replace dictionary 2 key/value pairs
    text_to_translate = replace_key_value(text_to_translate, wl.minimize_dict_2)
    # Check for text
    if text_to_translate == '':
        return ''
    # Replace double spaces
    text_to_translate = replace_double_spaces(text_to_translate)
    # Replace dictionary 3 key/value pairs
    text_to_translate = replace_key_value(text_to_translate, wl.minimize_dict_3)
    # Check for text
    if text_to_translate == '':
        return ''
    # Replace double spaces
    text_to_translate = replace_double_spaces(text_to_translate)
    # Replace dictionary 4 key/value pairs
    text_to_translate = replace_key_value(text_to_translate, wl.minimize_dict_4)
    # Check for text
    if text_to_translate == '':
        return ''
    # Replace double spaces
    text_to_translate = replace_double_spaces(text_to_translate)
    # Replace dictionary 5 key/value pairs
    text_to_translate = replace_key_value(text_to_translate, wl.minimize_dict_5)  
    # Check for text
    if text_to_translate == '':
        return ''
    # Replace double spaces
    text_to_translate = replace_double_spaces(text_to_translate)
    # Strip the text
    text_to_translate = text_to_translate.strip()
    # Check for a change
    #if text_to_translate != text_to_translate_ref:
        # Repeat the function until no changes are made
        #return translate_text_to_minimum(text_to_translate)
    # Return the minimized text
    text_to_translate_ref.content = text_to_translate
    return text_to_translate_ref

    
def reduce_text_to_minimum(text_to_reduce_ref, strip_exclamation=True):
    text_to_reduce = text_to_reduce_ref.content
    # Make the text lowercase
    return_text = str(text_to_reduce).lower().strip()
    # Check for a string
    if str(return_text) == '':
        return ''
    text_to_reduce_ref.content = return_text
    # Replace min/reduce dictionary key/value pairs
    return_text = replace_key_value(return_text, wl.min_reduce_dict)
    # Check for text
    if return_text == '':
        return ''
    # Strip non-alpha characters
    return_text = strip_non_alpha(return_text, strip_exclamation, False)
    # Check for text
    if return_text == '':
        return ''
    # Cleanup repeating characters
    return_text = replace_double_lowercase_characters(return_text).strip()
    # Replace common misspellings
    return_text = replace_common_misspellings(return_text)
    # Cleanup spaces
    return_text = replace_double_spaces(return_text).strip()
    # Strip the text
    return_text = return_text.strip()
    text_to_reduce_ref.content = return_text
    # Check for a change
    if return_text != text_to_reduce:
        # Call the function until no changes are made
        text_to_reduce_ref.content = reduce_text_to_minimum(text_to_reduce_ref).content
        return text_to_reduce_ref
    text_to_reduce_ref.content = return_text
    # Return the text
    return text_to_reduce_ref


def replace_base_commands(message):
    # Trim
    message = message.strip()
    # !support
    message = message.replace("!suport", "!support")
    return message


def strip_non_alpha(text_to_strip, strip_exclamation_point=False, strip_space=False):
    # Build the Regular Expression
    reg_ex = '[^a-z'
    # Check if spaces are stripped
    if not strip_space:
        reg_ex = reg_ex + ' '
    # Check if ! are stripped
    if not strip_exclamation_point:
        reg_ex = reg_ex + '!'
    # Close the Regular Expression
    reg_ex = reg_ex + ']'
    # Strip non-alphanumeric characters
    text_to_strip = re.sub(r'' + reg_ex + '', '', text_to_strip)
    # Return the stripped text
    return text_to_strip.strip()


def strip_non_alphanumeric(text_to_strip, strip_exclamation_point=False, strip_space=False):
    # Build the Regular Expression
    reg_ex = '[^a-z0-9'
    # Check if spaces are stripped
    if not strip_space:
        reg_ex = reg_ex + ' '
    # Check if ! are stripped
    if not strip_exclamation_point:
        reg_ex = reg_ex + '!'
    # Close the Regular Expression
    reg_ex = reg_ex + ']'
    # Strip non-alphanumeric characters
    text_to_strip = re.sub(r'' + reg_ex + '', '', text_to_strip)
    # Return the stripped text
    return text_to_strip.strip()


def replace_double_spaces(text_ref):
    # Setup the ref
    text = text_ref
    # Replace double spaces
    text = text.replace('  ', ' ')
    # Check for a non change
    if text != text_ref:
        return replace_double_spaces(text)
    # Return the text
    return text


def replace_double_lowercase_characters(text_ref):
    # Setup the ref
    text = text_ref.lower()
    # Loop through lowercase alphabet
    for char in ascii_lowercase:
        # Replace triple characters with a double
        text = text.replace(char + char + char, char + char)
    # Check for a non change
    if text != text_ref:
        return replace_double_lowercase_characters(text)
    # Return the text
    return text
    
    

def replace_key_value(text_to_update, dict_to_use):
    # Cycle through replace key/value pairs
    for key in dict_to_use.keys():
        # Replace the key directly
        text_to_update = text_to_update.replace(str(key), str(dict_to_use[key]))
        # Replace the key with left spaces removed, .startswith only
        if str(key).startswith(' '):
            if text_to_update.startswith(str(key).lstrip()):
                text_to_update = text_to_update.replace(str(key).lstrip(), str(dict_to_use[key]), 1) 
        # Check if the text ends in a space, if not add it
        if not text_to_update.endswith(' '):
            text_to_update = text_to_update + ' '  
        # Replace the key with left spaces removed, .endswith only
        if str(key).endswith(' '):
            if text_to_update.endswith(str(key).rstrip()):
                text_to_update = text_to_update.replace(str(key).rstrip(), str(dict_to_use[key]), 1)
    # Return the updated text
    return text_to_update


def contains_profanity(text_to_check):
    # Translate the text to its minimum value
    text_to_check = translate_text_to_minimum(text_to_check)
    # Cycle through profanity list
    text = text_to_check.content
    for profane in wlu.profanity_list:
        # Check if the word is in the text
        if ' ' + profane.lower() + ' ' in text:
            return True
        if text.startswith(profane.lower() + ' '):
            return True
        if text.endswith(' ' + profane.lower()):
            return True
        if text_to_check == profane.lower():
            return True
    # No profanity found
    return False


def contains_timeout_word(text_to_check):
    # Translate the text to its minimum value
    text_to_check = translate_text_to_minimum(text_to_check)
    # Cycle through profanity list
    text = text_to_check.content
    for timeout_word in wlu.timeout_no_ban_list:
        # Check if the word is in the text
        if ' ' + timeout_word.lower() + ' ' in text:
            return True
        if text.startswith(timeout_word.lower() + ' '):
            return True
        if text.endswith(' ' + timeout_word.lower()):
            return True
        if text == timeout_word.lower():
            return True
    # No timeout words found
    return False


def contains_self_promo(text_to_check):
    # Translate the text to its minimum value
    text_to_check = translate_text_to_minimum(text_to_check)
    # Cycle through self promo list
    text = text_to_check.content
    for self_promo in wlu.self_promo_list:
        # Check if the phrase is in the text
        if ' ' + self_promo.lower() + ' ' in text:
            return True
        if text.startswith(self_promo.lower() + ' '):
            return True
        if text.endswith(' ' + self_promo.lower()):
            return True
        if text == self_promo.lower():
            return True
    # No self promo phrase found
    return False


def get_date_now():
    return datetime.now().strftime("%Y-%m-%d")


def get_datetime_now_hour():
    return datetime.now().strftime("%Y-%m-%d %H")


def get_datetime_now_add_seconds(time_to_add):
    return (datetime.now() + timedelta(seconds=time_to_add))


def get_datetime_now_add_minutes(time_to_add):
    return (datetime.now() + timedelta(minutes=time_to_add))


def get_datetime_now_add_hours(time_to_add):
    return (datetime.now() + timedelta(hours=time_to_add))


def get_datetime_now_add_days(time_to_add):
    return (datetime.now() + timedelta(days=time_to_add))


def get_datetime_now_add_time(seconds_to_add = 0, minutes_to_add = 0, hours_to_add = 0, days_to_add = 0):
    return (datetime.now() + timedelta(days=days_to_add, hours=hours_to_add, minutes=minutes_to_add, seconds=seconds_to_add))


def get_datetime_object_add_time(datetime_object, seconds_to_add = 0, minutes_to_add = 0, hours_to_add = 0, days_to_add = 0):
    return (datetime_object + timedelta(days=days_to_add, hours=hours_to_add, minutes=minutes_to_add, seconds=seconds_to_add))


def get_date_object(year, month, day):
    return date(year, month, day)


def get_weekday(date_to_check):
    return date.weekday(date_to_check)


def printable_query(query, leading_spacer=True):
    # Set initial values
    spacer = '\r\n    '
    # Add splits
    query = query.replace(') VALUES', ')' + spacer + 'VALUES')
    query = query.replace('(', spacer + '(')
    # Check for a leading spacer
    if leading_spacer:
        # Return the query
        return str(spacer + query)
    # Return without the leading spacer
    return str(query)


# Function: set_chat_mode_threshold_with_trigger
# Changes the chat mode threshold
# Parameters:
#   threshold -- the threshold to set
def set_chat_mode_threshold_with_trigger(threshold=1000):
    values = []
    values.append(threshold)
    print('set_chat_mode_threshold_with_trigger(threshold=' + str(threshold) + ')')
    create_add_trigger_value(gc.TMS_CONTROLLER_THRESHOLD, threshold)


def create_add_trigger_value(trigger_reference, values):
    if len(values) == 0:
        add_utils_trigger(trigger_reference)
    else:
        trigger = get_full_trigger_reference(trigger_reference, values)
        for i in range(0, len(values) - 1):
            trigger = replace_trigger_value(trigger, i + 1, values[i])
        add_utils_trigger(trigger)



   
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]  
    else:
        return text


def create_ghost_chat_message(message, sender_username=gc.TWITCH_CONTROLLER_GHOST_USERNAME + '_param'):
    # Print the function call
    print('utils: create_ghost_chat_message(sender_username=' + str(sender_username) + ', message=' + str(message) + ')')
    # Add the message to the unprocessedlist
    gc.TWITCH_UNPROCESSED_MESSAGES.append([str(sender_username.lower()), str(message)])


def create_ghost_chat_messages(number_of_messages):
    # Print the function call
    print('utils: create_ghost_chat_messages(number_of_messages=' + str(number_of_messages) + ')')
    # Cycle through messages
    for num in range(1, number_of_messages):
        # Create a ghost message
        create_ghost_chat_message('This is a test message from ghost user (' + str(gc.TWITCH_CONTROLLER_GHOST_USERNAME + '_' + str(num)) + '): ' + str(time.time()), gc.TWITCH_CONTROLLER_GHOST_USERNAME + '_' + str(num))


def set_chat_mode_threshold(threshold=1000):
    # Print the function call
    print('utils: set_chat_mode_threshold(threshold=' + str(threshold) + ')')
    # Validate the threshold
    try:
        threshold = min(100000, max(200, int(threshold)))
    except KeyboardInterrupt as ki:
        print_exception(ki, 'set_chat_mode_threshold(threshold=' + str(threshold) + ')')
        threshold = 1000
    except Exception as e:
        print_exception(e, 'set_chat_mode_threshold(threshold=' + str(threshold) + ')')
        threshold = 1000
    # Set the threshold
    gc.CHAT_MODE_THRESHOLD = threshold
    # Set the threshold split
    gc.CHAT_MODE_THRESHOLD_SPLIT = min(1200, int(threshold * 0.05))


def get_message_command_value(command, message):
    # Print the function call
    print('get_message_command_value(command=' + str(command) + ', message=' + str(message) + ')')
    # Wrap the function in a try statement
    try:
        # Remove the command, return the value
        return str(remove_prefix(str(message).strip(), str(command).strip()).strip())
    except KeyboardInterrupt as ki:
        print_exception(ki, 'get_message_command_value(command=' + str(command) + ', message=' + str(message) + ')')
    except Exception as e:
        print_exception(e, 'get_message_command_value(command=' + str(command) + ', message=' + str(message) + ')')
    return 'None'
    
    
def get_message_command_value_int(command, message, on_fail_value=0):
    # Wrap the function in a try statement
    try:
        # Get the value
        command_value = get_message_command_value(command, message)
        print('command_value: [' + str(command_value) + ']')
        # Return the int value
        return int(command_value)
    except KeyboardInterrupt as ki:
        print_exception(ki, 'get_message_command_value_int(command=' + str(command) + ', message=' + str(message) + ')')        
    except Exception as e:
        print_exception(e, 'get_message_command_value_int(command=' + str(command) + ', message=' + str(message) + ')')
    # Return the on failv alue
    return on_fail_value

    
def convert_response_keywords(message_ref, username='', include_username_at=True):
    # Get the message
    message = message_ref.content
    # Replace keywords
  
    message = message.replace('((Yes))', get_random_affirmative())
    message = message.replace('((yes))', get_random_affirmative().lower())
    message = message.replace('((No))', get_random_negative())
    message = message.replace('((no))', get_random_negative().lower())
    message = message.replace('((Hi))', get_random_greeting())
    message = message.replace('((hi))', get_random_greeting().lower())
    message = message.replace('((Hey))', get_random_greeting())
    message = message.replace('((hey))', get_random_greeting().lower())
    message = message.replace('((Hello))', get_random_greeting())
    message = message.replace('((hello))', get_random_greeting().lower())
    message = message.replace('((Good))', get_random_good())
    message = message.replace('((good))', get_random_good().lower())
    message = message.replace('((Happy))', get_random_happy())
    message = message.replace('((happy))', get_random_happy().lower())
    message = message.replace('((ThankYou))', get_random_thanks())
    message = message.replace('((thankyou))', get_random_thanks().lower())
    message = message.replace('((Thank-You))', get_random_thanks())
    message = message.replace('((thank-you))', get_random_thanks().lower())
    message = message.replace('((Thanks))', get_random_thanks())
    message = message.replace('((thanks))', get_random_thanks().lower())
    # Random values
    #message = message.replace('((random0))', get_random_number_digits(0))
    #message = message.replace('((random1))', get_random_number_digits(1))
    #message = message.replace('((random2))', get_random_number_digits(2))
    #message = message.replace('((random3))', get_random_number_digits(3))
    #message = message.replace('((random4))', get_random_number_digits(4))
    #message = message.replace('((random5))', get_random_number_digits(5))
    #message = message.replace('((random6))', get_random_number_digits(6))
    #message = message.replace('((random7))', get_random_number_digits(7))
    #message = message.replace('((random8))', get_random_number_digits(8))
    #message = message.replace('((random9))', get_random_number_digits(9))
    message = message.replace('((random-0-10))', get_random_number(0, 10))
    message = message.replace('((random-0-100))', get_random_number(0, 100))
    message = message.replace('((random-0-1000))', get_random_number(0, 1000))
    message = message.replace('((random-1-10))', get_random_number(1, 10))
    message = message.replace('((random-1-100))', get_random_number(1, 100))
    message = message.replace('((random-1-1000))', get_random_number(1, 1000))
    # Replace full responses
    message = message.replace('((Food))', get_random_food_response())
    message = message.replace('((food))', get_random_food_response())
    message = message.replace('((Bye))', get_random_goodbye())
    message = message.replace('((bye))', get_random_goodbye())
    message = message.replace('((Dismiss))', get_random_dismiss())
    message = message.replace('((dismiss))', get_random_dismiss().lower())
    message = message.replace('((Dismis))', get_random_dismiss())
    message = message.replace('((dismis))', get_random_dismiss().lower())
    message = message.replace('((Not-Here))', get_random_not_here())
    message = message.replace('((not-here))', get_random_not_here().lower())
    # positive adjective
    message = message.replace('((Positive-Adjective))', get_random_positive_adjective())
    message = message.replace('((positive-adjective))', get_random_positive_adjective().lower())
    message = message.replace('((PAdj))', get_random_positive_adjective())
    message = message.replace('((padj))', get_random_positive_adjective().lower())
    message = message.replace('((P-Adj))', get_random_positive_adjective())
    message = message.replace('((p-adj))', get_random_positive_adjective().lower())
    # negative adjective
    message = message.replace('((Negative-Adjective))', get_random_negative_adjective())
    message = message.replace('((negative-adjective))', get_random_negative_adjective().lower())
    message = message.replace('((NAdj))', get_random_negative_adjective())
    message = message.replace('((nadj))', get_random_negative_adjective().lower())
    message = message.replace('((N-Adj))', get_random_negative_adjective())
    message = message.replace('((n-adj))', get_random_negative_adjective().lower())
    # positive attr+9active
    message = message.replace('((Positive-Attractive))', get_random_positive_attractive())
    message = message.replace('((positive-attractive))', get_random_positive_attractive().lower())
    message = message.replace('((PAtt))', get_random_positive_attractive())
    message = message.replace('((patt))', get_random_positive_attractive().lower())
    message = message.replace('((P-Att))', get_random_positive_attractive())
    message = message.replace('((p-att))', get_random_positive_attractive().lower())
    # negative attractive
    message = message.replace('((Negative-Attractive))', get_random_negative_attractive())
    message = message.replace('((negative-attractive))', get_random_negative_attractive().lower())
    message = message.replace('((NAtt))', get_random_negative_attractive())
    message = message.replace('((natt))', get_random_negative_attractive().lower())
    message = message.replace('((N-Att))', get_random_negative_attractive())
    message = message.replace('((n-att))', get_random_negative_attractive().lower())
    # Replace username keywords with one version
    message = message.replace('((@username))', '((username))')
    message = message.replace('((@Username))', '((username))')
    message = message.replace('((Username))', '((username))')
    # Replace duplicate username keywords
    for n in range(1, 3):
        n = n  # Remove warning
        message = message.replace('((username))((username))', '((username))')
        message = message.replace('((username))((username))', '((username))')
        message = message.replace('((username)) ((username))', '((username)) ')
        message = message.replace('((username)) ((username)),', '((username)), ')
        message = message.replace('((username)), ((username))', '((username)), ')
        message = message.replace('((username)),, ', '((username)), ')
        message = message.replace('((username)),  ', '((username)), ')
        message = message.replace('((username))  ', '((username)) ')
    # Check if the @ should be added
    if include_username_at:
        message = message.replace('((username))', '((@username))')
    # Check for a username
    if username != '':
        message = message.replace('((username))', username.lower())
        message = message.replace('((@username))', '@' + username.lower())
    else:
        # Remove username keyword
        message = message.replace('((username))', '')
        message = message.replace('((@username))', '')
    message_ref.content = message
    # Return the message
    return message_ref


def get_random_greeting():
    # Get a random number
    rand = random.randint(1, 10)
    # Return the reference
    if rand == 1:
        return 'Sup'
    elif rand == 2:
        return 'Hey'
    elif rand == 3:
        return 'Hello'
    elif rand == 4:
        return "What's up?"
    elif rand == 5:
        return 'Hey there!'
    elif rand == 6:
        return 'Greetings'
    elif rand == 7:
        return 'Welcome'
    else:
        return 'Hi'


def get_random_dismiss():
    # Get a random number
    rand = random.randint(1, 4)
    # Return the reference
    if rand == 1:
        return 'Who are you?'
    elif rand == 2:
        return 'Go away'
    elif rand == 3:
        return 'Why are you here?'
    else:
        return 'No one asked for your opinion'


def get_random_not_here():
    # Get a random number
    rand = random.randint(1, 4)
    # Return the reference
    if rand == 1:
        return "Please don't do that here"
    else:
        return "We don't do that here"

  

def get_random_affirmative():
    # Get a random number
    rand = random.randint(1, 5)
    # Return the reference
    if rand == 1:
        return 'Sure'
    elif rand == 2:
        return 'Absolutely'
    elif rand == 3:
        return 'Yeah'
    elif rand == 4:
        return 'Yep'
    else:
        return 'Yes'


def get_random_negative():
    # Get a random number
    rand = random.randint(1, 5)
    # Return the reference
    if rand == 1:
        return 'Nope'
    elif rand == 2:
        return 'Nah'
    else:
        return 'No'
    
def get_random_food_response():
    # Get a random number
    rand = random.randint(1, 3)
    # Return the reference
    if rand == 1:
        return 'Depends on my mood'
    elif rand == 2:
        return "I'm a big fan of any food"
    else:
        return 'I like food in general'

def get_random_goodbye():
    # Get a random number
    rand = random.randint(1, 3)
    # Return the reference
    if rand == 1:
        return "Come back soon!"
    elif rand == 2:
        return "Thank you for visiting!"
    else:
        return "Please come back soon!"


def get_random_good():
    # Get a random number
    rand = random.randint(1, 4)
    # Return the reference
    if rand == 1:
        return 'Great'
    elif rand == 2:
        return 'Wonderful'
    elif rand == 3:
        return 'Awesome'
    else:
        return 'Good'


def get_random_happy():
    # Get a random number
    rand = random.randint(1, 2)
    # Return the reference
    if rand == 1:
        return 'Glad'
    else:
        return 'Happy'


def get_random_thanks():
    # Get a random number
    rand = random.randint(1, 7)
    # Return the reference
    if rand == 1:
        return 'Thanks'
    if rand == 2:
        return 'Thank you lots'
    if rand == 3:
        return 'Thank you so much'
    if rand == 4:
        return 'Thanks so much'
    if rand == 5:
        return 'Thank you very much'
    else:
        return 'Thank you'


def get_random_number(low_num, high_num):
    # Get a random number
    rand = random.randint(low_num, high_num)
    # Return the random number
    return str(rand)



def send_alert_message_with_trigger(message, queue_num=1, alert_type=gc.ALERT_TYPE_WS_BB):
    create_add_trigger_value_3(gc.SMS_MESSAGE_ALERT, str(message), queue_num, str(alert_type))


def send_chat_message_with_trigger(message):
    create_add_trigger_value_1(gc.TMS_CONTROLLER_MESSAGE, str(message))


def send_chat_alert_with_trigger(message, alert_type=gc.ALERT_TYPE_WS_BB, queue_num=1):
    # Send chat message
    send_chat_message_with_trigger(message)
    # Send alert message
    send_alert_message_with_trigger(message, queue_num, alert_type)
    
    
def username_is_tester(username):
    # Make username lowercase
    username = username.lower()
    # Check if the username is a tester
    if username == 'tmi':
        return True
    elif username == gc.TWITCH_CONTROLLER_CHAN.lower():
        return True
    elif username == gc.ANONYMOUS:
        return True
    elif username == 'dtscrockett':
        return True
    elif username == 'linqlambda':
        return True
    # Return not a tester
    return False


def get_filled_list_str(list_size=100, message_starts_with=''):
    # Create a list
    new_list = list([])
    # Fill the list
    for n in range(1, min(max(list_size, 10), 1000)):
        # Remove warning
        n = n
        # Reset the word
        word = ''
        # Get a random length
        rand_length = random.randint(5, 10)
        # Cycle through length
        for m in range(1, rand_length):
            # Remove warning
            m = m
            # Get a letter
            word = word + chr(random.randint(97, 122))
        # Add the word to the list
        new_list.append(message_starts_with + word)
    # Return the list
    return new_list


def send_multiple_chat_messages(message_list):
    o_print('utils: send_multiple_chat_messages(' + str(len(message_list)) + ')')
    # Cycle through messages
    for message in message_list:
        # Send the message
        send_chat_message_with_trigger(message)


def set_system_message_visible_with_trigger(is_visible=True):
    create_add_trigger_value_1(gc.SMS_MESSAGE_SYSTEM_VISIBLE, is_visible)


def get_random_question_for_chat():
    # Get a random index
    ran_index = random.randint(0, len(rl.question_for_chat) - 1)
    # Return the question
    return rl.question_for_chat[ran_index]


def clean_database_user_messages_with_trigger(username):
    create_add_trigger_value_1(gc.DB_CLEAN_USER_MESSAGES, username)


def clean_database_user_commands_with_trigger(username='all'):
    create_add_trigger_value_1(gc.DB_CLEAN_USER_COMMANDS, username)
    
    
def replace_common_misspellings(text_to_check):
    # Make lowercase
    text_to_check = text_to_check.lower()
    # Replace common misspelled words
    text_to_check = text_to_check.replace('suppourter', 'supporter')
    text_to_check = text_to_check.replace('missclick', 'misclick')
    text_to_check = text_to_check.replace('revell', 'reveal')
    text_to_check = text_to_check.replace('atack', 'attack')
    text_to_check = text_to_check.replace('qustion', 'question')
    text_to_check = text_to_check.replace('queston', 'question')
    text_to_check = text_to_check.replace('m7ch', 'much')
    text_to_check = text_to_check.replace('rthis', 'this')
    text_to_check = text_to_check.replace('comand', 'command')
    text_to_check = text_to_check.replace('especific', 'specific')
    text_to_check = text_to_check.replace('happend', 'happened')
    # Return the text
    return text_to_check


def remove_common_sentence_starts_ends(text_to_check):
    # Remove starts
    text_to_check = remove_common_sentence_starts(text_to_check)
    # Remove end
    text_to_check = remove_common_sentence_ends(text_to_check)
    # Return the string
    return text_to_check


def remove_common_sentence_starts(text_to_check):
    # Make lowercase
    text_to_check = text_to_check.lower().strip()
    # Replace misspellings first
    text_to_check = replace_common_misspellings(text_to_check)
    # Replace common misspelled words
    text_to_check = remove_sentence_start(text_to_check, 'ah ')
    text_to_check = remove_sentence_start(text_to_check, 'alright ')
    text_to_check = remove_sentence_start(text_to_check, 'also ')
    text_to_check = remove_sentence_start(text_to_check, 'and ')
    text_to_check = remove_sentence_start(text_to_check, 'but ')
    text_to_check = remove_sentence_start(text_to_check, 'bye ')
    text_to_check = remove_sentence_start(text_to_check, 'can you ')
    text_to_check = remove_sentence_start(text_to_check, 'could you ')
    text_to_check = remove_sentence_start(text_to_check, 'correct me if i am wrong ')
    text_to_check = remove_sentence_start(text_to_check, 'correct me if i am wrong but ')
    text_to_check = remove_sentence_start(text_to_check, 'dad ')
    text_to_check = remove_sentence_start(text_to_check, 'dad said ')
    text_to_check = remove_sentence_start(text_to_check, 'dad wants to know ')
    text_to_check = remove_sentence_start(text_to_check, 'did you know ')
    text_to_check = remove_sentence_start(text_to_check, 'did you know that ')
    text_to_check = remove_sentence_start(text_to_check, 'do ')
    text_to_check = remove_sentence_start(text_to_check, 'good ')
    text_to_check = remove_sentence_start(text_to_check, 'hi ')
    text_to_check = remove_sentence_start(text_to_check, 'hello ')
    text_to_check = remove_sentence_start(text_to_check, 'hello yes ')
    text_to_check = remove_sentence_start(text_to_check, 'hey ')
    text_to_check = remove_sentence_start(text_to_check, 'hi again ')
    text_to_check = remove_sentence_start(text_to_check, 'hello again ')
    text_to_check = remove_sentence_start(text_to_check, 'hey again ')
    text_to_check = remove_sentence_start(text_to_check, 'hmm ')
    text_to_check = remove_sentence_start(text_to_check, 'i am do it to ')
    text_to_check = remove_sentence_start(text_to_check, 'I got to know ')
    text_to_check = remove_sentence_start(text_to_check, 'I think ')
    text_to_check = remove_sentence_start(text_to_check, 'I want to know ')
    text_to_check = remove_sentence_start(text_to_check, 'my first question is ') 
    text_to_check = remove_sentence_start(text_to_check, 'nevermind ') 
    text_to_check = remove_sentence_start(text_to_check, 'no ') 
    text_to_check = remove_sentence_start(text_to_check, 'not much ')
    text_to_check = remove_sentence_start(text_to_check, 'nothing much ')
    text_to_check = remove_sentence_start(text_to_check, 'ok ')
    text_to_check = remove_sentence_start(text_to_check, 'okay ')
    text_to_check = remove_sentence_start(text_to_check, 'oh ')
    text_to_check = remove_sentence_start(text_to_check, 'omg ')
    text_to_check = remove_sentence_start(text_to_check, 'or ')
    text_to_check = remove_sentence_start(text_to_check, 'ow ')
    text_to_check = remove_sentence_start(text_to_check, '!question ')
    text_to_check = remove_sentence_start(text_to_check, 'question ')
    text_to_check = remove_sentence_start(text_to_check, 'so ')
    text_to_check = remove_sentence_start(text_to_check, 'sorry ')
    text_to_check = remove_sentence_start(text_to_check, 'sorry but ')
    text_to_check = remove_sentence_start(text_to_check, '!story ')
    text_to_check = remove_sentence_start(text_to_check, 'story ')
    text_to_check = remove_sentence_start(text_to_check, 'the ')
    text_to_check = remove_sentence_start(text_to_check, '!think ')
    text_to_check = remove_sentence_start(text_to_check, 'think ')
    text_to_check = remove_sentence_start(text_to_check, 'um ')
    text_to_check = remove_sentence_start(text_to_check, 'umm ')
    text_to_check = remove_sentence_start(text_to_check, 'wait ')
    text_to_check = remove_sentence_start(text_to_check, 'what does it mean ')
    text_to_check = remove_sentence_start(text_to_check, 'will you ')
    text_to_check = remove_sentence_start(text_to_check, 'wtf ')
    text_to_check = remove_sentence_start(text_to_check, 'wow ')
    text_to_check = remove_sentence_start(text_to_check, 'yes ')
   
    # Return the text
    return text_to_check.strip()


def remove_sentence_start(text_to_check, remove):
    # Check if the sentence starts with the string
    if text_to_check.startswith(remove):
        return text_to_check.replace(remove, '', 1)
    # Returnt the updated text
    return text_to_check


def remove_common_sentence_ends(text_to_check):
    # Make lowercase
    text_to_check = text_to_check.lower().strip()
    # Replace misspellings first
    text_to_check = replace_common_misspellings(text_to_check)
    # Replace common misspelled words
    text_to_check = remove_sentence_end(text_to_check, ' animal')
    text_to_check = remove_sentence_end(text_to_check, ' at all')
    text_to_check = remove_sentence_end(text_to_check, ' bot')
    text_to_check = remove_sentence_end(text_to_check, ' cat')
    text_to_check = remove_sentence_end(text_to_check, ' here')
    text_to_check = remove_sentence_end(text_to_check, ' hey')
    text_to_check = remove_sentence_end(text_to_check, ' i forget')
    text_to_check = remove_sentence_end(text_to_check, ' now')
    text_to_check = remove_sentence_end(text_to_check, ' or something')
    text_to_check = remove_sentence_end(text_to_check, ' right now')
    text_to_check = remove_sentence_end(text_to_check, ' so much')
    text_to_check = remove_sentence_end(text_to_check, ' tbh')
    text_to_check = remove_sentence_end(text_to_check, ' the most')
    text_to_check = remove_sentence_end(text_to_check, ' though')
    # Return the text
    return text_to_check.strip()


def remove_sentence_end(text_to_check, remove):
    # Check if the sentence starts with the string
    if text_to_check.endswith(remove):
        return reverse_replace(text_to_check, remove, '', 1)
    # Returnt the updated text
    return text_to_check


def reverse_replace(string_to_replace, replace_value, replace_with, occurrences=1):
    li = string_to_replace.rsplit(replace_value, occurrences)
    return replace_with.join(li)


def get_random_positive_adjective():
    # Get a random number
    rand = random.randint(1, 35)
    # Return the reference
    if rand == 1:
        return 'Awesome'
    elif rand == 2:
        return 'Wonderful'
    elif rand == 3:
        return 'Generous'
    elif rand == 4:
        return 'Amazing'
    elif rand == 5:
        return 'Kind'
    elif rand == 6:
        return 'Bright'
    elif rand == 7:
        return 'Cheerful'
    elif rand == 8:
        return 'Beautiful'
    elif rand == 9:
        return 'Lovely'
    elif rand == 10:
        return 'Brilliant'
    elif rand == 11:
        return 'Caring'
    elif rand == 12:
        return 'Charismatic'
    elif rand == 13:
        return 'Charming'
    elif rand == 14:
        return 'Delightful'
    elif rand == 15:
        return 'Excellent'
    elif rand == 16:
        return 'Extraordinary'
    elif rand == 17:
        return 'Fabulous'
    elif rand == 18:
        return 'Fantastic'
    elif rand == 19:
        return 'Friendly'
    elif rand == 20:
        return 'Fun'
    elif rand == 21:
        return 'Good'
    elif rand == 22:
        return 'Generous'
    elif rand == 23:
        return 'Joyous'
    elif rand == 24:
        return 'Noble'
    elif rand == 25:
        return 'Outstanding'
    elif rand == 26:
        return 'Remarkable'
    elif rand == 27:
        return 'Spectacular'
    elif rand == 28:
        return 'Splendid'
    elif rand == 29:
        return 'Super'
    else:
        return 'Great'


def get_random_negative_adjective():
    # Get a random number
    rand = random.randint(1, 22)
    # Return the reference
    if rand == 1:
        return 'Mediocre'
    elif rand == 2:
        return 'Limited'
    elif rand == 3:
        return 'Unimportant'
    elif rand == 4:
        return 'Unremarkable'
    elif rand == 5:
        return 'Weak'
    elif rand == 6:
        return 'Ignorant'
    elif rand == 7:
        return 'Menial'
    elif rand == 8:
        return 'Stupid'
    elif rand == 9:
        return 'Unintelligent'
    elif rand == 10:
        return 'Unskilled'
    elif rand == 11:
        return 'Inconsequential'
    elif rand == 12:
        return 'Irrelevant'
    elif rand == 13:
        return 'Nonessential'
    elif rand == 14:
        return 'Petty'
    elif rand == 15:
        return 'Unsubstantial'
    elif rand == 16:
        return 'Trivial'
    elif rand == 17:
        return 'Worthless'
    elif rand == 18:
        return 'Useless'
    elif rand == 19:
        return 'Inadequate'
    else:
        return 'Insignificant'


def get_random_positive_attractive():
    # Get a random number
    rand = random.randint(1, 9)
    # Return the reference
    if rand == 1:
        return 'Gorgeous'
    elif rand == 2:
        return 'Charming'
    elif rand == 3:
        return 'Good-looking'
    elif rand == 4:
        return 'Beautiful'
    elif rand == 5:
        return 'Cute'
    elif rand == 6:
        return 'Enchanting'
    elif rand == 7:
        return 'Pretty'
    elif rand == 8:
        return 'Stunning'
    else:
        return 'Adorable'


def get_random_negative_attractive():
    # Get a random number
    rand = random.randint(1, 21)
    # Return the reference
    if rand == 1:
        return 'Boring'
    elif rand == 2:
        return 'Dull'
    elif rand == 3:
        return 'Unattractive'
    elif rand == 4:
        return 'Disgusting'
    elif rand == 5:
        return 'Homely'
    elif rand == 6:
        return 'Repulsive'
    elif rand == 7:
        return 'Undesirable'
    elif rand == 8:
        return 'Repellent'
    elif rand == 9:
        return 'Unappealing'
    elif rand == 10:
        return 'Grotesque'
    elif rand == 11:
        return 'Hideous'
    elif rand == 12:
        return 'Unseemly'
    elif rand == 13:
        return 'Unsightly'
    elif rand == 14:
        return 'Appalling'
    elif rand == 15:
        return 'Foul'
    elif rand == 16:
        return 'Gross'
    elif rand == 17:
        return 'Plain'
    elif rand == 18:
        return 'Repugnant'
    else:
        return 'Ugly'


def remove_filler_words(text_to_replace):
    # Replace "ahahahahaha"
    text_to_replace = remove_filler_words(text_to_replace, 'aha', 'ha')
    # Replace "hahahahaha"
    text_to_replace = remove_filler_words(text_to_replace, 'haha', 'ha')
    # Replace "umm"
    text_to_replace = remove_filler_words(text_to_replace, 'umm', 'um')
    # Return the text
    return text_to_replace


def remove_repeating(text_to_replace, base_word_pre, repeating_word, base_word_post='', replace_with='', replace_base_word=True):
    # Keep track of the replacement word
    to_replace = base_word_pre 
    # Replace the base word
    if replace_base_word:
        text_to_replace = text_to_replace.replace(to_replace, replace_with)
    # Cycle through multiple iterations
    for n in range(1, 10):
        # Remove warning
        n = n
        # Add the repeating word
        to_replace = to_replace + repeating_word 
        # Replace the word
        text_to_replace = text_to_replace.replace(to_replace + base_word_post, replace_with)
    # Return the replaced text
    return text_to_replace


def get_random_int(lowest_num, highest_num):
    # Validate the lowest number
    try:
        lowest_num = int(lowest_num)
    except KeyboardInterrupt as ki:
        lowest_num = 1
        print_exception(ki, 'get_random_int: lowest_num')
    except Exception as e:
        lowest_num = 1
        print_exception(e, 'get_random_int: lowest_num')
    # Validate the highest number
    try:
        highest_num = int(highest_num)
    except KeyboardInterrupt as ki:
        highest_num = lowest_num
        print_exception(ki, 'get_random_int: highest_num')
    except Exception as e:
        highest_num = lowest_num
        print_exception(e, 'get_random_int: highest_num')
    # Validate the range
    if highest_num < lowest_num:
        # Swap the numbers
        temp_num = highest_num
        highest_num = lowest_num
        lowest_num = temp_num
    # Return the random number
    return random.randint(lowest_num, highest_num)


def generate_unique_id():
    # Set the initial unique id
    unique_id = strip_non_alphanumeric(str(datetime.now()), True, True)
    # Cycle several times
    for n in range(1, 20):
        n=n
        unique_id = unique_id + str(random.randint(1, 9))
    # Return the id
    return unique_id
