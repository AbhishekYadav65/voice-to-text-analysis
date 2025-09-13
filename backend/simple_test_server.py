#!/usr/bin/env python3
"""
Simple test server for Truth Weaver
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

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

@app.route("/", methods=["GET"])
def root():
    """Root endpoint"""
    return jsonify({
        "service": "Truth Weaver - Whispering Shadows Mystery",
        "description": "AI Detective for analyzing deceptive audio testimonies",
        "status": "running"
    })

@app.route("/test-analysis", methods=["POST"])
def test_analysis():
    """Test the analysis pipeline without audio processing"""
    try:
        from pipeline import analyze
        
        # Get text from request
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Run analysis
        revealed_truth, deception_patterns = analyze.extract_truth(text, "test_shadow")
        
        return jsonify({
            "shadow_id": "test_shadow",
            "revealed_truth": revealed_truth,
            "deception_patterns": deception_patterns,
            "input_text": text
        })
        
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

if __name__ == "__main__":
    print("🕵️ Truth Weaver - Simple Test Server")
    print("🔍 Starting on http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
