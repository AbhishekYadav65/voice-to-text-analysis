from flask import Flask, request, jsonify
from pipeline import preprocess, stt, postprocess, analyze, output
import os

app = Flask(__name__)


@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    # Validate file in request
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Ensure uploads directory exists and save file
    os.makedirs("uploads", exist_ok=True)
    filepath = f"uploads/{file.filename}"
    file.save(filepath)

    # Run pipeline
    cleaned = preprocess.clean_audio(filepath)
    transcript = stt.transcribe_audio(cleaned)
    cleaned_text = postprocess.clean_text(transcript)
    facts, contradictions = analyze.extract_truth(cleaned_text)
    final_json = output.generate_json(cleaned_text, facts, contradictions)

    return jsonify(final_json)


if __name__ == "__main__":
    app.run(debug=True)
