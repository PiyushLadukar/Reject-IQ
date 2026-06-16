import json
import os
import hashlib

PATH = "data/users.json"

def load_users():
    if not os.path.exists(PATH):
        return []

    with open(PATH, "r") as f:
        return json.load(f)

def save_users(users):
    with open(PATH, "w") as f:
        json.dump(users, f, indent=4)

def encrypt(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password):

    users = load_users()

    for user in users:
        if user["username"] == username:
            return False

    users.append({
        "username": username,
        "password": encrypt(password)
    })

    save_users(users)

    return True

def login(username, password):

    users = load_users()

    password = encrypt(password)

    for user in users:
        if (
            user["username"] == username
            and
            user["password"] == password
        ):
            return True

    return False