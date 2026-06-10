"""
GitHub Storage Helper - Complete Resource Manager for Class 4 Learning Hub
Handles syllabus content, assignments, revision papers, projects, and all resources
"""

import streamlit as st
import requests
import json
import re
import urllib.parse
from typing import Dict, List, Optional, Any
from datetime import datetime

class GitHubStorage:
    def __init__(self):
        # Your GitHub info - UPDATE THESE!
        self.repo_owner = "saswat1087-code"  # Your GitHub username
        self.repo_name = "class4-learning-hub"
        self.branch = "main"
        
        # Path to your content (URL encoded for spaces)
        self.content_path = "data/CLASS 4 (2026-27)/FIRST TERM"
        self.encoded_path = urllib.parse.quote(self.content_path)
        
        # Base URLs for GitHub raw content and API
        self.raw_url = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.branch}/{self.encoded_path}"
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{self.encoded_path}"
        
        # Cache for loaded data to improve performance
        self.cache = {}
        
        # Subject configuration with icons and colors
        self.subjects_config = {
            "Computer Science": {"icon": "💻", "color": "#4A90E2", "id": "computer-science", "folder": "Computer Science"},
            "English": {"icon": "📖", "color": "#9C27B0", "id": "english", "folder": "English"},
            "English Literature": {"icon": "📚", "color": "#9C27B0", "id": "english-literature", "folder": "ENGLISH LITERATURE"},
            "English Language": {"icon": "✍️", "color": "#9C27B0", "id": "english-language", "folder": "ENGLISH LANGUAGE"},
            "Mathematics": {"icon": "🧮", "color": "#FF9800", "id": "mathematics", "folder": "MATHEMATICS"},
            "Science": {"icon": "🔬", "color": "#4CAF50", "id": "science", "folder": "SCIENCE"},
            "2ND LANGUAGE BENGALI": {"icon": "🇧🇩", "color": "#FF5722", "id": "bengali", "folder": "2ND LANGUAGE BENGALI"},
            "2ND LANGUAGE HINDI": {"icon": "🇮🇳", "color": "#FF5722", "id": "hindi", "folder": "2ND LANGUAGE HINDI"},
            "COMPUTER": {"icon": "💻", "color": "#4A90E2", "id": "computer", "folder": "COMPUTER"},
            "SOCIAL STUDIES": {"icon": "🌍", "color": "#F44336", "id": "social-studies", "folder": "SOCIAL STUDIES"}
        }
    
    # ==================== SYLLABUS CONTENT METHODS ====================
    
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
                            'id': config.get('id', item['name'].lower().replace(' ', '-')),
                            'name': item['name'],
                            'icon': config['icon'],
                            'color': config['color'],
                            'path': item['name']
                        })
                return subjects
            else:
                st.warning(f"Could not load subjects. Status: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error loading subjects: {str(e)}")
            return []
    
    def get_chapters(self, subject_path: str) -> List[Dict]:
        """Get all chapters for a subject"""
        try:
            subject_api_url = f"{self.api_url}/{subject_path}"
            response = requests.get(subject_api_url)
            if response.status_code == 200:
                items = response.json()
                chapters = []
                for item in items:
                    if item['type'] == 'dir':
                        # Clean up chapter name for display
                        title = item['name'].replace('_', ' ').replace('-', ' ')
                        # Remove leading numbers like "01 - " or "Chapter 1 - "
                        title = re.sub(r'^\d+\s*[-–]\s*', '', title)
                        title = re.sub(r'^Chapter\s+\d+\s*[-–]\s*', '', title, flags=re.IGNORECASE)
                        
                        chapters.append({
                            'id': item['name'],
                            'title': title.title(),
                            'path': f"{subject_path}/{item['name']}",
                            'folder': item['name']
                        })
                return chapters
            return []
        except Exception as e:
            st.error(f"Error loading chapters for {subject_path}: {str(e)}")
            return []
    
    def get_chapter_content(self, subject_path: str, chapter_path: str) -> Dict:
        """Get content.md from a chapter folder"""
        cache_key = f"chapter_{subject_path}_{chapter_path}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            content_url = f"{self.raw_url}/{subject_path}/{chapter_path}/content.md"
            response = requests.get(content_url)
            
            if response.status_code == 200:
                content = response.text
                parsed = self.parse_markdown(content)
                
                # Also try to load additional resources
                parsed['images'] = self.get_chapter_images(subject_path, chapter_path)
                parsed['worksheets'] = self.get_chapter_worksheets(subject_path, chapter_path)
                
                self.cache[cache_key] = parsed
                return parsed
            
            return self.get_empty_chapter()
        except Exception as e:
            return self.get_empty_chapter()
    
    def get_chapter_images(self, subject_path: str, chapter_path: str) -> List[Dict]:
        """Get images for a specific chapter"""
        images = []
        try:
            images_url = f"{self.api_url}/{subject_path}/{chapter_path}/images"
            response = requests.get(images_url)
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    if item['type'] == 'file' and item['name'].endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        images.append({
                            'name': item['name'],
                            'url': f"{self.raw_url}/{subject_path}/{chapter_path}/images/{item['name']}"
                        })
        except:
            pass
        return images
    
    def get_chapter_worksheets(self, subject_path: str, chapter_path: str) -> List[Dict]:
        """Get worksheets for a specific chapter"""
        worksheets = []
        try:
            worksheets_url = f"{self.api_url}/{subject_path}/{chapter_path}/worksheets"
            response = requests.get(worksheets_url)
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    if item['type'] == 'file':
                        worksheets.append({
                            'name': item['name'],
                            'url': f"{self.raw_url}/{subject_path}/{chapter_path}/worksheets/{item['name']}"
                        })
        except:
            pass
        return worksheets
    
    # ==================== ASSIGNMENTS METHODS ====================
    
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
                        subject_name = item['name']
                        subject_assignments = self.get_files_in_folder(f"ASSIGNMENTS/{subject_name}")
                        if subject_assignments:
                            all_assignments[subject_name] = subject_assignments
            
            return all_assignments
        except Exception as e:
            st.error(f"Error loading assignments: {e}")
            return {}
    
    def get_assignments_by_subject(self, subject_name: str) -> List[Dict]:
        """Get assignments for a specific subject"""
        try:
            folder_path = f"ASSIGNMENTS/{subject_name}"
            return self.get_files_in_folder(folder_path)
        except:
            return []
    
    # ==================== REVISION PAPERS METHODS ====================
    
    def get_revision_papers(self) -> List[Dict]:
        """Get all revision papers from FIRST REVIEW REVISION PAPERS folder"""
        try:
            return self.get_files_in_folder("FIRST REVIEW REVISION PAPERS")
        except:
            return []
    
    def get_revision_papers_by_type(self, paper_type: str = None) -> List[Dict]:
        """Get revision papers filtered by type (syllabus, test, review)"""
        papers = self.get_revision_papers()
        
        if paper_type:
            filtered = []
            for paper in papers:
                if paper_type.lower() in paper['name'].lower():
                    filtered.append(paper)
            return filtered
        return papers
    
    # ==================== PROJECTS METHODS ====================
    
    def get_projects(self) -> List[Dict]:
        """Get all project files from PROJECT folder"""
        try:
            return self.get_files_in_folder("PROJECT")
        except:
            return []
    
    def get_projects_by_type(self, project_type: str = None) -> List[Dict]:
        """Get projects filtered by type"""
        projects = self.get_projects()
        
        if project_type:
            filtered = []
            for project in projects:
                if project_type.lower() in project['name'].lower():
                    filtered.append(project)
            return filtered
        return projects
    
    # ==================== UTILITY METHODS ====================
    
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
                            'type': self.get_file_type(item['name']),
                            'download_url': item.get('download_url', '')
                        })
            return files
        except Exception as e:
            return []
    
    def get_file_content(self, file_path: str) -> Any:
        """Get content of a specific file"""
        cache_key = f"file_{file_path}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            url = f"{self.raw_url}/{file_path}"
            response = requests.get(url)
            response.raise_for_status()
            
            # Handle different file types
            if file_path.endswith('.json'):
                content = response.json()
            elif file_path.endswith(('.md', '.txt')):
                content = response.text
            elif file_path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                content = response.content
            elif file_path.endswith('.pdf'):
                content = response.content
            else:
                content = response.text
            
            self.cache[cache_key] = content
            return content
        except Exception as e:
            st.error(f"Error loading {file_path}: {str(e)}")
            return None
    
    def get_file_type(self, filename: str) -> str:
        """Determine file type from extension"""
        ext = filename.split('.')[-1].lower()
        file_types = {
            'pdf': 'pdf',
            'doc': 'word',
            'docx': 'word',
            'ppt': 'powerpoint',
            'pptx': 'powerpoint',
            'xls': 'excel',
            'xlsx': 'excel',
            'jpg': 'image',
            'jpeg': 'image',
            'png': 'image',
            'gif': 'image',
            'webp': 'image',
            'txt': 'text',
            'md': 'markdown',
            'csv': 'csv',
            'zip': 'archive'
        }
        return file_types.get(ext, 'unknown')
    
    def parse_markdown(self, content: str) -> Dict:
        """Parse markdown content into structured format"""
        lines = content.split('\n')
        
        chapter_data = {
            'title': '',
            'content': '',
            'key_points': [],
            'vocabulary': [],
            'fun_fact': '',
            'practice_questions': [],
            'images': [],
            'worksheets': []
        }
        
        current_section = None
        current_text = []
        
        for line in lines:
            # Title (first # heading)
            if line.startswith('# ') and not chapter_data['title']:
                chapter_data['title'] = line[2:].strip()
            
            # Content section
            elif line.startswith('## Content'):
                if current_section == 'key_points':
                    chapter_data['key_points'] = [p for p in current_text if p.strip()]
                current_section = 'content'
                current_text = []
            
            # Key Points section
            elif line.startswith('## Key Points'):
                if current_section == 'content':
                    chapter_data['content'] = '\n'.join(current_text).strip()
                current_section = 'key_points'
                current_text = []
            
            # Vocabulary section
            elif line.startswith('## Vocabulary'):
                if current_section == 'key_points':
                    chapter_data['key_points'] = [p for p in current_text if p.strip()]
                current_section = 'vocabulary'
                current_text = []
            
            # Fun Fact section
            elif line.startswith('## Fun Fact'):
                if current_section == 'vocabulary':
                    chapter_data['vocabulary'] = [v for v in current_text if v.strip()]
                current_section = 'fun_fact'
                current_text = []
            
            # Practice Questions section
            elif line.startswith('## Practice Questions'):
                if current_section == 'fun_fact':
                    chapter_data['fun_fact'] = '\n'.join(current_text).strip()
                current_section = 'questions'
                current_text = []
            
            # Bullet points (for key points and vocabulary)
            elif line.startswith('- ') or line.startswith('• ') or line.startswith('* '):
                if current_text is not None:
                    current_text.append(line[2:].strip())
            
            # Regular text
            elif line.strip() and not line.startswith('#'):
                if current_text is not None:
                    current_text.append(line.strip())
        
        # Handle last section
        if current_section == 'questions' and current_text:
            chapter_data['practice_questions'] = [q for q in current_text if q.strip()]
        
        return chapter_data
    
    def get_empty_chapter(self) -> Dict:
        """Return empty chapter structure for content not yet available"""
        return {
            'title': 'Content Coming Soon',
            'content': '📚 This chapter content is being prepared. Check back later for exciting lessons!',
            'key_points': ['✨ Exciting content coming soon!'],
            'vocabulary': ['📖 New words will appear here'],
            'fun_fact': '🌟 Learning is an adventure - every day brings something new!',
            'practice_questions': ['💭 What do you hope to learn in this chapter?'],
            'images': [],
            'worksheets': []
        }
    
    def get_total_resources_count(self) -> Dict:
        """Get count of all resources for dashboard display"""
        counts = {
            'assignments': 0,
            'revision_papers': 0,
            'projects': 0,
            'subjects': 0,
            'chapters': 0
        }
        
        # Count assignments
        all_assignments = self.get_all_assignments()
        for subject, files in all_assignments.items():
            counts['assignments'] += len(files)
        
        # Count revision papers
        counts['revision_papers'] = len(self.get_revision_papers())
        
        # Count projects
        counts['projects'] = len(self.get_projects())
        
        # Count subjects and chapters
        subjects = self.get_subjects()
        counts['subjects'] = len(subjects)
        
        for subject in subjects:
            chapters = self.get_chapters(subject['path'])
            counts['chapters'] += len(chapters)
        
        return counts
    
    def get_download_url(self, file_path: str) -> str:
        """Get direct download URL for a file"""
        return f"{self.raw_url}/{file_path}"
    
    def search_resources(self, query: str) -> List[Dict]:
        """Search for resources by keyword"""
        results = []
        query_lower = query.lower()
        
        # Search in assignments
        all_assignments = self.get_all_assignments()
        for subject, files in all_assignments.items():
            for file in files:
                if query_lower in file['name'].lower() or query_lower in subject.lower():
                    file['category'] = 'assignment'
                    file['subject'] = subject
                    results.append(file)
        
        # Search in revision papers
        for paper in self.get_revision_papers():
            if query_lower in paper['name'].lower():
                paper['category'] = 'revision'
                results.append(paper)
        
        # Search in projects
        for project in self.get_projects():
            if query_lower in project['name'].lower():
                project['category'] = 'project'
                results.append(project)
        
        return results
    
    def clear_cache(self):
        """Clear the entire cache"""
        self.cache = {}
        st.success("Cache cleared successfully!")

# Create singleton instance
@st.cache_resource
def get_github_storage():
    """Get or create the GitHub storage instance"""
    return GitHubStorage()

# Create global instance for easy importing
github_storage = get_github_storage()
