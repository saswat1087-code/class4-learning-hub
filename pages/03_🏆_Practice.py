"""
GitHub Storage Helper - Auto-Discover Files (No API Required)
Uses GitHub API with proper authentication to list files
"""

import streamlit as st
import requests
import re
import urllib.parse
from typing import Dict, List

class GitHubStorage:
    def __init__(self):
        self.repo_owner = "saswat1087-code"
        self.repo_name = "class4-learning-hub"
        self.branch = "main"
        
        self.content_path = "data/CLASS 4 (2026-27)/FIRST TERM"
        self.encoded_path = urllib.parse.quote(self.content_path)
        
        self.raw_base = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.branch}/{self.encoded_path}"
        
        # GitHub API with authentication (using token if available)
        self.api_base = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{self.encoded_path}"
        
        self.cache = {}
        self.file_cache = {}
        
        # Try to get GitHub token from secrets
        self.github_token = None
        try:
            self.github_token = st.secrets.get("GITHUB_TOKEN", None)
        except:
            pass
    
    def _get_headers(self):
        """Get headers for GitHub API requests"""
        headers = {
            'User-Agent': 'Class4LearningHub/2.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.github_token:
            headers['Authorization'] = f'token {self.github_token}'
        return headers
    
    def get_files_in_folder(self, folder_path: str) -> List[Dict]:
        """Automatically discover all files in a folder using GitHub API"""
        
        # Check cache first
        if folder_path in self.file_cache:
            return self.file_cache[folder_path]
        
        files = []
        
        # Build the API URL for the folder
        encoded_folder = urllib.parse.quote(folder_path)
        api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{self.encoded_path}/{encoded_folder}"
        
        try:
            response = requests.get(api_url, headers=self._get_headers(), timeout=15)
            
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    if item['type'] == 'file':
                        filename = item['name']
                        # Only include PDF files
                        if filename.lower().endswith('.pdf'):
                            files.append({
                                'name': filename,
                                'url': item['download_url'],
                                'size': item.get('size', 0),
                                'type': 'pdf'
                            })
                    elif item['type'] == 'dir':
                        # Recursively get files from subdirectories if needed
                        sub_files = self.get_files_in_folder(f"{folder_path}/{item['name']}")
                        files.extend(sub_files)
                
                # Cache the results
                self.file_cache[folder_path] = files
                return files
                
            elif response.status_code == 403:
                # Rate limit or permission issue - use fallback
                st.warning(f"GitHub API rate limit. Using fallback for {folder_path}")
                return self._get_fallback_files(folder_path)
                
            elif response.status_code == 404:
                # Folder doesn't exist
                return []
                
        except Exception as e:
            st.error(f"Error accessing {folder_path}: {str(e)[:100]}")
        
        return []
    
    def _get_fallback_files(self, folder_path: str) -> List[Dict]:
        """Fallback method to get files using raw GitHub (no API)"""
        # This is a best-effort fallback - you'll need to list files manually
        # or use the add_file method
        return []
    
    def discover_all_files(self) -> Dict:
        """Discover all PDF files in all relevant folders"""
        all_files = {
            "ASSIGNMENTS/COMPUTER": [],
            "ASSIGNMENTS/ENGLISH LANGUAGE": [],
            "ASSIGNMENTS/ENGLISH LITERATURE": [],
            "ASSIGNMENTS/MATHEMATICS": [],
            "ASSIGNMENTS/SCIENCE": [],
            "ASSIGNMENTS/SOCIAL STUDIES": [],
            "FIRST REVIEW REVISION PAPERS": [],
            "PROJECT": []
        }
        
        for folder in all_files.keys():
            files = self.get_files_in_folder(folder)
            all_files[folder] = files
        
        return all_files
    
    def extract_text_from_pdf(self, file_url: str) -> str:
        """Extract text from PDF file"""
        try:
            response = requests.get(file_url, timeout=30)
            if response.status_code == 200:
                import io
                import PyPDF2
                
                pdf_file = io.BytesIO(response.content)
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                text = ""
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                return text
        except ImportError:
            pass
        except Exception as e:
            pass
        
        return ""
    
    def extract_questions_from_text(self, text: str) -> list:
        """Extract questions from extracted PDF text"""
        questions = []
        
        if not text:
            return questions
        
        lines = text.split('\n')
        
        # Pattern for numbered questions
        patterns = [
            r'^(\d+)[\.\)]\s+(.+)$',
            r'^Q\.?\s*(\d+)[\.\)]?\s+(.+)$',
        ]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            for pattern in patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    question_text = match.group(2) if len(match.groups()) > 1 else line
                    if question_text and len(question_text) > 10:
                        questions.append(question_text)
                    break
        
        # Look for lines with question marks
        for line in lines:
            line = line.strip()
            if line.endswith('?') and 20 < len(line) < 300 and line not in questions:
                clean_q = re.sub(r'^\d+[\.\)]\s*', '', line)
                if clean_q:
                    questions.append(clean_q)
        
        return questions[:30]
    
    def get_questions_from_pdf(self, file_url: str) -> list:
        """Get questions from a PDF file"""
        text = self.extract_text_from_pdf(file_url)
        if text:
            return self.extract_questions_from_text(text)
        return []
    
    def get_file_type(self, filename: str) -> str:
        ext = filename.split('.')[-1].lower()
        types = {'pdf': 'pdf', 'doc': 'word', 'docx': 'word', 'jpg': 'image', 'png': 'image'}
        return types.get(ext, 'unknown')
    
    def get_subjects(self) -> List[Dict]:
        return [
            {'id': 'computer', 'name': 'Computer Science', 'folder_name': 'COMPUTER', 'icon': '💻', 'color': '#4A90E2', 'path': 'COMPUTER'},
            {'id': 'english-language', 'name': 'English Language', 'folder_name': 'ENGLISH LANGUAGE', 'icon': '✍️', 'color': '#9C27B0', 'path': 'ENGLISH LANGUAGE'},
            {'id': 'english-literature', 'name': 'English Literature', 'folder_name': 'ENGLISH LITERATURE', 'icon': '📖', 'color': '#9C27B0', 'path': 'ENGLISH LITERATURE'},
            {'id': 'mathematics', 'name': 'Mathematics', 'folder_name': 'MATHEMATICS', 'icon': '🧮', 'color': '#FF9800', 'path': 'MATHEMATICS'},
            {'id': 'science', 'name': 'Science', 'folder_name': 'SCIENCE', 'icon': '🔬', 'color': '#4CAF50', 'path': 'SCIENCE'},
            {'id': 'social-studies', 'name': 'Social Studies', 'folder_name': 'SOCIAL STUDIES', 'icon': '🌍', 'color': '#F44336', 'path': 'SOCIAL STUDIES'}
        ]
    
    def get_chapters(self, subject_path: str) -> List[Dict]:
        return []
    
    def get_chapter_content(self, subject_path: str, chapter_path: str) -> Dict:
        return {'content': '', 'key_points': [], 'vocabulary': [], 'fun_fact': '', 'practice_questions': []}
    
    def get_revision_papers(self) -> List[Dict]:
        return self.get_files_in_folder("FIRST REVIEW REVISION PAPERS")
    
    def get_projects(self) -> List[Dict]:
        return self.get_files_in_folder("PROJECT")
    
    def get_total_resources_count(self) -> Dict:
        all_files = self.discover_all_files()
        total_assignments = 0
        for folder, files in all_files.items():
            if folder.startswith("ASSIGNMENTS/"):
                total_assignments += len(files)
        
        return {
            'subjects': 6,
            'chapters': 0,
            'assignments': total_assignments,
            'revision_papers': len(all_files.get("FIRST REVIEW REVISION PAPERS", [])),
            'projects': len(all_files.get("PROJECT", []))
        }

# Create singleton instance
@st.cache_resource
def get_github_storage():
    return GitHubStorage()

github_storage = get_github_storage()
