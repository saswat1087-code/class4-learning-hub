"""
Practice & Tests Page
Interactive quiz system using questions from assignment files
"""

import streamlit as st
import requests
import json
import re
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
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0

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
.option-btn {
    width: 100%;
    text-align: left;
    margin: 5px 0;
}
.correct-answer {
    background-color: #d4edda;
    border-left: 4px solid #28a745;
    padding: 0.5rem;
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
    <p>Test your knowledge with questions from your assignments! 🌟</p>
</div>
""", unsafe_allow_html=True)

def load_questions_from_assignment(file_url: str) -> list:
    """Load questions from assignment PDF or text file"""
    questions = []
    try:
        response = requests.get(file_url, timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # Look for question patterns in the content
            lines = content.split('\n')
            current_question = None
            current_options = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect question numbers (1., 2., Q1., etc.)
                if re.match(r'^(\d+)[\.\)]\s|^Q\d+\.', line, re.IGNORECASE):
                    if current_question:
                        questions.append({
                            'question': current_question,
                            'type': 'open'
                        })
                    current_question = line
                    current_options = []
                
                # Detect multiple choice options (A., B., etc.)
                elif re.match(r'^[A-D][\.\)]\s', line) and current_question:
                    current_options.append(line)
                
                # If we have options, make it multiple choice
                elif current_question and current_options:
                    pass
            
            # Add last question
            if current_question:
                questions.append({
                    'question': current_question,
                    'type': 'open'
                })
    
    except Exception as e:
        pass
    
    return questions if questions else None

def load_questions_from_folder(subject_folder: str, subject_name: str) -> list:
    """Load all questions from assignment files in a subject folder"""
    all_questions = []
    
    # Get all files in the ASSIGNMENTS subject folder
    folder_path = f"ASSIGNMENTS/{subject_folder}"
    files = github_storage.get_files_in_folder(folder_path)
    
    for file in files:
        if file['type'] in ['pdf', 'txt', 'md', 'docx']:
            questions = load_questions_from_assignment(file['url'])
            if questions:
                for q in questions:
                    q['source'] = file['name']
                    all_questions.append(q)
    
    return all_questions

# Subject to folder mapping
SUBJECT_FOLDER_MAP = {
    "Computer Science": "COMPUTER",
    "English Language": "ENGLISH LANGUAGE",
    "English Literature": "ENGLISH LITERATURE",
    "Mathematics": "MATHEMATICS",
    "Science": "SCIENCE",
    "Social Studies": "SOCIAL STUDIES",
    "Hindi (2nd Language)": "2ND LANGUAGE HINDI",
    "Bengali (2nd Language)": "2ND LANGUAGE BENGALI"
}

if not st.session_state.quiz_active and not st.session_state.show_results:
    st.markdown("## 🎯 Choose Your Quiz")
    
    # Subject selection
    subjects = list(SUBJECT_FOLDER_MAP.keys())
    selected_subject = st.selectbox("Select Subject:", subjects)
    
    # Get assignment files for this subject
    subject_folder = SUBJECT_FOLDER_MAP[selected_subject]
    assignments_path = f"ASSIGNMENTS/{subject_folder}"
    assignment_files = github_storage.get_files_in_folder(assignments_path)
    
    if assignment_files:
        st.markdown(f"### 📁 Available Assignments for {selected_subject}")
        
        # Display assignment files as buttons
        cols = st.columns(2)
        for idx, file in enumerate(assignment_files):
            with cols[idx % 2]:
                if st.button(f"📄 {file['name']}", use_container_width=True):
                    with st.spinner("Loading questions..."):
                        questions = load_questions_from_assignment(file['url'])
                        if questions:
                            st.session_state.quiz_questions_list = questions[:10]
                            st.session_state.quiz_subject = selected_subject
                            st.session_state.quiz_chapter = file['name']
                            st.session_state.quiz_active = True
                            st.session_state.current_question_index = 0
                            st.session_state.user_answers = []
                            st.session_state.quiz_score = 0
                            st.session_state.quiz_start_time = datetime.now()
                            st.session_state.show_results = False
                            st.success(f"✅ Loaded {len(questions[:10])} questions from {file['name']}")
                            st.rerun()
                        else:
                            st.warning("No questions found in this file. Try another assignment.")
    else:
        st.info(f"No assignment files found for {selected_subject}. Please add assignment PDFs to the ASSIGNMENTS/{subject_folder} folder.")
    
    st.markdown("---")
    
    # Random quiz option
    st.markdown("## 🎲 Quick Practice")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Random Questions", use_container_width=True):
            # Load from all subjects
            all_questions = []
            for subj, folder in SUBJECT_FOLDER_MAP.items():
                questions = load_questions_from_folder(folder, subj)
                all_questions.extend(questions)
            
            if all_questions:
                random.shuffle(all_questions)
                st.session_state.quiz_questions_list = all_questions[:10]
                st.session_state.quiz_subject = "Random Practice"
                st.session_state.quiz_chapter = "Mixed Topics"
                st.session_state.quiz_active = True
                st.session_state.current_question_index = 0
                st.session_state.user_answers = []
                st.session_state.quiz_score = 0
                st.session_state.quiz_start_time = datetime.now()
                st.session_state.show_results = False
                st.success(f"✅ Loaded 10 random questions!")
                st.rerun()
            else:
                st.warning("No questions found in assignments.")
    
    with col2:
        if st.button("📚 Practice All", use_container_width=True):
            # Load all questions from selected subject
            questions = load_questions_from_folder(subject_folder, selected_subject)
            if questions:
                st.session_state.quiz_questions_list = questions[:20]
                st.session_state.quiz_subject = selected_subject
                st.session_state.quiz_chapter = "All Assignments"
                st.session_state.quiz_active = True
                st.session_state.current_question_index = 0
                st.session_state.user_answers = []
                st.session_state.quiz_score = 0
                st.session_state.quiz_start_time = datetime.now()
                st.session_state.show_results = False
                st.success(f"✅ Loaded {len(questions[:20])} questions from all assignments!")
                st.rerun()
            else:
                st.warning(f"No questions found for {selected_subject}.")

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
        
        st.markdown("### ✍️ Your Answer:")
        
        # Text area for answer
        user_input = st.text_area(
            "Type your answer here:",
            key=f"answer_{current_idx}",
            height=100,
            placeholder="Write your answer in your own words..."
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
                        data_manager.award_points(points_earned, f"for completing the quiz on {st.session_state.quiz_subject}!", category="quiz")
                        
                        quiz_name = f"{st.session_state.quiz_subject}_{st.session_state.quiz_chapter}"
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
            <div>💪 GOOD EFFORT! 💪</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Keep practicing!</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show answers
    st.markdown("### 📝 Your Answers")
    for i, q in enumerate(questions):
        answer = answers[i] if i < len(answers) else "Not answered"
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>Q{i+1}:</strong> {q['question']}<br>
            <strong>Your answer:</strong> {answer[:200]}{'...' if len(answer) > 200 else ''}
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
        valid_scores = [s.get('percentage', 0) for s in st.session_state.quiz_scores.values() if s.get('percentage', 0) > 0]
        if valid_scores:
            avg_score = sum(valid_scores) / len(valid_scores)
            st.metric("Average Score", f"{avg_score:.0f}%")
        else:
            st.metric("Average Score", "N/A")
    else:
        st.metric("Average Score", "N/A")

with col3:
    st.metric("Points Earned", st.session_state.points_earned)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    💪 Practice makes progress! Answer questions from your assignments to prepare for tests! 🌟
</div>
""", unsafe_allow_html=True)
