# 🎙️ VoiceAid

**VoiceAid** is an assistive web app that helps users improve the tone of their written communication. It rewrites messages in different tones using AI, speaks them aloud, and keeps a history for easy reuse.

## ✨ Features

- ✅ Rewrite messages in tones like professional, friendly, or apologetic
- ✅ Google-powered tone rewriting using Gemini API
- ✅ Speak rewritten messages using TTS (Google TTS or offline pyttsx3 fallback)
- ✅ Save message history (JSON-based) with favorites, reuse, delete options
- ✅ Filter favorites, sort messages (latest/oldest)
- ✅ Light/Dark mode toggle
- ✅ Fully offline fallback supported

## Target Users:

- People with ALS, cerebral palsy, and non-verbal autism
- ICU patients or post-surgery individuals
- The elderly with age-related speech impairments
- People with voice loss (e.g. laryngectomy)
- People not very fluent in English and just know a few words

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/voiceaid.git
   cd voiceaid
Set up your environment
Make sure Python 3.9+ is installed. Then:

bash
Copy
Edit
pip install -r requirements.txt
Set up Google API key

Get a Gemini API key from: https://makersuite.google.com/app/apikey

Create a .env file:

ini
Copy
Edit
GEMINI_API_KEY=your_key_here
Run the app

bash
Copy
Edit
streamlit run app.py
📁 Project Structure
bash
Copy
Edit
voiceaid/
├── app.py                # Main Streamlit app
├── tone_utils.py         # Tone rewriting via Gemini
├── tts_utils.py          # TTS engine (Google and offline)
├── history_utils.py      # Message history management (save, delete, favorites)
├── ui_utils.py           # UI helpers (filters, dropdowns, dark mode)
├── data/
│   └── history.json      # Stores all rewritten messages
├── .env                  # Gemini API key
├── requirements.txt      # Dependencies
└── README.md             # You're reading it!
🎯 Roadmap
 Basic tone rewriting

 Text-to-speech with online/offline fallback

 Message history with favorites

 Filters and sorting

 Dark mode UI

 Multi-language TTS (future)

🙌 Credits
Built with ❤️ using Streamlit, Google Gemini API, and Python.

📜 License
MIT License — free to use and modify.
