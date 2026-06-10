"""
Practice & Tests Page - Reads questions directly from assignment PDFs
"""

import streamlit as st
import random
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

# Subject to folder mapping
SUBJECT_FOLDER_MAP = {
    "Computer Science": "COMPUTER",
    "English Language": "ENGLISH LANGUAGE",
    "English Literature": "ENGLISH LITERATURE",
    "Mathematics": "MATHEMATICS",
    "Science": "SCIENCE",
    "Social Studies": "SOCIAL STUDIES"
}

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
    <p>Questions are automatically extracted from your assignment PDFs! 📄</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.quiz_active and not st.session_state.show_results:
    st.markdown("## 🎯 Choose Your Quiz")
    
    selected_subject = st.selectbox("Select Subject:", list(SUBJECT_FOLDER_MAP.keys()))
    subject_folder = SUBJECT_FOLDER_MAP[selected_subject]
    
    assignments_path = f"ASSIGNMENTS/{subject_folder}"
    pdf_files = [f for f in github_storage.get_files_in_folder(assignments_path) if f['type'] == 'pdf']
    
    if pdf_files:
        st.success(f"📄 Found {len(pdf_files)} assignment PDF(s) for {selected_subject}")
        
        quiz_source = st.radio("Choose questions from:", ["All PDFs", "Specific PDF"], horizontal=True)
        
        selected_questions = []
        
        if quiz_source == "Specific PDF":
            selected_pdf = st.selectbox("Select PDF:", [f['name'] for f in pdf_files])
            pdf_url = next(f['url'] for f in pdf_files if f['name'] == selected_pdf)
            
            with st.spinner(f"📖 Extracting questions from {selected_pdf}..."):
                selected_questions = github_storage.get_questions_from_pdf(pdf_url)
        else:
            with st.spinner(f"📖 Extracting questions from all PDFs..."):
                selected_questions = github_storage.get_questions_from_folder(assignments_path)
        
        if selected_questions:
            st.success(f"✅ Extracted {len(selected_questions)} questions")
            
            col1, col2 = st.columns(2)
            with col1:
                num_questions = st.selectbox("Number of questions:", [5, 10, 15, 20, len(selected_questions)], 
                                            index=min(1, len(selected_questions)-1) if len(selected_questions) > 1 else 0)
            
            with col2:
                if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
                    selected = random.sample(selected_questions, min(num_questions, len(selected_questions)))
                    st.session_state.quiz_questions_list = selected
                    st.session_state.quiz_subject = selected_subject
                    st.session_state.quiz_active = True
                    st.session_state.current_question_index = 0
                    st.session_state.user_answers = []
                    st.session_state.quiz_score = 0
                    st.session_state.show_results = False
                    st.rerun()
        else:
            st.warning("No questions could be extracted from the PDFs. Make sure your PDFs contain numbered questions with '1.', '2.', etc.")
            st.info("💡 Tip: The PDF should have questions numbered like '1. What is...', '2. Name...'")
    else:
        st.info(f"📁 No PDF files found in ASSIGNMENTS/{subject_folder}/")
        st.markdown("""
        **📌 How to add questions:**
        1. Upload your assignment PDFs to the ASSIGNMENTS folder
        2. Make sure questions are numbered (1., 2., 3. etc.)
        3. The system will automatically extract questions from the PDFs
        """)

# Active Quiz Mode
if st.session_state.quiz_active:
    questions = st.session_state.quiz_questions_list
    current_idx = st.session_state.current_question_index
    
    if current_idx < len(questions):
        current_q = questions[current_idx]
        
        st.progress(current_idx / len(questions))
        st.caption(f"Question {current_idx + 1} of {len(questions)}")
        
        st.markdown(f"""
        <div class="quiz-container">
            <div class="question-text">
                📝 {current_q['question']}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### ✍️ Your Answer:")
        user_input = st.text_area(
            "Type your answer here:",
            key=f"answer_{current_idx}",
            height=100,
            placeholder="Write your answer in your own words...",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if current_idx < len(questions) - 1:
                if st.button("Next Question ▶", use_container_width=True, type="primary"):
                    if user_input.strip():
                        if current_idx >= len(st.session_state.user_answers):
                            st.session_state.user_answers.append(user_input)
                        else:
                            st.session_state.user_answers[current_idx] = user_input
                        st.session_state.current_question_index += 1
                        st.rerun()
                    else:
                        st.warning("Please write your answer before continuing!")
            else:
                if st.button("📊 Submit Quiz", use_container_width=True, type="primary"):
                    if user_input.strip():
                        if current_idx >= len(st.session_state.user_answers):
                            st.session_state.user_answers.append(user_input)
                        else:
                            st.session_state.user_answers[current_idx] = user_input
                        
                        score = len([a for a in st.session_state.user_answers if a.strip()])
                        st.session_state.quiz_score = score
                        st.session_state.quiz_active = False
                        st.session_state.show_results = True
                        
                        points_earned = score * 5
                        data_manager.award_points(points_earned, f"for completing the {st.session_state.quiz_subject} quiz!", category="quiz")
                        
                        quiz_name = f"{st.session_state.quiz_subject}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        st.session_state.quiz_scores[quiz_name] = {
                            'score': score,
                            'total': len(questions),
                            'percentage': (score/len(questions))*100 if len(questions) > 0 else 0,
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'subject': st.session_state.quiz_subject
                        }
                        st.rerun()
                    else:
                        st.warning("Please answer the question before submitting!")
        
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
            <div>{percentage:.0f}% - Review the chapter and try again!</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📝 Your Answers")
    for i, q in enumerate(questions):
        answer = answers[i] if i < len(answers) else "Not answered"
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 0.8rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>Q{i+1}:</strong> {q['question']}<br>
            <strong>Your answer:</strong> {answer[:200]}{'...' if len(answer) > 200 else ''}
        </div>
        """, unsafe_allow_html=True)
    
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

# Statistics
st.markdown("---")
st.markdown("## 🏆 Your Quiz Statistics")

col1, col2 = st.columns(2)

with col1:
    total_quizzes = len(st.session_state.quiz_scores)
    st.metric("Total Quizzes Taken", total_quizzes)

with col2:
    st.metric("Points Earned", st.session_state.points_earned)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    💪 Practice makes progress! Answer questions from your assignments to prepare for tests! 🌟
</div>
""", unsafe_allow_html=True)
