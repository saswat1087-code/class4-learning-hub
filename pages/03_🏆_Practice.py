"""
Practice & Tests Page
Interactive quiz system with multiple question types, scoring, and progress tracking
"""

import streamlit as st
import random
import time
from datetime import datetime
from utils.data_manager import data_manager
from utils.gemini_helper import get_gemini_helper

# Page configuration
st.set_page_config(
    page_title="Practice & Tests | Class 4 Learning Hub",
    page_icon="🏆",
    layout="wide"
)

# Custom CSS for practice page
st.markdown("""
<style>
/* Quiz container */
.quiz-container {
    background: white;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin: 1rem 0;
    animation: slideIn 0.5s ease;
}

/* Question styling */
.question-text {
    font-size: 1.3rem;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: #f0f2f6;
    border-radius: 10px;
}

/* Option styling */
.option {
    background: #f8f9fa;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.option:hover {
    background: #e9ecef;
    transform: translateX(5px);
}

.option-selected {
    background: #e3f2fd;
    border-color: #2196F3;
}

.option-correct {
    background: #c8e6c9;
    border-color: #4CAF50;
    animation: pulse 0.5s ease;
}

.option-wrong {
    background: #ffcdd2;
    border-color: #f44336;
}

/* Score display */
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

/* Timer */
.timer {
    background: #ff9800;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 50px;
    display: inline-block;
    font-weight: bold;
    animation: pulse 1s infinite;
}

.timer-warning {
    background: #f44336;
    animation: shake 0.5s infinite;
}

/* Progress bar */
.quiz-progress {
    margin: 1rem 0;
}

/* Results section */
.result-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.perfect-score {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    animation: celebration 1s ease;
}

/* Animations */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

@keyframes shake {
    0%, 100% {
        transform: translateX(0);
    }
    25% {
        transform: translateX(-5px);
    }
    75% {
        transform: translateX(5px);
    }
}

@keyframes celebration {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.1);
    }
    100% {
        transform: scale(1);
    }
}

/* Badge notification */
.badge-notification {
    position: fixed;
    top: 20px;
    right: 20px;
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    z-index: 1000;
    animation: slideInRight 0.5s ease;
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(100px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize helper
gemini_helper = get_gemini_helper()

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
        },
        "Chapter 2: GUI Operating System": {
            "questions": [
                {
                    "question": "What does GUI stand for?",
                    "options": ["Graphical User Interface", "General User Interface", "Graphical Unit Interface", "General Unit Interface"],
                    "correct": "A",
                    "explanation": "GUI stands for Graphical User Interface - it uses pictures and icons instead of text commands."
                },
                {
                    "question": "Which of these is NOT a GUI element?",
                    "options": ["Desktop", "Taskbar", "Command Line", "Icons"],
                    "correct": "C",
                    "explanation": "Command Line is text-based, not a graphical element. GUI uses pictures and icons."
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
                },
                {
                    "question": "What is the real magic in the story?",
                    "options": ["Magic spells", "Friendship and courage", "Fairy godmother", "Magic potions"],
                    "correct": "B",
                    "explanation": "The story teaches that true magic comes from friendship, courage, and believing in yourself."
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
                    "explanation": "234 × 5 = 1,170 (200×5=1,000, 30×5=150, 4×5=20, total 1,170)"
                },
                {
                    "question": "If one book costs ₹125, how much do 8 books cost?",
                    "options": ["₹800", "₹900", "₹1,000", "₹1,100"],
                    "correct": "C",
                    "explanation": "125 × 8 = 1,000 rupees"
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
                    "explanation": "Plants need sunlight, water, and carbon dioxide (air) to make food through photosynthesis."
                },
                {
                    "question": "Which part of the plant absorbs water from the soil?",
                    "options": ["Leaves", "Stem", "Roots", "Flowers"],
                    "correct": "C",
                    "explanation": "Roots absorb water and minerals from the soil and send them up to the rest of the plant."
                }
            ]
        }
    }
}

# Question bank for random quizzes
QUESTION_BANK = {
    "General Knowledge": [
        {
            "question": "What is the capital of India?",
            "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"],
            "correct": "B",
            "explanation": "New Delhi is the capital city of India."
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["Jupiter", "Mars", "Venus", "Saturn"],
            "correct": "B",
            "explanation": "Mars is called the Red Planet because of its reddish appearance."
        },
        {
            "question": "Who wrote the National Anthem of India?",
            "options": ["Mahatma Gandhi", "Jawaharlal Nehru", "Rabindranath Tagore", "Subhash Chandra Bose"],
            "correct": "C",
            "explanation": "Rabindranath Tagore wrote 'Jana Gana Mana', India's National Anthem."
        }
    ],
    "Math Challenge": [
        {
            "question": "What is 15 × 8?",
            "options": ["100", "110", "120", "130"],
            "correct": "C",
            "explanation": "15 × 8 = 120"
        },
        {
            "question": "What is the value of 7²?",
            "options": ["14", "49", "56", "77"],
            "correct": "B",
            "explanation": "7² means 7 × 7 = 49"
        }
    ]
}

# Initialize session state for quiz
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
    st.session_state.quiz_type = None  # 'syllabus' or 'random' or 'ai'
if 'ai_questions' not in st.session_state:
    st.session_state.ai_questions = []

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>🏆 Practice & Assessment Zone</h1>
    <p>Test your knowledge, earn points, and become a learning champion! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Quiz selection mode (if no active quiz)
if not st.session_state.quiz_active and not st.session_state.show_results:
    st.markdown("## 🎯 Choose Your Quiz")
    
    quiz_type = st.radio(
        "Select quiz type:",
        ["📚 Subject Quiz", "🎲 Random Challenge", "🤖 AI Generated Quiz"],
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
            # Load questions from syllabus
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
                    st.warning("No questions available for this chapter yet. Try AI generated quiz!")
            else:
                st.warning("Please select a subject and chapter with questions.")
    
    elif quiz_type == "🎲 Random Challenge":
        st.info("🎲 Test your general knowledge with random questions!")
        
        num_questions = st.slider("Number of questions:", 3, 10, 5)
        category = st.selectbox("Category:", ["General Knowledge", "Math Challenge", "Mixed"])
        
        if st.button("🎲 Start Random Quiz", use_container_width=True, type="primary"):
            # Collect random questions
            questions = []
            if category == "Mixed":
                # Mix from all categories
                all_questions = []
                for cat_questions in QUESTION_BANK.values():
                    all_questions.extend(cat_questions)
                questions = random.sample(all_questions, min(num_questions, len(all_questions)))
            else:
                questions = random.sample(QUESTION_BANK[category], min(num_questions, len(QUESTION_BANK[category])))
            
            st.session_state.quiz_questions_list = questions
            st.session_state.quiz_subject = "Random Challenge"
            st.session_state.quiz_chapter = category
            st.session_state.quiz_type = 'random'
            st.session_state.quiz_active = True
            st.session_state.current_question_index = 0
            st.session_state.user_answers = []
            st.session_state.quiz_score = 0
            st.session_state.quiz_start_time = datetime.now()
            st.session_state.show_results = False
            st.rerun()
    
    elif quiz_type == "🤖 AI Generated Quiz":
        st.info("🤖 Let AI create a custom quiz just for you!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ai_subject = st.selectbox("Subject:", ["Computer Science", "English Literature", "Mathematics", "Science", "General"])
        
        with col2:
            ai_topic = st.text_input("Specific topic (optional):", placeholder="e.g., Multiplication, Plants, etc.")
        
        num_ai_questions = st.slider("Number of questions:", 3, 8, 5)
        
        if st.button("🤖 Generate AI Quiz", use_container_width=True, type="primary"):
            with st.spinner("AI is creating your personalized quiz..."):
                # Create prompt for AI
                if ai_topic:
                    prompt = f"Create {num_ai_questions} multiple choice questions for Class 4 students about {ai_topic} in {ai_subject}. Format as JSON with question, options (A, B, C, D), correct answer (letter), and explanation."
                else:
                    prompt = f"Create {num_ai_questions} multiple choice questions for Class 4 students about {ai_subject}. Format as JSON with question, options (A, B, C, D), correct answer (letter), and explanation."
                
                response = gemini_helper.generate_response(prompt)
                
                # Try to parse AI response
                try:
                    # Simple parsing - in production, use proper JSON parsing
                    st.session_state.ai_questions = []
                    # For now, use fallback questions
                    fallback_questions = [
                        {
                            "question": f"What is a key concept in {ai_subject}?",
                            "options": ["Option A", "Option B", "Option C", "Option D"],
                            "correct": "A",
                            "explanation": "This is a sample question. AI quiz generation is being enhanced!"
                        }
                    ]
                    st.session_state.quiz_questions_list = fallback_questions
                    st.session_state.quiz_subject = ai_subject
                    st.session_state.quiz_chapter = ai_topic if ai_topic else "General"
                    st.session_state.quiz_type = 'ai'
                    st.session_state.quiz_active = True
                    st.session_state.current_question_index = 0
                    st.session_state.user_answers = []
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_start_time = datetime.now()
                    st.session_state.show_results = False
                    st.rerun()
                except:
                    st.error("AI is still learning! Please try the Subject Quiz or Random Challenge for now.")
    
    # Practice mode - flashcards
    st.markdown("---")
    st.markdown("## 📇 Quick Practice Mode")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Daily Quiz (10 Questions)", use_container_width=True):
            # Create a quick 10-question mixed quiz
            all_questions = []
            for subject_data in SYLLABUS_DATA.values():
                for chapter_data in subject_data.values():
                    if 'questions' in chapter_data:
                        all_questions.extend(chapter_data['questions'])
            
            if len(all_questions) >= 10:
                quick_questions = random.sample(all_questions, 10)
                st.session_state.quiz_questions_list = quick_questions
                st.session_state.quiz_subject = "Daily Challenge"
                st.session_state.quiz_chapter = "Mixed Topics"
                st.session_state.quiz_type = 'daily'
                st.session_state.quiz_active = True
                st.session_state.current_question_index = 0
                st.session_state.user_answers = []
                st.session_state.quiz_score = 0
                st.session_state.quiz_start_time = datetime.now()
                st.session_state.show_results = False
                st.rerun()
            else:
                st.warning("Not enough questions available. Try the Random Challenge!")
    
    with col2:
        if st.button("🎯 Weak Areas Practice", use_container_width=True):
            # Practice questions from subjects with low scores
            low_score_subjects = []
            for subject, scores in st.session_state.subject_scores.items():
                if scores and sum(scores)/len(scores) < 70:
                    low_score_subjects.append(subject)
            
            if low_score_subjects:
                st.info(f"Let's practice: {', '.join(low_score_subjects)}")
                # Create practice quiz for weak subjects
                practice_questions = []
                for subject in low_score_subjects:
                    if subject in SYLLABUS_DATA:
                        for chapter_data in SYLLABUS_DATA[subject].values():
                            if 'questions' in chapter_data:
                                practice_questions.extend(chapter_data['questions'][:2])
                
                if practice_questions:
                    st.session_state.quiz_questions_list = practice_questions[:10]
                    st.session_state.quiz_subject = "Weak Areas Practice"
                    st.session_state.quiz_chapter = "Focus Topics"
                    st.session_state.quiz_type = 'practice'
                    st.session_state.quiz_active = True
                    st.session_state.current_question_index = 0
                    st.session_state.user_answers = []
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_start_time = datetime.now()
                    st.session_state.show_results = False
                    st.rerun()
            else:
                st.success("You're doing great in all subjects! Try the Daily Quiz for a challenge!")

# Active Quiz Mode
if st.session_state.quiz_active:
    questions = st.session_state.quiz_questions_list
    current_idx = st.session_state.current_question_index
    
    if current_idx < len(questions):
        current_q = questions[current_idx]
        
        # Calculate time elapsed
        if st.session_state.quiz_start_time:
            elapsed = (datetime.now() - st.session_state.quiz_start_time).seconds
            remaining = max(0, 300 - elapsed)  # 5 minutes per quiz
            
            # Timer display
            if remaining > 60:
                timer_text = f"⏰ Time Left: {remaining//60}:{remaining%60:02d}"
                timer_class = "timer"
            elif remaining > 0:
                timer_text = f"⚠️ Time Left: {remaining//60}:{remaining%60:02d}"
                timer_class = "timer timer-warning"
            else:
                timer_text = "⏰ Time's Up!"
                timer_class = "timer timer-warning"
                # Auto-submit if time's up
                st.session_state.quiz_active = False
                st.session_state.show_results = True
                st.rerun()
            
            st.markdown(f'<div class="{timer_class}" style="float: right;">{timer_text}</div>', unsafe_allow_html=True)
        
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
        
        # Display options as buttons
        options = current_q.get('options', [])
        option_letters = ['A', 'B', 'C', 'D']
        
        for i, option in enumerate(options[:4]):  # Max 4 options
            letter = option_letters[i]
            is_selected = selected_option == letter
            
            # Create button with appropriate styling
            if st.button(
                f"{letter}. {option}",
                key=f"q{current_idx}_opt{letter}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                # Save answer
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
                        # Calculate score
                        score = 0
                        for i, q in enumerate(questions):
                            if i < len(st.session_state.user_answers) and st.session_state.user_answers[i] == q['correct']:
                                score += 1
                        
                        st.session_state.quiz_score = score
                        st.session_state.quiz_active = False
                        st.session_state.show_results = True
                        
                        # Save quiz result
                        total_questions = len(questions)
                        percentage = (score / total_questions) * 100
                        
                        # Award points
                        points_earned = score * 10
                        data_manager.award_points(points_earned, f"for scoring {score}/{total_questions} on {st.session_state.quiz_subject} quiz!", category="quiz")
                        
                        # Save to quiz scores
                        quiz_name = f"{st.session_state.quiz_subject}_{st.session_state.quiz_chapter}"
                        st.session_state.quiz_scores[quiz_name] = {
                            'score': score,
                            'total': total_questions,
                            'percentage': percentage,
                            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'subject': st.session_state.quiz_subject
                        }
                        
                        st.rerun()
                    else:
                        st.warning(f"Please answer all questions! ({len(st.session_state.user_answers)}/{len(questions)} answered)")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # All questions answered
        st.session_state.quiz_active = False
        st.session_state.show_results = True
        st.rerun()

# Results Display
if st.session_state.show_results:
    questions = st.session_state.quiz_questions_list
    user_answers = st.session_state.user_answers
    score = st.session_state.quiz_score
    total = len(questions)
    percentage = (score / total) * 100 if total > 0 else 0
    
    # Results header
    st.markdown(f"""
    <div class="quiz-container">
        <div style="text-align: center;">
            <h1>🎉 Quiz Completed! 🎉</h1>
    """, unsafe_allow_html=True)
    
    # Score card
    if percentage == 100:
        st.markdown(f"""
        <div class="score-card perfect-score">
            <div>🏆 PERFECT SCORE! 🏆</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Outstanding! You're a superstar! ⭐</div>
        </div>
        """, unsafe_allow_html=True)
    elif percentage >= 80:
        st.markdown(f"""
        <div class="score-card">
            <div>🌟 EXCELLENT! 🌟</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Great job! Keep shining! ⭐</div>
        </div>
        """, unsafe_allow_html=True)
    elif percentage >= 60:
        st.markdown(f"""
        <div class="score-card">
            <div>👍 GOOD WORK! 👍</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - You're doing great! A little more practice will make you perfect!</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="score-card">
            <div>💪 KEEP PRACTICING! 💪</div>
            <div class="score-number">{score}/{total}</div>
            <div>{percentage:.0f}% - Every mistake is a learning opportunity! Try again!</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed results
    st.markdown("### 📝 Review Your Answers")
    
    for i, q in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else "Not answered"
        is_correct = user_answer == q['correct']
        
        # Find the actual answer text
        options = q.get('options', [])
        option_letters = ['A', 'B', 'C', 'D']
        
        correct_text = ""
        user_text = ""
        
        for j, letter in enumerate(option_letters):
            if j < len(options):
                if letter == q['correct']:
                    correct_text = options[j]
                if letter == user_answer:
                    user_text = options[j]
        
        st.markdown(f"""
        <div class="result-card">
            <div>
                <strong>Question {i + 1}:</strong> {q['question']}
            </div>
            <div style="margin-top: 0.5rem;">
                <span style="color: {'#4CAF50' if is_correct else '#f44336'}">
                    {'✅' if is_correct else '❌'} Your answer: {user_answer}. {user_text}
                </span>
            </div>
            <div style="margin-top: 0.3rem; color: #2196F3;">
                📖 Correct answer: {q['correct']}. {correct_text}
            </div>
            <div style="margin-top: 0.5rem; padding: 0.5rem; background: #f0f2f6; border-radius: 8px;">
                💡 {q.get('explanation', 'Keep learning and practicing!')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Performance tips
    st.markdown("---")
    st.markdown("### 💪 Tips to Improve")
    
    if percentage < 60:
        st.info("""
        📚 **Study Tips:**
        - Review the chapter materials again
        - Take notes while studying
        - Practice with flashcards
        - Ask Exam Buddy for help
        """)
    elif percentage < 80:
        st.info("""
        🎯 **Getting Better:**
        - Focus on the questions you missed
        - Practice similar questions
        - Teach someone else what you learned
        """)
    else:
        st.success("""
        🌟 **Keep Shining:**
        - Try more advanced questions
        - Challenge yourself with harder topics
        - Help other students learn
        """)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Take Another Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_active = False
            st.session_state.show_results = False
            st.session_state.user_answers = []
            st.session_state.quiz_questions_list = []
            st.rerun()
    
    with col2:
        if st.button("📚 Review Chapter", use_container_width=True):
            st.switch_page("pages/02_📚_Syllabus.py")
    
    with col3:
        if st.button("🤖 Ask Exam Buddy", use_container_width=True):
            st.switch_page("pages/04_🤖_Exam_Buddy.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Share achievement
    if percentage >= 80:
        st.balloons()
        st.snow()

# Leaderboard / High Scores
st.markdown("---")
st.markdown("## 🏆 Your Quiz Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    total_quizzes = len(st.session_state.quiz_scores)
    st.metric("Total Quizzes Taken", total_quizzes)

with col2:
    if st.session_state.quiz_scores:
        avg_score = data_manager.get_average_quiz_score()
        st.metric("Average Score", f"{avg_score:.0f}%")
    else:
        st.metric("Average Score", "N/A")

with col3:
    best_subject = data_manager.get_best_subject()
    st.metric("Best Subject", best_subject if best_subject else "N/A")

# Recent quiz scores
if st.session_state.quiz_scores:
    st.markdown("### 📊 Recent Quiz Performance")
    
    recent_scores = list(st.session_state.quiz_scores.values())[-5:]
    for score_data in recent_scores:
        percentage = score_data.get('percentage', 0)
        if percentage >= 80:
            st.success(f"📝 {score_data.get('date', 'Unknown date')[:10]}: {percentage:.0f}% ⭐")
        elif percentage >= 60:
            st.info(f"📝 {score_data.get('date', 'Unknown date')[:10]}: {percentage:.0f}% 📚")
        else:
            st.warning(f"📝 {score_data.get('date', 'Unknown date')[:10]}: {percentage:.0f}% 💪")

# Challenge section
st.markdown("---")
st.markdown("## 🎯 Weekly Challenge")

if 'weekly_challenge' not in st.session_state:
    challenges = [
        {"goal": "Complete 5 quizzes", "reward": 100, "progress": 0},
        {"goal": "Score 90% or higher on 3 quizzes", "reward": 150, "progress": 0},
        {"goal": "Answer 50 questions correctly", "reward": 200, "progress": 0},
        {"goal": "Study 4 different subjects", "reward": 120, "progress": 0}
    ]
    st.session_state.weekly_challenge = random.choice(challenges)

challenge = st.session_state.weekly_challenge
challenge['progress'] = len(st.session_state.quiz_scores)

st.info(f"""
🎯 **Challenge:** {challenge['goal']}
📊 **Progress:** {challenge['progress']} / {challenge['goal'].split()[1] if challenge['goal'].split()[1].isdigit() else '?'}
🎁 **Reward:** {challenge['reward']} bonus points!
""")

if st.button("Check Challenge Progress"):
    if challenge['progress'] >= int(challenge['goal'].split()[1]) if challenge['goal'].split()[1].isdigit() else False:
        data_manager.award_points(challenge['reward'], "Weekly challenge completed! 🎯", category="bonus")
        st.balloons()
        st.success(f"🎉 Congratulations! You completed the weekly challenge and earned {challenge['reward']} bonus points!")
        # Generate new challenge
        st.session_state.weekly_challenge = random.choice(challenges)
        st.rerun()
    else:
        st.info(f"Keep going! You need {int(challenge['goal'].split()[1]) - challenge['progress']} more to complete the challenge!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    💪 Practice makes progress! Every quiz brings you closer to mastery! 🌟
</div>
""", unsafe_allow_html=True)
