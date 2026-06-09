"""
Exam Buddy AI Chatbot Page
Interactive AI assistant that helps students with homework, explanations, and study tips
"""

import streamlit as st
import time
from datetime import datetime
from utils.data_manager import data_manager
from utils.groq_helper import get_groq_helper

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

/* Typing indicator */
.typing-indicator {
    background: white;
    padding: 0.5rem 1rem;
    border-radius: 15px;
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: #667eea;
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typing {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.5;
    }
    30% {
        transform: translateY(-10px);
        opacity: 1;
    }
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

/* Input area */
.input-container {
    background: white;
    border-radius: 30px;
    padding: 0.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* Features grid */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}

.feature-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: scale(1.05);
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

/* Voice input button */
.voice-btn {
    background: #f44336;
    color: white;
    border: none;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.voice-btn:hover {
    transform: scale(1.1);
    background: #d32f2f;
}

/* Suggestions */
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

# Initialize helper
gemini_helper = get_gemini_helper()

# Initialize session state for chat
if 'chat_messages' not in st.session_state:
    # Welcome message
    welcome_message = """🌟 **Hi there! I'm Exam Buddy, your AI study partner!** 🌟

I'm here to help you with:
- 📚 **Homework questions** - Just ask anything!
- 🎯 **Study tips** - Learn how to study better
- ✨ **Explanations** - I'll make things super simple
- 🧮 **Math help** - Solve problems step by step
- 📖 **Reading help** - Understand stories better
- 🔬 **Science fun** - Cool facts and explanations

**Try asking me:**
- "Explain photosynthesis like I'm 9"
- "Help me with multiplication"
- "Give me a study tip"
- "What's a noun?"

What would you like to learn today? 🚀"""
    
    st.session_state.chat_messages = [
        {"role": "assistant", "content": welcome_message, "timestamp": datetime.now()}
    ]

if 'voice_input' not in st.session_state:
    st.session_state.voice_input = ""
if 'show_suggestions' not in st.session_state:
    st.session_state.show_suggestions = True
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = None

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
            st.session_state.current_subject = subject
            # Add a contextual prompt
            context_prompt = f"I need help with {subject}. Can you help me understand it better?"
            st.session_state.chat_messages.append({"role": "user", "content": context_prompt, "timestamp": datetime.now()})
            
            with st.spinner("🤖 Thinking..."):
                response = gemini_helper.generate_response(f"A student in Class 4 needs help with {subject}. Provide a helpful, encouraging response with 2-3 study tips for this subject. Keep it fun with emojis.")
                st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                data_manager.award_points(5, f"for asking about {subject}!", category="ai")
            st.rerun()

# Features grid
st.markdown("---")
st.markdown("### 🎯 What can I help you with?")

feature_cols = st.columns(4)

features = [
    {"icon": "📝", "name": "Homework Help", "prompt": "Can you help me with my homework?"},
    {"icon": "📖", "name": "Explain Concept", "prompt": "Can you explain [topic] to me simply?"},
    {"icon": "✏️", "name": "Practice Questions", "prompt": "Can you give me some practice questions?"},
    {"icon": "💡", "name": "Study Tips", "prompt": "Give me some study tips please"}
]

for idx, feature in enumerate(features):
    with feature_cols[idx]:
        if st.button(f"{feature['icon']} {feature['name']}", use_container_width=True, key=f"feature_{idx}"):
            st.session_state.chat_messages.append({"role": "user", "content": feature['prompt'], "timestamp": datetime.now()})
            
            with st.spinner("🤖 Thinking..."):
                response = gemini_helper.generate_response(f"A Class 4 student asks: {feature['prompt']}. Respond in a friendly, helpful way with emojis. Keep it simple and encouraging.")
                st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                data_manager.award_points(5, f"for using {feature['name']} feature!", category="ai")
            st.rerun()

st.markdown("---")

# Chat display area
st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

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

# Auto-scroll to bottom
st.markdown("""
<script>
    var container = document.getElementById('chat-container');
    if(container) {
        container.scrollTop = container.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)

# Suggested questions
if st.session_state.show_suggestions and len(st.session_state.chat_messages) < 3:
    st.markdown("### 💡 Suggested Questions")
    
    suggestions = [
        "📖 Can you explain photosynthesis?",
        "🧮 How do I multiply large numbers?",
        "✍️ What's the difference between a noun and a verb?",
        "💻 What is a computer's CPU?",
        "🔬 Why is the sky blue?",
        "📚 How can I study better for exams?",
        "🎯 Can you give me a math challenge?",
        "🌟 Tell me a fun science fact"
    ]
    
    suggestion_cols = st.columns(4)
    for idx, suggestion in enumerate(suggestions[:4]):
        with suggestion_cols[idx]:
            if st.button(suggestion, use_container_width=True, key=f"suggestion_{idx}"):
                st.session_state.chat_messages.append({"role": "user", "content": suggestion, "timestamp": datetime.now()})
                
                with st.spinner("🤖 Thinking..."):
                    # Extract the actual question without emoji
                    clean_question = suggestion.split(" ", 1)[1] if " " in suggestion else suggestion
                    response = gemini_helper.generate_response(f"A Class 4 student asks: {clean_question}. Answer in a fun, simple way with examples. Keep it to 2-3 sentences if possible, but be helpful.")
                    st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                    data_manager.award_points(3, "for asking a question!", category="ai")
                st.rerun()

# Input area
st.markdown("---")
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Create columns for input and buttons
col1, col2 = st.columns([6, 1])

with col1:
    user_input = st.text_area(
        "💬 Type your question here...",
        height=80,
        placeholder="Example: Can you explain how plants make food? or Help me with my math homework...",
        key="user_input",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.button("📤 Send", use_container_width=True, type="primary")
    clear_button = st.button("🗑️ Clear", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle send button
if submit_button and user_input:
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": user_input, "timestamp": datetime.now()})
    
    # Show typing indicator
    with st.spinner("🤖 Exam Buddy is thinking..."):
        # Generate AI response with context
        context = f"""
        You are Exam Buddy, a friendly AI tutor for a 9-year-old Class 4 student.
        
        Rules:
        1. Be encouraging and positive (use emojis 😊, 🌟, 📚)
        2. Keep explanations simple (like explaining to a friend)
        3. Use real-life examples when possible
        4. If it's math, show steps
        5. If you don't know, say "Let me think..." and try your best
        6. Keep responses concise (2-4 sentences for simple questions)
        7. Always end with an encouraging question like "Does that help?" or "Want to learn more?"
        
        Student's question: {user_input}
        
        Remember: You're talking to a 9-year-old. Make learning fun!
        """
        
        response = gemini_helper.generate_response(context)
        
        # Add bot response
        st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
        
        # Award points for asking questions
        data_manager.award_points(3, "for learning with Exam Buddy!", category="ai")
        
        # Hide suggestions after first question
        st.session_state.show_suggestions = False
    
    st.rerun()

# Handle clear button
if clear_button:
    # Reset chat to welcome message
    welcome_message = """🌟 **Welcome back to Exam Buddy!** 🌟

I'm here to help you learn and grow! What would you like to study today?

Try asking me:
- "Help me understand fractions"
- "Explain the water cycle"
- "Give me a study tip"
- "Quiz me on science"

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
    if st.button("📝 Summarize Text", use_container_width=True):
        st.session_state.chat_messages.append({"role": "user", "content": "Can you help me summarize something I paste?", "timestamp": datetime.now()})
        st.session_state.chat_messages.append({"role": "assistant", "content": "Of course! Please paste the text you'd like me to summarize, and I'll make it super simple to understand! 📚", "timestamp": datetime.now()})
        st.rerun()

with tool_cols[1]:
    if st.button("✏️ Check My Answer", use_container_width=True):
        st.session_state.chat_messages.append({"role": "user", "content": "I have an answer I want to check. Can you help?", "timestamp": datetime.now()})
        st.session_state.chat_messages.append({"role": "assistant", "content": "Sure! Share your question and answer with me, and I'll help you check if it's correct. Even if it's not perfect, we'll learn together! 🌟", "timestamp": datetime.now()})
        st.rerun()

with tool_cols[2]:
    if st.button("🎯 Make a Quiz", use_container_width=True):
        st.session_state.chat_messages.append({"role": "user", "content": "Can you create a short quiz for me?", "timestamp": datetime.now()})
        st.session_state.chat_messages.append({"role": "assistant", "content": "I'd love to! Tell me what subject or topic you want to practice, and I'll create some fun quiz questions for you. For example: 'Math multiplication' or 'Science plants' 🎯", "timestamp": datetime.now()})
        st.rerun()

with tool_cols[3]:
    if st.button("💡 Study Motivation", use_container_width=True):
        st.session_state.chat_messages.append({"role": "user", "content": "Give me some motivation to study!", "timestamp": datetime.now()})
        
        with st.spinner("🤖 Thinking..."):
            response = gemini_helper.generate_response("Give an encouraging, motivational message for a 9-year-old student who's studying. Use emojis and make it fun! Keep it to 2-3 sentences.")
            st.session_state.chat_messages.append({"role": "assistant", "content": response, "timestamp": datetime.now()})
            data_manager.award_points(5, "for seeking motivation!", category="ai")
        st.rerun()

# Study tips section
with st.expander("💡 Study Tips from Exam Buddy"):
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("""
        **📚 Effective Study Habits:**
        - 🎯 Study for 25 minutes, then take a 5-minute break
        - ✏️ Take notes while reading
        - 🗣️ Teach what you learned to someone else
        - 📝 Practice with quizzes regularly
        - 🌙 Review before going to sleep
        
        **🎯 Test-Taking Tips:**
        - Read each question twice
        - Eliminate wrong answers first
        - Show your work for math problems
        - Check your answers before submitting
        """)
    
    with tips_col2:
        st.markdown("""
        **🧠 Memory Tricks:**
        - Use acronyms (like ROY G BIV for rainbow colors)
        - Create silly stories to remember facts
        - Draw pictures or diagrams
        - Make flashcards for vocabulary
        - Sing information as a song
        
        **🌟 Stay Motivated:**
        - Set small daily goals
        - Celebrate when you learn something new
        - Take breaks to move around
        - Ask for help when stuck
        - Remember: Every expert was once a beginner!
        """)

# Chat statistics
st.markdown("---")
st.markdown("### 📊 Your Chat Activity")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💬 Total Questions", st.session_state.ai_interactions)

with col2:
    # Calculate questions today
    today = datetime.now().strftime("%Y-%m-%d")
    today_questions = sum(1 for msg in st.session_state.chat_messages 
                         if msg["role"] == "user" and 
                         msg["timestamp"].strftime("%Y-%m-%d") == today)
    st.metric("📝 Questions Today", today_questions)

with col3:
    st.metric("⭐ Points from AI", st.session_state.ai_interactions * 3)

# Feedback section
st.markdown("---")
st.markdown("### 📢 Help Us Improve")

col1, col2 = st.columns([3, 1])

with col1:
    feedback = st.text_input("Was Exam Buddy helpful? Share your feedback:", placeholder="e.g., 'It helped me understand fractions better!'")

with col2:
    if st.button("Submit Feedback", use_container_width=True):
        if feedback:
            st.success("Thank you for your feedback! 🌟")
            data_manager.award_points(10, "for helping improve Exam Buddy!", category="helpful")
            # In production, save feedback to database
        else:
            st.warning("Please enter your feedback before submitting.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    🤖 <strong>Exam Buddy</strong> is here 24/7 to help you learn! Don't be shy - ask anything! 🌟
    <br>
    <small>Remember: There are no silly questions, only opportunities to learn!</small>
</div>
""", unsafe_allow_html=True)

# Auto-scroll JavaScript
st.markdown("""
<script>
    // Auto-scroll to bottom of chat
    function scrollToBottom() {
        const container = document.querySelector('.chat-container');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }
    
    // Call on load and after each update
    window.addEventListener('load', scrollToBottom);
    setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)

# Voice input placeholder (for future enhancement)
if False:  # Disabled for now, requires additional libraries
    st.markdown("""
    <div style="text-align: center; margin-top: 1rem;">
        <button class="voice-btn" onclick="startVoiceInput()">
            🎤
        </button>
        <small>Click to speak your question</small>
    </div>
    """, unsafe_allow_html=True)
