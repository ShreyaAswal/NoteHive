import streamlit as st
import os
import time
import sys
import base64

st.set_page_config(page_title="NoteHive | Dashboard", page_icon="🪶", layout="wide")

# --- PATH SETUP ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
backend_path = os.path.join(project_root, 'backend')
sys.path.append(backend_path)

from ai_processor import extract_text_from_pdf, summarize
from pdf_utils import create_summary_pdf, get_pdf_display


# --- AUTH GUARD ---
if not st.session_state.get('logged_in', False):
    st.error("You are not logged in. Please log in to access the dashboard.")
    time.sleep(1.5)
    st.switch_page("pages/login.py")

# --- STYLING ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

:root {
  --bg-light: #ffffff;
  --text-light: #0f172a;
  --bg-dark: #0f172a;
  --text-dark: #f1f5f9;
  --accent: #ffc107;
  --card-dark: #1e293b;
}

/* Smooth Transition */
body {
  transition: all 0.3s ease;
  font-family: 'Inter', sans-serif;
}
            
/* NAVBAR */
.navbar {
  position: sticky;
  top: 0;
  z-index: 999;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem 1rem 1rem; /* reduced left padding from 3rem → 1rem */
  background: var(--bg-light);
  color: var(--text-light);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  transition: all 0.3s ease;
}

.navbar.dark {
  background: var(--bg-dark);
  color: var(--text-dark);
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-left: 0; /* ensures it hugs the left edge */
}

