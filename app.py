import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Class 4 Learning Hub | AI-Powered Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for kid-friendly styling
def load_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease;
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    /* Chat message styling */
    .chat-message {
        background-color: #f0f2f6;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #4A90E2;
        animation: slideIn 0.5s ease;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 12px 18px;
        margin: 8px 0;
        text-align: right;
        animation: slideInRight 0.5s ease;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Info/Warning boxes */
    .stAlert {
        border-radius: 10px;
        animation: fadeIn 0.5s ease;
    }
    
    /* Metric styling */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    /* Celebration animation */
    .celebration {
        animation: bounce 0.6s ease;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 5px 10px;
        margin: 5px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .stButton > button {
            width: 100%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_css()

# Initialize session state variables
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'quiz_scores': {},
        'completed_chapters': [],
        'chat_history': [],
        'points_earned': 0,
        'badges': [],
        'daily_streak': 0,
        'last_active': None,
        'user_name': "Learner",
        'total_questions_answered': 0,
        'correct_answers': 0,
        'study_time': 0,
        'current_streak': 0,
        'longest_streak': 0
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Update daily streak
    if st.session_state.last_active:
        last_date = datetime.strptime(st.session_state.last_active, "%Y-%m-%d")
        today = datetime.now()
        if (today - last_date).days == 1:
            st.session_state.daily_streak += 1
            st.session_state.current_streak += 1
            if st.session_state.current_streak > st.session_state.longest_streak:
                st.session_state.longest_streak = st.session_state.current_streak
        elif (today - last_date).days > 1:
            st.session_state.daily_streak = 1
            st.session_state.current_streak = 1
    
    st.session_state.last_active = datetime.now().strftime("%Y-%m-%d")

# Initialize session state
init_session_state()

# Initialize Gemini client
try:
    from google import genai
    
    # Try to get API key from various sources
    api_key = os.getenv('GEMINI_API_KEY') or st.secrets.get("GEMINI_API_KEY", "")
    
    if not api_key:
        st.warning("""
        ⚠️ **API Key Not Found!**
        
        To use AI features, please set your Gemini API key:
        1. Get a free key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Add it to `.env` file: `GEMINI_API_KEY=your_key_here`
        3. Or add to Streamlit secrets when deploying
        
        The app will work with limited functionality until then.
        """)
        client = None
    else:
        client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"🔧 Error initializing AI: {str(e)}")
    client = None

# Helper functions
def generate_ai_response(prompt):
    """Generate response from Gemini AI"""
    if not client:
        return "🤖 I'm here to help! Please set up your Gemini API key to use all AI features. Check the sidebar for instructions."
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"🤔 I'm having a little trouble thinking right now. Error: {str(e)[:100]}"

def award_points(points, reason=""):
    """Award points to the user and check for badges"""
    st.session_state.points_earned += points
    st.session_state.total_questions_answered += 1
    
    # Show celebration
    if points > 0:
        st.toast(f"🎉 You earned {points} points! {reason}", icon="⭐")
    
    # Check for badges
    new_badge = check_badges()
    if new_badge:
        st.balloons()
        st.success(f"🏆 Congratulations! You earned the '{new_badge}' badge! 🏆")
    
    return points

def check_badges():
    """Check and award badges based on achievements"""
    badges_to_check = {
        'First Steps': st.session_state.points_earned >= 50,
        'Quiz Starter': len(st.session_state.quiz_scores) >= 1,
        'Knowledge Seeker': len(st.session_state.quiz_scores) >= 3,
        'Chapter Master': len(st.session_state.completed_chapters) >= 3,
        'Perfect Score': any(score.get('percentage', 0) == 100 for score in st.session_state.quiz_scores.values()),
        '100 Points Club': st.session_state.points_earned >= 100,
        'Star Learner': st.session_state.points_earned >= 500,
        'Streak Champion': st.session_state.current_streak >= 7,
        'Quiz Champion': len(st.session_state.quiz_scores) >= 10,
        'Learning Legend': st.session_state.points_earned >= 1000
    }
    
    for badge, earned in badges_to_check.items():
        if earned and badge not in st.session_state.badges:
            st.session_state.badges.append(badge)
            return badge
    return None

# Sidebar content
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2948/2948228.png", width=80)
    st.title("🎒 Class 4 Hub")
    
    # User info
    st.markdown(f"### 👋 Hello, {st.session_state.user_name}!")
    
    # Progress metrics
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("⭐ Points", st.session_state.points_earned)
    with col2:
        st.metric("🏆 Badges", len(st.session_state.badges))
    
    # Streak display
    if st.session_state.current_streak > 0:
        st.markdown(f"🔥 **Current Streak:** {st.session_state.current_streak} days")
        if st.session_state.longest_streak > 0:
            st.markdown(f"🏆 **Best Streak:** {st.session_state.longest_streak} days")
    
    # Progress bar
    progress_percent = min(st.session_state.points_earned / 500, 1.0)
    st.progress(progress_percent)
    st.caption(f"Level {int(progress_percent * 10) + 1} • Next level: {500 - st.session_state.points_earned} points")
    
    # Navigation
    st.markdown("---")
    app_mode = st.radio(
        "📖 Navigate to:",
        ["🏠 Home Dashboard", "📚 Syllabus & Lessons", "🏆 Practice & Tests", "🤖 Exam Buddy AI", "📊 My Progress"],
        index=0
    )
    
    # Parent Zone
    st.markdown("---")
    with st.expander("👨‍👩‍👧 Parent Zone"):
        admin_password = st.text_input("Enter access code:", type="password")
        if admin_password == "class4teacher2026":
            st.success("✅ Access Granted!")
            st.info(f"""
            **Learning Report:**
            - Total Points: {st.session_state.points_earned}
            - Quizzes Taken: {len(st.session_state.quiz_scores)}
            - Chapters Completed: {len(st.session_state.completed_chapters)}
            - Badges: {len(st.session_state.badges)}
            - Current Streak: {st.session_state.current_streak} days
            """)
            if st.button("Download Report"):
                report = f"""
                Class 4 Learning Hub - Progress Report
                =====================================
                Student: {st.session_state.user_name}
                Date: {datetime.now().strftime("%Y-%m-%d")}
                
                Statistics:
                - Total Points: {st.session_state.points_earned}
                - Quizzes Completed: {len(st.session_state.quiz_scores)}
                - Chapters Completed: {len(st.session_state.completed_chapters)}
                - Badges Earned: {', '.join(st.session_state.badges)}
                - Current Streak: {st.session_state.current_streak} days
                - Longest Streak: {st.session_state.longest_streak} days
                
                Quiz Scores:
                {st.session_state.quiz_scores}
                """
                st.download_button("📥 Save Report", report, file_name=f"progress_{datetime.now().strftime('%Y%m%d')}.txt")
        else:
            st.info("🔒 Parent access requires a code")
    
    # API Key status
    st.markdown("---")
    if client:
        st.success("✅ AI Assistant: Ready")
    else:
        st.warning("⚠️ AI features limited")
        st.caption("Add GEMINI_API_KEY to .env file")

# Syllabus data
SYLLABUS_DATA = {
    "Computer Science": {
        "Chapter 1: Storage and Memory Devices": "Data is raw facts. Information is processed data. RAM is volatile random-access memory. ROM is non-volatile read-only memory. Hard disks and pen drives are secondary storage.",
        "Chapter 2: GUI Operating System": "An operating system manages computer hardware and software. Windows 11 is a Graphical User Interface (GUI) OS using icons and menus.",
        "Chapter 3: Internet and Email": "The internet connects computers worldwide. Email lets us send messages online. Always be safe online!",
        "Chapter 4: MS Paint": "MS Paint is a drawing program. Learn to use shapes, colors, and tools to create beautiful pictures."
    },
    "English Literature": {
        "Chapter 1: The Magic Garden": "A beautiful garden where flowers and plants can talk. They teach us about friendship and caring for nature.",
        "Chapter 2: The Enchanted Castle": "Gerald, Jimmy, and Kathleen discover a castle with a hedge maze. They find a sleeping princess at the center who claims the castle is magical.",
        "Poem: A Home Song": "The poem describes how a true home is built on love, peace, and coexistence with nature, rather than just brick and mortar.",
        "Chapter 3: The Giving Tree": "A touching story about a tree that gives everything to a boy, teaching us about love and sacrifice."
    },
    "Mathematics": {
        "Chapter 1: Large Numbers": "Numbers up to 100,000. Learn place value, comparing numbers, and ordering.",
        "Chapter 2: Addition and Subtraction": "Adding and subtracting 5-digit numbers with regrouping.",
        "Chapter 3: Multiplication": "Multiplying 3-digit numbers by 2-digit numbers.",
        "Chapter 4: Division": "Dividing numbers with and without remainders."
    },
    "Science": {
        "Chapter 1: Plants": "Parts of a plant - roots, stem, leaves, flowers. Photosynthesis and how plants make food.",
        "Chapter 2: Animals": "Classification of animals - herbivores, carnivores, omnivores. Animal habitats.",
        "Chapter 3: Our Body": "Major organs - heart, lungs, brain, stomach. How they work together."
    }
}

PROJECTS_DATA = {
    "English Lit Project": "Task: Create a 3D model of a 'Hanging Garden Tree House' based on the poem 'A Home Song'. Show human and nature coexistence. Materials: Mount board, popsicle sticks, yarn, toothpicks, real soil sprout. Deadline: June 30, 2026.",
    "Science Project": "Task: Make a poster showing the life cycle of a plant. Include seeds, germination, seedling, adult plant, and flowers/fruits.",
    "Computer Project": "Task: Create a digital drawing in MS Paint showing your dream house. Use at least 5 different tools and 10 shapes."
}

# Main content area based on navigation
st.markdown('<div class="main-header">', unsafe_allow_html=True)

if app_mode == "🏠 Home Dashboard":
    st.markdown('<h1>🌟 Welcome to Class 4 Learning Hub!</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>Hello <strong>{st.session_state.user_name}</strong>! Ready for an amazing learning adventure today? 🚀</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Today's motivation
    motivational_quotes = [
        "💫 \"The more you read, the more things you will know!\"",
        "🎯 \"Practice makes progress, not perfect!\"",
        "🌟 \"Every expert was once a beginner!\"",
        "📚 \"Learning is a treasure that will follow you everywhere!\"",
        "🚀 \"Your attitude determines your direction!\""
    ]
    import random
    st.info(random.choice(motivational_quotes))
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📚 Today's Goal")
        st.write("Complete one chapter and earn 50 points!")
        if st.button("Start Learning →", key="home_study"):
            app_mode = "📚 Syllabus & Lessons"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🎯 Daily Challenge")
        remaining = 5 - st.session_state.total_questions_answered
        if remaining > 0:
            st.write(f"Answer {remaining} more questions today!")
        else:
            st.write("🎉 You've completed today's challenge!")
        if st.button("Take Quiz →", key="home_quiz"):
            app_mode = "🏆 Practice & Tests"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏆 Achievements")
        st.write(f"📊 Progress: {int(progress_percent * 100)}% to next level")
        st.write(f"⭐ Total Points: {st.session_state.points_earned}")
        st.write(f"🎖️ Badges: {len(st.session_state.badges)}")
        if st.button("View Progress →", key="home_progress"):
            app_mode = "📊 My Progress"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("---")
    st.subheader("📖 Quick Actions")
    quick_cols = st.columns(4)
    
    with quick_cols[0]:
        if st.button("📚 Computer Science", use_container_width=True):
            app_mode = "📚 Syllabus & Lessons"
            st.rerun()
    
    with quick_cols[1]:
        if st.button("📖 English", use_container_width=True):
            app_mode = "📚 Syllabus & Lessons"
            st.rerun()
    
    with quick_cols[2]:
        if st.button("🧮 Mathematics", use_container_width=True):
            app_mode = "📚 Syllabus & Lessons"
            st.rerun()
    
    with quick_cols[3]:
        if st.button("🔬 Science", use_container_width=True):
            app_mode = "📚 Syllabus & Lessons"
            st.rerun()
    
    # Featured content
    st.markdown("---")
    st.subheader("🎨 Featured Project")
    st.info(f"**{list(PROJECTS_DATA.keys())[0]}**\n\n{list(PROJECTS_DATA.values())[0]}")

elif app_mode == "📚 Syllabus & Lessons":
    st.markdown('<h1>📚 Syllabus & Lessons</h1>', unsafe_allow_html=True)
    st.markdown('<p>Explore your subjects and learn something new today!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        subject = st.selectbox("📖 Select Subject:", list(SYLLABUS_DATA.keys()))
    
    with col2:
        chapters = list(SYLLABUS_DATA[subject].keys())
        chapter = st.selectbox("📑 Select Chapter:", chapters)
    
    st.markdown("---")
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    st.subheader(f"📖 {chapter}")
    content = SYLLABUS_DATA[subject][chapter]
    st.write(content)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✨ Simplify for me", use_container_width=True):
            with st.spinner("Making it easier to understand..."):
                prompt = f"Explain this Class 4 topic to a 9-year-old in simple words with fun emojis and examples: {content}"
                summary = generate_ai_response(prompt)
                st.markdown(f'<div class="chat-message">🤖 <strong>Exam Buddy says:</strong><br>{summary}</div>', unsafe_allow_html=True)
                award_points(5, "for asking a question!")
    
    with col2:
        if st.button("📝 Take a quiz", use_container_width=True):
            with st.spinner("Creating quiz..."):
                prompt = f"Create 3 multiple choice questions for Class 4 students based on: {content}. Format with Q:, options A-D, Answer:, and Explanation:"
                quiz = generate_ai_response(prompt)
                st.markdown(f'<div class="chat-message">📋 <strong>Quick Quiz:</strong><br>{quiz}</div>', unsafe_allow_html=True)
                award_points(10, "for starting a quiz!")
    
    with col3:
        if st.button("✅ Mark as completed", use_container_width=True):
            if chapter not in st.session_state.completed_chapters:
                st.session_state.completed_chapters.append(chapter)
                award_points(20, f"for completing {chapter}!")
                st.balloons()
                st.success(f"🎉 Great job completing {chapter}! 🌟")
            else:
                st.info("📚 You've already completed this chapter!")
    
    # Related projects
    if subject == "English Literature":
        st.markdown("---")
        st.subheader("🎨 Related Project")
        st.info(PROJECTS_DATA["English Lit Project"])

elif app_mode == "🏆 Practice & Tests":
    st.markdown('<h1>🏆 Practice & Tests</h1>', unsafe_allow_html=True)
    st.markdown('<p>Test your knowledge and earn points!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quiz setup
    col1, col2 = st.columns(2)
    
    with col1:
        quiz_subject = st.selectbox("Choose subject:", list(SYLLABUS_DATA.keys()), key="quiz_subject")
    
    with col2:
        quiz_chapter = st.selectbox("Choose chapter:", list(SYLLABUS_DATA[quiz_subject].keys()), key="quiz_chapter")
    
    if st.button("🎲 Generate Quiz", use_container_width=True):
        content = SYLLABUS_DATA[quiz_subject][quiz_chapter]
        with st.spinner("Creating your personalized quiz..."):
            prompt = f"Create 5 multiple choice questions for Class 4 based on: {content}. Make it fun! Format each as: Q: [question]\\nA) [option]\\nB) [option]\\nC) [option]\\nD) [option]\\nAnswer: [letter]\\nExplanation: [simple explanation]"
            quiz_content = generate_ai_response(prompt)
            st.session_state.current_quiz = quiz_content
            st.session_state.quiz_active = True
            st.rerun()
    
    if st.session_state.get('quiz_active', False):
        st.markdown("---")
        st.subheader("📝 Your Quiz")
        st.markdown(f'<div class="card">{st.session_state.current_quiz}</div>', unsafe_allow_html=True)
        
        # Answer input (simplified - in production, parse MCQs)
        user_answer = st.text_input("Your answer (A, B, C, or D):")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Answer", use_container_width=True):
                award_points(10, "for attempting the quiz!")
                st.success("✅ Answer submitted! Check the explanation above.")
                st.session_state.quiz_active = False
                st.rerun()
        with col2:
            if st.button("New Quiz", use_container_width=True):
                st.session_state.quiz_active = False
                st.rerun()

elif app_mode == "🤖 Exam Buddy AI":
    st.markdown('<h1>🤖 Exam Buddy AI</h1>', unsafe_allow_html=True)
    st.markdown('<p>Your AI study partner - ask me anything!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat history display
    for message in st.session_state.chat_history[-10:]:  # Show last 10 messages
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
    
    # Quick question buttons
    st.subheader("Quick Questions")
    quick_q_cols = st.columns(3)
    
    quick_questions = [
        "Help me study for Computer Science",
        "Explain multiplication simply",
        "Give me a fun fact about plants"
    ]
    
    for idx, q in enumerate(quick_questions):
        with quick_q_cols[idx % 3]:
            if st.button(q, use_container_width=True):
                with st.spinner("Thinking..."):
                    response = generate_ai_response(f"Answer for a 9-year-old: {q}")
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    award_points(2, "for asking a question!")
                    st.rerun()
    
    # Chat input
    st.markdown("---")
    user_input = st.text_input("💬 Ask Exam Buddy anything:", key="chat_input")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        with st.spinner("🤖 Thinking..."):
            prompt = f"""
            You are Exam Buddy, a friendly AI tutor for a 9-year-old Class 4 student.
            Be encouraging, use emojis, and give simple explanations with examples.
            Keep responses to 2-3 sentences unless asked for more details.
            
            Student's question: {user_input}
            
            Respond in a fun, helpful way:
            """
            response = generate_ai_response(prompt)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            award_points(3, "for learning with Exam Buddy!")
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
        st.rerun()

elif app_mode == "📊 My Progress":
    st.markdown('<h1>📊 My Progress Report</h1>', unsafe_allow_html=True)
    st.markdown('<p>See how much you\'ve learned!</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("⭐ Total Points", st.session_state.points_earned, delta=50 if st.session_state.points_earned > 0 else None)
    with col2:
        st.metric("📚 Chapters Done", len(st.session_state.completed_chapters), delta=1 if st.session_state.completed_chapters else None)
    with col3:
        st.metric("🏆 Badges Earned", len(st.session_state.badges))
    with col4:
        st.metric("🔥 Current Streak", f"{st.session_state.current_streak} days")
    
    # Badges display
    if st.session_state.badges:
        st.subheader("🏅 Your Badges Collection")
        badge_cols = st.columns(min(len(st.session_state.badges), 4))
        for idx, badge in enumerate(st.session_state.badges):
            with badge_cols[idx % 4]:
                st.markdown(f'<div class="badge">🏆 {badge}</div>', unsafe_allow_html=True)
    else:
        st.info("🌟 Complete quizzes and chapters to earn badges! Start your learning journey today!")
    
    # Completed chapters
    if st.session_state.completed_chapters:
        st.subheader("✅ Completed Chapters")
        for chapter in st.session_state.completed_chapters:
            st.success(f"📖 {chapter}")
    
    # Quiz scores
    if st.session_state.quiz_scores:
        st.subheader("📊 Quiz Performance")
        for quiz_name, score in st.session_state.quiz_scores.items():
            st.markdown(f"**{quiz_name.replace('_quiz', '')}:** {score} points")
    
    # Learning tips
    st.markdown("---")
    st.subheader("💡 Learning Tips")
    tips = [
        "📚 Read for 20 minutes every day",
        "✏️ Take notes while studying",
        "🤔 Ask questions when confused",
        "🎯 Practice with quizzes regularly",
        "⭐ Review what you learned each week"
    ]
    for tip in tips:
        st.markdown(f"• {tip}")

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown("Made with ❤️ for Class 4 Students | Keep Learning, Keep Growing! 🌟")
st.markdown('</div>', unsafe_allow_html=True)
