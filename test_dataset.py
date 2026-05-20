import pandas as pd
from analyzer import analyze_content
from sklearn.metrics import confusion_matrix, accuracy_score
import matplotlib.pyplot as plt

# Load cleaned dataset
data = pd.read_csv("dataset_cleaned.csv")

y_true = []
y_pred = []

correct = 0
total = len(data)

print("\n🔍 Running Dataset Testing...\n")

for i, row in data.iterrows():
    text = str(row["text"])
    actual = row["label"]  # 0 or 1

    result = analyze_content(text)
    predicted = result['label']

    # Convert predicted to numeric
    predicted_num = 1 if predicted == "fake" else 0

    y_true.append(actual)
    y_pred.append(predicted_num)

    print("Text:", text[:100])
    print("Actual:", "Fake" if actual == 1 else "Real")
    print("Predicted:", predicted.capitalize())
    print("-" * 50)

    if predicted_num == actual:
        correct += 1

# ---------------- ACCURACY ----------------
accuracy = (correct / total) * 100

print("\n✅ Total Samples:", total)
print("✅ Correct Predictions:", correct)
print(f"🎯 Accuracy: {accuracy:.2f}%")

# ---------------- CONFUSION MATRIX ----------------
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(6, 4))
plt.imshow(cm)

for i in range(len(cm)):
    for j in range(len(cm)):
        plt.text(j, i, cm[i][j], ha='center', va='center')

plt.xticks([0, 1], ["Real", "Fake"])
plt.yticks([0, 1], ["Real", "Fake"])

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

plt.savefig("confusion_matrix.png")  # ✅ SAVES IMAGE
plt.show()

# ---------------- ACCURACY GRAPH ----------------
plt.figure()
plt.bar(['Accuracy'], [accuracy])

plt.ylabel("Percentage")
plt.title("Model Accuracy")

plt.savefig("accuracy_graph.png")  # ✅ SAVES IMAGE
plt.show()