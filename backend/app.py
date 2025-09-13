from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import preprocess, stt, postprocess, analyze, output
import os
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all origins in development

@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """
    Main endpoint for processing audio files from Whispering Shadows.
    Handles single session analysis.
    """
    try:
        print("\n=== New Upload Request ===")
        print("Headers:", dict(request.headers))
        print("Form data:", dict(request.form))
        print("Files:", request.files.keys())
        
        # Validate file in request
        if "file" not in request.files:
            print("Error: No file in request. Available keys:", request.files.keys())
            return jsonify({"error": "No file found in request"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            print("Error: Empty filename")
            return jsonify({"error": "No selected file"}), 400
        
        print(f"Received file: {file.filename}")
        print(f"Content Type: {file.content_type}")
        print(f"File size: {request.content_length} bytes")

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
        analysis_result = analyze.extract_truth(cleaned_text, shadow_id)
        
        # 5. Generate final output
        print("📊 Generating analysis...")
        final_json = {
            "transcript": cleaned_text,
            "shadow_id": shadow_id,
            "revealed_truth": analysis_result["revealed_truth"],
            "deception_patterns": analysis_result["deception_patterns"]
        }
        
        # 6. Save files for submission
        transcript_file = output.save_transcript(cleaned_text, shadow_id, 1)
        json_file = output.save_final_json(analysis_result["revealed_truth"], analysis_result["deception_patterns"], shadow_id)
        
        # Add file paths to response
        final_json["transcript_file"] = transcript_file
        final_json["json_file"] = json_file
        
        print(f"✅ Analysis complete for {shadow_id}")
        return jsonify(final_json)
        
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"❌ Error processing audio: {e}")
        print(tb)
        return jsonify({"error": f"Processing failed: {str(e)}", "traceback": tb}), 500

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
                    
                    print(f"Processing session {i} audio file: {filepath}")
                    try:
                        # Process this session
                        print("Cleaning audio...")
                        cleaned_audio = preprocess.clean_audio(filepath)
                        print("Transcribing audio...")
                        transcript = stt.transcribe_audio(cleaned_audio)
                        print("Cleaning text...")
                        cleaned_text = postprocess.clean_text(transcript)
                        print("Analyzing for truth...")
                        analysis_result = analyze.extract_truth(cleaned_text, shadow_id)
                    except Exception as e:
                        print(f"Error processing session {i}: {e}")
                        continue
                    
                    sessions_data.append({
                        "transcript": cleaned_text,
                        "revealed_truth": analysis_result["revealed_truth"],
                        "deception_patterns": analysis_result["deception_patterns"]
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
    app.run(debug=True, host="0.0.0.0", port=5001)
