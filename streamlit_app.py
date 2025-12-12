#!/usr/bin/env python3
"""
Smart Calendar Assistant - Streamlit UI
Timezone-aware meeting scheduler with multi-participant support and AI chatbot
"""

import os
import asyncio
import streamlit as st
from datetime import datetime, timedelta
import pytz
from google import genai
from fastmcp import Client
from pipedream import Pipedream
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Calendar Assistant",
    page_icon="📅",
    layout="wide"
)

# City to Timezone mapping (comprehensive)
CITY_TIMEZONES = {
    # Pakistan
    "Karachi": "Asia/Karachi",
    "Lahore": "Asia/Karachi",
    "Islamabad": "Asia/Karachi",
    "Peshawar": "Asia/Karachi",
    "Faisalabad": "Asia/Karachi",
    
    # UK
    "London": "Europe/London",
    "Manchester": "Europe/London",
    "Birmingham": "Europe/London",
    "Liverpool": "Europe/London",
    "Edinburgh": "Europe/London",
    "Glasgow": "Europe/London",
    
    # Spain
    "Madrid": "Europe/Madrid",
    "Barcelona": "Europe/Madrid",
    "Valencia": "Europe/Madrid",
    "Seville": "Europe/Madrid",
    "Bilbao": "Europe/Madrid",
    
    # France
    "Paris": "Europe/Paris",
    "Lyon": "Europe/Paris",
    "Marseille": "Europe/Paris",
    
    # Germany
    "Berlin": "Europe/Berlin",
    "Munich": "Europe/Berlin",
    "Frankfurt": "Europe/Berlin",
    "Hamburg": "Europe/Berlin",
    
    # Italy
    "Rome": "Europe/Rome",
    "Milan": "Europe/Rome",
    "Naples": "Europe/Rome",
    
    # Netherlands
    "Amsterdam": "Europe/Amsterdam",
    "Rotterdam": "Europe/Amsterdam",
    
    # India
    "Mumbai": "Asia/Kolkata",
    "Delhi": "Asia/Kolkata",
    "Bangalore": "Asia/Kolkata",
    "Chennai": "Asia/Kolkata",
    "Hyderabad": "Asia/Kolkata",
    "Kolkata": "Asia/Kolkata",
    "Pune": "Asia/Kolkata",
    
    # UAE
    "Dubai": "Asia/Dubai",
    "Abu Dhabi": "Asia/Dubai",
    
    # Saudi Arabia
    "Riyadh": "Asia/Riyadh",
    "Jeddah": "Asia/Riyadh",
    "Mecca": "Asia/Riyadh",
    
    # China
    "Beijing": "Asia/Shanghai",
    "Shanghai": "Asia/Shanghai",
    "Shenzhen": "Asia/Shanghai",
    "Guangzhou": "Asia/Shanghai",
    "Hong Kong": "Asia/Hong_Kong",
    
    # Japan
    "Tokyo": "Asia/Tokyo",
    "Osaka": "Asia/Tokyo",
    "Kyoto": "Asia/Tokyo",
    
    # South Korea
    "Seoul": "Asia/Seoul",
    "Busan": "Asia/Seoul",
    
    # Singapore
    "Singapore": "Asia/Singapore",
    
    # Malaysia
    "Kuala Lumpur": "Asia/Kuala_Lumpur",
    
    # Thailand
    "Bangkok": "Asia/Bangkok",
    
    # Indonesia
    "Jakarta": "Asia/Jakarta",
    "Bali": "Asia/Makassar",
    
    # Philippines
    "Manila": "Asia/Manila",
    
    # Vietnam
    "Ho Chi Minh City": "Asia/Ho_Chi_Minh",
    "Hanoi": "Asia/Ho_Chi_Minh",
    
    # Australia
    "Sydney": "Australia/Sydney",
    "Melbourne": "Australia/Melbourne",
    "Brisbane": "Australia/Brisbane",
    "Perth": "Australia/Perth",
    "Adelaide": "Australia/Adelaide",
    
    # New Zealand
    "Auckland": "Pacific/Auckland",
    "Wellington": "Pacific/Auckland",
    
    # USA - East
    "New York": "America/New_York",
    "Boston": "America/New_York",
    "Philadelphia": "America/New_York",
    "Washington DC": "America/New_York",
    "Miami": "America/New_York",
    "Atlanta": "America/New_York",
    
    # USA - Central
    "Chicago": "America/Chicago",
    "Houston": "America/Chicago",
    "Dallas": "America/Chicago",
    "Austin": "America/Chicago",
    
    # USA - Mountain
    "Denver": "America/Denver",
    "Phoenix": "America/Phoenix",
    
    # USA - Pacific
    "Los Angeles": "America/Los_Angeles",
    "San Francisco": "America/Los_Angeles",
    "Seattle": "America/Los_Angeles",
    "San Diego": "America/Los_Angeles",
    "Las Vegas": "America/Los_Angeles",
    
    # Canada
    "Toronto": "America/Toronto",
    "Vancouver": "America/Vancouver",
    "Montreal": "America/Montreal",
    "Calgary": "America/Edmonton",
    
    # Mexico
    "Mexico City": "America/Mexico_City",
    
    # Brazil
    "Sao Paulo": "America/Sao_Paulo",
    "Rio de Janeiro": "America/Sao_Paulo",
    
    # Argentina
    "Buenos Aires": "America/Argentina/Buenos_Aires",
    
    # South Africa
    "Johannesburg": "Africa/Johannesburg",
    "Cape Town": "Africa/Johannesburg",
    
    # Nigeria
    "Lagos": "Africa/Lagos",
    
    # Egypt
    "Cairo": "Africa/Cairo",
    
    # Kenya
    "Nairobi": "Africa/Nairobi",
    
    # Turkey
    "Istanbul": "Europe/Istanbul",
    "Ankara": "Europe/Istanbul",
    
    # Russia
    "Moscow": "Europe/Moscow",
    "St Petersburg": "Europe/Moscow",
    
    # Poland
    "Warsaw": "Europe/Warsaw",
    
    # Sweden
    "Stockholm": "Europe/Stockholm",
    
    # Norway
    "Oslo": "Europe/Oslo",
    
    # Denmark
    "Copenhagen": "Europe/Copenhagen",
    
    # Finland
    "Helsinki": "Europe/Helsinki",
    
    # Ireland
    "Dublin": "Europe/Dublin",
    
    # Portugal
    "Lisbon": "Europe/Lisbon",
    
    # Greece
    "Athens": "Europe/Athens",
    
    # Belgium
    "Brussels": "Europe/Brussels",
    
    # Switzerland
    "Zurich": "Europe/Zurich",
    "Geneva": "Europe/Zurich",
    
    # Austria
    "Vienna": "Europe/Vienna",
    
    # Czech Republic
    "Prague": "Europe/Prague",
    
    # Hungary
    "Budapest": "Europe/Budapest",
    
    # Romania
    "Bucharest": "Europe/Bucharest",
    
    # Ukraine
    "Kyiv": "Europe/Kiev",
    
    # Israel
    "Tel Aviv": "Asia/Jerusalem",
    "Jerusalem": "Asia/Jerusalem",
    
    # Qatar
    "Doha": "Asia/Qatar",
    
    # Kuwait
    "Kuwait City": "Asia/Kuwait",
    
    # Bangladesh
    "Dhaka": "Asia/Dhaka",
    
    # Sri Lanka
    "Colombo": "Asia/Colombo",
    
    # Nepal
    "Kathmandu": "Asia/Kathmandu",
    
    # Afghanistan
    "Kabul": "Asia/Kabul",
    
    # Iran
    "Tehran": "Asia/Tehran",
    
    # Iraq
    "Baghdad": "Asia/Baghdad",
}

