import streamlit as st
import os
import time
import sys
import json


# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NoteHIVE | Dashboard",
    layout="wide"
)

# --- AUTHENTICATION GUARD ---
# This is the most critical part of a secure dashboard.
# It checks if the 'logged_in' status is True in the session state. If not, it redirects the user to the login page.
if not st.session_state.get('logged_in', False):
    st.error("You are not logged in. Please log in to access the dashboard.")
    time.sleep(1.5)
    st.switch_page("pages/login.py")

#extracting function from ai_processor.py
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
backend_path = os.path.join(project_root, 'backend')
sys.path.append(backend_path)

from ai_processor import extract_text_from_pdf , summarize


# --- STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display.swap');

    body {
        font-family: 'Poppins', sans-serif;
        background-color: #F0F2F6;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 1rem; /* Reduced top padding */
    }
            
    /* Reduces the top padding of the page */
    .block-container {
        padding-top: 1.5rem;
        padding-left:1rem;
        padding-right:1rem;
    }

    /* Custom styling for the top container */
    .top-section {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }

            
    /* Styling for buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 10px 24px; /* Adjusted padding */
        font-weight: 600;
        transition: background-color 0.3s ease;
        /* width: 100%; Removed to stop buttons from stretching */
    }
    
    /* Primary button style */
    .stButton > button[kind="primary"] {
        background-color: #FF4B4B;
        color: white;
        border: none;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #E03C3C;
    }

    /* Secondary button style */
    .stButton > button[kind="secondary"] {
        background-color: #E0E0E0;
        color: #333333;
        border: 1px solid #CCCCCC;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #D3D3D3;
    }
    
    /* Styling for the folder containers */
    .folder-container {
        background: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.2s ease-in-out;
        min-height: 120px; /* Ensures folders have a consistent height */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
            
    .folder-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
            
    .folder-container:hover {
        transform: translateY(-5px);
    }

    /* Custom class for the logout button */
    .logout-button .stButton > button {
        width: 100%; /* Make button fill its column */
        padding: 8px 8px; /* Adjust padding as needed */

    }
    
</style>
""", unsafe_allow_html=True)

# --- HEADER, WELCOME MESSAGE, AND LOGOUT BUTTON ---
title_col, logout_col = st.columns([10, 1])

with title_col:
    # Get username from session state, with a fallback
    username = st.session_state.get('username', 'User')
    st.title(f"Welcome to Your Dashboard, {username}!")
    st.write("Upload a PDF to generate a summary, or browse your stored notes below.")

with logout_col:
    st.write("") # Spacer for vertical alignment
    st.markdown('<div class="logout-button">', unsafe_allow_html=True)
    if st.button("Logout", type="secondary"):
        #------END THE SESSION-------
        # Clear all session state variables
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        time.sleep(1)
        st.switch_page("pages/landing.py")
    st.markdown('</div>', unsafe_allow_html=True)


# --- TOP SECTION: PDF UPLOADER AND ACTIONS ---
with st.container():

    st.subheader("Summarize a New Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    # Use columns to place buttons next to each other, with empty space to the right
    col1, col2, col3 = st.columns([1.2, 1.5, 4])
    with col1:
        generate_button = st.button("Generate Summary", type="secondary")
    
    with col2:
        store_button = st.button("Store & Summarize", type="primary")

   # This logic block runs if either button is clicked and a file is uploaded
    if generate_button and uploaded_file is not None:
        with st.spinner('Extracting text from PDF...'):
            # 1. Call the backend function to get the text
            pdf_text = extract_text_from_pdf(uploaded_file)
            
            # 2. Call the Gemini API via our backend function
            # It securely accesses the API key from the .streamlit/secrets.toml file
            api_key = st.secrets["GOOGLE_API_KEY"]
         # The function now returns a dictionary of data instead of just text
            response_data, error = summarize(pdf_text, api_key)

            if error:
                st.error(error)
            else:
                # 3. Extract the subject and summary from the response dictionary
                #    We use .get() to safely access the keys, providing a default value if one is missing.
                subject = response_data.get("subject", "Unknown")
                summary = response_data.get("summary", "No summary could be generated.")

                st.success("Analysis Complete!")
                
                # 4. Display both pieces of information to the user
                st.subheader(f"Identified Subject: {subject}")
                st.text_area("Generated Summary", summary, height=200)

                if store_button:
                    # This placeholder logic now has access to the identified subject
                    st.info(f"PDF and summary are ready to be stored under the '{subject}' folder.")
    st.markdown('</div>', unsafe_allow_html=True)


# --- BOTTOM SECTION: SUBJECT FOLDERS ---
st.header("Your Stored Notes")
st.write("Click on a folder to view the PDFs stored inside.")

# --- Placeholder for Dynamic Folder Creation ---
subjects = ["Physics", "History", "Computer Science", "Biology", "Literature"]

# Display folders in a grid layout
num_columns = 4
cols = st.columns(num_columns)

for i, subject in enumerate(subjects):
    with cols[i % num_columns]:
        st.markdown(f"""
            <div class="folder-container">
                <div class="folder-icon">📁</div>
                <h4>{subject}</h4>
            </div>
        """, unsafe_allow_html=True)
        # In a real app, clicking this would lead to another page or expand to show files.
        # For example: if st.button(subject): st.switch_page(...)

