"""
Gemini AI Helper Module - Updated for Gemini 2.0
Handles all interactions with Google's Gemini AI for the Class 4 Learning Hub
"""

import streamlit as st
import os
import json
import hashlib
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiHelper:
    """Helper class for managing Gemini AI interactions"""
    
    def __init__(self):
        """Initialize the Gemini client with API key management"""
        self.model = None
        self.api_key = None
        self.request_count = 0
        self.last_request_time = None
        self.cache = {}
        self.is_available = False
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize the Gemini client with API key from various sources"""
        try:
            # Try to get API key from multiple sources
            self.api_key = (
                os.getenv('GEMINI_API_KEY') or 
                (st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, 'secrets') else "") or
                self.load_api_key_from_file()
            )
            
            if not self.api_key:
                st.warning("""
                ⚠️ **Gemini API Key Not Found**
                
                To enable AI features:
                1. Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey)
                2. Add it to Streamlit Secrets: `GEMINI_API_KEY = "your_key_here"`
                
                The app will work in limited mode without AI features.
                """)
                self.is_available = False
                return False
            
            import google.generativeai as genai
            
            # Configure the API key
            genai.configure(api_key=self.api_key)
            
            # UPDATED: Use gemini-2.0-flash (replaces discontinued 1.5-flash)
            # Alternative options: gemini-2.5-flash, gemini-3.5-flash
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Test the connection
            test_response = self.model.generate_content("Say 'OK' if you're working.")
            if test_response and test_response.text:
                self.is_available = True
                st.success("✅ AI Assistant is ready to help!")
                return True
            else:
                self.is_available = False
                st.error("❌ Failed to connect to AI service. Please check your API key.")
                return False
                
        except ImportError as e:
            self.is_available = False
            st.error(f"❌ Google Generative AI package not installed. Run: pip install google-generativeai>=0.8.0")
            return False
        except Exception as e:
            self.is_available = False
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                st.error("❌ Model not available. Please check your API key or try a different model.")
            else:
                st.error(f"❌ Error initializing AI: {error_msg[:200]}")
            return False
    
    def load_api_key_from_file(self) -> str:
        """Load API key from .env file manually"""
        try:
            env_path = os.path.join(os.getcwd(), '.env')
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('GEMINI_API_KEY='):
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
        Generate a response from Gemini AI with caching and rate limiting
        """
        if not self.is_available or not self.model:
            return self.get_fallback_response(prompt)
        
        # Check cache
        cache_key = self.get_cache_key(prompt)
        if use_cache and cache_key in self.cache:
            cache_time, response = self.cache[cache_key]
            if datetime.now() - cache_time < timedelta(hours=1):
                return response
        
        try:
            # Update rate limiting stats
            self.request_count += 1
            self.last_request_time = datetime.now()
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                    'top_p': 0.95,
                    'top_k': 40,
                }
            )
            
            result = response.text if response and response.text else "I couldn't generate a response. Please try again."
            
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
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                return "🔋 I've reached my daily limit! I'll be back tomorrow. Keep learning! 📚"
            elif "safety" in error_msg.lower() or "blocked" in error_msg.lower():
                return "🤔 I need to be careful with that question. Could you ask it differently?"
            elif "404" in error_msg:
                return "🤖 Model temporarily unavailable. Please try again in a few minutes."
            else:
                return f"🤖 I'm having a little trouble. Let's try something else! (Error: {error_msg[:100]})"
    
    def get_fallback_response(self, prompt: str) -> str:
        """Provide fallback responses when AI is unavailable"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
            return "👋 Hello! I'm your Exam Buddy! To use all my AI features, please add a valid Gemini API key to Streamlit Secrets. 🌟"
        
        elif any(word in prompt_lower for word in ['study', 'learn', 'help']):
            return "📚 Here are study tips:\n\n1. Read your chapter carefully\n2. Take notes as you read\n3. Practice with quizzes\n4. Ask questions when stuck\n\nAdd your API key for personalized help! 🚀"
        
        elif any(word in prompt_lower for word in ['quiz', 'test', 'practice']):
            return "🏆 Try these:\n\n• Make flashcards\n• Answer chapter questions\n• Teach someone what you learned\n\nI can generate custom quizzes once my AI features are enabled! ✨"
        
        else:
            return "🤖 I'm your Exam Buddy! To get full AI tutoring:\n\n1. Get a free Gemini API key from Google AI Studio\n2. Add it to Streamlit Secrets\n3. Restart the app\n\nThen I can answer any question and help you study better! 🚀"
    
    def summarize_content(self, content: str, for_child: bool = True) -> str:
        """Summarize educational content for better understanding"""
        if not self.is_available:
            sentences = content.split('.')[:3]
            return "📖 Quick summary:\n\n" + '. '.join(sentences) + "...\n\n💡 Add your Gemini API key for AI summaries!"
        
        if for_child:
            prompt = f"""
            Explain this Class 4 topic to a 9-year-old:
            
            {content[:800]}
            
            Rules:
            - Use simple words
            - Add fun emojis
            - Use 3-4 bullet points
            - Give 1 real-life example
            
            Start with "Here's what you need to know!"
            """
        else:
            prompt = f"Create a concise summary of this topic:\n\n{content[:800]}"
        
        return self.generate_response(prompt)
    
    def create_quiz_questions(self, content: str, num_questions: int = 3, difficulty: str = "easy") -> List[Dict]:
        """Create multiple choice quiz questions from content"""
        if not self.is_available:
            return []
        
        prompt = f"""
        Create {num_questions} multiple choice questions for Class 4 students based on:
        
        {content[:600]}
        
        Return ONLY valid JSON format:
        {{
            "questions": [
                {{
                    "question": "Question text?",
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "answer": "A",
                    "explanation": "Brief explanation"
                }}
            ]
        }}
        """
        
        response = self.generate_response(prompt, temperature=0.8)
        
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
            return f"📚 {concept} is interesting! Add your Gemini API key for a fun, simple explanation! 🌟"
        
        prompt = f"Explain {concept} to a 9-year-old. Use emojis and keep it to 2-3 sentences."
        return self.generate_response(prompt, temperature=0.9)
    
    def get_motivation(self) -> str:
        """Get a motivational message"""
        if not self.is_available:
            return "🌟 You're doing great! Keep learning every day!"
        
        return self.generate_response("Give a short encouraging message for a 9-year-old student. Use emojis. Keep it to 1 sentence.", temperature=1.0)
    
    def get_usage_stats(self) -> Dict:
        """Get AI usage statistics"""
        return {
            'total_requests': self.request_count,
            'cache_size': len(self.cache),
            'is_available': self.is_available,
            'last_request': self.last_request_time
        }

# Create a singleton instance
@st.cache_resource
def get_gemini_helper():
    """Get or create the Gemini helper instance"""
    return GeminiHelper()

# For backwards compatibility
if 'gemini_helper' not in st.session_state:
    st.session_state.gemini_helper = get_gemini_helper()
