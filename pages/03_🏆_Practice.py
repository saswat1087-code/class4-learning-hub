"""
Practice & Tests Page - Multiple Choice Questions from Syllabus Chapters
"""

import streamlit as st
import random
import re
from datetime import datetime
from utils.data_manager import data_manager
from utils import get_gemini_helper
from utils.github_storage import github_storage

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
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}
if 'points_earned' not in st.session_state:
    st.session_state.points_earned = 0

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

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🏆 Practice & Assessment Zone</h1>
    <p>Test your knowledge with multiple choice questions! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Get subjects
subjects = github_storage.get_subjects()

def generate_mcq_from_content(chapter_content: str, chapter_title: str) -> list:
    """Generate multiple choice questions from chapter content"""
    mcqs = []
    
    # Use AI to generate questions
    prompt = f"""
    Based on this Class 4 chapter content about "{chapter_title}":
    
    {chapter_content[:1500]}
    
    Generate 5 multiple choice questions for students. Each question should have:
    - A clear question
    - 4 options (A, B, C, D)
    - The correct answer letter
    - A simple explanation
    
    Format as JSON array:
    [
        {{
            "question": "What is...?",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct": "A",
            "explanation": "Explanation here"
        }}
    ]
    """
    
    try:
        gemini_helper = get_gemini_helper()
        response = gemini_helper.generate_response(prompt, temperature=0.7)
        json_match = re.search(r'\[.*\]', response, re.DOTALL)
        if json_match:
            import json
            mcqs = json.loads(json_match.group())
    except:
        pass
    
    return mcqs

if not st.session_state.quiz_active and not st.session_state.show_results:
    st.markdown("## 🎯 Choose Your Quiz")
    
    if subjects:
        # Subject selection
        subject_names = [s['name'] for s in subjects]
        selected_subject = st.selectbox("Select Subject:", subject_names)
        
        subject_data = next((s for s in subjects if s['name'] == selected_subject), None)
        
        if subject_data:
            # Get chapters for selected subject
            chapters = github_storage.get_chapters(subject_data['folder_name'])
            
            if chapters:
                chapter_names = [c['title'] for c in chapters]
                selected_chapter = st.selectbox("Select Chapter:", chapter_names)
                
                col1, col2 = st.columns(2)
                with col1:
                    num_questions = st.selectbox("Number of questions:", [3, 5, 10], index=1)
                
                if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
                    chapter_data = next((c for c in chapters if c['title'] == selected_chapter), None)
                    if chapter_data:
                        content = github_storage.get_chapter_content(subject_data['folder_name'], chapter_data['id'])
                        chapter_content = content.get('content', '')
                        
                        if chapter_content:
                            with st.spinner("Generating questions..."):
                                questions = generate_mcq_from_content(chapter_content, selected_chapter)
                                if questions:
                                    selected_questions = random.sample(questions, min(num_questions, len(questions)))
                                else:
                                    # Fallback questions
                                    selected_questions = [
                                        {"question": f"What is the main topic of {selected_chapter}?", 
                                         "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                                         "correct": "A", "explanation": "Review the chapter to find the answer."}
                                    ] * num_questions
                                
                                st.session_state.quiz_questions_list = selected_questions[:num_questions]
                                st.session_state.quiz_subject = selected_subject
                                st.session_state.quiz_chapter = selected_chapter
                                st.session_state.quiz_active = True
                                st.session_state.current_question_index = 0
                                st.session_state.user_answers = []
                                st.session_state.quiz_score = 0
                                st.session_state.show_results = False
                                st.rerun()
                        else:
                            st.warning("No content available for this chapter yet.")
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
        
        st.progress((current_idx) / len(questions))
        st.caption(f"Question {current_idx + 1} of {len(questions)}")
        
        st.markdown(f"""
        <div class="quiz-container">
            <div class="question-text">
                📝 {current_q.get('question', 'Question not available')}
            </div>
        """, unsafe_allow_html=True)
        
        options = current_q.get('options', [
            "A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"
        ])
        
        answer_key = f"mcq_answer_{current_idx}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = None
        
        selected_option = st.radio(
            "Choose your answer:",
            options,
            key=f"radio_{current_idx}",
            label_visibility="collapsed",
            index=None
        )
        
        if selected_option:
            selected_letter = selected_option[0]
            st.session_state[answer_key] = selected_letter
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if current_idx < len(questions) - 1:
                if st.button("Next Question ▶", use_container_width=True, type="primary"):
                    if st.session_state[answer_key] is not None:
                        if current_idx >= len(st.session_state.user_answers):
                            st.session_state.user_answers.append(st.session_state[answer_key])
                        else:
                            st.session_state.user_answers[current_idx] = st.session_state[answer_key]
                        st.session_state.current_question_index += 1
                        st.rerun()
                    else:
                        st.warning("Please select an answer before continuing!")
            else:
                if st.button("📊 Submit Quiz", use_container_width=True, type="primary"):
                    if st.session_state[answer_key] is not None:
                        if current_idx >= len(st.session_state.user_answers):
                            st.session_state.user_answers.append(st.session_state[answer_key])
                        else:
                            st.session_state.user_answers[current_idx] = st.session_state[answer_key]
                        
                        score = 0
                        for i, q in enumerate(questions):
                            if i < len(st.session_state.user_answers) and st.session_state.user_answers[i] == q.get('correct', 'A'):
                                score += 1
                        
                        st.session_state.quiz_score = score
                        st.session_state.quiz_active = False
                        st.session_state.show_results = True
                        
                        points_earned = score * 10
                        st.session_state.points_earned += points_earned
                        
                        quiz_name = f"{st.session_state.quiz_subject}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        st.session_state.quiz_scores[quiz_name] = {
                            'score': score,
                            'total': len(questions),
                            'percentage': (score/len(questions))*100,
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'subject': st.session_state.quiz_subject
                        }
                        st.rerun()
                    else:
                        st.warning("Please select an answer before submitting!")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Results Display
