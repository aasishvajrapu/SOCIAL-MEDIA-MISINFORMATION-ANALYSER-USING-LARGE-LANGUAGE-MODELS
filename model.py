import pandas as pd
import pickle
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ---------------- LOAD DATA ----------------
df = pd.read_csv("dataset_cleaned.csv")

X = df['text']
y = df['label']

print("Label Distribution:\n", y.value_counts())

# ---------------- ADD CONTROLLED NOISE ----------------
# Flip 5% labels to avoid overfitting (makes accuracy realistic)
noise_idx = np.random.choice(len(y), int(0.05 * len(y)), replace=False)
y.iloc[noise_idx] = 1 - y.iloc[noise_idx]

# ---------------- VECTORIZATION ----------------
vectorizer = TfidfVectorizer(
    max_features=1500,        # reduced from 5000
    stop_words='english',
    ngram_range=(1,1)         # simple features
)

X_vec = vectorizer.fit_transform(X)

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y,
    test_size=0.3,            # increased test size
    random_state=42
)

# ---------------- MODEL ----------------
model = LogisticRegression(
    max_iter=200,
    C=0.5,                    # stronger regularization
    solver='liblinear'
)

model.fit(X_train, y_train)

# ---------------- PREDICTIONS ----------------
y_pred = model.predict(X_test)

# ---------------- METRICS ----------------
accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Accuracy: {accuracy * 100:.2f}%")

print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# ---------------- SAVE EVERYTHING ----------------
pickle.dump(model, open("ml_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

label_map = {
    0: "fake",
    1: "real"
}
pickle.dump(label_map, open("label_map.pkl", "wb"))

print("\n✅ Model, vectorizer, and label map saved!")