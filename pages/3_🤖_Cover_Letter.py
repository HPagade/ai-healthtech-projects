"""
AI Cover Letter Generator
Automate personalized cover letter creation for startup applications using GPT-4
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Add project directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.styling import apply_custom_css, add_page_header, add_footer
from utils.helpers import check_api_key

# Page configuration
st.set_page_config(
    page_title="AI Cover Letter Generator",
    page_icon="🤖",
    layout="wide"
)

apply_custom_css()

# Initialize session state
if 'cover_letter' not in st.session_state:
    st.session_state.cover_letter = None
if 'generation_count' not in st.session_state:
    st.session_state.generation_count = 0


def generate_cover_letter(api_key, company_name, position, company_description,
                         job_description, user_background, tone="professional"):
    """Generate cover letter using OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"""
Write a compelling cover letter for the following position:

**Company:** {company_name}
**Position:** {position}
**Company Description:** {company_description}

**Job Requirements:**
{job_description}

**Candidate Background:**
{user_background}

**Tone:** {tone}

Create a professional cover letter that:
1. Shows enthusiasm for the company and role
2. Highlights relevant experience and skills
3. Demonstrates understanding of the company's mission
4. Explains why the candidate is a great fit
5. Maintains a {tone} tone throughout
6. Is concise (around 300-400 words)

Format the letter professionally with proper greeting and closing.
"""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert career coach and professional writer specializing in creating compelling cover letters for startup positions in the healthcare and AI sectors."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=800,
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Error generating cover letter: {str(e)}")


# Main header
add_page_header(
    "AI Cover Letter Generator",
    "Create personalized cover letters for startup applications using GPT-4",
    "🤖"
)

