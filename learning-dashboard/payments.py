def mark_payment_approved(user_id: int, txn_id: str = ""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM payments WHERE user_id=?", (user_id,))
    row = cur.fetchone()

    if row:
        cur.execute("""
            UPDATE payments
            SET status='approved', txn_id=?, updated_at=?
            WHERE user_id=?
        """, (txn_id, now_str(), user_id))
    else:
        cur.execute("""
            INSERT INTO payments (user_id, status, txn_id, screenshot_path, created_at, updated_at)
            VALUES (?, 'approved', ?, '', ?, ?)
        """, (user_id, txn_id, now_str(), now_str()))

    conn.commit()
    conn.close()

from database import get_conn

def is_user_unlocked(user_id: int) -> bool:
    """
    Returns True if user has an approved payment.
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT status
        FROM payments
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    # row can be dict (sqlite row_factory) OR tuple
    status = row["status"] if isinstance(row, dict) or hasattr(row, "keys") else row[0]
    return status == "approved"
