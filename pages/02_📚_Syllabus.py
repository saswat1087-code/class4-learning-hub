"""
Syllabus & Lessons Page
Interactive chapter browser with study tools, summaries, and quizzes
"""

import streamlit as st
import random
from datetime import datetime
from utils.data_manager import data_manager
from utils import get_gemini_helper  # Using the alias from __init__.py

# Page configuration
st.set_page_config(
    page_title="Syllabus | Class 4 Learning Hub",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for syllabus page
st.markdown("""
<style>
.chapter-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    cursor: pointer;
}
.chapter-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}
.chapter-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 0.5rem;
}
.chapter-status {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: bold;
}
.status-completed {
    background: #4CAF50;
    color: white;
}
.status-pending {
    background: #FF9800;
    color: white;
}
.status-current {
    background: #2196F3;
    color: white;
}
.content-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
}
.key-point {
    background: #e3f2fd;
    padding: 0.8rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    border-left: 4px solid #2196F3;
}
.vocab-word {
    background: #fff3e0;
    padding: 0.5rem;
    border-radius: 8px;
    margin: 0.3rem;
    display: inline-block;
}
.tool-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.75rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem 0;
    transition: all 0.3s ease;
}
.tool-btn:hover {
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}
.progress-tracker {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
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
.fade-in {
    animation: slideIn 0.5s ease;
}
</style>
""", unsafe_allow_html=True)

# Initialize helper - using alias
gemini_helper = get_gemini_helper()

# Syllabus Data
SYLLABUS_DATA = {
    "Computer Science": {
        "icon": "💻",
        "color": "#4A90E2",
        "chapters": {
            "Chapter 1: Storage and Memory Devices": {
                "content": "Data is raw facts. Information is processed data. RAM is volatile random-access memory that temporarily stores data while computer is on. ROM is non-volatile read-only memory that stores permanent instructions. Hard disks and pen drives are secondary storage devices that store data even when computer is off.",
                "key_points": [
                    "Data = Raw facts, Information = Processed data",
                    "RAM is temporary memory (volatile)",
                    "ROM is permanent memory (non-volatile)",
                    "Hard disks and pen drives are secondary storage"
                ],
                "vocabulary": ["Data", "Information", "RAM", "ROM", "Storage", "Memory"],
                "fun_fact": "The first hard disk drive weighed over 1 ton and could only store 5MB of data! Today's tiny SD cards can store thousands of times more! 💾"
            },
            "Chapter 2: GUI Operating System": {
                "content": "An operating system manages computer hardware and software. Windows 11 is a Graphical User Interface (GUI) OS using icons, windows, and menus. GUI makes computers easy to use with pictures instead of typing commands.",
                "key_points": [
                    "OS manages hardware and software",
                    "GUI uses pictures and icons",
                    "Windows 11 is a popular GUI OS",
                    "GUI elements: desktop, taskbar, icons, windows"
                ],
                "vocabulary": ["Operating System", "GUI", "Desktop", "Taskbar", "Icon", "Window"],
                "fun_fact": "The first GUI was created at Xerox PARC in the 1970s! 🖥️"
            },
            "Chapter 3: Internet and Email": {
                "content": "The internet connects millions of computers worldwide. Email lets us send messages instantly to anyone with an email address. Always be safe online - don't share personal information, use strong passwords, and ask parents before clicking links.",
                "key_points": [
                    "Internet connects computers globally",
                    "Email for instant messaging",
                    "Stay safe online",
                    "WWW = websites we browse"
                ],
                "vocabulary": ["Internet", "Email", "WWW", "Browser", "Password", "Safety"],
                "fun_fact": "The first email was sent in 1971 by Ray Tomlinson. He chose the @ symbol! 📧"
            }
        }
    },
    "English Literature": {
        "icon": "📖",
        "color": "#9C27B0",
        "chapters": {
            "Chapter 1: The Magic Garden": {
                "content": "In a beautiful garden where flowers and plants can talk, they teach us about friendship and caring for nature. The sunflowers stood tall and proud, the roses blushed with beauty, and the daisies danced in the breeze.",
                "key_points": [
                    "Plants can communicate in this magical story",
                    "Friendship between children and plants",
                    "Caring for nature is important",
                    "Every living thing needs love and care"
                ],
                "vocabulary": ["Garden", "Sunflower", "Daisy", "Blossom", "Nature", "Friendship"],
                "fun_fact": "Plants can actually communicate through their roots and release chemicals to warn other plants about danger! 🌱"
            },
            "Chapter 2: The Enchanted Castle": {
                "content": "Gerald, Jimmy, and Kathleen discover an ancient castle with a mysterious hedge maze. At the center, they find a sleeping princess who claims the castle is magical. The adventure teaches them to face their fears and work together.",
                "key_points": [
                    "Three friends discover a castle",
                    "Hedge maze leads to sleeping princess",
                    "Magic comes from friendship and courage",
                    "Face your fears with friends"
                ],
                "vocabulary": ["Castle", "Enchanted", "Maze", "Princess", "Magic", "Courage"],
                "fun_fact": "Castles often had secret passages and hidden rooms to protect kings and queens from enemies! 🏰"
            },
            "Poem: A Home Song": {
                "content": "This beautiful poem describes how a true home is built on love, peace, and coexistence with nature, rather than just brick and mortar. A home is where hearts are happy, where family shares meals and stories.",
                "key_points": [
                    "Home = Love, not just bricks",
                    "Peace and happiness make a home",
                    "Nature is part of a home",
                    "Family makes a home special"
                ],
                "vocabulary": ["Home", "Love", "Peace", "Family", "Shelter", "Comfort"],
                "fun_fact": "The word 'home' comes from the Old English word 'ham' meaning village or estate! 🏠"
            }
        }
    },
    "Mathematics": {
        "icon": "🧮",
        "color": "#FF9800",
        "chapters": {
            "Chapter 1: Large Numbers": {
                "content": "Numbers up to 100,000. Learn place value up to lakhs (100,000). Compare numbers using greater than (>), less than (<), and equal to (=). Arrange numbers in ascending and descending order.",
                "key_points": [
                    "Numbers up to 100,000 (1 lakh)",
                    "Place value: Ones, Tens, Hundreds, Thousands, Ten Thousands",
                    "Compare numbers with >, <, =",
                    "Ascending and descending order"
                ],
                "vocabulary": ["Place Value", "Ascending", "Descending", "Greater Than", "Less Than"],
                "fun_fact": "The largest number name is 'centillion' which has 303 zeros! 🔢"
            },
            "Chapter 2: Addition and Subtraction": {
                "content": "Adding and subtracting 5-digit numbers with regrouping (carrying and borrowing). Learn to add numbers vertically and horizontally. Solve word problems using addition and subtraction.",
                "key_points": [
                    "Add 5-digit numbers with carrying",
                    "Subtract with borrowing",
                    "Word problem strategies",
                    "Use inverse operations to check"
                ],
                "vocabulary": ["Addition", "Subtraction", "Regrouping", "Carry Over", "Borrow"],
                "fun_fact": "The plus (+) sign was first used in 1489! Before that, people wrote 'et' (Latin for 'and')! ➕"
            },
            "Chapter 3: Multiplication": {
                "content": "Multiplying 3-digit numbers by 2-digit numbers using the column method. Understand multiplication as repeated addition. Learn multiplication tables up to 20.",
                "key_points": [
                    "Multiply 3-digit × 2-digit numbers",
                    "Multiplication = repeated addition",
                    "Learn tables up to 20",
                    "Estimate products by rounding"
                ],
                "vocabulary": ["Multiplication", "Product", "Factor", "Times Tables", "Estimate"],
                "fun_fact": "The multiplication sign (×) was invented by William Oughtred in 1631! ✖️"
            }
        }
    },
    "Science": {
        "icon": "🔬",
        "color": "#4CAF50",
        "chapters": {
            "Chapter 1: Plants": {
                "content": "Plants are living things that make their own food through photosynthesis. They need sunlight, water, air, and soil. Parts of a plant: roots absorb water, stem transports food and water, leaves make food, flowers help in reproduction.",
                "key_points": [
                    "Plants make their own food (autotrophs)",
                    "Need: Sunlight, Water, Air, Soil",
                    "Parts: Roots, Stem, Leaves, Flowers",
                    "Photosynthesis uses chlorophyll"
                ],
                "vocabulary": ["Photosynthesis", "Chlorophyll", "Roots", "Stem", "Leaves", "Oxygen"],
                "fun_fact": "The tallest tree in the world is Hyperion, a redwood tree that is 379.7 feet tall! 🌲"
            },
            "Chapter 2: Animals": {
                "content": "Animals live in different habitats - places that provide food, water, shelter, and space. Types: terrestrial (land), aquatic (water), arboreal (trees), amphibious (both land and water).",
                "key_points": [
                    "Habitats provide survival needs",
                    "Land, water, tree, and both habitats",
                    "Animals adapt to habitats",
                    "Examples of adaptations"
                ],
                "vocabulary": ["Habitat", "Adaptation", "Terrestrial", "Aquatic", "Arboreal"],
                "fun_fact": "The Arctic fox can survive temperatures as low as -50°C (-58°F) because of its thick fur! 🦊"
            },
            "Chapter 3: Our Body": {
                "content": "Our body has many organs that work together. Brain controls everything. Heart pumps blood. Lungs help us breathe. Stomach digests food. Bones give shape and support. Muscles help us move.",
                "key_points": [
                    "Brain: Control center",
                    "Heart: Pumps blood",
                    "Lungs: Breathing",
                    "Stomach: Digests food",
                    "Bones and muscles: Movement"
                ],
                "vocabulary": ["Organs", "Brain", "Heart", "Lungs", "Stomach", "Skeleton"],
                "fun_fact": "Your heart beats about 100,000 times every day! That's 35 million times per year! ❤️"
            }
        }
    }
}

# Initialize session state
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = "Computer Science"
if 'current_chapter' not in st.session_state:
    st.session_state.current_chapter = None
if 'flashcard_mode' not in st.session_state:
    st.session_state.flashcard_mode = False
if 'current_flashcard' not in st.session_state:
    st.session_state.current_flashcard = 0

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>📚 Syllabus & Learning Hub</h1>
    <p>Explore chapters, learn new concepts, and track your progress! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Subject selector
st.markdown("## 📖 Choose Your Subject")

subject_cols = st.columns(4)
subjects_list = list(SYLLABUS_DATA.keys())

for idx, subject in enumerate(subjects_list):
    subject_data = SYLLABUS_DATA[subject]
    is_selected = st.session_state.current_subject == subject
    
    with subject_cols[idx]:
        if st.button(
            f"{subject_data['icon']} {subject}",
            use_container_width=True,
            type="primary" if is_selected else "secondary"
        ):
            st.session_state.current_subject = subject
            st.session_state.current_chapter = None
            st.rerun()

st.markdown("---")

# Subject progress tracking
subject_data = SYLLABUS_DATA[st.session_state.current_subject]
chapters_dict = subject_data['chapters']
total_chapters = len(chapters_dict)

completed_chapters = 0
for chapter_name in chapters_dict.keys():
    chapter_key = f"{st.session_state.current_subject}: {chapter_name}"
    if chapter_key in st.session_state.completed_chapters:
        completed_chapters += 1

progress_percentage = (completed_chapters / total_chapters) * 100 if total_chapters > 0 else 0

st.markdown(f"""
<div class="progress-tracker">
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
        <span>📊 {subject_data['icon']} {st.session_state.current_subject} Progress</span>
        <span>{completed_chapters}/{total_chapters} chapters completed ({progress_percentage:.0f}%)</span>
    </div>
    <div style="background: #e0e0e0; border-radius: 10px; overflow: hidden;">
        <div style="width: {progress_percentage}%; background: {subject_data['color']}; height: 10px; border-radius: 10px;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Two column layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📑 Chapters")
    
    for chapter_name in chapters_dict.keys():
        chapter_key = f"{st.session_state.current_subject}: {chapter_name}"
        is_completed = chapter_key in st.session_state.completed_chapters
        is_current = st.session_state.current_chapter == chapter_name
        
        if is_completed:
            status = "✅"
        elif is_current:
            status = "📖"
        else:
            status = "📄"
        
        if st.button(
            f"{status} {chapter_name[:35]}",
            key=f"chapter_{chapter_name}",
            use_container_width=True,
            type="primary" if is_current else "secondary"
        ):
            st.session_state.current_chapter = chapter_name
            st.rerun()

with col2:
    if st.session_state.current_chapter:
        chapter_name = st.session_state.current_chapter
        chapter_data = chapters_dict[chapter_name]
        chapter_key = f"{st.session_state.current_subject}: {chapter_name}"
        is_completed = chapter_key in st.session_state.completed_chapters
        
        st.markdown(f"""
        <div class="chapter-card" style="border-top: 4px solid {subject_data['color']};">
            <div class="chapter-title">{subject_data['icon']} {chapter_name}</div>
            <div class="chapter-status {'status-completed' if is_completed else 'status-pending'}">
                {'Completed ✓' if is_completed else 'In Progress 📖'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown(f"### 📖 {chapter_name}")
        st.write(chapter_data['content'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 💡 Key Points")
        for point in chapter_data['key_points']:
            st.markdown(f'<div class="key-point">• {point}</div>', unsafe_allow_html=True)
        
        st.markdown("### 📚 Vocabulary Words")
        vocab_cols = st.columns(3)
        for idx, word in enumerate(chapter_data['vocabulary']):
            with vocab_cols[idx % 3]:
                st.markdown(f'<div class="vocab-word"><strong>{word}</strong></div>', unsafe_allow_html=True)
        
        with st.expander("🎉 Fun Fact!"):
            st.info(chapter_data['fun_fact'])
        
        st.markdown("---")
        st.markdown("### 🛠️ Learning Tools")
        
        tool_cols = st.columns(2)
        
        with tool_cols[0]:
            if st.button("✨ AI Summary", use_container_width=True):
                with st.spinner("Creating summary..."):
                    summary = gemini_helper.summarize_content(chapter_data['content'], for_child=True)
                    st.markdown(f'<div class="tool-btn">🤖 {summary}</div>', unsafe_allow_html=True)
                    data_manager.award_points(5, "for getting a summary!", category="ai")
        
        with tool_cols[1]:
            if st.button("📝 Quick Quiz", use_container_width=True):
                with st.spinner("Generating quiz..."):
                    questions = gemini_helper.create_quiz_questions(chapter_data['content'], num_questions=3)
                    if questions:
                        st.success("✅ Quiz ready! Go to the Practice section to take it!")
                    else:
                        st.info("📚 Try the Practice section for quizzes!")
        
        if not is_completed:
            st.markdown("---")
            if st.button("✅ Mark as Completed", use_container_width=True):
                data_manager.complete_chapter(chapter_name, st.session_state.current_subject)
                st.balloons()
                st.success(f"🎉 Congratulations! You completed {chapter_name}! +50 points!")
                st.rerun()
    else:
        st.info("👈 Select a chapter from the left to start learning!")
        
        if completed_chapters == total_chapters and total_chapters > 0:
            st.success(f"🎉 AMAZING! You've completed all chapters in {st.session_state.current_subject}! 🎉")

# AI Status
st.markdown("---")
if gemini_helper.is_available:
    st.success("✅ AI Summary features are ready! (Powered by Groq/Llama)")
else:
    st.warning("⚠️ Add your GROQ_API_KEY to Streamlit Secrets to enable AI summaries and quizzes.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    🌟 Keep exploring and learning! Every chapter brings you closer to becoming an expert! 🌟
</div>
""", unsafe_allow_html=True)
