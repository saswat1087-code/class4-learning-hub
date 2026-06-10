"""
Home Dashboard Page
Main landing page showing overview, progress, and quick actions
"""

import streamlit as st
import random
from datetime import datetime
from utils.data_manager import data_manager
from utils import get_gemini_helper
from utils.github_storage import github_storage

# Page configuration
st.set_page_config(
    page_title="Home | Class 4 Learning Hub",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS for home page
st.markdown("""
<style>
.welcome-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    animation: fadeIn 0.8s ease;
}
.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s ease;
    margin-bottom: 1rem;
}
.stat-card:hover {
    transform: translateY(-5px);
}
.stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: #667eea;
    margin: 0.5rem 0;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# Initialize helpers
gemini_helper = get_gemini_helper()

# Get current level info
level_info = data_manager.get_current_level()

# Get resource statistics
stats = github_storage.get_total_resources_count()

# Welcome Banner
current_hour = datetime.now().hour
greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"

st.markdown(f"""
<div class="welcome-banner">
    <h1>🌟 {greeting}, {st.session_state.user_name}! 👋</h1>
    <p>Ready for an amazing learning adventure today? Let's explore and grow together! 🚀</p>
</div>
""", unsafe_allow_html=True)

# Stats row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div>⭐</div>
        <div class="stat-number">{st.session_state.points_earned}</div>
        <div>Total Points</div>
        <small>Level {level_info['level']}: {level_info['title']}</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    accuracy = 0
    if st.session_state.total_questions_answered > 0:
        accuracy = (st.session_state.correct_answers / st.session_state.total_questions_answered) * 100
    
    st.markdown(f"""
    <div class="stat-card">
        <div>📊</div>
        <div class="stat-number">{accuracy:.0f}%</div>
        <div>Accuracy Rate</div>
        <small>{st.session_state.correct_answers}/{st.session_state.total_questions_answered} correct</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div>🔥</div>
        <div class="stat-number">{st.session_state.current_streak}</div>
        <div>Day Streak</div>
        <small>Best: {st.session_state.longest_streak} days</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div>🏆</div>
        <div class="stat-number">{len(st.session_state.badges)}</div>
        <div>Badges Earned</div>
        <small>Keep going for more!</small>
    </div>
    """, unsafe_allow_html=True)

# Progress bar
st.markdown("## 📈 Your Progress")

if level_info['points_to_next'] > 0:
    current_level_points = st.session_state.points_earned - level_info['points_required']
    progress_percent = min(100, max(0, (current_level_points / level_info['points_to_next']) * 100))
    st.progress(progress_percent / 100)
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📍 Current: {level_info['title']} (Level {level_info['level']})")
    with col2:
        st.caption(f"🎯 Next: {level_info['next_title']} • Need {level_info['points_to_next']} more points")
else:
    st.progress(1.0)
    st.success("🏆 MAX LEVEL REACHED! 🏆")

# Quick actions
st.markdown("## 📚 Today's Learning Path")

# Get subjects from GitHub
subjects = github_storage.get_subjects()

if subjects:
    subject_names = [s['name'] for s in subjects]
    selected_subject = st.selectbox("Choose a subject to study:", subject_names)
    
    # Find selected subject data
    subject_data = next((s for s in subjects if s['name'] == selected_subject), None)
    
    if subject_data:
        chapters = github_storage.get_chapters(subject_data['path'])
        
        if chapters:
            # Find uncompleted chapters
            uncompleted = []
            for chapter in chapters:
                chapter_key = f"{selected_subject}: {chapter['title']}"
                if chapter_key not in st.session_state.completed_chapters:
                    uncompleted.append(chapter)
            
            if uncompleted:
                suggested_chapter = uncompleted[0]
                st.info(f"📖 **Recommended:** Continue with '{suggested_chapter['title']}'")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📖 Read Chapter", use_container_width=True):
                        st.switch_page("pages/02_📚_Syllabus.py")
                with col2:
                    if st.button("📝 Take Quiz", use_container_width=True):
                        st.switch_page("pages/03_🏆_Practice.py")
                with col3:
                    if st.button("🤖 Ask AI", use_container_width=True):
                        st.switch_page("pages/04_🤖_Exam_Buddy.py")
            else:
                st.success("🎉 Amazing! You've completed all chapters in this subject!")
        else:
            st.info("📚 Chapters coming soon for this subject!")
else:
    st.info("📚 Loading subjects from GitHub...")

# Daily motivation
st.markdown("## 💫 Daily Motivation")

motivational_messages = [
    "🌟 \"The expert in anything was once a beginner!\"",
    "📚 \"Every day is a chance to learn something new!\"",
    "🚀 \"Small progress is still progress! Keep going!\"",
    "💪 \"You are capable of amazing things!\"",
    "🎯 \"Don't stop until you're proud!\"",
    "⭐ \"Believe you can and you're halfway there!\""
]

st.info(random.choice(motivational_messages))

# Resource Statistics
st.markdown("## 📊 Available Resources")

res_col1, res_col2, res_col3, res_col4 = st.columns(4)

with res_col1:
    st.metric("📚 Subjects", stats['subjects'])

with res_col2:
    st.metric("📖 Chapters", stats['chapters'])

with res_col3:
    st.metric("📝 Assignments", stats['assignments'])

with res_col4:
    st.metric("📄 Papers", stats['revision_papers'] + stats['projects'])

# Recent activity
st.markdown("## 📋 Recent Activity")

if st.session_state.completed_chapters:
    st.markdown("**Recently completed chapters:**")
    for chapter in st.session_state.completed_chapters[-3:]:
        st.markdown(f"• ✅ {chapter}")
else:
    st.info("Start your learning journey to see activity here! 📚")

# AI Status
st.markdown("---")
if gemini_helper.is_available:
    st.success("✅ AI Assistant is ready to help! (Powered by Groq/Llama)")
else:
    st.warning("⚠️ Add your GROQ_API_KEY to Streamlit Secrets to enable AI features")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    🌟 <strong>Remember:</strong> Every expert was once a beginner. Keep learning, keep growing! 🌟
    <br>
    <small>Made with ❤️ for Class 4 Students | Powered by GitHub Storage</small>
</div>
""", unsafe_allow_html=True)
