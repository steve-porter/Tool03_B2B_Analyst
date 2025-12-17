import streamlit as st
import os
from dotenv import load_dotenv
from src.researcher import scrape_website, search_news
from src.analyzer import generate_brief
from src.utils import extract_company_name

import time
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="B2B Company Analyst",
    page_icon="💼",
    layout="centered"
)

# Custom CSS for modern aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Global Font - Target Text Elements Only (Avoid * to prevent breaking icons) */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Specific overrides for Streamlit elements to ensure coverage */
    p, h1, h2, h3, h4, h5, h6, li, span, label, 
    .stTextInput input, 
    .stTextArea textarea, 
    .stSelectbox select, 
    .stButton button {
        font-family: 'Inter', sans-serif !important;
    }

    .stApp {
        background-color: #1C1C2B;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6, .main-header {
        color: #E5E7EB !important;
    }
    
    .sub-header {
        color: #9CA3AF !important; /* Muted gray */
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea {
        background-color: #252538 !important; 
        color: #E5E7EB !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease;
        caret-color: #6366F1 !important; /* Visible caret */
    }

    /* Focus State */
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }

    /* Placeholder Text Fix */
    ::placeholder {
        color: #9CA3AF !important; /* Lighter gray for visibility */
        opacity: 1 !important;
    }
    
    /* Input Labels */
    .stMarkdown p, label {
        color: #E5E7EB !important;
    }

    /* Buttons */
    .stButton button {
        background-color: #6366F1 !important; 
        color: white !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton button:hover {
        background-color: #4F46E5 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }

    /* Result Container */
    .brief-container {
        background-color: #2A2A40; /* Increased contrast (lighter than #252538) */
        padding: 2.5rem;
        border-radius: 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        color: #E5E7EB;
        border: 1px solid #3F3F5E; /* Subtle border */
        margin-top: 2rem;
    }
    
    /* Markdown Text inside container */
    .brief-container h1, .brief-container h2, .brief-container h3 {
        color: #E5E7EB !important;
        margin-top: 1.5rem;
    }
    .data-header {
        color: #9CA3AF !important; /* For the data source header */
        font-weight: 400;
        font-size: 0.9rem;
        margin-bottom: 2rem;
        border-bottom: 1px solid #374151;
        padding-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .brief-container p, .brief-container li {
        color: #D1D5DB !important;
        line-height: 1.6;
    }

    /* Footer */
    .somar-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1C1C2B;
        color: #9CA3AF;
        text-align: center;
        padding: 15px;
        font-size: 0.85rem;
        border-top: 1px solid #252538;
        font-family: 'Inter', sans-serif;
        z-index: 9999;
    }
    .somar-footer a {
        color: #9CA3AF;
        text-decoration: none;
        transition: color 0.2s ease;
    }
    .somar-footer a:hover {
        color: #E5E7EB;
        text-decoration: underline;
    }

    /* Status Widget Visibility Fix - TARGET THE TEXT CONTAINER ONLY */
    /* Access the text inside the status widget without touching the icon parent */
    div[data-testid="stStatusWidget"] div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Remove white bar / Hide default footers */
    footer {display: none !important;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    .css-1lsmgbG {display: none !important;} /* Streamit specific class just in case */
    
    /* Fix success message overlap */
    .stAlert, .stSuccess {
        z-index: 999 !important;
        position: relative !important;
        margin: 1rem 0 !important;
        clear: both !important;
    }

    div[data-testid="stNotification"] {
        z-index: 1000 !important;
        display: block !important;
    }

    /* Ensure completion message is visible */
    .element-container:has(.stSuccess) {
        z-index: 1000 !important;
        position: relative !important;
    }
    
    </style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<h1 class="main-header">B2B Company Analyst</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Strategic Account Briefs in seconds.</p>', unsafe_allow_html=True)

# Input Section
st.markdown("### 1. Target Company")
url = st.text_input("Company URL", placeholder="e.g. https://www.salesforce.com")

st.markdown("### 2. My Solution")
value_proposition = st.text_area(
    "Value Proposition / Product Focus", 
    placeholder="Describe your solution (e.g., 'We provide enterprise cybersecurity solutions, specialising in managed threat detection...')",
    height=100
)

# Simple rate limiting (session-based)
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = None
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0

if st.button("Generate Strategic Brief"):
    # Rate limit check
    now = datetime.now()
    if st.session_state.last_request_time:
        time_since_last = (now - st.session_state.last_request_time).total_seconds()
        if time_since_last < 60:  # 1 minute cooldown
            st.warning(f"Please wait {int(60 - time_since_last)} seconds before next request.")
            st.stop()
    
    if st.session_state.request_count >= 5: 
        st.error("Demo limit reached (5 companies per session). Refresh page to try more.")
        st.stop()

    if not url:
        st.warning("Please enter a company URL.")
    elif not os.getenv("OPENAI_API_KEY"):
         st.error("OpenAI API Key not found. Please check your .env file or configuration.")
    else:
        # Update counters 
        st.session_state.last_request_time = now
        st.session_state.request_count += 1
        
        try:
                # Extract Company Name
                company_name = extract_company_name(url)
                if not company_name:
                    company_name = "Target Company"
                
                # Show loading with spinner
                with st.spinner(f"🔍 Analyzing {company_name}..."):
                    # Scrape Website
                    website_content = scrape_website(url)
                    if not website_content:
                        website_content = "Website content unavailable or blocked."

                    # Search News
                    news_results = search_news(company_name)
                    
                    # Generate Brief
                    brief = generate_brief(company_name, website_content, news_results, value_proposition)
                
                # Show success message BEFORE the output
                st.success("✅ Analysis Complete!")
                
                # Display Result
                st.markdown(f'<div class="brief-container">{brief}</div>', unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown('<div class="somar-footer"><a href="https://www.linkedin.com/in/stevedporter/" target="_blank">Built by Somar</a></div>', unsafe_allow_html=True)