# Get sorted city list
CITIES = sorted(CITY_TIMEZONES.keys())

# UTC Offset options
UTC_OFFSETS = {
    "UTC-12:00": -12,
    "UTC-11:00": -11,
    "UTC-10:00 (Hawaii)": -10,
    "UTC-09:00 (Alaska)": -9,
    "UTC-08:00 (US Pacific)": -8,
    "UTC-07:00 (US Mountain)": -7,
    "UTC-06:00 (US Central)": -6,
    "UTC-05:00 (US Eastern)": -5,
    "UTC-04:00": -4,
    "UTC-03:00 (Brazil)": -3,
    "UTC-02:00": -2,
    "UTC-01:00": -1,
    "UTC+00:00 (UK)": 0,
    "UTC+01:00 (Spain/France)": 1,
    "UTC+02:00 (Eastern Europe)": 2,
    "UTC+03:00 (Moscow/Saudi)": 3,
    "UTC+04:00 (Dubai)": 4,
    "UTC+04:30 (Afghanistan)": 4.5,
    "UTC+05:00 (Pakistan)": 5,
    "UTC+05:30 (India)": 5.5,
    "UTC+05:45 (Nepal)": 5.75,
    "UTC+06:00 (Bangladesh)": 6,
    "UTC+06:30 (Myanmar)": 6.5,
    "UTC+07:00 (Thailand)": 7,
    "UTC+08:00 (China/Singapore)": 8,
    "UTC+09:00 (Japan/Korea)": 9,
    "UTC+09:30 (Australia Central)": 9.5,
    "UTC+10:00 (Australia East)": 10,
    "UTC+11:00": 11,
    "UTC+12:00 (New Zealand)": 12,
    "UTC+13:00": 13,
}


