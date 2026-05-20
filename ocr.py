import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def clean_text(text):
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', ' ', text)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)

    # Split into words
    words = text.split()

    # Keep meaningful words only
    filtered = []
    for w in words:
        if len(w) > 3:   # remove small garbage words
            filtered.append(w)

    # Join back
    cleaned = " ".join(filtered)

    return cleaned


def extract_text_from_image(file):
    try:
        image = Image.open(file)

        # Improve OCR quality
        image = image.convert("L")  # grayscale

        raw_text = pytesseract.image_to_string(image)

        cleaned = clean_text(raw_text)

        # LIMIT LENGTH (avoid long garbage)
        cleaned = " ".join(cleaned.split()[:40])

        return cleaned

    except:
        return ""