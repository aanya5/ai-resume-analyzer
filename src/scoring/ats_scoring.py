# Builds a TF-IDF vectorizer on the JD keywords and checks resume overlap.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Tuple

def _semantic_score(resume_text: str, jd_keywords: List[str]) -> float:
    # If no keywords present, return 0. Use TF-IDF on small corpus [jd, resume]
    corpus = [" ".join(jd_keywords), resume_text]
    vect = TfidfVectorizer().fit_transform(corpus)
    sim = cosine_similarity(vect[0:1], vect[1:2])[0][0]
    return float(sim)

def _keyword_overlap_score(resume_text: str, jd_keywords: List[str]) -> float:
    rset = set(w.lower() for w in resume_text.split())
    if not jd_keywords:
        return 0.0
    found = sum(1 for k in jd_keywords if k.lower() in rset)
    return found / len(jd_keywords)

def compute_ats_score(resume_text: str, jd_keywords: List[str]) -> Tuple[float, dict]:
    kw_score = _keyword_overlap_score(resume_text, jd_keywords)
    sem_score = _semantic_score(resume_text, jd_keywords)
    # weighted sum (simple)
    score = 0.6 * kw_score + 0.4 * sem_score
    details = {"keyword_score": kw_score, "semantic_score": sem_score}
    final = round(float(score) * 100, 2)
    return final, details