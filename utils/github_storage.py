"""
GitHub Storage Helper - Working Version with Debug
"""

import streamlit as st
import requests
import re
from typing import Dict, List

class GitHubStorage:
    def __init__(self):
        # Define subjects and chapters with DIRECT URLs
        # IMPORTANT: The chapter titles here MUST MATCH your folder names EXACTLY
        self.subjects_data = {
            "COMPUTER": {
                "display_name": "Computer Science",
                "icon": "💻",
                "color": "#4A90E2",
                "chapters": {
                    "Chapter 1 - Storage and Memory Devices": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%201%20-%20Storage%20and%20Memory%20Devices/content.md"
                    },
                    "Chapter 2 - GUI Operating System": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%202%20-%20GUI%20Operating%20System/content.md"
                    }
                }
            },
            "SCIENCE": {
                "display_name": "Science",
                "icon": "🔬",
                "color": "#4CAF50",
                "chapters": {}
            },
            "MATHEMATICS": {
                "display_name": "Mathematics",
                "icon": "🧮",
                "color": "#FF9800",
                "chapters": {}
            },
            "ENGLISH LANGUAGE": {
                "display_name": "English Language",
                "icon": "✍️",
                "color": "#9C27B0",
                "chapters": {}
            },
            "ENGLISH LITERATURE": {
                "display_name": "English Literature",
                "icon": "📖",
                "color": "#9C27B0",
                "chapters": {}
            }
        }
        
        self.cache = {}
    
    def get_subjects(self) -> List[Dict]:
        """Get list of all subjects"""
        subjects = []
        for folder_name, data in self.subjects_data.items():
            subjects.append({
                'id': folder_name.lower().replace(' ', '-'),
                'name': data['display_name'],
                'folder_name': folder_name,
                'icon': data['icon'],
                'color': data['color'],
                'path': folder_name
            })
        return subjects
    
    def get_chapters(self, subject_path: str) -> List[Dict]:
        """Get chapters for a subject"""
        if subject_path in self.subjects_data:
            chapters = []
            for chapter_title in self.subjects_data[subject_path]['chapters'].keys():
                chapters.append({
                    'id': chapter_title,
                    'title': chapter_title,
                    'path': f"{subject_path}/{chapter_title}",
                    'folder': chapter_title
                })
            return chapters
        return []
    
    def get_chapter_content(self, subject_path: str, chapter_path: str) -> Dict:
        """Get chapter content directly from URL"""
        # Create a unique cache key
        cache_key = f"{subject_path}_{chapter_path}"
        
        # Check cache
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Extract chapter title from chapter_path (remove subject path)
        chapter_title = chapter_path.split('/')[-1] if '/' in chapter_path else chapter_path
        
        # Get the URL
        if subject_path in self.subjects_data:
            chapter_data = self.subjects_data[subject_path]['chapters'].get(chapter_title)
            
            if chapter_data and 'url' in chapter_data:
                url = chapter_data['url']
                
                try:
                    response = requests.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        content = response.text
                        parsed = self.parse_markdown(content, chapter_title)
                        self.cache[cache_key] = parsed
                        return parsed
                    else:
                        return self.get_empty_chapter(chapter_title, f"HTTP {response.status_code}")
                except Exception as e:
                    return self.get_empty_chapter(chapter_title, str(e))
        
        return self.get_empty_chapter(chapter_title, "No URL found")
    
    def get_files_in_folder(self, folder_path: str) -> List[Dict]:
        return []
    
    def get_all_assignments(self) -> Dict[str, List[Dict]]:
        return {}
    
    def get_revision_papers(self) -> List[Dict]:
        return []
    
    def get_projects(self) -> List[Dict]:
        return []
    
    def get_total_resources_count(self) -> Dict:
        total_chapters = 0
        for subject in self.subjects_data.values():
            total_chapters += len(subject.get('chapters', {}))
        
        return {
            'subjects': len(self.subjects_data),
            'chapters': total_chapters,
            'assignments': 0,
            'revision_papers': 0,
            'projects': 0
        }
    
    def parse_markdown(self, content: str, title: str = "") -> Dict:
        """Parse markdown content into structured format"""
        chapter_data = {
            'title': title,
            'content': '',
            'key_points': [],
            'vocabulary': [],
            'fun_fact': '',
            'practice_questions': []
        }
        
        # Try to extract using regex for better reliability
        # Extract title from # heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            chapter_data['title'] = title_match.group(1).strip()
        
        # Extract content section
        content_match = re.search(r'## Content\s+(.*?)(?=##|$)', content, re.DOTALL)
        if content_match:
            chapter_data['content'] = content_match.group(1).strip()
        
        # Extract key points
        points_match = re.search(r'## Key Points\s+(.*?)(?=##|$)', content, re.DOTALL)
        if points_match:
            points_text = points_match.group(1)
            points = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', points_text, re.DOTALL)
            if points:
                chapter_data['key_points'] = [p.strip() for p in points]
            else:
                # Fallback: split by lines
                chapter_data['key_points'] = [line.strip() for line in points_text.split('\n') if line.strip() and not line.startswith('#')]
        
        # Extract vocabulary
        vocab_match = re.search(r'## Vocabulary\s+(.*?)(?=##|$)', content, re.DOTALL)
        if vocab_match:
            vocab_text = vocab_match.group(1)
            # Look for bolded words or bullet points
            vocab_items = re.findall(r'\*\*(.*?)\*\*', vocab_text)
            if not vocab_items:
                vocab_items = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', vocab_text, re.DOTALL)
            chapter_data['vocabulary'] = [v.strip() for v in vocab_items][:10]
        
        # Extract fun fact
        fun_match = re.search(r'## Fun Fact\s+(.*?)(?=##|$)', content, re.DOTALL)
        if fun_match:
            chapter_data['fun_fact'] = fun_match.group(1).strip()
        
        # Extract practice questions
        questions_match = re.search(r'## Practice Questions\s+(.*?)(?=##|$)', content, re.DOTALL)
        if questions_match:
            questions_text = questions_match.group(1)
            questions = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', questions_text, re.DOTALL)
            if questions:
                chapter_data['practice_questions'] = [q.strip() for q in questions]
            else:
                chapter_data['practice_questions'] = [q.strip() for q in questions_text.split('\n') if q.strip() and not q.startswith('#')]
        
        # Fallback: if no structured content found, use raw content
        if not chapter_data['content'] and not chapter_data['key_points']:
            # Get first 500 characters as content
            chapter_data['content'] = content[:500] + ("..." if len(content) > 500 else "")
        
        return chapter_data
    
    def get_empty_chapter(self, title: str = "", error: str = "") -> Dict:
        """Return empty chapter structure"""
        return {
            'title': title if title else 'Content Coming Soon',
            'content': f'📚 This chapter content is being prepared. Check back later! {error}',
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