class CalendarUI:
    def __init__(self):
        self.pd_client = None
        self.access_token = None
        self.mcp_client = None
        self.gemini_client = None
        self.calendar_id = None
        
    async def initialize(self):
        """Initialize all connections"""
        if 'initialized' in st.session_state:
            return True
            
        try:
            self.pd_client = Pipedream(
                project_id=os.getenv('PIPEDREAM_PROJECT_ID'),
                project_environment=os.getenv('PIPEDREAM_ENVIRONMENT'),
                client_id=os.getenv('PIPEDREAM_CLIENT_ID'),
                client_secret=os.getenv('PIPEDREAM_CLIENT_SECRET'),
            )
            
            self.access_token = self.pd_client.raw_access_token
            self.gemini_client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
            
            self.mcp_client = Client({
                "mcpServers": {
                    "pipedream": {
                        "transport": "http",
                        "url": "https://remote.mcp.pipedream.net",
                        "headers": {
                            "Authorization": f"Bearer {self.access_token}",
                            "x-pd-project-id": os.getenv('PIPEDREAM_PROJECT_ID'),
                            "x-pd-environment": os.getenv('PIPEDREAM_ENVIRONMENT'),
                            "x-pd-external-user-id": os.getenv('EXTERNAL_USER_ID'),
                            "x-pd-app-slug": "google_calendar",
                        },
                    }
                }
            })
            
            self.calendar_id = "pinkpantherking20@gmail.com"
            st.session_state.initialized = True
            st.session_state.mcp_client = self.mcp_client
            st.session_state.calendar_id = self.calendar_id
            st.session_state.gemini_client = self.gemini_client
            st.session_state.access_token = self.access_token
            return True
        except Exception as e:
            st.error(f"Initialization error: {e}")
            return False
    
    async def create_meeting(self, title, start_time, end_time, attendees, description=""):
        """Create a meeting with timezone-aware invitations"""
        try:
            attendee_emails = [{"email": email.strip()} for email in attendees if email.strip()]
            
            instruction = f"""Create a new event with these details:
- Title: {title}
- Start: {start_time.isoformat()}
- End: {end_time.isoformat()}
- Calendar ID: {self.calendar_id}
- Attendees: {', '.join([a['email'] for a in attendee_emails])}
- Description: {description}
- Send invitations: Yes"""
            
            async with self.mcp_client:
                result = await self.mcp_client.call_tool(
                    'google_calendar-create-event',
                    {'instruction': instruction}
                )
                return True, "Meeting created and invitations sent!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    async def chat_with_ai(self, message):
        """Chat with AI for calendar assistance"""
        try:
            mcp_client = Client({
                "mcpServers": {
                    "pipedream": {
                        "transport": "http",
                        "url": "https://remote.mcp.pipedream.net",
                        "headers": {
                            "Authorization": f"Bearer {st.session_state.access_token}",
                            "x-pd-project-id": os.getenv('PIPEDREAM_PROJECT_ID'),
                            "x-pd-environment": os.getenv('PIPEDREAM_ENVIRONMENT'),
                            "x-pd-external-user-id": os.getenv('EXTERNAL_USER_ID'),
                            "x-pd-app-slug": "google_calendar",
                        },
                    }
                }
            })
            
            async with mcp_client:
                now = datetime.now()
                current_date = now.strftime("%A, %B %d, %Y at %I:%M %p")
                
                config = genai.types.GenerateContentConfig(
                    temperature=0.1,
                    tools=[mcp_client.session],
                    tool_config={'function_calling_config': {'mode': 'auto'}},
                    system_instruction=f"""You are a helpful calendar assistant. Current date/time: {current_date}
                    
Your timezone is Asia/Karachi (UTC+5). Calendar ID: {st.session_state.calendar_id}

You can help users:
1. Schedule meetings - Ask for title, date, time, and attendees
2. View their calendar - Show events for today, tomorrow, or any date
3. Find free time - Check availability
4. Cancel or modify events

IMPORTANT TIMEZONE REFERENCES:
- 12:00 PM in Spain = 11:00 AM in UK = 4:00 PM in Pakistan
- Pakistan is UTC+5
- UK is UTC+0 (UTC+1 during summer/BST)
- Spain is UTC+1 (UTC+2 during summer)
- India is UTC+5:30
- Dubai is UTC+4
- US East is UTC-5
- US West is UTC-8

When creating events with attendees in different cities, automatically mention the time in their local timezone.

Be concise and helpful. Always use google_calendar-list-events with the specific calendar ID.""",
                )
                
                gemini = st.session_state.gemini_client
                chat = gemini.aio.chats.create(
                    model="gemini-2.5-flash",
                    config=config
                )
                
                response = await chat.send_message(message)
                
                max_iterations = 5
                iteration = 0
                while response.candidates[0].content.parts and iteration < max_iterations:
                    parts = response.candidates[0].content.parts
                    has_function_calls = any(
                        hasattr(part, 'function_call') and part.function_call 
                        for part in parts
                    )
                    
                    if not has_function_calls:
                        break
                    
                    response = await chat.send_message("")
                    iteration += 1
                
                return response.text
                
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"


