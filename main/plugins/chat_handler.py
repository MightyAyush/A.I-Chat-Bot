"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import sys
import logging
import asyncio

try:
    import kurigram
except ImportError:
    import pyrogram as kurigram
    sys.modules["kurigram"] = kurigram

from kurigram import filters, enums
from kurigram.types import Message

try:
    from kurigram.types import LinkPreviewOptions
    NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
except Exception:
    NO_PREVIEW = None

import config
from main.services.cache_service import cache
from main.services.ai_router import ai_router
from main.services.tts_service import tts_service
from main.plugins.settings import PENDING_PROMPT_USERS, PENDING_API_KEY_USERS

logger = logging.getLogger("MistralBot.ChatHandler")

HUMAN_ERROR_FALLBACK = (
    "Umm hey... my internet connection is acting really weird right now and disconnecting me (╥﹏╥). "
    "Can you wait a tiny bit? I will talk to you as soon as it's fixed, promise! 💕"
)

async def send_response(client, message: Message, text: str):
    if config.ai_settings.voice_mode:
        try:
            await client.send_chat_action(chat_id=message.chat.id, action=enums.ChatAction.RECORD_AUDIO)
            audio = await tts_service.generate_speech(text)
            if audio:
                caption = text if len(text) <= 1000 else f"{text[:997]}..."
                await message.reply_voice(voice=audio, caption=caption)
                return
        except Exception as ve:
            logger.warning(f"Voice dispatch failed: {ve}. Falling back to text.")

    try:
        if NO_PREVIEW:
            await message.reply_text(text, link_preview_options=NO_PREVIEW)
        else:
            await message.reply_text(text)
    except Exception as te:
        logger.error(f"Text dispatch failed: {te}")
        await client.send_message(chat_id=message.chat.id, text=text)

@kurigram.Client.on_message(filters.text & ~filters.command(["start", "help", "ping", "id", "setting", "settings", "stats", "status", "cancel"]))
async def ai_message_handler(client, message: Message):
    user_id = message.from_user.id if message.from_user else 0
    raw_text = (message.text or "").strip()

    if not raw_text:
        return

    if user_id in PENDING_API_KEY_USERS:
        target = PENDING_API_KEY_USERS[user_id]
        del PENDING_API_KEY_USERS[user_id]
        try:
            await message.delete()
        except Exception:
            pass

        key_env = "MISTRAL_AI" if target == "mistral" else "GROQ_API_KEY"
        config.save_env_key(key_env, raw_text)
        prov_name = "Mistral AI" if target == "mistral" else "Groq AI"
        masked = config.mask_key(raw_text)

        await message.reply_text(
            f"✅ <b>{prov_name} API Key Updated!</b>\n\n"
            f"🔑 <b>Active Key:</b> <code>{masked}</code>\n"
            "Key successfully configured and activated on the fly."
        )
        return

    if user_id in PENDING_PROMPT_USERS:
        del PENDING_PROMPT_USERS[user_id]
        config.ai_settings.system_prompt = raw_text
        try:
            if NO_PREVIEW:
                await message.reply_text(
                    "✅ <b>Custom System Prompt Updated!</b> 💖\n\n"
                    f"<i>\"{raw_text[:200]}...\"</i>",
                    link_preview_options=NO_PREVIEW
                )
            else:
                await message.reply_text(
                    "✅ <b>Custom System Prompt Updated!</b> 💖\n\n"
                    f"<i>\"{raw_text[:200]}...\"</i>"
                )
        except Exception:
            pass
        return

    is_private = message.chat.type == enums.ChatType.PRIVATE
    bot_id = client.me.id if client.me else 0
    bot_username = (client.me.username or "").lower() if client.me else ""

    is_reply_to_bot = bool(
        message.reply_to_message and
        message.reply_to_message.from_user and
        message.reply_to_message.from_user.id == bot_id
    )
    is_mentioned = bool(bot_username and f"@{bot_username}" in raw_text.lower())

    if not is_private and not is_reply_to_bot and not is_mentioned:
        return

    clean_text = raw_text
    if is_mentioned and bot_username:
        clean_text = raw_text.replace(f"@{bot_username}", "").replace(f"@{client.me.username}", "").strip()

    if not clean_text:
        await send_response(client, message, "Hey there handsome, what's on your mind? 😏💖")
        return

    if len(clean_text) > config.MAX_INPUT_LENGTH:
        warn_msg = (
            f"Aww darling, that's a bit too long for me to read all at once! 💕\n"
            f"Please keep messages under <b>{config.MAX_INPUT_LENGTH} characters</b> so we can chat smoothly 😏✨"
        )
        await send_response(client, message, warn_msg)
        return

    cached_reply = cache.get(clean_text)
    if cached_reply:
        try:
            await client.send_chat_action(chat_id=message.chat.id, action=enums.ChatAction.TYPING)
            await send_response(client, message, cached_reply)
        except Exception as e:
            logger.error(f"Cached response delivery error: {e}")
        return

    try:
        await client.send_chat_action(chat_id=message.chat.id, action=enums.ChatAction.TYPING)
    except Exception:
        pass

    try:
        ai_reply, error_info = await ai_router.get_response(clean_text)

        if ai_reply:
            cache.set(clean_text, ai_reply)
            await send_response(client, message, ai_reply)
        else:
            if error_info:
                log_payload = (
                    f"⚠️ <b>A.I. Router Failure Notice</b>\n"
                    f"👤 <b>User:</b> <code>{user_id}</code>\n"
                    f"👥 <b>Chat:</b> <code>{message.chat.id}</code>\n"
                    f"❓ <b>Query:</b> <code>{clean_text[:100]}</code>\n"
                    f"🚨 <b>Error:</b> <code>{error_info}</code>"
                )
                asyncio.create_task(client.send_log(log_payload))

            await send_response(client, message, HUMAN_ERROR_FALLBACK)

    except Exception as e:
        logger.error(f"Unexpected chat exception: {e}", exc_info=True)
        error_log = (
            f"❌ <b>Unhandled Chat Exception</b>\n"
            f"👤 <b>User:</b> <code>{user_id}</code>\n"
            f"👥 <b>Chat:</b> <code>{message.chat.id}</code>\n"
            f"🚨 <b>Details:</b> <code>{type(e).__name__}: {str(e)}</code>"
        )
        asyncio.create_task(client.send_log(error_log))
        await send_response(client, message, HUMAN_ERROR_FALLBACK)
