#!/bin/bash

# ✅ Navigate to VoiceAid project (optional if you're already in the folder)
cd "$(dirname "$0")"

# ✅ Activate virtual environment
source venv/bin/activate

# ✅ Set Gemini API key (REPLACE with your real key!)
export GEMINI_API_KEY="AIzaSyDoaiJgfz_5CLWnBfsgK6RHX5ORNHIUuX4"

# ✅ Run the app
streamlit run app.py
