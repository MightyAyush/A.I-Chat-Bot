"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

import io
import re
import asyncio
from typing import Optional
from gtts import gTTS

class TTSService:
    @staticmethod
    def _clean_for_speech(text: str) -> str:
        cleaned = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        cleaned = re.sub(r"`.*?`", "", cleaned)
        cleaned = re.sub(r"\*+([^*]+)\*+", r"\1", cleaned)
        cleaned = re.sub(r"[^\w\s.,?!'\u0600-\u06FF\u0900-\u097F]", " ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned[:350]

    async def generate_speech(self, text: str) -> Optional[io.BytesIO]:
        clean = self._clean_for_speech(text)
        if not clean:
            return None

        def _synthesize():
            try:
                fp = io.BytesIO()
                tts = gTTS(text=clean, lang="en", tld="co.in", slow=False)
                tts.write_to_fp(fp)
                fp.seek(0)
                fp.name = "voice.ogg"
                return fp
            except Exception:
                return None

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _synthesize)

tts_service = TTSService()
