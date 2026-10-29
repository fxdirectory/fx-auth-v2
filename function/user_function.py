import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import query

def get_user_by_username(username):
    return query(
        "SELECT * FROM users WHERE username = %s",
        (username,), fetch_one=True,
    )

def get_user_by_token(token):
    return query(
        "SELECT * FROM users WHERE token = %s",
        (token,), fetch_one=True,
    )

def create_user(username, password, role="user"):
    row = query(
        "SELECT COUNT(*) AS c FROM users WHERE username = %s",
        (username,), fetch_one=True,
    )
    if row and row["c"] > 0:
        return None  # username sudah dipakai

    pw_hash = generate_password_hash(password)
    new_id = query(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
        (username, pw_hash, role),
    )
    if new_id is None:
        return None
    last = query("SELECT LAST_INSERT_ID() AS id", fetch_one=True)
    return last["id"] if last else None

def login_user(username, password):
    user = get_user_by_username(username)
    if not user or not check_password_hash(user["password"], password):
        return None

    token = secrets.token_hex(32)  # 64 karakter hex
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query(
        "UPDATE users SET token = %s, last_login = %s WHERE id = %s",
        (token, now, user["id"]),
    )
    user["token"] = token
    user["last_login"] = now
    return user


def public_user(user):
    data = dict(user)
    data.pop("password", None)
    for key in ("last_login", "created_at"):
        if isinstance(data.get(key), datetime):
            data[key] = data[key].strftime("%Y-%m-%d %H:%M:%S")
    return data


def logout_user(user_id):
    query("UPDATE users SET token = NULL WHERE id = %s", (user_id,))
