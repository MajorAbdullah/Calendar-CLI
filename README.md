# Smart Calendar Assistant

A powerful calendar management tool with both CLI and Web UI interfaces for managing Google Calendar with AI assistance powered by Google Gemini.

## Features

- 📅 View your calendar schedule (today, tomorrow, this week, etc.)
- ➕ Schedule new events with natural language
- 🔍 Find free time in your schedule
- ⚠️ Automatic conflict detection
- 🤖 AI-powered intelligent scheduling suggestions
- 🌍 **Multi-Timezone Meeting Scheduler** - Schedule meetings with friends across different timezones
- 👥 Send calendar invites to multiple participants
- 🌐 **Web UI** - Beautiful Streamlit interface for easy meeting creation

## Prerequisites

1. Python 3.8 or higher
2. Pipedream account with Google Calendar connected
3. Google API key for Gemini
4. Required environment variables

## Installation

1. Clone or navigate to this directory:
```bash
cd /Users/abdullah/my_projects/Calendar-CLI
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your credentials:
```bash
cp .env.example .env
```

## Configuration

Edit your `.env` file with your credentials:

```
PIPEDREAM_PROJECT_ID=your_project_id
PIPEDREAM_ENVIRONMENT=production
PIPEDREAM_CLIENT_ID=your_client_id
PIPEDREAM_CLIENT_SECRET=your_client_secret
EXTERNAL_USER_ID=your_user_id
GOOGLE_API_KEY=your_gemini_api_key
```

## Usage

### Option 1: Web UI (Recommended for Meeting Creation)

Run the Streamlit web interface:
```bash
streamlit run streamlit_app.py
```

This will open a web browser with an intuitive interface where you can:
- Create meetings with multiple attendees
- Specify different timezones for each participant
- See real-time timezone conversions
- Send calendar invites automatically
- Use the Quick Meeting feature for faster setup

**Web UI Features:**
- **Create Meeting Tab**: Detailed meeting setup with individual timezone selection
- **Quick Meeting Tab**: Fast bulk entry format (email, timezone per line)
- Live timezone preview showing meeting time for each attendee
- Automatic calendar invite generation and email delivery

### Option 2: CLI (For AI-Powered Scheduling)

Run the calendar assistant:
```bash
python3 calendar_assistant.py
## Project Structure

```
Calendar-CLI/
├── calendar_assistant.py   # CLI application
├── streamlit_app.py        # Web UI for meeting creation
├── requirements.txt        # Python dependencies
├── .env                    # Your configuration (not in git)
├── .env.example           # Example configuration template
└── README.md              # This file
```

## Multi-Timezone Meeting Example

Using the Web UI, you can easily schedule a meeting with friends across the globe:

**Scenario:** You're in Karachi and want to meet with:
- Friend in New York (US/Eastern)
- Friend in London (Europe/London)
- Friend in Tokyo (Asia/Tokyo)

**Steps:**
1. Open the Streamlit UI: `streamlit run streamlit_app.py`
2. Enter meeting title: "Global Team Sync"
3. Select your timezone: Asia/Karachi
4. Pick date and time in YOUR timezone
5. Add each friend with their email and timezone
6. Click "Create Meeting" - everyone gets an invite in their local time! 🎉

**Quick Meeting Format:**
```
john@example.com, US/Eastern
maria@example.com, Europe/London
akira@example.com, Asia/Tokyo
```xit:** Type `quit`, `exit`, or press `Ctrl+C`

## How It Works

1. **Authentication**: Connects to Pipedream for Google Calendar access
2. **AI Integration**: Uses Google Gemini for natural language processing
3. **MCP Protocol**: Leverages Model Context Protocol for tool calling
4. **Conflict Detection**: Automatically checks for scheduling conflicts
5. **Smart Scheduling**: Suggests optimal times based on your schedule

## Project Structure

```
Calendar-CLI/
├── calendar_assistant.py   # Main application
├── requirements.txt        # Python dependencies
├── .env                    # Your configuration (not in git)
├── .env.example           # Example configuration template
└── README.md              # This file
```

## Configuration

The calendar ID is automatically detected from your primary Google Calendar. The default timezone is set to Asia/Karachi (UTC+5). You can modify these in the code if needed.

## Error Handling

- Automatic retry logic for API overload
- Clear error messages for user guidance
- Graceful handling of network issues

## License

This is a standalone CLI tool for personal calendar management.
