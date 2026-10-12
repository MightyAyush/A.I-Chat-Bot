"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import re
import json
import logging
import aiohttp
from typing import Tuple, Optional

import config
from .token_tracker import token_tracker

logger = logging.getLogger("MistralBot.MistralService")

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
        sanitized = text
        if config.BOT_TOKEN:
            sanitized = sanitized.replace(config.BOT_TOKEN, "[REDACTED]")
        if config.MISTRAL_API_KEY:
            sanitized = sanitized.replace(config.MISTRAL_API_KEY, "[REDACTED]")
        if config.GROQ_API_KEY:
            sanitized = sanitized.replace(config.GROQ_API_KEY, "[REDACTED]")
        if config.API_HASH:
            sanitized = sanitized.replace(config.API_HASH, "[REDACTED]")
        return sanitized.strip()

    @staticmethod
    def sanitize_output(text: str) -> str:
        cleaned = text
        if config.BOT_TOKEN:
            cleaned = cleaned.replace(config.BOT_TOKEN, "[PROTECTED]")
        if config.MISTRAL_API_KEY:
            cleaned = cleaned.replace(config.MISTRAL_API_KEY, "[PROTECTED]")
        if config.GROQ_API_KEY:
            cleaned = cleaned.replace(config.GROQ_API_KEY, "[PROTECTED]")
        if config.API_HASH:
            cleaned = cleaned.replace(config.API_HASH, "[PROTECTED]")
        return cleaned.strip()

    async def generate_response(self, user_message: str) -> Tuple[Optional[str], Optional[str]]:
        if not config.MISTRAL_API_KEY:
            return None, "MISTRAL_AI key not configured"

        safe_user_text = self.sanitize_input(user_message)

        api_key = (config.MISTRAL_API_KEY or "").strip()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        system_prompt = config.ai_settings.system_prompt
        if "json" not in system_prompt.lower():
            system_prompt = f"{system_prompt}\n\nSTRICT REQUIREMENT: Respond strictly in valid JSON format: {{\"reply\": \"<your response>\"}}."

        payload = {
            "model": config.ai_settings.mistral_model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
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

                        usage = data.get("usage", {})
                        p_tok = usage.get("prompt_tokens", 0)
                        c_tok = usage.get("completion_tokens", 0)
                        t_tok = usage.get("total_tokens", 0)
                        token_tracker.record_mistral(p_tok, c_tok, t_tok)

                        content = data["choices"][0]["message"]["content"]
                        cleaned_content = re.sub(r"^```json\s*", "", content.strip(), flags=re.IGNORECASE)
                        cleaned_content = re.sub(r"^```\s*", "", cleaned_content.strip())
                        cleaned_content = re.sub(r"```$", "", cleaned_content.strip()).strip()

                        try:
                            parsed_json = json.loads(cleaned_content)
                            if isinstance(parsed_json, dict) and "reply" in parsed_json:
                                reply = str(parsed_json["reply"])
                            elif isinstance(parsed_json, dict) and len(parsed_json) > 0:
                                reply = str(next(iter(parsed_json.values())))
                            else:
                                reply = cleaned_content
                        except json.JSONDecodeError:
                            reply = cleaned_content

                        return self.sanitize_output(reply), None

                    except Exception as je:
                        logger.warning(f"Mistral parse warning: {je}")
                        return self.sanitize_output(content), None

                else:
                    err_info = f"Mistral HTTP {status}: {raw_text[:200]}"
                    logger.error(err_info)
                    return None, err_info

        except Exception as e:
            err_info = f"Mistral exception: {type(e).__name__}: {str(e)}"
            logger.error(err_info)
            return None, err_info

mistral_service = MistralService()
