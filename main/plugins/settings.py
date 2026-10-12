"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import sys
import logging
from typing import Dict

try:
    import kurigram
except ImportError:
    import pyrogram as kurigram
    sys.modules["kurigram"] = kurigram

from kurigram import filters
from kurigram.types import Message, CallbackQuery

import config
from main.plugins.keyboard.inline import (
    settings_main_keyboard,
    api_keys_keyboard,
    provider_keyboard,
    temperature_keyboard,
    models_keyboard,
    prompt_keyboard,
    tokens_keyboard,
    cache_keyboard,
    cb_data
)
from main.services.cache_service import cache

logger = logging.getLogger("MistralBot.Settings")

PENDING_PROMPT_USERS: Dict[int, bool] = {}
PENDING_API_KEY_USERS: Dict[int, str] = {}

def get_settings_overview() -> str:
    stats = cache.stats
    v_mode = "Enabled 🎙️" if config.ai_settings.voice_mode else "Disabled 💬"
    return (
        "⚙️ <b>A.I. Control & Configuration Panel</b>\n\n"
        f"🤖 <b>A.I. Provider:</b> <code>{config.ai_settings.provider.upper()}</code>\n"
        f"🌸 <b>Mistral Model:</b> <code>{config.ai_settings.mistral_model}</code>\n"
        f"⚡ <b>Groq Model:</b> <code>{config.ai_settings.groq_model}</code>\n"
        f"🔑 <b>Mistral Key:</b> <code>{config.mask_key(config.MISTRAL_API_KEY)}</code>\n"
        f"🔑 <b>Groq Key:</b> <code>{config.mask_key(config.GROQ_API_KEY)}</code>\n"
        f"🎙️ <b>Voice Mode (TTS):</b> <code>{v_mode}</code>\n"
        f"🌡️ <b>Temperature:</b> <code>{config.ai_settings.temperature}</code>\n"
        f"🔢 <b>Max Tokens:</b> <code>{config.ai_settings.max_tokens}</code>\n"
        f"⚡ <b>Cache Status:</b> <code>{stats['cached_entries']} entries</code> (Hits: <code>{stats['hits']}</code>)\n\n"
        "<i>Select any parameter below to configure it:</i>"
    )

@kurigram.Client.on_message(filters.command(["setting", "settings"]))
async def settings_command_handler(client, message: Message):
    user_id = message.from_user.id if message.from_user else 0
    if not client.is_owner(user_id):
        await message.reply_text("⛔ <b>Access Denied:</b> This command is restricted to bot owners only.")
        return

    await message.reply_text(
        get_settings_overview(),
        reply_markup=settings_main_keyboard()
    )

@kurigram.Client.on_message(filters.command(["cancel"]) & filters.private)
async def cancel_handler(client, message: Message):
    user_id = message.from_user.id
    canceled = False
    if user_id in PENDING_PROMPT_USERS:
        del PENDING_PROMPT_USERS[user_id]
        canceled = True
    if user_id in PENDING_API_KEY_USERS:
        del PENDING_API_KEY_USERS[user_id]
        canceled = True

    if canceled:
        await message.reply_text("✅ Operation cancelled.", reply_markup=settings_main_keyboard())
    else:
        await message.reply_text("Nothing to cancel! ✨")

