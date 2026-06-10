"""
Practice & Tests Page - Smart Question Extraction (No Numbering Needed)
Detects questions using AI and patterns
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
    <p>Smart questions extracted from your PDFs - No numbering needed! 📄</p>
</div>
""", unsafe_allow_html=True)

def extract_questions_smart(text: str) -> list:
    """Extract questions intelligently without relying on numbering"""
    questions = []
    
    if not text:
        return questions
    
    lines = text.split('\n')
    
    # Method 1: Look for sentences ending with question marks
    for line in lines:
        line = line.strip()
        # Check if line ends with question mark and has reasonable length
        if line.endswith('?') and 20 < len(line) < 300:
            # Clean up the question
            clean_q = re.sub(r'^\d+[\.\)]\s*', '', line)  # Remove numbering if present
            if clean_q and clean_q not in questions:
                questions.append(clean_q)
    
    # Method 2: Look for lines that start with question words
    question_words = ['what', 'why', 'how', 'when', 'where', 'which', 'who', 'whom', 
                      'define', 'explain', 'describe', 'list', 'name', 'state', 
                      'differentiate', 'compare', 'distinguish']
    
    for line in lines:
        line = line.strip()
        line_lower = line.lower()
        # Check if line starts with question word and has reasonable length
        if any(line_lower.startswith(qw) for qw in question_words):
            if 20 < len(line) < 300 and line not in questions:
                questions.append(line)
    
    # Method 3: Look for lines that are likely questions (capital start, meaningful content)
    for line in lines:
        line = line.strip()
        # Check if line has capital letter at start and contains question-like patterns
        if (line and line[0].isupper() and 
            len(line) > 25 and 
            any(word in line.lower() for word in ['?', 'explain', 'describe', 'define', 'what is', 'how does'])):
            if line not in questions and not line.endswith('.'):
                questions.append(line)
    
    # Method 4: Use AI to identify questions if traditional methods fail
    if len(questions) < 3 and len(text) > 200:
        try:
            gemini_helper = get_gemini_helper()
            prompt = f"""
            Extract all the questions from this text. Return ONLY the questions, one per line.
            Do not include any other text or numbering.
            
            Text:
            {text[:2000]}
            """
            ai_questions = gemini_helper.generate_response(prompt, temperature=0.3)
            if ai_questions:
                for line in ai_questions.split('\n'):
                    line = line.strip()
                    if line and len(line) > 15 and '?' in line:
                        questions.append(line)
        except:
            pass
    
    # Remove duplicates while preserving order
    seen = set()
    unique_questions = []
    for q in questions:
        if q not in seen:
            seen.add(q)
            unique_questions.append(q)
    
    return unique_questions[:25]  # Limit to 25 questions

def generate_smart_question(question_text: str, index: int) -> dict:
    """Generate appropriate question with options using AI"""
    
    prompt = f"""
    Convert this question into an interactive multiple choice question for Class 4 students:
    
    Original question: "{question_text}"
    
    Generate a response in JSON format with:
    1. "question": A clear, well-formatted version of the question
    2. "options": 4 options (A, B, C, D) with one correct answer
    3. "correct": The letter of the correct option (A, B, C, or D)
    4. "explanation": A simple explanation for a 9-year-old
    5. "type": "mcq"
    
    Example:
    {{
        "question": "What is the main function of RAM in a computer?",
        "options": ["A) Permanent storage", "B) Temporary storage", "C) Processing data", "D) Displaying images"],
        "correct": "B",
        "explanation": "RAM is temporary memory that stores data while the computer is running.",
        "type": "mcq"
    }}
    
    Return ONLY valid JSON, no other text.
    """
    
    try:
        gemini_helper = get_gemini_helper()
        response = gemini_helper.generate_response(prompt, temperature=0.7)
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            if all(k in result for k in ['question', 'options', 'correct', 'explanation']):
                return result
    except Exception as e:
        pass
    
    # Fallback
    return {
        "question": question_text,
        "options": ["A) Review your notes", "B) Check the textbook", "C) Ask your teacher", "D) All of the above"],
        "correct": "D",
        "explanation": "When in doubt, review your study materials or ask for help.",
        "type": "mcq"
    }

def extract_questions_from_pdf(file_url: str) -> list:
    """Extract questions from PDF using multiple methods"""
    text = github_storage.extract_text_from_pdf(file_url)
    if text:
        return extract_questions_smart(text)
    return []

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
            num_questions = st.selectbox("Number of questions:", [5, 10, 15, 20], index=1)
        
        if st.button("🚀 Extract Questions & Generate Quiz", use_container_width=True, type="primary"):
            with st.spinner(f"📖 Scanning PDF for questions (no numbering needed)..."):
                extracted_questions = extract_questions_from_pdf(pdf_url)
                
                if extracted_questions:
                    st.success(f"✅ Found {len(extracted_questions)} questions in the PDF")
                    
                    selected_questions = random.sample(extracted_questions, min(num_questions, len(extracted_questions)))
                    
                    with st.spinner("🎯 Creating multiple choice questions..."):
                        mcq_questions = []
                        for i, q in enumerate(selected_questions):
                            mcq = generate_smart_question(q, i)
                            mcq_questions.append(mcq)
                        
                        st.session_state.quiz_questions_list = mcq_questions
                        st.session_state.quiz_subject = selected_subject
                        st.session_state.quiz_chapter = selected_pdf
                        st.session_state.quiz_active = True
                        st.session_state.current_question_index = 0
                        st.session_state.user_answers = []
                        st.session_state.quiz_score = 0
                        st.session_state.show_results = False
                        st.rerun()
                else:
                    st.error("No questions could be extracted from the PDF. Try a PDF with clear question sentences.")
                    st.info("💡 Tip: Questions should end with question marks (?) or start with words like 'What', 'Why', 'How'")
    else:
        st.info(f"📁 No PDF files found in ASSIGNMENTS/{subject_folder}/")

# Active Quiz Mode
if st.session_state.quiz_active:
    questions = st.session_state.quiz_questions_list
    current_idx = st.session_state.current_question_index
    
    if current_idx < len(questions):
        current_q = questions[current_idx]
        
        # Progress bar
        st.progress((current_idx) / len(questions))
        st.caption(f"Question {current_idx + 1} of {len(questions)}")
        
        # Type badge
        st.markdown(f"""
        <div class="quiz-container">
            <div style="margin-bottom: 0.5rem;">
                <span class="question-type-badge mcq-badge">Multiple Choice</span>
            </div>
            <div class="question-text">
                📝 {current_q.get('question', 'Question not available')}
            </div>
        """, unsafe_allow_html=True)
        
        # Get options
        options = current_q.get('options', [
            "A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"
        ])
        
        # Store selected answer
        answer_key = f"mcq_answer_{current_idx}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = None
        
        # Display radio buttons
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
            <strong>🔘 Q{i+1}:</strong> {q.get('question', 'Question not available')}<br>
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
    💪 Questions are automatically detected - no numbering needed! Look for sentences with question marks or starting with What/Why/How! 🌟
</div>
""", unsafe_allow_html=True)
