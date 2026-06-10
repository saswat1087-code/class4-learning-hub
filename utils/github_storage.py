"""
GitHub Storage Helper - Updated for your folder structure
"""

import streamlit as st
import requests
import urllib.parse
from typing import Dict, List

class GitHubStorage:
    def __init__(self):
        # YOUR GITHUB USERNAME
        self.repo_owner = "saswat1087-code"
        self.repo_name = "class4-learning-hub"
        self.branch = "main"
        
        # Path to your content
        self.content_path = "data/CLASS 4 (2026-27)/FIRST TERM"
        self.encoded_path = urllib.parse.quote(self.content_path)
        
        # Base URLs
        self.raw_url = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.branch}/{self.encoded_path}"
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{self.encoded_path}"
        
        self.cache = {}
        
        # Subject configuration - MATCHING YOUR ACTUAL FOLDER NAMES
        self.subjects_config = {
            "COMPUTER": {"icon": "💻", "color": "#4A90E2", "id": "computer", "display_name": "Computer Science"},
            "ENGLISH LANGUAGE": {"icon": "✍️", "color": "#9C27B0", "id": "english-language", "display_name": "English Language"},
            "ENGLISH LITERATURE": {"icon": "📖", "color": "#9C27B0", "id": "english-literature", "display_name": "English Literature"},
            "MATHEMATICS": {"icon": "🧮", "color": "#FF9800", "id": "mathematics", "display_name": "Mathematics"},
            "SCIENCE": {"icon": "🔬", "color": "#4CAF50", "id": "science", "display_name": "Science"}
        }
    
    def get_subjects(self) -> List[Dict]:
        """Get list of all subjects from the FIRST TERM folder"""
        try:
            response = requests.get(self.api_url)
            
            if response.status_code == 200:
                items = response.json()
                subjects = []
                for item in items:
                    if item['type'] == 'dir' and item['name'] in self.subjects_config:
                        config = self.subjects_config[item['name']]
                        subjects.append({
                            'id': config['id'],
                            'name': config['display_name'],  # Use display name for UI
                            'folder_name': item['name'],     # Keep original folder name
                            'icon': config['icon'],
                            'color': config['color'],
                            'path': item['name']
                        })
                return subjects
            else:
                st.error(f"Failed to load subjects. Status: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error loading subjects: {str(e)}")
            return []
    
    def get_chapters(self, subject_path: str) -> List[Dict]:
        """Get chapters for a subject (looks for folders inside subject)"""
        try:
            subject_api_url = f"{self.api_url}/{subject_path}"
            response = requests.get(subject_api_url)
            
            if response.status_code == 200:
                items = response.json()
                chapters = []
                for item in items:
                    if item['type'] == 'dir':
                        chapters.append({
                            'id': item['name'],
                            'title': item['name'].replace('_', ' ').replace('-', ' ').title(),
                            'path': f"{subject_path}/{item['name']}",
                            'folder': item['name']
                        })
                return chapters
            return []
        except Exception as e:
            return []
    
    def get_chapter_content(self, subject_path: str, chapter_path: str) -> Dict:
        """Get content.md from a chapter folder"""
        try:
            content_url = f"{self.raw_url}/{subject_path}/{chapter_path}/content.md"
            response = requests.get(content_url)
            
            if response.status_code == 200:
                content = response.text
                return self.parse_markdown(content)
            return self.get_empty_chapter()
        except Exception as e:
            return self.get_empty_chapter()
    
    def get_files_in_folder(self, folder_path: str) -> List[Dict]:
        """Get all files in a specific folder"""
        files = []
        try:
            folder_api_url = f"{self.api_url}/{folder_path}"
            response = requests.get(folder_api_url)
            
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    if item['type'] == 'file':
                        files.append({
                            'name': item['name'],
                            'url': f"{self.raw_url}/{folder_path}/{item['name']}",
                            'size': item.get('size', 0),
                            'type': self.get_file_type(item['name'])
                        })
            return files
        except:
            return []
    
    def get_all_assignments(self) -> Dict[str, List[Dict]]:
        """Get all assignments grouped by subject"""
        all_assignments = {}
        try:
            assignments_url = f"{self.api_url}/ASSIGNMENTS"
            response = requests.get(assignments_url)
            
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    if item['type'] == 'dir':
                        subject_assignments = self.get_files_in_folder(f"ASSIGNMENTS/{item['name']}")
                        if subject_assignments:
                            all_assignments[item['name']] = subject_assignments
            return all_assignments
        except:
            return {}
    
    def get_revision_papers(self) -> List[Dict]:
        """Get revision papers from FIRST REVIEW REVISION PAPERS folder"""
        try:
            return self.get_files_in_folder("FIRST REVIEW REVISION PAPERS")
        except:
            return []
    
    def get_projects(self) -> List[Dict]:
        """Get projects from PROJECT folder"""
        try:
            return self.get_files_in_folder("PROJECT")
        except:
            return []
    
    def get_total_resources_count(self) -> Dict:
        """Get resource counts"""
        subjects = self.get_subjects()
        total_chapters = 0
        for subject in subjects:
            chapters = self.get_chapters(subject['path'])
            total_chapters += len(chapters)
        
        return {
            'subjects': len(subjects),
            'chapters': total_chapters,
            'assignments': sum(len(v) for v in self.get_all_assignments().values()),
            'revision_papers': len(self.get_revision_papers()),
            'projects': len(self.get_projects())
        }
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from extension"""
        ext = filename.split('.')[-1].lower()
        types = {
            'pdf': 'pdf', 'doc': 'word', 'docx': 'word',
            'jpg': 'image', 'png': 'image', 'gif': 'image',
            'txt': 'text', 'md': 'markdown', 'pptx': 'powerpoint',
            'xlsx': 'excel'
        }
        return types.get(ext, 'unknown')
    
    def parse_markdown(self, content: str) -> Dict:
        """Parse markdown content into structured format"""
        lines = content.split('\n')
        
        chapter_data = {
            'title': '',
            'content': '',
            'key_points': [],
            'vocabulary': [],
            'fun_fact': '',
            'practice_questions': []
        }
        
        current_section = None
        current_text = []
        
        for line in lines:
            if line.startswith('# ') and not chapter_data['title']:
                chapter_data['title'] = line[2:].strip()
            elif line.startswith('## Content'):
                current_section = 'content'
                current_text = []
            elif line.startswith('## Key Points'):
                if current_section == 'content':
                    chapter_data['content'] = '\n'.join(current_text).strip()
                current_section = 'key_points'
                current_text = []
            elif line.startswith('## Vocabulary'):
                if current_section == 'key_points':
                    chapter_data['key_points'] = [p for p in current_text if p.strip()]
                current_section = 'vocabulary'
                current_text = []
            elif line.startswith('## Fun Fact'):
                if current_section == 'vocabulary':
                    chapter_data['vocabulary'] = [v for v in current_text if v.strip()]
                current_section = 'fun_fact'
                current_text = []
            elif line.startswith('## Practice Questions'):
                if current_section == 'fun_fact':
                    chapter_data['fun_fact'] = '\n'.join(current_text).strip()
                current_section = 'questions'
                current_text = []
            elif line.startswith('- ') or line.startswith('• '):
                if current_text is not None:
                    current_text.append(line[2:].strip())
            elif line.strip() and not line.startswith('#'):
                if current_text is not None:
                    current_text.append(line.strip())
        
        if current_section == 'questions' and current_text:
            chapter_data['practice_questions'] = [q for q in current_text if q.strip()]
        
        return chapter_data
    
    def get_empty_chapter(self) -> Dict:
        return {
            'title': 'Content Coming Soon',
            'content': '📚 This chapter content is being prepared. Check back later!',
            'key_points': ['✨ Exciting content coming soon!'],
            'vocabulary': ['📖 New words will appear here'],
            'fun_fact': '🌟 Learning is an adventure!',
            'practice_questions': ['💭 What do you hope to learn in this chapter?']
        }
    
    def clear_cache(self):
        self.cache = {}

# Create instance
@st.cache_resource
def get_github_storage():
    return GitHubStorage()

github_storage = get_github_storage()
