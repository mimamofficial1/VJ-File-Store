# Force Subscribe helper functions

from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton
from plugins.settings_db import get_settings, force_sub_channel_id


async def not_joined_channels(client: Client, user_id: int):
    """Return the list of force-sub channel ids this user has NOT joined.
    Returns [] if force_sub is disabled or the user has joined everything."""
    settings = await get_settings()
    if not settings.get("force_sub"):
        return []
    entries = settings.get("force_sub_channels") or []
    missing = []
    for entry in entries:
        ch = force_sub_channel_id(entry)
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


@Client.on_chat_join_request()
async def auto_approve_join_request(client: Client, update):
    """For channels added in 'Join Request Mode', auto-approve incoming join
    requests so the force-sub check passes right after the user requests."""
    settings = await get_settings()
    entries = settings.get("force_sub_channels") or []
    for entry in entries:
        if isinstance(entry, dict) and entry.get("mode") == "request" and force_sub_channel_id(entry) == update.chat.id:
            try:
                await client.approve_chat_join_request(update.chat.id, update.from_user.id)
            except Exception:
                pass
            break
