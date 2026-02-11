# Smart Calendar Assistant

**AI-powered Google Calendar management with CLI and Web UI interfaces**

Smart Calendar Assistant is a Python application that connects to Google Calendar through Pipedream MCP and uses Google Gemini AI to help you schedule meetings, check availability, and manage your calendar using natural language. It supports 100+ global cities with automatic timezone conversion for multi-participant scheduling.

---

## Features

### Core Capabilities
- View your calendar schedule for any timeframe (today, tomorrow, this week, custom dates)
- Schedule new events using natural language commands
- Find free time slots in your schedule automatically
- Automatic conflict detection that warns before double-booking
- AI-powered intelligent scheduling suggestions via Google Gemini

### Multi-Timezone Support
- Over 100 cities supported with automatic timezone detection
- UTC offset selection for manual timezone specification
- Automatic time conversion across attendee timezones
- Calendar invitations sent with correct local times for each participant

### Web UI (Streamlit)
- AI chatbot tab for natural language calendar commands
- Visual meeting creator with form-based event setup
- World time converter showing current time across the globe
- Multi-attendee support with up to 10 participants in different timezones
- Timezone reference guide with UTC offsets by region

### CLI Mode
- Interactive command-line interface for terminal-based calendar management
- Retry logic with exponential backoff for API resilience
- Same AI capabilities as the web interface

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Google Calendar](https://img.shields.io/badge/Google_Calendar-API-0F9D58?style=for-the-badge&logo=googlecalendar&logoColor=white)

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| AI Engine | Google Gemini 2.5 Flash |
| Calendar API | Google Calendar via Pipedream MCP |
| Timezone Handling | pytz |
| MCP Client | fastmcp |
| Environment | python-dotenv |

---

## Prerequisites

- **Python 3.8+**
- **Pipedream Account** -- for Google Calendar API access via MCP
- **Google API Key** -- for Gemini AI integration
- **Google Calendar** -- connected through Pipedream

---

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/MajorAbdullah/Calendar-CLI.git
cd Calendar-CLI

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

### Configuration

Edit the `.env` file with your credentials:

```env
PIPEDREAM_PROJECT_ID=your_project_id
PIPEDREAM_ENVIRONMENT=production
PIPEDREAM_CLIENT_ID=your_client_id
PIPEDREAM_CLIENT_SECRET=your_client_secret
EXTERNAL_USER_ID=your_user_id
GOOGLE_API_KEY=your_gemini_api_key
```

For Streamlit Cloud deployment, add the same variables to `.streamlit/secrets.toml` (see `.streamlit/secrets.example.toml` for the template).

---

## Usage

### Web UI (Recommended)

```bash
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501` with four tabs:

| Tab | Description |
|-----|-------------|
| AI Chatbot | Natural language calendar commands powered by Gemini |
| Schedule Meeting | Visual meeting creator with timezone support for up to 10 attendees |
| Time Converter | World clock and time conversion across major cities |
| Settings | Timezone reference guide organized by region |

### CLI Mode

```bash
python3 calendar_assistant.py
```

Example commands:
- "What's on my calendar today?"
- "Schedule a meeting tomorrow at 2 PM"
- "Do I have any free time on Friday?"
- "Schedule a dentist appointment at 4:30 PM today"

---

## Project Structure

```
Calendar-CLI/
├── streamlit_app.py          # Streamlit web UI application
├── calendar_assistant.py     # CLI application
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .streamlit/
│   ├── config.toml           # Streamlit configuration
│   └── secrets.example.toml  # Secrets template for cloud deployment
├── RUN.md                    # Detailed running instructions
└── README.md
```

---

## Timezone Examples

When scheduling a meeting at **12:00 PM in Madrid (Spain)**:

| City | Local Time |
|------|-----------|
| London, UK | 11:00 AM |
| Karachi, Pakistan | 4:00 PM |
| Mumbai, India | 4:30 PM |
| Dubai, UAE | 3:00 PM |
| New York, USA | 6:00 AM |
| Tokyo, Japan | 8:00 PM |

Supported regions include Pakistan, UK, Spain, France, Germany, India, UAE, Saudi Arabia, China, Japan, South Korea, Singapore, Australia, USA, Canada, Brazil, South Africa, Turkey, and many more.

---

## License

MIT License -- feel free to use and modify.

## Author

**Syed Abdullah Shah** -- [@MajorAbdullah](https://github.com/MajorAbdullah)
