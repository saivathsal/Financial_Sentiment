import streamlit as st
from auth import  auth_section
from dashboard import sentiment_dashboard

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if __name__ == "__main__":
    if st.session_state.logged_in:
        sentiment_dashboard()
    else:
        auth_section()
