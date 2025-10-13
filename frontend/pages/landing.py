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
                .col1-content {
                    padding: 0rem !important;
                    border: 0rem !important;
                }
                .right-col-content {
                    padding-top: 4rem !important;
                }
        </style>
        """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col1, col2 = st.columns([2, 1])

with col1:
  
    st.header("NoteHIVE")
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
left_col, right_col = st.columns([3, 1.5])
with left_col:
    st.markdown('<div class="col1-content">', unsafe_allow_html=True)
    st.header("Upload, Summarize, Organize. It's that simple.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.write(
        """

        Turn your study materials into manageable insights.
        NoteHIVE is designed for students and researchers who need to get to the core of their reading material, fast. 
        Upload your lecture notes, academic papers, or textbooks, 
        and let our AI provide you with a clear summary and identify the subject, 
        so you can organize your knowledge and study more effectively.

        NoteHIVE streamlines how you interact with your documents. 
        Our platform allows you to upload any PDF and instantly receive a clear, AI-generated summary. 
        The document is automatically categorized by subject, helping you build an organized, 
        searchable library of your most important information.
        Find clarity and save time with every upload.
        """
    )
    if st.button("Get Started for Free", type="primary", use_container_width=True):
        st.switch_page("pages/signup.py")

with right_col:
    # A more relevant image for a study/tech app
    st.markdown('<div class="right-col-content">', unsafe_allow_html=True)
    st.image(
        "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=2070",
        caption="Organize, Summarize, Succeed",
    )
    st.markdown('</div>', unsafe_allow_html=True)

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
st.markdown("<p style='text-align: center;'>© 2025 NoteHIVE.</p>", unsafe_allow_html=True)