from database import get_conn
from utils import hash_password, verify_password, now_str

def register_user(name, username, password):
    conn = get_conn()
    cur = conn.cursor()
    try:
        pw_hash = hash_password(password)
        cur.execute("INSERT INTO users (name, username, password_hash, created_at) VALUES (?, ?, ?, ?)",
                    (name, username, pw_hash, now_str()))
        conn.commit()
        return True, "Registration successful!"
    except Exception:
        return False, "Username already exists."
    finally:
        conn.close()

def authenticate(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()
    conn.close()
    if user and verify_password(password, user['password_hash']):
        return dict(user)
    return None