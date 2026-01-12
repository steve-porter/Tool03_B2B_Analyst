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

    /* Global font enforcement - Universal + Specific Overrides */
    * , html, body, [class*="css"], [data-testid="stAppViewContainer"], .stMarkdown, p, div, span, button, h1, h2, h3, h4, h5, h6, label, input, textarea {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background-color: #1C1C2B;
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



    /* Input Fields */
    .stTextInput input, .stTextArea textarea {
        background-color: #232335 !important; 
        color: #FFFFFF !important;
        border: 1px solid #2F3045 !important;
        border-radius: 18px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #22D3EE !important;
        box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.2) !important;
    }
    
    ::placeholder {
        color: #6B7280 !important;
        opacity: 1 !important;
    }

    /* ===== CTA BUTTON STYLING (Targeted via marker) ===== */
    
    /* Find the button container that follows our marker */
    div.element-container:has(#cta-marker) + div.element-container button {
        background: #22D3EE !important;
        color: #1C1C2B !important;
        border-radius: 18px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
        width: 100% !important;
    }
    
    /* Force dark text on CTA button elements */
    div.element-container:has(#cta-marker) + div.element-container button *,
    div.element-container:has(#cta-marker) + div.element-container button p,
    div.element-container:has(#cta-marker) + div.element-container button span,
    div.element-container:has(#cta-marker) + div.element-container button div {
        color: #1C1C2B !important;
    }
    
    /* Hover State */
    div.element-container:has(#cta-marker) + div.element-container button:hover {
        background: #06B6D4 !important;
        color: #1C1C2B !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(34, 211, 238, 0.4) !important;
    }
    
    /* Focus State */
    div.element-container:has(#cta-marker) + div.element-container button:focus {
        background: #06B6D4 !important;
        color: #1C1C2B !important;
        outline: 2px solid #22D3EE !important;
        outline-offset: 2px !important;
        box-shadow: 0 8px 25px rgba(34, 211, 238, 0.4) !important;
    }
    
    /* Active State */
    div.element-container:has(#cta-marker) + div.element-container button:active {
        background: #0891B2 !important;
        color: #1C1C2B !important;
        transform: translateY(0) !important;
        box-shadow: 0 4px 12px rgba(34, 211, 238, 0.3) !important;
    }
    
    /* ===== MODE SELECTOR BUTTON STATES ===== */
    
    /* Primary button (SELECTED) - bordered card with cyan glow */
    button[data-testid="stBaseButton-primary"] {
        background-color: #232335 !important;
        color: #FFFFFF !important;
        border: 2px solid #22D3EE !important;
        border-radius: 18px !important;
        min-height: 4rem !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Override text color for primary button */
    button[data-testid="stBaseButton-primary"] *,
    button[data-testid="stBaseButton-primary"] p,
    button[data-testid="stBaseButton-primary"] span,
    button[data-testid="stBaseButton-primary"] div {
        color: #FFFFFF !important;
    }
    
    /* Secondary button (UNSELECTED) - subtle border, muted */
    button[data-testid="stBaseButton-secondary"] {
        background-color: #232335 !important;
        color: #9CA3AF !important;
        border: 1.5px solid #2F3045 !important;
        border-radius: 18px !important;
        min-height: 4rem !important;
        padding: 1rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    /* Override text color for secondary button */
    button[data-testid="stBaseButton-secondary"] *,
    button[data-testid="stBaseButton-secondary"] p,
    button[data-testid="stBaseButton-secondary"] span,
    button[data-testid="stBaseButton-secondary"] div {
        color: #9CA3AF !important;
    }
    
    /* Hover states for mode selector */
    button[data-testid="stBaseButton-secondary"]:hover {
        border-color: #22D3EE !important;
        color: #C7C9D3 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    button[data-testid="stBaseButton-primary"]:hover {
        box-shadow: 0 0 25px rgba(34, 211, 238, 0.4) !important;
    }
    
    /* Mobile adjustments */
    @media (max-width: 768px) {
        button[data-testid="stBaseButton-primary"],
        button[data-testid="stBaseButton-secondary"] {
            min-height: 3.5rem !important;
            font-size: 0.9rem !important;
        }
    }

    /* Brief Container */\r
    .brief-container {\r
        background-color: #232335;\r
        padding: 2.5rem;\r
        border-radius: 18px;\r
        border: 1px solid #2F3045;\r
        margin-top: 2rem;\r
        color: #E5E7EB;\r
    }\r
    \r
    /* Mobile Responsive - Title and Subtitle */\r
    @media (max-width: 768px) {\r
        h1.main-header {\r
            font-size: 2rem !important;\r
            margin-bottom: 0.75rem !important;\r
        }\r
        \r
        h1.main-header + p {\r
            font-size: 1rem !important;\r
            margin-bottom: 2rem !important;\r
        }\r
        \r
        button[data-testid="stBaseButton-primary"],\r
        button[data-testid="stBaseButton-secondary"] {\r
            min-height: 3.5rem !important;\r
            font-size: 0.9rem !important;\r
        }\r
    }

    footer {display: none !important;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)



# Main Content
col_spacer, col_content = st.columns([1, 10])

with col_content:
    st.markdown('<h1 class="main-header">Company Intelligence Platform</h1>', unsafe_allow_html=True)
    
    # Subtitle
    st.markdown(
        '<p style="text-align: left; color: #C7C9D3; font-size: 1.15rem; '
        'font-weight: 400; margin-bottom: 2.2rem; letter-spacing: 0.01em; '
        'margin-left: 0.25rem; margin-top: -1.2rem;">'
        'AI-powered deep company research</p>', 
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize session state for mode
    if 'analysis_mode' not in st.session_state:
        st.session_state.analysis_mode = "Target Account Research"
    
    # Mode selector label
    st.markdown(
        '<p class="mode-selector-label" style="text-align: center; color: #FFFFFF; font-size: 1rem; '
        'margin-bottom: 1rem; font-weight: 500; letter-spacing: 0.02em;">Select your intelligence focus:</p>',
        unsafe_allow_html=True
    )
    
    # Button-based mode selector (no radio buttons!)
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        is_selected_research = st.session_state.analysis_mode == "Target Account Research"
        if st.button(
            "Target Account Research",
            key="btn_research",
            use_container_width=True,
            type="primary" if is_selected_research else "secondary"
        ):
            st.session_state.analysis_mode = "Target Account Research"
            st.rerun()
    
    with col2:
        is_selected_interview = st.session_state.analysis_mode == "Job Interview Prep"
        if st.button(
            "Job Interview Prep",
            key="btn_interview",
            use_container_width=True,
            type="primary" if is_selected_interview else "secondary"
        ):
            st.session_state.analysis_mode = "Job Interview Prep"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Input Section
    st.markdown("### 1. Target Company")
    url = st.text_input("Company URL", placeholder="e.g. https://www.salesforce.com", label_visibility="collapsed")

    # Conditional Inputs
    jd_content = None
    cv_text = None
    value_proposition = None

    if st.session_state.analysis_mode == "Target Account Research":
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
    
    # Action Button - target specifically with marker for stable styling
    btn_label = "Generate Strategic Brief" if st.session_state.analysis_mode == "Target Account Research" else "Generate Interview Strategy"
    
    st.markdown('<span id="cta-marker"></span>', unsafe_allow_html=True)
    if st.button(btn_label, key="cta_main", use_container_width=True):
        if not url:
            st.warning("Please enter a company URL.")
        elif st.session_state.analysis_mode == "Job Interview Prep" and not jd_content:
            st.warning("Please provide a Job Description.")
        elif not os.getenv("OPENAI_API_KEY"):
             st.error("API Key missing.")
        else:
            try:
                company_name = extract_company_name(url) or "Target Company"
                
                with st.status(f"🛠️ Building {st.session_state.analysis_mode} Report...") as status:
                    st.write("Scraping website...")
                    website_content = scrape_website(url) or "Website content unavailable."
                    
                    st.write("Analyzing news...")
                    news_results = search_news(company_name)
                    
                    st.write("Generating AI strategy...")
                    report = generate_brief(
                        company_name=company_name,
                        website_content=website_content,
                        news_results=news_results,
                        mode=st.session_state.analysis_mode,
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
    st.markdown('<div style="text-align: center; color: #6B7280; font-size: 0.85rem; margin-top: 1rem;">v2.2 Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #6B7280; font-size: 0.85rem;"><a href="https://www.linkedin.com/in/stevedporter/" style="color: #6B7280; text-decoration: none;">Built by Somar Intelligence</a></div>', unsafe_allow_html=True)
