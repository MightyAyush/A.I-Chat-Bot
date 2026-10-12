"""
══════════════════════════════════════════════════════════════════════════════
  MADE WITH LOVE BY AYUSH 
  GitHub: https://github.com/MightyAyush | Telegram: @MightyAyush
  Visionary Developer & Creator of High-Performance Asynchronous Projects (Including web, apps, bots and ML stuffs too)
══════════════════════════════════════════════════════════════════════════════
"""

class TokenTracker:
    def __init__(self):
        self.mistral_prompt = 0
        self.mistral_completion = 0
        self.mistral_total = 0
        self.mistral_requests = 0

        self.groq_prompt = 0
        self.groq_completion = 0
        self.groq_total = 0
        self.groq_requests = 0

    def record_mistral(self, prompt: int, completion: int, total: int):
        self.mistral_prompt += prompt
        self.mistral_completion += completion
        self.mistral_total += total if total > 0 else (prompt + completion)
        self.mistral_requests += 1

    def record_groq(self, prompt: int, completion: int, total: int):
        self.groq_prompt += prompt
        self.groq_completion += completion
        self.groq_total += total if total > 0 else (prompt + completion)
        self.groq_requests += 1

    def get_stats(self) -> dict:
        total_ai_tokens = self.mistral_total + self.groq_total
        total_ai_requests = self.mistral_requests + self.groq_requests
        return {
            "mistral": {
                "requests": self.mistral_requests,
                "prompt_tokens": self.mistral_prompt,
                "completion_tokens": self.mistral_completion,
                "total_tokens": self.mistral_total
            },
            "groq": {
                "requests": self.groq_requests,
                "prompt_tokens": self.groq_prompt,
                "completion_tokens": self.groq_completion,
                "total_tokens": self.groq_total
            },
            "total_tokens": total_ai_tokens,
            "total_requests": total_ai_requests
        }

token_tracker = TokenTracker()
