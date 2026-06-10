"""
GitHub Storage Helper - Using Raw URLs (No API Rate Limits)
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
        
        # Use RAW URL for direct file access (no API rate limits!)
        self.raw_base = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.branch}/{self.encoded_path}"
        
        self.cache = {}
        
        # Subject configuration - MATCHING YOUR ACTUAL FOLDER NAMES
        self.subjects_config = {
            "COMPUTER": {"icon": "💻", "color": "#4A90E2", "id": "computer", "display_name": "Computer Science"},
            "ENGLISH LANGUAGE": {"icon": "✍️", "color": "#9C27B0", "id": "english-language", "display_name": "English Language"},
            "ENGLISH LITERATURE": {"icon": "📖", "color": "#9C27B0", "id": "english-literature", "display_name": "English Literature"},
            "MATHEMATICS": {"icon": "🧮", "color": "#FF9800", "id": "mathematics", "display_name": "Mathematics"},
            "SCIENCE": {"icon": "🔬", "color": "#4CAF50", "id": "science", "display_name": "Science"}
        }
        
        # Store subject list directly (no API call needed)
        self.subjects_list = [
            {"id": "computer", "name": "Computer Science", "folder_name": "COMPUTER", "icon": "💻", "color": "#4A90E2"},
            {"id": "english-language", "name": "English Language", "folder_name": "ENGLISH LANGUAGE", "icon": "✍️", "color": "#9C27B0"},
            {"id": "english-literature", "name": "English Literature", "folder_name": "ENGLISH LITERATURE", "icon": "📖", "color": "#9C27B0"},
            {"id": "mathematics", "name": "Mathematics", "folder_name": "MATHEMATICS", "icon": "🧮", "color": "#FF9800"},
            {"id": "science", "name": "Science", "folder_name": "SCIENCE", "icon": "🔬", "color": "#4CAF50"}
        ]
    
    def get_subjects(self) -> List[Dict]:
        """Get list of all subjects - using pre-defined list"""
        subjects = []
        for subject in self.subjects_list:
            subjects.append({
                'id': subject['id'],
                'name': subject['name'],
                'folder_name': subject['folder_name'],
                'icon': subject['icon'],
                'color': subject['color'],
                'path': subject['folder_name']
            })
        return subjects
    
    def get_chapters(self, subject_path: str) -> List[Dict]:
        """
        Get chapters for a subject by checking for content.md files
        Since we can't list directories without API, we'll use known chapter names
        or you can add them manually
        """
        # For now, return empty list - you can add chapters manually
        # OR we can try a different approach
        chapters = []
        
        # Try to get a known chapter file
        test_url = f"{self.raw_base}/{subject_path}/Chapter 1/content.md"
        response = requests.get(test_url)
        if response.status_code == 200:
            chapters.append({
                'id': 'Chapter 1',
                'title': 'Chapter 1',
                'path': f"{subject_path}/Chapter 1",
                'folder': 'Chapter 1'
            })
        
        return chapters
    
    def get_chapter_content(self, subject_path: str, chapter_path: str) -> Dict:
        """Get content.md from a chapter folder using raw URL"""
        try:
            content_url = f"{self.raw_base}/{subject_path}/{chapter_path}/content.md"
            response = requests.get(content_url)
            
            if response.status_code == 200:
                content = response.text
                return self.parse_markdown(content)
            return self.get_empty_chapter()
        except Exception as e:
            return self.get_empty_chapter()
    
    def get_files_in_folder(self, folder_path: str) -> List[Dict]:
        """Get files by checking common file patterns"""
        files = []
        
        # Common file patterns to check
        file_patterns = [
            f"{folder_path}/Class 4 1st Review Test .pdf",
            f"{folder_path}/Class 4 First Term Syllabus (2026-27)-2.pdf"
        ]
        
        for file_path in file_patterns:
            try:
                test_url = f"{self.raw_base}/{file_path}"
                response = requests.head(test_url)
                if response.status_code == 200:
                    files.append({
                        'name': file_path.split('/')[-1],
                        'url': test_url,
                        'type': 'pdf'
                    })
            except:
                pass
        
        return files
    
    def get_all_assignments(self) -> Dict[str, List[Dict]]:
        """Get assignments - simplified version"""
        return {}
    
    def get_revision_papers(self) -> List[Dict]:
        """Get revision papers"""
        papers = []
        try:
            # Check for known files
            known_files = [
                "FIRST REVIEW REVISION PAPERS/Class 4 1st Review Test .pdf",
                "FIRST REVIEW REVISION PAPERS/Class 4 First Term Syllabus (2026-27)-2.pdf"
            ]
            
            for file_path in known_files:
                test_url = f"{self.raw_base}/{file_path}"
                response = requests.head(test_url)
                if response.status_code == 200:
                    papers.append({
                        'name': file_path.split('/')[-1],
                        'url': test_url,
                        'type': 'pdf'
                    })
        except:
            pass
        
        return papers
    
    def get_projects(self) -> List[Dict]:
        """Get projects"""
        projects = []
        try:
            known_files = [
                "PROJECT/Class 4 1st Review Test .pdf",
                "PROJECT/Class 4 First Term Syllabus (2026-27)-2.pdf"
            ]
            
            for file_path in known_files:
                test_url = f"{self.raw_base}/{file_path}"
                response = requests.head(test_url)
                if response.status_code == 200:
                    projects.append({
                        'name': file_path.split('/')[-1],
                        'url': test_url,
                        'type': 'pdf'
                    })
        except:
            pass
        
        return projects
    
    def get_total_resources_count(self) -> Dict:
        """Get resource counts"""
        return {
            'subjects': len(self.get_subjects()),
            'chapters': 0,
            'assignments': 0,
            'revision_papers': len(self.get_revision_papers()),
            'projects': len(self.get_projects())
        }
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from extension"""
        ext = filename.split('.')[-1].lower()
        types = {
            'pdf': 'pdf', 'doc': 'word', 'docx': 'word',
            'jpg': 'image', 'png': 'image', 'gif': 'image',
            'txt': 'text', 'md': 'markdown'
        }
        return types.get(ext, 'unknown')
    
    def parse_markdown(self, content: str) -> Dict:
        """Parse markdown content"""
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
            'practice_questions': ['💭 What do you hope to learn?']
        }
    
    def clear_cache(self):
        self.cache = {}

# Create instance
@st.cache_resource
def get_github_storage():
    return GitHubStorage()

github_storage = get_github_storage()
