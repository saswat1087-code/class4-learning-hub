"""
Practice & Tests Page - Smart Multiple Choice with Question Type Detection
Supports: Fill in the blanks, True/False, Multiple Choice, Matching
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
.question-type-badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.mcq-badge { background: #2196F3; color: white; }
.truefalse-badge { background: #4CAF50; color: white; }
.fillblank-badge { background: #FF9800; color: white; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🏆 Practice & Assessment Zone</h1>
    <p>Smart questions - Multiple Choice, True/False, Fill in the Blanks! 📄</p>
</div>
""", unsafe_allow_html=True)

def detect_question_type(question_text: str) -> str:
    """Detect the type of question based on its content"""
    text_lower = question_text.lower()
    
    # True/False detection
    if any(phrase in text_lower for phrase in ['true or false', 'true/false', 'state whether', 'is it true', 'is this true']):
        return "truefalse"
    
    # Fill in the blanks detection
    if any(symbol in question_text for symbol in ['_____', '___', '______', '__', 'blank', 'fill in']):
        return "fillblank"
    
    # Multiple choice detection (already has options or keywords)
    if any(phrase in text_lower for phrase in ['choose', 'select', 'which of the following', 'which one', 'multiple choice']):
        return "mcq"
    
    # Default to multiple choice
    return "mcq"

def generate_question_with_options(question_text: str, index: int) -> dict:
    """Generate appropriate options based on question type"""
    
    question_type = detect_question_type(question_text)
    
    prompt = f"""
    Create an interactive question for Class 4 students based on: "{question_text}"
    
    Question type detected: {question_type}
    
    Generate response in JSON format:
    
    For MULTIPLE CHOICE (mcq):
    {{
        "question": "Clear question text",
        "type": "mcq",
        "options": ["A) First option", "B) Second option", "C) Third option", "D) Fourth option"],
        "correct": "A",
        "explanation": "Why this is correct"
    }}
    
    For TRUE/FALSE (truefalse):
    {{
        "question": "Statement to judge as true or false",
        "type": "truefalse",
        "options": ["A) True", "B) False"],
        "correct": "A",
        "explanation": "Explanation why this is true or false"
    }}
    
    For FILL IN THE BLANKS (fillblank):
    {{
        "question": "Question with _____ blank space",
        "type": "fillblank",
        "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
        "correct": "A",
        "explanation": "Why this word/phrase fits the blank"
    }}
    
    Return ONLY valid JSON.
    """
    
    try:
        gemini_helper = get_gemini_helper()
        response = gemini_helper.generate_response(prompt, temperature=0.7)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            if all(k in result for k in ['question', 'type', 'options', 'correct', 'explanation']):
                return result
    except Exception as e:
        pass
    
    # Fallback based on question type
    if question_type == "truefalse":
        return {
            "question": question_text,
            "type": "truefalse",
            "options": ["A) True", "B) False"],
            "correct": "A",
            "explanation": "Review the chapter to verify this statement."
        }
    elif question_type == "fillblank":
        return {
            "question": question_text.replace('_____', '__________'),
            "type": "fillblank",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct": "A",
            "explanation": "Review the chapter for the correct term."
        }
    else:
        return {
            "question": question_text,
            "type": "mcq",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct": "A",
            "explanation": "Review your study materials for the correct answer."
        }

def extract_questions_from_pdf(file_url: str) -> list:
    """Extract questions from PDF"""
    text = github_storage.extract_text_from_pdf(file_url)
    questions = []
    
    if text:
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Look for numbered questions
            if re.match(r'^(\d+[\.\)]|Q\d+\.)', line, re.IGNORECASE) and len(line) > 15:
                clean_question = re.sub(r'^(\d+[\.\)]|Q\d+\.)\s*', '', line, flags=re.IGNORECASE)
                if clean_question and len(clean_question) > 10:
                    questions.append(clean_question[:200])  # Limit length
    
    return questions[:20]

def questions_to_smart_questions(questions: list) -> list:
    """Convert text questions to smart questions with appropriate types"""
    smart_questions = []
    for i, q in enumerate(questions):
        smart_q = generate_question_with_options(q, i)
        smart_questions.append(smart_q)
    return smart_questions

