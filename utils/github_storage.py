"""
GitHub Storage Helper - Complete with PDF Question Extraction
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
        
        # Subject configuration
        self.subjects_data = {
            "COMPUTER": {
                "display_name": "Computer Science",
                "icon": "💻",
                "color": "#4A90E2",
                "chapters": {
                    "Chapter 1 - Storage and Memory Devices": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%201%20-%20Storage%20and%20Memory%20Devices/content.md"
                    },
                    "Chapter 2 - Editing in MS Word 2013": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%202%20-%20Editing%20in%20MS%20Word%202013/content.md"
                    },
                    "Chapter 3 - Formatting in MS Word 2013": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%203%20-%20Formatting%20in%20MS%20Word%202013/content.md"
                    },
                    "Chapter 4 - Desktop Management": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%204%20-%20Desktop%20Management/content.md"
                    },
                    "Chapter 5 - AI and Humans": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%205%20-%20AI%20and%20Humans/content.md"
                    }
                }
            },
            "ENGLISH LANGUAGE": {
                "display_name": "English Language",
                "icon": "✍️",
                "color": "#9C27B0",
                "chapters": {
                    "Chapter 1 - The Sentence": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%201%20-%20The%20Sentence/content.md"
                    },
                    "Chapter 2 - Subject and Predicate": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%202%20-%20Subject%20and%20Predicate/content.md"
                    },
                    "Chapter 3 - Nouns (Possessive, Collective, Abstract)": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%203%20-%20Nouns%20(Possessive%2C%20Collective%2C%20Abstract)/content.md"
                    },
                    "Chapter 4 - Adjectives (Kinds and Degrees)": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%204%20-%20Adjectives%20(Kinds%20and%20Degrees)/content.md"
                    },
                    "Chapter 5 - Prepositions": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%205%20-%20Prepositions/content.md"
                    }
                }
            },
            "ENGLISH LITERATURE": {
                "display_name": "English Literature",
                "icon": "📖",
                "color": "#9C27B0",
                "chapters": {
                    "Poem - A Home Song": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Poem%20-%20A%20Home%20Song/content.md"
                    },
                    "Chapter 1 - The Enchanted Castle": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Chapter%201%20-%20The%20Enchanted%20Castle/content.md"
                    },
                    "Chapter 2 - What Robin Told Me": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Chapter%202%20-%20What%20Robin%20Told%20Me/content.md"
                    },
                    "Chapter 3 - The Grateful Snow Crane": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Chapter%203%20-%20The%20Grateful%20Snow%20Crane/content.md"
                    },
                    "Chapter 4 - The Big Race": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Chapter%204%20-%20The%20Big%20Race/content.md"
                    }
                }
            },
            "MATHEMATICS": {
                "display_name": "Mathematics",
                "icon": "🧮",
                "color": "#FF9800",
                "chapters": {
                    "Chapter 1 - Large Numbers": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/MATHEMATICS/Chapter%201%20-%20Large%20Numbers/content.md"
                    },
                    "Chapter 2 - Addition and Subtraction": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/MATHEMATICS/Chapter%202%20-%20Addition%20and%20Subtraction/content.md"
                    },
                    "Chapter 3 - Multiplication": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/MATHEMATICS/Chapter%203%20-%20Multiplication/content.md"
                    },
                    "Chapter 4 - Division": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/MATHEMATICS/Chapter%204%20-%20Division/content.md"
                    },
                    "Chapter 5 - Multiples and Factors": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/MATHEMATICS/Chapter%205%20-%20Multiples%20and%20Factors/content.md"
                    },
                    "Chapter 6 - HCF and LCM": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/MATHEMATICS/Chapter%206%20-%20HCF%20and%20LCM/content.md"
                    },
                    "Chapter 7 - Geometry": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/MATHEMATICS/Chapter%207%20-%20Geometry/content.md"
                    }
                }
            },
            "SCIENCE": {
                "display_name": "Science",
                "icon": "🔬",
                "color": "#4CAF50",
                "chapters": {
                    "Chapter 1 - Human Body - The Food We Eat": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SCIENCE/Chapter%201%20-%20Human%20Body%20-%20The%20Food%20We%20Eat/content.md"
                    },
                    "Chapter 2 - Push and Pull": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SCIENCE/Chapter%202%20-%20Push%20and%20Pull/content.md"
                    },
                    "Chapter 3 - Friction as a Force": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SCIENCE/Chapter%203%20-%20Friction%20as%20a%20Force/content.md"
                    },
                    "Chapter 4 - Plants in the Surroundings": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SCIENCE/Chapter%204%20-%20Plants%20in%20the%20Surroundings/content.md"
                    },
                    "Chapter 5 - Adaptation in Plants": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SCIENCE/Chapter%205%20-%20Adaptation%20in%20Plants/content.md"
                    }
                }
            },
            "SOCIAL STUDIES": {
                "display_name": "Social Studies",
                "icon": "🌍",
                "color": "#F44336",
                "chapters": {
                    "Chapter 1 - Types and Elements of Maps": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SOCIAL%20STUDIES/Chapter%201%20-%20Types%20and%20Elements%20of%20Maps/content.md"
                    },
                    "Chapter 2 - The Iron Age": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SOCIAL%20STUDIES/Chapter%202%20-%20The%20Iron%20Age/content.md"
                    },
                    "Chapter 3 - Political Divisions of North and West India": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SOCIAL%20STUDIES/Chapter%203%20-%20Political%20Divisions%20of%20North%20and%20West%20India/content.md"
                    },
                    "Chapter 4 - Other River-based Civilizations": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SOCIAL%20STUDIES/Chapter%204%20-%20Other%20River-based%20Civilizations/content.md"
                    },
                    "Chapter 5 - We Depend on Each Other": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SOCIAL%20STUDIES/Chapter%205%20-%20We%20Depend%20on%20Each%20Other/content.md"
                    }
                }
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
        cache_key = f"{subject_path}_{chapter_path}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        chapter_title = chapter_path.split('/')[-1] if '/' in chapter_path else chapter_path
        
        if subject_path in self.subjects_data:
            chapter_data = self.subjects_data[subject_path]['chapters'].get(chapter_title)
            
            if chapter_data and 'url' in chapter_data:
                url = chapter_data['url']
                
                try:
                    response = requests.get(url, timeout=15)
                    
                    if response.status_code == 200:
                        content = response.text
                        parsed = self.parse_markdown(content, chapter_title)
                        self.cache[cache_key] = parsed
                        return parsed
                    else:
                        return self.get_empty_chapter(chapter_title, f"HTTP {response.status_code}")
                except Exception as e:
                    return self.get_empty_chapter(chapter_title, str(e))
        
        return self.get_empty_chapter(chapter_title, "No URL configured")
    
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
                            'url': f"{self.raw_base}/{folder_path}/{item['name']}",
                            'size': item.get('size', 0),
                            'type': self.get_file_type(item['name'])
                        })
            return files
        except:
            return []
    
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
            st.warning("PyPDF2 not installed. PDF extraction may be limited.")
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
            r'^Question\s*(\d+)[:\.\)]\s+(.+)$',
            r'^[\(](\d+)[\)]\s+(.+)$',
        ]
        
        current_question = None
        current_text = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            matched = False
            for pattern in patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    if current_question:
                        full_text = ' '.join(current_text).strip()
                        if full_text and len(full_text) > 10:
                            questions.append({'question': full_text, 'type': 'open'})
                    current_question = match.group(2) if len(match.groups()) > 1 else line
                    current_text = [current_question]
                    matched = True
                    break
            
            if not matched and current_question:
                current_text.append(line)
        
        if current_question:
            full_text = ' '.join(current_text).strip()
            if full_text and len(full_text) > 10:
                questions.append({'question': full_text, 'type': 'open'})
        
        if len(questions) < 3:
            for line in lines:
                line = line.strip()
                if '?' in line and len(line) > 15 and len(line) < 200:
                    if not re.match(r'^[A-D][\.\)]', line):
                        questions.append({'question': line, 'type': 'open'})
        
        return questions[:30]
    
    def get_questions_from_pdf(self, file_url: str) -> list:
        """Get questions from a PDF file"""
        text = self.extract_text_from_pdf(file_url)
        if text:
            return self.extract_questions_from_text(text)
        return []
    
    def get_questions_from_folder(self, folder_path: str) -> list:
        """Get all questions from PDF files in a folder"""
        all_questions = []
        files = self.get_files_in_folder(folder_path)
        
        for file in files:
            if file['type'] == 'pdf':
                questions = self.get_questions_from_pdf(file['url'])
                if questions:
                    for q in questions:
                        q['source'] = file['name']
                    all_questions.extend(questions)
        
        return all_questions
    
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
        """Get revision papers"""
        try:
            return self.get_files_in_folder("FIRST REVIEW REVISION PAPERS")
        except:
            return []
    
    def get_projects(self) -> List[Dict]:
        """Get projects"""
        try:
            return self.get_files_in_folder("PROJECT")
        except:
            return []
    
    def get_total_resources_count(self) -> Dict:
        """Get resource counts"""
        total_chapters = 0
        for subject in self.subjects_data.values():
            total_chapters += len(subject.get('chapters', {}))
        
        return {
            'subjects': len(self.subjects_data),
            'chapters': total_chapters,
            'assignments': 0,
            'revision_papers': len(self.get_revision_papers()),
            'projects': len(self.get_projects())
        }
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from extension"""
        ext = filename.split('.')[-1].lower()
        types = {
            'pdf': 'pdf', 'doc': 'word', 'docx': 'word',
            'jpg': 'image', 'png': 'image', 'md': 'markdown',
            'txt': 'text'
        }
        return types.get(ext, 'unknown')
    
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
        
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            chapter_data['title'] = title_match.group(1).strip()
        
        content_match = re.search(r'## Content\s+(.*?)(?=##|$)', content, re.DOTALL)
        if content_match:
            chapter_data['content'] = content_match.group(1).strip()
        
        points_match = re.search(r'## Key Points\s+(.*?)(?=##|$)', content, re.DOTALL)
        if points_match:
            points_text = points_match.group(1)
            points = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', points_text, re.DOTALL)
            if points:
                chapter_data['key_points'] = [p.strip() for p in points]
            else:
                chapter_data['key_points'] = [line.strip() for line in points_text.split('\n') if line.strip() and not line.startswith('#')]
        
        vocab_match = re.search(r'## Vocabulary\s+(.*?)(?=##|$)', content, re.DOTALL)
        if vocab_match:
            vocab_text = vocab_match.group(1)
            vocab_items = re.findall(r'\*\*(.*?)\*\*', vocab_text)
            if not vocab_items:
                vocab_items = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', vocab_text, re.DOTALL)
            chapter_data['vocabulary'] = [v.strip() for v in vocab_items][:10]
        
        fun_match = re.search(r'## Fun Fact\s+(.*?)(?=##|$)', content, re.DOTALL)
        if fun_match:
            chapter_data['fun_fact'] = fun_match.group(1).strip()
        
        questions_match = re.search(r'## Practice Questions\s+(.*?)(?=##|$)', content, re.DOTALL)
        if questions_match:
            questions_text = questions_match.group(1)
            questions = re.findall(r'[-•*]\s*(.+?)(?=\n[-•*]|\n\n|$)', questions_text, re.DOTALL)
            if questions:
                chapter_data['practice_questions'] = [q.strip() for q in questions]
            else:
                chapter_data['practice_questions'] = [q.strip() for q in questions_text.split('\n') if q.strip() and not q.startswith('#')]
        
        if not chapter_data['content'] and not chapter_data['key_points']:
            chapter_data['content'] = content[:500] + ("..." if len(content) > 500 else "")
        
        return chapter_data
    
    def get_empty_chapter(self, title: str = "", error: str = "") -> Dict:
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

# Create singleton instance
@st.cache_resource
def get_github_storage():
    return GitHubStorage()

github_storage = get_github_storage()
