"""
GitHub Storage Helper - Complete with Fixed File Listing
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
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{self.encoded_path}"
        
        self.cache = {}
        
        # Subject configuration (keep your existing subjects_data here)
        self.subjects_data = {
            "COMPUTER": {
                "display_name": "Computer Science",
                "icon": "💻",
                "color": "#4A90E2",
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
            },
            "MATHEMATICS": {
                "display_name": "Mathematics",
                "icon": "🧮",
                "color": "#FF9800",
                "chapters": {}
            },
            "SCIENCE": {
                "display_name": "Science",
                "icon": "🔬",
                "color": "#4CAF50",
                "chapters": {}
            },
            "SOCIAL STUDIES": {
                "display_name": "Social Studies",
                "icon": "🌍",
                "color": "#F44336",
                "chapters": {}
            }
        }
    
    def get_files_in_folder(self, folder_path: str) -> List[Dict]:
        """Get all files in a specific folder using direct GitHub API"""
        files = []
        
        # Build the API URL for the folder
        folder_api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{self.encoded_path}/{folder_path}"
        
        # URL encode the folder path
        folder_api_url = folder_api_url.replace(' ', '%20')
        
        try:
            # Add a User-Agent header to avoid API restrictions
            headers = {
                'User-Agent': 'Class4LearningHub/1.0',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(folder_api_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                items = response.json()
                for item in items:
                    if item['type'] == 'file':
                        # Get file extension
                        file_ext = item['name'].split('.')[-1].lower() if '.' in item['name'] else ''
                        
                        files.append({
                            'name': item['name'],
                            'url': item['download_url'],
                            'size': item.get('size', 0),
                            'type': self.get_file_type(item['name'])
                        })
            else:
                st.warning(f"Could not access folder: {folder_path} (Status: {response.status_code})")
                
        except Exception as e:
            st.error(f"Error accessing folder {folder_path}: {str(e)[:100]}")
        
        return files
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from extension"""
        ext = filename.split('.')[-1].lower()
        types = {
            'pdf': 'pdf', 'doc': 'word', 'docx': 'word',
            'jpg': 'image', 'png': 'image', 'md': 'markdown',
            'txt': 'text', 'pptx': 'powerpoint', 'xlsx': 'excel'
        }
        return types.get(ext, 'unknown')
    
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
    
    # Keep other existing methods...
    def get_subjects(self) -> List[Dict]:
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
        return []
    
    def get_chapter_content(self, subject_path: str, chapter_path: str) -> Dict:
        return {'content': '', 'key_points': [], 'vocabulary': [], 'fun_fact': '', 'practice_questions': []}
    
    def get_all_assignments(self) -> Dict[str, List[Dict]]:
        return {}
    
    def get_revision_papers(self) -> List[Dict]:
        return self.get_files_in_folder("FIRST REVIEW REVISION PAPERS")
    
    def get_projects(self) -> List[Dict]:
        return self.get_files_in_folder("PROJECT")
    
    def get_total_resources_count(self) -> Dict:
        return {'subjects': 6, 'chapters': 0, 'assignments': 0, 'revision_papers': 0, 'projects': 0}

# Create singleton instance
@st.cache_resource
def get_github_storage():
    return GitHubStorage()

github_storage = get_github_storage()
