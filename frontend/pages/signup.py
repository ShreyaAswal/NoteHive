import streamlit as st
import re
import sys
import os

# This code navigates up two levels from the current file (signup.py) to the project root (Notehive),
# then constructs the correct path to the 'backend' folder.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
backend_path = os.path.join(project_root, 'backend')
sys.path.append(backend_path) #list of all folders python will search whenever we import a file i.e it will search in backend folder
 
# Now, import the function from your signupDb.py file 
from signupDb import add_user


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NoteHIVE | Signup",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLING ---
st.markdown("""
<style>
    /* Import a modern font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* General body styling */
    body {
        font-family: 'Poppins', sans-serif;
    }
    
    /* --- MODIFIED SECTION START --- */

    /* 1. PAGE BACKGROUND */
    .stApp {
        background-color: #F0F2F6; /* Subtle light grey background */
    }

    /* Center the main content vertically */
    .main .block-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    /* 2. FORM CONTAINER */
    [data-testid="stForm"] {
        background: #FFFFFF; /* Clean white background */
        border-radius: 20px;
        padding: 2rem 3rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1); /* Shadow to make it "float" */
        border: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    /* 3. TEXT & INPUTS */
    /* Style for text inputs */
    .stTextInput input {
        border-radius: 10px;
        border: 1px solid #ced4da; /* Standard input border color */
        background-color: #FFFFFF;
        color: #495057; /* Dark text color */
    }
    
    /* Style for placeholders */
    ::placeholder {
        color: #6c757d !important;
    }

    /* Custom styling for all text */
    h1, h2, h3, h4, h5, h6, p, .stMarkdown {
        color: #212529; /* Dark text for readability */
    }
    
    /* 4. BUTTONS & LINKS */
    /* Styling for the submit button */
    [data-testid="stForm"] .stButton > button {
        background: #FF4B4B; /* Re-using the brand's primary red */
        color: white;
        border-radius: 15px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }
    
    [data-testid="stForm"] .stButton > button:hover {
        background: #E03C3C; /* Darker red on hover */
    }
    
    /* Link styling */
    a {
        color: #FF4B4B; /* Brand red for links */
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }

    /* --- MODIFIED SECTION END --- */
    
    /* Hide the default Streamlit header, footer, and toolbar for a cleaner look */
    #MainMenu, .stHeader, footer {
        visibility: hidden;
    }
    
</style>
""", unsafe_allow_html=True)


# --- LAYOUT ---
# Using a two-column layout for a modern look
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown("<h1 style='font-size: 3.5rem; font-weight: 600;'>Welcome to NoteHIVE </h1>", unsafe_allow_html=True)
    st.markdown("### Your new hub for capturing ideas, organizing notes, and boosting productivity.")
    st.markdown("Join thousands of users who are transforming their workflow. Sign up now to get started!")

with right_col:
    # --- SIGNUP FORM ---
    with st.form("signup_form"):
        st.subheader("Create a New Account")

        # Input fields with custom labels and icons
        st.markdown("**✉️ Email**")
        email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed")
        
        st.markdown("**👤 Username**")
        username = st.text_input("Username", placeholder="Choose a unique username", label_visibility="collapsed")
        
        st.markdown("**🔑 Password**")
        password = st.text_input("Password", type="password", placeholder="Create a strong password", label_visibility="collapsed")
        
        st.markdown("**🔑 Confirm Password**")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", label_visibility="collapsed")

        # Submit button
        submitted = st.form_submit_button("Sign Up", use_container_width=True)

        if submitted:
            is_valid = True
            if not email or not username or not password or not confirm_password:
                st.error("⚠️ Please fill out all fields.")
                is_valid = False
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("📧 Please enter a valid email address.")
                is_valid = False
            elif password != confirm_password:
                st.error("🔑 Passwords do not match.")
                is_valid = False
            elif len(password) < 8:
                st.error("🔒 Password must be at least 8 characters long.")
                is_valid = False

            if is_valid:
                success, message = add_user(username, email, password)
            
                if success:
                    st.success(f"✅ {message} You can now log in.")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")


    # Link to login page
    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            Already have an account? <a href="/login" target="_self">Log In</a>
        </div>
    """, unsafe_allow_html=True)