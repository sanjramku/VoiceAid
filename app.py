import streamlit as st
import json
import os
from datetime import datetime
from gtts import gTTS
from pathlib import Path

# Optional Gemini integration
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts.chat import ChatPromptTemplate

# Load Gemini API key from Streamlit secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# Tone options
TONE_MAP = {
    "Neutral": "A clear and straightforward voice, without emotion.",
    "Friendly": "Warm, positive, and kind.",
    "Assertive": "Confident and direct, but respectful.",
    "Empathetic": "Understanding and compassionate.",
    "Professional": "Formal and respectful, suitable for a workplace.",
    "Humorous": "Light-hearted and funny.",
}

# App title
st.set_page_config(page_title="VoiceAid - AI Speech Assistant", page_icon="🗣️")

st.title("🗣️ VoiceAid - AI Speech Assistant")
st.markdown("Helping people express themselves clearly and naturally.")

# UI inputs
dark_mode = st.checkbox("🌙 Dark Mode")
input_text = st.text_input("Type a short message you'd like to say:", placeholder="e.g. Can you help me with this?")
tone = st.selectbox("Choose a tone:", list(TONE_MAP.keys()))

if tone:
    st.markdown(f"💡 **Tone preview:** {TONE_MAP[tone]}")

# Output placeholder
output_box = st.empty()

# Generate voice with gTTS and return path
def generate_voice(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# Load Gemini model
def get_rewritten_text(message, tone_style):
    if not GEMINI_API_KEY:
        return "[❌ Gemini API key missing. Please add it in Streamlit secrets.]"
    chat = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)
    system = f"""You are an assistant helping users rewrite short messages to match a specific tone.
Respond ONLY with the rewritten message – do NOT include explanations or commentary."""
    user_prompt = f"""Rewrite the following message in a {tone_style.lower()} tone:\n\n\"{message}\""""
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system),
        HumanMessage(content=user_prompt)
    ])
    chain = prompt | chat
    response = chain.invoke({})
    return response.content.strip()

# Main app logic
if st.button("Rewrite & Speak") and input_text.strip():
    with st.spinner("Rewriting your message..."):
        rewritten = get_rewritten_text(input_text, tone)
        output_box.success(f"📝 **Rewritten message:** {rewritten}")

        # Generate voice
        audio_path = "speech_output.mp3"
        generate_voice(rewritten, audio_path)

        # Audio playback (cross-platform)
        with open(audio_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        # Save history
        history = {
            "input": input_text,
            "tone": tone,
            "output": rewritten,
            "timestamp": str(datetime.now())
        }
        with open("history.json", "a") as f:
            f.write(json.dumps(history) + "\n")
else:
    st.markdown("👆 Enter a message and click **Rewrite & Speak**")

# Optional dark mode style
if dark_mode:
    st.markdown(
        """
        <style>
            body {
                background-color: #1e1e1e;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


#source venv/bin/activate
#export GEMINI_API_KEY="your-api-key-here"
#cd /Users/sanjanaramkumar/Downloads/Python/VoiceAid
#./start.sh




