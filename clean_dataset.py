import pandas as pd

df = pd.read_csv("dataset_cleaned.csv")  # your current dataset

# ---------------- FIX LABELS ----------------
def clean_label(x):
    x = str(x).strip().lower()

    if x == "fake":
        return 1
    elif x == "real":
        return 0
    else:
        return None

df["label"] = df["label"].apply(clean_label)

# Remove invalid rows
df = df[df["label"].notnull()]

# Convert type
df["label"] = df["label"].astype(int)

# Save again
df.to_csv("dataset_cleaned.csv", index=False)

print("✅ Dataset fixed!")
print("Rows:", len(df))
print("Labels:", df["label"].value_counts())