import streamlit as st
import os
from dotenv import load_dotenv
from src.researcher import scrape_website, search_news
from src.analyzer import generate_brief
from src.utils import extract_company_name
from src.pdf_utils import extract_text_from_pdf

import time
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Company Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0F0F17;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161625 !important;
        border-right: 1px solid #252538;
    }
    
    /* Style radio buttons as clickable tiles */
    div.row-widget.stRadio > div {
        background-color: transparent !important;
        gap: 12px;
    }
    
    div.row-widget.stRadio div[role="radiogroup"] > label {
        background-color: #252538 !important;
        border: 2px solid #374151 !important;
        padding: 20px !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
        display: block !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    div.row-widget.stRadio div[role="radiogroup"] > label:hover {
        border-color: #6366F1 !important;
        background-color: #2A2A40 !important;
        transform: translateY(-2px);
    }
    
    div.row-widget.stRadio div[role="radiogroup"] > label:has(input:checked) {
        border-color: #6366F1 !important;
        background-color: #1E1E3F !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3) !important;
    }

    div.row-widget.stRadio div[role="radiogroup"] label span[data-testid="stWidgetLabel"] {
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    div.row-widget.stRadio input {
        display: none;
    }

    /* Text Contrast */
    h1, h2, h3, h4, h5, h6, label {
        color: #F3F4F6 !important;
    }
    
    p, .stMarkdown p {
        color: #D1D5DB !important;
    }

    .main-header {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin-bottom: 0.5rem !important;
    }

    .mode-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        background-color: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid rgba(129, 140, 248, 0.4);
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 2rem;
    }

    /* Input Fields */
    .stTextInput input, .stTextArea textarea {
        background-color: #161625 !important; 
        color: #FFFFFF !important;
        border: 1px solid #374151 !important;
        border-radius: 10px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }
    
    ::placeholder {
        color: #6B7280 !important;
        opacity: 1 !important;
    }

    /* Blue Gradient Button */
    .stButton button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5) !important;
    }

    /* Brief Container */
    .brief-container {
        background-color: #161625;
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid #2D2D3F;
        margin-top: 2rem;
        color: #E5E7EB;
    }

    footer {display: none !important;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### Platform Mode")
    st.markdown('<p style="color: #9CA3AF; font-size: 0.9rem; margin-bottom: 1.5rem;">Choose your intelligence focus:</p>', unsafe_allow_html=True)
    
    mode_options = [
        "🎯 Sales & Marketing Outreach", 
        "🎓 Career Strategy & Interview Prep"
    ]
    
    selected_mode_text = st.radio(
        "Select Analysis Mode",
        mode_options,
        index=0,
        label_visibility="collapsed",
        help="Sales: Strategic account briefs with buying signals and messaging hooks.\nCareers: CV-to-company alignment with strategic interview questions."
    )
    
    # Extract mode for logic
    analysis_mode = "Sales Outreach" if "Sales" in selected_mode_text else "Interview Prep"

    st.markdown("---")
    st.caption("v2.2 Intelligence Platform")

# Main Content
col_spacer, col_content = st.columns([1, 10])

with col_content:
    st.markdown('<h1 class="main-header">Company Intelligence Platform</h1>', unsafe_allow_html=True)
    
    badge_text = "Strategic Account Briefs" if analysis_mode == "Sales Outreach" else "Career Strategy Advisor"
    st.markdown(f'<div class="mode-badge">{badge_text}</div>', unsafe_allow_html=True)

    # Input Section
    st.markdown("### 1. Target Company")
    url = st.text_input("Company URL", placeholder="e.g. https://www.salesforce.com", label_visibility="collapsed")

    # Conditional Inputs
    jd_content = None
    cv_text = None
    value_proposition = None

    if analysis_mode == "Sales Outreach":
        st.markdown("### 2. My Solution")
        value_proposition = st.text_area(
            "Value Proposition / Product Focus", 
            placeholder="Describe your solution (e.g., 'We provide enterprise cybersecurity solutions...')",
            height=120,
            label_visibility="collapsed"
        )
    else:
        st.markdown("### 2. Job Description")
        jd_content = st.text_area(
            "Job Description (JD)",
            placeholder="Paste the full job description here...",
            height=200,
            label_visibility="collapsed"
        )
        
        st.markdown("### 3. Your CV")
        uploaded_cv = st.file_uploader("Upload CV (PDF)", type=["pdf"], label_visibility="collapsed")
        if uploaded_cv:
            with st.spinner("Processing CV..."):
                cv_text = extract_text_from_pdf(uploaded_cv)
                if cv_text.startswith("Error"):
                    st.error("Failed to parse CV. Please try a different file.")
                    cv_text = None
                else:
                    st.success("✓ CV processed successfully")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Button
    btn_label = "Generate Strategic Brief" if analysis_mode == "Sales Outreach" else "Generate Interview Strategy"
    
    if st.button(btn_label, use_container_width=True):
        if not url:
            st.warning("Please enter a company URL.")
        elif analysis_mode == "Interview Prep" and not jd_content:
            st.warning("Please provide a Job Description.")
        elif not os.getenv("OPENAI_API_KEY"):
             st.error("API Key missing.")
        else:
            try:
                company_name = extract_company_name(url) or "Target Company"
                
                with st.status(f"🛠️ Building {analysis_mode} Report...") as status:
                    st.write("Scraping website...")
                    website_content = scrape_website(url) or "Website content unavailable."
                    
                    st.write("Analyzing news...")
                    news_results = search_news(company_name)
                    
                    st.write("Generating AI strategy...")
                    report = generate_brief(
                        company_name=company_name,
                        website_content=website_content,
                        news_results=news_results,
                        mode=analysis_mode,
                        value_proposition=value_proposition,
                        job_description=jd_content,
                        cv_text=cv_text
                    )
                    status.update(label="✓ Complete!", state="complete")
                
                st.markdown(f'<div class="brief-container">{report}</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Footer
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #6B7280; font-size: 0.85rem;"><a href="https://www.linkedin.com/in/stevedporter/" style="color: #6B7280; text-decoration: none;">Built by Somar Intelligence</a></div>', unsafe_allow_html=True)
