import streamlit as st

# Set page configuration
st.set_page_config(layout="wide", page_title="NoteHIVE | AI Study Notes Organizer")

# --- CSS INJECTION FOR LAYOUT AND STYLE CORRECTIONS ---
st.markdown("""
        <style>
               /* Reduces the top padding of the page */
               .block-container {
                    padding-top: 1.5rem;
                    padding-left:1rem;
                    padding-right:1rem;
                }
               /* Aligns the header text and buttons vertically */
               div[data-testid="stHorizontalBlock"]:has(div[data-testid="stButton"]) {
                    align-items: center;
               }
               /* Custom style for the primary button */
               .stButton>button {
                    background-color: #FFC107; /* A nice yellow color */
                    color: black;
                    border: none;
               }
               .stButton>button:hover {
                    background-color: #FFD54F;
                    color: black;
                    border: none;
                }
        </style>
        """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("NoteHIVE 🐝")
    st.markdown("Your AI-Powered Study Notes Organizer")

with col2:
    button_col1, button_col2 = st.columns(2)
    with button_col1:
        if st.button("Login", use_container_width=True):
            st.switch_page("pages/login.py")
    with button_col2:
        if st.button("Signup", type="primary", use_container_width=True):
            st.switch_page("pages/signup.py")

# --- HERO SECTION ---
# Adjusted column ratio to [3, 2] to give more space to the text and reduce the gap.
left_col, right_col = st.columns([3, 1.7])
with left_col:
    st.header("Transform Your Study Notes with AI")
    st.write(
        """
        Tired of messy notes and endless reading? **NoteHIVE** is your personal AI assistant
        that turns cluttered study materials into clear, organized, and summarized notes.
        Upload your PDFs and let our AI do the heavy lifting.
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum
        """
    )
    if st.button("Get Started for Free", type="primary", use_container_width=True):
        st.switch_page("pages/signup.py")


with right_col:
    # A more relevant image for a study/tech app
    st.image(
        "https://images.pexels.com/photos/346529/pexels-photo-346529.jpeg",
        caption="Collaborate, Learn, and Succeed",
    )

st.divider()

# --- HOW IT WORKS SECTION ---
st.header("How It Works in 3 Simple Steps")
step_col1, step_col2, step_col3 = st.columns(3)
with step_col1:
    st.markdown("<h3 style='text-align: center;'>1. Upload</h3>", unsafe_allow_html=True)
    st.write("Drag and drop any PDF study material—lecture notes, textbooks, or research papers.")
with step_col2:
    st.markdown("<h3 style='text-align: center;'>2. AI Magic</h3>", unsafe_allow_html=True)
    st.write("Our AI analyzes the content, generates concise summaries, and auto-tags it by subject.")
with step_col3:
    st.markdown("<h3 style='text-align: center;'>3. Organize</h3>", unsafe_allow_html=True)
    st.write("Access your neatly organized, summarized notes from anywhere, anytime.")

st.divider()

# --- CUSTOMER REVIEWS SECTION ---
# st.header("What Our Students Say 🗣️")
# review_col1, review_col2, review_col3 = st.columns(3)
# with review_col1:
#     with st.container(border=True):
#         st.markdown("⭐⭐⭐⭐⭐")
#         st.write("NoteHIVE's AI summaries saved me hours of reading for my final exams. An absolute game-changer!")
#         st.markdown("<p style='text-align: right; color: grey;'>- Sarah J., University Student</p>", unsafe_allow_html=True)
# with review_col2:
#     with st.container(border=True):
#         st.markdown("⭐⭐⭐⭐⭐")
#         st.write("I upload all my lecture slides, and NoteHIVE organizes them perfectly. My backpack has never been lighter!")
#         st.markdown("<p style='text-align: right; color: grey;'>- Michael B., College Student</p>", unsafe_allow_html=True)
# with review_col3:
#     with st.container(border=True):
#         st.markdown("⭐⭐⭐⭐⭐")
#         st.write("The auto-tagging feature is incredibly smart. It correctly identified all my subjects without any help.")
#         st.markdown("<p style='text-align: right; color: grey;'>- Emily L., High School Student</p>", unsafe_allow_html=True)

# st.divider()

# --- FAQ SECTION ---
st.header("Frequently Asked Questions")
with st.expander("Is NoteHIVE free to use?"):
    st.write("Yes, we offer a generous free plan that includes up to 10 document uploads per month and access to all core AI features.")
with st.expander("What file types can I upload?"):
    st.write("Currently, we support PDF files. We are working on adding support for other formats like .docx and .pptx soon!")
with st.expander("Is my data secure?"):
    st.write("Absolutely. We use industry-standard encryption to ensure your study materials are stored safely and privately.")

# --- FOOTER ---
st.divider()
st.markdown("<p style='text-align: center;'>© 2025 NoteHIVE. Built with ❤️ using Streamlit.</p>", unsafe_allow_html=True)