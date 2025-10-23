# AI Patient Triage Chatbot

Conversational AI agent for symptom assessment and triage recommendations using LangChain and Streamlit.

**⚠️ MEDICAL DISCLAIMER: This is a demonstration tool for educational purposes ONLY. Do not use for actual medical advice. Always consult healthcare professionals.**

## Features

- Natural language symptom assessment
- Context-aware follow-up questions
- Urgency level classification (Emergency/Urgent/Semi-urgent/Non-urgent)
- Red flag detection for emergencies
- Triage recommendations
- Conversation memory
- Session summaries
- Web interface (Streamlit) and CLI

## Tech Stack

- **Python** - Core language
- **LangChain** - AI agent framework
- **OpenAI GPT-4** - Large language model
- **Streamlit** - Web interface
- **Conversation Memory** - Context retention

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

Or create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your API key
```

## Usage

### Streamlit Web App (Recommended)

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

Features:
- Interactive chat interface
- Real-time responses
- Session management
- Triage summary generation

### Command-Line Interface

```bash
python chatbot.py
```

Interact via terminal:
- Type your symptoms
- Answer questions
- Type 'exit' to get summary and quit
- Type 'reset' to start over

## How It Works

### 1. Symptom Gathering

The chatbot asks about:
- Chief complaint (main symptom)
- Onset and duration
- Severity (1-10 scale)
- Associated symptoms
- Medical history
- Current medications
- Allergies

### 2. Red Flag Detection

Automatically detects emergencies:
- Chest pain/pressure
- Difficulty breathing
- Severe bleeding
- Loss of consciousness
- Stroke symptoms (FAST)
- Severe allergic reactions
- Suicidal thoughts

### 3. Urgency Classification

**🚨 Emergency** - Go to ER immediately:
- Life-threatening symptoms
- Red flag conditions
- Severe pain or distress

**🟠 Urgent** - Seek care today:
- High fever with other symptoms
- Moderate breathing difficulty
- Severe pain
- Persistent vomiting

**🟡 Semi-urgent** - See doctor within 1-3 days:
- Ongoing symptoms
- Minor infections
- Moderate pain

**🟢 Non-urgent** - Self-care or routine appointment:
- Mild symptoms
- Chronic condition management
- Preventive care

### 4. Recommendations

Based on assessment:
- Next steps (ER, urgent care, PCP, self-care)
- What to monitor
- When to seek further care
- General care tips

## Example Conversation

```
User: I've been having chest pain for the past hour

Bot: I understand you're experiencing chest pain. This is important, and I want to gather
     more information. On a scale of 1-10, how would you rate the pain severity?

User: About 7

Bot: That's concerning. A few critical questions:
     1. Is the pain sharp or more of a pressure/squeezing sensation?
     2. Does the pain spread to your arm, jaw, or back?
     3. Are you experiencing shortness of breath or sweating?

User: It's more pressure, and yes, I'm having trouble catching my breath

Bot: ⚠️ EMERGENCY RECOMMENDATION ⚠️

     Based on your symptoms - chest pressure with difficulty breathing - this could be a
     serious medical emergency requiring immediate attention.

     IMMEDIATE ACTION REQUIRED:
     1. Call 911 or have someone drive you to the nearest emergency room NOW
     2. Do not drive yourself
     3. If you have aspirin and are not allergic, chew one 325mg tablet
     4. Sit down and try to remain calm

     These symptoms require urgent evaluation by medical professionals to rule out
     heart attack or other serious conditions.
```

## Safety Features

### Built-in Safeguards

1. **Disclaimer** - Clear warnings about limitations
2. **Red Flag Detection** - Immediate ER recommendations
3. **No Diagnosis** - Avoids specific diagnoses
4. **Professional Referral** - Always recommends consulting doctors
5. **Emergency Escalation** - Clear guidance for serious symptoms

### What the Chatbot WON'T Do

- Provide specific diagnoses
- Prescribe medications
- Replace doctor visits
- Make treatment decisions
- Handle true emergencies (directs to 911)

## Customization

### Adjust Prompt

Edit the system message in `chatbot.py` to:
- Change tone/style
- Add specialty focus (pediatrics, geriatrics)
- Include specific protocols
- Adjust questioning style

### Add Specializations

```python
# Example: Pediatric focus
system_message = """You are a pediatric triage assistant...
Ask about age, immunization status, growth/development..."""
```

### Integrate with EHR

Extend to include:
- Patient history lookup
- Medication lists
- Allergy information
- Previous visits

## Project Structure

```
08-patient-triage-chatbot/
├── chatbot.py              # Core chatbot logic
├── app.py                  # Streamlit web interface
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## API Costs

- GPT-4: ~$0.03-0.06 per conversation
- GPT-3.5-turbo: ~$0.002-0.01 per conversation
- Average conversation: 10-20 messages

## Ethical Considerations

### Responsible AI in Healthcare

1. **Transparency** - Clear about AI limitations
2. **Safety** - Conservative recommendations
3. **Privacy** - No data storage (in this demo)
4. **Accessibility** - Available 24/7
5. **Human Oversight** - Directs to professionals

### Regulatory Compliance

For production use:
- **HIPAA** - Implement encryption, access controls
- **FDA** - May require clearance as SaMD (Software as Medical Device)
- **State Laws** - Telemedicine regulations
- **Liability** - Professional oversight required

## Production Considerations

To make this production-ready:

1. **Clinical Validation** - Test with medical professionals
2. **HIPAA Compliance** - Encryption, audit logs, BAA
3. **Data Privacy** - Secure storage, consent forms
4. **Integration** - EHR connectivity
5. **Monitoring** - Track outcomes, errors
6. **Human Oversight** - Nurse triage review
7. **FDA Clearance** - If making recommendations
8. **Insurance** - Liability coverage

## Future Enhancements

- [ ] Multi-language support
- [ ] Voice interface
- [ ] Image analysis (rashes, injuries)
- [ ] Appointment scheduling integration
- [ ] Follow-up tracking
- [ ] Provider handoff notes
- [ ] Analytics dashboard
- [ ] A/B testing for prompts
- [ ] Integration with wearables
- [ ] Pediatric and geriatric modes

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FDA Guidance on Clinical Decision Support](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software)
- [HIPAA for Developers](https://www.hhs.gov/hipaa/for-professionals/index.html)

## Contributing

Improvements welcome! Areas of focus:
- Clinical accuracy
- Safety features
- User experience
- Accessibility
- Documentation

---

**Remember:** This is a demonstration tool. Real medical triage systems require clinical validation, regulatory approval, and professional oversight.
