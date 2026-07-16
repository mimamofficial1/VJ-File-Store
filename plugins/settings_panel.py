# /settings admin panel — lets admins change bot behaviour from chat,
# without redeploying (values are stored in MongoDB via settings_db.py)

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMINS, CUSTOM_FILE_CAPTION
from Script import script
from plugins.settings_db import get_settings, update_setting, add_force_sub_channel, remove_force_sub_channel


def main_menu_markup():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Start Message", callback_data="adm_start")],
        [InlineKeyboardButton("📢 Force Subscribe", callback_data="adm_fsub")],
        [InlineKeyboardButton("🔒 Protect Content", callback_data="adm_protect")],
        [InlineKeyboardButton("♻️ Auto Delete", callback_data="adm_autodel")],
        [InlineKeyboardButton("🎬 Custom Caption", callback_data="adm_caption")],
        [InlineKeyboardButton("📊 Bot Status", callback_data="adm_status")],
        [InlineKeyboardButton("✖ Close", callback_data="adm_close")],
    ])


@Client.on_message(filters.command(["settings", "customize"]) & filters.user(ADMINS))
async def settings_cmd(client, message: Message):
    await message.reply_text(
        "<b>⚙️ BOT SETTINGS</b>\n\nChoose what you want to configure:",
        reply_markup=main_menu_markup()
    )


