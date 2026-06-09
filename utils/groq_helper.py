"""
Groq AI Helper Module - Super fast AI for Class 4 Learning Hub
Uses Groq's Llama 3.3 70B model (16,000+ free requests/day)
"""

import streamlit as st
import os
import json
import hashlib
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

class GroqHelper:
    """Helper class for managing Groq AI interactions"""
    
    def __init__(self):
        self.client = None
        self.api_key = None
        self.model = "llama-3.3-70b-versatile"  # Groq's fastest, most capable model
        self.request_count = 0
        self.cache = {}
        self.is_available = False
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize the Groq client with API key"""
        try:
            # Get API key from various sources
            self.api_key = (
                os.getenv('GROQ_API_KEY') or 
                (st.secrets.get("GROQ_API_KEY", "") if hasattr(st, 'secrets') else "") or
                self.load_api_key_from_file()
            )
            
            if not self.api_key:
                st.warning("""
                ⚠️ **Groq API Key Not Found**
                
                To enable AI features:
                1. Get a free API key from [console.groq.com](https://console.groq.com)
                2. Add it to Streamlit Secrets: `GROQ_API_KEY = "your_key_here"`
                
                Free tier: 16,000+ requests/day with Llama 3.3 70B!
                """)
                self.is_available = False
                return False
            
            # Import Groq
            from groq import Groq
            
            # Initialize client
            self.client = Groq(api_key=self.api_key)
            
            # Test the connection
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Say 'OK' if you're working."}],
                max_tokens=5
            )
            
            if test_response and test_response.choices[0].message.content:
                self.is_available = True
                st.success("✅ AI Assistant is ready! (Powered by Groq/Llama 3.3)")
                return True
            else:
                self.is_available = False
                st.error("❌ Failed to connect to Groq API. Please check your API key.")
                return False
                
        except ImportError:
            self.is_available = False
            st.error("❌ Groq package not installed. Run: pip install groq")
            return False
        except Exception as e:
            self.is_available = False
            st.error(f"❌ Error initializing AI: {str(e)[:200]}")
            return False
    
    def load_api_key_from_file(self) -> str:
        """Load API key from .env file manually"""
        try:
            env_path = os.path.join(os.getcwd(), '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('GROQ_API_KEY='):
                            return line.split('=')[1].strip().strip('"').strip("'")
        except Exception:
            pass
        return ""
    
    def get_cache_key(self, prompt: str) -> str:
        """Generate a cache key for a prompt"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def generate_response(
        self, 
        prompt: str, 
        use_cache: bool = True,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        Generate a response from Groq AI with caching
        """
        if not self.is_available or not self.client:
            return self.get_fallback_response(prompt)
        
        # Check cache
        cache_key = self.get_cache_key(prompt)
        if use_cache and cache_key in self.cache:
            cache_time, response = self.cache[cache_key]
            if datetime.now() - cache_time < timedelta(hours=1):
                return response
        
        try:
            # Update request count
            self.request_count += 1
            
            # System prompt for child-friendly responses
            system_prompt = """You are Exam Buddy, a friendly AI tutor for a 9-year-old Class 4 student.
            Rules:
            - Use simple words (like explaining to a friend)
            - Add fun emojis (😊, 🌟, 📚, 🎯) 
            - Keep responses short (2-4 sentences when possible)
            - Be encouraging and positive
            - Use real-life examples"""
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=0.95
            )
            
            result = response.choices[0].message.content
            
            # Cache the result
            if use_cache:
                self.cache[cache_key] = (datetime.now(), result)
                if len(self.cache) > 100:
                    keys_to_remove = list(self.cache.keys())[:20]
                    for key in keys_to_remove:
                        del self.cache[key]
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "rate" in error_msg.lower() or "quota" in error_msg.lower():
                return "🔋 I've reached my daily limit! I'll be back tomorrow. Keep learning! 📚"
            elif "429" in error_msg:
                return "🔄 Too many requests! Please wait a moment and try again."
            else:
                return f"🤖 I'm having a little trouble. Let's try again! (Error: {error_msg[:100]})"
    
    def get_fallback_response(self, prompt: str) -> str:
        """Provide fallback responses when AI is unavailable"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
            return "👋 Hello! I'm your Exam Buddy! Add your Groq API key to Streamlit Secrets to unlock all my features! 🚀"
        
        elif any(word in prompt_lower for word in ['study', 'learn', 'help']):
            return "📚 Here are study tips:\n\n1. Read your chapter carefully\n2. Take notes as you read\n3. Practice with quizzes\n\nAdd your API key for personalized help! 🌟"
        
        elif any(word in prompt_lower for word in ['quiz', 'test', 'practice']):
            return "🏆 Try these:\n\n• Make flashcards\n• Answer chapter questions\n• Teach someone what you learned\n\nI can generate custom quizzes once my AI features are enabled! ✨"
        
        else:
            return "🤖 I'm Exam Buddy! To get AI tutoring:\n\n1. Get a free API key from console.groq.com\n2. Add it to Streamlit Secrets\n3. Restart the app\n\nFree tier: 16,000+ requests/day! 🎯"
    
    def summarize_content(self, content: str, for_child: bool = True) -> str:
        """Summarize educational content for better understanding"""
        if not self.is_available:
            sentences = content.split('.')[:3]
            return "📖 Quick summary:\n\n" + '. '.join(sentences) + "...\n\n💡 Add your Groq API key for AI summaries!"
        
        if for_child:
            prompt = f"Explain this to a 9-year-old in simple words with emojis and bullet points:\n\n{content[:800]}"
        else:
            prompt = f"Summarize this in 3 key points:\n\n{content[:800]}"
        
        return self.generate_response(prompt)
    
    def create_quiz_questions(self, content: str, num_questions: int = 3, difficulty: str = "easy") -> List[Dict]:
        """Create multiple choice quiz questions from content"""
        if not self.is_available:
            return []
        
        prompt = f"""
        Create {num_questions} multiple choice questions for Class 4 students based on:
        
        {content[:600]}
        
        Return ONLY valid JSON format. No other text.
        Example format:
        {{
            "questions": [
                {{
                    "question": "Question text?",
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "answer": "A",
                    "explanation": "Brief explanation for a 9-year-old"
                }}
            ]
        }}
        """
        
        response = self.generate_response(prompt, temperature=0.8, max_tokens=1000)
        
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return data.get('questions', [])
        except:
            pass
        
        return []
    
    def explain_concept(self, concept: str) -> str:
        """Explain a concept in a child-friendly way"""
        if not self.is_available:
            return f"📚 {concept} is interesting! Add your Groq API key for a fun, simple explanation! 🌟"
        
        return self.generate_response(f"Explain '{concept}' to a 9-year-old. Use an analogy or fun example. Keep it to 2-3 sentences.", temperature=0.9)
    
    def get_motivation(self) -> str:
        """Get a motivational message"""
        if not self.is_available:
            return "🌟 You're doing great! Keep learning every day!"
        
        return self.generate_response("Give a short, encouraging motivational message for a 9-year-old student. Use emojis. Keep it to 1 sentence.", temperature=1.0)
    
    def get_usage_stats(self) -> Dict:
        """Get AI usage statistics"""
        return {
            'total_requests': self.request_count,
            'cache_size': len(self.cache),
            'is_available': self.is_available,
            'model': self.model
        }

# Create a singleton instance
@st.cache_resource
def get_groq_helper():
    """Get or create the Groq helper instance"""
    return GroqHelper()

# For backwards compatibility with existing code
if 'groq_helper' not in st.session_state:
    st.session_state.groq_helper = get_groq_helper()
