from src.scoring.ats_scoring import compute_ats_score

def test_simple():
    resume = "Python developer with experience in flask, docker, aws"
    jd = "Looking for a python developer with flask and aws experience"
    keywords = jd.split()
    score, details = compute_ats_score(resume, keywords)
    assert score > 50