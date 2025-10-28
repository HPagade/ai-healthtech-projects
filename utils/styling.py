"""
Styling utilities for consistent UI across all pages
"""

import streamlit as st


def apply_custom_css():
    """Apply consistent custom CSS styling across all pages"""
    st.markdown("""
    <style>
        /* Main styling */
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1f77b4;
            margin-bottom: 0.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 2rem;
        }

        /* Cards */
        .metric-card {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            border-left: 4px solid #1f77b4;
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #1f77b4;
        }
        .metric-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.5rem;
        }

        /* Info boxes */
        .info-card {
            background-color: #e7f3ff;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #1f77b4;
            margin: 1rem 0;
        }
        .warning-card {
            background-color: #fff3cd;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #ffc107;
            margin: 1rem 0;
        }
        .success-card {
            background-color: #d4edda;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
        }

        /* Buttons */
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #1565a0;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Sidebar styling */
        .css-1d391kg {
            padding-top: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)


def create_metric_card(label, value, delta=None):
    """Create a styled metric card"""
    delta_html = f'<div style="color: #28a745; font-size: 0.9rem;">▲ {delta}</div>' if delta else ''
    return f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """


def create_info_card(message, card_type="info"):
    """
    Create an info/warning/success card
    card_type: 'info', 'warning', or 'success'
    """
    return f'<div class="{card_type}-card">{message}</div>'


def add_page_header(title, subtitle=None, icon=None):
    """Add a consistent page header"""
    title_with_icon = f"{icon} {title}" if icon else title
    st.markdown(f'<div class="main-header">{title_with_icon}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="sub-header">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown("---")


def add_footer():
    """Add a consistent footer"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; padding: 2rem;">
        <p>AI Healthtech Projects Portfolio | Built with Streamlit</p>
        <p><a href="https://github.com/HPagade/ai-healthtech-projects">GitHub</a> |
        <a href="https://linkedin.com/in/hannah-pagade">LinkedIn</a></p>
    </div>
    """, unsafe_allow_html=True)
