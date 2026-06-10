"""
Practice & Tests Page - Smart File Categorization
Automatically detects and categorizes revision papers and assignments
"""

import streamlit as st
import random
import re
import json
from datetime import datetime
from utils.data_manager import data_manager
from utils import get_gemini_helper
from utils.github_storage import github_storage

st.set_page_config(
    page_title="Practice & Tests | Class 4 Learning Hub",
    page_icon="🏆",
    layout="wide"
)

# ============================================================================
# INITIALIZE ALL SESSION STATE VARIABLES
# ============================================================================
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
if 'quiz_subject' not in st.session_state:
    st.session_state.quiz_subject = None
if 'quiz_chapter' not in st.session_state:
    st.session_state.quiz_chapter = None
if 'quiz_start_time' not in st.session_state:
    st.session_state.quiz_start_time = None
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
.file-card {
    background: #f8f9fa;
    padding: 0.8rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border-left: 4px solid #667eea;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🏆 Practice & Assessment Zone</h1>
    <p>Assignments & Revision Papers - Automatically categorized! 📄</p>
</div>
""", unsafe_allow_html=True)

def categorize_file(filename: str) -> str:
    """Smartly categorize files based on filename patterns"""
    filename_lower = filename.lower()
    
    # Computer Science patterns
    comp_patterns = ['comp', 'computer', 'cs', 'it', 'coding', 'programming', 'ms word', 'excel', 'powerpoint']
    for pattern in comp_patterns:
        if pattern in filename_lower:
            return "COMPUTER"
    
    # English patterns
    english_patterns = ['eng', 'english', 'grammar', 'literature', 'reading', 'writing', 'essay', 'poem', 'story']
    for pattern in english_patterns:
        if pattern in filename_lower:
            return "ENGLISH LANGUAGE"
    
    # Mathematics patterns
    math_patterns = ['math', 'maths', 'mathematics', 'algebra', 'geometry', 'arithmetic', 'numbers', 'calculation']
    for pattern in math_patterns:
        if pattern in filename_lower:
            return "MATHEMATICS"
    
    # Science patterns
    science_patterns = ['science', 'sci', 'physics', 'chemistry', 'biology', 'plants', 'animals', 'human body', 'force']
    for pattern in science_patterns:
        if pattern in filename_lower:
            return "SCIENCE"
    
    # Social Studies patterns
    ss_patterns = ['social', 'sst', 'history', 'geography', 'civics', 'map', 'civilization', 'india', 'political']
    for pattern in ss_patterns:
        if pattern in filename_lower:
            return "SOCIAL STUDIES"
    
    return None

def get_all_available_files() -> dict:
    """Get all assignments and revision papers, smartly categorized"""
    all_files = {
        "COMPUTER": [],
        "ENGLISH LANGUAGE": [],
        "ENGLISH LITERATURE": [],
        "MATHEMATICS": [],
        "SCIENCE": [],
        "SOCIAL STUDIES": [],
        "OTHER": []
    }
    
    # Get files from ASSIGNMENTS folder
    for subject_folder in ["COMPUTER", "ENGLISH LANGUAGE", "ENGLISH LITERATURE", "MATHEMATICS", "SCIENCE", "SOCIAL STUDIES"]:
        folder_path = f"ASSIGNMENTS/{subject_folder}"
        files = github_storage.get_files_in_folder(folder_path)
        for file in files:
            if file['type'] == 'pdf':
                file['category'] = 'assignment'
                file['display_subject'] = subject_folder
                all_files[subject_folder].append(file)
    
    # Get files from FIRST REVIEW REVISION PAPERS folder
    revision_files = github_storage.get_files_in_folder("FIRST REVIEW REVISION PAPERS")
    for file in revision_files:
        if file['type'] == 'pdf':
            file['category'] = 'revision'
            categorized_subject = categorize_file(file['name'])
            if categorized_subject and categorized_subject in all_files:
                all_files[categorized_subject].append(file)
            else:
                all_files["OTHER"].append(file)
    
    # Get files from PROJECT folder
    project_files = github_storage.get_files_in_folder("PROJECT")
    for file in project_files:
        if file['type'] == 'pdf':
            file['category'] = 'project'
            categorized_subject = categorize_file(file['name'])
            if categorized_subject and categorized_subject in all_files:
                all_files[categorized_subject].append(file)
            else:
                all_files["OTHER"].append(file)
    
    return all_files

def extract_questions_smart(text: str) -> list:
    """Extract questions intelligently without relying on numbering"""
    questions = []
    
    if not text:
        return questions
    
    lines = text.split('\n')
    
    # Method 1: Look for sentences ending with question marks
    for line in lines:
        line = line.strip()
        if line.endswith('?') and 20 < len(line) < 300:
            clean_q = re.sub(r'^\d+[\.\)]\s*', '', line)
            if clean_q and clean_q not in questions:
                questions.append(clean_q)
    
    # Method 2: Look for lines that start with question words
    question_words = ['what', 'why', 'how', 'when', 'where', 'which', 'who', 'whom', 
                      'define', 'explain', 'describe', 'list', 'name', 'state', 
                      'differentiate', 'compare', 'distinguish']
    
    for line in lines:
        line = line.strip()
        line_lower = line.lower()
        if any(line_lower.startswith(qw) for qw in question_words):
            if 20 < len(line) < 300 and line not in questions:
                questions.append(line)
    
    # Method 3: Look for lines that are likely questions
    for line in lines:
        line = line.strip()
        if (line and line[0].isupper() and 
            len(line) > 25 and 
            any(word in line.lower() for word in ['?', 'explain', 'describe', 'define', 'what is', 'how does'])):
            if line not in questions and not line.endswith('.'):
                questions.append(line)
    
    return questions[:25]

def generate_smart_question(question_text: str) -> dict:
    """Generate multiple choice question using AI"""
    
    prompt = f"""
    Convert this question into an interactive multiple choice question for Class 4 students:
    
    Original question: "{question_text}"
    
    Generate JSON:
    {{
        "question": "Clear question text",
        "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
        "correct": "A",
        "explanation": "Simple explanation"
    }}
    """
    
    try:
        gemini_helper = get_gemini_helper()
        response = gemini_helper.generate_response(prompt, temperature=0.7)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            if all(k in result for k in ['question', 'options', 'correct', 'explanation']):
                return result
    except:
        pass
    
    return {
        "question": question_text,
        "options": ["A) Review your notes", "B) Check the textbook", "C) Ask your teacher", "D) All of the above"],
        "correct": "D",
        "explanation": "Review your study materials for the correct answer."
    }

if not st.session_state.quiz_active and not st.session_state.show_results:
    # Get all available files
    all_files = get_all_available_files()
    
    st.markdown("## 🎯 Select Source for Quiz")
    
    # Create tabs for different sources
    tab1, tab2, tab3 = st.tabs(["📚 Assignments", "📝 Revision Papers", "🎯 Projects"])
    
    all_available_quizzes = []
    
    with tab1:
        st.markdown("### 📚 Assignment Files")
        for subject, files in all_files.items():
            assignment_files = [f for f in files if f.get('category') == 'assignment']
            if assignment_files:
                with st.expander(f"📁 {subject.replace('_', ' ').title()}", expanded=False):
                    for file in assignment_files:
                        if st.button(f"📄 {file['name']}", key=f"assign_{file['name']}", use_container_width=True):
                            all_available_quizzes.append({
                                'name': file['name'],
                                'url': file['url'],
                                'subject': subject,
                                'type': 'assignment'
                            })
    
    with tab2:
        st.markdown("### 📝 Revision Papers")
        revision_found = False
        for subject, files in all_files.items():
            revision_files = [f for f in files if f.get('category') == 'revision']
            if revision_files:
                revision_found = True
                with st.expander(f"📁 {subject.replace('_', ' ').title()}", expanded=False):
                    for file in revision_files:
                        st.markdown(f"""
                        <div class="file-card">
                            <strong>📄 {file['name']}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Select {file['name']}", key=f"revision_{file['name']}", use_container_width=True):
                            all_available_quizzes.append({
                                'name': file['name'],
                                'url': file['url'],
                                'subject': subject,
                                'type': 'revision'
                            })
        if not revision_found:
            st.info("No revision papers found. Add PDFs to the 'FIRST REVIEW REVISION PAPERS' folder.")
    
    with tab3:
        st.markdown("### 🎯 Project Files")
        project_found = False
        for subject, files in all_files.items():
            project_files = [f for f in files if f.get('category') == 'project']
            if project_files:
                project_found = True
                with st.expander(f"📁 {subject.replace('_', ' ').title()}", expanded=False):
                    for file in project_files:
                        st.markdown(f"""
                        <div class="file-card">
                            <strong>📄 {file['name']}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"Select {file['name']}", key=f"project_{file['name']}", use_container_width=True):
                            all_available_quizzes.append({
                                'name': file['name'],
                                'url': file['url'],
                                'subject': subject,
                                'type': 'project'
                            })
        if not project_found:
            st.info("No project files found. Add PDFs to the 'PROJECT' folder.")
    
    # Quiz generation section
    if all_available_quizzes:
        st.markdown("---")
        st.markdown("## 🎯 Generate Quiz")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_quiz = st.selectbox(
                "Select a file:", 
                [f"{q['name']} ({q['type']})" for q in all_available_quizzes],
                key="quiz_selector"
            )
        
        # Find selected quiz
        selected_quiz_data = None
        for q in all_available_quizzes:
            if f"{q['name']} ({q['type']})" == selected_quiz:
                selected_quiz_data = q
                break
        
        if selected_quiz_data:
            with col2:
                num_questions = st.selectbox("Number of questions:", [5, 10, 15, 20], index=1)
            
            if st.button("🚀 Generate Quiz", use_container_width=True, type="primary"):
                with st.spinner(f"📖 Extracting questions from {selected_quiz_data['name']}..."):
                    text = github_storage.extract_text_from_pdf(selected_quiz_data['url'])
                    
                    if text:
                        questions = extract_questions_smart(text)
                        
                        if questions:
                            st.success(f"✅ Found {len(questions)} questions")
                            selected_questions = random.sample(questions, min(num_questions, len(questions)))
                            
                            with st.spinner("🎯 Creating multiple choice questions..."):
                                mcq_questions = []
                                for q in selected_questions:
                                    mcq = generate_smart_question(q)
                                    mcq_questions.append(mcq)
                                
                                st.session_state.quiz_questions_list = mcq_questions
                                st.session_state.quiz_subject = selected_quiz_data['subject']
                                st.session_state.quiz_chapter = selected_quiz_data['name']
                                st.session_state.quiz_active = True
                                st.session_state.current_question_index = 0
                                st.session_state.user_answers = []
                                st.session_state.quiz_score = 0
                                st.session_state.show_results = False
                                st.rerun()
                        else:
                            st.error("No questions could be extracted. Make sure the PDF contains question sentences.")
                    else:
                        st.error("Could not read the PDF file.")

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
                        # Award points using data_manager
                        if 'points_earned' in st.session_state:
                            st.session_state.points_earned += points_earned
                        
                        # Save to quiz scores
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
    💪 Practice with questions from your assignments and revision papers! 🌟
</div>
""", unsafe_allow_html=True)
