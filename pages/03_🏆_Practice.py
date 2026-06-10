"""
Practice & Tests Page - Multiple Choice Questions from PDFs
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
.option-btn {
    width: 100%;
    text-align: left;
    margin: 8px 0;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #ddd;
    background: white;
    cursor: pointer;
    transition: all 0.3s ease;
}
.option-btn:hover {
    background: #e3f2fd;
    border-color: #2196F3;
}
.selected-option {
    background: #2196F3;
    color: white;
    border-color: #2196F3;
}
.correct-feedback {
    background: #d4edda;
    color: #155724;
    padding: 0.5rem;
    border-radius: 8px;
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🏆 Practice & Assessment Zone</h1>
    <p>Multiple choice questions from your assignment PDFs! 📄</p>
</div>
""", unsafe_allow_html=True)

def generate_mcq_from_question(question_text: str, index: int) -> dict:
    """Generate multiple choice options for a question using AI"""
    
    # Use AI to generate options
    prompt = f"""
    Create a multiple choice question for Class 4 students based on this question: "{question_text}"
    
    Generate:
    1. The same question rephrased clearly
    2. 4 options (A, B, C, D) - one correct and three plausible but incorrect
    3. The correct answer letter
    4. A brief explanation of why the answer is correct
    
    Format as JSON:
    {{
        "question": "rephrased question here",
        "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
        "correct": "A",
        "explanation": "Brief explanation"
    }}
    """
    
    try:
        response = gemini_helper.generate_response(prompt)
        # Parse JSON response
        import json
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass
    
    # Fallback options if AI fails
    return {
        "question": question_text,
        "options": ["A) Yes", "B) No", "C) Maybe", "D) Not sure"],
        "correct": "A",
        "explanation": "Review the chapter to find the correct answer."
    }

def extract_questions_from_pdf(file_url: str) -> list:
    """Extract questions from PDF and convert to MCQs"""
    text = github_storage.extract_text_from_pdf(file_url)
    questions = []
    
    if text:
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Look for numbered questions
            if re.match(r'^\d+[\.\)]\s+', line) and len(line) > 10:
                clean_question = re.sub(r'^\d+[\.\)]\s*', '', line)
                if clean_question and len(clean_question) > 10:
                    questions.append(clean_question)
    
    return questions[:20]

def questions_to_mcq(questions: list) -> list:
    """Convert text questions to multiple choice format"""
    mcqs = []
    for i, q in enumerate(questions):
        # Generate MCQ using AI
        prompt = f"""
        Create a multiple choice question for Class 4 students.
        
        Original question: "{q}"
        
        Generate:
        1. A clear question (rephrase if needed)
        2. 4 options (A, B, C, D)
        3. The correct answer letter
        4. A simple explanation
        
        Format as JSON:
        {{
            "question": "question text",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "correct": "A",
            "explanation": "explanation"
        }}
        """
        
        try:
            response = gemini_helper.generate_response(prompt)
            import json
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                mcq = json.loads(json_match.group())
                mcq['original'] = q
                mcqs.append(mcq)
            else:
                # Fallback
                mcqs.append({
                    "question": q,
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "correct": "A",
                    "explanation": "Review your study materials for the correct answer.",
                    "original": q
                })
        except:
            mcqs.append({
                "question": q,
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct": "A",
                "explanation": "Review your study materials.",
                "original": q
            })
    
    return mcqs

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
        
        if st.button("🚀 Generate Multiple Choice Quiz", use_container_width=True, type="primary"):
            with st.spinner(f"📖 Extracting and processing questions from {selected_pdf}..."):
                # Extract questions from PDF
                extracted_questions = extract_questions_from_pdf(pdf_url)
                
                if extracted_questions:
                    # Take requested number of questions
                    selected_questions = random.sample(extracted_questions, min(num_questions, len(extracted_questions)))
                    
                    # Convert to multiple choice
                    with st.spinner("🎯 Generating multiple choice options..."):
                        mcq_questions = questions_to_mcq(selected_questions)
                        
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
                    st.error("No questions could be extracted from the PDF. Make sure it contains numbered questions (1., 2., etc.)")
    else:
        st.info(f"📁 No PDF files found in ASSIGNMENTS/{subject_folder}/")
        st.markdown("""
        **📌 How to add questions:**
        1. Upload your assignment PDFs to the ASSIGNMENTS folder
        2. Make sure questions are numbered (1., 2., 3. etc.)
        3. The system will automatically create multiple choice questions
        """)

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
                📝 {current_q['question']}
            </div>
        """, unsafe_allow_html=True)
        
        # Store selected answer in session state
        answer_key = f"answer_{current_idx}"
        if answer_key not in st.session_state:
            st.session_state[answer_key] = None
        
        # Display options as radio buttons
        selected_option = st.radio(
            "Choose your answer:",
            current_q['options'],
            key=f"radio_{current_idx}",
            label_visibility="collapsed"
        )
        
        # Extract letter from selected option (e.g., "A) Option" -> "A")
        if selected_option:
            selected_letter = selected_option[0]
            st.session_state[answer_key] = selected_letter
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if current_idx < len(questions) - 1:
                if st.button("Next Question ▶", use_container_width=True, type="primary"):
                    if st.session_state[answer_key]:
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
                    if st.session_state[answer_key]:
                        if current_idx >= len(st.session_state.user_answers):
                            st.session_state.user_answers.append(st.session_state[answer_key])
                        else:
                            st.session_state.user_answers[current_idx] = st.session_state[answer_key]
                        
                        # Calculate score
                        score = 0
                        for i, q in enumerate(questions):
                            if i < len(st.session_state.user_answers) and st.session_state.user_answers[i] == q['correct']:
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
        is_correct = user_answer == q['correct']
        
        # Find the option text
        option_text = ""
        for opt in q['options']:
            if opt.startswith(user_answer):
                option_text = opt
                break
        
        correct_option_text = ""
        for opt in q['options']:
            if opt.startswith(q['correct']):
                correct_option_text = opt
                break
        
        st.markdown(f"""
        <div style="background: {'#d4edda' if is_correct else '#f8d7da'}; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
            <strong>Q{i+1}:</strong> {q['question']}<br>
            <strong>Your answer:</strong> {user_answer}. {option_text}<br>
            <strong>Correct answer:</strong> {q['correct']}. {correct_option_text}<br>
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

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    💪 Practice with multiple choice questions to prepare for your tests! 🌟
</div>
""", unsafe_allow_html=True)
