"""
Practice & Tests Page
Interactive quiz system with multiple question types, scoring, and progress tracking
"""

import streamlit as st
import random
import time
from datetime import datetime
from utils.data_manager import data_manager
from utils.groq_helper import get_groq_helper

# Page configuration
st.set_page_config(
    page_title="Practice & Tests | Class 4 Learning Hub",
    page_icon="🏆",
    layout="wide"
)

# Initialize session state for quiz - THIS MUST BE FIRST
if 'quiz_active' not in st.session_state:
    st.session_state.quiz_active = False
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = []
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
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
if 'quiz_type' not in st.session_state:
    st.session_state.quiz_type = None
if 'ai_questions' not in st.session_state:
    st.session_state.ai_questions = []
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}
if 'completed_quizzes' not in st.session_state:
    st.session_state.completed_quizzes = []
if 'subject_scores' not in st.session_state:
    st.session_state.subject_scores = {}

# Custom CSS
st.markdown("""
<style>
.quiz-container {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin: 1rem 0;
    animation: fadeIn 0.5s ease;
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
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# Initialize helper
groq_helper = get_groq_helper()

# Syllabus data for quizzes
SYLLABUS_DATA = {
    "Computer Science": {
        "Chapter 1: Storage and Memory Devices": {
            "questions": [
                {
                    "question": "What does RAM stand for?",
                    "options": ["Readily Available Memory", "Random Access Memory", "Read Access Memory", "Rapid Action Memory"],
                    "correct": "B",
                    "explanation": "RAM stands for Random Access Memory. It's temporary memory that stores data while the computer is on."
                },
                {
                    "question": "Which of these is a secondary storage device?",
                    "options": ["RAM", "CPU", "Pen Drive", "Monitor"],
                    "correct": "C",
                    "explanation": "A pen drive is a secondary storage device. It stores data even when the computer is off."
                },
                {
                    "question": "What makes ROM different from RAM?",
                    "options": ["ROM is faster", "ROM is non-volatile (permanent)", "ROM stores more data", "ROM is cheaper"],
                    "correct": "B",
                    "explanation": "ROM is non-volatile, meaning it keeps data even when the power is turned off."
                }
            ]
        }
    },
    "English Literature": {
        "Chapter 2: The Enchanted Castle": {
            "questions": [
                {
                    "question": "What did the children find in the castle?",
                    "options": ["Treasure", "Sleeping Princess", "Magic Wand", "Dragon"],
                    "correct": "B",
                    "explanation": "The children found a sleeping princess in the hedge maze at the center of the castle."
                }
            ]
        }
    },
    "Mathematics": {
        "Chapter 3: Multiplication": {
            "questions": [
                {
                    "question": "What is 234 × 5?",
                    "options": ["1,070", "1,170", "1,270", "1,370"],
                    "correct": "B",
                    "explanation": "234 × 5 = 1,170"
                }
            ]
        }
    },
    "Science": {
        "Chapter 1: Plants": {
            "questions": [
                {
                    "question": "What do plants need to make their own food?",
                    "options": ["Only water", "Only sunlight", "Sunlight, water, and air", "Only soil"],
                    "correct": "C",
                    "explanation": "Plants need sunlight, water, and carbon dioxide to make food through photosynthesis."
                }
            ]
        }
    }
}

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🏆 Practice & Assessment Zone</h1>
    <p>Test your knowledge, earn points, and become a learning champion! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Quiz selection mode (if no active quiz and not showing results)
if not st.session_state.quiz_active and not st.session_state.show_results:
    st.markdown("## 🎯 Choose Your Quiz")
    
    quiz_type = st.radio(
        "Select quiz type:",
        ["📚 Subject Quiz", "🎲 Random Challenge"],
        horizontal=True
    )
    
    if quiz_type == "📚 Subject Quiz":
        col1, col2 = st.columns(2)
        
        with col1:
            subject = st.selectbox("Select Subject:", list(SYLLABUS_DATA.keys()))
        
        with col2:
            chapters = list(SYLLABUS_DATA[subject].keys())
            chapter = st.selectbox("Select Chapter:", chapters)
        
        if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
            if subject in SYLLABUS_DATA and chapter in SYLLABUS_DATA[subject]:
                questions_data = SYLLABUS_DATA[subject][chapter].get('questions', [])
                if questions_data:
                    st.session_state.quiz_questions_list = questions_data.copy()
                    st.session_state.quiz_subject = subject
                    st.session_state.quiz_chapter = chapter
                    st.session_state.quiz_type = 'syllabus'
                    st.session_state.quiz_active = True
                    st.session_state.current_question_index = 0
                    st.session_state.user_answers = []
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_start_time = datetime.now()
                    st.session_state.show_results = False
                    st.rerun()
                else:
                    st.warning("No questions available for this chapter yet.")
            else:
                st.warning("Please select a subject and chapter.")
    
    elif quiz_type == "🎲 Random Challenge":
        st.info("🎲 Test your general knowledge with random questions!")
        
        num_questions = st.slider("Number of questions:", 3, 5, 3)
        
        if st.button("🎲 Start Random Quiz", use_container_width=True, type="primary"):
            # Create simple random questions
            random_questions = [
                {
                    "question": "What is the capital of India?",
                    "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
                    "correct": "B",
                    "explanation": "New Delhi is the capital of India."
                },
                {
                    "question": "Which planet is known as the Red Planet?",
                    "options": ["Mars", "Jupiter", "Venus", "Saturn"],
                    "correct": "A",
                    "explanation": "Mars is called the Red Planet."
                },
                {
                    "question": "What is 15 × 4?",
                    "options": ["45", "60", "75", "80"],
                    "correct": "B",
                    "explanation": "15 × 4 = 60"
                }
            ]
            
            st.session_state.quiz_questions_list = random_questions[:num_questions]
            st.session_state.quiz_subject = "Random Challenge"
            st.session_state.quiz_chapter = "General Knowledge"
            st.session_state.quiz_type = 'random'
            st.session_state.quiz_active = True
            st.session_state.current_question_index = 0
            st.session_state.user_answers = []
            st.session_state.quiz_score = 0
            st.session_state.quiz_start_time = datetime.now()
            st.session_state.show_results = False
            st.rerun()

# Active Quiz Mode
if st.session_state.quiz_active:
    questions = st.session_state.quiz_questions_list
    current_idx = st.session_state.current_question_index
    
    if current_idx < len(questions):
        current_q = questions[current_idx]
        
        # Progress
        progress_value = (current_idx) / len(questions)
        st.progress(progress_value)
        st.caption(f"Question {current_idx + 1} of {len(questions)}")
        
        # Quiz container
        st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
        
        # Question
        st.markdown(f'<div class="question-text">📝 {current_q["question"]}</div>', unsafe_allow_html=True)
        
        # Options
        st.markdown("### Choose your answer:")
        
        # Store selected answer
        selected_option = st.session_state.user_answers[current_idx] if current_idx < len(st.session_state.user_answers) else None
        
        # Display options
        options = current_q.get('options', [])
        option_letters = ['A', 'B', 'C', 'D']
        
        for i, option in enumerate(options[:4]):
            letter = option_letters[i]
            
            if st.button(
                f"{letter}. {option}",
                key=f"q{current_idx}_opt{letter}",
                use_container_width=True,
                type="primary" if selected_option == letter else "secondary"
            ):
                if current_idx >= len(st.session_state.user_answers):
                    st.session_state.user_answers.append(letter)
                else:
                    st.session_state.user_answers[current_idx] = letter
                st.rerun()
        
        # Navigation buttons
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_idx > 0 and st.button("◀ Previous", use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()
        
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
                        score = 0
                        for i, q in enumerate(questions):
                            if i < len(st.session_state.user_answers) and st.session_state.user_answers[i] == q['correct']:
                                score += 1
                        
                        st.session_state.quiz_score = score
                        st.session_state.quiz_active = False
                        st.session_state.show_results = True
                        
                        total_questions = len(questions)
                        points_earned = score * 10
                        data_manager.award_points(points_earned, f"for scoring {score}/{total_questions} on quiz!", category="quiz")
                        
                        # Save to quiz scores
                        quiz_name = f"{st.session_state.quiz_subject}_{st.session_state.quiz_chapter}"
                        if 'quiz_scores' not in st.session_state:
                            st.session_state.quiz_scores = {}
                        st.session_state.quiz_scores[quiz_name] = {
                            'score': score,
                            'total': total_questions,
                            'percentage': (score/total_questions)*100,
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'subject': st.session_state.quiz_subject
                        }
                        
                        if 'completed_quizzes' not in st.session_state:
                            st.session_state.completed_quizzes = []
                        st.session_state.completed_quizzes.append(quiz_name)
                        
                        st.rerun()
                    else:
                        st.warning(f"Please answer all questions! ({len(st.session_state.user_answers)}/{len(questions)} answered)")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Results Display
if st.session_state.show_results:
    questions = st.session_state.quiz_questions_list
    user_answers = st.session_state.user_answers
    score = st.session_state.quiz_score
    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0
    
    st.markdown(f"""
    <div class="quiz-container">
        <div style="text-align: center;">
            <h1>🎉 Quiz Completed! 🎉</h1>
    """, unsafe_allow_html=True)
    
    # Score card
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
    
    # Detailed results
    st.markdown("### 📝 Review Your Answers")
    
    for i, q in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else "Not answered"
        is_correct = user_answer == q['correct']
        
        st.markdown(f"""
        <div style="background: {'#c8e6c9' if is_correct else '#ffcdd2'}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>Q{i+1}:</strong> {q['question']}<br>
            {'✅' if is_correct else '❌'} <strong>Your answer:</strong> {user_answer}<br>
            <strong>Correct answer:</strong> {q['correct']}<br>
            <strong>💡 Explanation:</strong> {q.get('explanation', 'Keep learning!')}
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

# Quiz Statistics Section
st.markdown("---")
st.markdown("## 🏆 Your Quiz Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    if 'quiz_scores' in st.session_state:
        total_quizzes = len(st.session_state.quiz_scores)
        st.metric("Total Quizzes Taken", total_quizzes)
    else:
        st.metric("Total Quizzes Taken", 0)

with col2:
    if 'quiz_scores' in st.session_state and st.session_state.quiz_scores:
        avg_score = sum(s.get('percentage', 0) for s in st.session_state.quiz_scores.values()) / len(st.session_state.quiz_scores)
        st.metric("Average Score", f"{avg_score:.0f}%")
    else:
        st.metric("Average Score", "N/A")

with col3:
    best_subject = "Math"
    st.metric("Best Subject", best_subject)

# Recent quiz scores
if 'quiz_scores' in st.session_state and st.session_state.quiz_scores:
    st.markdown("### 📊 Recent Quiz Performance")
    
    recent_scores = list(st.session_state.quiz_scores.values())[-5:]
    for score_data in recent_scores:
        percentage = score_data.get('percentage', 0)
        if percentage >= 80:
            st.success(f"📝 {score_data.get('date', 'Unknown')[:10]}: {percentage:.0f}% ⭐")
        elif percentage >= 60:
            st.info(f"📝 {score_data.get('date', 'Unknown')[:10]}: {percentage:.0f}% 📚")
        else:
            st.warning(f"📝 {score_data.get('date', 'Unknown')[:10]}: {percentage:.0f}% 💪")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    💪 Practice makes progress! Every quiz brings you closer to mastery! 🌟
</div>
""", unsafe_allow_html=True)
