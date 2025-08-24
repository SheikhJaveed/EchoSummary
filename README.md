
# AI Lecture Assistant (Speech → Notes → Google Doc)

This is a minimal working prototype that:
1) Accepts an audio file (lecture recording)
2) Transcribes it with **Whisper** (local, free)
3) Summarizes it with **Gemini**
4) Creates a **Google Doc** with the summary

> MVP: upload an audio file via a simple HTML form, then receive a Google Doc link.

---

## 🔧 Prerequisites

- **Python 3.10+**
- **ffmpeg** installed and on PATH (required by Whisper)
- A **Gemini API key** (for summarization). Get one at: https://ai.google.dev/
- A **Google Cloud project** with the **Google Docs API** enabled
  - Download an OAuth **credentials.json** for a Desktop app and place it at the project root.
  - The first run will open a browser to authorize; it will create `token.json`.

---

## ▶️ Quickstart

```bash
# 1) Create & activate a virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Set your Gemini key (Linux/macOS)
export GEMINI_API_KEY=YOUR_KEY_HERE
# Windows (PowerShell): 
#   setx GEMINI_API_KEY "YOUR_KEY_HERE" ; then restart terminal

# 4) Put your Google OAuth credentials
#    Place the file named 'credentials.json' in the project root

# 5) Run the server
python app.py

# 6) Open the UI and upload audio
#    http://127.0.0.1:8000
```

### Test locally without the UI
```bash
curl -F "file=@sample.mp3" http://127.0.0.1:8000/upload
```

---

## 🧠 Notes

- Whisper runs locally and can be slow on CPU. You can switch the model size in `transcribe.py` (`tiny`, `base`, `small`, `medium`, `large`). 
- For long lectures, we chunk the transcript for summarization to fit model limits.
- The created Google Doc URL will be printed in the server logs and returned by the API.

---

## 📁 Project Structure

```
lecture-assistant/
  app.py                 # Flask server + routes
  transcribe.py          # Whisper transcription
  summarize.py           # Gemini summarization (chunks long text)
  google_docs.py         # Create & write to Google Doc
  templates/
    index.html           # Simple upload page
  requirements.txt
  credentials.json       # (you provide)
  token.json             # (auto-created after first auth)
```

---

## 🔐 Environment variables

- `GEMINI_API_KEY` — your Gemini API key

---

## 🚀 Future ideas

- Real-time mic capture and streaming
- Notion integration
- Flashcard/Quiz generation from lecture notes
- Multi-language translation of notes
