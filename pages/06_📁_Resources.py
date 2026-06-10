"""
Resources Page - View assignments, revision papers, and projects
"""

import streamlit as st
import requests
from utils.github_storage import github_storage

st.set_page_config(
    page_title="Resources | Class 4 Learning Hub",
    page_icon="📁",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.resource-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    border-left: 4px solid #667eea;
    transition: all 0.3s ease;
}
.resource-card:hover {
    transform: translateX(5px);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.subject-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}
.download-btn {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 0.3rem 1rem;
    border-radius: 5px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

st.title("📁 Learning Resources Hub")
st.markdown("Access all your assignments, revision papers, and projects in one place!")

# Create tabs for different resource types
tab1, tab2, tab3 = st.tabs(["📝 Assignments", "📚 Revision Papers", "🎯 Projects"])

# ==================== TAB 1: ASSIGNMENTS ====================
with tab1:
    st.header("📝 Subject-wise Assignments")
    
    # Define subjects with their icons and colors
    subjects_config = {
        "2ND LANGUAGE BENGALI": {"icon": "🇧🇩", "color": "#FF9800"},
        "2ND LANGUAGE HINDI": {"icon": "🇮🇳", "color": "#FF5722"},
        "COMPUTER": {"icon": "💻", "color": "#4A90E2"},
        "ENGLISH LANGUAGE": {"icon": "✍️", "color": "#9C27B0"},
        "ENGLISH LITERATURE": {"icon": "📖", "color": "#9C27B0"},
        "MATHEMATICS": {"icon": "🧮", "color": "#FF9800"},
        "SCIENCE": {"icon": "🔬", "color": "#4CAF50"},
        "SOCIAL STUDIES": {"icon": "🌍", "color": "#F44336"}
    }
    
    # Fetch assignments from each subject folder
    all_assignments = {}
    
    for subject in subjects_config.keys():
        folder_path = f"ASSIGNMENTS/{subject}"
        files = github_storage.get_files_in_folder(folder_path)
        if files:
            all_assignments[subject] = files
    
    if all_assignments:
        for subject, files in all_assignments.items():
            config = subjects_config.get(subject, {"icon": "📚", "color": "#667eea"})
            
            st.markdown(f"""
            <div class="subject-header">
                {config['icon']} <strong>{subject}</strong> ({len(files)} files)
            </div>
            """, unsafe_allow_html=True)
            
            for file in files:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    # File icon based on type
                    if file['type'] == 'pdf':
                        file_icon = "📄"
                    elif file['type'] == 'word':
                        file_icon = "📝"
                    elif file['type'] == 'image':
                        file_icon = "🖼️"
                    else:
                        file_icon = "📎"
                    
                    st.markdown(f"{file_icon} **{file['name']}**")
                    st.caption(f"Size: {file['size']} bytes")
                
                with col2:
                    # File type badge
                    st.markdown(f"`{file['type'].upper()}`")
                
                with col3:
                    # Download button
                    try:
                        file_content = requests.get(file['url']).content
                        st.download_button(
                            label="📥 Download",
                            data=file_content,
                            file_name=file['name'],
                            key=f"assign_{subject}_{file['name']}",
                            use_container_width=True
                        )
                    except:
                        st.error("Error loading file")
                
                st.markdown("---")
    else:
        st.info("📭 No assignments found. Check back later for updates!")

# ==================== TAB 2: REVISION PAPERS ====================
with tab2:
    st.header("📚 First Review Revision Papers")
    
    # Get files from FIRST REVIEW REVISION PAPERS folder
    revision_files = github_storage.get_files_in_folder("FIRST REVIEW REVISION PAPERS")
    
    if revision_files:
        st.markdown("### 📝 Practice Papers for First Review")
        
        for file in revision_files:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"📄 **{file['name']}**")
                if "syllabus" in file['name'].lower():
                    st.caption("📖 Term Syllabus Document")
                elif "test" in file['name'].lower() or "review" in file['name'].lower():
                    st.caption("📝 Revision Test Paper")
                else:
                    st.caption(f"Size: {file['size']} bytes")
            
            with col2:
                st.markdown("`REVISION`")
            
            with col3:
                try:
                    file_content = requests.get(file['url']).content
                    st.download_button(
                        label="📥 Download",
                        data=file_content,
                        file_name=file['name'],
                        key=f"revision_{file['name']}",
                        use_container_width=True
                    )
                except:
                    st.error("Error")
            
            st.markdown("---")
    else:
        st.info("📭 No revision papers available yet. Please check back later!")
    
    # Study tips for revision
    with st.expander("💡 Revision Tips"):
        st.markdown("""
        **📚 How to Make the Most of Revision Papers:**
        
        1. **Set a timer** - Practice completing papers within time limits
        2. **Create a quiet space** - Minimize distractions while studying
        3. **Review mistakes** - Learn from incorrect answers
        4. **Take breaks** - Study for 25-30 minutes, then take a 5-minute break
        5. **Ask for help** - Use Exam Buddy AI when you get stuck
        """)

# ==================== TAB 3: PROJECTS ====================
with tab3:
    st.header("🎯 Projects & Assignments")
    
    # Get files from PROJECT folder
    project_files = github_storage.get_files_in_folder("PROJECT")
    
    if project_files:
        st.markdown("### 🎨 Project Materials")
        
        for file in project_files:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                if "test" in file['name'].lower():
                    st.markdown(f"📝 **{file['name']}**")
                    st.caption("📋 Test Paper")
                elif "syllabus" in file['name'].lower():
                    st.markdown(f"📖 **{file['name']}**")
                    st.caption("📚 Syllabus Document")
                else:
                    st.markdown(f"📎 **{file['name']}**")
                    st.caption(f"Size: {file['size']} bytes")
            
            with col2:
                st.markdown("`PROJECT`")
            
            with col3:
                try:
                    file_content = requests.get(file['url']).content
                    st.download_button(
                        label="📥 Download",
                        data=file_content,
                        file_name=file['name'],
                        key=f"project_{file['name']}",
                        use_container_width=True
                    )
                except:
                    st.error("Error")
            
            st.markdown("---")
    else:
        st.info("📭 No projects uploaded yet!")

# ==================== QUICK STATS ====================
st.markdown("---")
st.subheader("📊 Resource Statistics")

# Calculate totals
total_assignments = sum(len(files) for files in all_assignments.values())
total_revision = len(revision_files) if revision_files else 0
total_projects = len(project_files) if project_files else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📝 Assignments", total_assignments)

with col2:
    st.metric("📚 Revision Papers", total_revision)

with col3:
    st.metric("🎯 Projects", total_projects)

with col4:
    total_resources = total_assignments + total_revision + total_projects
    st.metric("📦 Total Resources", total_resources)

# ==================== ANNOUNCEMENTS ====================
with st.expander("📢 Important Announcements"):
    st.info("""
    **📅 Upcoming Deadlines:**
    - First Review Tests: Check with your class teacher
    - Project Submissions: End of First Term
    
    **💡 Reminders:**
    - All assignments are available for download
    - Use Exam Buddy AI for homework help
    - Track your progress in the Progress section
    """)

# ==================== FEEDBACK SECTION ====================
st.markdown("---")
st.markdown("### 📝 Need Help?")

col1, col2 = st.columns(2)

with col1:
    if st.button("🤖 Ask Exam Buddy", use_container_width=True):
        st.switch_page("pages/04_🤖_Exam_Buddy.py")

with col2:
    if st.button("📧 Request Missing Materials", use_container_width=True):
        st.info("Please contact your class teacher for missing materials. Check the Parent Zone for contact information.")
