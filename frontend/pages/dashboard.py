import streamlit as st
import os
import time
import sys
import json
import base64


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
from pdf_utils import create_summary_pdf,get_pdf_display


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

# --- Initialize session state variables ---
# We use these to remember the app's state across reruns.
if 'summary_data' not in st.session_state:
    st.session_state.summary_data = None
if 'show_store_form' not in st.session_state:
    st.session_state.show_store_form = False
if 'pdf_bytes_to_store' not in st.session_state:
    st.session_state.pdf_bytes_to_store = None


# --- TOP SECTION: PDF UPLOADER AND ACTIONS ---
with st.container():

    st.subheader("Summarize a New Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    # Use columns to place buttons next to each other, with empty space to the right
    col1, col2, col3 = st.columns([1.2, 1.5, 4])
    with col1:
        generate_button = st.button("Generate Summary", type="primary")

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
                st.session_state.summary_data = None
            else:
                st.session_state.summary_data = response_data
                #reset other data
                st.session_state.show_store_form = False 
                st.session_state.pdf_bytes_to_store = None


    # --- DISPLAY SUMMARY & "STORE" BUTTON ---
    # This block runs AFTER a summary has been generated and saved to the session state.
    if st.session_state.summary_data is not None:
        data = st.session_state.summary_data
        title = data.get("title", "No title generated.")
        summary = data.get("summary", "No summary generated.")

        st.success("Analysis Complete!")
        st.subheader(f"Identified Title: {title}")
        st.text_area("Generated Summary", summary, height=200)

        # Create the "Store" button, which will set another state variable
        if st.button("Store", type="secondary"):
            with st.spinner("Creating PDF document..."):

            # 1. Generate the PDF bytes
                pdf_bytes = create_summary_pdf(title, summary)
                # 2. Store the bytes in session state
                st.session_state.pdf_bytes_to_store = pdf_bytes
                # 3. Set the flag to show the form
                st.session_state.show_store_form = True
                st.rerun()

    
    # --- DISPLAY "STORE" FORM ---
    # This block runs AFTER the "Store" button has been clicked.
    if st.session_state.show_store_form:
        st.subheader("Store this summary")


        # --- DISPLAY THE PDF PREVIEW ---
        st.write("Preview of the summary PDF to be stored:")
        pdf_bytes = st.session_state.pdf_bytes_to_store
        if pdf_bytes:
            base64_pdf = get_pdf_display(pdf_bytes)
            pdf_display=f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)




        # Placeholder list of subjects (in a real app, you'd fetch this from the DB)
        subjects_placeholder = ["Physics", "History", "Computer Science", "Biology", "Literature", "create new subject"]

        with st.form("store_form"):
            selected_subject = st.selectbox(
                "Choose a folder to store this note:",
                options=subjects_placeholder
            )

            submit_store_button = st.form_submit_button("Submit")

            if submit_store_button:
                    st.success(f"summary stored successfully in :{selected_subject}")                
                    st.session_state.summary_data = None
                    st.session_state.show_store_form = False
                    time.sleep(2) # Show the success message for 2 seconds
                    st.rerun() # Rerun to hide the form and summary

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

