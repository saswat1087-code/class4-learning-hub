import streamlit as st
import os
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Class 4 Learning Hub | AI-Powered Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for kid-friendly styling
def load_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    /* Chat message styling */
    .chat-message {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #4A90E2;
        animation: slideIn 0.5s ease;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 12px 18px;
        margin: 8px 0;
        text-align: right;
        animation: slideInRight 0.5s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .celebration {
        animation: bounce 0.6s ease;
    }
    
    .badge {
        display: inline-block;
        padding: 5px 10px;
        margin: 5px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #666;
        font-size: 0.9rem;
    }
    
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .stButton > button {
            width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# Import utilities
from utils.data_manager import data_manager
from utils.groq_helper import get_groq_helper

# Initialize helpers
groq_helper = get_groq_helper()

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'quiz_scores': {},
        'completed_chapters': [],
        'chat_history': [],
        'points_earned': 0,
        'badges': [],
        'daily_streak': 0,
        'last_active': None,
        'user_name': "Learner",
        'total_questions_answered': 0,
        'correct_answers': 0,
        'study_time': 0,
        'current_streak': 0,
        'longest_streak': 0
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Update daily streak
    if st.session_state.last_active:
        try:
            last_date = datetime.strptime(st.session_state.last_active, "%Y-%m-%d")
            today = datetime.now()
            if (today - last_date).days == 1:
                st.session_state.daily_streak += 1
                st.session_state.current_streak += 1
                if st.session_state.current_streak > st.session_state.longest_streak:
                    st.session_state.longest_streak = st.session_state.current_streak
            elif (today - last_date).days > 1:
                st.session_state.daily_streak = 1
                st.session_state.current_streak = 1
        except:
            pass
    
    st.session_state.last_active = datetime.now().strftime("%Y-%m-%d")

# Initialize session state
init_session_state()

# Helper functions
def award_points(points, reason=""):
    """Award points to the user and check for badges"""
    st.session_state.points_earned += points
    st.session_state.total_questions_answered += 1
    
    if points > 0:
        st.toast(f"🎉 You earned {points} points! {reason}", icon="⭐")
    
    new_badge = check_badges()
    if new_badge:
        st.balloons()
        st.success(f"🏆 Congratulations! You earned the '{new_badge}' badge! 🏆")
    
    return points

def check_badges():
    """Check and award badges based on achievements"""
    badges_to_check = {
        'First Steps': st.session_state.points_earned >= 50,
        'Quiz Starter': len(st.session_state.quiz_scores) >= 1,
        'Knowledge Seeker': len(st.session_state.quiz_scores) >= 3,
        'Chapter Master': len(st.session_state.completed_chapters) >= 3,
        'Perfect Score': any(score.get('percentage', 0) == 100 for score in st.session_state.quiz_scores.values()),
        '100 Points Club': st.session_state.points_earned >= 100,
        'Star Learner': st.session_state.points_earned >= 500,
        'Streak Champion': st.session_state.current_streak >= 7,
        'Learning Legend': st.session_state.points_earned >= 1000
    }
    
    for badge, earned in badges_to_check.items():
        if earned and badge not in st.session_state.badges:
            st.session_state.badges.append(badge)
            return badge
    return None

# Sidebar content
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2948/2948228.png", width=80)
    st.title("🎒 Class 4 Hub")
    
    st.markdown(f"### 👋 Hello, {st.session_state.user_name}!")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⭐ Points", st.session_state.points_earned)
    with col2:
        st.metric("🏆 Badges", len(st.session_state.badges))
    
    if st.session_state.current_streak > 0:
        st.markdown(f"🔥 **Current Streak:** {st.session_state.current_streak} days")
    
    progress_percent = min(st.session_state.points_earned / 500, 1.0)
    st.progress(progress_percent)
    st.caption(f"Level {int(progress_percent * 10) + 1}")
    
    st.markdown("---")
    app_mode = st.radio(
        "📖 Navigate to:",
        ["🏠 Home Dashboard", "📚 Syllabus & Lessons", "🏆 Practice & Tests", "🤖 Exam Buddy AI", "📊 My Progress"],
        index=0
    )
    
    st.markdown("---")
    with st.expander("👨‍👩‍👧 Parent Zone"):
        admin_password = st.text_input("Enter access code:", type="password")
        if admin_password == "class4teacher2026":
            st.success("✅ Access Granted!")
            st.info(f"""
            **Learning Report:**
            - Total Points: {st.session_state.points_earned}
            - Quizzes Taken: {len(st.session_state.quiz_scores)}
            - Chapters Completed: {len(st.session_state.completed_chapters)}
            - Badges: {len(st.session_state.badges)}
            """)
    
    if groq_helper.is_available:
        st.success("✅ AI Assistant: Ready (Groq/Llama)")
    else:
        st.warning("⚠️ AI features limited - Add GROQ_API_KEY")

# Syllabus data
SYLLABUS_DATA = {
    "Computer Science": {
        "Chapter 1: Storage and Memory Devices": "Data is raw facts. Information is processed data. RAM is volatile random-access memory. ROM is non-volatile read-only memory. Hard disks and pen drives are secondary storage.",
        "Chapter 2: GUI Operating System": "An operating system manages computer hardware and software. Windows 11 is a Graphical User Interface (GUI) OS using icons and menus.",
        "Chapter 3: Internet and Email": "The internet connects computers worldwide. Email lets us send messages online. Always be safe online!"
    },
    "English Literature": {
        "Chapter 1: The Magic Garden": "A beautiful garden where flowers and plants can talk. They teach us about friendship and caring for nature.",
        "Chapter 2: The Enchanted Castle": "Gerald, Jimmy, and Kathleen discover a castle with a hedge maze. They find a sleeping princess at the center.",
        "Poem: A Home Song": "The poem describes how a true home is built on love, peace, and coexistence with nature."
    },
    "Mathematics": {
        "Chapter 1: Large Numbers": "Numbers up to 100,000. Learn place value, comparing numbers, and ordering.",
        "Chapter 2: Addition and Subtraction": "Adding and subtracting 5-digit numbers with regrouping.",
        "Chapter 3: Multiplication": "Multiplying 3-digit numbers by 2-digit numbers."
    },
    "Science": {
        "Chapter 1: Plants": "Parts of a plant - roots, stem, leaves, flowers. Photosynthesis and how plants make food.",
        "Chapter 2: Animals": "Classification of animals - herbivores, carnivores, omnivores. Animal habitats.",
        "Chapter 3: Our Body": "Major organs - heart, lungs, brain, stomach. How they work together."
    }
}

PROJECTS_DATA = {
    "English Lit Project": "Task: Create a 3D model of a 'Hanging Garden Tree House' based on the poem 'A Home Song'. Deadline: June 30, 2026.",
    "Science Project": "Task: Make a poster showing the life cycle of a plant.",
    "Computer Project": "Task: Create a digital drawing in MS Paint showing your dream house."
}

# Main content area based on navigation
st.markdown('<div class="main-header">', unsafe_allow_html=True)

if app_mode == "🏠 Home Dashboard":
    st.markdown('<h1>🌟 Welcome to Class 4 Learning Hub!</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>Hello <strong>{st.session_state.user_name}</strong>! Ready for an amazing learning adventure today? 🚀</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    motivational_quotes = [
        "💫 \"The more you read, the more things you will know!\"",
        "🎯 \"Practice makes progress!\"",
        "🌟 \"Every expert was once a beginner!\""
    ]
    st.info(random.choice(motivational_quotes))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📚 Today's Goal")
        st.write("Complete one chapter and earn 50 points!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Daily Challenge")
        st.write("Answer 5 questions correctly today!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏆 Achievements")
        st.write(f"⭐ Total Points: {st.session_state.points_earned}")
        st.write(f"🎖️ Badges: {len(st.session_state.badges)}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📖 Featured Project")
    st.info(f"**{list(PROJECTS_DATA.keys())[0]}**\n\n{list(PROJECTS_DATA.values())[0]}")

elif app_mode == "📚 Syllabus & Lessons":
    st.markdown('<h1>📚 Syllabus & Lessons</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        subject = st.selectbox("📖 Select Subject:", list(SYLLABUS_DATA.keys()))
    
    with col2:
        chapters = list(SYLLABUS_DATA[subject].keys())
        chapter = st.selectbox("📑 Select Chapter:", chapters)
    
    st.markdown("---")
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    st.subheader(f"📖 {chapter}")
    content = SYLLABUS_DATA[subject][chapter]
    st.write(content)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ AI Summary", use_container_width=True):
            with st.spinner("Making it easier to understand..."):
                summary = groq_helper.summarize_content(content)
                st.markdown(f'<div class="chat-message">🤖 <strong>Exam Buddy says:</strong><br>{summary}</div>', unsafe_allow_html=True)
                award_points(5, "for asking for a summary!")
    
    with col2:
        if st.button("✅ Mark as completed", use_container_width=True):
            chapter_key = f"{subject}: {chapter}"
            if chapter_key not in st.session_state.completed_chapters:
                st.session_state.completed_chapters.append(chapter_key)
                award_points(20, f"for completing {chapter}!")
                st.balloons()
                st.success(f"🎉 Great job completing {chapter}! 🌟")
            else:
                st.info("📚 You've already completed this chapter!")

elif app_mode == "🏆 Practice & Tests":
    st.markdown('<h1>🏆 Practice & Tests</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        quiz_subject = st.selectbox("Choose subject:", list(SYLLABUS_DATA.keys()), key="quiz_subject")
    
    with col2:
        quiz_chapter = st.selectbox("Choose chapter:", list(SYLLABUS_DATA[quiz_subject].keys()), key="quiz_chapter")
    
    if st.button("🎲 Generate Quiz", use_container_width=True):
        content = SYLLABUS_DATA[quiz_subject][quiz_chapter]
        with st.spinner("Creating your personalized quiz..."):
            questions = groq_helper.create_quiz_questions(content, num_questions=3)
            if questions:
                st.session_state.quiz_questions = questions
                st.success("✅ Quiz ready! Answer the questions below:")
                
                score = 0
                for i, q in enumerate(questions):
                    st.markdown(f"### Q{i+1}: {q.get('question', 'Question')}")
                    options = q.get('options', [])
                    answer = st.radio(f"Choose your answer for Q{i+1}:", options, key=f"q_{i}")
                    if st.button(f"Check Q{i+1}", key=f"check_{i}"):
                        if answer and answer[0] == q.get('answer', 'A'):
                            st.success("✅ Correct! " + q.get('explanation', 'Great job!'))
                            score += 1
                            award_points(10, "for correct answer!")
                        else:
                            st.info("💡 " + q.get('explanation', 'Keep practicing!'))
                
                if st.button("Submit All"):
                    st.success(f"🎉 You scored {score}/{len(questions)}!")
                    award_points(score * 10, f"for scoring {score}/{len(questions)}!")
            else:
                st.warning("Try the random quiz for now!")

elif app_mode == "🤖 Exam Buddy AI":
    st.markdown('<h1>🤖 Exam Buddy AI</h1>', unsafe_allow_html=True)
    st.markdown('<p>Your AI study partner - ask me anything!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    for message in st.session_state.chat_history[-10:]:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
    
    quick_q_cols = st.columns(3)
    quick_questions = [
        "Help me study for Computer Science",
        "Explain multiplication simply",
        "Give me a fun fact about plants"
    ]
    
    for idx, q in enumerate(quick_questions):
        with quick_q_cols[idx % 3]:
            if st.button(q, use_container_width=True):
                with st.spinner("Thinking..."):
                    response = groq_helper.generate_response(q)
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    award_points(2, "for asking a question!")
                    st.rerun()
    
    user_input = st.text_input("💬 Ask Exam Buddy anything:", key="chat_input")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("🤖 Thinking..."):
            response = groq_helper.generate_response(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            award_points(3, "for learning with Exam Buddy!")
            st.rerun()
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
        st.rerun()

elif app_mode == "📊 My Progress":
    st.markdown('<h1>📊 My Progress Report</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⭐ Total Points", st.session_state.points_earned)
    with col2:
        st.metric("📚 Chapters Done", len(st.session_state.completed_chapters))
    with col3:
        st.metric("🏆 Badges Earned", len(st.session_state.badges))
    with col4:
        st.metric("🔥 Current Streak", f"{st.session_state.current_streak} days")
    
    if st.session_state.badges:
        st.subheader("🏅 Your Badges")
        badge_cols = st.columns(4)
        for idx, badge in enumerate(st.session_state.badges[:8]):
            with badge_cols[idx % 4]:
                st.markdown(f'<div class="badge">🏆 {badge}</div>', unsafe_allow_html=True)
    else:
        st.info("🌟 Complete quizzes and chapters to earn badges!")
    
    if st.session_state.completed_chapters:
        st.subheader("✅ Completed Chapters")
        for chapter in st.session_state.completed_chapters:
            st.success(f"📖 {chapter}")

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("Made with ❤️ for Class 4 Students | Powered by Groq AI 🚀")
st.markdown('</div>', unsafe_allow_html=True)
