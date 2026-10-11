import re
import json
import logging
import aiohttp
import random
from typing import Tuple, Optional

import config

logger = logging.getLogger("MistralBot.MistralService")

FALLBACK_RESPONSES = [
    "Aww darling, *giggles* my thoughts got a little tangled for a second 💕 Ask me that again, okay? ✨",
    "Hehe, so many cuties are talking to me right now that I need a quick second to catch my breath! 🌸 Say that again, sweetie? 😏",
    "Oopsie! My mind drifted off thinking about you 💕 Say that once more, darling? 💖"
]

class MistralService:
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None

    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                resolver=aiohttp.ThreadedResolver(),
                limit=100,
                ttl_dns_cache=120
            )
            timeout = aiohttp.ClientTimeout(total=20, connect=5)
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            )
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    @staticmethod
    def sanitize_input(text: str) -> str:
        sanitized = text.replace(config.BOT_TOKEN, "[REDACTED]")
        sanitized = sanitized.replace(config.MISTRAL_API_KEY, "[REDACTED]")
        sanitized = sanitized.replace(config.API_HASH, "[REDACTED]")
        return sanitized.strip()

    @staticmethod
    def sanitize_output(text: str) -> str:
        cleaned = text.replace(config.BOT_TOKEN, "[PROTECTED]")
        cleaned = cleaned.replace(config.MISTRAL_API_KEY, "[PROTECTED]")
        cleaned = cleaned.replace(config.API_HASH, "[PROTECTED]")
        return cleaned.strip()

    async def generate_response(self, user_message: str) -> Tuple[str, Optional[str]]:
        safe_user_text = self.sanitize_input(user_message)

        headers = {
            "Authorization": f"Bearer {config.MISTRAL_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        payload = {
            "model": config.ai_settings.model,
            "messages": [
                {
                    "role": "system",
                    "content": config.ai_settings.system_prompt
                },
                {
                    "role": "user",
                    "content": safe_user_text
                }
            ],
            "response_format": {"type": "json_object"},
            "temperature": float(config.ai_settings.temperature),
            "max_tokens": int(config.ai_settings.max_tokens)
        }

        session = await self.get_session()
        try:
            async with session.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                status = response.status
                raw_text = await response.text()

                if status == 200:
                    try:
                        data = json.loads(raw_text)
                        content = data["choices"][0]["message"]["content"]
                        
                        cleaned_content = re.sub(r"^```json\s*", "", content.strip(), flags=re.IGNORECASE)
                        cleaned_content = re.sub(r"```$", "", cleaned_content.strip()).strip()

                        parsed_json = json.loads(cleaned_content)
                        if isinstance(parsed_json, dict) and "reply" in parsed_json:
                            reply = str(parsed_json["reply"])
                        elif isinstance(parsed_json, dict) and len(parsed_json) > 0:
                            reply = str(next(iter(parsed_json.values())))
                        else:
                            reply = cleaned_content

                        return self.sanitize_output(reply), None

                    except json.JSONDecodeError as je:
                        logger.warning(f"Mistral JSON decode warning: {je}")
                        return self.sanitize_output(content), f"JSON parse notice: {je}"

                else:
                    err_info = f"HTTP {status}: {raw_text[:250]}"
                    logger.error(f"Mistral API error: {err_info}")
                    return random.choice(FALLBACK_RESPONSES), err_info

        except Exception as e:
            err_info = f"Mistral exception: {type(e).__name__}: {str(e)}"
            logger.error(err_info)
            return random.choice(FALLBACK_RESPONSES), err_info

mistral_service = MistralService()
