"""
GitHub Storage Helper - With Your Actual PDF Files
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
        
        # ADD YOUR ACTUAL PDF FILES HERE
        # Based on your screenshots, you have these files:
        self.known_files = {
            "ASSIGNMENTS/COMPUTER": [
                {"name": "Computer Assignment 1.pdf", "url": f"{self.raw_base}/ASSIGNMENTS/COMPUTER/Computer%20Assignment%201.pdf", "type": "pdf", "size": 0}
            ],
            "ASSIGNMENTS/ENGLISH LANGUAGE": [
                {"name": "English Assignment.pdf", "url": f"{self.raw_base}/ASSIGNMENTS/ENGLISH%20LANGUAGE/English%20Assignment.pdf", "type": "pdf", "size": 0}
            ],
            "ASSIGNMENTS/ENGLISH LITERATURE": [
                {"name": "Literature Assignment.pdf", "url": f"{self.raw_base}/ASSIGNMENTS/ENGLISH%20LITERATURE/Literature%20Assignment.pdf", "type": "pdf", "size": 0}
            ],
            "ASSIGNMENTS/MATHEMATICS": [
                {"name": "Math Assignment.pdf", "url": f"{self.raw_base}/ASSIGNMENTS/MATHEMATICS/Math%20Assignment.pdf", "type": "pdf", "size": 0}
            ],
            "ASSIGNMENTS/SCIENCE": [
                {"name": "Science Assignment.pdf", "url": f"{self.raw_base}/ASSIGNMENTS/SCIENCE/Science%20Assignment.pdf", "type": "pdf", "size": 0}
            ],
            "ASSIGNMENTS/SOCIAL STUDIES": [
                {"name": "Social Studies Assignment.pdf", "url": f"{self.raw_base}/ASSIGNMENTS/SOCIAL%20STUDIES/Social%20Studies%20Assignment.pdf", "type": "pdf", "size": 0}
            ],
            "FIRST REVIEW REVISION PAPERS": [
                {"name": "Class 4 1st Review Test.pdf", "url": f"{self.raw_base}/FIRST%20REVIEW%20REVISION%20PAPERS/Class%204%201st%20Review%20Test.pdf", "type": "pdf", "size": 0},
                {"name": "Class 4 First Term Syllabus (2026-27)-2.pdf", "url": f"{self.raw_base}/FIRST%20REVIEW%20REVISION%20PAPERS/Class%204%20First%20Term%20Syllabus%20(2026-27)-2.pdf", "type": "pdf", "size": 0}
            ],
            "PROJECT": [
                {"name": "Class 4 First Term Syllabus.pdf", "url": f"{self.raw_base}/PROJECT/Class%204%20First%20Term%20Syllabus.pdf", "type": "pdf", "size": 0}
            ]
        }
    
    def get_files_in_folder(self, folder_path: str) -> List[Dict]:
        """Get files from a folder using known files list"""
        if folder_path in self.known_files:
            return self.known_files[folder_path]
        return []
    
    def add_file(self, folder_path: str, filename: str, file_url: str) -> None:
        """Add a file to the known files list"""
        if folder_path not in self.known_files:
            self.known_files[folder_path] = []
        
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
                    if question_text and len(question_text) > 10 and '?' in question_text:
                        questions.append(question_text)
                    break
        
        # Also look for lines with question marks
        for line in lines:
            line = line.strip()
            if line.endswith('?') and 20 < len(line) < 300 and line not in questions:
                clean_q = re.sub(r'^\d+[\.\)]\s*', '', line)
                if clean_q:
                    questions.append(clean_q)
        
        return questions[:25]
    
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
    
    def get_revision_papers(self) -> List[Dict]:
        return self.known_files.get("FIRST REVIEW REVISION PAPERS", [])
    
    def get_projects(self) -> List[Dict]:
        return self.known_files.get("PROJECT", [])
    
    def get_total_resources_count(self) -> Dict:
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
