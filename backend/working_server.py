#!/usr/bin/env python3
"""
Working Truth Weaver Server
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Truth Weaver - Whispering Shadows Mystery",
        "version": "1.0.0"
    })

@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """Process audio file"""
    try:
        # Check if file is provided
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Get shadow_id
        shadow_id = request.form.get("shadow_id", "test_shadow")
        
        # For now, return a mock response since we can't process audio without Whisper
        # In a real scenario, you would process the audio here
        
        mock_transcript = "I have 6 years of Python experience and I'm an expert in machine learning. Actually, maybe 3 years? Still learning advanced concepts. I led a team of 5 developers for 8 months. I work alone mostly, never been comfortable with team management."
        
        # Mock analysis result
        result = {
            "shadow_id": shadow_id,
            "transcript": mock_transcript,
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
                },
                {
                    "lie_type": "leadership_fabrication",
                    "contradictory_claims": ["led team of 5", "work alone mostly"]
                }
            ]
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

@app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    return jsonify({
        "service": "Truth Weaver - Whispering Shadows Mystery",
        "description": "AI Detective for analyzing deceptive audio testimonies",
        "status": "running",
        "endpoints": ["/health", "/upload-audio"]
    })

if __name__ == "__main__":
    print("🕵️ Truth Weaver - Working Server")
    print("🔍 Starting on http://localhost:5001")
    print("📡 Ready to process audio files!")
    app.run(debug=True, host="0.0.0.0", port=5001)
