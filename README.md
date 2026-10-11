# 🌸 Sweet Mistral AI Telegram Bot (Powered by Kurigram)

An ultra-fast, sweet-talking Telegram AI chatbot powered by **Mistral AI** and built on top of the high-performance **Kurigram** asynchronous framework. Features a 30-minute in-memory response cache to minimize token consumption, an interactive owner configuration panel, Rose-style ID inspection, strict JSON-based AI responses, and a built-in health endpoint for UptimeRobot.

---

## ✨ Features

1. **🌸 Sweet Chatting Girl Persona**:
   - Natural, affectionate, warm, and cheerful personality.
   - Enforces strict JSON responses (`{"reply": "..."}`) for bulletproof parsing.
   - Intelligent input length limitation to prevent excessive token burn.
   - Robust error shielding: Users never see API failures, timeouts, or stack traces.

2. **⚡ 30-Minute Temporary Response Cache**:
   - High-speed in-memory TTL cache (`{user_text: a.i_responsed}`).
   - Automatically expires after 30 minutes.
   - Instant response times (< 15ms) for repeated queries, dramatically cutting down API costs.

3. **⚙️ Real-Time `/setting` Dashboard (Bot Owners Only)**:
   - **Temperature / Logic Scale**: Adjust creativity vs. strictness (0.2, 0.5, 0.7, 1.0, or ±0.1).
   - **Model Selector**: Switch between `open-mistral-7b`, `mistral-small-latest`, `mistral-medium-latest`, etc.
   - **Dynamic System Prompt**: Change persona on the fly or reset to default.
   - **Max Token Limiter**: Optimize generation length.
   - **Cache Stats & Flush**: View real-time hit ratio and flush cache with one tap.

4. **🆔 Rose-Style `/id` Command**:
   - Reply to any message to view the sender's ID, username, DC, message ID, and forward origin.
   - Run in any chat to view your user ID, chat ID, and chat type.

5. **🌐 UptimeRobot / Health Endpoint**:
   - Built-in asynchronous HTTP server powered by `aiohttp`.
   - Exposes `GET /` and `GET /health` to keep your bot awake 24/7 on free hosts like Render.

6. **🛡️ Privacy & Security**:
   - Zero disclosure: Filters out bot tokens, API hashes, and secret keys from both user queries and AI outputs.
   - Detailed, safe error logging sent to `LOGGER_GROUP_ID`.

---

## 📁 Project Structure

```
A.I-Chat-Bot/
├── main/
│   ├── client/
│   │   ├── __init__.py
│   │   └── bot.py               # Kurigram Bot client class
│   ├── plugins/
│   │   ├── __init__.py
│   │   ├── start.py             # /start, /help, /ping and callback navigation
│   │   ├── id.py                # Rose-bot style /id command
│   │   ├── settings.py          # /setting interactive owner panel
│   │   ├── chat_handler.py      # AI conversation handler & cache integration
│   │   └── keyboard/
│   │       ├── __init__.py
│   │       └── inline.py        # All inline button keyboards
│   └── services/
│       ├── __init__.py
│       ├── cache_service.py     # 30-min TTL in-memory cache
│       └── mistral_service.py   # Mistral AI client with strict JSON parsing
├── config.py                    # Static & dynamic runtime configurations
├── main.py                      # Main entrypoint + aiohttp web server
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker container definition
├── docker-compose.yml           # Docker Compose setup
├── render.yaml                  # 1-Click Render.com blueprint
├── Procfile                     # Process file for cloud hosters
├── .env.example                 # Example environment variables
└── README.md                    # Project documentation
```

---

## 🚀 Quick Start (Local Run)

### 1. Prerequisites
- Python 3.10+
- Telegram `API_ID`, `API_HASH`, and `BOT_TOKEN`
- Mistral AI API Key

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your values:
```env
API_ID=32901283
API_HASH=4a330ad3bb00eb9fdc96d5641e28f83d
MASTER_BOT_TOKEN=7921523663:AAHpCzGY7UY-zdPfeSwI7VE0iuj0nDMyeQo
MISTRAL_AI=mstrl_T2Ks20Mjot1TTJgnHsmlLi9QzZl5EplB_2EYihO
OWNER_IDS=[7467775243]
LOGGER_GROUP_ID=-1004318545679
PORT=8080
HOST=0.0.0.0
```

### 4. Run the Bot
```bash
python main.py
```

---

## ☁️ Deploying on Render

1. Fork or push this repository to GitHub.
2. Sign in to [Render.com](https://render.com) and click **New +** -> **Web Service**.
3. Select your repository.
4. Set the following:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
5. Under **Advanced** -> **Environment Variables**, add the keys from your `.env`:
   - `API_ID`
   - `API_HASH`
   - `MASTER_BOT_TOKEN`
   - `MISTRAL_AI`
   - `OWNER_IDS`
   - `LOGGER_GROUP_ID`
   - `PORT` (set to `10000`)
6. Click **Create Web Service**.

### ⏰ Setting Up UptimeRobot (24/7 Keep-Alive)
1. In Render, copy your public service URL (e.g. `https://sweet-mistral-bot.onrender.com`).
2. Go to [UptimeRobot.com](https://uptimerobot.com).
3. Create a **New Monitor**:
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `Sweet Mistral Bot`
   - **URL (or IP)**: `https://your-service-name.onrender.com/health`
   - **Monitoring Interval**: Every `5 minutes`
4. Save the monitor. Your bot will now stay awake without sleeping!

---

## 🤖 Available Commands

| Command | Permission | Description |
|---|---|---|
| `/start` | Everyone | Displays the welcome message and inline navigation menu |
| `/help` | Everyone | Guide on chatting and commands |
| `/ping` | Everyone | Check bot latency, uptime, and cache statistics |
| `/id` | Everyone | Rose-bot style Telegram ID inspector (user, chat, replied message) |
| `/setting` | Owner Only | Opens the interactive AI logic/temperature & model configuration menu |
| `/cancel` | Owner Only | Cancels pending custom prompt update |
