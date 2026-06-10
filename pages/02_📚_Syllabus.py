"""
Syllabus & Lessons Page
Interactive chapter browser with study tools, summaries, and quizzes
"""

import streamlit as st
import random
from datetime import datetime
from utils.data_manager import data_manager
from utils import get_gemini_helper
from utils.github_storage import github_storage

# Page configuration
st.set_page_config(
    page_title="Syllabus | Class 4 Learning Hub",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.chapter-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
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
.progress-tracker {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize helpers
gemini_helper = get_gemini_helper()

# Initialize session state
if 'current_subject' not in st.session_state:
    st.session_state.current_subject = None
if 'current_chapter' not in st.session_state:
    st.session_state.current_chapter = None

# Header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>📚 Syllabus & Learning Hub</h1>
    <p>Explore chapters, learn new concepts, and track your progress! 🌟</p>
</div>
""", unsafe_allow_html=True)

# Get subjects from GitHub
subjects = github_storage.get_subjects()

if subjects:
    # Subject selector
    st.markdown("## 📖 Choose Your Subject")
    
    subject_cols = st.columns(min(len(subjects), 4))
    
    for idx, subject in enumerate(subjects):
        with subject_cols[idx % 4]:
            is_selected = st.session_state.current_subject == subject['name']
            if st.button(
                f"{subject['icon']} {subject['name']}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
                key=f"subject_{subject['id']}"
            ):
                st.session_state.current_subject = subject['name']
                st.session_state.current_chapter = None
                st.rerun()
    
    st.markdown("---")
    
    if st.session_state.current_subject:
        # Find selected subject
        subject_data = next((s for s in subjects if s['name'] == st.session_state.current_subject), None)
        
        if subject_data:
            # Get chapters
            chapters = github_storage.get_chapters(subject_data['folder_name'])
            
            # Calculate progress
            total_chapters = len(chapters)
            completed_chapters = 0
            for chapter in chapters:
                chapter_key = f"{subject_data['name']}: {chapter['title']}"
                if chapter_key in st.session_state.completed_chapters:
                    completed_chapters += 1
            
            progress_percentage = (completed_chapters / total_chapters) * 100 if total_chapters > 0 else 0
            
            st.markdown(f"""
            <div class="progress-tracker">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                    <span>📊 {subject_data['icon']} {subject_data['name']} Progress</span>
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
                
                if chapters:
                    for chapter in chapters:
                        chapter_key = f"{subject_data['name']}: {chapter['title']}"
                        is_completed = chapter_key in st.session_state.completed_chapters
                        is_current = st.session_state.current_chapter == chapter['id']
                        
                        status = "✅" if is_completed else ("📖" if is_current else "📄")
                        
                        if st.button(
                            f"{status} {chapter['title'][:35]}",
                            key=f"chapter_{chapter['id']}",
                            use_container_width=True,
                            type="primary" if is_current else "secondary"
                        ):
                            st.session_state.current_chapter = chapter['id']
                            st.rerun()
                else:
                    st.info("No chapters available for this subject yet.")
            
            with col2:
                if st.session_state.current_chapter:
                    # Find selected chapter
                    chapter_data = next((c for c in chapters if c['id'] == st.session_state.current_chapter), None)
                    
                    if chapter_data:
                        # Get chapter content
                        content = github_storage.get_chapter_content(subject_data['folder_name'], chapter_data['id'])
                        chapter_key = f"{subject_data['name']}: {chapter_data['title']}"
                        is_completed = chapter_key in st.session_state.completed_chapters
                        
                        st.markdown(f"""
                        <div class="chapter-card" style="border-top: 4px solid {subject_data['color']};">
                            <div class="chapter-title">{subject_data['icon']} {chapter_data['title']}</div>
                            <div class="chapter-status {'status-completed' if is_completed else 'status-pending'}">
                                {'Completed ✓' if is_completed else 'In Progress 📖'}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display content
                        if content.get('content'):
                            st.markdown('<div class="content-section">', unsafe_allow_html=True)
                            st.markdown("### 📖 Lesson Content")
                            st.write(content['content'])
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.info("📚 Lesson content is being prepared. Check back soon!")
                        
                        # Display key points
                        if content.get('key_points') and len(content['key_points']) > 0:
                            st.markdown("### 💡 Key Points")
                            for point in content['key_points']:
                                if point and 'coming soon' not in point.lower():
                                    st.markdown(f'<div class="key-point">• {point}</div>', unsafe_allow_html=True)
                        
                        # Display vocabulary
                        if content.get('vocabulary') and len(content['vocabulary']) > 0:
                            st.markdown("### 📚 Vocabulary Words")
                            vocab_cols = st.columns(3)
                            for idx, word in enumerate(content['vocabulary'][:9]):
                                if word and 'coming soon' not in word.lower():
                                    with vocab_cols[idx % 3]:
                                        st.markdown(f'<div class="vocab-word"><strong>{word}</strong></div>', unsafe_allow_html=True)
                        
                        # Display fun fact
                        if content.get('fun_fact') and 'coming soon' not in content['fun_fact'].lower():
                            with st.expander("🎉 Fun Fact!"):
                                st.info(content['fun_fact'])
                        
                        # Display practice questions
                        if content.get('practice_questions') and len(content['practice_questions']) > 0:
                            st.markdown("### ❓ Practice Questions")
                            for q in content['practice_questions']:
                                if q and 'coming soon' not in q.lower():
                                    st.markdown(f"• {q}")
                        
                        # Learning tools
                        st.markdown("---")
                        st.markdown("### 🛠️ Learning Tools")
                        
                        tool_cols = st.columns(2)
                        
                        with tool_cols[0]:
                            if st.button("✨ AI Summary", use_container_width=True):
                                with st.spinner("Creating summary..."):
                                    if content.get('content'):
                                        summary = gemini_helper.summarize_content(content['content'], for_child=True)
                                        st.markdown(f'<div style="background: #e3f2fd; padding: 1rem; border-radius: 10px;">🤖 {summary}</div>', unsafe_allow_html=True)
                                        data_manager.award_points(5, "for getting a summary!", category="ai")
                                    else:
                                        st.info("Content not available for summary yet.")
                        
                        with tool_cols[1]:
                            if st.button("📝 Practice Mode", use_container_width=True):
                                st.info("Go to the Practice section for quizzes!")
                        
                        # Mark as completed button
                        if not is_completed and content.get('content'):
                            st.markdown("---")
                            if st.button("✅ Mark as Completed", use_container_width=True):
                                data_manager.complete_chapter(chapter_data['title'], subject_data['name'])
                                st.balloons()
                                st.success(f"🎉 Congratulations! You completed {chapter_data['title']}! +50 points!")
                                st.rerun()
                    else:
                        st.error(f"Chapter not found: {st.session_state.current_chapter}")
                else:
                    st.info("👈 Select a chapter from the left to start learning!")
    else:
        st.info("👈 Select a subject from above to begin learning!")
else:
    st.warning("📚 No subjects found. Please check your GitHub storage configuration.")

# AI Status
st.markdown("---")
if gemini_helper.is_available:
    st.success("✅ AI Summary features are ready! (Powered by Groq/Llama)")
else:
    st.warning("⚠️ Add your GROQ_API_KEY to Streamlit Secrets to enable AI summaries.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    🌟 Keep exploring and learning! Every chapter brings you closer to becoming an expert! 🌟
</div>
""", unsafe_allow_html=True)
