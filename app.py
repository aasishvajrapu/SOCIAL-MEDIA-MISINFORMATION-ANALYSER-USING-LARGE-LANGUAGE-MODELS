from flask import Flask, render_template, request, redirect, session
from analyzer import analyze_content
import json

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- USERS ----------------
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# ---------------- STATS ----------------
def load_stats():
    try:
        with open("stats.json", "r") as f:
            return json.load(f)
    except:
        return {"fake": 0, "real": 0, "manipulative": 0}

def save_stats(stats):
    with open("stats.json", "w") as f:
        json.dump(stats, f)

# ---------------- ROUTES ----------------

@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    result = None
    user_input = ""

    if request.method == "POST":
        text = request.form.get("content")
        user_input = text

        # OCR
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != "":
                from ocr import extract_text_from_image
                text = extract_text_from_image(image)
                user_input = text

        if not text or text.strip() == "":
            result = {
                "label": "No Input Provided",
                "confidence": 0,
                "tone": "N/A",
                "post_type": "N/A",
                "credibility": 0,
                "verification": "No input",
                "highlighted": "",
                "refined_text": ""
            }
        else:
            # ✅ ANALYZE CONTENT
            result = analyze_content(text)

            # 📊 UPDATE STATS
            stats = load_stats()

            if "Fake" in result["label"]:
                stats["fake"] += 1
            else:
                stats["real"] += 1

            if "Manipulative" in result["tone"]:
                stats["manipulative"] += 1

            save_stats(stats)

    return render_template(
        "home.html",
        result=result,
        user_input=user_input
    )


@app.route("/dashboard")
def dashboard():
    stats = load_stats()
    return render_template("dashboard.html", data=stats)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        users = load_users()
        username = request.form.get("username")
        password = request.form.get("password")

        users[username] = password
        save_users(users)

        return redirect("/login")

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)