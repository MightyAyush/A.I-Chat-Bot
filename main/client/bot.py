"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import sys
import time
import logging

try:
    import kurigram
except ImportError:
    import pyrogram as kurigram
    sys.modules["kurigram"] = kurigram

from kurigram import Client, enums

try:
    from kurigram.types import LinkPreviewOptions
    NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
except Exception:
    NO_PREVIEW = None

import config

logger = logging.getLogger("MistralBot.Client")

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="MistralSweetBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            plugins=dict(root="main/plugins"),
            workers=16,
            parse_mode=enums.ParseMode.HTML
        )
        self.start_time = time.time()
        self.me = None

    async def start(self):
        await super().start()
        self.me = await self.get_me()
        logger.info(f"Bot started as @{self.me.username} (ID: {self.me.id})")
        
        startup_msg = (
            f"🚀 <b>AI Anime Companion Online</b>\n\n"
            f"👑 <b>Creator:</b> Ayush (@MightyAyush)\n"
            f"🤖 <b>Bot:</b> @{self.me.username} (<code>{self.me.id}</code>)\n"
            f"⚙️ <b>Engine:</b> <code>{config.ai_settings.provider.upper()}</code>\n"
            f"🌸 <b>Mistral Model:</b> <code>{config.ai_settings.mistral_model}</code>\n"
            f"⚡ <b>Groq Model:</b> <code>{config.ai_settings.groq_model}</code>\n"
            f"🎙️ <b>Voice Mode:</b> <code>{'Enabled' if config.ai_settings.voice_mode else 'Disabled'}</code>\n"
            f"🌡️ <b>Temperature:</b> <code>{config.ai_settings.temperature}</code>\n"
            f"⏱️ <b>Cache TTL:</b> <code>{config.CACHE_TTL_SECONDS // 60} mins</code>\n"
            f"👑 <b>Owners:</b> <code>{config.OWNER_IDS}</code>"
        )
        await self.send_log(startup_msg)

    async def stop(self, *args):
        logger.info("Bot stopping...")
        await super().stop(*args)

    async def send_log(self, text: str):
        if not config.LOGGER_GROUP_ID:
            return
        try:
            safe_text = text
            if config.BOT_TOKEN:
                safe_text = safe_text.replace(config.BOT_TOKEN, "[HIDDEN_TOKEN]")
            if config.MISTRAL_API_KEY:
                safe_text = safe_text.replace(config.MISTRAL_API_KEY, "[HIDDEN_KEY]")
            if config.GROQ_API_KEY:
                safe_text = safe_text.replace(config.GROQ_API_KEY, "[HIDDEN_KEY]")

            kwargs = {
                "chat_id": config.LOGGER_GROUP_ID,
                "text": safe_text
            }
            if NO_PREVIEW:
                kwargs["link_preview_options"] = NO_PREVIEW

            await self.send_message(**kwargs)
        except Exception as e:
            logger.warning(f"Could not deliver log to LOGGER_GROUP_ID: {e}")

    @staticmethod
    def is_owner(user_id: int) -> bool:
        return user_id in config.OWNER_IDS

    @property
    def uptime(self) -> str:
        diff = int(time.time() - self.start_time)
        hours, remainder = divmod(diff, 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        return f"{hours}h {minutes}m {seconds}s"
