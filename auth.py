import json
import os

USER_FILE = "users.json"

# Create file if not exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def authenticate(username, password):
    users = load_users()
    return username in users and users[username] == password

def register_user(username, password):
    users = load_users()

    if username in users:
        return False  # already exists

    users[username] = password
    save_users(users)
    return True