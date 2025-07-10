import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from gtts import gTTS
import tempfile
import os

# Securely load Gemini API key from Streamlit secrets
genai_api_key = st.secrets.get("genai_api_key")

if not genai_api_key:
    st.error("❌ Gemini API key missing. Please add it in Streamlit secrets.")
    st.stop()

# Setup LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=genai_api_key)

# Prompt template for best quality tone conversion
prompt = ChatPromptTemplate.from_template("""
You are a professional communication assistant that rewrites user messages in a specified tone.

Available tones: professional, casual, friendly, witty, urgent.

Your job is to rewrite the input message to match the selected tone as naturally as possible, while preserving its meaning and intent.

Tone: {tone}
Original Message: {input_text}

Rewritten Message:
""")

# LLM Chain
chain = prompt | llm

# Streamlit App UI
st.set_page_config(page_title="VoiceAid", page_icon="🗣️", layout="centered")
st.title("🗣️ VoiceAid")
st.subheader("Transform your message into a new tone")

# Tone selector
tone = st.selectbox("Select a tone", ["professional", "casual", "friendly", "witty", "urgent"])

# Message input
input_text = st.text_area("Enter your original message")

# Action button
if st.button("Rewrite"):
    if not input_text.strip():
        st.warning("Please enter a message to rewrite.")
        st.stop()

    with st.spinner("Rewriting your message..."):
        try:
            response = chain.invoke({"tone": tone, "input_text": input_text})
            rewritten = response.content.strip()

            st.markdown("### ✨ Rewritten Message")
            st.success(rewritten)

            # Text-to-speech
            tts = gTTS(text=rewritten, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                st.audio(tmp_file.name, format="audio/mp3")
        except Exception as e:
            st.error(f"⚠️ Something went wrong while generating the rewritten message.\n\nError: {e}")

#source venv/bin/activate
#export GEMINI_API_KEY="your-api-key-here"
#cd /Users/sanjanaramkumar/Downloads/Python/VoiceAid
#./start.sh




