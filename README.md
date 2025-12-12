# Smart Calendar Assistant 📅

A powerful calendar management tool with both **CLI** and **Web UI** interfaces for managing Google Calendar with AI assistance powered by Google Gemini.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

### Core Features
- 📅 View your calendar schedule (today, tomorrow, this week, etc.)
- ➕ Schedule new events with natural language
- 🔍 Find free time in your schedule
- ⚠️ Automatic conflict detection
- 🤖 AI-powered intelligent scheduling suggestions

### Multi-Timezone Support
- 🌍 **100+ Cities Supported** - Just select a city, timezone auto-detected
- 🔢 **UTC Offset Selection** - Choose by UTC+5, UTC-8, etc.
- ⏰ **Automatic Time Conversion** - Set YOUR time, friends see THEIR local time
- 📧 **Smart Invitations** - Calendar invites sent with correct local times

### Web UI Features
- 💬 **AI Chatbot** - Schedule meetings using natural language
- 📝 **Visual Meeting Creator** - Easy form-based meeting setup
- 🌍 **World Time Converter** - See current time across the globe
- 👥 **Multi-Attendee Support** - Add up to 10 friends with different timezones

## 🚀 Quick Start

See [RUN.md](RUN.md) for detailed instructions.

```bash
# Clone the repository
git clone https://github.com/MajorAbdullah/Calendar-CLI.git
cd Calendar-CLI

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run Web UI
streamlit run streamlit_app.py

# Or run CLI
python3 calendar_assistant.py
```

## 📋 Prerequisites

1. **Python 3.8+**
2. **Pipedream Account** - For Google Calendar API access
3. **Google API Key** - For Gemini AI
4. **Google Calendar** - Connected via Pipedream

## 🔧 Configuration

Create a `.env` file with your credentials:

```env
PIPEDREAM_PROJECT_ID=your_project_id
PIPEDREAM_ENVIRONMENT=production
PIPEDREAM_CLIENT_ID=your_client_id
PIPEDREAM_CLIENT_SECRET=your_client_secret
EXTERNAL_USER_ID=your_user_id
GOOGLE_API_KEY=your_gemini_api_key
```

## 📱 Usage

### Web UI (Recommended)

```bash
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501` with:

| Tab | Description |
|-----|-------------|
| 💬 AI Chatbot | Natural language calendar commands |
| 📝 Schedule Meeting | Visual meeting creator with timezone support |
| 🌍 Time Converter | World clock and time conversion |
| ⚙️ Settings | Timezone reference guide |

### CLI Mode

```bash
python3 calendar_assistant.py
```

Example commands:
- "What's on my calendar today?"
- "Schedule a meeting tomorrow at 2 PM"
- "Do I have any free time on Friday?"

## 🌍 Timezone Examples

**When it's 12:00 PM in Spain (Madrid):**
- 🇬🇧 UK (London): 11:00 AM
- 🇵🇰 Pakistan (Karachi): 4:00 PM
- 🇮🇳 India (Mumbai): 4:30 PM
- 🇺🇸 New York: 6:00 AM

**Supported Cities Include:**
- 🇵🇰 Karachi, Lahore, Islamabad
- 🇬🇧 London, Manchester, Edinburgh
- 🇪🇸 Madrid, Barcelona, Valencia
- 🇮🇳 Mumbai, Delhi, Bangalore
- 🇦🇪 Dubai, Abu Dhabi
- 🇺🇸 New York, Los Angeles, Chicago
- 🇯🇵 Tokyo, Osaka
- 🇦🇺 Sydney, Melbourne
- And 80+ more cities!

## 📁 Project Structure

```
Calendar-CLI/
├── streamlit_app.py        # 🌐 Web UI application
├── calendar_assistant.py   # 💻 CLI application
├── requirements.txt        # 📦 Python dependencies
├── .env.example           # 🔧 Environment template
├── README.md              # 📖 This file
└── RUN.md                 # 🚀 Running instructions
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.5 Flash
- **Calendar API**: Google Calendar via Pipedream MCP
- **Timezone**: pytz
- **Backend**: Python 3.8+

## 📝 License

MIT License - feel free to use and modify!

## 👨‍💻 Author

**Abdullah** - [@MajorAbdullah](https://github.com/MajorAbdullah)

---

⭐ Star this repo if you find it useful!
