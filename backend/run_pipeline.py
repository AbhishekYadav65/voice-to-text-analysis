from pipeline import preprocess, stt, postprocess, analyze, output


def main():
    # 1. Example input audio file (put one in backend/uploads/)
    input_audio = r"C:\Users\Abhishek\Documents\Sound Recordings\Recording.m4a"

    # 2. Preprocess
    cleaned_audio = preprocess.clean_audio(input_audio)
    print("[DEBUG] Cleaned audio:", cleaned_audio)

    # 3. Transcribe (currently dummy until API integrated)
    transcript = stt.transcribe_audio(cleaned_audio)
    print("[DEBUG] Transcript:", transcript)

    # 4. Postprocess
    cleaned_text = postprocess.clean_text(transcript)
    print("[DEBUG] Cleaned text:", cleaned_text)

    # 5. Analyze
    facts, contradictions = analyze.extract_truth(cleaned_text)
    print("[DEBUG] Facts:", facts)
    print("[DEBUG] Contradictions:", contradictions)

    # 6. Output
    result_json = output.generate_json(cleaned_text, facts, contradictions)
    print("[FINAL JSON]", result_json)


if __name__ == "__main__":
    main()
