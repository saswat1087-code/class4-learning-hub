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
from utils.gemini_helper import get_gemini_helper

# Page configuration
st.set_page_config(
    page_title="Progress Report | Class 4 Learning Hub",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for progress page
st.markdown("""
<style>
/* Progress cards */
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
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

/* Achievement badge */
.achievement-badge {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem;
    display: inline-block;
    min-width: 120px;
    animation: fadeIn 0.5s ease;
}

/* Milestone tracker */
.milestone-tracker {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
}

.milestone-point {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #e0e0e0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin: 0 0.5rem;
    transition: all 0.3s ease;
}

.milestone-point.achieved {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    animation: bounce 0.5s ease;
}

/* Growth chart */
.growth-chart {
    background: white;
    padding: 1rem;
    border-radius: 15px;
    margin: 1rem 0;
}

/* Certificate card */
.certificate-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    border: 2px solid gold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.certificate-card:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
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
        transform: translateY(-10px);
    }
}

/* Stats number */
.stat-number-large {
    font-size: 2.5rem;
    font-weight: bold;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Heatmap */
.heatmap-cell {
    width: 30px;
    height: 30px;
    background: #e0e0e0;
    margin: 2px;
    display: inline-block;
    border-radius: 5px;
    transition: all 0.3s ease;
}

.heatmap-cell.active {
    background: #4CAF50;
    animation: pulse 0.5s ease;
}

/* Recommendation card */
.recommendation-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.recommendation-card:hover {
    transform: translateX(5px);
}
</style>
""", unsafe_allow_html=True)

# Initialize helper
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
    # Calculate progress to next level
    if level_info['points_to_next'] > 0:
        current_level_points = progress_report['total_points'] - level_info['points_required']
        progress_percent = (current_level_points / level_info['points_to_next']) * 100
        progress_percent = min(100, max(0, progress_percent))
        
        st.markdown(f"""
        <div class="progress-card">
            <div style="margin-bottom: 1rem;">
                <strong>Current Level:</strong> {level_info['level']} - {level_info['title']}
            </div>
            <div class="stProgress">
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
    # Next level preview
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
    
    # Create radar chart for subject mastery
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
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100]
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
    # Prepare data for timeline
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
        
        # Show trend
        if len(df) > 1:
            first_score = df.iloc[0]['Score']
            last_score = df.iloc[-1]['Score']
            improvement = last_score - first_score
            
            if improvement > 0:
                st.success(f"📈 Amazing progress! Your scores have improved by {improvement:.0f}%! 🎉")
            elif improvement < 0:
                st.info(f"💪 Keep practicing! Your scores will improve with more practice. You've got this!")
            else:
                st.info(f"🌟 Keep up the consistent work! You're maintaining good scores!")
else:
    st.info("🎯 Take your first quiz to start tracking your performance!")

# Study Streak and Activity Heatmap
st.markdown("## 🔥 Study Streak & Activity")

col1, col2 = st.columns(2)

with col1:
    # Current streak display
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
                {'⭐' * min(current_streak, 5)} {'🌟' * max(0, current_streak - 5)}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Streak milestones
    if current_streak >= 7:
        st.success("🏆 Amazing! You've earned the 'Streak Champion' badge! Keep going!")
    elif current_streak >= 3:
        st.info("🎯 Great consistency! You're building a strong learning habit!")

with col2:
    # Study time this week
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
    # Display badges in a grid
    badge_cols = st.columns(4)
    for idx, badge in enumerate(progress_report['badges'][:8]):  # Show up to 8 badges
        with badge_cols[idx % 4]:
            badge_config = data_manager.achievements_config["badges"].get(badge, {})
            icon = badge_config.get("icon", "🏆")
            description = badge_config.get("description", "Achievement unlocked!")
            
            st.markdown(f"""
            <div class="achievement-badge">
                <div style="font-size: 2rem;">{icon}</div>
                <div><strong>{badge}</strong></div>
                <small>{description}</small>
            </div>
            """, unsafe_allow_html=True)
    
    if len(progress_report['badges']) > 8:
        st.info(f"And {len(progress_report['badges']) - 8} more badges! Keep collecting! 🌟")
else:
    st.info("🌟 Complete quizzes and study regularly to earn awesome badges! Start your journey today!")

# Recent Activity Timeline
st.markdown("## 📅 Recent Activity")

recent_activity = data_manager.get_recent_activity(days=7)

if recent_activity:
    for activity in recent_activity:
        with st.expander(f"📅 {activity['day_name']} - {activity['date']}"):
            for act in activity['activities']:
                st.markdown(f"• {act}")
else:
    st.info("Start studying to see your activity timeline here!")

# Milestones and Achievements
st.markdown("## 🎯 Learning Milestones")

# Define milestones
milestones = [
    {"name": "First Quiz", "points": 50, "achieved": len(st.session_state.quiz_scores) >= 1},
    {"name": "100 Points", "points": 100, "achieved": progress_report['total_points'] >= 100},
    {"name": "5 Quizzes", "points": 150, "achieved": len(st.session_state.quiz_scores) >= 5},
    {"name": "250 Points", "points": 250, "achieved": progress_report['total_points'] >= 250},
    {"name": "10 Quizzes", "points": 300, "achieved": len(st.session_state.quiz_scores) >= 10},
    {"name": "500 Points", "points": 500, "achieved": progress_report['total_points'] >= 500},
    {"name": "Perfect Score", "points": 400, "achieved": any(score.get('percentage', 0) == 100 for score in st.session_state.quiz_scores.values())},
    {"name": "7-Day Streak", "points": 350, "achieved": progress_report['study_stats']['current_streak'] >= 7}
]

# Display milestones
milestone_cols = st.columns(4)
for idx, milestone in enumerate(milestones):
    with milestone_cols[idx % 4]:
        if milestone['achieved']:
            st.markdown(f"""
            <div class="milestone-tracker" style="background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);">
                <div style="text-align: center;">
                    <div>✅</div>
                    <div><strong>{milestone['name']}</strong></div>
                    <small>Achieved! 🎉</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="milestone-tracker">
                <div style="text-align: center;">
                    <div>🎯</div>
                    <div><strong>{milestone['name']}</strong></div>
                    <small>{milestone['points']} points</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

# AI-Powered Insights and Recommendations
st.markdown("## 🤖 AI Learning Insights")

if progress_report['quiz_stats']['total_quizzes'] >= 3:
    with st.spinner("AI is analyzing your progress..."):
        # Generate personalized insights
        insight_prompt = f"""
        Based on this student's learning data:
        - Best subject: {progress_report['quiz_stats']['best_subject']}
        - Average score: {progress_report['quiz_stats']['average_score']:.0f}%
        - Total points: {progress_report['total_points']}
        - Badges earned: {len(progress_report['badges'])}
        - Study streak: {progress_report['study_stats']['current_streak']} days
        
        Provide 3 personalized learning tips for a Class 4 student.
        Keep each tip short (1 sentence) and encouraging. Use emojis.
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

# Growth Predictions
st.markdown("## 📈 Growth Forecast")

if len(st.session_state.quiz_scores) >= 5:
    # Simple trend prediction
    scores = [score.get('percentage', 0) for score in st.session_state.quiz_scores.values() if isinstance(score, dict)]
    if len(scores) >= 3:
        recent_avg = sum(scores[-3:]) / 3
        overall_avg = sum(scores) / len(scores)
        
        if recent_avg > overall_avg:
            st.success(f"📈 You're on an upward trend! Your last 3 quizzes averaged {recent_avg:.0f}%, which is {recent_avg - overall_avg:.0f}% higher than your overall average. Keep up the great work! 🚀")
        elif recent_avg < overall_avg:
            st.info(f"💪 Your last few quizzes show room for growth. Your overall average is {overall_avg:.0f}%. Try reviewing the chapters before taking quizzes - you'll improve! 🌟")
        else:
            st.info(f"🎯 You're consistently scoring around {overall_avg:.0f}%. To level up, try the 'Study Tips' from Exam Buddy! 📚")
        
        # Projection
        if recent_avg >= 80:
            st.balloons()
            st.success("🏆 EXCELLENT! At this rate, you're on track to become a subject master! Keep challenging yourself!")
elif len(st.session_state.quiz_scores) > 0:
    st.info(f"📊 Take {5 - len(st.session_state.quiz_scores)} more quizzes to unlock growth predictions!")

# Certificate of Achievement
st.markdown("## 🎓 Certificate of Achievement")

if progress_report['total_points'] >= 500 or len(progress_report['badges']) >= 5:
    st.markdown(f"""
    <div class="certificate-card" onclick="alert('Congratulations! 🎓 You\'ve earned a Certificate of Achievement!')">
        <div style="font-size: 3rem;">🎓</div>
        <h3>Certificate of Achievement</h3>
        <p>This certifies that</p>
        <h2>{st.session_state.user_name}</h2>
        <p>has demonstrated outstanding learning progress in Class 4</p>
        <p><strong>{progress_report['total_points']} Points Earned</strong> | <strong>{len(progress_report['badges'])} Badges</strong></p>
        <small>Click to download certificate</small>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📜 Generate Certificate PDF"):
        # Create certificate content
        certificate_content = f"""
        CERTIFICATE OF ACHIEVEMENT
        ===========================
        
        This certifies that
        
        {st.session_state.user_name}
        
        has demonstrated outstanding academic progress
        
        Points Earned: {progress_report['total_points']}
        Badges Collected: {len(progress_report['badges'])}
        Quizzes Completed: {progress_report['quiz_stats']['total_quizzes']}
        Study Streak: {progress_report['study_stats']['current_streak']} days
        
        Date: {datetime.now().strftime("%B %d, %Y")}
        
        Keep shining! 🌟
        """
        
        st.download_button(
            label="📥 Download Certificate",
            data=certificate_content,
            file_name=f"certificate_{st.session_state.user_name}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
else:
    st.info("🎯 Earn 500 points or 5 badges to unlock your Certificate of Achievement! Keep going! 🌟")

# Share Progress
st.markdown("---")
st.markdown("## 📤 Share Your Progress")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📸 Take Progress Screenshot", use_container_width=True):
        st.info("📸 Screenshot saved! Share your progress with parents and teachers!")

with col2:
    if st.button("📧 Email Progress Report", use_container_width=True):
        report_text = data_manager.get_progress_report()
        st.code(report_text, language="markdown")
        st.success("Copy the report above to share via email!")

with col3:
    if st.button("🏆 Share Achievement", use_container_width=True):
        if progress_report['badges']:
            latest_badge = progress_report['badges'][-1]
            st.balloons()
            st.success(f"🎉 I just earned the '{latest_badge}' badge on Class 4 Learning Hub! 📚✨")
        else:
            st.info("Earn your first badge to share your achievement!")

# Parent-Teacher Section
st.markdown("---")
st.markdown("## 👨‍👩‍👧 Parent-Teacher Corner")

with st.expander("📊 Detailed Progress Report for Parents/Teachers"):
    st.markdown("### Comprehensive Learning Analytics")
    
    # Generate detailed report
    detailed_report = f"""
    **Student Name:** {st.session_state.user_name}
    **Report Date:** {datetime.now().strftime("%B %d, %Y")}
    **Grade:** Class 4
    
    **Academic Progress:**
    - Total Learning Points: {progress_report['total_points']}
    - Current Level: {level_info['level']} - {level_info['title']}
    - Chapters Completed: {progress_report['completion_stats']['chapters_completed']}/20
    - Average Quiz Score: {progress_report['quiz_stats']['average_score']:.0f}%
    - Best Subject: {progress_report['quiz_stats']['best_subject'] or 'N/A'}
    
    **Engagement Metrics:**
    - Study Streak: {progress_report['study_stats']['current_streak']} days
    - Longest Streak: {progress_report['study_stats']['longest_streak']} days
    - Total Study Time: {progress_report['study_stats']['total_study_time']} minutes
    - Badges Earned: {len(progress_report['badges'])}
    - Quizzes Completed: {progress_report['quiz_stats']['total_quizzes']}
    
    **Subject Mastery:**
    """
    
    for subject, score in progress_report['subject_mastery'].items():
        detailed_report += f"\n    - {subject}: {score:.0f}%"
    
    detailed_report += f"""
    
    **Recommendations:**
    - Continue encouraging regular study habits
    - Focus on subjects with lower mastery scores
    - Celebrate achievements and milestones
    - Use Exam Buddy AI for additional support
    
    **Notes:**
    The student has shown {'excellent' if progress_report['quiz_stats']['average_score'] >= 80 else 'good' if progress_report['quiz_stats']['average_score'] >= 60 else 'developing'} progress.
    {'Continue the great work!' if progress_report['quiz_stats']['average_score'] >= 70 else 'Encourage consistent practice for improvement.'}
    """
    
    st.markdown(detailed_report)
    
    # Download button for detailed report
    st.download_button(
        label="📥 Download Full Report (JSON)",
        data=str(progress_report),
        file_name=f"progress_report_{st.session_state.user_name}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json"
    )

# Footer with motivation
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    🌟 <strong>Remember:</strong> Progress is progress, no matter how small. Every point, every quiz, every day of studying 
    brings you closer to your goals. Keep going, keep growing! 🌟
    <br><br>
    <small>📊 Track your progress daily and celebrate every achievement!</small>
</div>
""", unsafe_allow_html=True)

# Celebration for major milestones
if progress_report['total_points'] >= 1000 and 'milestone_1000' not in st.session_state:
    st.session_state.milestone_1000 = True
    st.balloons()
    st.snow()
    st.success("🎉🎉🎉 INCREDIBLE MILESTONE! You've earned 1000 points - You're a Learning Legend! 🎉🎉🎉")

elif progress_report['total_points'] >= 500 and 'milestone_500' not in st.session_state:
    st.session_state.milestone_500 = True
    st.balloons()
    st.success("🎉 AMAZING! You've reached 500 points - Star Learner badge unlocked! 🎉")
