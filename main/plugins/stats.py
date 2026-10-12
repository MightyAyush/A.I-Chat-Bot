"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import sys
import psutil
import logging

try:
    import kurigram
except ImportError:
    import pyrogram as kurigram
    sys.modules["kurigram"] = kurigram

from kurigram import filters
from kurigram.types import Message, CallbackQuery

import config
from main.services.token_tracker import token_tracker
from main.services.cache_service import cache
from main.plugins.keyboard.inline import close_keyboard, cb_data

logger = logging.getLogger("MistralBot.Stats")

def render_stats_text(client) -> str:
    vm = psutil.virtual_memory()
    ram_used = round(vm.used / (1024 ** 3), 2)
    ram_total = round(vm.total / (1024 ** 3), 2)
    ram_pct = vm.percent

    cpu_pct = psutil.cpu_percent(interval=0.1)
    cpu_cores_phys = psutil.cpu_count(logical=False) or 1
    cpu_cores_log = psutil.cpu_count(logical=True) or 1

    try:
        disk = psutil.disk_usage("/")
        disk_used = round(disk.used / (1024 ** 3), 2)
        disk_total = round(disk.total / (1024 ** 3), 2)
        disk_pct = disk.percent
        disk_str = f"{disk_used}GB / {disk_total}GB ({disk_pct}%)"
    except Exception:
        disk_str = "N/A"

    ai_stats = token_tracker.get_stats()
    m_info = ai_stats["mistral"]
    g_info = ai_stats["groq"]
    c_info = cache.stats

    text = (
        "📊 <b>System & A.I. Usage Statistics</b>\n\n"
        "👑 <b>Lead Architect:</b> Ayush (@MightyAyush)\n"
        "🖥️ <b>System Hardware:</b>\n"
        f"• <b>CPU Usage:</b> <code>{cpu_pct}%</code>\n"
        f"• <b>CPU Cores:</b> <code>{cpu_cores_phys} Core(s) / {cpu_cores_log} Threads</code>\n"
        f"• <b>RAM Usage:</b> <code>{ram_used}GB / {ram_total}GB ({ram_pct}%)</code>\n"
        f"• <b>Disk Usage:</b> <code>{disk_str}</code>\n"
        f"• <b>Uptime:</b> <code>{client.uptime}</code>\n\n"
        "🤖 <b>A.I. Engine Configuration:</b>\n"
        f"• <b>Active Provider:</b> <code>{config.ai_settings.provider.upper()}</code>\n"
        f"• <b>Mistral Model:</b> <code>{config.ai_settings.mistral_model}</code>\n"
        f"• <b>Groq Model:</b> <code>{config.ai_settings.groq_model}</code>\n"
        f"• <b>Voice Mode (TTS):</b> <code>{'Enabled' if config.ai_settings.voice_mode else 'Disabled'}</code>\n\n"
        "🌸 <b>Mistral AI Token Usage:</b>\n"
        f"• <b>Requests:</b> <code>{m_info['requests']}</code>\n"
        f"• <b>Prompt Tokens:</b> <code>{m_info['prompt_tokens']}</code>\n"
        f"• <b>Completion Tokens:</b> <code>{m_info['completion_tokens']}</code>\n"
        f"• <b>Total Tokens:</b> <code>{m_info['total_tokens']}</code>\n\n"
        "⚡ <b>Groq AI Token Usage:</b>\n"
        f"• <b>Requests:</b> <code>{g_info['requests']}</code>\n"
        f"• <b>Prompt Tokens:</b> <code>{g_info['prompt_tokens']}</code>\n"
        f"• <b>Completion Tokens:</b> <code>{g_info['completion_tokens']}</code>\n"
        f"• <b>Total Tokens:</b> <code>{g_info['total_tokens']}</code>\n\n"
        f"📈 <b>Combined Total Tokens:</b> <code>{ai_stats['total_tokens']}</code>\n"
        f"🎯 <b>Total AI Queries:</b> <code>{ai_stats['total_requests']}</code>\n\n"
        "⚡ <b>Cache Performance:</b>\n"
        f"• <b>Cached Items:</b> <code>{c_info['cached_entries']}</code>\n"
        f"• <b>Hits:</b> <code>{c_info['hits']}</code> | <b>Misses:</b> <code>{c_info['misses']}</code>\n"
        f"• <b>Hit Ratio:</b> <code>{c_info['hit_ratio_percent']}%</code>"
    )
    return text

@kurigram.Client.on_message(filters.command(["stats", "status"]))
async def stats_command_handler(client, message: Message):
    user_id = message.from_user.id if message.from_user else 0
    if not client.is_owner(user_id):
        await message.reply_text("⛔ <b>Access Denied:</b> This command is restricted to bot owners.")
        return

    text = render_stats_text(client)
    await message.reply_text(text, reply_markup=close_keyboard())

@kurigram.Client.on_callback_query(cb_data(r"^view_stats_callback$"))
async def cb_view_stats(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    text = render_stats_text(client)
    await callback.message.edit_text(text, reply_markup=close_keyboard())
    await callback.answer()
