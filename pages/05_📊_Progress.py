"""
Progress Tracking Page
Comprehensive dashboard showing learning analytics, achievements, and growth metrics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from collections import defaultdict
from utils.data_manager import data_manager
from utils import get_gemini_helper  # Using the alias from __init__.py

# Page configuration
st.set_page_config(
    page_title="Progress Report | Class 4 Learning Hub",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for progress page
st.markdown("""
<style>
.progress-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    transition: transform 0.3s ease;
}
.progress-card:hover {
    transform: translateY(-5px);
}
.achievement-badge {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem;
    display: inline-block;
    min-width: 120px;
}
.stat-number-large {
    font-size: 2.5rem;
    font-weight: bold;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# Initialize helper - using alias
gemini_helper = get_gemini_helper()

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>📊 Your Learning Journey</h1>
    <p>Track your progress, celebrate achievements, and watch yourself grow! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Get comprehensive progress report
progress_report = data_manager.get_progress_report()
level_info = data_manager.get_current_level()

# Overview Statistics Row
st.markdown("## 📈 Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="progress-card">
        <div style="text-align: center;">
            <div>⭐</div>
            <div class="stat-number-large">{progress_report['total_points']}</div>
            <div><strong>Total Points</strong></div>
            <small>Level {level_info['level']}: {level_info['title']}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    completion_rate = (progress_report['completion_stats']['chapters_completed'] / 20 * 100) if progress_report['completion_stats']['chapters_completed'] > 0 else 0
    st.markdown(f"""
    <div class="progress-card">
        <div style="text-align: center;">
            <div>📚</div>
            <div class="stat-number-large">{progress_report['completion_stats']['chapters_completed']}/20</div>
            <div><strong>Chapters Completed</strong></div>
            <small>{completion_rate:.0f}% Complete</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="progress-card">
        <div style="text-align: center;">
            <div>🏆</div>
            <div class="stat-number-large">{progress_report['completion_stats']['badges_earned']}</div>
            <div><strong>Badges Earned</strong></div>
            <small>Keep going for more!</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_score = progress_report['quiz_stats']['average_score']
    st.markdown(f"""
    <div class="progress-card">
        <div style="text-align: center;">
            <div>📝</div>
            <div class="stat-number-large">{avg_score:.0f}%</div>
            <div><strong>Average Quiz Score</strong></div>
            <small>{progress_report['quiz_stats']['total_quizzes']} quizzes taken</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Level Progress
st.markdown("## 🎯 Level Progress")
col1, col2 = st.columns([2, 1])

with col1:
    if level_info['points_to_next'] > 0:
        current_level_points = progress_report['total_points'] - level_info['points_required']
        progress_percent = min(100, max(0, (current_level_points / level_info['points_to_next']) * 100))
        
        st.markdown(f"""
        <div class="progress-card">
            <div style="margin-bottom: 1rem;">
                <strong>Current Level:</strong> {level_info['level']} - {level_info['title']}
            </div>
            <div style="background: #e0e0e0; border-radius: 15px; overflow: hidden;">
                <div style="width: {progress_percent}%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 30px; border-radius: 15px; display: flex; align-items: center; justify-content: center; color: white;">
                    {progress_percent:.0f}%
                </div>
            </div>
            <div style="margin-top: 0.5rem;">
                <small>🎯 {level_info['points_to_next']} more points to reach {level_info['next_title']}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(f"🏆 MAX LEVEL REACHED! You're a {level_info['title']}! 🏆")

with col2:
    st.markdown(f"""
    <div class="progress-card">
        <div style="text-align: center;">
            <div>🚀</div>
            <div><strong>Next Milestone</strong></div>
            <div style="font-size: 1.2rem;">{level_info['next_title']}</div>
            <small>Level {level_info['level'] + 1}</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Subject Mastery
st.markdown("## 📚 Subject Mastery")

if progress_report['subject_mastery']:
    subjects = list(progress_report['subject_mastery'].keys())
    scores = list(progress_report['subject_mastery'].values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=scores,
        theta=subjects,
        fill='toself',
        marker=dict(color='rgba(102, 126, 234, 0.8)'),
        line=dict(color='#667eea', width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="Subject Mastery Scores (%)",
        height=400,
        margin=dict(l=80, r=80, t=50, b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📊 Take some quizzes to see your subject mastery chart appear here!")

# Quiz Performance Timeline
st.markdown("## 📊 Quiz Performance Over Time")

if st.session_state.quiz_scores:
    quiz_data = []
    for quiz_name, score_data in st.session_state.quiz_scores.items():
        if isinstance(score_data, dict):
            quiz_data.append({
                'Date': score_data.get('date', 'Unknown')[:10],
                'Score': score_data.get('percentage', 0),
                'Quiz': quiz_name[:30]
            })
    
    if quiz_data:
        df = pd.DataFrame(quiz_data)
        df = df.sort_values('Date')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Score'],
            mode='lines+markers',
            name='Quiz Score',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#764ba2')
        ))
        
        fig.update_layout(
            title="Your Learning Progress",
            xaxis_title="Date",
            yaxis_title="Score (%)",
            yaxis_range=[0, 100],
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        if len(df) > 1:
            first_score = df.iloc[0]['Score']
            last_score = df.iloc[-1]['Score']
            improvement = last_score - first_score
            
            if improvement > 0:
                st.success(f"📈 Amazing progress! Your scores have improved by {improvement:.0f}%! 🎉")
            elif improvement < 0:
                st.info(f"💪 Keep practicing! Your scores will improve. You've got this!")
            else:
                st.info(f"🌟 Keep up the consistent work!")
else:
    st.info("🎯 Take your first quiz to start tracking your performance!")

# Study Streak
st.markdown("## 🔥 Study Streak")

col1, col2 = st.columns(2)

with col1:
    current_streak = progress_report['study_stats']['current_streak']
    longest_streak = progress_report['study_stats']['longest_streak']
    
    st.markdown(f"""
    <div class="progress-card">
        <div style="text-align: center;">
            <div style="font-size: 3rem;">🔥</div>
            <div class="stat-number-large">{current_streak}</div>
            <div><strong>Current Streak</strong></div>
            <small>Longest: {longest_streak} days</small>
            <div style="margin-top: 0.5rem;">
                {'⭐' * min(current_streak, 5)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_study_time = progress_report['study_stats']['total_study_time']
    week_study_time = progress_report['study_stats']['week_study_time']
    
    st.markdown(f"""
    <div class="progress-card">
        <div style="text-align: center;">
            <div style="font-size: 3rem;">⏱️</div>
            <div class="stat-number-large">{week_study_time}</div>
            <div><strong>Minutes Studied This Week</strong></div>
            <small>Total: {total_study_time} minutes</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Badges Collection
st.markdown("## 🏅 Your Badge Collection")

if progress_report['badges']:
    badge_cols = st.columns(4)
    for idx, badge in enumerate(progress_report['badges'][:8]):
        with badge_cols[idx % 4]:
            st.markdown(f"""
            <div class="achievement-badge">
                <div style="font-size: 2rem;">🏆</div>
                <div><strong>{badge}</strong></div>
                <small>Achievement unlocked!</small>
            </div>
            """, unsafe_allow_html=True)
    
    if len(progress_report['badges']) > 8:
        st.info(f"And {len(progress_report['badges']) - 8} more badges! Keep collecting! 🌟")
else:
    st.info("🌟 Complete quizzes and study regularly to earn awesome badges!")

# Recent Activity
st.markdown("## 📅 Recent Activity")

recent_activity = data_manager.get_recent_activity(days=7)

if recent_activity:
    for activity in recent_activity:
        with st.expander(f"📅 {activity['day_name']} - {activity['date']}"):
            for act in activity['activities']:
                st.markdown(f"• {act}")
else:
    st.info("Start studying to see your activity timeline here!")

# Milestones
st.markdown("## 🎯 Learning Milestones")

milestones = [
    {"name": "First Quiz", "achieved": len(st.session_state.quiz_scores) >= 1},
    {"name": "100 Points", "achieved": progress_report['total_points'] >= 100},
    {"name": "5 Quizzes", "achieved": len(st.session_state.quiz_scores) >= 5},
    {"name": "250 Points", "achieved": progress_report['total_points'] >= 250},
    {"name": "10 Quizzes", "achieved": len(st.session_state.quiz_scores) >= 10},
    {"name": "500 Points", "achieved": progress_report['total_points'] >= 500},
    {"name": "7-Day Streak", "achieved": progress_report['study_stats']['current_streak'] >= 7}
]

milestone_cols = st.columns(4)
for idx, milestone in enumerate(milestones):
    with milestone_cols[idx % 4]:
        if milestone['achieved']:
            st.success(f"✅ {milestone['name']}")
        else:
            st.info(f"🎯 {milestone['name']}")

# AI-Powered Insights
st.markdown("## 🤖 AI Learning Insights")

if progress_report['quiz_stats']['total_quizzes'] >= 3:
    with st.spinner("AI is analyzing your progress..."):
        insight_prompt = f"""
        Based on this student's learning data:
        - Best subject: {progress_report['quiz_stats']['best_subject']}
        - Average score: {progress_report['quiz_stats']['average_score']:.0f}%
        - Total points: {progress_report['total_points']}
        - Badges earned: {len(progress_report['badges'])}
        
        Provide 3 short, encouraging learning tips for a Class 4 student.
        Keep each tip to 1 sentence. Use emojis.
        """
        
        insights = gemini_helper.generate_response(insight_prompt)
        st.markdown(f"""
        <div class="progress-card">
            <div style="font-size: 1.2rem; margin-bottom: 1rem;">💡 Personalized Study Tips</div>
            {insights}
        </div>
        """, unsafe_allow_html=True)
        
        data_manager.award_points(5, "for reviewing AI learning insights!", category="ai")
else:
    st.info("🤖 Take more quizzes (at least 3) for AI-powered personalized learning insights!")

# AI Status
st.markdown("---")
if gemini_helper.is_available:
    st.success("✅ AI Assistant is ready to provide personalized insights! (Powered by Groq/Llama)")
else:
    st.warning("⚠️ Add your GROQ_API_KEY to Streamlit Secrets to enable AI learning insights.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    🌟 <strong>Remember:</strong> Progress is progress, no matter how small. Keep going, keep growing! 🌟
    <br><br>
    <small>📊 Track your progress daily and celebrate every achievement!</small>
</div>
""", unsafe_allow_html=True)

# Celebration for major milestones
if progress_report['total_points'] >= 1000 and 'milestone_1000' not in st.session_state:
    st.session_state.milestone_1000 = True
    st.balloons()
    st.success("🎉🎉🎉 INCREDIBLE MILESTONE! You've earned 1000 points - You're a Learning Legend! 🎉🎉🎉")

elif progress_report['total_points'] >= 500 and 'milestone_500' not in st.session_state:
    st.session_state.milestone_500 = True
    st.balloons()
    st.success("🎉 AMAZING! You've reached 500 points - Star Learner badge unlocked! 🎉")
