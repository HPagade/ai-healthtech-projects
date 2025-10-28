"""
AI Patient Triage Chatbot
Conversational AI agent for symptom assessment and triage
⚠️ EDUCATIONAL PURPOSES ONLY - NOT FOR ACTUAL MEDICAL USE
"""

import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.styling import apply_custom_css, add_page_header
from utils.helpers import check_api_key

st.set_page_config(page_title="AI Patient Triage", page_icon="🤖", layout="wide")
apply_custom_css()

# Medical disclaimer - PROMINENT
st.markdown("""
<div style="background-color: #f8d7da; padding: 1.5rem; border-radius: 8px; border-left: 5px solid #dc3545; margin-bottom: 1.5rem;">
    <h3 style="color: #721c24; margin-top: 0;">⚠️ CRITICAL MEDICAL DISCLAIMER</h3>
    <p style="color: #721c24; margin-bottom: 0;">
    <strong>THIS IS FOR EDUCATIONAL PURPOSES ONLY.</strong><br/>
    This chatbot does NOT provide medical diagnosis or treatment and should NOT be used for medical emergencies or actual healthcare decisions.
    <br/><br/>
    <strong>For emergencies: Call 911 or go to your nearest emergency room.</strong><br/>
    Always consult qualified healthcare professionals for medical advice.
    </p>
</div>
""", unsafe_allow_html=True)

add_page_header("AI Patient Triage Chatbot", "Conversational symptom assessment using AI", "🤖")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False


def get_ai_response(messages, api_key):
    """Get response from OpenAI API"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        system_prompt = """You are a medical triage assistant for educational purposes.
Your role is to:
1. Ask about symptoms in a conversational manner
2. Gather relevant information (duration, severity, other symptoms)
3. Provide GENERAL guidance on urgency level
4. Always remind users this is educational only

Important limitations to mention:
- This is NOT a diagnosis
- This does NOT replace professional medical advice
- For emergencies, always direct to 911 or emergency services

Be empathetic, clear, and thorough. Ask follow-up questions to understand the situation better.
When providing triage assessment, use these levels:
- EMERGENCY: Seek immediate emergency care (911/ER)
- URGENT: See a doctor within 24 hours
- ROUTINE: Schedule a doctor appointment soon
- SELF-CARE: May manage at home with monitoring

Always end with a disclaimer reminding this is educational only."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + messages,
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"


