"""
AI Patient Triage Chatbot
Conversational AI agent for symptom assessment and triage using LangChain
"""

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, AIMessage
import os


class TriageChatbot:
    """AI chatbot for patient triage and symptom assessment"""

    def __init__(self, api_key=None, model="gpt-4"):
        """
        Initialize the triage chatbot

        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4, gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key required")

        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=model,
            temperature=0.7
        )

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

        self.setup_prompt()

    def setup_prompt(self):
        """Set up the chatbot prompt template"""
        system_message = """You are a helpful and empathetic AI medical triage assistant. Your role is to:

1. Gather information about the patient's symptoms and medical history through natural conversation
2. Ask relevant follow-up questions to understand the severity and context
3. Provide a preliminary assessment and urgency level
4. Recommend appropriate next steps (ER, urgent care, schedule appointment, self-care)

IMPORTANT GUIDELINES:
- Always be empathetic and supportive
- Never provide specific medical diagnoses or treatment recommendations
- Always recommend consulting with a healthcare professional
- Assess urgency levels: Emergency, Urgent, Semi-urgent, Non-urgent
- Ask about: chief complaint, onset, severity, associated symptoms, medical history, medications, allergies
- Watch for red flags requiring immediate emergency care

EMERGENCY RED FLAGS (recommend ER immediately):
- Chest pain or pressure
- Difficulty breathing or shortness of breath
- Sudden severe headache
- Loss of consciousness
- Severe bleeding
- Stroke symptoms (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call 911)
- Severe allergic reaction
- Suicidal thoughts

Remember: You are providing triage guidance, not medical diagnosis. Always direct patients to appropriate healthcare professionals.

Current conversation:
{chat_history}

Patient: {user_input}

AI Medical Assistant:"""

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{user_input}")
        ])

    def chat(self, user_input):
        """
        Process user input and generate response

        Args:
            user_input: User's message

        Returns:
            AI response string
        """
        # Get chat history
        history = self.memory.load_memory_variables({})
        chat_history = history.get('chat_history', [])

        # Format the prompt
        messages = self.prompt.format_messages(
            chat_history=chat_history,
            user_input=user_input
        )

        # Get response
        response = self.llm(messages)

        # Save to memory
        self.memory.save_context(
            {"user_input": user_input},
            {"output": response.content}
        )

        return response.content

    def reset(self):
        """Reset conversation memory"""
        self.memory.clear()

    def get_triage_summary(self):
        """Generate a summary of the triage session"""
        history = self.memory.load_memory_variables({})
        chat_history = history.get('chat_history', [])

        if not chat_history:
            return "No conversation history"

        summary_prompt = f"""Based on this patient conversation, provide a brief triage summary including:
1. Chief complaint
2. Key symptoms
3. Urgency level (Emergency/Urgent/Semi-urgent/Non-urgent)
4. Recommended next steps

Conversation:
{chat_history}

Summary:"""

        response = self.llm([HumanMessage(content=summary_prompt)])
        return response.content


def main():
    """Command-line interface for the chatbot"""
    print("=" * 80)
    print(" " * 25 + "AI PATIENT TRIAGE CHATBOT")
    print("=" * 80)
    print("\nDISCLAIMER: This is a demonstration tool for educational purposes only.")
    print("For medical emergencies, call 911. Always consult healthcare professionals.")
    print("=" * 80 + "\n")

    try:
        chatbot = TriageChatbot()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your OpenAI API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return

    print("Chatbot: Hello! I'm your AI triage assistant. I'm here to help assess your")
    print("         symptoms and guide you to appropriate care. How are you feeling today?\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
            print("\nGenerating triage summary...\n")
            summary = chatbot.get_triage_summary()
            print("=" * 80)
            print("TRIAGE SUMMARY")
            print("=" * 80)
            print(summary)
            print("\n" + "=" * 80)
            print("Thank you for using the AI Triage Assistant. Take care!")
            break

        if user_input.lower() == 'reset':
            chatbot.reset()
            print("\nChatbot: Conversation reset. How can I help you?\n")
            continue

        # Get response
        response = chatbot.chat(user_input)
        print(f"\nChatbot: {response}\n")


if __name__ == "__main__":
    main()
