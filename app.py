import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from datetime import datetime
import time

from modules.config import configure_genai
from modules.utils.pdf_parser import extract_text_from_pdf
from modules.services.ai_client import get_gemini_response
from modules.prompts import PROMPT_REVIEW, PROMPT_IMPROVE, PROMPT_MATCH

# CONFIGURATION SECTION
AUTHOR_NAME = "Vasanth Rao"
AUTHOR_EMAIL = "vasanthraochalla@gmail.com"
LINKEDIN_URL = "https://www.linkedin.com/in/vasanth-rao-challa/"
GITHUB_URL = "https://github.com/vasanth2809"
X_URL = "https://x.com/ChallaVasanth"
COPYRIGHT_YEAR = "2025"

# Configure page
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #1f77e6;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 1.3em;
        color: #555;
        margin-bottom: 20px;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77e6;
        color: #1a1a1a;
        font-size: 1em;
        line-height: 1.6;
    }
    .success-box {
        background-color: #d4edda;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        color: #155724;
        font-weight: 500;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #17a2b8;
        color: #0c5460;
    }
    
    /* Intro Animation Styles */
    .intro-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        flex-direction: column;
    }
    
    .intro-content {
        text-align: center;
        color: white;
        padding: 40px;
        max-width: 800px;
    }
    
    .intro-content h1 {
        font-size: 3em;
        margin-bottom: 20px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .intro-step {
        font-size: 1.2em;
        margin: 15px 0;
        animation: slideIn 0.6s ease-out forwards;
        opacity: 0;
    }
    
    .intro-step:nth-child(2) { animation-delay: 0.3s; }
    .intro-step:nth-child(3) { animation-delay: 0.6s; }
    .intro-step:nth-child(4) { animation-delay: 0.9s; }
    .intro-step:nth-child(5) { animation-delay: 1.2s; }
    
    .intro-buttons {
        margin-top: 30px;
        display: flex;
        justify-content: center;
        gap: 20px;
        width: 100%;
    }
    
    .intro-buttons .stButton>button {
        min-width: 160px;
        padding: 12px 24px;
        border-radius: 30px;
        border: none;
        background-color: rgba(255, 255, 255, 0.2);
        color: #fff;
        font-size: 1.1em;
        cursor: pointer;
        transition: background 0.2s ease-out, color 0.2s ease-out;
    }
    
    .intro-buttons .stButton>button:hover {
        background-color: #fff;
        color: #764ba2;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* History Styles */
    .history-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
    }
    
    .history-item {
        background: white;
        padding: 12px;
        margin: 8px 0;
        border-radius: 6px;
        border-left: 4px solid #1f77e6;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    
    /* Footer Styles */
    .footer {
        margin-top: 50px;
        padding: 30px 20px;
        border-top: 2px solid #e0e0e0;
        text-align: center;
        color: #666;
        font-size: 0.9em;
    }
    
    .footer-section {
        margin: 10px 0;
    }
    
    .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 15px 0;
        flex-wrap: wrap;
    }
    
    .social-links a {
        color: #1f77e6;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }
    
    .social-links a:hover {
        color: #764ba2;
    }
    
    .divider-line {
        border-bottom: 1px solid #ddd;
        margin: 20px 0;
    }
    
    .action-button {
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
if "current_response" not in st.session_state:
    st.session_state.current_response = None

# Configure GenAI
try:
    configure_genai()
except Exception as e:
    st.error(f"⚠️ Error configuring GenAI: {e}")
    st.info("Please ensure GOOGLE_API_KEY is set in your environment.")
    st.stop()

# # Show intro animation on first load
# if st.session_state.show_intro:
#     with st.container():
#         st.markdown("""
#         <div class="intro-overlay">
#             <div class="intro-content">
#                 <h1>📄 ATS Resume Expert</h1>
#                 <div class="intro-step">✅ Analyze your resume</div>
#                 <div class="intro-step">💡 Get improvement suggestions</div>
#                 <div class="intro-step">📊 Get match percentage scores</div>
#                 <div class="intro-step">🚀 Optimize for ATS systems</div>
#                 <div class="intro-buttons">
#         """, unsafe_allow_html=True)

#         button_col1, button_col2 = st.columns([1, 1], gap="large")
#         with button_col1:
#             if st.button("🚀 Get Started", key="get_started"):
#                 st.session_state.show_intro = False
#                 st.rerun()
#         with button_col2:
#             if st.button("⏭️ Skip", key="skip_intro"):
#                 st.session_state.show_intro = False
#                 st.rerun()

#         st.markdown("""
#                 </div>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header">📄 ATS Resume Tracking System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Resume Analysis & Optimization</div>', unsafe_allow_html=True)

# Two-column layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Job Description")
    input_text = st.text_area(
        "Paste the job description here:",
        height=200,
        placeholder="Enter job description, requirements, responsibilities...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF only):",
        type=["pdf"],
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        st.markdown('<div class="success-box">✅ Resume uploaded successfully!</div>', unsafe_allow_html=True)
        st.caption(f"File: {uploaded_file.name} | Size: {uploaded_file.size / 1024:.1f} KB")

add_vertical_space(2)

# Action buttons
st.markdown("### 🚀 Analysis Options")
button_col1, button_col2, button_col3 = st.columns(3, gap="small")

with button_col1:
    submit1 = st.button(
        "👤 Resume Review",
        use_container_width=True,
        help="Get professional evaluation of your resume against the job"
    )

with button_col2:
    submit2 = st.button(
        "💡 Improve Skills",
        use_container_width=True,
        help="Get suggestions to enhance your resume and match the job"
    )

with button_col3:
    submit3 = st.button(
        "📊 Match Score",
        use_container_width=True,
        help="Get percentage match and missing keywords"
    )

add_vertical_space(2)

# Define action handler
def handle_action(prompt_constant, action_type):
    if not input_text.strip():
        st.warning("⚠️ Please enter a job description first")
        return
    
    if uploaded_file is None:
        st.warning("⚠️ Please upload your resume (PDF)")
        return

    # Progress indicator
    with st.spinner("🔄 Analyzing your resume..."):
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
        except Exception as e:
            st.error(f"❌ Could not extract resume text: {e}")
            return

        try:
            response = get_gemini_response(input_text, resume_text, prompt_constant)
            st.session_state.current_response = response
            
            # Add to history
            st.session_state.analysis_history.append({
                "type": action_type,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "response": response
            })
        except Exception as e:
            st.error(f"❌ Error generating response: {e}")
            return

    # Display response
    st.markdown("---")
    st.markdown("### 📋 Analysis Result")
    
    with st.container():
        st.markdown('<div class="response-box">', unsafe_allow_html=True)
        st.markdown(f"**{action_type}**\n\n{response}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons for response
    col_copy, col_download = st.columns(2)
    with col_copy:
        st.button(
            "📋 Copy to Clipboard",
            key="copy_btn",
            help="Copy response text",
            on_click=lambda: st.write("Copied!")
        )
    
    with col_download:
        st.download_button(
            "⬇️ Download as Text",
            data=response,
            file_name=f"analysis_{action_type.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_btn"
        )

# Handle button clicks
if submit1:
    handle_action(PROMPT_REVIEW, "Resume Review")
elif submit2:
    handle_action(PROMPT_IMPROVE, "Skill Improvement Suggestions")
elif submit3:
    handle_action(PROMPT_MATCH, "Match Score Analysis")

add_vertical_space(3)

# HISTORY SECTION AT BOTTOM
if st.session_state.analysis_history:
    st.markdown('<div class="history-container">', unsafe_allow_html=True)
    st.markdown("### 📜 Analysis History")
    for i, item in enumerate(st.session_state.analysis_history[::-1], 1):
        with st.expander(f"📋 {item['type']} - {item['time']}"):
            st.write(item['response'][:300] + "..." if len(item['response']) > 300 else item['response'])
            if st.button(f"View Full", key=f"view_{i}"):
                st.write(item['response'])
    st.markdown('</div>', unsafe_allow_html=True)

add_vertical_space(3)

# ===================== FOOTER COMPONENT ===================== #
st.markdown(f"""
<div class="footer">
    <div class="footer-section">
        <h3 style="color: #1f77e6;">Made with ❤️ by {AUTHOR_NAME}</h3>
    </div>
</div>
""", unsafe_allow_html=True)