# Sidebar - API Key Management
with st.sidebar:
    st.markdown("### API Configuration")

    # Check for API key in secrets or environment
    saved_api_key = check_api_key('OPENAI_API_KEY')

    if saved_api_key:
        st.success("✅ API Key configured")
        api_key = saved_api_key
        use_saved_key = True
    else:
        st.warning("⚠️ No API key found in secrets")
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key. Get one at https://platform.openai.com/api-keys"
        )
        api_key = api_key_input
        use_saved_key = False

    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This tool uses GPT-4 to generate personalized cover letters.

    **Features:**
    - Customizable tone
    - Tailored to job requirements
    - Professional formatting
    - Instant generation

    **Cost:** ~$0.03-0.06 per letter
    """)

    st.markdown("---")
    st.markdown("### Tips for Best Results")
    st.markdown("""
    - Be specific about requirements
    - Include quantifiable achievements
    - Mention company-specific details
    - Highlight relevant skills
    """)

# Check if API key is available
if not api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to use this tool.")
    st.info("""
    **To get started:**
    1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
    2. Enter it in the sidebar
    3. Fill out the form below
    4. Click "Generate Cover Letter"
    """)

# Main form
st.markdown("### 📝 Cover Letter Details")

with st.form("cover_letter_form"):
    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input(
            "Company Name *",
            placeholder="e.g., HealthTech AI",
            help="The company you're applying to"
        )

        position = st.text_input(
            "Position Title *",
            placeholder="e.g., Product Manager",
            help="The role you're applying for"
        )

        tone = st.selectbox(
            "Letter Tone",
            options=["professional", "enthusiastic", "casual"],
            index=0,
            help="The overall tone of the cover letter"
        )

    with col2:
        company_description = st.text_area(
            "Company Description *",
            placeholder="Brief description of the company, its mission, and what it does",
            height=100,
            help="What does the company do? What's their mission?"
        )

    job_description = st.text_area(
        "Job Requirements & Description *",
        placeholder="Key requirements, responsibilities, and what they're looking for",
        height=150,
        help="Paste the job description or summarize key requirements"
    )

    user_background = st.text_area(
        "Your Background & Experience *",
        placeholder="Your relevant experience, skills, achievements, and why you're interested in this role",
        height=150,
        help="Include specific achievements, technologies you know, and relevant experience"
    )

    # Submit button
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        submit_button = st.form_submit_button(
            "✨ Generate Cover Letter",
            use_container_width=True,
            type="primary"
        )
    with col2:
        clear_button = st.form_submit_button(
            "🗑️ Clear Form",
            use_container_width=True
        )

# Handle form submission
if submit_button:
    # Validate inputs
    if not all([company_name, position, company_description, job_description, user_background]):
        st.error("❌ Please fill in all required fields (marked with *)")
    elif not api_key:
        st.error("❌ Please enter your OpenAI API key in the sidebar")
    else:
        with st.spinner("✨ Generating your personalized cover letter..."):
            try:
                cover_letter = generate_cover_letter(
                    api_key=api_key,
                    company_name=company_name,
                    position=position,
                    company_description=company_description,
                    job_description=job_description,
                    user_background=user_background,
                    tone=tone
                )
                st.session_state.cover_letter = cover_letter
                st.session_state.generation_count += 1
                st.success("✅ Cover letter generated successfully!")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if "api_key" in str(e).lower():
                    st.info("Please check that your API key is valid and has credits available.")

if clear_button:
    st.session_state.cover_letter = None
    st.rerun()

# Display generated cover letter
if st.session_state.cover_letter:
    st.markdown("---")
    st.markdown("### 📄 Generated Cover Letter")

    # Display in a nice box
    st.markdown("""
    <style>
    .cover-letter-box {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        font-family: 'Georgia', serif;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="cover-letter-box">{st.session_state.cover_letter}</div>', unsafe_allow_html=True)

    # Action buttons
    st.markdown("### 📥 Download Options")
    col1, col2, col3 = st.columns(3)

    with col1:
        # Download as text
        filename = f"cover_letter_{company_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
        st.download_button(
            label="📄 Download as TXT",
            data=st.session_state.cover_letter,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        # Copy to clipboard button (via text area)
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.code(st.session_state.cover_letter, language=None)
            st.info("Select the text above and copy it (Ctrl+C / Cmd+C)")

    with col3:
        # Generate another version
        if st.button("🔄 Generate Another Version", use_container_width=True):
            st.session_state.cover_letter = None
            st.rerun()

    # Statistics
    word_count = len(st.session_state.cover_letter.split())
    char_count = len(st.session_state.cover_letter)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Word Count", word_count)
    with col2:
        st.metric("Character Count", char_count)
    with col3:
        st.metric("Letters Generated", st.session_state.generation_count)

# Example section
with st.expander("💡 See Example Input & Output"):
    st.markdown("""
    ### Example Application

    **Company:** Vital AI
    **Position:** Senior Product Manager
    **Tone:** Enthusiastic

    **Company Description:**
    Series B healthtech startup building AI diagnostic tools for primary care physicians.
    We're on a mission to make healthcare more accessible and accurate using cutting-edge AI.

    **Job Requirements:**
    - 5+ years product management experience
    - Strong technical background (SQL, APIs)
    - Healthcare software experience
    - Proven ability to ship products
    - Experience with AI/ML products preferred

    **Your Background:**
    7 years product management experience, 4 years in healthcare tech. Led development of
    AI-powered patient triage system at previous company that reduced ER wait times by 40%.
    Strong technical skills including SQL, Python, and API design. MBA from Stanford.
    Passionate about using technology to improve healthcare access.

    ---

    This would generate a personalized cover letter highlighting your relevant experience
    and showing enthusiasm for the company's mission!
    """)

# Pricing information
with st.expander("💰 Pricing & Usage Information"):
    st.markdown("""
    ### OpenAI API Costs

    This tool uses GPT-4, which costs approximately:
    - **$0.03 - $0.06 per cover letter** (depending on length)
    - Input: ~$0.03 per 1K tokens
    - Output: ~$0.06 per 1K tokens

    ### Tips to Minimize Costs:
    1. Be concise in your inputs
    2. Review and edit generated letters rather than regenerating multiple times
    3. Consider using GPT-3.5-turbo for lower cost (modify the code)

    ### Rate Limits:
    - Free tier: 3 requests/minute
    - Paid tier: 3,500 requests/minute

    [View OpenAI Pricing](https://openai.com/pricing)
    """)

add_footer()
