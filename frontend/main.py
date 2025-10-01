import streamlit as st

# --- PAGE CONFIGURATION ---
# Sets the browser tab title, icon, and layout for the entire app.
# This should always be the first Streamlit command in your main script.
st.set_page_config(
    page_title="NoteHIVE",
    page_icon="🐝",
    layout="wide"
)


# --- DEFAULT PAGE REDIRECTION ---
#
# This is the core logic that makes your landing page the default.
# When a user opens your app, this app.py script runs first.
# The st.switch_page() command immediately stops the execution of this script
# and tells Streamlit to load and display the landing.py page instead.
#
# Make sure the file path "pages/landing.py" is correct.
st.switch_page("pages/landing.py")
