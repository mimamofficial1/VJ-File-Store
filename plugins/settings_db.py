# Dynamic bot settings stored in MongoDB so admins can change them
# from chat (via /settings) without redeploying the bot.

import motor.motor_asyncio
from config import DB_URI, DB_NAME

_client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
_db = _client[DB_NAME]
_col = _db.bot_settings

DEFAULTS = {
    "_id": "settings",
    "force_sub": False,
    "force_sub_channels": [],          # list of channel ids or @usernames
    "force_sub_message": "<b>👋 Please join our channel(s) below to use this bot, then tap 🔄 Try Again.</b>",
    "protect_content": False,
    "auto_delete": True,
    "auto_delete_time": 1800,          # seconds
    "custom_caption": None,            # None -> fall back to config.CUSTOM_FILE_CAPTION
    "start_message": None,             # None -> fall back to Script.script.START_TXT
}


async def get_settings():
    doc = await _col.find_one({"_id": "settings"})
    if not doc:
        doc = DEFAULTS.copy()
        await _col.insert_one(doc)
        return doc
    changed = False
    for k, v in DEFAULTS.items():
        if k not in doc:
            doc[k] = v
            changed = True
    if changed:
        await _col.update_one({"_id": "settings"}, {"$set": doc}, upsert=True)
    return doc


async def update_setting(key, value):
    await _col.update_one({"_id": "settings"}, {"$set": {key: value}}, upsert=True)


async def add_force_sub_channel(channel):
    await _col.update_one({"_id": "settings"}, {"$addToSet": {"force_sub_channels": channel}}, upsert=True)


async def remove_force_sub_channel(channel):
    await _col.update_one({"_id": "settings"}, {"$pull": {"force_sub_channels": channel}})
