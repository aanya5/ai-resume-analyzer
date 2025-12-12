# placeholder file — kept for extensibility (e.g., sentence-transformers)
def semantic_similarity_placeholder(a: str, b: str) -> float:
    # Very naive
    if not a or not b:
        return 0.0
    set_a = set(a.lower().split())
    set_b = set(b.lower().split())
    intersect = set_a.intersection(set_b)
    return len(intersect) / max(1, min(len(set_a), len(set_b)))