import os
import streamlit as st

from database import init_db
from auth import register_user, login_user
from payments import submit_payment_request, get_user_payment_status, is_user_unlocked
from admin import list_pending_payments
from payments import approve_payment, reject_payment
from utils import read_yaml_safely

init_db()

st.set_page_config(page_title="Premium Learning Dashboard", layout="wide")

# ------------------ Session init ------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ------------------ Helper ------------------
def show_video(youtube_id):
    st.components.v1.iframe(
        f"https://www.youtube.com/embed/{youtube_id}",
        height=420
    )

def logout():
    st.session_state.user = None
    st.rerun()

# ------------------ Login/Register UI ------------------
if not st.session_state.user:
    st.title("🔐 Learning Dashboard Premium")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            ok, result = login_user(username, password)
            if ok:
                st.session_state.user = result
                st.success("✅ Login success")
                st.rerun()
            else:
                st.error(result)

    with tab2:
        name = st.text_input("Name")
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")
        if st.button("Register", use_container_width=True):
            ok, msg = register_user(name, username, password)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

    st.stop()

# ------------------ Logged in ------------------
user = st.session_state.user

st.sidebar.success(f"👋 Welcome {user['name']}")
if st.sidebar.button("Logout"):
    logout()

# ------------------ Main Tabs ------------------
main_tabs = st.tabs(["📚 Dashboard", "💳 Subscription", "🛠 Admin"])

# ==================================================
# DASHBOARD
# ==================================================
with main_tabs[0]:
    st.title("📚 Learning Dashboard")

    # 4 subject tabs
    dash_tabs = st.tabs(["C++", "DevOps", "SRE", "Linux"])

    data = read_yaml_safely("resources.yaml")
    all_resources = data.get("resources", [])

    def render_resources(domain):
        unlocked = is_user_unlocked(user["id"])

        items = [r for r in all_resources if r.get("domain") == domain]
        if not items:
            st.info("No resources found")
            return

        for r in items:
            with st.container(border=True):
                st.subheader(r["title"])
                st.caption(r.get("description", ""))

                # Locked video
                if r.get("locked", False) and not unlocked:
                    st.warning("🔒 Locked — Subscribe to unlock")
                else:
                    if r.get("type") == "video":
                        show_video(r["youtube_id"])
                    else:
                        st.link_button("Open Resource", r.get("url", "#"))

    with dash_tabs[0]:
        render_resources("cpp")
    with dash_tabs[1]:
        render_resources("devops")
    with dash_tabs[2]:
        render_resources("sre")
    with dash_tabs[3]:
        render_resources("linux")

# ==================================================
# SUBSCRIPTION TAB (QR + upload proof)
# ==================================================
with main_tabs[1]:
    st.title("💳 Subscription (₹599 / ₹5999)")
    st.write("Pay subscription and upload payment screenshot. Admin will approve.")

    if is_user_unlocked(user["id"]):
        st.success("✅ Subscription Active — Dashboard Unlocked")
    else:
        st.warning("🔒 Locked — Upload payment proof after paying")

        # show QR
        qr_path = "uploads/qr.png"
        if os.path.exists(qr_path):
            st.image(qr_path, caption="Scan QR and Pay")
        else:
            st.info("Admin needs to upload QR file to uploads/qr.png")

        proof = st.file_uploader("Upload payment screenshot (PNG/JPG)", type=["png", "jpg", "jpeg"])
        if proof and st.button("Submit Proof"):
            ok, msg = submit_payment_request(user["id"], proof)
            if ok:
                st.success(msg)
            else:
                st.error(msg)

        status = get_user_payment_status(user["id"])
        if status:
            st.info(f"Current Payment Status: **{status['status']}**")

# ==================================================
# ADMIN TAB
# ==================================================
with main_tabs[2]:
    if user.get("role") != "admin":
        st.error("❌ You are not admin.")
    else:
        st.title("🛠 Admin Approval Panel")

        pending = list_pending_payments()
        if not pending:
            st.success("✅ No pending payments.")
        else:
            for p in pending:
                with st.container(border=True):
                    st.subheader(f"User: {p['username']} ({p['name']})")

                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.image(p["screenshot_path"], caption="Payment Proof")
                    with col2:
                        if st.button("✅ Approve", key=f"approve_{p['id']}"):
                            approve_payment(p["id"], txn_id="MANUAL_APPROVAL")
                            st.success("Approved")
                            st.rerun()
                    with col3:
                        if st.button("❌ Reject", key=f"reject_{p['id']}"):
                            reject_payment(p["id"])
                            st.warning("Rejected")
                            st.rerun()
