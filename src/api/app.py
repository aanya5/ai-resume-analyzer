from flask import Flask, request, jsonify, render_template
import os
from src.nlp.extract_text import extract_text_from_file
from src.nlp.job_description_parser import extract_keywords_from_jd
from src.scoring.ats_scoring import compute_ats_score

# Helper to save uploaded files temporarily
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # 1. Route to show the HTML Page
    @app.route("/", methods=["GET"])
    def home():
        return render_template("index.html")

    @app.route("/health", methods=["GET"])
    def health():
        return "ok", 200

    # 2. OLD API (JSON Text) - kept for compatibility
    @app.route("/analyze", methods=["POST"])
    def analyze():
        data = request.get_json() or {}
        resume_text = data.get("resume_text", "")
        jd_text = data.get("job_description", "")
        if not resume_text:
            return jsonify({"error": "resume_text required"}), 400

        jd_keywords = extract_keywords_from_jd(jd_text)
        score, details = compute_ats_score(resume_text, jd_keywords)
        return jsonify({"score": score, "details": details})

    # 3. NEW API (File Upload) - for the Frontend
    @app.route("/analyze_file", methods=["POST"])
    def analyze_file():
        if 'resume' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['resume']
        jd_text = request.form.get('job_description', '')

        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Save file temporarily to read it
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            # Extract text using your existing logic
            resume_text = extract_text_from_file(filepath)
            
            # Run Analysis
            jd_keywords = extract_keywords_from_jd(jd_text)
            score, details = compute_ats_score(resume_text, jd_keywords)
            
            # Clean up (delete temp file)
            os.remove(filepath)

            return jsonify({"score": score, "details": details})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app