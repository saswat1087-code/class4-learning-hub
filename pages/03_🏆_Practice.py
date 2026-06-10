"""
Practice & Tests Page
Interactive quiz system with multiple question types, scoring, and progress tracking
"""

import streamlit as st
import random
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
    display: block;
    width: 100%;
    margin: 8px 0;
    text-align: left;
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

def generate_questions_from_chapter(content: str, chapter_title: str, num_questions: int = 5) -> list:
    """Generate meaningful quiz questions from chapter content"""
    questions = []
    
    # Extract key points and vocabulary from content
    key_points = []
    vocab_words = []
    
    # Parse the content to extract key points
    points_match = re.search(r'## Key Points\s+(.*?)(?=##|$)', content, re.DOTALL)
    if points_match:
        points_text = points_match.group(1)
        points = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', points_text, re.DOTALL)
        key_points = [p.strip() for p in points if p.strip()]
    
    # Extract vocabulary
    vocab_match = re.search(r'## Vocabulary\s+(.*?)(?=##|$)', content, re.DOTALL)
    if vocab_match:
        vocab_text = vocab_match.group(1)
        vocab_items = re.findall(r'\*\*(.*?)\*\*', vocab_text)
        vocab_words = [v.strip() for v in vocab_items if v.strip()]
    
    # Get practice questions from chapter
    practice_qs_match = re.search(r'## Practice Questions\s+(.*?)(?=##|$)', content, re.DOTALL)
    if practice_qs_match:
        practice_text = practice_qs_match.group(1)
        practice_qs = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', practice_text, re.DOTALL)
        if practice_qs:
            for q in practice_qs[:num_questions]:
                questions.append({
                    'question': q.strip(),
                    'type': 'open'
                })
    
    # If no practice questions, create from key points
    if not questions and key_points:
        for i, point in enumerate(key_points[:num_questions]):
            questions.append({
                'question': f"What is meant by: '{point[:50]}...'?",
                'type': 'open'
            })
    
    # If still no questions, create basic ones from chapter title
    if not questions:
        questions = [
            {'question': f'What is the main topic of {chapter_title}?', 'type': 'open'},
            {'question': f'Why is {chapter_title} important to learn?', 'type': 'open'},
            {'question': f'Can you explain one key concept from {chapter_title}?', 'type': 'open'}
        ]
    
    return questions[:num_questions]

# Get subjects for quiz selection
subjects = github_storage.get_subjects()

if not st.session_state.quiz_active and not st.session_state.show_results:
    st.markdown("## 🎯 Choose Your Quiz")
    
    if subjects:
        subject_names = [s['name'] for s in subjects]
        selected_subject = st.selectbox("Select Subject:", subject_names)
        
        subject_data = next((s for s in subjects if s['name'] == selected_subject), None)
        if subject_data:
            chapters = github_storage.get_chapters(subject_data['folder_name'])
            if chapters:
                chapter_names = [c['title'] for c in chapters]
                selected_chapter = st.selectbox("Select Chapter:", chapter_names)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    num_questions = st.selectbox("Number of questions:", [3, 5, 10], index=0)
                
                with col2:
                    quiz_type = st.selectbox("Quiz type:", ["Easy", "Medium", "Hard"], index=0)
                
                if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
                    chapter_data = next((c for c in chapters if c['title'] == selected_chapter), None)
                    if chapter_data:
                        content_data = github_storage.get_chapter_content(subject_data['folder_name'], chapter_data['id'])
                        chapter_content = content_data.get('content', '')
                        
                        if chapter_content:
                            questions = generate_questions_from_chapter(chapter_content, selected_chapter, num_questions)
                        else:
                            # Fallback questions
                            questions = [
                                {'question': f'What did you learn in {selected_chapter}?', 'type': 'open'},
                                {'question': f'Why is {selected_chapter} important?', 'type': 'open'},
                                {'question': f'Can you give an example related to {selected_chapter}?', 'type': 'open'}
                            ]
                        
                        st.session_state.quiz_questions_list = questions
                        st.session_state.quiz_subject = selected_subject
                        st.session_state.quiz_chapter = selected_chapter
                        st.session_state.quiz_active = True
                        st.session_state.current_question_index = 0
                        st.session_state.user_answers = []
                        st.session_state.quiz_score = 0
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
        
        st.markdown("### ✍️ Your Answer:")
        
        # For open-ended questions, use text area
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
                        
                        # Calculate score (give points for attempting)
                        score = len([a for a in st.session_state.user_answers if a.strip()])
                        st.session_state.quiz_score = score
                        st.session_state.quiz_active = False
                        st.session_state.show_results = True
                        
                        points_earned = score * 5
                        data_manager.award_points(points_earned, f"for completing the quiz on {st.session_state.quiz_chapter}!", category="quiz")
                        
                        # Save to quiz scores
                        quiz_name = f"{st.session_state.quiz_subject}_{st.session_state.quiz_chapter}"
                        st.session_state.quiz_scores[quiz_name] = {
                            'score': score,
                            'total': len(questions),
                            'percentage': (score/len(questions))*100,
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
            <div>{percentage:.0f}% - Outstanding! You answered all questions! ⭐</div>
        </div>
        """, unsafe_allow_html=True)
    elif percentage >= 70:
        st.markdown(f"""
        <div class="score-card">
            <div>🌟 EXCELLENT! 🌟</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Great job! Keep learning! ⭐</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="score-card">
            <div>💪 GOOD EFFORT! 💪</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Review the chapter and try again!</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show answers review
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
        avg_score = sum(s.get('percentage', 0) for s in st.session_state.quiz_scores.values()) / len(st.session_state.quiz_scores)
        st.metric("Average Score", f"{avg_score:.0f}%")
    else:
        st.metric("Average Score", "N/A")

with col3:
    st.metric("Points Earned", st.session_state.points_earned)

# Study Tips
with st.expander("💡 Quiz Tips"):
    st.markdown("""
    **📚 How to do well on quizzes:**
    
    1. **Read the chapter carefully** before taking the quiz
    2. **Take notes** while studying
    3. **Write answers in your own words** - this helps you remember better
    4. **Review your answers** before submitting
    5. **Learn from mistakes** - review questions you found difficult
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    💪 Practice makes progress! Every quiz brings you closer to mastery! 🌟
</div>
""", unsafe_allow_html=True)
