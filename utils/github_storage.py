"""
GitHub Storage Helper - Direct URL Version for Class 4 Learning Hub
Fetches chapter content directly from raw GitHub URLs
"""

import streamlit as st
import requests
import re
from typing import Dict, List

class GitHubStorage:
    def __init__(self):
        # Define subjects and chapters with DIRECT URLs to content.md
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
                    },
                    "Chapter 3 - Internet and Email": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%203%20-%20Internet%20and%20Email/content.md"
                    },
                    "Chapter 4 - MS Paint": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/COMPUTER/Chapter%204%20-%20MS%20Paint/content.md"
                    }
                }
            },
            "SCIENCE": {
                "display_name": "Science",
                "icon": "🔬",
                "color": "#4CAF50",
                "chapters": {
                    "Chapter 1 - Plants": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SCIENCE/Chapter%201%20-%20Plants/content.md"
                    },
                    "Chapter 2 - Animals": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SCIENCE/Chapter%202%20-%20Animals/content.md"
                    },
                    "Chapter 3 - Our Body": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/SCIENCE/Chapter%203%20-%20Our%20Body/content.md"
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
                    }
                }
            },
            "ENGLISH LANGUAGE": {
                "display_name": "English Language",
                "icon": "✍️",
                "color": "#9C27B0",
                "chapters": {
                    "Chapter 1 - Nouns and Pronouns": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%201%20-%20Nouns%20and%20Pronouns/content.md"
                    },
                    "Chapter 2 - Verbs and Tenses": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%202%20-%20Verbs%20and%20Tenses/content.md"
                    },
                    "Chapter 3 - Adjectives and Adverbs": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%203%20-%20Adjectives%20and%20Adverbs/content.md"
                    },
                    "Chapter 4 - Sentence Formation": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LANGUAGE/Chapter%204%20-%20Sentence%20Formation/content.md"
                    }
                }
            },
            "ENGLISH LITERATURE": {
                "display_name": "English Literature",
                "icon": "📖",
                "color": "#9C27B0",
                "chapters": {
                    "Chapter 1 - The Magic Garden": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Chapter%201%20-%20The%20Magic%20Garden/content.md"
                    },
                    "Chapter 2 - The Enchanted Castle": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Chapter%202%20-%20The%20Enchanted%20Castle/content.md"
                    },
                    "Chapter 3 - The Giving Tree": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Chapter%203%20-%20The%20Giving%20Tree/content.md"
                    },
                    "Poem - A Home Song": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/ENGLISH%20LITERATURE/Poem%20-%20A%20Home%20Song/content.md"
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
                    'id': chapter_title.lower().replace(' ', '-').replace('-', '-'),
                    'title': chapter_title,
                    'path': f"{subject_path}/{chapter_title}",
                    'folder': chapter_title
                })
            return chapters
        return []
    
    def get_chapter_content(self, subject_path: str, chapter_path: str) -> Dict:
        """Get chapter content directly from URL"""
        cache_key = f"chapter_{subject_path}_{chapter_path}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Extract chapter title from chapter_path
        chapter_title = chapter_path.split('/')[-1]
        
        # Get the chapter URL from our data
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
        """Get files from a folder (for assignments, projects)"""
        # This is for future implementation
        return []
    
    def get_all_assignments(self) -> Dict[str, List[Dict]]:
        """Get all assignments grouped by subject"""
        # This is for future implementation
        return {}
    
    def get_revision_papers(self) -> List[Dict]:
        """Get revision papers from FIRST REVIEW REVISION PAPERS folder"""
        # This is for future implementation
        return []
    
    def get_projects(self) -> List[Dict]:
        """Get projects from PROJECT folder"""
        # This is for future implementation
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
            'revision_papers': 0,
            'projects': 0
        }
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from extension"""
        ext = filename.split('.')[-1].lower()
        types = {
            'pdf': 'pdf', 'doc': 'word', 'docx': 'word',
            'jpg': 'image', 'png': 'image', 'md': 'markdown'
        }
        return types.get(ext, 'unknown')
    
    def parse_markdown(self, content: str, title: str = "") -> Dict:
        """Parse markdown content into structured format"""
        lines = content.split('\n')
        
        chapter_data = {
            'title': title if title else 'Chapter',
            'content': '',
            'key_points': [],
            'vocabulary': [],
            'fun_fact': '',
            'practice_questions': []
        }
        
        current_section = None
        current_text = []
        
        for line in lines:
            # Title from markdown heading
            if line.startswith('# ') and not chapter_data['title']:
                chapter_data['title'] = line[2:].strip()
            
            # Detect sections
            elif line.startswith('## Content'):
                current_section = 'content'
                current_text = []
            elif line.startswith('## Key Points'):
                if current_section == 'content' and current_text:
                    chapter_data['content'] = '\n'.join(current_text).strip()
                current_section = 'key_points'
                current_text = []
            elif line.startswith('## Vocabulary'):
                if current_section == 'key_points' and current_text:
                    chapter_data['key_points'] = [p for p in current_text if p.strip()]
                current_section = 'vocabulary'
                current_text = []
            elif line.startswith('## Fun Fact'):
                if current_section == 'vocabulary' and current_text:
                    # Handle vocabulary words that might be bolded
                    vocab_items = []
                    for v in current_text:
                        # Extract bold text or clean up
                        bold_match = re.search(r'\*\*(.*?)\*\*', v)
                        if bold_match:
                            vocab_items.append(bold_match.group(1))
                        elif v.strip():
                            vocab_items.append(v.strip())
                    chapter_data['vocabulary'] = vocab_items if vocab_items else current_text
                current_section = 'fun_fact'
                current_text = []
            elif line.startswith('## Practice Questions'):
                if current_section == 'fun_fact' and current_text:
                    chapter_data['fun_fact'] = '\n'.join(current_text).strip()
                current_section = 'questions'
                current_text = []
            
            # Bullet points
            elif line.startswith('- ') or line.startswith('• ') or line.startswith('* '):
                if current_text is not None:
                    bullet_text = line.lstrip('-•* ').strip()
                    if bullet_text:
                        current_text.append(bullet_text)
            
            # Bold text for vocabulary
            elif '**' in line and current_section == 'vocabulary':
                if current_text is not None:
                    current_text.append(line.strip())
            
            # Regular text (not empty and not a header)
            elif line.strip() and not line.startswith('#'):
                if current_text is not None:
                    current_text.append(line.strip())
        
        # Handle last section
        if current_section == 'questions' and current_text:
            chapter_data['practice_questions'] = [q for q in current_text if q.strip()]
        
        # If no content was parsed, use regex to extract
        if not chapter_data['content'] and not chapter_data['key_points']:
            # Try to extract content between ## Content and next ##
            content_match = re.search(r'## Content\s+(.*?)(?=##|$)', content, re.DOTALL)
            if content_match:
                chapter_data['content'] = content_match.group(1).strip()
            else:
                chapter_data['content'] = content[:500] if content else "Content not available"
        
        return chapter_data
    
    def get_empty_chapter(self, title: str = "", error: str = "") -> Dict:
        """Return empty chapter structure for missing content"""
        error_msg = f" ({error})" if error else ""
        return {
            'title': title if title else 'Content Coming Soon',
            'content': f'📚 This chapter content is being prepared. Check back later!{error_msg}',
            'key_points': ['✨ Exciting content coming soon!'],
            'vocabulary': ['📖 New words will appear here'],
            'fun_fact': '🌟 Learning is an adventure!',
            'practice_questions': ['💭 What do you hope to learn in this chapter?']
        }
    
    def clear_cache(self):
        """Clear the cache"""
        self.cache = {}

# Create singleton instance
@st.cache_resource
def get_github_storage():
    """Get or create the GitHub storage instance"""
    return GitHubStorage()

# Global instance
github_storage = get_github_storage()
