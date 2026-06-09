"""
Syllabus & Lessons Page
Interactive chapter browser with study tools, summaries, and quizzes
"""

import streamlit as st
import random
from datetime import datetime
from utils.data_manager import data_manager
from utils.gemini_helper import get_gemini_helper

# Page configuration
st.set_page_config(
    page_title="Syllabus | Class 4 Learning Hub",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for syllabus page
st.markdown("""
<style>
/* Chapter card styling */
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

/* Content section */
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

/* Tool buttons */
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

/* Progress tracker */
.progress-tracker {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.subject-progress {
    margin: 0.5rem 0;
}

.progress-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.3rem;
}

/* Flashcard styling */
.flashcard {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.flashcard:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

/* Animations */
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

# Initialize helper
gemini_helper = get_gemini_helper()

# Syllabus Data (expanded)
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
                "vocabulary": ["Data", "Information", "RAM", "ROM", "Storage", "Memory", "Volatile", "Non-volatile"],
                "fun_fact": "The first hard disk drive weighed over 1 ton and could only store 5MB of data! Today's tiny SD cards can store thousands of times more! 💾",
                "practice_questions": [
                    "What's the difference between RAM and ROM?",
                    "Name two examples of secondary storage devices.",
                    "Why is RAM called volatile memory?"
                ]
            },
            "Chapter 2: GUI Operating System": {
                "content": "An operating system manages computer hardware and software. Windows 11 is a Graphical User Interface (GUI) OS using icons, windows, and menus. GUI makes computers easy to use with pictures instead of typing commands. Common GUI elements include desktop, taskbar, icons, and start menu.",
                "key_points": [
                    "OS manages hardware and software",
                    "GUI uses pictures and icons",
                    "Windows 11 is a popular GUI OS",
                    "GUI elements: desktop, taskbar, icons, windows"
                ],
                "vocabulary": ["Operating System", "GUI", "Desktop", "Taskbar", "Icon", "Window", "Menu"],
                "fun_fact": "The first GUI was created at Xerox PARC in the 1970s, but Apple made it popular with the Macintosh in 1984! 🖥️",
                "practice_questions": [
                    "What does an operating system do?",
                    "What does GUI stand for?",
                    "Name three GUI elements you see on your computer."
                ]
            },
            "Chapter 3: Internet and Email": {
                "content": "The internet connects millions of computers worldwide. Email lets us send messages instantly to anyone with an email address. Always be safe online - don't share personal information, use strong passwords, and ask parents before clicking links. The World Wide Web (WWW) is the part of internet we browse with websites.",
                "key_points": [
                    "Internet connects computers globally",
                    "Email for instant messaging",
                    "Stay safe online",
                    "WWW = websites we browse"
                ],
                "vocabulary": ["Internet", "Email", "WWW", "Browser", "Password", "Safety", "Website"],
                "fun_fact": "The first email was sent in 1971 by Ray Tomlinson. He chose the @ symbol to separate the username from the computer name! 📧",
                "practice_questions": [
                    "What is the internet?",
                    "List 3 internet safety rules.",
                    "What does @ mean in an email address?"
                ]
            },
            "Chapter 4: MS Paint": {
                "content": "MS Paint is a drawing program that comes with Windows. You can draw shapes, add colors, and create beautiful pictures. Tools include pencil, brush, shapes, text, and fill color. You can save your artwork as an image file and print it. Let your creativity shine!",
                "key_points": [
                    "MS Paint is a drawing program",
                    "Many tools: pencil, brush, shapes, text",
                    "Can save and print artwork",
                    "Great for creative projects"
                ],
                "vocabulary": ["MS Paint", "Tool", "Canvas", "Shape", "Color Palette", "Fill", "Brush"],
                "fun_fact": "MS Paint has been included in Windows since 1985! Many famous digital artists started with MS Paint! 🎨",
                "practice_questions": [
                    "What can you create with MS Paint?",
                    "Name three tools in MS Paint.",
                    "How do you save your drawing?"
                ]
            }
        }
    },
    "English Literature": {
        "icon": "📖",
        "color": "#9C27B0",
        "chapters": {
            "Chapter 1: The Magic Garden": {
                "content": "In a beautiful garden where flowers and plants can talk, they teach us about friendship and caring for nature. The sunflowers stood tall and proud, the roses blushed with beauty, and the daisies danced in the breeze. When children came to play, they learned that every plant has feelings and needs care to grow.",
                "key_points": [
                    "Plants can communicate in this magical story",
                    "Friendship between children and plants",
                    "Caring for nature is important",
                    "Every living thing needs love and care"
                ],
                "vocabulary": ["Garden", "Sunflower", "Daisy", "Blossom", "Nature", "Friendship", "Care"],
                "fun_fact": "Plants can actually communicate through their roots and release chemicals to warn other plants about danger! 🌱",
                "practice_questions": [
                    "What lesson did the children learn?",
                    "How did the plants feel when children cared for them?",
                    "Why is it important to care for nature?"
                ]
            },
            "Chapter 2: The Enchanted Castle": {
                "content": "Gerald, Jimmy, and Kathleen discover an ancient castle with a mysterious hedge maze. At the center, they find a sleeping princess who claims the castle is magical. They learn that true magic comes from friendship, courage, and believing in yourself. The adventure teaches them to face their fears and work together.",
                "key_points": [
                    "Three friends discover a castle",
                    "Hedge maze leads to sleeping princess",
                    "Magic comes from friendship and courage",
                    "Face your fears with friends"
                ],
                "vocabulary": ["Castle", "Enchanted", "Maze", "Princess", "Magic", "Courage", "Adventure"],
                "fun_fact": "Castles often had secret passages and hidden rooms to protect kings and queens from enemies! 🏰",
                "practice_questions": [
                    "Who are the main characters?",
                    "What did they find in the maze?",
                    "What is the real magic in the story?"
                ]
            },
            "Poem: A Home Song": {
                "content": "This beautiful poem describes how a true home is built on love, peace, and coexistence with nature, rather than just brick and mortar. A home is where hearts are happy, where family shares meals and stories, and where everyone feels safe and loved. The poet reminds us that home is not a building, but a feeling.",
                "key_points": [
                    "Home = Love, not just bricks",
                    "Peace and happiness make a home",
                    "Nature is part of a home",
                    "Family makes a home special"
                ],
                "vocabulary": ["Home", "Love", "Peace", "Family", "Shelter", "Comfort", "Belonging"],
                "fun_fact": "The word 'home' comes from the Old English word 'ham' meaning village or estate. It's over 1000 years old! 🏠",
                "practice_questions": [
                    "What makes a house a home?",
                    "Why is love important in a home?",
                    "How does nature connect to a home?"
                ]
            },
            "Chapter 3: The Giving Tree": {
                "content": "A touching story about a tree that gives everything to a boy throughout his life. The tree gives apples, branches, and finally its trunk, always asking nothing in return. It teaches us about unconditional love, sacrifice, and the importance of giving. Sometimes we take things for granted, but true happiness comes from appreciation and gratitude.",
                "key_points": [
                    "Tree gives selflessly to the boy",
                    "Different stages of life",
                    "Unconditional love and sacrifice",
                    "Learn to appreciate what we have"
                ],
                "vocabulary": ["Selfless", "Sacrifice", "Unconditional", "Gratitude", "Appreciation", "Generosity"],
                "fun_fact": "The Giving Tree was published in 1964 and has sold over 10 million copies worldwide! 📚",
                "practice_questions": [
                    "What did the tree give the boy?",
                    "Why is the tree called 'giving'?",
                    "What lesson does this story teach?"
                ]
            }
        }
    },
    "Mathematics": {
        "icon": "🧮",
        "color": "#FF9800",
        "chapters": {
            "Chapter 1: Large Numbers": {
                "content": "Numbers up to 100,000. Learn place value up to lakhs (100,000). Compare numbers using greater than (>), less than (<), and equal to (=). Arrange numbers in ascending (smallest to largest) and descending (largest to smallest) order. Understand expanded form and number names.",
                "key_points": [
                    "Numbers up to 100,000 (1 lakh)",
                    "Place value: Ones, Tens, Hundreds, Thousands, Ten Thousands",
                    "Compare numbers with >, <, =",
                    "Ascending and descending order"
                ],
                "vocabulary": ["Place Value", "Ascending", "Descending", "Greater Than", "Less Than", "Expanded Form"],
                "fun_fact": "The largest number name is 'centillion' which has 303 zeros! That's way more than all the grains of sand on Earth! 🔢",
                "practice_questions": [
                    "Write 45,678 in expanded form.",
                    "Which is larger: 45,678 or 45,876?",
                    "Arrange these numbers in ascending order: 23,456; 23,654; 23,546"
                ]
            },
            "Chapter 2: Addition and Subtraction": {
                "content": "Adding and subtracting 5-digit numbers with regrouping (carrying and borrowing). Learn to add numbers vertically and horizontally. Solve word problems using addition and subtraction. Check your answers using inverse operations (addition to check subtraction, subtraction to check addition).",
                "key_points": [
                    "Add 5-digit numbers with carrying",
                    "Subtract with borrowing",
                    "Word problem strategies",
                    "Use inverse operations to check"
                ],
                "vocabulary": ["Addition", "Subtraction", "Regrouping", "Carry Over", "Borrow", "Inverse Operation"],
                "fun_fact": "The plus (+) sign was first used in 1489! Before that, people wrote 'et' (Latin for 'and') to add numbers! ➕",
                "practice_questions": [
                    "Solve: 45,678 + 32,456 = ?",
                    "Solve: 78,543 - 23,789 = ?",
                    "Word problem: A school has 45,678 students. 12,345 are girls. How many boys?"
                ]
            },
            "Chapter 3: Multiplication": {
                "content": "Multiplying 3-digit numbers by 2-digit numbers using the column method. Understand multiplication as repeated addition. Learn multiplication tables up to 20. Solve real-world multiplication problems. Estimate products by rounding numbers.",
                "key_points": [
                    "Multiply 3-digit × 2-digit numbers",
                    "Multiplication = repeated addition",
                    "Learn tables up to 20",
                    "Estimate products by rounding"
                ],
                "vocabulary": ["Multiplication", "Product", "Factor", "Times Tables", "Estimate", "Column Method"],
                "fun_fact": "The multiplication sign (×) was invented by William Oughtred in 1631. Before that, people used a dot (·) or just put numbers next to each other! ✖️",
                "practice_questions": [
                    "What is 234 × 45?",
                    "If one book costs ₹125, how much do 25 books cost?",
                    "Estimate: 234 × 48 ≈ ?"
                ]
            },
            "Chapter 4: Division": {
                "content": "Dividing numbers with and without remainders. Long division method for 4-digit numbers divided by 1-digit numbers. Understand dividend, divisor, quotient, and remainder. Check division using multiplication. Solve sharing and grouping word problems.",
                "key_points": [
                    "Divide numbers with/without remainder",
                    "Long division method",
                    "Dividend, Divisor, Quotient, Remainder",
                    "Check with multiplication"
                ],
                "vocabulary": ["Division", "Dividend", "Divisor", "Quotient", "Remainder", "Long Division"],
                "fun_fact": "The division sign (÷) is called an 'obelus'. It was first used in 1659 by Johann Rahn! ➗",
                "practice_questions": [
                    "What is 5,678 ÷ 5? (with remainder)",
                    "If 234 candies are shared among 6 friends, how many each?",
                    "Check your answer using multiplication."
                ]
            }
        }
    },
    "Science": {
        "icon": "🔬",
        "color": "#4CAF50",
        "chapters": {
            "Chapter 1: Plants - The Food Makers": {
                "content": "Plants are living things that make their own food through photosynthesis. They need sunlight, water, air, and soil. Parts of a plant: roots absorb water, stem transports food and water, leaves make food, flowers help in reproduction. Photosynthesis happens in leaves using chlorophyll (green color).",
                "key_points": [
                    "Plants make their own food (autotrophs)",
                    "Need: Sunlight, Water, Air, Soil",
                    "Parts: Roots, Stem, Leaves, Flowers",
                    "Photosynthesis uses chlorophyll"
                ],
                "vocabulary": ["Photosynthesis", "Chlorophyll", "Roots", "Stem", "Leaves", "Oxygen", "Carbon Dioxide"],
                "fun_fact": "The tallest tree in the world is Hyperion, a redwood tree in California that is 379.7 feet tall - taller than the Statue of Liberty! 🌲",
                "practice_questions": [
                    "What do plants need to make food?",
                    "Which part of the plant makes food?",
                    "Why are plants called 'producers'?"
                ]
            },
            "Chapter 2: Animals and Their Habitats": {
                "content": "Animals live in different habitats - places that provide food, water, shelter, and space. Types: terrestrial (land), aquatic (water), arboreal (trees), amphibious (both land and water). Animals adapt to their habitats: camels store water, polar bears have thick fur, fish have gills to breathe underwater.",
                "key_points": [
                    "Habitats provide survival needs",
                    "Land, water, tree, and both habitats",
                    "Animals adapt to habitats",
                    "Examples of adaptations"
                ],
                "vocabulary": ["Habitat", "Adaptation", "Terrestrial", "Aquatic", "Arboreal", "Amphibious"],
                "fun_fact": "The Arctic fox can survive temperatures as low as -50°C (-58°F) because of its thick, warm fur! 🦊",
                "practice_questions": [
                    "What is a habitat?",
                    "How do camels adapt to desert life?",
                    "Name three different habitats and give an example animal for each."
                ]
            },
            "Chapter 3: Our Amazing Body": {
                "content": "Our body has many organs that work together. Brain controls everything. Heart pumps blood. Lungs help us breathe. Stomach digests food. Bones give shape and support. Muscles help us move. Eat healthy food, exercise daily, and sleep well to keep your body strong.",
                "key_points": [
                    "Brain: Control center",
                    "Heart: Pumps blood",
                    "Lungs: Breathing",
                    "Stomach: Digests food",
                    "Bones and muscles: Movement"
                ],
                "vocabulary": ["Organs", "Brain", "Heart", "Lungs", "Stomach", "Skeleton", "Muscles"],
                "fun_fact": "Your heart beats about 100,000 times every day! That's 35 million times per year! ❤️",
                "practice_questions": [
                    "What does your brain do?",
                    "Why do we need to eat healthy food?",
                    "How many bones are in an adult human body?"
                ]
            }
        }
    }
}

# Initialize session state for chapter tracking
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

# Subject selector with icons
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

# Calculate progress for this subject
completed_chapters = 0
for chapter_name in chapters_dict.keys():
    chapter_key = f"{st.session_state.current_subject}: {chapter_name}"
    if chapter_key in st.session_state.completed_chapters:
        completed_chapters += 1

progress_percentage = (completed_chapters / total_chapters) * 100 if total_chapters > 0 else 0

# Progress bar
st.markdown(f"""
<div class="progress-tracker">
    <div class="progress-label">
        <span>📊 {subject_data['icon']} {st.session_state.current_subject} Progress</span>
        <span>{completed_chapters}/{total_chapters} chapters completed ({progress_percentage:.0f}%)</span>
    </div>
    <div class="stProgress">
        <div style="width: {progress_percentage}%; background: {subject_data['color']}; height: 8px; border-radius: 4px;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Two column layout - Chapters list and Content
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📑 Chapters")
    
    for chapter_name in chapters_dict.keys():
        chapter_key = f"{st.session_state.current_subject}: {chapter_name}"
        is_completed = chapter_key in st.session_state.completed_chapters
        is_current = st.session_state.current_chapter == chapter_name
        
        # Status badge
        if is_completed:
            status = "✅"
            status_class = "status-completed"
        elif is_current:
            status = "📖"
            status_class = "status-current"
        else:
            status = "📄"
            status_class = "status-pending"
        
        # Chapter button
        if st.button(
            f"{status} {chapter_name[:40]}",
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
        
        # Chapter header
        st.markdown(f"""
        <div class="chapter-card" style="border-top: 4px solid {subject_data['color']};">
            <div class="chapter-title">{subject_data['icon']} {chapter_name}</div>
            <div class="chapter-status { 'status-completed' if is_completed else 'status-pending' }">
                { 'Completed ✓' if is_completed else 'In Progress 📖' }
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Chapter content
        st.markdown('<div class="content-section">', unsafe_allow_html=True)
        st.markdown(f"### 📖 {chapter_name}")
        st.write(chapter_data['content'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key points
        st.markdown("### 💡 Key Points")
        for point in chapter_data['key_points']:
            st.markdown(f'<div class="key-point">• {point}</div>', unsafe_allow_html=True)
        
        # Vocabulary
        st.markdown("### 📚 Vocabulary Words")
        vocab_cols = st.columns(3)
        for idx, word in enumerate(chapter_data['vocabulary']):
            with vocab_cols[idx % 3]:
                st.markdown(f'<div class="vocab-word"><strong>{word}</strong></div>', unsafe_allow_html=True)
        
        # Fun fact
        with st.expander("🎉 Fun Fact!"):
            st.info(chapter_data['fun_fact'])
        
        # Practice questions
        with st.expander("❓ Practice Questions"):
            for q in chapter_data['practice_questions']:
                st.markdown(f"• {q}")
            
            # Check answers with AI
            if st.button("🤖 Check My Answers", use_container_width=True):
                with st.spinner("AI is ready to help..."):
                    prompt = f"Based on the topic '{chapter_name}', provide simple answers to these questions: {', '.join(chapter_data['practice_questions'])}"
                    answers = gemini_helper.generate_response(prompt)
                    st.markdown("### 💬 Exam Buddy Says:")
                    st.info(answers)
                    data_manager.award_points(5, "for practicing with questions!", category="question")
        
        # Learning tools
        st.markdown("---")
        st.markdown("### 🛠️ Learning Tools")
        
        tool_cols = st.columns(3)
        
        with tool_cols[0]:
            if st.button("✨ AI Summary", use_container_width=True):
                with st.spinner("Creating summary..."):
                    summary = gemini_helper.summarize_content(chapter_data['content'], for_child=True)
                    st.markdown(f'<div class="tool-btn">🤖 {summary}</div>', unsafe_allow_html=True)
                    data_manager.award_points(5, "for getting a summary!", category="ai")
        
        with tool_cols[1]:
            if st.button("🎴 Flashcards", use_container_width=True):
                st.session_state.flashcard_mode = True
                st.session_state.current_flashcard = 0
                # Generate flashcards
                with st.spinner("Creating flashcards..."):
                    flashcards = []
                    for point in chapter_data['key_points']:
                        flashcards.append(("Key Point", point))
                    for word in chapter_data['vocabulary']:
                        flashcards.append(("Vocabulary", f"{word}: {chapter_data['content'].split(word)[1][:50] if word in chapter_data['content'] else 'Learn this term'}"[:100]))
                    st.session_state.flashcards = flashcards
                st.rerun()
        
        with tool_cols[2]:
            if st.button("📝 Quick Quiz", use_container_width=True):
                with st.spinner("Generating quiz..."):
                    questions = gemini_helper.create_quiz_questions(chapter_data['content'], num_questions=3)
                    if questions:
                        st.session_state.quiz_questions = questions
                        st.session_state.quiz_active = True
                        st.success("Quiz ready! Go to Practice section to take it!")
                    else:
                        st.warning("Please visit the Practice section for quizzes!")
        
        # Mark as completed button
        if not is_completed:
            st.markdown("---")
            if st.button("✅ Mark as Completed", use_container_width=True):
                data_manager.complete_chapter(chapter_name, st.session_state.current_subject)
                st.balloons()
                st.success(f"🎉 Congratulations! You completed {chapter_name}! +50 points!")
                st.rerun()
    
    else:
        # No chapter selected
        st.info("👈 Select a chapter from the left to start learning!")
        
        # Show achievement for subject completion
        if completed_chapters == total_chapters and total_chapters > 0:
            st.success(f"🎉 AMAZING! You've completed all chapters in {st.session_state.current_subject}! 🎉")
            
            # Special badge check
            if f"{st.session_state.current_subject}_master" not in st.session_state.badges:
                st.balloons()
                st.session_state.badges.append(f"{st.session_state.current_subject}_master")
                st.success(f"🏆 You earned the '{st.session_state.current_subject} Master' badge!")

# Flashcard modal
if st.session_state.get('flashcard_mode', False):
    st.markdown("---")
    st.markdown("## 🎴 Flashcards Mode")
    
    flashcards = st.session_state.get('flashcards', [])
    current_idx = st.session_state.current_flashcard
    
    if flashcards and current_idx < len(flashcards):
        card_type, card_content = flashcards[current_idx]
        
        # Flashcard display
        st.markdown(f"""
        <div class="flashcard">
            <div>
                <div style="font-size: 1.2rem; margin-bottom: 1rem;">📇 {card_type}</div>
                <div style="font-size: 1.1rem;">{card_content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("◀ Previous", use_container_width=True) and current_idx > 0:
                st.session_state.current_flashcard -= 1
                st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center;'>{current_idx + 1} / {len(flashcards)}</div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("Next ▶", use_container_width=True) and current_idx < len(flashcards) - 1:
                st.session_state.current_flashcard += 1
                st.rerun()
        
        if st.button("Close Flashcards", use_container_width=True):
            st.session_state.flashcard_mode = False
            st.rerun()
        
        # Award points for using flashcards
        if 'flashcard_points_awarded' not in st.session_state:
            data_manager.award_points(10, "for using flashcards to study!", category="study")
            st.session_state.flashcard_points_awarded = True
    else:
        st.warning("No flashcards available for this chapter.")
        if st.button("Close"):
            st.session_state.flashcard_mode = False
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    🌟 Keep exploring and learning! Every chapter brings you closer to becoming an expert! 🌟
</div>
""", unsafe_allow_html=True)
