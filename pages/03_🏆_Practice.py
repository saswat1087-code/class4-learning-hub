"""
Practice & Tests Page
Interactive quiz system with multiple question types, scoring, and progress tracking
"""

import streamlit as st
import random
from datetime import datetime
from utils.data_manager import data_manager
from utils import get_gemini_helper
from utils.github_storage import github_storage

# Page configuration
st.set_page_config(
    page_title="Practice & Tests | Class 4 Learning Hub",
    page_icon="🏆",
    layout="wide"
)

# Initialize session state
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'quiz_questions_list' not in st.session_state:
    st.session_state.quiz_questions_list = []
if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = None
if 'quiz_subject' not in st.session_state:
    st.session_state.quiz_subject = None
if 'quiz_chapter' not in st.session_state:
    st.session_state.quiz_chapter = None
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

# Custom CSS
st.markdown("""
<style>
.quiz-container {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
.question-text {
    font-size: 1.3rem;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: #f0f2f6;
    border-radius: 10px;
}
.score-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    margin: 1rem 0;
}
.score-number {
    font-size: 3rem;
    font-weight: bold;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize helpers
gemini_helper = get_gemini_helper()

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🏆 Practice & Assessment Zone</h1>
    <p>Test your knowledge, earn points, and become a learning champion! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Get subjects for quiz selection
subjects = github_storage.get_subjects()

if not st.session_state.quiz_active and not st.session_state.show_results:
    st.markdown("## 🎯 Choose Your Quiz")
    
    if subjects:
        subject_names = [s['name'] for s in subjects]
        selected_subject = st.selectbox("Select Subject:", subject_names)
        
        # Get chapters for selected subject
        subject_data = next((s for s in subjects if s['name'] == selected_subject), None)
        if subject_data:
            chapters = github_storage.get_chapters(subject_data['path'])
            if chapters:
                chapter_names = [c['title'] for c in chapters]
                selected_chapter = st.selectbox("Select Chapter:", chapter_names)
                
                if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
                    # Create sample quiz questions from chapter content
                    chapter_data = next((c for c in chapters if c['title'] == selected_chapter), None)
                    if chapter_data:
                        content = github_storage.get_chapter_content(subject_data['path'], chapter_data['id'])
                        
                        # Create questions from content
                        questions = []
                        if content['practice_questions']:
                            for i, q in enumerate(content['practice_questions'][:5]):
                                questions.append({
                                    'question': q,
                                    'options': ['A) Yes', 'B) No', 'C) Maybe', 'D) Not sure'],
                                    'correct': 'A',
                                    'explanation': 'Think about what you learned in this chapter!'
                                })
                        else:
                            # Fallback questions
                            questions = [
                                {
                                    'question': f"What is the main topic of {selected_chapter}?",
                                    'options': ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4'],
                                    'correct': 'A',
                                    'explanation': 'Review the chapter to find the answer!'
                                }
                            ]
                        
                        st.session_state.quiz_questions_list = questions
                        st.session_state.quiz_subject = selected_subject
                        st.session_state.quiz_chapter = selected_chapter
                        st.session_state.quiz_active = True
                        st.session_state.current_question_index = 0
                        st.session_state.user_answers = []
                        st.session_state.quiz_start_time = datetime.now()
                        st.session_state.show_results = False
                        st.rerun()
            else:
                st.info("No chapters available for this subject yet.")
    else:
        st.info("Loading subjects...")

# Active Quiz Mode
if st.session_state.quiz_active:
    questions = st.session_state.quiz_questions_list
    current_idx = st.session_state.current_question_index
    
    if current_idx < len(questions):
        current_q = questions[current_idx]
        
        # Progress
        progress_value = current_idx / len(questions)
        st.progress(progress_value)
        st.caption(f"Question {current_idx + 1} of {len(questions)}")
        
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">📝 {current_q["question"]}</div>', unsafe_allow_html=True)
        
        st.markdown("### Choose your answer:")
        
        selected_option = st.session_state.user_answers[current_idx] if current_idx < len(st.session_state.user_answers) else None
        
        options = current_q.get('options', ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4'])
        
        for option in options:
            if st.button(option, key=f"q{current_idx}_{option}", use_container_width=True):
                if current_idx >= len(st.session_state.user_answers):
                    st.session_state.user_answers.append(option[0])
                else:
                    st.session_state.user_answers[current_idx] = option[0]
                st.rerun()
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if current_idx < len(questions) - 1:
                if st.button("Next Question ▶", use_container_width=True, type="primary"):
                    if current_idx < len(st.session_state.user_answers):
                        st.session_state.current_question_index += 1
                        st.rerun()
                    else:
                        st.warning("Please select an answer before continuing!")
            else:
                if st.button("📊 Submit Quiz", use_container_width=True, type="primary"):
                    if len(st.session_state.user_answers) == len(questions):
                        score = sum(1 for i, q in enumerate(questions) 
                                   if i < len(st.session_state.user_answers) and 
                                   st.session_state.user_answers[i] == q['correct'])
                        
                        st.session_state.quiz_active = False
                        st.session_state.show_results = True
                        st.session_state.quiz_score = score
                        
                        points_earned = score * 10
                        data_manager.award_points(points_earned, f"for scoring {score}/{len(questions)} on quiz!", category="quiz")
                        
                        st.rerun()
                    else:
                        st.warning(f"Please answer all questions! ({len(st.session_state.user_answers)}/{len(questions)} answered)")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Results Display
if st.session_state.show_results:
    questions = st.session_state.quiz_questions_list
    score = st.session_state.quiz_score
    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0
    
    st.markdown(f"""
    <div class="quiz-container">
        <div style="text-align: center;">
            <h1>🎉 Quiz Completed! 🎉</h1>
    """, unsafe_allow_html=True)
    
    if percentage == 100:
        st.markdown(f"""
        <div class="score-card">
            <div>🏆 PERFECT SCORE! 🏆</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Outstanding! ⭐</div>
        </div>
        """, unsafe_allow_html=True)
    elif percentage >= 70:
        st.markdown(f"""
        <div class="score-card">
            <div>🌟 EXCELLENT! 🌟</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Great job! ⭐</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="score-card">
            <div>💪 KEEP PRACTICING! 💪</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Try again to improve!</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Take Another Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_active = False
            st.session_state.show_results = False
            st.session_state.user_answers = []
            st.session_state.quiz_questions_list = []
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.quiz_active = False
            st.session_state.show_results = False
            st.switch_page("app.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if percentage >= 70:
        st.balloons()

# Quiz Statistics
st.markdown("---")
st.markdown("## 🏆 Your Quiz Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    total_quizzes = len(st.session_state.quiz_scores)
    st.metric("Total Quizzes Taken", total_quizzes)

with col2:
    if st.session_state.quiz_scores:
        avg_score = sum(s.get('percentage', 0) for s in st.session_state.quiz_scores.values()) / len(st.session_state.quiz_scores)
        st.metric("Average Score", f"{avg_score:.0f}%")
    else:
        st.metric("Average Score", "N/A")

with col3:
    st.metric("Points Earned", st.session_state.points_earned)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    💪 Practice makes progress! Every quiz brings you closer to mastery! 🌟
</div>
""", unsafe_allow_html=True)
