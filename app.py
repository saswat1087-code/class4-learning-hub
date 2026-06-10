"""
Class 4 Learning Hub - Main Application
An AI-powered interactive learning platform for Class 4 students
"""

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
    
    /* Success/Info/Warning boxes */
    .stAlert {
        border-radius: 10px;
        animation: fadeIn 0.5s ease;
    }
    
    /* Metric styling */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
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
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
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
    
    /* Celebration animation */
    .celebration {
        animation: bounce 0.6s ease;
    }
    
    /* Badge styling */
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
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Responsive design */
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
from utils import get_gemini_helper
from utils.github_storage import github_storage

# Initialize helpers
gemini_helper = get_gemini_helper()

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
        'user_name': os.getenv("STUDENT_NAME", "Mayra"),
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
    
    # User info
    st.markdown(f"### 👋 Hello, {st.session_state.user_name}!")
    
    # Progress metrics
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⭐ Points", st.session_state.points_earned)
    with col2:
        st.metric("🏆 Badges", len(st.session_state.badges))
    
    # Streak display
    if st.session_state.current_streak > 0:
        st.markdown(f"🔥 **Current Streak:** {st.session_state.current_streak} days")
        if st.session_state.longest_streak > 0:
            st.markdown(f"🏆 **Best Streak:** {st.session_state.longest_streak} days")
    
    # Progress bar
    progress_percent = min(st.session_state.points_earned / 500, 1.0)
    st.progress(progress_percent)
    st.caption(f"Level {int(progress_percent * 10) + 1} • Next level: {500 - st.session_state.points_earned} points")
    
    # Navigation
    st.markdown("---")
    app_mode = st.radio(
        "📖 Navigate to:",
        ["🏠 Home Dashboard", "📚 Syllabus & Lessons", "🏆 Practice & Tests", "🤖 Exam Buddy AI", "📊 My Progress", "📁 Resources"],
        index=0
    )
    
    # Parent Zone
    st.markdown("---")
    with st.expander("👨‍👩‍👧 Parent Zone"):
        admin_password = st.text_input("Enter access code:", type="password")
        if admin_password == "class4teacher2026":
            st.success("✅ Access Granted!")
            
            # Get resource statistics
            stats = github_storage.get_total_resources_count()
            
            st.info(f"""
            **Learning Report:**
            - Total Points: {st.session_state.points_earned}
            - Quizzes Taken: {len(st.session_state.quiz_scores)}
            - Chapters Completed: {len(st.session_state.completed_chapters)}
            - Badges: {len(st.session_state.badges)}
            - Current Streak: {st.session_state.current_streak} days
            
            **📚 Available Resources:**
            - Subjects: {stats['subjects']}
            - Chapters: {stats['chapters']}
            - Assignments: {stats['assignments']}
            - Revision Papers: {stats['revision_papers']}
            - Projects: {stats['projects']}
            """)
            
            if st.button("Download Progress Report"):
                report = data_manager.get_progress_report()
                st.download_button(
                    label="📥 Save Report",
                    data=str(report),
                    file_name=f"progress_{datetime.now().strftime('%Y%m%d')}.txt"
                )
        else:
            st.info("🔒 Parent access requires a code")
    
    # AI Status
    st.markdown("---")
    if gemini_helper.is_available:
        st.success("✅ AI Assistant: Ready")
        st.caption("Powered by Groq/Llama")
    else:
        st.warning("⚠️ AI features limited")
        st.caption("Add GROQ_API_KEY to secrets")

# Main content area based on navigation
st.markdown('<div class="main-header">', unsafe_allow_html=True)

if app_mode == "🏠 Home Dashboard":
    st.markdown('<h1>🌟 Welcome to Class 4 Learning Hub!</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>Hello <strong>{st.session_state.user_name}</strong>! Ready for an amazing learning adventure today? 🚀</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get resource statistics
    stats = github_storage.get_total_resources_count()
    
    # Motivational quotes
    motivational_quotes = [
        "💫 \"The more you read, the more things you will know!\"",
        "🎯 \"Practice makes progress, not perfect!\"",
        "🌟 \"Every expert was once a beginner!\"",
        "📚 \"Learning is a treasure that will follow you everywhere!\"",
        "🚀 \"Your attitude determines your direction!\""
    ]
    st.info(random.choice(motivational_quotes))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📚 Your Progress")
        st.write(f"⭐ **Points:** {st.session_state.points_earned}")
        st.write(f"🏆 **Badges:** {len(st.session_state.badges)}")
        st.write(f"📖 **Chapters:** {len(st.session_state.completed_chapters)}/20")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📚 Available Resources")
        st.write(f"📚 **Subjects:** {stats['subjects']}")
        st.write(f"📖 **Chapters:** {stats['chapters']}")
        st.write(f"📝 **Assignments:** {stats['assignments']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Today's Goal")
        remaining = 50 - (st.session_state.points_earned % 50)
        if remaining > 0:
            st.write(f"Earn {remaining} more points to reach next level!")
        else:
            st.write("🎉 You're on a roll! Keep going!")
        if st.button("Take a Quiz →", key="home_quiz"):
            st.switch_page("pages/03_🏆_Practice.py")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("---")
    st.subheader("📖 Quick Actions")
    quick_cols = st.columns(4)
    
    with quick_cols[0]:
        if st.button("📚 Study Materials", use_container_width=True):
            st.switch_page("pages/02_📚_Syllabus.py")
    
    with quick_cols[1]:
        if st.button("📝 Assignments", use_container_width=True):
            st.switch_page("pages/06_📁_Resources.py")
    
    with quick_cols[2]:
        if st.button("🤖 Ask AI", use_container_width=True):
            st.switch_page("pages/04_🤖_Exam_Buddy.py")
    
    with quick_cols[3]:
        if st.button("🏆 View Progress", use_container_width=True):
            st.switch_page("pages/05_📊_Progress.py")

elif app_mode == "📚 Syllabus & Lessons":
    st.switch_page("pages/02_📚_Syllabus.py")

elif app_mode == "🏆 Practice & Tests":
    st.switch_page("pages/03_🏆_Practice.py")

elif app_mode == "🤖 Exam Buddy AI":
    st.switch_page("pages/04_🤖_Exam_Buddy.py")

elif app_mode == "📊 My Progress":
    st.switch_page("pages/05_📊_Progress.py")

elif app_mode == "📁 Resources":
    st.switch_page("pages/06_📁_Resources.py")

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("Made with ❤️ for Class 4 Students | Powered by Groq AI 🚀")
st.markdown('</div>', unsafe_allow_html=True)
