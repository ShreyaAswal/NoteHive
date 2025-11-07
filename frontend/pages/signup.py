import streamlit as st
import re
import sys
import os

# --- PATH SETUP ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
backend_path = os.path.join(project_root, 'backend')
sys.path.append(backend_path)
from signupDb import add_user

# --- PAGE CONFIG ---
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
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.logo {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-left: -1rem; 
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

/* Layout padding to push below navbar */
.main .block-container {
  padding-top: 5rem;   /* adds space below navbar */
  padding-bottom: 3rem;
}

/* Signup card */
[data-testid="stForm"] {
  background: var(--card-bg);
  border-radius: 20px;
  padding: 2.5rem 2.8rem;
  margin-top: 1rem;
  box-shadow: 0 6px 30px rgba(0,0,0,0.1);
  border: 1px solid rgba(0,0,0,0.04);
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

/* Make the Sign Up button full width */
[data-testid="stForm"] .stButton > button {
  width: 100% !important;
  display: block;
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


/* Inputs */
.stTextInput input {
  border-radius: 10px;
  border: 1px solid #d0d7de;
  background-color: var(--input-bg);
  color: #0f172a;
  height: 42px;
  padding: 0.6rem 1rem;
}
::placeholder { color: #9ca3af !important; }

/* Text styling */
h1 {
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.8rem;
}
h3, h4, p {
  color: #334155;
}

/* Bottom link */
a {
  color: #ffb703;
  font-weight: 500;
  text-decoration: none;
}
a:hover { text-decoration: underline; }

#MainMenu, header, footer {visibility: hidden;}
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
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown("<h1>Welcome to NoteHIVE</h1>", unsafe_allow_html=True)
    st.markdown("### Your new hub for capturing ideas, organizing notes, and boosting productivity.")
    st.markdown("Join thousands of users who are transforming their workflow. Sign up now to get started!")

with right_col:
    with st.form("signup_form"):
        st.subheader("Create a New Account")
        st.markdown("**Email**")
        email = st.text_input("Email", placeholder="your.email@example.com", label_visibility="collapsed")

        st.markdown("**Username**")
        username = st.text_input("Username", placeholder="Choose a unique username", label_visibility="collapsed")

        st.markdown("**Password**")
        password = st.text_input("Password", type="password", placeholder="Create a strong password", label_visibility="collapsed")

        st.markdown("**Confirm Password**")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password", label_visibility="collapsed")

        submitted = st.form_submit_button("Sign Up")

        if submitted:
            is_valid = True
            if not email or not username or not password or not confirm_password:
                st.error("⚠️ Please fill out all fields.")
                is_valid = False
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address.")
                is_valid = False
            elif password != confirm_password:
                st.error("Passwords do not match.")
                is_valid = False
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
                is_valid = False

            if is_valid:
                success, message = add_user(username, email, password)
                if success:
                    st.success(f"✅ {message} You can now log in.")
                else:
                    st.error(f"{message}")

    st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            Already have an account? <a href="/login" target="_self">Log In</a>
        </div>
    """, unsafe_allow_html=True)
