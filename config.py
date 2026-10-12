"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import os
import json
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()

API_ID: int = int(os.getenv("API_ID") or 0)
API_HASH: str = os.getenv("API_HASH") or ""
BOT_TOKEN: str = os.getenv("MASTER_BOT_TOKEN") or ""
MISTRAL_API_KEY: str = os.getenv("MISTRAL_AI") or ""
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY") or ""

_raw_owners = os.getenv("OWNER_IDS", "[]")
try:
    if _raw_owners.startswith("["):
        OWNER_IDS: List[int] = [int(x) for x in json.loads(_raw_owners)]
    else:
        OWNER_IDS: List[int] = [int(x.strip()) for x in _raw_owners.split(",") if x.strip()]
except Exception:
    OWNER_IDS: List[int] = []

LOGGER_GROUP_ID: int = int(os.getenv("LOGGER_GROUP_ID") or 0)

PORT: int = int(os.getenv("PORT", "8080"))
HOST: str = os.getenv("HOST", "0.0.0.0")

CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "1800"))
CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "5000"))
MAX_INPUT_LENGTH: int = int(os.getenv("MAX_INPUT_LENGTH", "400"))

DEFAULT_SYSTEM_PROMPT: str = (
    "You are a charming, flirty anime girl chat companion. You are playful, witty, teasing, cute, and never cringe. "
    "Always respond in the EXACT same language that the user is talking in (for example: if the user talks in Hindi or Hinglish, reply in natural flirty Hinglish; if English, reply in English; if another language, match it). "
    "Keep responses concise, lively, and attractive with fitting emojis (😏, 💖, ✨, 🌸, ⁄(⁄ ⁄•⁄-⁄•⁄ ⁄)⁄). Never break character and never state that you are an AI, Mistral, or Groq. "
    "STRICT REQUIREMENT: You must respond ONLY with a valid JSON object in this exact schema: {\"reply\": \"<your response>\"}. "
    "Do NOT wrap it in markdown code blocks like ```json."
)

MISTRAL_MODELS = [
    "open-mistral-7b",
    "mistral-small-latest",
    "open-mixtral-8x7b"
]

GROQ_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "allam-2-7b"
]

@dataclass
class AISettings:
    provider: str = "auto"
    mistral_model: str = "open-mistral-7b"
    groq_model: str = "openai/gpt-oss-20b"
    temperature: float = 0.7
    max_tokens: int = 180
    voice_mode: bool = False
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    @property
    def model(self) -> str:
        if self.provider == "groq":
            return self.groq_model
        return self.mistral_model

    def reset_prompt(self):
        self.system_prompt = DEFAULT_SYSTEM_PROMPT

ai_settings = AISettings()

def mask_key(key: str) -> str:
    if not key or len(key) < 8:
        return "Not Configured"
    return f"{key[:6]}...{key[-4:]}"

def save_env_key(key_name: str, key_value: str):
    global MISTRAL_API_KEY, GROQ_API_KEY
    clean_val = key_value.strip()
    os.environ[key_name] = clean_val
    if key_name == "MISTRAL_AI":
        MISTRAL_API_KEY = clean_val
    elif key_name == "GROQ_API_KEY":
        GROQ_API_KEY = clean_val

    env_path = os.path.join(os.path.dirname(__file__), ".env")
    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    lines.append(f"{key_name}={key_value}\n")
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"{key_name}={key_value}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
