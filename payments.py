import os
import time
from database import get_conn
from utils import now_str, ensure_dir

UPLOAD_DIR = "uploads"

def submit_payment_request(user_id: int, uploaded_file):
    ensure_dir(UPLOAD_DIR)
    filename = f"user_{user_id}_{int(time.time())}_{uploaded_file.name}"
    save_path = os.path.join(UPLOAD_DIR, filename)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO payments (user_id, screenshot_path, status, created_at, updated_at)
        VALUES (?, ?, 'pending', ?, ?)
    """, (user_id, save_path, now_str(), now_str()))
    conn.commit()
    conn.close()
    return True

def get_user_payment_status(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT status, screenshot_path, created_at, updated_at, admin_note 
        FROM payments WHERE user_id=? ORDER BY id DESC LIMIT 1
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None