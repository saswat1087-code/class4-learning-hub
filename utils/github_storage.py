"""
GitHub Storage Helper - Corrected Version
"""

import streamlit as st
import requests
import urllib.parse
from typing import Dict, List

class GitHubStorage:
    def __init__(self):
        self.repo_owner = "saswat1087-code"
        self.repo_name = "class4-learning-hub"
        self.branch = "main"
        
        # Path to your content
        self.content_path = "data/CLASS 4 (2026-27)/FIRST TERM"
        self.encoded_path = urllib.parse.quote(self.content_path)
        
        # Raw URL base
        self.raw_base = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.branch}/{self.encoded_path}"
        
        self.cache = {}
        
        # Define your subjects and chapters
        self.subjects_list = [
            {
                "id": "computer",
                "name": "Computer Science",
                "folder_name": "COMPUTER",
                "icon": "💻",
                "color": "#4A90E2",
                "chapters": [
                    {"id": "chapter1", "title": "Chapter 1 - Storage and Memory Devices", "folder": "Chapter 1 - Storage and Memory Devices"},
                    {"id": "chapter2", "title": "Chapter 2 - GUI Operating System", "folder": "Chapter 2 - GUI Operating System"},
                    {"id": "chapter3", "title": "Chapter 3 - Internet and Email", "folder": "Chapter 3 - Internet and Email"},
                    {"id": "chapter4", "title": "Chapter 4 - MS Paint", "folder": "Chapter 4 - MS Paint"}
                ]
            },
            {
                "id": "science",
                "name": "Science",
                "folder_name": "SCIENCE",
                "icon": "🔬",
                "color": "#4CAF50",
                "chapters": [
                    {"id": "chapter1", "title": "Chapter 1 - Plants", "folder": "Chapter 1 - Plants"},
                    {"id": "chapter2", "title": "Chapter 2 - Animals", "folder": "Chapter 2 - Animals"},
                    {"id": "chapter3", "title": "Chapter 3 - Our Body", "folder": "Chapter 3 - Our Body"}
                ]
            },
            {
                "id": "mathematics",
                "name": "Mathematics",
                "folder_name": "MATHEMATICS",
                "icon": "🧮",
                "color": "#FF9800",
                "chapters": [
                    {"id": "chapter1", "title": "Chapter 1 - Large Numbers", "folder": "Chapter 1 - Large Numbers"},
                    {"id": "chapter2", "title": "Chapter 2 - Addition and Subtraction", "folder": "Chapter 2 - Addition and Subtraction"},
                    {"id": "chapter3", "title": "Chapter 3 - Multiplication", "folder": "Chapter 3 - Multiplication"}
                ]
            },
            {
                "id": "english-language",
                "name": "English Language",
                "folder_name": "ENGLISH LANGUAGE",
                "icon": "✍️",
                "color": "#9C27B0",
                "chapters": [
                    {"id": "chapter1", "title": "Chapter 1 - Nouns and Pronouns", "folder": "Chapter 1 - Nouns and Pronouns"},
                    {"id": "chapter2", "title": "Chapter 2 - Verbs and Tenses", "folder": "Chapter 2 - Verbs and Tenses"}
                ]
            },
            {
                "id": "english-literature",
                "name": "English Literature",
                "folder_name": "ENGLISH LITERATURE",
                "icon": "📖",
                "color": "#9C27B0",
                "chapters": [
                    {"id": "chapter1", "title": "Chapter 1 - The Magic Garden", "folder": "Chapter 1 - The Magic Garden"},
                    {"id": "chapter2", "title": "Chapter 2 - The Enchanted Castle", "folder": "Chapter 2 - The Enchanted Castle"}
                ]
            }
        ]
    
    def get_subjects(self) -> List[Dict]:
        """Get list of all subjects"""
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
        """Get chapters for a subject"""
        for subject in self.subjects_list:
            if subject['folder_name'] == subject_path:
                chapters = []
                for chapter in subject.get('chapters', []):
                    chapters.append({
                        'id': chapter['id'],
                        'title': chapter['title'],
                        'path': f"{subject_path}/{chapter['folder']}",
                        'folder': chapter['folder']
                    })
                return chapters
        return []
    
    def get_chapter_content(self, subject_path: str, chapter_path: str) -> Dict:
        """Get content.md from a chapter folder"""
        cache_key = f"chapter_{subject_path}_{chapter_path}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Build the URL - URL encode spaces
        encoded_subject = urllib.parse.quote(subject_path)
        encoded_chapter = urllib.parse.quote(chapter_path.split('/')[-1])
        
        content_url = f"{self.raw_base}/{encoded_subject}/{encoded_chapter}/content.md"
        
        try:
            response = requests.get(content_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                parsed = self.parse_markdown(content)
                # Set the title from the chapter
                if not parsed.get('title'):
                    parsed['title'] = chapter_path.split('/')[-1].replace('_', ' ').replace('-', ' ')
                self.cache[cache_key] = parsed
                return parsed
            else:
                return self.get_empty_chapter()
        except Exception as e:
            return self.get_empty_chapter()
    
    def get_files_in_folder(self, folder_path: str) -> List[Dict]:
        """Get files from folders (simplified)"""
        return []
    
    def get_all_assignments(self) -> Dict[str, List[Dict]]:
        """Get assignments"""
        return {}
    
    def get_revision_papers(self) -> List[Dict]:
        """Get revision papers"""
        return []
    
    def get_projects(self) -> List[Dict]:
        """Get projects"""
        return []
    
    def get_total_resources_count(self) -> Dict:
        """Get resource counts"""
        total_chapters = 0
        for subject in self.subjects_list:
            total_chapters += len(subject.get('chapters', []))
        
        return {
            'subjects': len(self.subjects_list),
            'chapters': total_chapters,
            'assignments': 0,
            'revision_papers': 0,
            'projects': 0
        }
    
    def get_file_type(self, filename: str) -> str:
        return 'unknown'
    
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
            # Title
            if line.startswith('# ') and not chapter_data['title']:
                chapter_data['title'] = line[2:].strip()
            
            # Content section
            elif line.startswith('## Content'):
                current_section = 'content'
                current_text = []
            
            # Key Points section
            elif line.startswith('## Key Points'):
                if current_section == 'content' and current_text:
                    chapter_data['content'] = '\n'.join(current_text).strip()
                current_section = 'key_points'
                current_text = []
            
            # Vocabulary section
            elif line.startswith('## Vocabulary'):
                if current_section == 'key_points' and current_text:
                    chapter_data['key_points'] = [p for p in current_text if p.strip()]
                current_section = 'vocabulary'
                current_text = []
            
            # Fun Fact section
            elif line.startswith('## Fun Fact'):
                if current_section == 'vocabulary' and current_text:
                    chapter_data['vocabulary'] = [v for v in current_text if v.strip()]
                current_section = 'fun_fact'
                current_text = []
            
            # Practice Questions section
            elif line.startswith('## Practice Questions'):
                if current_section == 'fun_fact' and current_text:
                    chapter_data['fun_fact'] = '\n'.join(current_text).strip()
                current_section = 'questions'
                current_text = []
            
            # Bullet points
            elif line.startswith('- ') or line.startswith('• ') or line.startswith('* '):
                if current_text is not None:
                    # Clean up the bullet point
                    bullet_text = line.lstrip('-•* ').strip()
                    if bullet_text:
                        current_text.append(bullet_text)
            
            # Regular text (not empty and not a header)
            elif line.strip() and not line.startswith('#'):
                if current_text is not None:
                    current_text.append(line.strip())
        
        # Handle last section
        if current_section == 'questions' and current_text:
            chapter_data['practice_questions'] = [q for q in current_text if q.strip()]
        
        # If content is still empty, use the raw text
        if not chapter_data['content'] and not chapter_data['key_points']:
            # Just use the first few paragraphs as content
            chapter_data['content'] = content[:500]
        
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
