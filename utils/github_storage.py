"""
GitHub Storage Helper - Complete Version for Class 4 Learning Hub
Contains all subjects and chapters from the syllabus
"""

import streamlit as st
import requests
import re
from typing import Dict, List

class GitHubStorage:
    def __init__(self):
        # Define all subjects and chapters with DIRECT URLs to content.md
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
            },
            "HINDI": {
                "display_name": "Hindi (2nd Language)",
                "icon": "🇮🇳",
                "color": "#FF5722",
                "chapters": {
                    "Chapter 1 - झंडा ऊँचा रहे हमारा": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/HINDI/Chapter%201%20-%20%E0%A4%9D%E0%A4%82%E0%A4%A1%E0%A4%BE%20%E0%A4%8A%E0%A4%81%E0%A4%9A%E0%A4%BE%20%E0%A4%B0%E0%A4%B9%E0%A5%87%20%E0%A4%B9%E0%A4%AE%E0%A4%BE%E0%A4%B0%E0%A4%BE/content.md"
                    },
                    "Chapter 2 - एकता में बल": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/HINDI/Chapter%202%20-%20%E0%A4%8F%E0%A4%95%E0%A4%A4%E0%A4%BE%20%E0%A4%AE%E0%A5%87%E0%A4%82%20%E0%A4%AC%E0%A4%B2/content.md"
                    }
                }
            },
            "BENGALI": {
                "display_name": "Bengali (2nd Language)",
                "icon": "🇧🇩",
                "color": "#FF9800",
                "chapters": {
                    "Chapter 1 - ইদুরের ভাজ": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/BENGALI/Chapter%201%20-%20%E0%A6%87%E0%A6%A6%E0%A7%81%E0%A6%B0%E0%A7%87%E0%A6%B0%20%E0%A6%AD%E0%A6%BE%E0%A6%9C/content.md"
                    },
                    "Chapter 2 - আমরা ঘোসের ছোট ছোট ফুল": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/BENGALI/Chapter%202%20-%20%E0%A6%86%E0%A6%AE%E0%A6%B0%E0%A6%BE%20%E0%A6%98%E0%A7%8B%E0%A6%B8%E0%A7%87%E0%A6%B0%20%E0%A6%9B%E0%A7%8B%E0%A6%9F%20%E0%A6%9B%E0%A7%8B%E0%A6%9F%20%E0%A6%AB%E0%A7%81%E0%A6%B2/content.md"
                    },
                    "Chapter 3 - খাকেনের বন্ধু": {
                        "url": "https://raw.githubusercontent.com/saswat1087-code/class4-learning-hub/main/data/CLASS%204%20(2026-27)/FIRST%20TERM/BENGALI/Chapter%203%20-%20%E0%A6%96%E0%A6%BE%E0%A6%95%E0%A7%87%E0%A6%A8%E0%A7%87%E0%A6%B0%20%E0%A6%AC%E0%A6%A8%E0%A7%8D%E0%A6%A7%E0%A7%81/content.md"
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
        """Get files from a folder (for assignments, projects)"""
        return []
    
    def get_all_assignments(self) -> Dict[str, List[Dict]]:
        """Get all assignments grouped by subject"""
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
        chapter_data = {
            'title': title,
            'content': '',
            'key_points': [],
            'vocabulary': [],
            'fun_fact': '',
            'practice_questions': []
        }
        
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
                chapter_data['key_points'] = [line.strip() for line in points_text.split('\n') if line.strip() and not line.startswith('#')]
        
        # Extract vocabulary
        vocab_match = re.search(r'## Vocabulary\s+(.*?)(?=##|$)', content, re.DOTALL)
        if vocab_match:
            vocab_text = vocab_match.group(1)
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
        """Clear the cache"""
        self.cache = {}

# Create singleton instance
@st.cache_resource
def get_github_storage():
    """Get or create the GitHub storage instance"""
    return GitHubStorage()

# Global instance
github_storage = get_github_storage()
