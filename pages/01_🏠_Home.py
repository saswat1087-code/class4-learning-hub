"""
Home Dashboard Page
Main landing page showing overview, progress, and quick actions
"""

import streamlit as st
import random
from datetime import datetime, timedelta
from utils.data_manager import data_manager
from utils.groq_helper import get_groq_helper

# Page configuration
st.set_page_config(
    page_title="Home | Class 4 Learning Hub",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS for home page
st.markdown("""
<style>
/* Welcome banner */
.welcome-banner {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 20px;
    color: white;
    margin-bottom: 2rem;
    animation: fadeIn 0.8s ease;
}

.welcome-banner h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.welcome-banner p {
    font-size: 1.2rem;
    opacity: 0.95;
}

/* Stats cards */
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
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: #667eea;
    margin: 0.5rem 0;
}

.stat-label {
    color: #666;
    font-size: 0.9rem;
}

/* Activity card */
.activity-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border-left: 4px solid #667eea;
}

/* Quick action buttons */
.quick-action-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 0.5rem 0;
}

.quick-action-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Motivation card */
.motivation-card {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin: 1rem 0;
}

/* Progress section */
.progress-section {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.celebration {
    animation: pulse 0.5s ease;
}
</style>
""", unsafe_allow_html=True)

# Initialize helper
gemini_helper = get_gemini_helper()

# Get current level info
level_info = data_manager.get_current_level()

# Welcome Banner
current_hour = datetime.now().hour
greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"

st.markdown(f"""
<div class="welcome-banner">
    <h1>🌟 {greeting}, {st.session_state.user_name}! 👋</h1>
    <p>Ready for an amazing learning adventure today? Let's explore and grow together! 🚀</p>
</div>
""", unsafe_allow_html=True)

# Main layout - 3 columns for stats
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div>⭐</div>
        <div class="stat-number">{st.session_state.points_earned}</div>
        <div class="stat-label">Total Points</div>
        <small>Level {level_info['level']}: {level_info['title']}</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Calculate accuracy
    accuracy = 0
    if st.session_state.total_questions_answered > 0:
        accuracy = (st.session_state.correct_answers / st.session_state.total_questions_answered) * 100
    
    st.markdown(f"""
    <div class="stat-card">
        <div>📊</div>
        <div class="stat-number">{accuracy:.0f}%</div>
        <div class="stat-label">Accuracy Rate</div>
        <small>{st.session_state.correct_answers}/{st.session_state.total_questions_answered} correct</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div>🔥</div>
        <div class="stat-number">{st.session_state.current_streak}</div>
        <div class="stat-label">Day Streak</div>
        <small>Best: {st.session_state.longest_streak} days</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div>🏆</div>
        <div class="stat-number">{len(st.session_state.badges)}</div>
        <div class="stat-label">Badges Earned</div>
        <small>Keep going for more!</small>
    </div>
    """, unsafe_allow_html=True)

# Progress bar for next level
st.markdown('<div class="progress-section">', unsafe_allow_html=True)
st.subheader(f"📈 Journey to {level_info['next_title']}")

# Calculate progress percentage
if level_info['points_to_next'] > 0:
    current_level_points = st.session_state.points_earned - level_info['points_required']
    progress_percent = (current_level_points / level_info['points_to_next']) * 100
    progress_percent = min(100, max(0, progress_percent))
    
    st.progress(progress_percent / 100)
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📍 Current: {level_info['title']} (Level {level_info['level']})")
    with col2:
        st.caption(f"🎯 Next: {level_info['next_title']} • Need {level_info['points_to_next']} more points")
else:
    st.progress(1.0)
    st.success("🏆 MAX LEVEL REACHED! You're a Legendary Learner! 🏆")
st.markdown('</div>', unsafe_allow_html=True)

# Two column layout for main content
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown("## 📚 Today's Learning Path")
    
    # Quick subject selection
    subjects = ["Computer Science", "English Literature", "Mathematics", "Science"]
    selected_subject = st.selectbox("Choose a subject to study:", subjects)
    
    # Chapter suggestions based on what's not completed
    from app import SYLLABUS_DATA  # Import from main app
    
    if selected_subject in SYLLABUS_DATA:
        chapters = list(SYLLABUS_DATA[selected_subject].keys())
        
        # Find uncompleted chapters
        uncompleted = []
        for chapter in chapters:
            chapter_key = f"{selected_subject}: {chapter}"
            if chapter_key not in st.session_state.completed_chapters:
                uncompleted.append(chapter)
        
        if uncompleted:
            suggested_chapter = uncompleted[0]
            st.info(f"📖 **Recommended:** Continue with '{suggested_chapter}'")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📖 Read Chapter", use_container_width=True):
                    st.session_state.selected_subject = selected_subject
                    st.session_state.selected_chapter = suggested_chapter
                    st.switch_page("pages/02_📚_Syllabus.py")
            
            with col2:
                if st.button("📝 Take Quiz", use_container_width=True):
                    st.session_state.quiz_subject = selected_subject
                    st.session_state.quiz_chapter = suggested_chapter
                    st.switch_page("pages/03_🏆_Practice.py")
            
            with col3:
                if st.button("🤖 Ask AI", use_container_width=True):
                    st.session_state.ai_question = f"Help me understand {suggested_chapter}"
                    st.switch_page("pages/04_🤖_Exam_Buddy.py")
        else:
            st.success("🎉 Amazing! You've completed all chapters in this subject!")
            st.balloons()
    
    # Recent activity
    st.markdown("## 📋 Recent Activity")
    recent_activity = data_manager.get_recent_activity(days=5)
    
    if recent_activity:
        for activity in recent_activity:
            with st.expander(f"📅 {activity['day_name']} - {activity['date']}"):
                for act in activity['activities']:
                    st.markdown(f"• {act}")
    else:
        st.info("Start your learning journey to see activity here! 📚")

with right_col:
    # Daily Motivation
    st.markdown("## 💫 Daily Motivation")
    
    motivational_messages = [
        "🌟 \"The expert in anything was once a beginner!\"",
        "📚 \"Every day is a chance to learn something new!\"",
        "🚀 \"Small progress is still progress! Keep going!\"",
        "💪 \"You are capable of amazing things!\"",
        "🎯 \"Don't stop until you're proud!\"",
        "⭐ \"Believe you can and you're halfway there!\"",
        "🌱 \"Learning grows your brain like water grows a plant!\"",
        "🏆 \"Champions keep playing until they get it right!\""
    ]
    
    st.markdown(f"""
    <div class="motivation-card">
        <div style="font-size: 3rem;">✨</div>
        <p style="font-size: 1.1rem; margin-top: 0.5rem;">{random.choice(motivational_messages)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Today's Challenge
    st.markdown("## 🎯 Today's Challenge")
    
    # Generate daily challenge if not exists
    if 'daily_challenge' not in st.session_state or st.session_state.daily_challenge is None:
        challenges = [
            {"task": "Complete 1 quiz", "points": 30},
            {"task": "Read 2 chapters", "points": 40},
            {"task": "Answer 10 questions correctly", "points": 50},
            {"task": "Study for 20 minutes", "points": 35},
            {"task": "Earn 100 points today", "points": 60},
            {"task": "Help another student", "points": 25}
        ]
        st.session_state.daily_challenge = random.choice(challenges)
        st.session_state.daily_challenge_completed = False
    
    if not st.session_state.get('daily_challenge_completed', False):
        st.info(f"""
        🎯 **Challenge:** {st.session_state.daily_challenge['task']}
        
        🎁 **Reward:** {st.session_state.daily_challenge['points']} bonus points!
        """)
        
        if st.button("✅ Mark as Completed", use_container_width=True):
            data_manager.award_points(
                st.session_state.daily_challenge['points'], 
                f"Completed daily challenge: {st.session_state.daily_challenge['task']}",
                category="bonus"
            )
            st.session_state.daily_challenge_completed = True
            st.balloons()
            st.success("🎉 Great job! You completed today's challenge!")
            st.rerun()
    else:
        st.success("✅ Today's challenge completed! Come back tomorrow for a new challenge! 🌟")
    
    # Quick Stats
    st.markdown("## 📊 Quick Stats")
    
    # Study time today
    today = datetime.now().strftime("%Y-%m-%d")
    study_time_today = st.session_state.daily_study_time.get(today, 0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📖 Chapters Done", len(st.session_state.completed_chapters))
    with col2:
        st.metric("📝 Quizzes Taken", len(st.session_state.completed_quizzes))
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⏱️ Study Time Today", f"{study_time_today} min")
    with col2:
        st.metric("🤖 AI Questions", st.session_state.ai_interactions)
    
    # Badge showcase (show recent badges)
    if st.session_state.badges:
        st.markdown("## 🏅 Recent Badges")
        recent_badges = st.session_state.badges[-3:] if len(st.session_state.badges) > 3 else st.session_state.badges
        
        for badge in recent_badges:
            badge_config = data_manager.achievements_config["badges"].get(badge, {})
            icon = badge_config.get("icon", "🏆")
            st.markdown(f"""
            <div class="activity-card">
                {icon} <strong>{badge}</strong><br>
                <small>{badge_config.get('description', 'Achievement unlocked!')}</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Tips section
    with st.expander("💡 Study Tips"):
        tips = [
            "📚 Take short breaks every 25 minutes",
            "✏️ Write down important points",
            "🎯 Set small daily goals",
            "🤔 Ask questions when confused",
            "⭐ Review what you learned before bed",
            "👥 Study with friends sometimes",
            "🏆 Celebrate small victories!"
        ]
        for tip in tips:
            st.markdown(f"• {tip}")

# Featured Projects Section
st.markdown("---")
st.markdown("## 🎨 Featured Projects")

from app import PROJECTS_DATA

project_cols = st.columns(2)
for idx, (project_name, project_desc) in enumerate(PROJECTS_DATA.items()):
    with project_cols[idx % 2]:
        with st.container():
            st.markdown(f"""
            <div class="stat-card">
                <h4>📐 {project_name}</h4>
                <p>{project_desc}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Get Help with {project_name}", key=f"help_{idx}"):
                with st.spinner("Generating project tips..."):
                    prompt = f"Give 3 helpful tips for a Class 4 student working on this project: {project_desc}"
                    tips_response = gemini_helper.generate_response(prompt)
                    st.info(tips_response)

# Learning Resources
st.markdown("---")
st.markdown("## 📚 Recommended Resources")

resource_cols = st.columns(3)

with resource_cols[0]:
    st.markdown("""
    <div class="activity-card">
        <h4>📖 Educational Websites</h4>
        • Khan Academy Kids<br>
        • National Geographic Kids<br>
        • BBC Bitesize
    </div>
    """, unsafe_allow_html=True)

with resource_cols[1]:
    st.markdown("""
    <div class="activity-card">
        <h4>📱 Learning Apps</h4>
        • Duolingo (Languages)<br>
        • Prodigy (Math)<br>
        • Scratch (Coding)
    </div>
    """, unsafe_allow_html=True)

with resource_cols[2]:
    st.markdown("""
    <div class="activity-card">
        <h4>📺 Educational Channels</h4>
        • SciShow Kids<br>
        • Numberphile<br>
        • Crash Course Kids
    </div>
    """, unsafe_allow_html=True)

# Footer with encouragement
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    🌟 <strong>Remember:</strong> Every expert was once a beginner. Keep learning, keep growing! 🌟
    <br>
    <small>Made with ❤️ for Class 4 Students</small>
</div>
""", unsafe_allow_html=True)

# Celebration animation for milestones
if st.session_state.points_earned > 0 and st.session_state.points_earned % 100 == 0:
    # Show celebration for every 100 points
    if 'last_celebration' not in st.session_state or st.session_state.points_earned > st.session_state.get('last_celebration', 0):
        st.session_state.last_celebration = st.session_state.points_earned
        st.balloons()
        st.snow()
        st.success(f"🎉🎉🎉 CONGRATULATIONS! You've reached {st.session_state.points_earned} points! 🎉🎉🎉")
