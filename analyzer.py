import re
from bert_model import bert_analyze
from news_api import check_news

# ---------------- TEXT REFINEMENT ----------------
def refine_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s.,]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    words = text.split()
    words = [w for w in words if len(w) > 3]

    return " ".join(words[:30]).capitalize()


# ---------------- PATTERN DETECTION ----------------
def detect_fake_patterns(text):
    patterns = [
        "won't believe", "shocking", "breaking",
        "secret", "100% guaranteed", "doctors hate this",
        "click here", "limited time"
    ]

    return [p for p in patterns if p in text.lower()]


# ---------------- HIGHLIGHT ----------------
def highlight_text(text, patterns):
    for p in patterns:
        text = text.replace(
            p,
            f"<span class='highlight'>{p}</span>"
        )
    return text


# ---------------- MAIN ANALYZER ----------------
def analyze_content(text):

    # -------- EMPTY INPUT --------
    if not text or text.strip() == "":
        return {
            "label": "real",
            "confidence": 0,
            "credibility": 100,
            "patterns": [],
            "refined_text": "",
            "verification": "No input",
            "tone": "Neutral"
        }

    # -------- PREPROCESS --------
    refined = refine_text(text)

    # -------- MODEL --------
    label, confidence = bert_analyze(refined)
    label = "fake" if "fake" in label.lower() else "real"

    # -------- PATTERN DETECTION --------
    patterns = detect_fake_patterns(refined)

    # -------- TONE DETECTION --------
    if patterns:
        tone = "Manipulative"
    elif label == "fake":
        tone = "Suspicious"
    else:
        tone = "Informative"

    # -------- SCORING --------
    score = 0

    if label == "fake":
        score += 50

    if patterns:
        score += 30

    credibility = max(0, 100 - score)

    # -------- OUTPUT --------
    return {
        "label": label,
        "confidence": confidence,
        "credibility": credibility,
        "patterns": patterns,
        "refined_text": refined,
        "verification": check_news(refined),
        "tone": tone
    }