if not st.session_state.quiz_active and not st.session_state.show_results:
    st.markdown("## 🎯 Choose Your Quiz")
    
    selected_subject = st.selectbox("Select Subject:", list(SUBJECT_FOLDER_MAP.keys()))
    subject_folder = SUBJECT_FOLDER_MAP[selected_subject]
    
    assignments_path = f"ASSIGNMENTS/{subject_folder}"
    pdf_files = [f for f in github_storage.get_files_in_folder(assignments_path) if f['type'] == 'pdf']
    
    if pdf_files:
        st.success(f"📄 Found {len(pdf_files)} assignment PDF(s) for {selected_subject}")
        
        selected_pdf = st.selectbox("Select Assignment PDF:", [f['name'] for f in pdf_files])
        pdf_url = next(f['url'] for f in pdf_files if f['name'] == selected_pdf)
        
        col1, col2 = st.columns(2)
        with col1:
            num_questions = st.selectbox("Number of questions:", [5, 10, 15], index=1)
        
        if st.button("🚀 Generate Smart Quiz", use_container_width=True, type="primary"):
            with st.spinner(f"📖 Extracting questions from {selected_pdf}..."):
                extracted_questions = extract_questions_from_pdf(pdf_url)
                
                if extracted_questions:
                    selected_questions = random.sample(extracted_questions, min(num_questions, len(extracted_questions)))
                    
                    with st.spinner("🎯 Creating smart questions (Multiple Choice, True/False, Fill in blanks)..."):
                        smart_questions = questions_to_smart_questions(selected_questions)
                        
                        st.session_state.quiz_questions_list = smart_questions
                        st.session_state.quiz_subject = selected_subject
                        st.session_state.quiz_chapter = selected_pdf
                        st.session_state.quiz_active = True
                        st.session_state.current_question_index = 0
                        st.session_state.user_answers = []
                        st.session_state.quiz_score = 0
                        st.session_state.show_results = False
                        st.rerun()
                else:
                    st.error("No questions could be extracted. Make sure your PDF has numbered questions (1., 2., etc.)")
    else:
        st.info(f"📁 No PDF files found in ASSIGNMENTS/{subject_folder}/")

# Active Quiz Mode
if st.session_state.quiz_active:
    questions = st.session_state.quiz_questions_list
    current_idx = st.session_state.current_question_index
    
    if current_idx < len(questions):
        current_q = questions[current_idx]
        q_type = current_q.get('type', 'mcq')
        
        # Progress bar
        st.progress((current_idx) / len(questions))
        st.caption(f"Question {current_idx + 1} of {len(questions)}")
        
        # Type badge
        badge_class = {
            'mcq': 'mcq-badge',
            'truefalse': 'truefalse-badge',
            'fillblank': 'fillblank-badge'
        }.get(q_type, 'mcq-badge')
        
        type_name = {
            'mcq': 'Multiple Choice',
            'truefalse': 'True or False',
            'fillblank': 'Fill in the Blanks'
        }.get(q_type, 'Multiple Choice')
        
        st.markdown(f"""
        <div class="quiz-container">
            <div style="margin-bottom: 0.5rem;">
                <span class="question-type-badge {badge_class}">{type_name}</span>
            </div>
            <div class="question-text">
                📝 {current_q.get('question', 'Question not available')}
            </div>
        """, unsafe_allow_html=True)
        
        # Get options
        options = current_q.get('options', [])
        if not options:
            if q_type == 'truefalse':
                options = ["A) True", "B) False"]
            else:
                options = ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"]
        
        # Store selected answer
        answer_key = f"smart_answer_{current_idx}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = None
        
        # Display based on question type
        if q_type == 'truefalse':
            st.markdown("### Choose: True or False")
            selected_option = st.radio(
                "Select your answer:",
                options,
                key=f"tf_radio_{current_idx}",
                label_visibility="collapsed",
                index=None
            )
        elif q_type == 'fillblank':
            st.markdown("### Choose the correct word/phrase to fill the blank:")
            selected_option = st.radio(
                "Select your answer:",
                options,
                key=f"fb_radio_{current_idx}",
                label_visibility="collapsed",
                index=None
            )
        else:  # mcq
            selected_option = st.radio(
                "Choose the correct answer:",
                options,
                key=f"mcq_radio_{current_idx}",
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
                        
                        # Calculate score
                        score = 0
                        for i, q in enumerate(questions):
                            if i < len(st.session_state.user_answers) and st.session_state.user_answers[i] == q.get('correct', 'A'):
                                score += 1
                        
                        st.session_state.quiz_score = score
                        st.session_state.quiz_active = False
                        st.session_state.show_results = True
                        
                        points_earned = score * 10
                        data_manager.award_points(points_earned, f"scored {score}/{len(questions)} on {st.session_state.quiz_subject} quiz!", category="quiz")
                        
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
        
        q_type = q.get('type', 'mcq')
        type_icon = {'mcq': '🔘', 'truefalse': '✓✗', 'fillblank': '___'}.get(q_type, '🔘')
        
        st.markdown(f"""
        <div style="background: {'#d4edda' if is_correct else '#f8d7da'}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>{type_icon} Q{i+1}:</strong> {q.get('question', 'Question not available')}<br>
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
    💪 Smart questions help you prepare better for tests! Multiple Choice, True/False, and Fill in the Blanks! 🌟
</div>
""", unsafe_allow_html=True)