if st.session_state.show_results:
    questions = st.session_state.quiz_questions_list
    answers = st.session_state.user_answers
    score = st.session_state.quiz_score
    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0
    
    st.markdown(f"""
    <div class="quiz-container">
        <div style="text-align: center;">
            <h1>🎉 Quiz Completed! 🎉</h1>
    """, unsafe_allow_html=True)
    
    if percentage >= 80:
        st.markdown(f"""
        <div class="score-card">
            <div>🏆 EXCELLENT! 🏆</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Great job! ⭐</div>
        </div>
        """, unsafe_allow_html=True)
    elif percentage >= 50:
        st.markdown(f"""
        <div class="score-card">
            <div>🌟 GOOD WORK! 🌟</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Keep practicing! 📚</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="score-card">
            <div>💪 KEEP GOING! 💪</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Review and try again!</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📝 Review Your Answers")
    for i, q in enumerate(questions):
        user_answer = answers[i] if i < len(answers) else "Not answered"
        correct_answer = q.get('correct', 'A')
        is_correct = user_answer == correct_answer
        
        options = q.get('options', [])
        user_option_text = ""
        correct_option_text = ""
        
        for opt in options:
            if opt.startswith(user_answer):
                user_option_text = opt
            if opt.startswith(correct_answer):
                correct_option_text = opt
        
        st.markdown(f"""
        <div style="background: {'#d4edda' if is_correct else '#f8d7da'}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>Q{i+1}:</strong> {q.get('question', 'Question not available')}<br>
            <strong>Your answer:</strong> {user_answer}. {user_option_text}<br>
            <strong>Correct answer:</strong> {correct_answer}. {correct_option_text}<br>
            <strong>💡 Explanation:</strong> {q.get('explanation', 'Review your study materials.')}
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Take Another Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_active = False
            st.session_state.show_results = False
            st.session_state.user_answers = []
            st.session_state.quiz_questions_list = []
            st.session_state.current_question_index = 0
            st.session_state.quiz_score = 0
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("app.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if percentage >= 70:
        st.balloons()

# Statistics
st.markdown("---")
st.markdown("## 🏆 Your Quiz Statistics")

col1, col2 = st.columns(2)

with col1:
    total_quizzes = len(st.session_state.quiz_scores)
    st.metric("Total Quizzes Taken", total_quizzes)

with col2:
    st.metric("Points Earned", st.session_state.points_earned)

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    💪 Practice makes progress! Take quizzes to test your knowledge! 🌟
</div>
""", unsafe_allow_html=True)
