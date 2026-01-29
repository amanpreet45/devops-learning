import streamlit as st
import database
import auth_logic
import payments
import admin
from utils import read_yaml_safely

database.init_db()

if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    if not st.session_state.user:
        st.title("DevOps Learning Portal")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Login"):
                user = auth_logic.authenticate(u, p)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else: st.error("Invalid Login")
        with tab2:
            n = st.text_input("Full Name")
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.button("Register"):
                s, m = auth_logic.register_user(n, nu, np)
                if s: st.success(m)
                else: st.error(m)
    else:
        st.sidebar.title(f"Hi, {st.session_state.user['name']}")
        page = st.sidebar.radio("Menu", ["Dashboard", "Resources", "Admin Panel"])
        
        if page == "Dashboard":
            st.title("My Status")
            stat = payments.get_user_payment_status(st.session_state.user['id'])
            if not stat:
                st.warning("Upload receipt to gain access.")
                st.image("qr.png", width=250)
                up = st.file_uploader("Screenshot", type=['png','jpg'])
                if up and st.button("Submit"):
                    payments.submit_payment_request(st.session_state.user['id'], up)
                    st.rerun()
            else:
                st.info(f"Status: {stat['status'].upper()}")
        
        elif page == "Resources":
            stat = payments.get_user_payment_status(st.session_state.user['id'])
            if stat and stat['status'] == 'approved':
                data = read_yaml_safely()
                st.title("📚 Course Content")
                st.write(data)
            else: st.error("Access Locked.")

        elif page == "Admin Panel" and st.session_state.user['role'] == 'admin':
            st.title("Review Payments")
            pending = admin.list_pending_payments()
            for p in pending:
                st.write(f"User: {p['username']}")
                st.image(p['screenshot_path'], width=300)
                if st.button(f"Approve {p['payment_id']}"):
                    admin.approve_payment(p['payment_id'], True)
                    st.rerun()

if __name__ == "__main__":
    main()