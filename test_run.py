import requests
import json
import os
import sys

# Add the current folder to path so we can import your project code
sys.path.append(os.getcwd())

# Import your own text extractor function
from src.nlp.extract_text import extract_text_from_file

# CONFIGURATION
URL = "http://127.0.0.1:5001/analyze"
RESUME_PATH = os.path.join("data", "sample_resumes", "test_resume.docx")

# A real Job Description to test against
# A Job Description that actually matches your Resume
JOB_DESCRIPTION = """
We are looking for an experienced Closing Manager to oversee real estate transactions.
Must have experience with RESPA, TRID, and regulatory compliance.
Skills in risk management, strategic planning, and team leadership are required.
Experience with mortgage loans and financial acumen is a plus.
"""

def run_test():
    # 1. Check if file exists
    if not os.path.exists(RESUME_PATH):
        print(f"Error: File not found at {RESUME_PATH}")
        print("Please put a file named 'test_resume.pdf' in 'data/sample_resumes/'")
        return

    # 2. Extract text from the PDF using your project logic
    print(f"Reading resume from: {RESUME_PATH}...")
    try:
        resume_text = extract_text_from_file(RESUME_PATH)
        print(f"Successfully extracted {len(resume_text)} characters.")
    except Exception as e:
        print(f"Failed to read PDF: {e}")
        return

    # 3. Send to Server
    payload = {
        "resume_text": resume_text,
        "job_description": JOB_DESCRIPTION
    }

    print("Analyzing...")
    try:
        response = requests.post(URL, json=payload)
        result = response.json()
        
        print("\n" + "="*30)
        print("   📄 RESUME ANALYSIS REPORT   ")
        print("="*30)
        print(f"FINAL SCORE: {result.get('score')}%")
        print("-" * 30)
        print("DETAILS:")
        print(f" • Keyword Match:  {round(result['details']['keyword_score'] * 100, 1)}%")
        print(f" • Semantic Match: {round(result['details']['semantic_score'] * 100, 1)}%")
        print("="*30)

    except Exception as e:
        print(f"Server Error: {e}")

if __name__ == "__main__":
    run_test()