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
        background-color: #1C1C2B;
    }

    /* ===== INLINE MODE TOGGLE (SEGMENTED CONTROL) ===== */
    
    /* Container */
    div[data-testid="stRadio"][data-baseweb="radio"] {
        background-color: transparent !important;
    }

    /* Radio group - horizontal card-style layout */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        flex-direction: row !important;
        gap: 16px !important;  /* Space between cards */
        justify-content: center !important;
        background-color: transparent !important;  /* Remove container background */
        border-radius: 0 !important;
        padding: 0 !important;
        border: none !important;
    }

    /* Individual radio labels - bordered card style */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        flex: 1 !important;
        min-height: 5rem !important;
        max-width: 280px !important;
        padding: 1rem 1.5rem !important;
        
        /* Always show border for definition */
        border: 1.5px solid #2F3045 !important;
        background-color: #232335 !important;
        
        border-radius: 18px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin: 0 !important;
        
        /* Center text */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        
        color: #C7C9D3 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        line-height: 1.4 !important;
    }

    /* Hover state - preview selection with cyan border */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        border-color: #22D3EE !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }

    /* Selected state - cyan border + glow, SAME background */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        /* KEY: Keep same background as unselected for balance */
        background-color: #232335 !important;
        
        /* Differentiate with border + glow */
        border: 2px solid #22D3EE !important;
        box-shadow: 0 0 20px rgba(34, 211, 238, 0.3) !important;
        
        /* Brighter text for selected state */
        color: #FFFFFF !important;
        font-weight: 600 !important;
        
        transform: none !important;
    }

    /* Force white text on selected state - override Streamlit */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) *,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) span,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p,
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) div {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* Hide radio circles completely - ULTRA AGGRESSIVE */
    div[data-testid="stRadio"] input[type="radio"],
    div[data-testid="stRadio"] input[type="radio"] + div,
    div[data-testid="stRadio"] span[data-testid="stWidgetLabel"] > div:first-child {
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        pointer-events: none !important;
        clip-path: inset(100%) !important;
    }

    /* Mobile: stack vertically with full-width tiles */
    @media (max-width: 768px) {
        div[data-testid="stRadio"] > div[role="radiogroup"] {
            flex-direction: column !important;
            gap: 12px !important;
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {
            max-width: 100% !important;
            width: 100% !important;
            min-height: 4rem !important;
            padding: 1rem !important;
        }
        
        /* Mobile: left-align the label */
        .mode-selector-label {
            text-align: left !important;
            padding-left: 0 !important;
        }
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

    /* Primary CTA Button */
    .stButton button {
        background: #22D3EE !important;
        color: #1C1C2B !important;
        border-radius: 18px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    /* Force dark text on button - override Streamlit */
    .stButton button *,
    .stButton button p,
    .stButton button span,
    .stButton button div {
        color: #1C1C2B !important;
    }
    
    .stButton button:hover {
        background: #06B6D4 !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(34, 211, 238, 0.5) !important;
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

    /* Brief Container */
    .brief-container {
        background-color: #232335;
        padding: 2.5rem;
        border-radius: 18px;
        border: 1px solid #2F3045;
        margin-top: 2rem;
        color: #E5E7EB;
    }

    footer {display: none !important;}
    header {visibility: hidden;}
    
    </style>
""", unsafe_allow_html=True)



# Main Content
col_spacer, col_content = st.columns([1, 10])

with col_content:
    st.markdown('<h1 class="main-header">Company Intelligence Platform</h1>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize session state for mode
    if 'analysis_mode' not in st.session_state:
        st.session_state.analysis_mode = "Target Account Research"
    
    # Mode selector label
    st.markdown(
        '<p class="mode-selector-label" style="text-align: center; color: #C7C9D3; font-size: 0.9rem; '
        'margin-bottom: 0.75rem; font-weight: 500;">Select your intelligence focus:</p>',
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
    
    # Action Button
    btn_label = "Generate Strategic Brief" if st.session_state.analysis_mode == "Target Account Research" else "Generate Interview Strategy"
    
    if st.button(btn_label, use_container_width=True):
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