@Client.on_callback_query(filters.regex(r"^adm_"))
async def settings_cb(client: Client, query: CallbackQuery):
    if query.from_user.id not in ADMINS:
        return await query.answer("Admins only!", show_alert=True)

    data = query.data
    settings = await get_settings()

    # ---------------- Main menu ----------------
    if data == "adm_menu":
        await query.message.edit_text(
            "<b>⚙️ BOT SETTINGS</b>\n\nChoose what you want to configure:",
            reply_markup=main_menu_markup()
        )

    elif data == "adm_close":
        await query.message.delete()

    elif data == "adm_status":
        import time, psutil
        from plugins.dbusers import db
        from plugins.moderation import BOT_START_TIME, get_readable_time
        total_users = await db.total_users_count()
        total_banned = await db.total_banned_count()
        try:
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent
        except Exception:
            cpu = ram = 0
        uptime = get_readable_time(int(time.time() - BOT_START_TIME))
        text = (
            "<b>🤖 BOT STATUS</b>\n\n"
            f"👤 Users - <code>{total_users}</code>\n"
            f"🚫 Ban Users - <code>{total_banned}</code>\n"
            f"⚙️ CPU - <code>{cpu}%</code>\n"
            f"💾 RAM - <code>{ram}%</code>\n"
            f"⚡ Uptime - <code>{uptime}</code>"
        )
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("« Back", callback_data="adm_menu")]]
        ))

    # ---------------- Force Subscribe ----------------
    elif data == "adm_fsub":
        await render_fsub_menu(query, settings)

    elif data == "adm_fsub_toggle":
        new_state = not settings.get("force_sub", False)
        await update_setting("force_sub", new_state)
        settings["force_sub"] = new_state
        await render_fsub_menu(query, settings)

    elif data == "adm_fsub_add":
        prompt = await query.message.reply_text(
            "<b>Send the channel username (e.g. @Mrn_Officialx) or channel ID.</b>\n\n"
            "Make sure the bot is an <b>admin</b> in that channel.\n/cancel to cancel."
        )
        ans = await client.ask(query.message.chat.id, "")
        if ans.text and ans.text.strip() == "/cancel":
            await ans.reply_text("Cancelled.")
        elif ans.text:
            channel = ans.text.strip()
            try:
                chat = await client.get_chat(channel)
                member = await client.get_chat_member(chat.id, "me")
                if not member.privileges:
                    await ans.reply_text("<b>⚠️ I must be an admin in that channel first.</b>")
                else:
                    await add_force_sub_channel(chat.id)
                    await ans.reply_text(f"<b>✅ Added {chat.title} to Force Subscribe.</b>")
            except Exception as e:
                await ans.reply_text(f"<b>❌ Couldn't verify that channel.</b>\n<code>{e}</code>")
        settings = await get_settings()
        await render_fsub_menu(query, settings, edit=False)

    elif data == "adm_fsub_remove":
        channels = settings.get("force_sub_channels") or []
        if not channels:
            return await query.answer("No channels added yet.", show_alert=True)
        buttons = []
        for ch in channels:
            try:
                chat = await client.get_chat(ch)
                label = chat.title
            except Exception:
                label = str(ch)
            buttons.append([InlineKeyboardButton(f"❌ {label}", callback_data=f"adm_fsub_rm_{ch}")])
        buttons.append([InlineKeyboardButton("« Back", callback_data="adm_fsub")])
        await query.message.edit_text("<b>Tap a channel to remove it:</b>", reply_markup=InlineKeyboardMarkup(buttons))

    elif data.startswith("adm_fsub_rm_"):
        ch = data.replace("adm_fsub_rm_", "", 1)
        try:
            ch = int(ch)
        except ValueError:
            pass
        await remove_force_sub_channel(ch)
        settings = await get_settings()
        await render_fsub_menu(query, settings)

    elif data == "adm_fsub_msg":
        await query.message.reply_text("<b>Send the new Force Subscribe message text.</b>\n/cancel to cancel.")
        ans = await client.ask(query.message.chat.id, "")
        if ans.text and ans.text.strip() != "/cancel":
            await update_setting("force_sub_message", ans.text)
            await ans.reply_text("<b>✅ Force Subscribe message updated.</b>")
        settings = await get_settings()
        await render_fsub_menu(query, settings, edit=False)

    # ---------------- Protect Content ----------------
    elif data == "adm_protect":
        await render_protect_menu(query, settings)

    elif data in ("adm_protect_on", "adm_protect_off"):
        await update_setting("protect_content", data == "adm_protect_on")
        settings["protect_content"] = data == "adm_protect_on"
        await render_protect_menu(query, settings)

    # ---------------- Auto Delete ----------------
    elif data == "adm_autodel":
        await render_autodel_menu(query, settings)

    elif data == "adm_autodel_toggle":
        new_state = not settings.get("auto_delete", True)
        await update_setting("auto_delete", new_state)
        settings["auto_delete"] = new_state
        await render_autodel_menu(query, settings)

    elif data == "adm_autodel_time":
        await query.message.reply_text("<b>Send auto-delete time in minutes (e.g. 30).</b>\n/cancel to cancel.")
        ans = await client.ask(query.message.chat.id, "")
        if ans.text and ans.text.strip() != "/cancel":
            try:
                minutes = int(ans.text.strip())
                await update_setting("auto_delete_time", minutes * 60)
                await ans.reply_text(f"<b>✅ Auto delete time set to {minutes} minutes.</b>")
            except ValueError:
                await ans.reply_text("<b>❌ Please send a number.</b>")
        settings = await get_settings()
        await render_autodel_menu(query, settings, edit=False)

    # ---------------- Custom Caption ----------------
    elif data == "adm_caption":
        await render_caption_menu(query, settings)

    elif data == "adm_caption_edit":
        await query.message.reply_text(
            "<b>Send the new caption format.</b>\n\n"
            "Variables: <code>{file_name}</code> <code>{file_size}</code> <code>{file_caption}</code>\n/cancel to cancel."
        )
        ans = await client.ask(query.message.chat.id, "")
        if ans.text and ans.text.strip() != "/cancel":
            await update_setting("custom_caption", ans.text)
            await ans.reply_text("<b>✅ Custom caption updated.</b>")
        settings = await get_settings()
        await render_caption_menu(query, settings, edit=False)

    elif data == "adm_caption_show":
        current = settings.get("custom_caption") or CUSTOM_FILE_CAPTION
        await query.message.reply_text(f"<b>Current caption format:</b>\n\n<code>{current}</code>")
        await query.answer()

    elif data == "adm_caption_delete":
        await update_setting("custom_caption", None)
        settings["custom_caption"] = None
        await query.answer("Reset to default caption.", show_alert=True)
        await render_caption_menu(query, settings)

    # ---------------- Start Message ----------------
    elif data == "adm_start":
        await render_start_menu(query, settings)

    elif data == "adm_start_edit":
        await query.message.reply_text(
            "<b>Send the new start message text.</b>\n\n"
            "You can use <code>{}</code> <code>{}</code> as placeholders for user mention and bot mention (optional).\n/cancel to cancel."
        )
        ans = await client.ask(query.message.chat.id, "")
        if ans.text and ans.text.strip() != "/cancel":
            await update_setting("start_message", ans.text)
            await ans.reply_text("<b>✅ Start message updated.</b>")
        settings = await get_settings()
        await render_start_menu(query, settings, edit=False)

    elif data == "adm_start_reset":
        await update_setting("start_message", None)
        settings["start_message"] = None
        await query.answer("Reset to default start message.", show_alert=True)
        await render_start_menu(query, settings)


