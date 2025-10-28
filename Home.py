"""
AI Healthtech Projects Portfolio
Multi-page Streamlit Application
"""

import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Healthtech Portfolio",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/HPagade/ai-healthtech-projects',
        'Report a bug': 'https://github.com/HPagade/ai-healthtech-projects/issues',
        'About': "AI-powered healthcare innovation projects"
    }
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .project-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 5px solid #1f77b4;
    }
    .project-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .project-desc {
        color: #666;
        margin-bottom: 0.5rem;
    }
    .tech-badge {
        display: inline-block;
        background-color: #e1e8f0;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.85rem;
        color: #1f77b4;
    }
    .status-badge {
        display: inline-block;
        background-color: #d4edda;
        color: #155724;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .footer {
        text-align: center;
        color: #999;
        margin-top: 3rem;
        padding: 2rem;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏥 AI Healthtech Projects Portfolio</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Production-Ready AI Solutions for Healthcare Innovation</div>', unsafe_allow_html=True)

# Introduction
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Projects", "8", "100% Complete")
with col2:
    st.metric("Technologies", "10+", "Python, AI, ML")
with col3:
    st.metric("Deployment", "Ready", "Streamlit Cloud")

st.markdown("---")

# Overview
st.markdown("## 🚀 Welcome")
st.markdown("""
This portfolio showcases **8 production-ready AI healthtech projects** built to demonstrate
expertise in healthcare technology, artificial intelligence, and data science. Each project
is fully functional and ready for deployment.

**Navigate using the sidebar** to explore each project. All applications are interactive,
with live demos and full functionality.
""")

st.markdown("---")

# Projects Overview
st.markdown("## 📂 Available Projects")

projects = [
    {
        "icon": "🚀",
        "name": "YC AI Healthtech Startup Tracker",
        "desc": "Analyze 200+ AI and healthcare startups to identify market trends and funding patterns",
        "tech": ["Python", "BeautifulSoup", "Pandas", "Matplotlib"],
        "page": "1_🚀_YC_Tracker"
    },
    {
        "icon": "📊",
        "name": "Customer Health Score Calculator",
        "desc": "Predict customer churn using usage metrics with an interactive dashboard",
        "tech": ["Streamlit", "Pandas", "Plotly", "ML"],
        "page": "2_📊_Health_Score"
    },
    {
        "icon": "🤖",
        "name": "AI Cover Letter Generator",
        "desc": "Automate personalized cover letter creation for startup applications using GPT-4",
        "tech": ["OpenAI GPT-4", "Python", "NLP"],
        "page": "3_🤖_Cover_Letter"
    },
    {
        "icon": "🏥",
        "name": "AI Clinical Decision Support Tool",
        "desc": "Prototype symptom checker using decision trees and machine learning",
        "tech": ["Scikit-learn", "Random Forest", "Healthcare AI"],
        "page": "4_🏥_Clinical_Support"
    },
    {
        "icon": "📈",
        "name": "Startup Job Market Analysis",
        "desc": "Analyze job postings to identify hiring trends, skills demand, and salary ranges",
        "tech": ["Web Scraping", "Data Analysis", "Visualization"],
        "page": "5_📈_Job_Analysis"
    },
    {
        "icon": "💡",
        "name": "AI Healthtech Product Teardown",
        "desc": "Deep strategic analysis framework for leading AI healthtech products",
        "tech": ["Strategic Analysis", "Market Research", "Frameworks"],
        "page": "6_💡_Product_Teardown"
    },
    {
        "icon": "💰",
        "name": "Healthcare Startup Funding Analysis",
        "desc": "Interactive dashboard analyzing AI healthtech funding trends and patterns",
        "tech": ["SQL", "Python", "Tableau", "Data Viz"],
        "page": "7_💰_Funding_Analysis"
    },
    {
        "icon": "🤖",
        "name": "AI Patient Triage Chatbot",
        "desc": "Conversational AI agent for symptom assessment and triage recommendations",
        "tech": ["LangChain", "OpenAI GPT-4", "Streamlit", "Healthcare"],
        "page": "8_🤖_Patient_Triage"
    }
]

# Display projects in a grid
for i in range(0, len(projects), 2):
    col1, col2 = st.columns(2)

    with col1:
        project = projects[i]
        st.markdown(f"""
        <div class="project-card">
            <div class="project-title">{project['icon']} {project['name']}</div>
            <div class="project-desc">{project['desc']}</div>
            <span class="status-badge">✓ Live</span><br/>
            {''.join([f'<span class="tech-badge">{tech}</span>' for tech in project['tech']])}
        </div>
        """, unsafe_allow_html=True)

    if i + 1 < len(projects):
        with col2:
            project = projects[i + 1]
            st.markdown(f"""
            <div class="project-card">
                <div class="project-title">{project['icon']} {project['name']}</div>
                <div class="project-desc">{project['desc']}</div>
                <span class="status-badge">✓ Live</span><br/>
                {''.join([f'<span class="tech-badge">{tech}</span>' for tech in project['tech']])}
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# Key Features
st.markdown("## 🎯 Key Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🔧 Production-Ready
    - Complete implementations
    - Full functionality
    - Error handling
    - User-friendly interfaces
    """)

with col2:
    st.markdown("""
    ### 🤖 AI-Powered
    - GPT-4 integration
    - Machine learning models
    - Natural language processing
    - Intelligent automation
    """)

with col3:
    st.markdown("""
    ### 📊 Data-Driven
    - Real-time analysis
    - Interactive dashboards
    - Comprehensive visualizations
    - Actionable insights
    """)

st.markdown("---")

# Tech Stack
st.markdown("## 🛠️ Technology Stack")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **Core**
    - Python 3.9+
    - Streamlit
    - Pandas
    """)

with col2:
    st.markdown("""
    **AI/ML**
    - OpenAI GPT-4
    - LangChain
    - Scikit-learn
    """)

with col3:
    st.markdown("""
    **Data Viz**
    - Plotly
    - Matplotlib
    - Seaborn
    """)

with col4:
    st.markdown("""
    **Tools**
    - SQL/SQLite
    - BeautifulSoup
    - Git/GitHub
    """)

st.markdown("---")

# Getting Started
with st.expander("📖 Getting Started Guide", expanded=False):
    st.markdown("""
    ### How to Use This Portfolio

    1. **Navigate**: Use the sidebar to select any project
    2. **Interact**: Each project has live, interactive features
    3. **Explore**: Test functionality, upload data, generate results
    4. **Learn**: View code, documentation, and methodology

    ### API Keys Required

    Some projects require API keys:
    - **Project 3 (Cover Letter)**: OpenAI API key
    - **Project 8 (Patient Triage)**: OpenAI API key

    You can add API keys in the sidebar of each project page.

    ### Medical Disclaimer

    Projects 4 and 8 involve medical content but are for **EDUCATIONAL purposes only**.
    Not for actual medical use. Always consult healthcare professionals for medical advice.
    """)

# Footer
st.markdown("""
<div class="footer">
    <p><strong>AI Healthtech Projects Portfolio</strong></p>
    <p>Built with Python, Streamlit, and AI</p>
    <p>© 2024 | <a href="https://github.com/HPagade/ai-healthtech-projects" target="_blank">GitHub</a> |
    <a href="https://linkedin.com/in/hannah-pagade" target="_blank">LinkedIn</a></p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">Last Updated: {}</p>
</div>
""".format(datetime.now().strftime("%B %Y")), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🏥 AI Healthtech Portfolio")
    st.markdown("---")
    st.markdown("""
    ### Quick Navigation
    Select a project from the sidebar to begin.

    ### About
    This portfolio demonstrates expertise in:
    - Healthcare Technology
    - Artificial Intelligence
    - Data Science
    - Product Development

    ### Contact
    - 📧 hannah.pagade@gmail.com
    - 💼 [LinkedIn](https://linkedin.com/in/hannah-pagade)
    - 🌐 [Portfolio](https://hpagade.github.io)
    """)

    st.markdown("---")
    st.markdown("**⭐ Star on GitHub**")
    st.markdown("[View Repository](https://github.com/HPagade/ai-healthtech-projects)")
