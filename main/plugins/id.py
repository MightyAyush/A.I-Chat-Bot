"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import sys
import logging

try:
    import kurigram
except ImportError:
    import pyrogram as kurigram
    sys.modules["kurigram"] = kurigram

from kurigram import filters
from kurigram.types import Message

try:
    from kurigram.types import LinkPreviewOptions
    NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
except Exception:
    NO_PREVIEW = None

logger = logging.getLogger("MistralBot.ID")

@kurigram.Client.on_message(filters.command(["id"]))
async def id_handler(client, message: Message):
    chat = message.chat
    user = message.from_user
    reply = message.reply_to_message

    text_parts = []

    if reply:
        if reply.from_user:
            rep_user = reply.from_user
            mention = f"<a href='tg://user?id={rep_user.id}'>{rep_user.first_name}</a>"
            text_parts.append(f"👤 <b>Replied User ID:</b> <code>{rep_user.id}</code>")
            text_parts.append(f"📌 <b>Replied User:</b> {mention}")
            if rep_user.username:
                text_parts.append(f"🔗 <b>Username:</b> @{rep_user.username}")
            if getattr(rep_user, "dc_id", None):
                text_parts.append(f"🌐 <b>Data Centre (DC):</b> <code>{rep_user.dc_id}</code>")
        elif reply.sender_chat:
            text_parts.append(f"📢 <b>Replied Channel/Chat ID:</b> <code>{reply.sender_chat.id}</code>")
            text_parts.append(f"📌 <b>Title:</b> {reply.sender_chat.title}")

        text_parts.append(f"💬 <b>Replied Message ID:</b> <code>{reply.id}</code>")

        if reply.forward_from:
            fwd_u = reply.forward_from
            text_parts.append(f"⏩ <b>Forwarded From User ID:</b> <code>{fwd_u.id}</code> ({fwd_u.first_name})")
        elif reply.forward_from_chat:
            fwd_c = reply.forward_from_chat
            text_parts.append(f"⏩ <b>Forwarded From Channel ID:</b> <code>{fwd_c.id}</code> ({fwd_c.title})")

        text_parts.append("")

    if user:
        user_mention = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
        text_parts.append(f"🆔 <b>Your User ID:</b> <code>{user.id}</code>")
        text_parts.append(f"👤 <b>Your Name:</b> {user_mention}")
        if user.username:
            text_parts.append(f"🔗 <b>Your Username:</b> @{user.username}")
    
    text_parts.append(f"👥 <b>Chat ID:</b> <code>{chat.id}</code>")
    if chat.title:
        text_parts.append(f"🏷️ <b>Chat Title:</b> {chat.title}")
    text_parts.append(f"📂 <b>Chat Type:</b> <code>{chat.type.name}</code>")
    text_parts.append(f"📩 <b>Current Message ID:</b> <code>{message.id}</code>")

    kwargs = {}
    if NO_PREVIEW:
        kwargs["link_preview_options"] = NO_PREVIEW

    await message.reply_text("\n".join(text_parts), **kwargs)
