"""
Exam Buddy AI Chatbot Page
Interactive AI assistant that helps students with homework, explanations, and study tips
"""

import streamlit as st
from datetime import datetime
from utils.data_manager import data_manager
from utils import get_gemini_helper

# Page configuration
st.set_page_config(
    page_title="Exam Buddy AI | Class 4 Learning Hub",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.chat-container {
    background: #f8f9fa;
    border-radius: 20px;
    padding: 1.5rem;
    height: 500px;
    overflow-y: auto;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}
.message {
    margin: 0.5rem 0;
    padding: 0.8rem 1rem;
    border-radius: 15px;
    max-width: 80%;
    animation: fadeIn 0.3s ease;
}
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    align-self: flex-end;
    margin-left: auto;
    border-bottom-right-radius: 5px;
}
.bot-message {
    background: white;
    color: #2c3e50;
    align-self: flex-start;
    border: 1px solid #e0e0e0;
    border-bottom-left-radius: 5px;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.welcome-emoji {
    font-size: 4rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Initialize helpers
gemini_helper = get_gemini_helper()

# Initialize chat history
if 'chat_messages' not in st.session_state:
    welcome_message = """🌟 **Hi there! I'm Exam Buddy, your AI study partner!** 🌟

I'm here to help you with:
- 📚 **Homework questions** - Just ask anything!
- 🎯 **Study tips** - Learn how to study better
- ✨ **Explanations** - I'll make things super simple

**Try asking me:**
- "Explain photosynthesis"
- "Help me with multiplication"
- "Give me a study tip"

What would you like to learn today? 🚀"""
    
    st.session_state.chat_messages = [
        {"role": "assistant", "content": welcome_message, "timestamp": datetime.now()}
    ]

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <div class="welcome-emoji">🤖</div>
    <h1>Exam Buddy AI Assistant</h1>
    <p>Your 24/7 AI study partner - ask me anything about your schoolwork! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Quick subject buttons
st.markdown("### 📚 Quick Help")
subject_cols = st.columns(5)

subjects = ["Computer Science", "English", "Mathematics", "Science", "Study Tips"]
subject_icons = ["💻", "📖", "🧮", "🔬", "💡"]

for idx, (subject, icon) in enumerate(zip(subjects, subject_icons)):
    with subject_cols[idx]:
        if st.button(f"{icon} {subject}", use_container_width=True):
            with st.spinner("🤖 Thinking..."):
                prompt = f"Give me 2-3 helpful study tips for {subject} for a Class 4 student. Keep it fun with emojis."
                response = gemini_helper.generate_response(prompt)
                st.session_state.chat_messages.append({"role": "user", "content": f"Help me with {subject}", "timestamp": datetime.now()})
                st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                data_manager.award_points(5, f"for asking about {subject}!", category="ai")
            st.rerun()

st.markdown("---")

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for message in st.session_state.chat_messages[-20:]:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="message user-message">
            <strong>👤 You:</strong><br>
            {message["content"]}
            <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.3rem;">
                {message["timestamp"].strftime("%I:%M %p")}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message bot-message">
            <strong>🤖 Exam Buddy:</strong><br>
            {message["content"]}
            <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.3rem;">
                {message["timestamp"].strftime("%I:%M %p")}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Suggested questions for new
