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
    .stApp {
        background-color: #f8f9fa;
    }
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-family: 'Inter', sans-serif;
        color: #666;
        margin-bottom: 2rem;
    }
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px 15px;
    }
    .stButton button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #0052a3;
    }
    .brief-container {
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        color: #333;
    }
    /* Hide Streamlit default menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<h1 class="main-header">B2B Company Analyst</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Strategic Account Briefs in seconds.</p>', unsafe_allow_html=True)

# Input Section
st.markdown("### 1. Target Company")
url = st.text_input("Company URL", placeholder="e.g. https://www.salesforce.com")

st.markdown("### 2. My Solution")
default_val_prop = "We provide enterprise cybersecurity solutions, specialising in managed threat detection (MDR) and zero-trust architecture to protect regulated data from ransomware and breaches."
value_proposition = st.text_area("Value Proposition / Product Focus", value=default_val_prop, height=100)

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
    
    if st.session_state.request_count >= 5: # Increased limit to 5
        st.error("Demo limit reached (5 companies per session). Refresh page to try more.")
        st.stop()

    if not url:
        st.warning("Please enter a company URL.")
    elif not os.getenv("OPENAI_API_KEY"):
         st.error("OpenAI API Key not found. Please check your .env file or configuration.")
    else:
        # Update counters only if we proceed to generate (or try to)
        st.session_state.last_request_time = now
        st.session_state.request_count += 1
        # Create a container for the status messages
        status_container = st.empty()
        
        try:
            # Step 1: Extract Company Name
            company_name = extract_company_name(url)
            if not company_name:
                company_name = "Target Company" # Fallback
            
            # Step 2: Scrape Website
            with st.spinner(f"Reading website content for {company_name}..."):
                website_content = scrape_website(url)
                if not website_content:
                    st.warning("Could not scrape the website. Generating brief based on news only.")
                    website_content = "Website content unavailable or blocked."

            # Step 3: Search News
            with st.spinner(f"Searching recent news for {company_name}..."):
                news_results = search_news(company_name)
            
            # Step 4: Analyze with LLM
            with st.spinner("Analyzing data and generating strategy..."):
                brief = generate_brief(company_name, website_content, news_results, value_proposition)
            
            # Display Result
            st.markdown(f'<div class="brief-container">{brief}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
