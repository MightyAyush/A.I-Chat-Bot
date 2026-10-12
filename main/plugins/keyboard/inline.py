"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import sys
import re

try:
    import kurigram
except ImportError:
    import pyrogram as kurigram
    sys.modules["kurigram"] = kurigram

from kurigram import filters
from kurigram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

def cb_data(pattern):
    p = re.compile(pattern) if isinstance(pattern, str) else pattern

    async def func(flt, _, query):
        data = getattr(query, "data", None)
        if data:
            matches = list(flt.p.finditer(data))
            if matches:
                query.matches = matches
                return True
        return False

    return filters.create(func, "CallbackDataFilter", p=p)

def start_keyboard(is_owner: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("❓ Help & Commands", callback_data="help_menu"),
            InlineKeyboardButton("ℹ️ About Me", callback_data="about_menu")
        ],
        [
            InlineKeyboardButton("⚡ Bot Ping & Status", callback_data="ping_status"),
            InlineKeyboardButton("👑 Creator", url="https://t.me/MightyAyush")
        ]
    ]
    if is_owner:
        buttons.append([
            InlineKeyboardButton("⚙️ AI Configuration Menu", callback_data="settings_main")
        ])
    return InlineKeyboardMarkup(buttons)

def back_to_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Start", callback_data="start_menu")]
    ])

def settings_main_keyboard() -> InlineKeyboardMarkup:
    temp_display = f"{config.ai_settings.temperature}"
    voice_display = "ON 🎙️" if config.ai_settings.voice_mode else "OFF 💬"
    provider_display = config.ai_settings.provider.upper()
    
    buttons = [
        [
            InlineKeyboardButton(f"🤖 Engine: {provider_display}", callback_data="setting_provider_menu"),
            InlineKeyboardButton("🧩 Models", callback_data="setting_model_menu")
        ],
        [
            InlineKeyboardButton(f"🌡️ Temp: {temp_display}", callback_data="setting_temp_menu"),
            InlineKeyboardButton(f"🎙️ Voice: {voice_display}", callback_data="setting_toggle_voice")
        ],
        [
            InlineKeyboardButton("🔑 Manage API Keys", callback_data="setting_apikeys_menu"),
            InlineKeyboardButton("📝 Edit Prompt", callback_data="setting_prompt_menu")
        ],
        [
            InlineKeyboardButton(f"🔢 Tokens: {config.ai_settings.max_tokens}", callback_data="setting_tokens_menu"),
            InlineKeyboardButton("⚡ Cache Stats", callback_data="setting_cache_menu")
        ],
        [
            InlineKeyboardButton("📊 System & AI Stats", callback_data="view_stats_callback"),
            InlineKeyboardButton("🔄 Reset All", callback_data="setting_reset_all")
        ],
        [
            InlineKeyboardButton("❌ Close", callback_data="close_menu")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def api_keys_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("✏️ Set Mistral API Key", callback_data="set_key_mistral"),
            InlineKeyboardButton("✏️ Set Groq API Key", callback_data="set_key_groq")
        ],
        [
            InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_main")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def provider_keyboard() -> InlineKeyboardMarkup:
    curr = config.ai_settings.provider
    def mark(val, title):
        return f"✅ {title}" if curr == val else title

    buttons = [
        [
            InlineKeyboardButton(mark("auto", "Auto (Smart Failover)"), callback_data="set_provider_auto")
        ],
        [
            InlineKeyboardButton(mark("mistral", "Mistral AI"), callback_data="set_provider_mistral"),
            InlineKeyboardButton(mark("groq", "Groq AI"), callback_data="set_provider_groq")
        ],
        [
            InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_main")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def models_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    curr_mistral = config.ai_settings.mistral_model
    curr_groq = config.ai_settings.groq_model

    buttons.append([InlineKeyboardButton("--- Mistral Free Models ---", callback_data="noop")])
    for m in config.MISTRAL_MODELS:
        prefix = "✅ " if m == curr_mistral else "▫️ "
        buttons.append([InlineKeyboardButton(f"{prefix}{m}", callback_data=f"set_model_m_{m}")])

    buttons.append([InlineKeyboardButton("--- Groq Free Models ---", callback_data="noop")])
    for g in config.GROQ_MODELS:
        prefix = "✅ " if g == curr_groq else "▫️ "
        buttons.append([InlineKeyboardButton(f"{prefix}{g}", callback_data=f"set_model_g_{g}")])

    buttons.append([InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_main")])
    return InlineKeyboardMarkup(buttons)

def temperature_keyboard(current_temp: float) -> InlineKeyboardMarkup:
    def mark(val: float, text: str) -> str:
        return f"✅ {text}" if round(current_temp, 2) == round(val, 2) else text

    buttons = [
        [
            InlineKeyboardButton(mark(0.2, "0.2 (Strict)"), callback_data="set_temp_0.2"),
            InlineKeyboardButton(mark(0.5, "0.5 (Balanced)"), callback_data="set_temp_0.5")
        ],
        [
            InlineKeyboardButton(mark(0.7, "0.7 (Flirty/Anime)"), callback_data="set_temp_0.7"),
            InlineKeyboardButton(mark(1.0, "1.0 (Vibrant)"), callback_data="set_temp_1.0")
        ],
        [
            InlineKeyboardButton("➖ Decrease (-0.1)", callback_data="temp_adjust_dec"),
            InlineKeyboardButton("➕ Increase (+0.1)", callback_data="temp_adjust_inc")
        ],
        [
            InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_main")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def prompt_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("✏️ Set New Prompt", callback_data="prompt_set_custom"),
            InlineKeyboardButton("🔄 Reset Flirty Anime Girl", callback_data="prompt_reset_default")
        ],
        [
            InlineKeyboardButton("👀 View Full Prompt", callback_data="prompt_view_full")
        ],
        [
            InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_main")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def tokens_keyboard(current_tokens: int) -> InlineKeyboardMarkup:
    tokens = [100, 150, 200, 300, 500]
    row = []
    buttons = []
    for t in tokens:
        label = f"✅ {t}" if t == current_tokens else str(t)
        row.append(InlineKeyboardButton(label, callback_data=f"set_tokens_{t}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    buttons.append([
        InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_main")
    ])
    return InlineKeyboardMarkup(buttons)

def cache_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("🗑️ Clear Cache Now", callback_data="cache_flush"),
            InlineKeyboardButton("🔄 Refresh Stats", callback_data="setting_cache_menu")
        ],
        [
            InlineKeyboardButton("🔙 Back to Settings", callback_data="settings_main")
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def close_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Close", callback_data="close_menu")]
    ])