def get_time_in_city(base_datetime, from_tz, to_city):
    """Convert time from one timezone to a city's timezone"""
    to_tz_name = CITY_TIMEZONES.get(to_city)
    if not to_tz_name:
        return None, None
    
    to_tz = pytz.timezone(to_tz_name)
    converted = base_datetime.astimezone(to_tz)
    return converted, to_tz_name


def main():
    st.title("📅 Smart Calendar Assistant")
    
    # Initialize
    calendar_ui = CalendarUI()
    
    if 'initialized' not in st.session_state:
        with st.spinner("🔄 Connecting to Google Calendar..."):
            success = asyncio.run(calendar_ui.initialize())
            if success:
                st.success("✅ Connected!")
            else:
                st.error("Failed to connect. Check credentials.")
                return
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Chatbot", "📝 Schedule Meeting", "🌍 Time Converter", "⚙️ Settings"])
    
    # ==================== TAB 1: AI CHATBOT ====================
    with tab1:
        st.markdown("### 🤖 AI Calendar Assistant")
        st.markdown("*Just tell me what you want in plain English!*")
        
        with st.expander("💡 Example commands"):
            st.markdown("""
            - "What's on my calendar today?"
            - "Schedule a meeting tomorrow at 3 PM with john@example.com"
            - "Create a team call on Monday at 10 AM"
            - "Schedule a call at 4 PM Pakistan time with friends in UK and Spain"
            - "Do I have any free time on Friday?"
            - "Show my schedule for next week"
            """)
        
        # Chat display
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.chat_message("user").write(msg['content'])
            else:
                st.chat_message("assistant").write(msg['content'])
        
        # Chat input
        if prompt := st.chat_input("Type your message... e.g., Schedule a meeting tomorrow at 2 PM"):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    calendar_ui.mcp_client = st.session_state.mcp_client
                    calendar_ui.calendar_id = st.session_state.calendar_id
                    response = asyncio.run(calendar_ui.chat_with_ai(prompt))
                st.write(response)
            
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # ==================== TAB 2: SCHEDULE MEETING ====================
    with tab2:
        st.markdown("### 📝 Schedule Meeting")
        st.info("💡 Set YOUR time and city - friends' times auto-adjust based on their city!")
        
        # Your settings
        st.markdown("#### 🧑 Your Details")
        col1, col2 = st.columns(2)
        
        with col1:
            meeting_title = st.text_input("Meeting Title *", placeholder="Team Sync")
            meeting_date = st.date_input("Date *", value=datetime.now())
            meeting_time = st.time_input("Time (YOUR local time) *", value=datetime.now().replace(hour=14, minute=0).time())
        
        with col2:
            # Your timezone selection
            tz_mode = st.radio("Select your timezone by:", ["🏙️ City", "🔢 UTC Offset"], horizontal=True)
            
            if tz_mode == "🏙️ City":
                your_city = st.selectbox(
                    "Your City *",
                    CITIES,
                    index=CITIES.index("Karachi") if "Karachi" in CITIES else 0
                )
                your_timezone = CITY_TIMEZONES[your_city]
            else:
                offset_label = st.selectbox(
                    "UTC Offset *",
                    list(UTC_OFFSETS.keys()),
                    index=list(UTC_OFFSETS.keys()).index("UTC+05:00 (Pakistan)")
                )
                offset_hours = UTC_OFFSETS[offset_label]
                # Map to pytz timezone
                if offset_hours == 0:
                    your_timezone = "UTC"
                elif offset_hours == 5:
                    your_timezone = "Asia/Karachi"
                elif offset_hours == 5.5:
                    your_timezone = "Asia/Kolkata"
                elif offset_hours == 1:
                    your_timezone = "Europe/Madrid"
                else:
                    your_timezone = f"Etc/GMT{-int(offset_hours)}" if offset_hours != int(offset_hours) else f"Etc/GMT{-int(offset_hours)}"
            
            duration = st.selectbox("Duration", [30, 45, 60, 90, 120], index=2)
        
        st.markdown("---")
        
        # Friends
        st.markdown("#### 👥 Add Friends (just select their city!)")
        
        num_friends = st.number_input("Number of friends", min_value=1, max_value=10, value=3)
        
        friends = []
        
        # Create localized meeting time
        try:
            your_tz = pytz.timezone(your_timezone)
            meeting_dt = datetime.combine(meeting_date, meeting_time)
            meeting_dt = your_tz.localize(meeting_dt)
        except:
            meeting_dt = None
        
        cols = st.columns(3)
        for i in range(int(num_friends)):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"**Friend {i+1}**")
                    email = st.text_input(f"Email", key=f"friend_email_{i}", placeholder="friend@email.com")
                    city = st.selectbox(f"City", CITIES, key=f"friend_city_{i}", index=0)
                    
                    if email and meeting_dt:
                        friends.append({"email": email, "city": city})
                        # Show their local time
                        friend_time, friend_tz = get_time_in_city(meeting_dt, your_timezone, city)
                        if friend_time:
                            day_diff = ""
                            if friend_time.date() > meeting_dt.date():
                                day_diff = " *(+1 day)*"
                            elif friend_time.date() < meeting_dt.date():
                                day_diff = " *(-1 day)*"
                            st.success(f"⏰ **{friend_time.strftime('%I:%M %p')}**{day_diff}")
        
        st.markdown("---")
        
        # Preview
        if meeting_title and friends and meeting_dt:
            st.markdown("#### 📋 Meeting Preview")
            
            preview_col1, preview_col2 = st.columns(2)
            
            with preview_col1:
                st.markdown(f"**📌 {meeting_title}**")
                st.markdown(f"📅 {meeting_dt.strftime('%A, %B %d, %Y')}")
                st.markdown(f"⏰ Your time: **{meeting_dt.strftime('%I:%M %p')}** ({your_timezone})")
            
            with preview_col2:
                st.markdown("**Attendees & Their Local Times:**")
                for friend in friends:
                    friend_time, friend_tz = get_time_in_city(meeting_dt, your_timezone, friend['city'])
                    if friend_time:
                        st.write(f"• {friend['email']}: **{friend_time.strftime('%I:%M %p')}** ({friend['city']})")
        
        # Create button
        if st.button("🚀 Create Meeting & Send Invites", type="primary", use_container_width=True):
            if not meeting_title:
                st.error("Please enter a meeting title")
            elif not friends:
                st.error("Please add at least one friend")
            elif not meeting_dt:
                st.error("Invalid timezone configuration")
            else:
                with st.spinner("Creating meeting..."):
                    end_dt = meeting_dt + timedelta(minutes=duration)
                    attendee_emails = [f['email'] for f in friends]
                    
                    # Build description with all times
                    desc_lines = ["Meeting times for attendees:\n"]
                    for friend in friends:
                        friend_time, _ = get_time_in_city(meeting_dt, your_timezone, friend['city'])
                        if friend_time:
                            desc_lines.append(f"• {friend['email']} ({friend['city']}): {friend_time.strftime('%I:%M %p on %b %d')}")
                    
                    calendar_ui.mcp_client = st.session_state.mcp_client
                    calendar_ui.calendar_id = st.session_state.calendar_id
                    
                    success, message = asyncio.run(
                        calendar_ui.create_meeting(
                            meeting_title,
                            meeting_dt,
                            end_dt,
                            attendee_emails,
                            "\n".join(desc_lines)
                        )
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(message)
    
    # ==================== TAB 3: TIME CONVERTER ====================
    with tab3:
        st.markdown("### 🌍 World Time Converter")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Enter Time")
            conv_time = st.time_input("Time", value=datetime.now().time(), key="conv_time")
            conv_date = st.date_input("Date", value=datetime.now(), key="conv_date")
            from_city = st.selectbox("From City", CITIES, index=CITIES.index("Karachi") if "Karachi" in CITIES else 0, key="from_city")
        
        with col2:
            st.markdown("#### Time Around the World")
            
            from_tz = pytz.timezone(CITY_TIMEZONES[from_city])
            base_dt = datetime.combine(conv_date, conv_time)
            base_dt = from_tz.localize(base_dt)
            
            # Key cities to show
            show_cities = ["London", "Madrid", "Karachi", "Mumbai", "Dubai", "New York", "Los Angeles", "Tokyo", "Sydney"]
            
            for city in show_cities:
                if city in CITY_TIMEZONES:
                    converted, _ = get_time_in_city(base_dt, from_city, city)
                    if converted:
                        day_diff = ""
                        if converted.date() > base_dt.date():
                            day_diff = " (+1 day)"
                        elif converted.date() < base_dt.date():
                            day_diff = " (-1 day)"
                        
                        flag = {"London": "🇬🇧", "Madrid": "🇪🇸", "Karachi": "🇵🇰", "Mumbai": "🇮🇳", 
                               "Dubai": "🇦🇪", "New York": "🇺🇸", "Los Angeles": "🇺🇸", "Tokyo": "🇯🇵", "Sydney": "🇦🇺"}.get(city, "🌍")
                        st.write(f"{flag} **{city}**: {converted.strftime('%I:%M %p')}{day_diff}")
        
        st.markdown("---")
        st.markdown("#### ⏰ Current Times")
        
        current_cols = st.columns(4)
        current_cities = [("🇵🇰", "Karachi"), ("🇬🇧", "London"), ("🇪🇸", "Madrid"), ("🇮🇳", "Mumbai"),
                         ("🇦🇪", "Dubai"), ("🇺🇸", "New York"), ("🇯🇵", "Tokyo"), ("🇦🇺", "Sydney")]
        
        for i, (flag, city) in enumerate(current_cities):
            with current_cols[i % 4]:
                tz = pytz.timezone(CITY_TIMEZONES[city])
                now = datetime.now(tz)
                st.metric(f"{flag} {city}", now.strftime("%I:%M %p"), now.strftime("%b %d"))
        
        # Quick reference
        st.markdown("---")
        st.markdown("#### 📖 Quick Reference")
        st.info("""
        **Example**: When it's **12:00 PM in Spain (Madrid)**:
        - 🇬🇧 UK (London): **11:00 AM** (1 hour behind)
        - 🇵🇰 Pakistan (Karachi): **4:00 PM** (4 hours ahead)
        - 🇮🇳 India (Mumbai): **4:30 PM** (4.5 hours ahead)
        - 🇦🇪 Dubai: **3:00 PM** (3 hours ahead)
        - 🇺🇸 New York: **6:00 AM** (6 hours behind)
        """)
    
    # ==================== TAB 4: SETTINGS ====================
    with tab4:
        st.markdown("### ⚙️ Timezone Reference")
        
        st.markdown("#### UTC Offsets by Region")
        
        regions = {
            "🇵🇰 Pakistan & Neighbors": [
                ("Pakistan", "UTC+5"),
                ("India", "UTC+5:30"),
                ("Bangladesh", "UTC+6"),
                ("Nepal", "UTC+5:45"),
                ("Afghanistan", "UTC+4:30"),
            ],
            "🇪🇺 Europe": [
                ("UK (London)", "UTC+0"),
                ("Spain (Madrid)", "UTC+1"),
                ("France (Paris)", "UTC+1"),
                ("Germany (Berlin)", "UTC+1"),
                ("Greece (Athens)", "UTC+2"),
                ("Turkey (Istanbul)", "UTC+3"),
            ],
            "🇺🇸 Americas": [
                ("US Eastern (New York)", "UTC-5"),
                ("US Central (Chicago)", "UTC-6"),
                ("US Mountain (Denver)", "UTC-7"),
                ("US Pacific (LA)", "UTC-8"),
                ("Brazil (Sao Paulo)", "UTC-3"),
            ],
            "🌏 Asia Pacific": [
                ("Dubai", "UTC+4"),
                ("China/Singapore", "UTC+8"),
                ("Japan/Korea", "UTC+9"),
                ("Australia Sydney", "UTC+10"),
                ("New Zealand", "UTC+12"),
            ],
        }
        
        cols = st.columns(2)
        for i, (region, countries) in enumerate(regions.items()):
            with cols[i % 2]:
                st.markdown(f"**{region}**")
                for country, utc in countries:
                    st.write(f"• {country}: {utc}")
                st.markdown("")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📅 Calendar Assistant")
        st.markdown("---")
        
        st.markdown("**⏰ Quick Times:**")
        for city in ["Karachi", "London", "Madrid"]:
            tz = pytz.timezone(CITY_TIMEZONES[city])
            now = datetime.now(tz)
            st.text(f"{city}: {now.strftime('%I:%M %p')}")
        
        st.markdown("---")
        st.markdown("**💡 Tips:**")
        st.markdown("""
        - Use **AI Chatbot** for quick commands
        - Just select friend's **city** - time auto-adjusts!
        - Spain is 1hr ahead of UK
        - Pakistan is 4hrs ahead of Spain
        """)


if __name__ == "__main__":
    main()