# Sidebar
with st.sidebar:
    st.markdown("### Configuration")

    # Check for API key
    saved_api_key = check_api_key('OPENAI_API_KEY')

    if saved_api_key:
        st.success("✅ API Key configured")
        api_key = saved_api_key
    else:
        st.warning("⚠️ No API key found")
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key"
        )

    st.markdown("---")
    st.markdown("### How to Use")
    st.markdown("""
    1. Enter your symptoms
    2. Answer the chatbot's questions
    3. Receive triage guidance
    4. Remember: Educational only!
    """)

    st.markdown("---")
    st.markdown("### Quick Actions")

    if st.button("🔄 Start New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_started = False
        st.rerun()

    if st.button("💾 Save Conversation", use_container_width=True):
        if st.session_state.messages:
            conversation_text = "\n\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in st.session_state.messages
            ])
            st.download_button(
                "📥 Download Chat Log",
                data=conversation_text,
                file_name=f"triage_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    st.markdown("---")
    st.markdown("### Emergency Numbers")
    st.markdown("""
    **USA:** 911
    **UK:** 999 / 111
    **EU:** 112

    **Poison Control:** 1-800-222-1222
    **Suicide Hotline:** 988
    """)

# Main interface
if not api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to start.")
    st.info("""
    **To get started:**
    1. Get an API key from [OpenAI Platform](https://platform.openai.com/api-keys)
    2. Enter it in the sidebar
    3. Start a conversation about your symptoms

    **Cost:** ~$0.03-0.10 per conversation with GPT-4
    """)
    st.stop()

# Start conversation greeting
if not st.session_state.conversation_started:
    st.markdown("""
    ### Welcome to the AI Triage Assistant

    I'm here to help assess your symptoms and provide guidance on the appropriate level of care.

    **Please remember:**
    - This is for educational purposes only
    - I cannot diagnose or prescribe treatment
    - If you're experiencing a medical emergency, call 911 immediately

    **Start by telling me:** What symptoms are you experiencing?
    """)

    st.session_state.conversation_started = True

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Describe your symptoms..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check for emergency keywords
    emergency_keywords = ['chest pain', 'can\'t breathe', 'difficulty breathing',
                         'unconscious', 'severe bleeding', 'stroke', 'heart attack']

    if any(keyword in prompt.lower() for keyword in emergency_keywords):
        emergency_response = """
🚨 **EMERGENCY ALERT** 🚨

Based on what you've described, this could be a medical emergency.

**IMMEDIATE ACTION REQUIRED:**
- **Call 911 now** (or your local emergency number)
- **Do not drive yourself** to the hospital
- Stay on the line with emergency services
- If alone, unlock your door for emergency responders

This is a potentially life-threatening situation that requires immediate professional medical attention.
        """

        st.session_state.messages.append({"role": "assistant", "content": emergency_response})

        with st.chat_message("assistant"):
            st.error(emergency_response)

    else:
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing symptoms..."):
                response = get_ai_response(
                    [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                    api_key
                )

                st.markdown(response)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

# Show conversation summary if there are messages
if len(st.session_state.messages) > 4:
    with st.expander("📊 Conversation Summary"):
        user_messages = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        st.markdown(f"""
        **Conversation Statistics:**
        - Total messages: {len(st.session_state.messages)}
        - Your messages: {len(user_messages)}
        - Started: {datetime.now().strftime('%Y-%m-%d %H:%M')}

        **Your main concerns:**
        {chr(10).join([f'- {msg[:100]}...' if len(msg) > 100 else f'- {msg}' for msg in user_messages[:3]])}
        """)

# Information tabs at bottom
st.markdown("---")
with st.expander("ℹ️ About This Tool"):
    tab1, tab2, tab3 = st.tabs(["How It Works", "Limitations", "When to Seek Help"])

    with tab1:
        st.markdown("""
        ### How the AI Triage Chatbot Works

        **Technology:**
        - Powered by OpenAI's GPT-4
        - Trained on medical conversation patterns
        - Uses natural language understanding

        **Process:**
        1. **Symptom Collection:** Asks about your symptoms
        2. **Information Gathering:** Follows up with relevant questions
        3. **Assessment:** Evaluates urgency based on responses
        4. **Guidance:** Provides general triage recommendation

        **Triage Levels:**
        - **EMERGENCY:** Life-threatening - Call 911
        - **URGENT:** Needs care within 24 hours
        - **ROUTINE:** Schedule an appointment soon
        - **SELF-CARE:** May manage at home with monitoring
        """)

    with tab2:
        st.markdown("""
        ### Important Limitations

        **This Tool Cannot:**
        - Provide medical diagnosis
        - Prescribe medications
        - Replace a doctor's examination
        - Access your medical history
        - Perform physical examinations
        - Order tests or labs
        - Provide definitive medical advice

        **Why This Matters:**
        - Real diagnosis requires physical examination
        - Medical history affects treatment
        - Lab tests may be necessary
        - Symptoms can have multiple causes
        - Professional judgment is essential

        **Always Remember:**
        This is a demonstration tool showing how AI can assist in healthcare,
        NOT a replacement for actual medical care.
        """)

    with tab3:
        st.markdown("""
        ### When to Seek Immediate Medical Help

        **Call 911 or go to ER immediately if experiencing:**

        **Cardiac/Breathing:**
        - Chest pain or pressure
        - Severe difficulty breathing
        - Choking

        **Neurological:**
        - Sudden severe headache
        - Confusion or altered consciousness
        - Difficulty speaking or weakness on one side
        - Seizures

        **Trauma:**
        - Severe bleeding
        - Major injuries
        - Severe burns

        **Other Emergencies:**
        - Signs of stroke (F.A.S.T.)
        - Severe allergic reactions
        - Poisoning or overdose
        - Suicidal thoughts

        **Seek Urgent Care (within 24 hours) for:**
        - High fever (>103°F)
        - Persistent vomiting/diarrhea
        - Severe pain
        - Signs of infection

        **Trust Your Instincts:**
        If you feel something is seriously wrong, seek immediate medical attention.
        It's better to be cautious.
        """)

# Footer
st.markdown("""
<div style="text-align: center; color: #999; padding: 2rem; margin-top: 2rem; border-top: 1px solid #ddd;">
    <p><strong>Educational Tool</strong> | Not for Medical Use | AI Healthtech Portfolio</p>
    <p style="font-size: 0.9rem;">Powered by OpenAI GPT-4 | Remember: Always consult healthcare professionals</p>
</div>
""", unsafe_allow_html=True)
