# Very simple keyword extractor: lowercases, splits on nonalpha, returns top N frequent words excluding stopwords
import re
from collections import Counter

STOPWORDS = {
    "and","or","the","to","of","in","on","for","with","a","an","is","are","be","by","that","this","as","at"
}

def tokenize(text: str):
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 2]

def extract_keywords_from_jd(text: str, top_k: int = 20):
    tokens = tokenize(text)
    counts = Counter(tokens)
    return [w for w,_ in counts.most_common(top_k)]