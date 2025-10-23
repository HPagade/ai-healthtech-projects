"""
AI Patient Triage Chatbot - Streamlit App
Interactive web interface for the triage chatbot
"""

import streamlit as st
from chatbot import TriageChatbot
import os


# Page configuration
st.set_page_config(
    page_title="AI Patient Triage",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stAlert {
    margin-top: 1rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}
.user-message {
    background-color: #E3F2FD;
}
.bot-message {
    background-color: #F5F5F5;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏥 AI Patient Triage Chatbot")

# Disclaimer
st.error("""
**⚠️ IMPORTANT MEDICAL DISCLAIMER**

This is a demonstration tool for educational purposes ONLY. This chatbot:
- Does NOT provide medical diagnosis or treatment
- Does NOT replace professional medical advice
- Should NOT be used for medical emergencies

**For emergencies: Call 911 or go to your nearest emergency room**

Always consult with qualified healthcare professionals for medical advice.
""")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your OpenAI API key. It will not be stored."
    )

    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')

    # Model selection
    model = st.selectbox(
        "Model",
        ["gpt-4", "gpt-3.5-turbo"],
        help="GPT-4 is more accurate but slower and more expensive"
    )

    # Reset button
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.session_state.chatbot = None
        st.rerun()

    # Info
    st.markdown("---")
    st.markdown("""
    ### How to use:
    1. Describe your symptoms
    2. Answer the chatbot's questions
    3. Review the assessment
    4. Follow recommended next steps

    ### Urgency Levels:
    - 🚨 **Emergency**: Go to ER
    - 🟠 **Urgent**: Urgent care today
    - 🟡 **Semi-urgent**: See doctor soon
    - 🟢 **Non-urgent**: Self-care or routine appointment
    """)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None

# Initialize chatbot
if api_key and st.session_state.chatbot is None:
    try:
        st.session_state.chatbot = TriageChatbot(api_key=api_key, model=model)

        # Add welcome message
        welcome_msg = """Hello! I'm your AI triage assistant. I'm here to help assess your symptoms and guide you to appropriate care.

Please tell me what symptoms or concerns are bringing you here today. I'll ask some questions to better understand your situation."""

        st.session_state.messages.append({
            "role": "assistant",
            "content": welcome_msg
        })
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to start chatting.")
else:
    if prompt := st.chat_input("Describe your symptoms..."):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    response = st.session_state.chatbot.chat(prompt)
                    st.markdown(response)

                    # Add to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response
                    })

                except Exception as e:
                    st.error(f"Error: {e}")

# Summary section
if len(st.session_state.messages) > 2:
    with st.expander("📋 View Triage Summary"):
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                try:
                    summary = st.session_state.chatbot.get_triage_summary()
                    st.markdown("### Triage Summary")
                    st.info(summary)

                    st.markdown("---")
                    st.caption("This summary is for informational purposes only. Please consult with a healthcare professional.")
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

# Footer
st.markdown("---")
st.caption("AI Patient Triage Chatbot v1.0 | For Educational Purposes Only")
