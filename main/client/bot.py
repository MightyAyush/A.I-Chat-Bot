import sys
import time
import logging

try:
    import kurigram
except ImportError:
    import pyrogram as kurigram
    sys.modules["kurigram"] = kurigram

from kurigram import Client, enums
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
            f"🚀 <b>Mistral Anime Bot Online</b>\n\n"
            f"🤖 <b>Bot:</b> @{self.me.username} (<code>{self.me.id}</code>)\n"
            f"🧠 <b>Model:</b> <code>{config.ai_settings.model}</code>\n"
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
            safe_text = text.replace(config.BOT_TOKEN, "[HIDDEN_TOKEN]").replace(config.MISTRAL_API_KEY, "[HIDDEN_KEY]")
            await self.send_message(
                chat_id=config.LOGGER_GROUP_ID,
                text=safe_text,
                disable_web_page_preview=True
            )
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
