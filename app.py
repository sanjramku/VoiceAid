import streamlit as st
import google.generativeai as genai
import os
import socket
import json
from gtts import gTTS
from playsound import playsound
import tempfile
import pyttsx3
from datetime import datetime

# 🔧 Page configuration
st.set_page_config(page_title="VoiceAid", layout="centered")
st.title("🗣️ VoiceAid - AI Speech Assistant")

# 🌙 Dark mode toggle
dark_mode = st.checkbox("🌃 Dark Mode", value=False)

# 💅 Apply dark mode CSS
if dark_mode:
    st.markdown("""
        <style>
            body, .stApp, .stMarkdown, .stTextInput, .stSelectbox, .stButton, .stCheckbox, .stExpander {
                background-color: #121212 !important;
                color: #f5f5f5 !important;
            }
            .stTextInput input, .stSelectbox div[data-baseweb="select"] {
                background-color: #1e1e1e !important;
                color: #f5f5f5 !important;
            }
            .stButton > button {
                background-color: #333333 !important;
                color: #f5f5f5 !important;
            }
            ::-webkit-scrollbar {
                width: 8px;
            }
            ::-webkit-scrollbar-thumb {
                background: #555;
            }
        </style>
    """, unsafe_allow_html=True)

st.markdown("Helping people express themselves clearly and naturally.")

# 🌐 Internet check
def has_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# 💾 File path for history
HISTORY_FILE = "history.json"

# 📁 Load history from JSON file
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# 💾 Save history to JSON file
def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# 🔃 Initialize history in session state
if "history" not in st.session_state:
    st.session_state.history = load_history()

# 🧠 Input fields
user_input = st.text_input("Type a short message you'd like to say:", placeholder="e.g. help tired now")
tone = st.selectbox("Choose a tone:", ["Neutral", "Polite", "Friendly", "Urgent"])

# 💡 Tone description
tone_descriptions = {
    "Neutral": "A clear and straightforward voice, without emotion.",
    "Polite": "Softened, courteous and respectful tone.",
    "Friendly": "Warm and casual, like talking to a friend.",
    "Urgent": "Short, fast, and direct — for emergencies or important situations."
}
st.info(f"💡 Tone preview: {tone_descriptions[tone]}")

# ✅ Load Gemini API key
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("❌ Gemini API key not found in Streamlit secrets. Please add it.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# 🌟 Rewriting and speaking logic
if st.button("🔁 Rewrite and Speak"):
    if not user_input:
        st.warning("Please enter a message.")
    else:
        with st.spinner("Rewriting with Gemini..."):
            prompt = f"""
You are a communication assistant. Your job is to rewrite the following message in a **{tone.lower()}** tone.
Keep the rewritten version short, clear, and appropriate for speech.

Guidelines:
- Maintain the original meaning.
- Use natural spoken phrasing.
- Avoid overly formal or complex language.
{"- Be direct, short, and urgent-sounding. Use action words if appropriate.\n" if tone == "Urgent" else ""}

Original message: "{user_input}"

Rewritten:
"""
            try:
                response = model.generate_content(prompt)
                rewritten = response.candidates[0].content.parts[0].text.strip()
                st.success("✅ Rewritten message:")
                st.write(f"💬 {rewritten}")

                # Save to history
                new_entry = {
                    "tone": tone,
                    "message": rewritten,
                    "favorite": False,
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.history.append(new_entry)
                save_history(st.session_state.history)

                # Speak message
                with st.spinner("Speaking..."):
                    if has_internet():
                        tts = gTTS(rewritten)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                            tts.save(fp.name)
                            playsound(fp.name)
                    else:
                        engine = pyttsx3.init()
                        engine.setProperty('rate', 170 if tone == "Urgent" else 150)
                        engine.say(rewritten)
                        engine.runAndWait()
            except Exception as e:
                st.error("⚠️ Something went wrong while connecting to Gemini or TTS.")
                st.exception(e)

# 🔍 Filter & sort options
with st.expander("🔍 Filter History"):
    search_query = st.text_input("Search by keyword")
    tone_filter = st.selectbox("Filter by tone", ["All"] + list(tone_descriptions.keys()))
    sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Favorites First"])

# 📜 Display history
if st.session_state.history:
    st.subheader("🕓 Previous Messages")
    history = st.session_state.history

    # Filtering
    if search_query:
        history = [h for h in history if search_query.lower() in h["message"].lower()]
    if tone_filter != "All":
        history = [h for h in history if h["tone"] == tone_filter]

    # Sorting
    if sort_by == "Newest":
        history = sorted(history, key=lambda x: x["timestamp"], reverse=True)
    elif sort_by == "Oldest":
        history = sorted(history, key=lambda x: x["timestamp"])
    elif sort_by == "Favorites First":
        history = sorted(history, key=lambda x: (not x["favorite"], x["timestamp"]), reverse=True)

    # Display
    for i, entry in enumerate(history):
        col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
        with col1:
            st.markdown(f"**[{entry['tone']}]** {entry['message']}")
        with col2:
            if st.button("🔊", key=f"speak_{i}"):
                with st.spinner("Speaking..."):
                    try:
                        if has_internet():
                            tts = gTTS(entry["message"])
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                                tts.save(fp.name)
                                playsound(fp.name)
                        else:
                            engine = pyttsx3.init()
                            engine.setProperty('rate', 170 if entry["tone"] == "Urgent" else 150)
                            engine.say(entry["message"])
                            engine.runAndWait()
                    except Exception as e:
                        st.error("⚠️ Failed to speak.")
                        st.exception(e)
        with col3:
            if st.button("⭐" if entry.get("favorite") else "☆", key=f"fav_{i}"):
                entry["favorite"] = not entry.get("favorite", False)
                save_history(st.session_state.history)
                st.rerun()
        with col4:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.history.remove(entry)
                save_history(st.session_state.history)
                st.rerun()

#source venv/bin/activate
#export GEMINI_API_KEY="your-api-key-here"
#cd /Users/sanjanaramkumar/Downloads/Python/VoiceAid
#./start.sh




