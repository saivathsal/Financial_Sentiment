import streamlit as st
from utils import create_user_table,get_user,add_user,check_password
def auth_section():
    create_user_table()
    if "menu" not in st.session_state:
        st.session_state.menu = "Login"
    menu = st.sidebar.selectbox("Menu", ["Login", "Signup"], key="menu")

    if menu == "Signup":
        st.title("Signup")
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        if st.button("Sign Up"):
            if not all([new_user, new_pass, confirm_pass]):
                st.warning("All fields required.")
            elif new_pass != confirm_pass:
                st.warning("Passwords do not match.")
            elif get_user(new_user):
                st.warning("Username already exists.")
            elif add_user(new_user, new_pass):
                st.session_state.logged_in = True
                st.session_state.user = new_user
                st.rerun()
            else:
                st.error("Signup failed.")

    else:
        st.title("Login") 
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = get_user(username)
            if user and check_password(password, user[1]):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials.")