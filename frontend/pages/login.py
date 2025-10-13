import streamlit as st
import time
import os
import sys

# --- Path logic to find the backend folder ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
backend_path = os.path.join(project_root, 'backend')
sys.path.append(backend_path)

# Import the new verification function
from signupDb import verify_user


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NoteHIVE | Login",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLING (Same as Signup Page for consistency) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display.swap');

    body {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background-color: #F0F2F6;
    }

    .main .block-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    [data-testid="stForm"] {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 2rem 3rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .stTextInput input {
        border-radius: 10px;
        border: 1px solid #ced4da;
        background-color: #FFFFFF;
        color: #495057;
    }
    
    ::placeholder {
        color: #6c757d !important;
    }

    h1, h2, h3, h4, h5, h6, p, .stMarkdown {
        color: #212529;
    }
    
    [data-testid="stForm"] .stButton > button {
        background: #FF4B4B;
        color: white;
        border-radius: 15px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    
    [data-testid="stForm"] .stButton > button:hover {
        background: #E03C3C;
    }
    
    a {
        color: #FF4B4B;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }

    #MainMenu, .stHeader, footer {
        visibility: hidden;
    }
    
</style>
""", unsafe_allow_html=True)


# --- LAYOUT ---
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown("<h1 style='font-size: 3.5rem; font-weight: 600;'>Welcome Back! </h1>", unsafe_allow_html=True)
    st.markdown("### Log in to access your dashboard, manage your notes, and continue your journey with NoteHIVE.")
    st.markdown("Ready to get back to productivity?")

with right_col:
    # --- LOGIN FORM ---
    with st.form("login_form"):
        st.subheader("Login to Your Account")

        # Input fields
        st.markdown("** Email or Username**")
        username_or_email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed")
        
        st.markdown("** Password**")
        password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
        
        # # 'Forgot Password?' and 'Remember Me' in one row
        # form_row1, form_row2 = st.columns([1.5, 1])
        # with form_row1:
        #     st.checkbox("Remember Me")
        # with form_row2:
        #     st.markdown('<div style="text-align: right;"><a href="#" target="_self">Forgot Password?</a></div>', unsafe_allow_html=True)

        # Submit button
        submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            if not username_or_email or not password:
                st.warning("⚠️ Please fill out all fields.")
            else:
                # Call the verification function from the backend
                success, result = verify_user(username_or_email, password)
                
                if success:
                    # --- START THE SESSION ---
                    # On successful login, store user info in the session state
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = result['id']
                    st.session_state['username'] = result['username']
                    
                    st.success("Login Successful! Redirecting...")
                    st.balloons()
                    # Redirect to the user's dashboard
                    st.switch_page("pages/dashboard.py")
                else:
                    # Display the error message from the backend
                    st.error(f"{result}")

    # Link to signup page
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            Don't have an account? <a href="/signup" target="_self">Sign Up</a>
        </div>
    """, unsafe_allow_html=True)