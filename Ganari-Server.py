from fastapi import FastAPI
import uvicorn
import hashlib
import json

serv = FastAPI()

# Load users
with open("users.json", "r", encoding="utf-8") as fileusers: 
    usersfile = json.load(fileusers)

# Function for saving users.json file
def save_users_file(content):
    with open('users.json', 'w', encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Password verification
def password_hash_verify(entered_password_hash, user):
    stored_hash = usersfile.get(user, {}).get("password_hash", None)
    return stored_hash == entered_password_hash if stored_hash else False

@serv.get("/")
def home():
    return {"msg": "test"}

@serv.post("/send_msg")
def send_msg(password_hash: str, user: str, msg_for_user: str, to_user: str):
    if password_hash_verify(password_hash, user):
        # Create chats for sender and receiver
        if to_user not in usersfile[user]["msgs"]:
            usersfile[user]["msgs"][to_user] = []
        if user not in usersfile[to_user]["msgs"]:
            usersfile[to_user]["msgs"][user] = []

        # Add a message to both chat rooms
        usersfile[user]["msgs"][to_user].append(f"{user}: {msg_for_user}")  # Message from the sender
        usersfile[to_user]["msgs"][user].append(f"{user}: {msg_for_user}")  # Message to the recipient

        save_users_file(usersfile)
        return {"details": "success"}
    else:
        return {"details": "no", "reason": "invalid password"}

@serv.get("/get_msgs")
def get_msgs(password_hash: str, user: str, to_user: str):
    if password_hash_verify(password_hash, user):
        return usersfile[user]["msgs"][to_user]
    else:
        return {"details": "no", "reason": "invalid password"}


if __name__ == "__main__":
    uvicorn.run(serv, host="127.0.0.1", port=8080)
