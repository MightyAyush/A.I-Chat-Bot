"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import sys
import asyncio
import logging
import time
from aiohttp import web

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import kurigram
except ImportError:
    import pyrogram as kurigram
    sys.modules["kurigram"] = kurigram

from kurigram import idle

import config
from main.client.bot import Bot
from main.services.cache_service import cache
from main.services.mistral_service import mistral_service
from main.services.groq_service import groq_service
from main.services.token_tracker import token_tracker

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s - %(name)s] -> %(message)s",
    datefmt="%d-%b-%y %H:%M:%S"
)
logger = logging.getLogger("MistralBot.Main")

async def handle_root(request: web.Request) -> web.Response:
    stats = cache.stats
    bot_instance: Bot = request.app["bot"]
    data = {
        "status": "online",
        "service": "AI Anime Companion Bot",
        "dev": "Ayush (@MightyAyush)",
        "github": "https://github.com/MightyAyush",
        "bot_username": bot_instance.me.username if bot_instance.me else None,
        "uptime": bot_instance.uptime if bot_instance else "0s",
        "provider": config.ai_settings.provider.upper(),
        "mistral_model": config.ai_settings.mistral_model,
        "groq_model": config.ai_settings.groq_model,
        "voice_mode": config.ai_settings.voice_mode,
        "temperature": config.ai_settings.temperature,
        "tokens": token_tracker.get_stats(),
        "cache": stats
    }
    return web.json_response(data)

async def handle_health(request: web.Request) -> web.Response:
    return web.json_response({
        "status": "healthy",
        "timestamp": time.time()
    })

def make_web_app(bot: Bot) -> web.Application:
    app = web.Application()
    app["bot"] = bot
    app.router.add_get("/", handle_root)
    app.router.add_get("/health", handle_health)
    app.router.add_get("/ping", handle_health)
    return app

async def main():
    logger.info("Initializing Flirty Anime Chat Bot...")
    bot = Bot()

    web_app = make_web_app(bot)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, config.HOST, config.PORT)
    await site.start()
    logger.info(f"HTTP Server listening on http://{config.HOST}:{config.PORT}")

    await bot.start()
    logger.info(f"Bot connected to Telegram as @{bot.me.username}")

    try:
        await idle()
    finally:
        logger.info("Shutting down...")
        await bot.stop()
        await mistral_service.close()
        await groq_service.close()
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Stopped.")
