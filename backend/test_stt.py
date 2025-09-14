# backend/test_stt.py
import os
from pipeline import stt
from pipeline import postprocess, analyze, output

test_dir = "test_audio"
shadow_id = "test_shadow"

sessions = []
session_num = 1

for f in sorted(os.listdir(test_dir)):
    if f.lower().endswith((".wav", ".mp3", ".m4a", ".flac", ".ogg")):
        path = os.path.join(test_dir, f)
        print(f"\n🎙️ File: {f}")
        try:
            # Step 1: Transcribe
            raw_text = stt.transcribe_audio(path)
            cleaned_text = postprocess.clean_text(raw_text)
            print("Transcript:", cleaned_text)

            # Step 2: Save transcript file
            transcript_file = output.save_transcript_single(
                cleaned_text, shadow_id, session_idx=session_num, base_dir="transcripts"
            )
            print(f"Saved transcript: {transcript_file}")

            # Step 3: Store session data for later analysis
            sessions.append({"session": session_num, "text": cleaned_text})
            session_num += 1

        except Exception as e:
            print("Error:", e)

# Step 4: Run analysis across all sessions
if sessions:
    analysis_result = analyze.extract_truth_for_sessions(sessions, shadow_id=shadow_id)
    json_file = output.save_final_json(analysis_result, shadow_id, base_dir="output")
    print(f"\n📊 Saved analysis JSON: {json_file}")
