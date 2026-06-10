"""
GitHub Storage Helper - Using Raw URLs (No API required)
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
        
        self.cache = {}
        
        # Manually list known PDF files in each folder
        # Add your PDF files here as you upload them
        self.known_files = {
            "ASSIGNMENTS/COMPUTER": [
                # Add your Computer Science PDFs here
                # {"name": "your_file.pdf", "url": f"{self.raw_base}/ASSIGNMENTS/COMPUTER/your_file.pdf"}
            ],
            "ASSIGNMENTS/ENGLISH LANGUAGE": [
                # Add your English PDFs here
            ],
            "ASSIGNMENTS/ENGLISH LITERATURE": [
                # Add your English Literature PDFs here
            ],
            "ASSIGNMENTS/MATHEMATICS": [
                # Add your Math PDFs here
            ],
            "ASSIGNMENTS/SCIENCE": [
                # Add your Science PDFs here
            ],
            "ASSIGNMENTS/SOCIAL STUDIES": [
                # Add your Social Studies PDFs here
            ],
            "FIRST REVIEW REVISION PAPERS": [
                # Add revision papers here
                # {"name": "Class 4 1st Review Test.pdf", "url": f"{self.raw_base}/FIRST REVIEW REVISION PAPERS/Class 4 1st Review Test.pdf"}
            ],
            "PROJECT": [
                # Add project files here
            ]
        }
    
    def get_files_in_folder(self, folder_path: str) -> List[Dict]:
        """Get files from a folder using known files list"""
        
        # Return known files for this folder
        if folder_path in self.known_files:
            return self.known_files[folder_path]
        
        # If not in known files, try to fetch from GitHub raw (will only work if file exists)
        files = []
        return files
    
    def add_file(self, folder_path: str, filename: str, file_url: str) -> None:
        """Add a file to the known files list (call this when you add new PDFs)"""
        if folder_path not in self.known_files:
            self.known_files[folder_path] = []
        
        # Check if file already exists
        exists = False
        for f in self.known_files[folder_path]:
            if f['name'] == filename:
                exists = True
                break
        
        if not exists:
            self.known_files[folder_path].append({
                'name': filename,
                'url': file_url,
                'type': 'pdf',
                'size': 0
            })
    
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
            st.warning("PyPDF2 not installed. Install with: pip install PyPDF2")
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)[:100]}")
        
        return ""
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from extension"""
        ext = filename.split('.')[-1].lower()
        types = {
            'pdf': 'pdf', 'doc': 'word', 'docx': 'word',
            'jpg': 'image', 'png': 'image', 'md': 'markdown',
            'txt': 'text'
        }
        return types.get(ext, 'unknown')
    
    def extract_questions_from_text(self, text: str) -> list:
        """Extract questions from extracted PDF text"""
        questions = []
        
        if not text:
            return questions
        
        lines = text.split('\n')
        
        patterns = [
            r'^(\d+)[\.\)]\s+(.+)$',
            r'^Q\.?\s*(\d+)[\.\)]?\s+(.+)$',
            r'^Question\s*(\d+)[:\.\)]\s+(.+)$',
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
        
        return questions[:30]
    
    def get_questions_from_pdf(self, file_url: str) -> list:
        """Get questions from a PDF file"""
        text = self.extract_text_from_pdf(file_url)
        if text:
            return self.extract_questions_from_text(text)
        return []
    
    def get_all_assignments(self) -> Dict[str, List[Dict]]:
        """Get all assignments grouped by subject"""
        all_assignments = {}
        for folder_path, files in self.known_files.items():
            if folder_path.startswith("ASSIGNMENTS/"):
                subject = folder_path.replace("ASSIGNMENTS/", "")
                if files:
                    all_assignments[subject] = files
        return all_assignments
    
    def get_revision_papers(self) -> List[Dict]:
        """Get revision papers"""
        return self.known_files.get("FIRST REVIEW REVISION PAPERS", [])
    
    def get_projects(self) -> List[Dict]:
        """Get projects"""
        return self.known_files.get("PROJECT", [])
    
    def get_total_resources_count(self) -> Dict:
        """Get resource counts"""
        total_assignments = 0
        for folder, files in self.known_files.items():
            if folder.startswith("ASSIGNMENTS/"):
                total_assignments += len(files)
        
        return {
            'subjects': 6,
            'chapters': 0,
            'assignments': total_assignments,
            'revision_papers': len(self.known_files.get("FIRST REVIEW REVISION PAPERS", [])),
            'projects': len(self.known_files.get("PROJECT", []))
        }
    
    def get_subjects(self) -> List[Dict]:
        """Get list of subjects"""
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

# Create singleton instance
@st.cache_resource
def get_github_storage():
    return GitHubStorage()

github_storage = get_github_storage()
