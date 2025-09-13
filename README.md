# 🕵️ Truth Weaver - Whispering Shadows Mystery

**AI Detective for Analyzing Deceptive Audio Testimonies**

Built for **Innov8 3.0** - ARIES & Eightfold AI at Rendezvous IIT Delhi

## 🎯 Project Overview

The Truth Weaver is an advanced AI system designed to analyze audio recordings from "Whispering Shadows" - deceptive individuals who provide conflicting testimonies across multiple sessions. The system uses OpenAI Whisper for speech-to-text conversion and sophisticated analysis to detect contradictions and extract the most likely truth.

## 🔧 Features

### Core Capabilities
- **Advanced Audio Processing**: Handles poor quality audio with static, whispers, shouts, and background noise
- **Whisper Integration**: Uses OpenAI Whisper for accurate speech-to-text conversion
- **Contradiction Detection**: Identifies conflicting claims across multiple sessions
- **Truth Extraction**: Determines the most likely truth from deceptive testimonies
- **Multi-Session Analysis**: Processes up to 5 sessions per shadow for comprehensive analysis

### Audio Quality Handling
- Trembling whispers that are barely audible
- Nervous rambling and emotional breakdowns
- Background static from truth chambers
- Volume variations (whispers to shouts)
- Static and click removal

### Deception Pattern Detection
- Experience inflation (claiming more years than reality)
- Leadership fabrication (false team management claims)
- Skill exaggeration (overstating technical abilities)
- Contradictory statements across sessions

## 🚀 Installation

### Prerequisites
- Python 3.8+
- CUDA-compatible GPU (recommended for faster processing)

### Setup
```bash
# Clone the repository
cd backend

# Install dependencies
pip install -r requirements.txt

# Download Whisper model (first run will download automatically)
python -c "import whisper; whisper.load_model('base')"
```

## 🎮 Usage

### Starting the Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### 1. Single Session Analysis
```bash
curl -X POST http://localhost:5000/upload-audio \
  -F "file=@audio_file.wav" \
  -F "shadow_id=phoenix_2024"
```

#### 2. Multiple Sessions Analysis
```bash
curl -X POST http://localhost:5000/upload-multiple-sessions \
  -F "shadow_id=phoenix_2024" \
  -F "session_1=@session1.wav" \
  -F "session_2=@session2.wav" \
  -F "session_3=@session3.wav" \
  -F "session_4=@session4.wav" \
  -F "session_5=@session5.wav"
```

#### 3. Health Check
```bash
curl http://localhost:5000/health
```

## 📊 Output Format

### JSON Analysis Output
```json
{
  "shadow_id": "phoenix_2024",
  "revealed_truth": {
    "programming_experience": "3-4 years",
    "programming_language": "python",
    "skill_mastery": "intermediate",
    "leadership_claims": "fabricated",
    "team_experience": "individual contributor",
    "skills and other keywords": ["Machine Learning"]
  },
  "deception_patterns": [
    {
      "lie_type": "experience_inflation",
      "contradictory_claims": ["6 years", "3 years"]
    }
  ]
}
```

### File Outputs
- **Transcript Files**: `transcripts/{shadow_id}_session_{n}.txt`
- **Analysis JSON**: `output/{shadow_id}_analysis.json`
- **Combined Transcript**: `transcripts/{shadow_id}_combined_session_0.txt`

## 🏗️ Architecture

### Pipeline Components

1. **Preprocessing** (`pipeline/preprocess.py`)
   - Audio cleaning and noise reduction
   - Volume normalization
   - Speech enhancement
   - Static removal

2. **Speech-to-Text** (`pipeline/stt.py`)
   - OpenAI Whisper integration
   - Optimized for poor quality audio
   - Word-level timestamps

3. **Text Processing** (`pipeline/postprocess.py`)
   - Text cleaning and normalization
   - Whitespace handling

4. **Analysis** (`pipeline/analyze.py`)
   - Pattern extraction
   - Contradiction detection
   - Truth resolution algorithms

5. **Output** (`pipeline/output.py`)
   - JSON generation
   - File management
   - Multi-session merging

## 🧪 Testing

### Test with Sample Data
```bash
# Test single session
python -c "
from pipeline import preprocess, stt, postprocess, analyze, output
# Add your test audio file path
audio_file = 'test_audio.wav'
cleaned = preprocess.clean_audio(audio_file)
transcript = stt.transcribe_audio(cleaned)
cleaned_text = postprocess.clean_text(transcript)
revealed_truth, deception_patterns = analyze.extract_truth(cleaned_text)
result = output.generate_json(cleaned_text, revealed_truth, deception_patterns)
print(result)
"
```

## 📈 Performance Optimization

### GPU Acceleration
- Automatically detects CUDA availability
- Falls back to CPU if GPU not available
- Uses optimized Whisper settings for poor audio

### Audio Processing
- Efficient spectral processing
- Memory-optimized operations
- Batch processing for multiple sessions

## 🔍 Evaluation Metrics

The system is designed to optimize for:

1. **Transcript Accuracy**: Character similarity with ground truth
2. **Truth Extraction**: Jaccard similarity for JSON analysis
3. **Contradiction Detection**: Pattern recognition accuracy

## 🛠️ Development

### Adding New Deception Patterns
Edit `pipeline/analyze.py` to add new pattern detection:

```python
def detect_custom_pattern(transcript: str) -> List[Dict]:
    # Add your custom detection logic
    pass
```

### Extending Audio Processing
Modify `pipeline/preprocess.py` for additional audio enhancements:

```python
def custom_audio_enhancement(y, sr):
    # Add your custom processing
    return enhanced_audio
```

## 📝 Submission Requirements

For Innov8 3.0 submission, ensure you have:

1. ✅ **Transcript File** (.txt) - Generated automatically
2. ✅ **Final JSON File** (.json) - Generated automatically  
3. ✅ **Source Code Archive** (.zip) - This repository
4. ✅ **README** - This file with clear instructions

## 🎯 Agentic Flow (Bonus Challenge)

The system includes an intelligent decision-making framework for real-time interview adaptation:

### States
- **Listening**: Passive audio collection
- **Analyzing**: Processing current session
- **Intervening**: Active questioning based on contradictions
- **Validating**: Cross-referencing with previous sessions

### Signals
- Voice tone changes (confidence → uncertainty)
- Silence patterns (hesitation detection)
- Contradiction triggers (inconsistent claims)
- Emotional indicators (stress, panic)

### Actions
- **Continue Listening**: When testimony is consistent
- **Gentle Probe**: Ask clarifying questions
- **Direct Challenge**: Confront contradictions
- **Session Transition**: Move to next session

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is developed for Innov8 3.0 hackathon. All rights reserved.

## 🏆 Acknowledgments

- **Innov8 3.0** - ARIES & Eightfold AI at Rendezvous IIT Delhi
- **OpenAI Whisper** - For advanced speech recognition
- **The Whispering Shadows Mystery** - For the fascinating challenge

---

*"May your algorithms pierce every shadow"* 🕵️‍♂️
