from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def bert_analyze(text):
    result = classifier(text[:512])[0]
    label = result['label']
    score = result['score']

    text_lower = text.lower()

    # ---------------- SMART RULES ----------------

    # 🔥 Death / serious claim detection
    if any(phrase in text_lower for phrase in ["is dead", "has died", "death of"]):
        return "Fake / Misleading", 95.0

    # 🔥 Medical fake claims
    if any(phrase in text_lower for phrase in ["100% cure", "guaranteed cure", "miracle cure"]):
        return "Fake / Misleading", 92.0

    # 🔥 Clickbait patterns
    if any(word in text_lower for word in ["shocking", "secret", "won't believe"]):
        return "Fake / Misleading", 90.0

    # ---------------- SENTIMENT LOGIC ----------------

    if label == "NEGATIVE":
        prediction = "Fake / Misleading"
    else:
        prediction = "Real / Informative"

    return prediction, round(score * 100, 2)