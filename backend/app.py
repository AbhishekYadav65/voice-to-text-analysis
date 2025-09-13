from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import preprocess, stt, postprocess, analyze, output
import os
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """
    Main endpoint for processing audio files from Whispering Shadows.
    Handles single session analysis.
    """
    try:
        # Validate file in request
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        # Get shadow_id from request or generate one
        shadow_id = request.form.get("shadow_id", f"shadow_{uuid.uuid4().hex[:8]}")
        
        # Ensure uploads directory exists and save file
        os.makedirs("uploads", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"uploads/{shadow_id}_{timestamp}_{file.filename}"
        file.save(filepath)

        # Run the Truth Weaver pipeline
        print(f"🔍 Processing Shadow: {shadow_id}")
        
        # 1. Preprocess audio (handle poor quality, static, whispers)
        print("🎵 Cleaning audio...")
        cleaned_audio = preprocess.clean_audio(filepath)
        
        # 2. Transcribe using Whisper
        print("🎤 Transcribing audio...")
        transcript = stt.transcribe_audio(cleaned_audio)
        
        # 3. Postprocess text
        print("📝 Cleaning transcript...")
        cleaned_text = postprocess.clean_text(transcript)
        
        # 4. Analyze for truth and deception patterns
        print("🕵️ Analyzing for truth and deception...")
        revealed_truth, deception_patterns = analyze.extract_truth(cleaned_text, shadow_id)
        
        # 5. Generate final output
        print("📊 Generating analysis...")
        final_json = output.generate_json(cleaned_text, revealed_truth, deception_patterns, shadow_id)
        
        # 6. Save files for submission
        transcript_file = output.save_transcript(cleaned_text, shadow_id, 1)
        json_file = output.save_final_json(revealed_truth, deception_patterns, shadow_id)
        
        # Add file paths to response
        final_json["transcript_file"] = transcript_file
        final_json["json_file"] = json_file
        
        print(f"✅ Analysis complete for {shadow_id}")
        return jsonify(final_json)
        
    except Exception as e:
        print(f"❌ Error processing audio: {e}")
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

@app.route("/upload-multiple-sessions", methods=["POST"])
def upload_multiple_sessions():
    """
    Endpoint for processing multiple sessions for a single shadow.
    Handles the 5-session structure described in the project.
    """
    try:
        shadow_id = request.form.get("shadow_id", f"shadow_{uuid.uuid4().hex[:8]}")
        sessions_data = []
        
        # Process each uploaded file as a separate session
        for i in range(1, 6):  # Sessions 1-5
            file_key = f"session_{i}"
            if file_key in request.files:
                file = request.files[file_key]
                if file.filename:
                    # Save and process each session
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filepath = f"uploads/{shadow_id}_session_{i}_{timestamp}_{file.filename}"
                    file.save(filepath)
                    
                    # Process this session
                    cleaned_audio = preprocess.clean_audio(filepath)
                    transcript = stt.transcribe_audio(cleaned_audio)
                    cleaned_text = postprocess.clean_text(transcript)
                    revealed_truth, deception_patterns = analyze.extract_truth(cleaned_text, shadow_id)
                    
                    sessions_data.append({
                        "transcript": cleaned_text,
                        "revealed_truth": revealed_truth,
                        "deception_patterns": deception_patterns
                    })
        
        if not sessions_data:
            return jsonify({"error": "No valid sessions provided"}), 400
        
        # Process multiple sessions
        result = output.process_multiple_sessions(sessions_data, shadow_id)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error processing multiple sessions: {e}")
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Truth Weaver - Whispering Shadows Mystery",
        "version": "1.0.0"
    })

@app.route("/", methods=["GET"])
def root():
    """Root endpoint with service information"""
    return jsonify({
        "service": "Truth Weaver - Whispering Shadows Mystery",
        "description": "AI Detective for analyzing deceptive audio testimonies",
        "endpoints": {
            "/upload-audio": "Process single audio session",
            "/upload-multiple-sessions": "Process multiple sessions for one shadow",
            "/health": "Health check"
        }
    })

if __name__ == "__main__":
    print("🕵️ Truth Weaver - Whispering Shadows Mystery")
    print("🔍 AI Detective Service Starting...")
    app.run(debug=True, host="0.0.0.0", port=5000)
