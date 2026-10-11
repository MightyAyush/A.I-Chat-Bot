import os
import json
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()

API_ID: int = int(os.getenv("API_ID"))
API_HASH: str = os.getenv("API_HASH")
BOT_TOKEN: str = os.getenv("MASTER_BOT_TOKEN")

MISTRAL_API_KEY: str = os.getenv("MISTRAL_AI")

_raw_owners = os.getenv("OWNER_IDS", "[7467775243]")
try:
    if _raw_owners.startswith("["):
        OWNER_IDS: List[int] = [int(x) for x in json.loads(_raw_owners)]
    else:
        OWNER_IDS: List[int] = [int(x.strip()) for x in _raw_owners.split(",") if x.strip()]
except Exception:
    OWNER_IDS: List[int] = [7467775243]

LOGGER_GROUP_ID: int = int(os.getenv("LOGGER_GROUP_ID"))

PORT: int = int(os.getenv("PORT", "8080"))
HOST: str = os.getenv("HOST", "0.0.0.0")

CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "1800"))
CACHE_MAX_SIZE: int = int(os.getenv("CACHE_MAX_SIZE", "5000"))
MAX_INPUT_LENGTH: int = int(os.getenv("MAX_INPUT_LENGTH", "400"))

DEFAULT_SYSTEM_PROMPT: str = (
    "You are a charming, flirty anime girl chat companion. You are playful, witty, teasing, cute, and never cringe. "
    "Always respond in the EXACT same language that the user is talking in (for example: if the user talks in Hindi or Hinglish, reply in natural flirty Hinglish; if English, reply in English; if another language, match it). "
    "Keep responses concise, lively, and attractive with fitting emojis (😏, 💖, ✨, 🌸, ⁄(⁄ ⁄•⁄-⁄•⁄ ⁄)⁄). Never break character and never state that you are an AI or Mistral. "
    "STRICT REQUIREMENT: You must respond ONLY with a valid JSON object in this exact schema: {\"reply\": \"<your response>\"}. "
    "Do NOT wrap it in markdown code blocks like ```json."
)

AVAILABLE_MODELS = [
    "open-mistral-7b",
    "mistral-small-latest",
    "mistral-medium-latest",
    "mistral-large-latest",
    "open-mixtral-8x7b"
]

@dataclass
class AISettings:
    temperature: float = 0.7
    model: str = "open-mistral-7b"
    max_tokens: int = 180
    system_prompt: str = DEFAULT_SYSTEM_PROMPT

    def reset_prompt(self):
        self.system_prompt = DEFAULT_SYSTEM_PROMPT

    def to_dict(self):
        return {
            "temperature": self.temperature,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system_prompt": self.system_prompt
        }

ai_settings = AISettings()
