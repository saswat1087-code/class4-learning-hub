"""
Exam Buddy AI Chatbot Page
Interactive AI assistant that helps students with homework, explanations, and study tips
"""

import streamlit as st
import time
from datetime import datetime
from utils.data_manager import data_manager
from utils import get_gemini_helper  # Using the alias from __init__.py

# Page configuration
st.set_page_config(
    page_title="Exam Buddy AI | Class 4 Learning Hub",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for chatbot
st.markdown("""
<style>
/* Chat container */
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

/* Message bubbles */
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

/* Quick action buttons */
.quick-action {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 0.2rem;
    display: inline-block;
}

.quick-action:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Subject cards */
.subject-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.subject-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    border-color: #667eea;
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes bounce {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-5px);
    }
}

.welcome-emoji {
    font-size: 4rem;
    animation: bounce 2s infinite;
}

/* Suggestion chips */
.suggestion-chip {
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-block;
    margin: 0.2rem;
    font-size: 0.9rem;
}

.suggestion-chip:hover {
    background: #bbdef5;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# Initialize helper - using alias
gemini_helper = get_gemini_helper()

# Initialize session state for chat
if 'chat_messages' not in st.session_state:
    welcome_message = """🌟 **Hi there! I'm Exam Buddy, your AI study partner!** 🌟

I'm here to help you with:
- 📚 **Homework questions** - Just ask anything!
- 🎯 **Study tips** - Learn how to study better
- ✨ **Explanations** - I'll make things super simple
- 🧮 **Math help** - Solve problems step by step

**Try asking me:**
- "Explain photosynthesis like I'm 9"
- "Help me with multiplication"
- "Give me a study tip"

What would you like to learn today? 🚀"""
    
    st.session_state.chat_messages = [
        {"role": "assistant", "content": welcome_message, "timestamp": datetime.now()}
    ]

if 'show_suggestions' not in st.session_state:
    st.session_state.show_suggestions = True

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <div class="welcome-emoji">🤖</div>
    <h1>Exam Buddy AI Assistant</h1>
    <p>Your 24/7 AI study partner - ask me anything about your schoolwork! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Quick subject selector
st.markdown("### 📚 Quick Subject Help")
subject_cols = st.columns(5)

subjects = ["Computer Science", "English", "Mathematics", "Science", "General"]
subject_icons = ["💻", "📖", "🧮", "🔬", "🎯"]

for idx, (subject, icon) in enumerate(zip(subjects, subject_icons)):
    with subject_cols[idx]:
        if st.button(f"{icon} {subject}", use_container_width=True, key=f"subject_{subject}"):
            with st.spinner("🤖 Thinking..."):
                response = gemini_helper.generate_response(f"A student in Class 4 needs help with {subject}. Provide a helpful, encouraging response with 2-3 study tips for this subject. Keep it fun with emojis.")
                st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                data_manager.award_points(5, f"for asking about {subject}!", category="ai")
            st.rerun()

st.markdown("---")

# Chat display area
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.chat_messages:
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

# Suggested questions for new users
if st.session_state.show_suggestions and len(st.session_state.chat_messages) < 3:
    st.markdown("### 💡 Suggested Questions")
    
    suggestions = [
        "📖 Can you explain photosynthesis?",
        "🧮 How do I multiply large numbers?",
        "✍️ What's the difference between a noun and a verb?",
        "💻 What is a computer's CPU?",
        "🔬 Why is the sky blue?",
        "📚 How can I study better for exams?"
    ]
    
    suggestion_cols = st.columns(3)
    for idx, suggestion in enumerate(suggestions[:3]):
        with suggestion_cols[idx]:
            if st.button(suggestion, use_container_width=True, key=f"suggestion_{idx}"):
                st.session_state.chat_messages.append({"role": "user", "content": suggestion, "timestamp": datetime.now()})
                
                with st.spinner("🤖 Thinking..."):
                    clean_question = suggestion.split(" ", 1)[1] if " " in suggestion else suggestion
                    response = gemini_helper.generate_response(f"A Class 4 student asks: {clean_question}. Answer in a fun, simple way with examples. Keep it to 2-3 sentences.")
                    st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                    data_manager.award_points(3, "for asking a question!", category="ai")
                st.rerun()

# Input area
st.markdown("---")
user_input = st.text_area(
    "💬 Type your question here...",
    height=80,
    placeholder="Example: Can you explain how plants make food? or Help me with my math homework...",
    key="user_input"
)

col1, col2 = st.columns([1, 5])

with col1:
    submit_button = st.button("📤 Send", use_container_width=True, type="primary")

with col2:
    clear_button = st.button("🗑️ Clear Chat", use_container_width=True)

# Handle send button
if submit_button and user_input:
    st.session_state.chat_messages.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
    
    with st.spinner("🤖 Exam Buddy is thinking..."):
        response = gemini_helper.generate_response(user_input)
        st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
        data_manager.award_points(3, "for learning with Exam Buddy!", category="ai")
        st.session_state.show_suggestions = False
    
    st.rerun()

# Handle clear button
if clear_button:
    welcome_message = """🌟 **Welcome back to Exam Buddy!** 🌟

I'm here to help you learn and grow! What would you like to study today?

Try asking me:
- "Help me understand fractions"
- "Explain the water cycle"
- "Give me a study tip"

Let's make learning fun! 🚀"""
    
    st.session_state.chat_messages = [
        {"role": "assistant", "content": welcome_message, "timestamp": datetime.now()}
    ]
    st.session_state.show_suggestions = True
    st.rerun()

# Quick tools section
st.markdown("---")
st.markdown("### 🛠️ Quick Study Tools")

tool_cols = st.columns(4)

with tool_cols[0]:
    if st.button("📝 Get Study Tips", use_container_width=True):
        with st.spinner("🤖 Thinking..."):
            response = gemini_helper.generate_response("Give me 3 study tips for a Class 4 student. Keep it fun with emojis.")
            st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
            data_manager.award_points(5, "for getting study tips!", category="ai")
            st.rerun()

with tool_cols[1]:
    if st.button("💡 Get Motivation", use_container_width=True):
        with st.spinner("🤖 Thinking..."):
            response = gemini_helper.get_motivation()
            st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
            data_manager.award_points(5, "for seeking motivation!", category="ai")
            st.rerun()

with tool_cols[2]:
    if st.button("❓ Explain Concept", use_container_width=True):
        concept = st.text_input("What concept do you want explained?", key="concept_input", placeholder="e.g., Photosynthesis")
        if concept:
            with st.spinner("🤖 Thinking..."):
                response = gemini_helper.explain_concept(concept)
                st.session_state.chat_messages.append({"role": "user", "content": f"Explain: {concept}", "timestamp": datetime.now()})
                st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                data_manager.award_points(5, f"for learning about {concept}!", category="ai")
                st.rerun()

with tool_cols[3]:
    if st.button("✨ Fun Fact", use_container_width=True):
        with st.spinner("🤖 Thinking..."):
            response = gemini_helper.generate_response("Give me a fun educational fact for a 9-year-old. Use emojis.")
            st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
            data_manager.award_points(3, "for learning a fun fact!", category="ai")
            st.rerun()

# Study tips expandable section
with st.expander("💡 Study Tips from Exam Buddy"):
    st.markdown("""
    **📚 Effective Study Habits:**
    - 🎯 Study for 25 minutes, then take a 5-minute break
    - ✏️ Take notes while reading
    - 🗣️ Teach what you learned to someone else
    - 📝 Practice with quizzes regularly
    
    **🧠 Memory Tricks:**
    - Use acronyms (like ROY G BIV for rainbow colors)
    - Create silly stories to remember facts
    - Draw pictures or diagrams
    - Make flashcards for vocabulary
    """)

# Chat statistics
st.markdown("---")
st.markdown("### 📊 Your Chat Activity")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💬 Total Questions", st.session_state.ai_interactions)

with col2:
    today = datetime.now().strftime("%Y-%m-%d")
    today_questions = sum(1 for msg in st.session_state.chat_messages 
                         if msg["role"] == "user" and 
                         msg["timestamp"].strftime("%Y-%m-%d") == today)
    st.metric("📝 Questions Today", today_questions)

with col3:
    st.metric("⭐ Points from AI", st.session_state.ai_interactions * 3)

# AI Status
st.markdown("---")
if gemini_helper.is_available:
    st.success("✅ AI Assistant is connected and ready! (Powered by Groq/Llama)")
else:
    st.warning("⚠️ AI features limited. Please add GROQ_API_KEY to Streamlit Secrets to enable full AI capabilities.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    🤖 <strong>Exam Buddy</strong> is here 24/7 to help you learn! Don't be shy - ask anything! 🌟
    <br>
    <small>Remember: There are no silly questions, only opportunities to learn!</small>
</div>
""", unsafe_allow_html=True)
