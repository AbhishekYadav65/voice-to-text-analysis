# backend/app.py
import os
import uuid
import json
import traceback
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from pipeline import preprocess, stt, postprocess, analyze, output

ALLOWED_EXT = {".wav", ".mp3", ".m4a", ".flac", ".ogg"}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "transcripts")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

for d in (UPLOAD_DIR, TRANSCRIPTS_DIR, OUTPUT_DIR):
    os.makedirs(d, exist_ok=True)

def save_uploaded_file(file_obj, dest_dir, prefix="upload"):
    filename = secure_filename(file_obj.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext == "":
        raise ValueError("Uploaded file missing extension")
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    name = f"{prefix}_{ts}_{uuid.uuid4().hex[:8]}_{filename}"
    path = os.path.join(dest_dir, name)
    file_obj.save(path)
    return path

@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """Single session processing. Expects file under 'file'."""
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided under key 'file'"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        shadow_id = request.form.get("shadow_id") or f"shadow_{uuid.uuid4().hex[:8]}"
        saved_path = save_uploaded_file(file, UPLOAD_DIR, prefix=shadow_id)
        app.logger.info(f"Saved upload: {saved_path}")

        cleaned_audio = preprocess.clean_audio(saved_path)
        transcript = stt.transcribe_audio(cleaned_audio)
        cleaned_text = postprocess.clean_text(transcript)

        # Make analysis accept sessions list for deterministic interface
        analysis_result = analyze.extract_truth_for_sessions(sessions=[{"session": 1, "text": cleaned_text}], shadow_id=shadow_id)

        # Save files
        transcript_file = output.save_transcript_single(cleaned_text, shadow_id, session_idx=1, base_dir=TRANSCRIPTS_DIR)
        final_json_file = output.save_final_json(analysis_result, shadow_id, base_dir=OUTPUT_DIR)

        response = {
            "shadow_id": shadow_id,
            "transcript": cleaned_text,
            "transcript_file": transcript_file,
            "json_file": final_json_file,
            "revealed_truth": analysis_result["revealed_truth"],
            "deception_patterns": analysis_result["deception_patterns"],
        }
        return jsonify(response)

    except Exception as e:
        tb = traceback.format_exc()
        app.logger.error(f"Error in /upload-audio: {e}\n{tb}")
        return jsonify({"error": str(e), "traceback": tb.splitlines()[-10:]}), 500


@app.route("/upload-multiple-sessions", methods=["POST"])
def upload_multiple_sessions():
    try:
        shadow_id = request.form.get("shadow_id") or f"shadow_{uuid.uuid4().hex[:8]}"
        sessions = []

        for i in range(1, 6):
            key = f"session_{i}"
            if key in request.files:
                f = request.files[key]
                if f and f.filename:
                    saved_path = save_uploaded_file(f, UPLOAD_DIR, prefix=f"{shadow_id}_s{i}")
                    cleaned_audio = preprocess.clean_audio(saved_path)
                    transcript = stt.transcribe_audio(cleaned_audio)
                    cleaned_text = postprocess.clean_text(transcript)
                    sessions.append({"session": i, "text": cleaned_text})

        if not sessions:
            return jsonify({"error": "No session files uploaded"}), 400

        analysis_result = analyze.extract_truth_for_sessions(sessions, shadow_id=shadow_id)

        transcript_files = []
        for s in sessions:
            tf = output.save_transcript_single(s["text"], shadow_id, session_idx=s["session"], base_dir=TRANSCRIPTS_DIR)
            transcript_files.append({"session": s["session"], "file": tf})

        final_json_file = output.save_final_json(analysis_result, shadow_id, base_dir=OUTPUT_DIR)

        return jsonify({
            "shadow_id": shadow_id,
            "transcript_files": transcript_files,
            "json_file": final_json_file,
            "revealed_truth": analysis_result["revealed_truth"],
            "deception_patterns": analysis_result["deception_patterns"],
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "truth-weaver", "version": "1.0.0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