@kurigram.Client.on_callback_query(cb_data(r"^noop$"))
async def cb_noop(client, callback: CallbackQuery):
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^settings_main$"))
async def cb_settings_main(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    await callback.message.edit_text(
        get_settings_overview(),
        reply_markup=settings_main_keyboard()
    )
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^setting_apikeys_menu$"))
async def cb_apikeys_menu(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    text = (
        "🔑 <b>A.I. API Key Configuration</b>\n\n"
        f"🌸 <b>Mistral AI Key:</b> <code>{config.mask_key(config.MISTRAL_API_KEY)}</code>\n"
        f"⚡ <b>Groq AI Key:</b> <code>{config.mask_key(config.GROQ_API_KEY)}</code>\n\n"
        "Tap a button below to update either key on the fly:"
    )
    await callback.message.edit_text(text, reply_markup=api_keys_keyboard())
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^set_key_(mistral|groq)$"))
async def cb_set_key_prompt(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    target = callback.matches[0].group(1)
    PENDING_API_KEY_USERS[callback.from_user.id] = target
    provider_name = "Mistral AI" if target == "mistral" else "Groq AI"
    await callback.message.reply_text(
        f"🔑 <b>Send New {provider_name} API Key</b>\n\n"
        "Please send your new API key in your next message.\n"
        "<i>(Your message will be deleted immediately for privacy)</i>\n\n"
        "Send <code>/cancel</code> anytime to abort."
    )
    await callback.answer(f"Awaiting new {provider_name} key...")

@kurigram.Client.on_callback_query(cb_data(r"^setting_provider_menu$"))
async def cb_provider_menu(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    text = (
        "🤖 <b>Select Active A.I. Engine</b>\n\n"
        f"• <b>Current Setting:</b> <code>{config.ai_settings.provider.upper()}</code>\n\n"
        "• <b>Auto (Smart Failover):</b> Uses primary A.I. and automatically switches to the backup if any rate limit or error occurs.\n"
        "• <b>Mistral AI:</b> Primary Mistral AI integration.\n"
        "• <b>Groq AI:</b> Ultra-fast Groq LPU inference.\n\n"
        "Choose an option below:"
    )
    await callback.message.edit_text(text, reply_markup=provider_keyboard())
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^set_provider_(auto|mistral|groq)$"))
async def cb_set_provider(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    p = callback.matches[0].group(1)
    config.ai_settings.provider = p
    await callback.message.edit_reply_markup(reply_markup=provider_keyboard())
    await callback.answer(f"Provider set to {p.upper()}!")

@kurigram.Client.on_callback_query(cb_data(r"^setting_toggle_voice$"))
async def cb_toggle_voice(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    config.ai_settings.voice_mode = not config.ai_settings.voice_mode
    status = "Enabled 🎙️" if config.ai_settings.voice_mode else "Disabled 💬"
    await callback.answer(f"Voice Mode {status}!")
    await callback.message.edit_text(
        get_settings_overview(),
        reply_markup=settings_main_keyboard()
    )

@kurigram.Client.on_callback_query(cb_data(r"^setting_temp_menu$"))
async def cb_temperature_menu(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    text = (
        "🌡️ <b>A.I. Logic Ability / Temperature Scale</b>\n\n"
        f"• <b>Current Temperature:</b> <code>{config.ai_settings.temperature}</code>\n\n"
        "• <b>0.2 (Logical & Strict):</b> Factual, precise, less variation.\n"
        "• <b>0.5 (Balanced):</b> Good mix of logic and conversational warmth.\n"
        "• <b>0.7 (Flirty & Anime):</b> Charming, anime girl persona.\n"
        "• <b>1.0+ (Wild & Unpredictable):</b> Highest creativity and randomness.\n\n"
        "<i>Tap a preset or use +/- to fine-tune:</i>"
    )
    await callback.message.edit_text(
        text,
        reply_markup=temperature_keyboard(config.ai_settings.temperature)
    )
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^set_temp_(\d+(\.\d+)?)$"))
async def cb_set_temperature(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    val = float(callback.matches[0].group(1))
    config.ai_settings.temperature = round(val, 2)
    await callback.message.edit_reply_markup(
        reply_markup=temperature_keyboard(config.ai_settings.temperature)
    )
    await callback.answer(f"Temperature set to {config.ai_settings.temperature}!")

@kurigram.Client.on_callback_query(cb_data(r"^temp_adjust_(inc|dec)$"))
async def cb_adjust_temperature(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    action = callback.matches[0].group(1)
    current = config.ai_settings.temperature
    if action == "inc":
        new_val = min(1.5, current + 0.1)
    else:
        new_val = max(0.1, current - 0.1)
    config.ai_settings.temperature = round(new_val, 2)
    await callback.message.edit_reply_markup(
        reply_markup=temperature_keyboard(config.ai_settings.temperature)
    )
    await callback.answer(f"Temperature changed to {config.ai_settings.temperature}!")

@kurigram.Client.on_callback_query(cb_data(r"^setting_model_menu$"))
async def cb_models_menu(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    text = (
        "🧩 <b>Configure Models</b>\n\n"
        f"• <b>Mistral Model:</b> <code>{config.ai_settings.mistral_model}</code>\n"
        f"• <b>Groq Model:</b> <code>{config.ai_settings.groq_model}</code>\n\n"
        "Tap any free model to activate it for that provider:"
    )
    await callback.message.edit_text(text, reply_markup=models_keyboard())
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^set_model_m_(.+)$"))
async def cb_set_mistral_model(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    chosen = callback.matches[0].group(1)
    config.ai_settings.mistral_model = chosen
    await callback.message.edit_reply_markup(reply_markup=models_keyboard())
    await callback.answer(f"Mistral model set to {chosen}!")

@kurigram.Client.on_callback_query(cb_data(r"^set_model_g_(.+)$"))
async def cb_set_groq_model(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    chosen = callback.matches[0].group(1)
    config.ai_settings.groq_model = chosen
    await callback.message.edit_reply_markup(reply_markup=models_keyboard())
    await callback.answer(f"Groq model set to {chosen}!")

@kurigram.Client.on_callback_query(cb_data(r"^setting_prompt_menu$"))
async def cb_prompt_menu(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    prompt_snip = config.ai_settings.system_prompt[:180] + ("..." if len(config.ai_settings.system_prompt) > 180 else "")
    text = (
        "📝 <b>System Persona / Prompt Settings</b>\n\n"
        f"<b>Current Prompt Preview:</b>\n"
        f"<i>\"{prompt_snip}\"</i>\n\n"
        "Choose an action below:"
    )
    await callback.message.edit_text(
        text,
        reply_markup=prompt_keyboard()
    )
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^prompt_view_full$"))
async def cb_prompt_view_full(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    text = (
        "📝 <b>Current Full System Prompt:</b>\n\n"
        f"<code>{config.ai_settings.system_prompt}</code>"
    )
    await callback.message.edit_text(
        text,
        reply_markup=prompt_keyboard()
    )
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^prompt_reset_default$"))
async def cb_prompt_reset_default(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    config.ai_settings.reset_prompt()
    await callback.answer("Reset to flirty anime girl persona! 💖", show_alert=True)
    await cb_prompt_menu(client, callback)

@kurigram.Client.on_callback_query(cb_data(r"^prompt_set_custom$"))
async def cb_prompt_set_custom(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    PENDING_PROMPT_USERS[callback.from_user.id] = True
    await callback.message.reply_text(
        "✏️ <b>Enter New System Prompt:</b>\n\n"
        "Please send the new prompt in your next message.\n"
        "<i>(Remember: The AI must be asked to return JSON format <code>{\"reply\": \"...\"}</code>)</i>\n\n"
        "Send <code>/cancel</code> anytime to abort."
    )
    await callback.answer("Awaiting your new prompt message...")

@kurigram.Client.on_callback_query(cb_data(r"^setting_tokens_menu$"))
async def cb_tokens_menu(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    text = (
        "🔢 <b>Max Output Tokens</b>\n\n"
        f"• <b>Current Limit:</b> <code>{config.ai_settings.max_tokens} tokens</code>\n\n"
        "Limiting tokens reduces API usage and ensures quick responses."
    )
    await callback.message.edit_text(
        text,
        reply_markup=tokens_keyboard(config.ai_settings.max_tokens)
    )
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^set_tokens_(\d+)$"))
async def cb_set_tokens(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    t = int(callback.matches[0].group(1))
    config.ai_settings.max_tokens = t
    await callback.message.edit_reply_markup(
        reply_markup=tokens_keyboard(config.ai_settings.max_tokens)
    )
    await callback.answer(f"Max tokens set to {t}!")

@kurigram.Client.on_callback_query(cb_data(r"^setting_cache_menu$"))
async def cb_cache_menu(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    stats = cache.stats
    text = (
        "⚡ <b>Response Cache Metrics</b>\n\n"
        f"• <b>Cached User Prompts:</b> <code>{stats['cached_entries']}</code>\n"
        f"• <b>Cache Hits:</b> <code>{stats['hits']}</code>\n"
        f"• <b>Cache Misses:</b> <code>{stats['misses']}</code>\n"
        f"• <b>Total Lookups:</b> <code>{stats['total_queries']}</code>\n"
        f"• <b>Hit Ratio:</b> <code>{stats['hit_ratio_percent']}%</code>\n"
        f"• <b>TTL Expiry:</b> <code>{stats['ttl_minutes']} minutes</code>"
    )
    await callback.message.edit_text(
        text,
        reply_markup=cache_keyboard()
    )
    await callback.answer()

@kurigram.Client.on_callback_query(cb_data(r"^cache_flush$"))
async def cb_cache_flush(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    cache.clear()
    await callback.answer("Temporary cache flushed completely! 🗑️", show_alert=True)
    await cb_cache_menu(client, callback)

@kurigram.Client.on_callback_query(cb_data(r"^setting_reset_all$"))
async def cb_setting_reset_all(client, callback: CallbackQuery):
    if not client.is_owner(callback.from_user.id):
        return await callback.answer("Unauthorized.", show_alert=True)
    config.ai_settings.provider = "auto"
    config.ai_settings.temperature = 0.7
    config.ai_settings.mistral_model = "open-mistral-7b"
    config.ai_settings.groq_model = "llama-3.1-8b-instant"
    config.ai_settings.max_tokens = 180
    config.ai_settings.voice_mode = False
    config.ai_settings.reset_prompt()
    await callback.answer("All settings restored to defaults! 🔄", show_alert=True)
    await cb_settings_main(client, callback)
