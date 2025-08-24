
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from transcribe import transcribe_file
from summarize import summarize_long_text
from google_docs import clean_markdown, create_doc_with_text


load_dotenv()

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save temporarily
    os.makedirs("uploads", exist_ok=True)
    in_path = os.path.join("uploads", f.filename)
    f.save(in_path)

    # 1) Transcribe
    try:
        transcript_text = transcribe_file(in_path)
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {e}"}), 500

    # 2) Summarize
    try:
        title = "Lecture Summary"
        summary = summarize_long_text(transcript_text, title_hint=title)
    except Exception as e:
        return jsonify({"error": f"Summarization failed: {e}"}), 500

    # 3) Push to Google Docs
    try:
        doc_url = create_doc_with_text(title, summary)
    except Exception as e:
        return jsonify({"error": f"Google Docs write failed: {e}"}), 500

    # Clean up temp file
    try:
        os.remove(in_path)
    except Exception:
        pass

    plain_summary = clean_markdown(summary)

    return jsonify({
        "message": "Success",
        "google_doc_url": doc_url,
        "summary_preview": plain_summary[:500] + ("..." if len(plain_summary) > 500 else "")
    })


if __name__ == "__main__":
    # Run on port 8000 by default
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
