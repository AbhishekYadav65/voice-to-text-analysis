🕵️ Truth Weaver – Whispering Shadows Mystery

An AI-powered Digital Detective that listens to deceptive audio testimonies, transcribes them, and extracts the most likely truth by spotting contradictions and unreliable claims.

Built for Rendezvous IIT Delhi Hackathon – Organized by ARIES & Eightfold AI.

🚀 Features

🎙️ Speech-to-Text: Converts audio (via Whisper) into transcripts.

🧹 Preprocessing & Postprocessing: Cleans noisy, distorted speech.

🕵️ Truth Analysis: Detects contradictions, inflated claims, and fabrications.

📑 Hackathon-Compliant Outputs:

Transcript file (.txt) per session.

Final structured JSON (.json) with revealed truth & deception patterns.

🌐 Full-Stack App: Flask backend + Next.js frontend with clean UI.

⚡ Multi-Session Support: Upload up to 5 testimonies per shadow.

📂 Project Structure
voice-to-text-analysis/
│── backend/              # Flask backend
│   ├── app.py            # Main API server
│   ├── pipeline/         # Processing modules
│   │   ├── preprocess.py
│   │   ├── stt.py        # Whisper STT
│   │   ├── postprocess.py
│   │   ├── analyze.py    # Truth extraction
│   │   └── output.py
│   ├── transcripts/      # Generated .txt transcripts
│   ├── output/           # Generated .json analysis
│   ├── requirements.txt  # Python dependencies
│
│── frontend/             # Next.js frontend
│   ├── src/app/          # App router
│   │   └── api/          # API routes (proxy to backend)
│   ├── public/           # Static assets
│   ├── package.json      # Node dependencies
│
└── README.md             # You are here

⚙️ Setup Instructions
1️⃣ Backend (Flask + Whisper)

Go to backend:

cd backend


Install dependencies:

pip install -r requirements.txt


If Whisper/ffmpeg missing:

pip install openai-whisper torch torchaudio ffmpeg-python
sudo apt-get update && sudo apt-get install -y ffmpeg


Run backend server:

python app.py


Runs on:
👉 http://localhost:5001

2️⃣ Frontend (Next.js)

Go to frontend:

cd frontend


Install dependencies:

npm install


Start dev server:

npm run dev


Runs on:
👉 http://localhost:3000

3️⃣ Upload Audio & Analyze

Open http://localhost:3000

Choose:

🎙️ Record audio live

📂 Upload a single session file

📂 Upload multiple sessions (session_1 … session_5)

Results shown in UI:

Transcript (cleaned)

Truth Analysis (programming experience, language, leadership, contradictions)

Outputs saved in backend:

backend/transcripts/{shadow_id}_session_X.txt

backend/output/{shadow_id}_analysis.json

📑 Output Format (JSON Schema)
{
  "shadow_id": "string",
  "revealed_truth": {
    "programming_experience": "string",
    "programming_language": "string",
    "skill_mastery": "string",
    "leadership_claims": "string",
    "team_experience": "string",
    "skills and other keywords": ["string", "string"]
  },
  "deception_patterns": [
    {
      "lie_type": "string",
      "contradictory_claims": ["string", "string"]
    }
  ]
}

🛠 Development Notes

Whisper model can be changed in stt.py (tiny, base, small, medium, large).

Default: base (CPU-friendly).

Multi-session analysis merges testimonies to detect contradictions.

Analysis rules are in pipeline/analyze.py.

Extendable with more NLP logic (for advanced truth inference).

🎯 Hackathon Deliverables

✅ Transcript files (.txt)

✅ Final JSON (.json)

✅ Source code archive (this repo, minus audio/model weights)

⚡ Bonus: Agentic Flow diagram (AI interviewer decision-making)

📦 Example Requirements (backend/requirements.txt)
flask
flask-cors
openai-whisper
torch
torchaudio
ffmpeg-python

👨‍💻 Author

Abhishek Yadav

Built for Whispering Shadows Mystery – IIT Delhi Hackathon