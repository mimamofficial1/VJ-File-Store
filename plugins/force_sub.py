# Force Subscribe helper functions

from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton
from plugins.settings_db import get_settings


async def not_joined_channels(client: Client, user_id: int):
    """Return the list of force-sub channels this user has NOT joined.
    Returns [] if force_sub is disabled or the user has joined everything."""
    settings = await get_settings()
    if not settings.get("force_sub"):
        return []
    channels = settings.get("force_sub_channels") or []
    missing = []
    for ch in channels:
        try:
            member = await client.get_chat_member(ch, user_id)
            if member.status in ("kicked", "left"):
                missing.append(ch)
        except UserNotParticipant:
            missing.append(ch)
        except Exception:
            # Bot not admin there / invalid channel -> don't lock everyone out
            continue
    return missing


async def force_sub_join_buttons(client: Client, channels):
    """Build one 'Join <channel>' button per row for the given channels."""
    buttons = []
    for ch in channels:
        try:
            chat = await client.get_chat(ch)
            link = chat.invite_link or (f"https://t.me/{chat.username}" if chat.username else None)
            if link:
                buttons.append([InlineKeyboardButton(f"🔔 Join {chat.title}", url=link)])
        except Exception:
            continue
    return buttons
