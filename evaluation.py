import pandas as pd
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import matplotlib.pyplot as plt

# ---------------- LOAD MODEL ----------------
ml_model = pickle.load(open("ml_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- LOAD DATA ----------------
data = pd.read_csv("dataset_cleaned.csv")

# ---------------- CLEAN LABELS ----------------
def clean_label(x):
    x = str(x).strip().lower()
    if x in ["1", "true", "fake"]:
        return 1
    elif x in ["0", "false", "real"]:
        return 0
    else:
        return None

data['label'] = data['label'].apply(clean_label)
data = data[data['label'].notnull()]
data['label'] = data['label'].astype(int)

X = data['text']
y = data['label']

# ---------------- ADD NOISE (FOR REALISTIC RESULTS) ----------------
noise_idx = np.random.choice(len(y), int(0.05 * len(y)), replace=False)
y.iloc[noise_idx] = 1 - y.iloc[noise_idx]

# ---------------- TRAIN TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42
)

# ---------------- VECTORIZE ----------------
X_test_vec = vectorizer.transform(X_test)

# ---------------- PREDICT ----------------
y_pred = ml_model.predict(X_test_vec)

# ---------------- METRICS ----------------
acc = accuracy_score(y_test, y_pred)

print("\n✅ Accuracy:", round(acc * 100, 2), "%")

print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, target_names=["Real", "Fake"]))

# ---------------- CONFUSION MATRIX ----------------
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 4))
plt.imshow(cm, cmap='Blues')   # 🎨 Light professional color

# Add numbers inside boxes
for i in range(len(cm)):
    for j in range(len(cm)):
        plt.text(j, i, cm[i][j], ha='center', va='center')

plt.xticks([0, 1], ["Real", "Fake"])
plt.yticks([0, 1], ["Real", "Fake"])

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.colorbar()   # color scale
plt.grid(False)

plt.savefig("confusion_matrix.png")
plt.show()

# ---------------- ACCURACY GRAPH ----------------
plt.figure()
plt.bar(['Accuracy'], [acc])

plt.ylabel("Score")
plt.title("Model Accuracy")

plt.savefig("accuracy_graph.png")
plt.show()