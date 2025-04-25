import streamlit as st
from scrape import scrape_website,split_dom_content,clean_body_content,extract_boby_content
from parse import parse_with_gemini
import subprocess
import streamlit as st

try:
    version = subprocess.check_output(['google-chrome', '--version']).decode('utf-8')
    st.write(f"Chrome version: {version}")
except Exception as e:
    st.write(f"Could not get Chrome version: {e}")

if "user_db" not in st.session_state:
    st.session_state.user_db = {}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""
if 'page' not in st.session_state:
    st.session_state.page = 'create_account'

def switch_page(page):
    st.session_state.page = page
    st.rerun()

st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #c3ecb2, #7dd87d);
            padding: 20px;
            border-radius: 10px;
            max-width: 500px;
            margin: auto;
            color: #333;
            font-family: 'Poppins', sans-serif;
        }
        input, div.stButton>button {
            border-radius: 8px !important;
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Create Account Page
# -------------------------------
def create_account_page():
    user_db = st.session_state.user_db
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.header("🌱 Create Account")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if not full_name or not email or not password:
            st.warning("Please fill in all fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        elif email in user_db:
            st.error("Email already registered.")
        else:
            user_db[email] = {'name': full_name, 'password': password}
            st.success("Account created successfully! You can now log in.")
            switch_page("login")

    st.markdown("Already have an account? [Login](#)", unsafe_allow_html=True)
    if st.button("Go to Login"):
        switch_page("login")
    st.markdown("</div>", unsafe_allow_html=True)
def login_page():
    user_db = st.session_state.user_db
    st.markdown("<div class='main'>", unsafe_allow_html=True)
    st.header("🔐 Login")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if email in user_db and user_db[email]['password'] == password:
            st.success(f"Welcome back, {user_db[email]['name']}!")
            st.session_state.logged_in = True
            st.session_state.current_user = email
            switch_page("welcome")
        else:
            st.error("Invalid email or password.")

    st.markdown("Don't have an account? [Create one](#)", unsafe_allow_html=True)
    if st.button("Go to Create Account"):
        switch_page("create_account")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# AI Web Scraper (Welcome Page)
# -------------------------------
def welcome_page():
    user_db = st.session_state.user_db
    if not st.session_state.logged_in:
        st.warning("You must be logged in to view this page.")
        switch_page("login")
        return

    st.markdown("<div class='main'>", unsafe_allow_html=True)
    user_name = user_db[st.session_state.current_user]['name']
    st.title("🧠 AI Web Scraper for Data Science Students")
    st.write(f"Welcome, **{user_name}**!")

    # Step 1: Enter URL
    url = st.text_input("Enter site's URL:")
    if st.button("Scrape site"):
        if url:
            st.write("🔍 Scraping...")
            try:
                result = scrape_website(url)
                body_content = extract_boby_content(result)
                cleaned_content = clean_body_content(body_content)
                st.session_state.dom_content = cleaned_content

                with st.expander("🧾 View Cleaned DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            except Exception as e:
                st.error(f"❌ Error scraping site: {e}")
        else:
            st.warning("Please enter a valid URL.")

    # Step 2: Ask what to parse
    if "dom_content" in st.session_state:
        parse_description = st.text_area("Describe what you want to parse:")
        if st.button("Parse content"):
            if parse_description:
                st.write("🤖 Parsing the content...")
                try:
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    result = parse_with_gemini(dom_chunks, parse_description)
                    st.write("✅ **Result:**")
                    st.write(result)
                except Exception as e:
                    st.error(f"❌ Parsing failed: {e}")
            else:
                st.warning("Please enter a description to parse.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        switch_page("login")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# 🧭 Page Routing
# -------------------------------
if st.session_state.page == "create_account":
    create_account_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "welcome":
    welcome_page()
else:
    st.write("404: Page not found.")
    
#-----------------
#         or
#------------------
# st.title("AI Web Scraper for Data Science Students")
# url=st.text_input("Enter sites URL: ")
# if st.button("Srape site"):
#     st.write("Scrapping...")
#     result=scrape_website(url)
#     body_content=extract_boby_content(result)
#     cleaned_cotent=clean_body_content(body_content)
#     st.session_state.dom_content = cleaned_cotent
    
#     with st.expander("View DOM Content"):
#         st.text_area("Dom Content",cleaned_cotent,height=300)

# if "dom_content" in st.session_state:
#     parse_description=st.text_area("Describe what you want to parse?")
#     if st.button("Parse content"):
#         if parse_description:
#             st.write("Parsing the content....")
#             dom_chunks=split_dom_content(st.session_state.dom_content)
#             result= parse_with_gemini(dom_chunks,parse_description)
#             st.write(result)
