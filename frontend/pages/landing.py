import streamlit as st

st.set_page_config(page_title="NoteHive | AI Study Notes Organizer", page_icon="🪶", layout="wide")

# --- CUSTOM STYLING + DARK MODE JS ---
st.markdown("""
<style>
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
  padding: 1rem 3rem;
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
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent);
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

/* HERO */
.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4rem 8%;
  flex-wrap: wrap;
  gap: 2rem;
}

.hero-text {
  flex: 1 1 450px;
}

.hero h1 {
  font-size: 2.8rem;
  color: var(--text-light);
  margin-bottom: 1rem;
  font-weight: 800;
}

.hero p {
  color: #475569;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  max-width: 600px;
}

.hero.dark h1, .hero.dark p {
  color: var(--text-dark);
}

.hero-img {
  flex: 1 1 400px;
  text-align: center;
}

.hero-img img {
  width: 90%;
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0,0,0,0.08);
}

.get-started {
  background: var(--accent);
  border: none;
  color: #000;
  font-weight: 700;
  border-radius: 12px;
  padding: 0.8rem 1.8rem;
  cursor: pointer;
  transition: 0.3s;
}

.get-started:hover {
  transform: scale(1.05);
}

/* FEATURE BOXES */
.feature-boxes {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
  padding: 2rem 0;
}

.feature {
  background: var(--bg-light);
  color: var(--text-light);
  padding: 1.5rem 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  flex: 1 1 250px;
  text-align: center;
  transition: all 0.3s ease;
}

.feature.dark {
  background: var(--card-dark);
  color: var(--text-dark);
}

/* CARDS SECTION */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 4rem 8%;
}

.card {
  background: var(--bg-light);
  color: var(--text-light);
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  padding: 2rem;
  transition: all 0.3s;
  text-align: center;
}

.card.dark {
  background: var(--card-dark);
  color: var(--text-dark);
  box-shadow: 0 0 20px rgba(255,255,255,0.05);
}

.card:hover {
  transform: translateY(-5px);
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
            
/* SECTION TITLES */
.section-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin-top: 4rem;
  margin-bottom: 2rem;
  color: var(--text-light);
}
.section-title.dark {
  color: var(--text-dark);
}

/* FAQ */
.faq {
  padding: 2rem 8%;
}
.faq-item {
  margin-bottom: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 10px;
  background: var(--bg-light);
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: 0.3s;
}
.faq-item.dark {
  background: var(--card-dark);
  color: var(--text-dark);
}
.faq-item:hover {
  transform: translateY(-3px);
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
            
</style>

<script>
function toggleTheme() {
  document.body.classList.toggle('dark');
  document.querySelector('.navbar').classList.toggle('dark');
  document.querySelector('.hero').classList.toggle('dark');
  document.querySelectorAll('.feature').forEach(c => c.classList.toggle('dark'));
  document.querySelectorAll('.card').forEach(c => c.classList.toggle('dark'));
  document.querySelectorAll('.faq-item').forEach(c => c.classList.toggle('dark'));
  document.querySelector('.footer').classList.toggle('dark');
  document.querySelectorAll('.section-title').forEach(c => c.classList.toggle('dark'));
}
</script>
""", unsafe_allow_html=True)

# --- NAVBAR ---
st.markdown("""
<div class="navbar">
  <div class="logo">🪶 NoteHive</div>
  <div class="nav-buttons">
    <a href="/landing" target="_self"><button>Home</button></a>
    <a href="#how-it-works" target="_self"><button>How it Works</button></a>
    <a href="/login" target="_self"><button>Login</button></a>
    <a href="/signup" target="_self"><button>Signup</button></a>
  </div>
</div>
""", unsafe_allow_html=True)


# --- HERO SECTION ---
st.markdown("""
<div class="hero">
  <div class="hero-text">
    <p style="color:#3b82f6; font-weight:600;">Study Smarter — Not Harder</p>
    <h1>Upload. Summarize. Memorize.<br>Build knowledge faster with AI.</h1>
    <p>NoteHive turns long PDFs into concise, searchable notes with automatic subject tagging and quick export — designed for students and researchers.</p>
    <a href="/signup" target="_self"><button class="get-started">Get Started — It's Free</button></a>
  </div>
  <div class="hero-img">
    <img src="https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=900&q=80" alt="Study with AI">
  </div>
</div>

<div class="feature-boxes">
  <div class="feature">
    <h3>10+</h3>
    <p>uploads/month free</p>
  </div>
  <div class="feature">
    <h3>📄 PDF</h3>
    <p>support</p>
  </div>
  <div class="feature">
    <h3>🤖 Auto</h3>
    <p>subject tagging</p>
  </div>
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

# --- FAQ SECTION ---
st.markdown("""
<h2 class="section-title">❓Frequently Asked Questions</h2>
<div class="faq">
  <div class="faq-item">
    <h4>Is NoteHive free to use?</h4>
    <p>Yes! You can use all essential features for free with optional premium upgrades.</p>
  </div>
  <div class="faq-item">
    <h4>Can I upload handwritten notes?</h4>
    <p>Absolutely! You can upload scanned handwritten notes as PDFs or images.</p>
  </div>
  <div class="faq-item">
    <h4>Does it support multiple devices?</h4>
    <p>Yes, your notes are securely synced across all your devices in real-time.</p>
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