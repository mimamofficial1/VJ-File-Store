# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01


import re
import os
from os import environ
from Script import script

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default
      
# Bot Information
API_ID = int(environ.get("API_ID", "23631217"))
API_HASH = environ.get("API_HASH", "567c6df308dc6901790309499f729d12")
BOT_TOKEN = environ.get("BOT_TOKEN", "")

PICS = (environ.get('PICS', 'https://graph.org/file/b40ec933c5cfe1c4f92d0-1c4eb4466dbd880cc5.jpg https://graph.org/file/afb26904467e6d288066d-e47db06938c1b2426d.jpg https://graph.org/file/93ab4f396b7e1702c0f1e-9240161b97e8d7ad9b.jpg https://graph.org/file/784c2dbbbcc0a5b8f8481-bedb60c5a57f254efc.jpg https://graph.org/file/6342f9ae8571659b764d2-adb46a36274462e7f5.jpg https://graph.org/file/58588618cd2547af98235-c024050c84364be078.jpg https://graph.org/file/413bdcc12fffa83f2e44f-d55d528ec54053892f.jpg https://graph.org/file/4bb4161b9b29ca7a9a68b-09129a323354e7ca94.jpg https://graph.org/file/afb26904467e6d288066d-e47db06938c1b2426d.jpg  https://graph.org/file/1c9861f4bff950b2ccb6b-4a686c9d9244369aeb.jpg')).split() # Bot Start Picture
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '6139759254').split()]
BOT_USERNAME = environ.get("BOT_USERNAME", "MRN_File_StoreBot") # without @
PORT = environ.get("PORT", "8080")

# Clone Info :-
CLONE_MODE = bool(environ.get('CLONE_MODE', True)) # Set True or False

# If Clone Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
CLONE_DB_URI = environ.get("CLONE_DB_URI", "mongodb+srv://mrnoffice692:PsO4VGHI9heKd7WA@cluster0.o1vcj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
CDB_NAME = environ.get("CDB_NAME", "clonetechvj")

# Database Information
DB_URI = environ.get("DB_URI", "mongodb+srv://mrnoffice692:PsO4VGHI9heKd7WA@cluster0.o1vcj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = environ.get("DB_NAME", "techvjbotz")

# Auto Delete Information
AUTO_DELETE_MODE = bool(environ.get('AUTO_DELETE_MODE', True)) # Set True or False

# If Auto Delete Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
AUTO_DELETE = int(environ.get("AUTO_DELETE", "15")) # Time in Minutes
AUTO_DELETE_TIME = int(environ.get("AUTO_DELETE_TIME", "900")) # Time in Seconds

# Channel Information
LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1002338165303"))

# auth_channel means force subscribe channel.
# if REQUEST_TO_JOIN_MODE is true then force subscribe work like request to join fsub, else if false then work like normal fsub.
REQUEST_TO_JOIN_MODE = bool(environ.get('REQUEST_TO_JOIN_MODE', True)) # Set True Or False
TRY_AGAIN_BTN = bool(environ.get('TRY_AGAIN_BTN', True)) # Set True Or False (This try again button is only for request to join fsub not for normal fsub)

# This Is Force Subscribe Channel, also known as Auth Channel 
auth_channel = environ.get('AUTH_CHANNEL', '-1002111679640') # give your force subscribe channel id here else leave it blank
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

# File Caption Information
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)

# Enable - True or Disable - False
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

# Verify Info :-
VERIFY_MODE = bool(environ.get('VERIFY_MODE', False)) # Set True or False

# If Verify Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
SHORTLINK_URL = environ.get("SHORTLINK_URL", "") # shortlink domain without https://
SHORTLINK_API = environ.get("SHORTLINK_API", "") # shortlink api
VERIFY_TUTORIAL = environ.get("VERIFY_TUTORIAL", "") # how to open link 

# Website Info:
WEBSITE_URL_MODE = bool(environ.get('WEBSITE_URL_MODE', True)) # Set True or False

# If Website Url Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
WEBSITE_URL = environ.get("WEBSITE_URL", "https://mrnfilesharing.blogspot.com/2025/01/redirecting-to-your-link-code-credit.html") # For More Information Check Video On Yt - @Tech_VJ

# File Stream Config
STREAM_MODE = bool(environ.get('STREAM_MODE', True)) # Set True or False

# If Stream Mode Is True Then Fill All Required Variable, If False Then Don't Fill.
MULTI_CLIENT = False
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
else:
    ON_HEROKU = False
URL = environ.get("URL", "https://equivalent-ann-marie-mrnmz-1ad684e3.koyeb.app/")


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