async def render_fsub_menu(query, settings, edit=True):
    state = "✅ ON" if settings.get("force_sub") else "❌ OFF"
    channels = settings.get("force_sub_channels") or []
    text = (
        "<b>📢 FORCE SUBSCRIBE</b>\n\n"
        "Users must join the added channel(s) before using the bot.\n\n"
        f"<b>Status:</b> {state}\n"
        f"<b>Channels added:</b> {len(channels)}"
    )
    buttons = [
        [InlineKeyboardButton("➕ Add Channel", callback_data="adm_fsub_add"),
         InlineKeyboardButton("➖ Remove Channel", callback_data="adm_fsub_remove")],
        [InlineKeyboardButton("Toggle ON/OFF", callback_data="adm_fsub_toggle")],
        [InlineKeyboardButton("✏️ Edit Message", callback_data="adm_fsub_msg")],
        [InlineKeyboardButton("« Back", callback_data="adm_menu")],
    ]
    markup = InlineKeyboardMarkup(buttons)
    if edit:
        await query.message.edit_text(text, reply_markup=markup)
    else:
        await query.message.reply_text(text, reply_markup=markup)


async def render_protect_menu(query, settings, edit=True):
    state = "✅ ENABLED" if settings.get("protect_content") else "❌ DISABLED"
    text = (
        "<b>🔒 PROTECT CONTENT</b>\n\n"
        "Restrict users from forwarding/saving files sent by this bot.\n\n"
        f"<b>Status:</b> {state}"
    )
    buttons = [
        [InlineKeyboardButton("✅ Enable", callback_data="adm_protect_on"),
         InlineKeyboardButton("❌ Disable", callback_data="adm_protect_off")],
        [InlineKeyboardButton("« Back", callback_data="adm_menu")],
    ]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))


async def render_autodel_menu(query, settings, edit=True):
    state = "✅ ON" if settings.get("auto_delete") else "❌ OFF"
    minutes = max(1, settings.get("auto_delete_time", 1800) // 60)
    text = (
        "<b>♻️ AUTO DELETE</b>\n\n"
        "Automatically deletes delivered files after a set time.\n\n"
        f"<b>Status:</b> {state}\n"
        f"<b>Delete Time:</b> {minutes} minutes"
    )
    buttons = [
        [InlineKeyboardButton("Toggle ON/OFF", callback_data="adm_autodel_toggle")],
        [InlineKeyboardButton("⏱ Set Time", callback_data="adm_autodel_time")],
        [InlineKeyboardButton("« Back", callback_data="adm_menu")],
    ]
    markup = InlineKeyboardMarkup(buttons)
    if edit:
        await query.message.edit_text(text, reply_markup=markup)
    else:
        await query.message.reply_text(text, reply_markup=markup)


async def render_caption_menu(query, settings, edit=True):
    text = "<b>🎬 CUSTOM CAPTION</b>\n\nSet the caption format used when files are delivered."
    buttons = [
        [InlineKeyboardButton("✏️ Edit Caption", callback_data="adm_caption_edit")],
        [InlineKeyboardButton("👁 Show Caption", callback_data="adm_caption_show"),
         InlineKeyboardButton("🗑 Reset", callback_data="adm_caption_delete")],
        [InlineKeyboardButton("« Back", callback_data="adm_menu")],
    ]
    markup = InlineKeyboardMarkup(buttons)
    if edit:
        await query.message.edit_text(text, reply_markup=markup)
    else:
        await query.message.reply_text(text, reply_markup=markup)


async def render_start_menu(query, settings, edit=True):
    text = "<b>📝 START MESSAGE</b>\n\nThis text is shown when a user sends /start."
    buttons = [
        [InlineKeyboardButton("✏️ Edit Start Text", callback_data="adm_start_edit")],
        [InlineKeyboardButton("🗑 Reset to Default", callback_data="adm_start_reset")],
        [InlineKeyboardButton("« Back", callback_data="adm_menu")],
    ]
    markup = InlineKeyboardMarkup(buttons)
    if edit:
        await query.message.edit_text(text, reply_markup=markup)
    else:
        await query.message.reply_text(text, reply_markup=markup)