.nav-buttons {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-buttons button {
  border: none;
  background: none;
  font-size: 1rem;
  color: inherit;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 500;
}

.nav-buttons button:hover {
  color: var(--accent);
}

.toggle-btn {
  background: var(--accent);
  color: black;
  border: none;
  border-radius: 20px;
  padding: 0.4rem 1rem;
  cursor: pointer;
  font-weight: 600;
  transition: 0.3s;
}

.toggle-btn:hover {
  opacity: 0.9;
}

/* Main container */
.main .block-container {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
/* --- HOW IT WORKS --- */
.how-section {
  text-align: center;
  margin-top: 4rem;
  padding: 3rem 2rem;
}
.steps {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin-top: 2rem;
}
.step {
  background: #ffffff;
  border-radius: 14px;
  padding: 2rem;
  width: 280px;
  box-shadow: 0 4px 14px rgba(0,0,0,0.06);
  transition: all 0.3s ease-in-out;
}
.step:hover {
  transform: translateY(-6px);
  box-shadow: 0 6px 18px rgba(0,0,0,0.1);
}
.step-icon {
  font-size: 2.5rem;
  color: var(--accent);
  margin-bottom: 1rem;
}

/* Buttons */
.stButton > button {
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    transition: background-color 0.3s ease;
}
.stButton > button[kind="primary"] {
    background-color: #2563eb;
    color: white;
    border: none;
}
.stButton > button[kind="primary"]:hover {
    background-color: #1e40af;
}
.stButton > button[kind="secondary"] {
    background-color: #e0e0e0;
    color: #333;
}
.stButton > button[kind="secondary"]:hover {
    background-color: #d4d4d4;
}

/* Folder cards */
.folder-container {
    background: #ffffff;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    text-align: center;
    transition: transform 0.2s ease-in-out;
    margin-bottom: 1.5rem;
}
.folder-container:hover {
    transform: translateY(-5px);
}
.folder-icon {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

/* --- FOOTER --- */
.footer {
  padding: 4rem 3rem 2rem;
  background: #0f172a;
  color: #f8fafc;
  margin-top: 5rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.footer-logo {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 0.5rem;
}

.footer h4 {
  font-weight: 600;
  color: #f1f5f9;
  margin-bottom: 0.75rem;
}

.footer a {
  color: #94a3b8;
  text-decoration: none;
  display: block;
  margin-bottom: 0.4rem;
  transition: 0.3s;
}

.footer a:hover {
  color: var(--accent);
}

.footer-bottom {
  text-align: center;
  border-top: 1px solid #334155;
  margin-top: 2rem;
  padding-top: 1.2rem;
  font-size: 0.9rem;
  color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)


# --- NAVBAR ---
st.markdown("""
<div class="navbar">
  <div class="logo">🪶 NoteHive</div>
  <div class="nav-buttons">
    <a href="/landing" target="_self"><button>Home</button></a>
    <a href="#how-it-works" target="_self"><button>How it Works</button></a>
    <a href="/signup" target="_self"><button>Signup</button></a>
    <a href="/landing" target="_self"><button>Logout</button></a>
  </div>
</div>
""", unsafe_allow_html=True)


# --- HEADER & LOGOUT ---
username = st.session_state.get('username', 'User')
st.title(f"Welcome to Your Dashboard, {username} 👋")
st.write("Upload a PDF to generate a summary, or browse your stored notes below.")


# --- SESSION INITIALIZATION ---
if 'summary_data' not in st.session_state:
    st.session_state.summary_data = None
if 'show_store_form' not in st.session_state:
    st.session_state.show_store_form = False
if 'pdf_bytes_to_store' not in st.session_state:
    st.session_state.pdf_bytes_to_store = None


# --- PDF UPLOADER ---
st.subheader("Summarize a New Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

col1, col2, _ = st.columns([1.2, 1.5, 4])
with col1:
    generate_button = st.button("Generate Summary", type="primary")

if generate_button and uploaded_file is not None:
    with st.spinner('Extracting text from PDF...'):
        pdf_text = extract_text_from_pdf(uploaded_file)
        api_key = st.secrets["GOOGLE_API_KEY"]
        response_data, error = summarize(pdf_text, api_key)

        if error:
            st.error(error)
            st.session_state.summary_data = None
        else:
            st.session_state.summary_data = response_data
            st.session_state.show_store_form = False
            st.session_state.pdf_bytes_to_store = None


# --- SHOW SUMMARY ---
if st.session_state.summary_data is not None:
    data = st.session_state.summary_data
    title = data.get("title", "No title generated.")
    summary = data.get("summary", "No summary generated.")

    st.success("Analysis Complete!")
    st.subheader(f"Identified Title: {title}")
    st.text_area("Generated Summary", summary, height=200)

    if st.button("Store", type="secondary"):
        with st.spinner("Creating PDF document..."):
            pdf_bytes = create_summary_pdf(title, summary)
            st.session_state.pdf_bytes_to_store = pdf_bytes
            st.session_state.show_store_form = True
            st.rerun()


# --- STORE FORM ---
if st.session_state.show_store_form:
    st.subheader("Store this summary")

    st.write("Preview of the summary PDF to be stored:")
    pdf_bytes = st.session_state.pdf_bytes_to_store
    if pdf_bytes:
        base64_pdf = get_pdf_display(pdf_bytes)
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="500" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    subjects_placeholder = ["Physics", "History", "Computer Science", "Biology", "Literature", "create new subject"]

    with st.form("store_form"):
        selected_subject = st.selectbox("Choose a folder to store this note:", options=subjects_placeholder)
        submit_store_button = st.form_submit_button("Submit")

        if submit_store_button:
            st.success(f"Summary stored successfully in: {selected_subject}")
            st.session_state.summary_data = None
            st.session_state.show_store_form = False
            time.sleep(2)
            st.rerun()


# --- STORED NOTES SECTION ---
st.header("Your Stored Notes")
st.write("Click on a folder to view the PDFs stored inside.")

subjects = ["Physics", "History", "Computer Science", "Biology", "Literature"]

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

# --- HOW IT WORKS SECTION ---
st.markdown("""
<div class="how-section" id="how-it-works">
  <h2>⚙️ How It Works</h2>
  <p>From upload to organized insights — your study flow made effortless.</p>
  <div class="steps">
    <div class="step">
      <div class="step-icon">📤</div>
      <h4>1. Upload</h4>
      <p>Choose your lecture notes, textbooks, or research papers in PDF format.</p>
    </div>
    <div class="step">
      <div class="step-icon">🤖</div>
      <h4>2. AI Summarize</h4>
      <p>Our AI extracts key topics, summaries, and insights automatically.</p>
    </div>
    <div class="step">
      <div class="step-icon">📂</div>
      <h4>3. Organize</h4>
      <p>Summaries are auto-categorized by subject — easy to browse anytime.</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# --- FOOTER (Same as Landing Page) ---
st.markdown("""
<footer class="footer">
  <div class="footer-grid">
    <div>
      <div class="footer-logo">🪶 NoteHive</div>
      <p>Smarter studying, simplified. Create, summarize, and organize your notes effortlessly with AI.</p>
    </div>
    <div>
      <h4>Explore</h4>
      <a href="#features">Features</a>
      <a href="#how-it-works">How It Works</a>
      <a href="#faq">FAQ</a>
    </div>
    <div>
      <h4>Company</h4>
      <a href="#">About Us</a>
      <a href="#">Privacy Policy</a>
      <a href="#">Terms of Service</a>
    </div>
    <div>
      <h4>Connect</h4>
      <a href="#">LinkedIn</a>
      <a href="#">GitHub</a>
      <a href="#">Twitter</a>
    </div>
  </div>
  <div class="footer-bottom">
    © 2025 NoteHive. All rights reserved.
  </div>
</footer>
""", unsafe_allow_html=True)