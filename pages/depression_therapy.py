import streamlit as st
from auth import init_session_state, check_authenticated
import streamlit as st
import random
from config import apply_dark_theme

# Predefined responses and suggestions
RESPONSES = {
    "general": [
        "I hear you, and I want you to know that your feelings are valid.",
        "Thank you for sharing that with me. It takes courage to open up.",
        "You're not alone in this. Many people experience similar feelings.",
        "It's okay to not be okay sometimes. What matters is that you're reaching out.",
        "I'm here to listen and support you."
    ],
    "exercise_suggestions": [
        {
            "title": "Gentle Walking",
            "description": "A 10-minute walk can help clear your mind and boost endorphins.",
            "emoji": "🚶‍♂️"
        },
        {
            "title": "Deep Breathing",
            "description": "Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8.",
            "emoji": "🧘‍♀️"
        },
        {
            "title": "Stretching",
            "description": "Simple stretches can help release physical tension and mental stress.",
            "emoji": "🤸‍♂️"
        },
        {
            "title": "Dancing",
            "description": "Put on your favorite music and move freely for 5 minutes.",
            "emoji": "💃"
        },
        {
            "title": "Yoga",
            "description": "Basic yoga poses can help ground you and reduce anxiety.",
            "emoji": "🧘"
        }
    ],
    "positive_affirmations": [
        "You are stronger than you know 💪",
        "Every small step forward is progress 👣",
        "Your feelings are valid and important ❤️",
        "This moment is temporary ⏳",
        "You deserve peace and happiness 🌟"
    ],
    "emergency_resources": """
    🆘 If you're having thoughts of self-harm or suicide, please reach out:
    
    - National Suicide Prevention Lifeline (US): 988 or 1-800-273-8255
    - Crisis Text Line: Text HOME to 741741
    - Emergency Services: 911 (US) or your local emergency number
    
    These services are available 24/7 and are staffed by caring professionals.
    """
}

def get_exercise_suggestion():
    """Return a random exercise suggestion"""
    suggestion = random.choice(RESPONSES["exercise_suggestions"])
    return f"{suggestion['emoji']} **{suggestion['title']}**\n{suggestion['description']}"

def main():
    # Initialize session state FIRST
    init_session_state()
    check_authenticated()
    # Apply dark theme
    apply_dark_theme()
    
    st.title("💭 Depression Therapy")
    st.write("AI-powered emotional support and mental wellness guidance.")
    
    # Add your depression therapy functionality here
    
    # Introduction
    st.write("""
    Welcome to a safe and supportive space. While I'm not a replacement for 
    professional therapy, I'm here to listen and offer some gentle suggestions 
    for managing difficult emotions through movement and exercise.
    """)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Share what's on your mind..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display response
        with st.chat_message("assistant"):
            response = random.choice(RESPONSES["general"])
            suggestion = get_exercise_suggestion()
            affirmation = random.choice(RESPONSES["positive_affirmations"])
            
            full_response = f"""
            {response}

            Here's a gentle exercise suggestion that might help:
            {suggestion}

            Remember: {affirmation}
            """
            
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    # Sidebar with resources and tips
    st.sidebar.title("💡 Helpful Resources")
    
    with st.sidebar.expander("🆘 Emergency Resources"):
        st.markdown(RESPONSES["emergency_resources"])
    
    with st.sidebar.expander("🌟 Self-Care Tips"):
        st.markdown("""
        - Take one small step at a time
        - Stay hydrated and try to eat regularly
        - Get some sunlight if possible
        - Reach out to someone you trust
        - Remember that rest is productive too
        """)
    
    with st.sidebar.expander("🧘‍♀️ Quick Grounding Exercise"):
        st.markdown("""
        Try the 5-4-3-2-1 technique:
        - 👀 Name 5 things you can see
        - 👆 Touch 4 things around you
        - 👂 Notice 3 sounds you hear
        - 👃 Identify 2 things you can smell
        - 👅 Notice 1 thing you can taste
        """)
    
    # Disclaimer
    st.sidebar.warning("""
    ⚠️ Important: This is not a substitute for professional mental health support. 
    If you're in crisis, please use the emergency resources provided.
    """)

if __name__ == "__main__":
    main() 