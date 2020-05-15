# global_constants.py
# Contains constants for the program

# CONVERSION CONSTANTS
MILLI_TO_SECONDS = 1000
UTF8 = "utf-8"
#WINDOW_MID_X = 0
#WINDOW_MID_Y = 0
#WINDOW_WIDTH = 0
#WINDOW_HEIGHT = 0
PRINT_LINE_BREAK = '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
TWITCH_STARTUP_MESSAGE = 'twitch chat bot started'

# TEMPORARY VARIABLES
temp_uid = 'None'

# GLOBAL REFERENCE VARIABLES
full_alert_list = list([])
PROGRAM_PRINT_OUT = ''

# DISPLAY CONSTANTS
#WINDOW_TITLE = 'Social Manager Program Window'
#BG_DEFAULT_R = 100  # 0.392  # Default red color
#BG_DEFAULT_R2 = 0.3921516  # Default red color
#BG_DEFAULT_G = 0  # Default green color
#BG_DEFAULT_G2 = 0  # Default green color
#BG_DEFAULT_B = 150  # Default blue color
#BG_DEFAULT_B2 = 0.588235  # Default blue color
#BG_DEFAULT_COLOR = (BG_DEFAULT_R, BG_DEFAULT_G, BG_DEFAULT_B, 255)  # Default color
#BG_DEFAULT_COLOR2 = (BG_DEFAULT_R2, BG_DEFAULT_G2, BG_DEFAULT_B2, 1)  # Default color
#COLORS = {'black':(0,0,0,255), 
          #'white':(255,255,255,255),
          #'default':(BG_DEFAULT_R,BG_DEFAULT_G,BG_DEFAULT_B,255),  #640096
          #'purple':(100,0,150,255),
          #'twitch':(100,65,165,255),
          #'red':(255,0,0,255),
          #'green':(0,255,0,255),
          #'blue':(0,0,255,255),
          #'yellow':(255,255,0,255),
          #'alert-green':(0,255,0,255),
          #'alert-light-green':(153,204,51,255),
          #'alert-yellow':(255,204,0,255),
          #'alert-tan':(255,153,102,255),
          #'alert-orange':(204,51,0,255)}
#TEXT_COLOR = (255,255,255,255)
#TEXT_FONT = 'Garamond'
#TEXT_FONT_SIZE = 30
#ANIMATION_RANGE = 1000  # 1000 when active
#ANIMATION_PERCENTAGE = 10  # 10 when active
#SYSTEM_MESSAGE_DISPLAY_TIME = 10  # Seconds
#PRINT_OUT_FULL = False  # Print out full execution displays

# CHAT FILTER CONSTANTS
FILTER_LOCATION = ' filterb location filtere '
FILTER_NATIONALITY = ' filterb nationality filtere '
FILTER_NO_COMMENT_PERSON = ' filterb no comment person filtere '
FILTER_NO_COMMENT_TOPIC = ' filterb no comment topic filtere '
FILTER_SOCIAL_MEDIA = ' filterb social media filtere '
FILTER_GAME = ' filterb game filtere '

# USER CONSTANTS
TWITCH_USER_MAX_TIMEOUT_COUNT = 10  # Number of times a user can be timed out before ban
TWITCH_USER_EVENT_TRIGGER_VALUE = 50  # 1 in this many times likely to trigger an event with a chat message
TWITCH_USER_VALUE_TIMEOUT_COUNT_BAN = 'timeout_ban_count'
TWITCH_USER_VALUE_TIMEOUT_COUNT_NO_BAN = 'timeout_noban_count'
TWITCH_USER_VALUE_SUPPORT_COUNT = 'support_count'  # !support
TWITCH_USER_VALUE_TROLL_COUNT = 'troll_count'  # !troll
TWITCH_USER_VALUE_COMMENT_COUNT = 'comment_count'  # unassigned
TWITCH_USER_VALUE_PLAYER_TYPE = 'player_type'  # unassigned
TWITCH_USER_VALUE_IS_VIP = 'is_vip'  # True/False
TWITCH_USER_VALUE_FOLLOWER_TYPE_CURRENT = 'follower_type_current'
TWITCH_USER_VALUE_FOLLOWER_TYPE_HIGHEST = 'follower_type_highest'
TWITCH_USER_VALUE_EVENT_PREFERENCE = 'event_preference'
TWITCH_USER_VALUE_LAST_SPAWN = 'last_spawn'

# PROGRAM VALUE CONSTANTS
PROGRAM_VALUE_LAST_MERGE_DATE = 'last_merge_date'

# ANIMATION CONSTANTS
#IMAGES_FOLDER = 'images/'
#SPRITES_STANDARD_HEIGHT = 300  # The number of pixels in height a typical sprite image is
#SPRITES_STANDARD_WIDTH = 300  # The number of pixels in width a typical sprite image is
#SPRITES_Y_PAD_BOTTOM = 0
#SPRITES_Y_PAD_TOP = 0
#SPRITES_X_PAD_LEFT = 0
#SPRITES_X_PAD_RIGHT = 0
#ANONYMOUS = 'anonymous'
#TWITCH_PROGRAM_USER = 'Twitch'
#SCALE_DEFAULT = 0.2

