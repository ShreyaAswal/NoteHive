import streamlit as st
import time
import os
import sys

# --- Path logic to find the backend folder ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
backend_path = os.path.join(project_root, 'backend')
sys.path.append(backend_path)

# Import verification function
from signupDb import verify_user

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NoteHive | AI Study Notes Organizer", page_icon="🪶", layout="wide")

# --- STYLING ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

:root {
  --bg-light: #f8fafc;
  --text-light: #0f172a;
  --accent: #ffc107;
  --card-bg: #ffffff;
  --input-bg: #f9fafb;
}

/* Base setup */
body, .stApp {
  font-family: 'Poppins', sans-serif;
  background-color: var(--bg-light);
  color: var(--text-light);
  transition: all 0.3s ease;
}

/* NAVBAR */
.navbar {
  position: sticky;
  top: 0;
  z-index: 999;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2.5rem;
  background: var(--bg-light);
  color: var(--text-light);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.logo {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-left: -1rem; /* ✅ Shift logo slightly left */
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
.nav-buttons button:hover { color: var(--accent); }

/* Layout adjustments */
.main .block-container {
  padding-top: 6rem;
  padding-bottom: 3rem;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
}

/* LOGIN CARD */
[data-testid="stForm"] {
  background: var(--card-bg);
  border-radius: 24px;
  padding: 2.8rem 3rem;
  margin-top: 1rem;
  box-shadow: 0 6px 30px rgba(0,0,0,0.08);
  border: 1px solid rgba(0,0,0,0.05);
  width: 100%;
  max-width: 520px; /* ✅ Increased width */
  transition: all 0.3s ease;
}

/* Inputs */
.stTextInput input {
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background-color: var(--input-bg);
  color: #0f172a;
  padding: 0.6rem 0.9rem;
}
::placeholder { color: #6b7280 !important; }

/* Button (Full Width & Themed) */
[data-testid="stForm"] .stButton > button {
  width: 100% !important;
  background: linear-gradient(135deg, #ffd84f, #ffc107);
  color: #0f172a;
  border-radius: 14px;
  border: none;
  padding: 0.9rem 1rem;
  font-weight: 600;
  font-size: 1.05rem;
  letter-spacing: 0.3px;
  box-shadow: 0 4px 10px rgba(255, 193, 7, 0.3);
  transition: all 0.3s ease;
}
[data-testid="stForm"] .stButton > button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(255, 193, 7, 0.45);
  background: linear-gradient(135deg, #ffe17a, #ffca2b);
}

/* Text + Links */
a {
  color: var(--accent);
  text-decoration: none;
}
a:hover { text-decoration: underline; }

h1, h2, h3, h4, h5, h6, p, .stMarkdown { color: var(--text-light); }

#MainMenu, .stHeader, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
st.markdown("""
<div class="navbar">
  <div class="logo">🪶 NoteHive</div>
  <div class="nav-buttons">
    <a href="/landing" target="_self"><button>Home</button></a>
    <a href="/dashboard" target="_self"><button>Dashboard</button></a>
    <a href="/login" target="_self"><button>Login</button></a>
    <a href="/signup" target="_self"><button>Signup</button></a>
  </div>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2 = st.columns([1, 1.1], gap="large")

with col1:
    st.markdown("<h1 style='font-size: 3.2rem; font-weight: 600;'>Welcome Back! </h1>", unsafe_allow_html=True)
    st.markdown("""
        <p style='font-size:1.1rem; margin-top:0.5rem;'>
        Log in to access your dashboard, manage your notes, and continue your journey with <b>NoteHive</b>.
        </p>
        <p style='font-size:1.05rem; color:#334155;'>Your smart note organizer awaits!</p>
    """, unsafe_allow_html=True)

with col2:
    with st.form("login_form"):
        st.subheader("Login to Your Account")

        st.markdown("**Email or Username**")
        username_or_email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed")

        st.markdown("**Password**")
        password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")

        submitted = st.form_submit_button("Login")

        if submitted:
            if not username_or_email or not password:
                st.warning("⚠️ Please fill out all fields.")
            else:
                success, result = verify_user(username_or_email, password)
                if success:
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = result['id']
                    st.session_state['username'] = result['username']
                    st.success("Login Successful! Redirecting...")
                    st.balloons()
                    st.switch_page("pages/dashboard.py")
                else:
                    st.error(f"{result}")

    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            Don't have an account? <a href="/signup" target="_self">Sign Up</a>
        </div>
    """, unsafe_allow_html=True)
