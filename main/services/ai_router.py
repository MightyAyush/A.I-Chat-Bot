"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

from typing import Tuple, Optional
import config
from .mistral_service import mistral_service
from .groq_service import groq_service

class AIRouter:
    async def get_response(self, user_message: str) -> Tuple[Optional[str], Optional[str]]:
        provider = config.ai_settings.provider
        errors = []

        if provider == "groq":
            reply, err = await groq_service.generate_response(user_message)
            if reply:
                return reply, None
            if err:
                errors.append(err)
            reply, err2 = await mistral_service.generate_response(user_message)
            if reply:
                return reply, None
            if err2:
                errors.append(err2)

        elif provider == "mistral":
            reply, err = await mistral_service.generate_response(user_message)
            if reply:
                return reply, None
            if err:
                errors.append(err)
            reply, err2 = await groq_service.generate_response(user_message)
            if reply:
                return reply, None
            if err2:
                errors.append(err2)

        else:
            if config.MISTRAL_API_KEY:
                reply, err = await mistral_service.generate_response(user_message)
                if reply:
                    return reply, None
                if err:
                    errors.append(err)

            if config.GROQ_API_KEY:
                reply, err2 = await groq_service.generate_response(user_message)
                if reply:
                    return reply, None
                if err2:
                    errors.append(err2)

        return None, " | ".join(errors) if errors else "No AI service available"

ai_router = AIRouter()