# ALERT CONSTANTS
ALERT_DISPLAY_DEFAULT_LENGTH = 10  # Seconds
ALERT_REFERENCE_QUEUE_1 = 'alert_reference_queue_1'
ALERT_REFERENCE_QUEUE_2 = 'alert_reference_queue_2'

# FOLLOWER TYPE CONSTANTS
TWITCH_FOLLOWER_TYPE_NONE = 'lurker'  # Comments occassionally
TWITCH_FOLLOWER_TYPE_COMMENTER = 'commenter'  # Regular commenter
TWITCH_FOLLOWER_TYPE_FOLLOWER = 'follower'  # Follows channel
TWITCH_FOLLOWER_TYPE_SUB_DONATOR = 'donator'  # Donates to channel (bits/donation)
TWITCH_FOLLOWER_TYPE_SUB_TIER_1 = 'tier 1 sub'  # Subs to channel (tier 1)
TWITCH_FOLLOWER_TYPE_SUB_TIER_2 = 'tier 2 sub'  # Subs to channel (tier 2)
TWITCH_FOLLOWER_TYPE_SUB_TIER_3 = 'tier 3 sub'  # Subs to channel (tier 3)

# TWITCH CONSTANTS
#TWITCH_CONTROLLER_PASS = "oauth:insert auth code here"
TWITCH_CONTROLLER_HOST = "irc.chat.twitch.tv"
TWITCH_CONTROLLER_PORT = 6667
#TWITCH_CONTROLLER_NICK = "ChannelNicknameHere"
#TWITCH_CONTROLLER_CHAN = "ChannelNameHere"
TWITCH_CONTROLLER_RATE = "20/30"  # messages per second
TWITCH_CONTROLLER_MAX_IN_30 = 100  # max messages per 30 second period
TWITCH_CONTROLLER_GHOST_USERNAME = 'ghost_user_no_ref'
TWITCH_CONTROLLER_MAX_VIP = 10
TWITCH_CHAT_MODE_ALL_VIEWERS = 'all-viewers'
TWITCH_CHAT_MODE_SLOW = 'all-viewers-slow'
TWITCH_CHAT_MODE_EMOTES_ONLY = 'emotes-only'
TWITCH_CHAT_MODE_FOLLOWERS_ONLY = 'followers-only'
TWITCH_CHAT_MODE_SUBS_ONLY = 'subs-only'
TWITCH_CHAT_MODE_THRESHOLD = 10000  # Minimum 200
TWITCH_CHAT_MODE_THRESHOLD_SPLIT = 500  # Should be 5% of threshold
TWITCH_CHAT_MODE_CHANGE_FREQUENCY = 10  # Seconds

# MESSAGE VARIABLE
#TWITCH_UNPROCESSED_MESSAGES = list([])
#SYSTEM_MESSAGES_VISIBLE = False

# ALERT CONSTANTS
ALERT_TYPE_WS_BB = 'white-square-black-border'
ALERT_TYPE_WS_RB = 'white-square-red-border'
ALERT_TYPE_WS_GB = 'white-square-green-border'

# TRIGGER CONSTANTS
TRIGGER_CHECK_PERIOD = 2  # The number of seconds between trigger pulls
REF_BEG = '{'
REF_END = '}'
REF_VALUE_S = '['
REF_VALUE_E = ']'
REPLACE_FULL = REF_VALUE_S + '**REPLACE.THIS.STRING.WITH.VALUE.#**' + REF_VALUE_E

# DATABASE TRIGGERS
DB_REFERENCE = REF_BEG + 'db.'
DB_CHECK_CONN = DB_REFERENCE + 'check-db-connection' + REF_END
DB_CLEAN_USER_MESSAGES = DB_REFERENCE + 'clean-user-messages' + REF_END  # [username]
DB_CLEAN_USER_COMMANDS = DB_REFERENCE + 'clean-user-commands' + REF_END  # [username]

# SYSTEM MESSAGE TRIGGERS
SMS_REFERENCE = REF_BEG + 'system.'
SMS_MESSAGE_SYSTEM = SMS_REFERENCE + 'message' + REF_END # [message text]
SMS_MESSAGE_SYSTEM_VISIBLE = SMS_REFERENCE + 'message-visible' + REF_END # [is_visible]
SMS_MESSAGE_ALERT = SMS_REFERENCE + 'alert-message' + REF_END # [message text]

# TWITCH MESSAGE TRIGGERS
TMS_REFERENCE = REF_BEG + 'twitch-message.'
TMS_CONTROLLER_THRESHOLD = TMS_REFERENCE + 'twitch-chat-threshold' + REF_END # [threshold]
TMS_CONTROLLER_MESSAGE = TMS_REFERENCE + 'twitch-chat-message' + REF_END # [message]

# SETTINGS TRIGGERS
SE_REFERENCE = REF_BEG + 'setting.'
SE_BG_COLOR = SE_REFERENCE + 'background-color' + REF_END  # [R][G][B]