from database import init_db, get_conn
from utils import hash_password, now_str

def create_initial_admin():
    # Initialize DB and create folders
    init_db()
    
    conn = get_conn()
    cur = conn.cursor()
    
    # Configuration for your admin account
    admin_name = "Amanpreet"
    admin_user = "admin"
    admin_pass = "admin123" # Change this after first login
    hashed = hash_password(admin_pass)
    
    try:
        cur.execute("""
            INSERT INTO users (name, username, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (admin_name, admin_user, hashed, 'admin', now_str()))
        conn.commit()
        print(f"✅ Admin account created successfully!")
        print(f"Username: {admin_user}")
        print(f"Password: {admin_pass}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Note: If the error says 'UNIQUE constraint failed', the admin already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_initial_admin()