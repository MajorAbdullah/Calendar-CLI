# 🚀 Running the Smart Calendar Assistant

This guide will help you get the Calendar Assistant up and running quickly.

## 📋 Prerequisites

Before you begin, make sure you have:

- ✅ Python 3.8 or higher installed
- ✅ A Pipedream account with Google Calendar connected
- ✅ A Google API key for Gemini AI
- ✅ Git installed (for cloning)

## 🔧 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/MajorAbdullah/Calendar-CLI.git
cd Calendar-CLI
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `google-genai` - Google Gemini AI
- `fastmcp` - Model Context Protocol client
- `pipedream` - Pipedream API client
- `python-dotenv` - Environment variable management
- `streamlit` - Web UI framework
- `pytz` - Timezone handling

### Step 4: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your credentials
nano .env  # or use any text editor
```

Your `.env` file should contain:

```env
PIPEDREAM_PROJECT_ID=your_project_id
PIPEDREAM_ENVIRONMENT=production
PIPEDREAM_CLIENT_ID=your_client_id
PIPEDREAM_CLIENT_SECRET=your_client_secret
EXTERNAL_USER_ID=your_user_id
GOOGLE_API_KEY=your_gemini_api_key
```

### Step 5: Get Your Credentials

#### Pipedream Credentials:
1. Go to [Pipedream](https://pipedream.com)
2. Create a project and connect your Google Calendar
3. Go to Project Settings → API Credentials
4. Copy your Project ID, Client ID, and Client Secret

#### Google API Key:
1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click "Get API Key"
3. Create a new API key
4. Copy the key to your `.env` file

---

## ▶️ Running the Application

### Option 1: Web UI (Recommended) 🌐

```bash
streamlit run streamlit_app.py
```

This will:
- Start a local web server
- Open your browser at `http://localhost:8501`
- Show the Calendar Assistant UI

**Web UI Features:**

| Tab | What You Can Do |
|-----|-----------------|
| 💬 **AI Chatbot** | Chat naturally: "Schedule a meeting tomorrow at 3 PM" |
| 📝 **Schedule Meeting** | Visual form with timezone support for each attendee |
| 🌍 **Time Converter** | Convert times between 100+ cities worldwide |
| ⚙️ **Settings** | View timezone reference and UTC offsets |

### Option 2: Command Line Interface (CLI) 💻

```bash
python3 calendar_assistant.py
```

**CLI Commands:**
- "What's on my calendar today?"
- "Schedule a meeting tomorrow at 2 PM"
- "Show my schedule for this week"
- "Do I have any free time on Friday?"

Type `quit` or `exit` to close.

---

## 🌍 Using the Multi-Timezone Feature

### Scheduling a Meeting Across Timezones

1. Open the Web UI: `streamlit run streamlit_app.py`
2. Go to **📝 Schedule Meeting** tab
3. Enter meeting title
4. Select YOUR city (e.g., Karachi)
5. Pick date and time in YOUR timezone
6. Add friends - just select their city!
7. The app automatically shows their local time
8. Click **Create Meeting** - done! 🎉

### Example:
You're in **Karachi** scheduling a 4:00 PM meeting with:
- Friend in **London** → sees 11:00 AM
- Friend in **Madrid** → sees 12:00 PM
- Friend in **New York** → sees 6:00 AM

---

## 🔧 Troubleshooting

### "Connection Error"
- Check your internet connection
- Verify your `.env` credentials are correct
- Make sure Pipedream account has Google Calendar connected

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Permission denied"
```bash
chmod +x calendar_assistant.py
```

### Port 8501 in use
```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 🛑 Stopping the Application

- **Web UI**: Press `Ctrl+C` in the terminal
- **CLI**: Type `quit` or press `Ctrl+C`

---

## 📞 Need Help?

Open an issue on [GitHub](https://github.com/MajorAbdullah/Calendar-CLI/issues)

---

Happy Scheduling! 📅✨
