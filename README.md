# 🌸 Sweet Anime Companion A.I. Bot (Kurigram + Mistral + Groq)

A high-performance Telegram chatbot featuring dual AI support (Mistral AI & Groq LPU) with automatic smart failover, TTS voice messaging, 30-minute in-memory response cache, interactive settings panel, Rose-style ID tool, and real-time hardware/token metrics.

---

## ✨ Features

1. **🌸 Flirty Anime Companion**:
   - Responds in the exact language the user talks in (Hinglish, Hindi, English, etc.).
   - Strictly enforces JSON schemas for clean, reliable response parsing.
   - Intelligent input length limiter to safeguard token budgets.
   - Zero disclosure: Filters secrets and keys from user conversations and AI outputs.
   - Natural human error handling: If servers disconnect, the bot responds in a friendly, human-toned voice.

2. **⚡ Dual A.I. Engine (Mistral & Groq with Smart Failover)**:
   - Configurable between **Mistral AI**, **Groq AI**, or **Auto Failover**.
   - If the active AI hits rate limits or server issues, it automatically falls back to the other AI.

3. **🎙️ Natural Voice Message (TTS) Support**:
   - Can generate natural audio replies and send voice notes on Telegram.
   - Easily toggled on or off from the `/setting` panel.
   - Smooth fallback to normal text if audio synthesis fails.

4. **📊 Hardware & Token Usage `/stats`**:
   - Real-time CPU, RAM, Disk, and uptime statistics.
   - Per-engine token analytics (Mistral & Groq prompt, completion, and total tokens).
   - Real-time cache hit ratios.

5. **⚡ 30-Minute Temporary Response Cache**:
   - In-memory TTL cache to return repeated queries in <15ms without burning tokens.

6. **⚙️ Interactive `/setting` Panel (Owner Only)**:
   - Switch AI engines (Mistral / Groq / Auto).
   - Configure models for Mistral and Groq independently.
   - Adjust temperature and token limits.
   - Toggle Voice mode (TTS) on/off.
   - View, set custom, or reset prompts.
   - Flush response cache.

7. **🆔 Rose-Style `/id` Command**:
   - Look up user, chat, channel, forward origin, and message IDs.

8. **🌐 Built-in Keep-Alive HTTP Server**:
   - Runs an asynchronous health server on port `8080` (or `PORT` env var).
   - Endpoints `GET /` and `GET /health` for 24/7 uptime monitoring with UptimeRobot.

---

## 📁 Directory Structure

```
A.I-Chat-Bot/
├── main/
│   ├── client/
│   │   ├── __init__.py
│   │   └── bot.py               # Kurigram Bot client
│   ├── plugins/
│   │   ├── __init__.py
│   │   ├── start.py             # /start, /help, /ping
│   │   ├── id.py                # Rose-bot style /id command
│   │   ├── stats.py             # /stats system & token tracking
│   │   ├── settings.py          # /setting interactive owner panel
│   │   ├── chat_handler.py      # AI message router, TTS, cache
│   │   └── keyboard/
│   │       ├── __init__.py
│   │       └── inline.py        # All inline button keyboards
│   └── services/
│       ├── __init__.py
│       ├── cache_service.py     # 30-min TTL in-memory cache
│       ├── token_tracker.py     # Token usage metrics
│       ├── tts_service.py       # Voice message generation
│       ├── groq_service.py      # Groq AI client
│       ├── mistral_service.py   # Mistral AI client
│       └── ai_router.py         # Multi-AI failover router
├── config.py                    # Environment configurations
├── main.py                      # Main entrypoint + aiohttp server
├── requirements.txt             # Dependencies
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Docker Compose setup
├── render.yaml                  # Render.com blueprint
├── Procfile                     # Procfile for cloud hosters
├── .env.example                 # Example environment variables
└── README.md                    # Project documentation
```

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure `.env`
```env
API_ID=
API_HASH=
MASTER_BOT_TOKEN=
MISTRAL_AI=
GROQ_API_KEY=
OWNER_IDS=[]
LOGGER_GROUP_ID=
PORT=8080
HOST=0.0.0.0
```

### 3. Run the Bot
```bash
python main.py
```

---

## 🤖 Commands

| Command | Permission | Description |
|---|---|---|
| `/start` | Everyone | Welcome menu with interactive buttons |
| `/help` | Everyone | Guidance and command overview |
| `/ping` | Everyone | Network latency and uptime |
| `/id` | Everyone | Rose-style Telegram ID inspector |
| `/stats` | Owner Only | System hardware metrics & AI token consumption |
| `/setting` | Owner Only | AI provider, models, temperature, TTS voice, and prompt settings |
| `/cancel` | Owner Only | Cancel pending custom prompt input |
