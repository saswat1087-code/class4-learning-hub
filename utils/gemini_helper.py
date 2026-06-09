"""
Gemini AI Helper Module
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
                1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
                2. Create a `.env` file with: `GEMINI_API_KEY=your_key_here`
                3. Or add to Streamlit secrets when deploying
                
                The app will work in limited mode without AI features.
                """)
                self.is_available = False
                return False
            
            # CORRECT IMPORT SYNTAX for Google Gemini AI
            import google.generativeai as genai
            
            # Configure the API key
            genai.configure(api_key=self.api_key)
            
            # Initialize the model
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Test the connection
            test_response = self.test_connection()
            if test_response:
                self.is_available = True
                st.success("✅ AI Assistant is ready to help!")
                return True
            else:
                self.is_available = False
                st.error("❌ Failed to connect to AI service. Please check your API key.")
                return False
                
        except ImportError as e:
            self.is_available = False
            st.error(f"❌ Google Generative AI package not installed. Run: pip install google-generativeai")
            return False
        except Exception as e:
            self.is_available = False
            st.error(f"❌ Error initializing AI: {str(e)}")
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
    
    def test_connection(self) -> bool:
        """Test if the API connection is working"""
        try:
            response = self.model.generate_content("Say 'OK' if you're working.")
            return response and len(response.text) > 0
        except Exception:
            return False
    
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
        
        Args:
            prompt: The prompt to send to AI
            use_cache: Whether to use cached responses
            temperature: Creativity level (0-1)
            max_tokens: Maximum response length
        
        Returns:
            AI generated response string
        """
        # Check if client is available
        if not self.is_available or not self.model:
            return self.get_fallback_response(prompt)
        
        # Check cache
        cache_key = self.get_cache_key(prompt)
        if use_cache and cache_key in self.cache:
            cache_time, response = self.cache[cache_key]
            # Cache for 1 hour
            if datetime.now() - cache_time < timedelta(hours=1):
                return response
        
        # Rate limiting (max 10 requests per second)
        if self.last_request_time:
            time_diff = datetime.now() - self.last_request_time
            if time_diff.total_seconds() < 0.1:
                import time
                time.sleep(0.1)
        
        try:
            # Update rate limiting stats
            self.request_count += 1
            self.last_request_time = datetime.now()
            
            # Generate response with specified parameters
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
            
            # Limit cache size
            if len(self.cache) > 100:
                keys_to_remove = list(self.cache.keys())[:20]
                for key in keys_to_remove:
                    del self.cache[key]
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                return "🔋 I've reached my daily limit! I'll be back tomorrow. Keep learning with the offline materials! 📚"
            elif "safety" in error_msg.lower() or "blocked" in error_msg.lower():
                return "🤔 I need to be careful with that question. Could you ask it differently?"
            else:
                return f"🤖 I'm having a little trouble thinking right now. Let's try something else! (Error: {error_msg[:100]})"
    
    def get_fallback_response(self, prompt: str) -> str:
        """Provide fallback responses when AI is unavailable"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['hello', 'hi', 'hey']):
            return "👋 Hello! I'm your Exam Buddy! I'd love to help you learn, but my AI brain needs an API key to work fully. Ask your parent to add the Gemini API key to unlock all my features! 🌟"
        
        elif any(word in prompt_lower for word in ['study', 'learn', 'help']):
            return "📚 I'm here to help you study! Here are some tips:\n\n1. Read your chapter carefully\n2. Take notes as you read\n3. Practice with quizzes\n4. Ask questions when stuck\n\nWant me to explain a specific topic? Get my AI features working by adding the API key! 🚀"
        
        elif any(word in prompt_lower for word in ['quiz', 'test', 'practice']):
            return "🏆 Quizzes are great for learning! Try these:\n\n• Make flashcards\n• Answer questions at the end of chapters\n• Teach what you learned to someone else\n\nI can generate custom quizzes once my AI features are enabled! ✨"
        
        elif any(word in prompt_lower for word in ['math', 'multiplication', 'addition']):
            return "🧮 Math is fun! Here's a practice problem:\n\nWhat is 25 × 4?\n\n(Hint: Think 20×4 + 5×4)\n\nWant more practice? I can make custom worksheets when my AI is active! ➗"
        
        elif any(word in prompt_lower for word in ['science', 'plant', 'animal']):
            return "🔬 Science is amazing! Did you know? Plants make their own food through photosynthesis! 🌱\n\nI can explain more science topics once my AI features are connected! 🌟"
        
        else:
            return "🤖 I'm your Exam Buddy! Right now I'm in basic mode. To get full AI tutoring:\n\n1. Get a free Gemini API key from Google AI Studio\n2. Add it to your .env file or Streamlit secrets\n3. Restart the app\n\nThen I can answer any question, create quizzes, and help you study better! 🚀"
    
    def summarize_content(self, content: str, for_child: bool = True) -> str:
        """Summarize educational content for better understanding"""
        if not self.is_available:
            sentences = content.split('.')[:3]
            return "📖 Here's a quick summary:\n\n" + '. '.join(sentences) + "...\n\n💡 For a better summary, please add your Gemini API key!"
        
        if for_child:
            prompt = f"""
            Explain this Class 4 topic to a 9-year-old:
            
            {content}
            
            Rules:
            - Use simple words (no big vocabulary)
            - Add fun emojis (😊, 🌟, 📚, 🎯)
            - Use 3-4 bullet points
            - Give 1 real-life example
            - Make it encouraging and fun
            
            Start with "Here's what you need to know!"
            """
        else:
            prompt = f"""
            Create a concise summary of this Class 4 topic:
            
            {content}
            
            Format:
            - Key points (3-5 bullets)
            - Important terms with definitions
            - 1 practice question
            
            Keep it clear and educational.
            """
        
        return self.generate_response(prompt)
    
    def create_quiz_questions(self, content: str, num_questions: int = 5, difficulty: str = "easy") -> List[Dict]:
        """Create multiple choice quiz questions from content"""
        if not self.is_available:
            return [
                {
                    "question": "What is the main topic of this chapter?",
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "answer": "A",
                    "explanation": "Please add your Gemini API key to get custom quiz questions!"
                }
            ]
        
        prompt = f"""
        Create {num_questions} {difficulty} multiple choice questions for Class 4 students based on:
        
        {content}
        
        Format EXACTLY as JSON:
        {{
            "questions": [
                {{
                    "question": "What is the question?",
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "answer": "A",
                    "explanation": "Explanation here"
                }}
            ]
        }}
        
        Make questions fun and engaging. Use emojis in questions.
        Return ONLY valid JSON, no other text.
        """
        
        response = self.generate_response(prompt, temperature=0.8)
        
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                return data.get('questions', [])
        except:
            pass
        
        return []
    
    def explain_concept(self, concept: str) -> str:
        """Explain a concept in a child-friendly way"""
        if not self.is_available:
            return f"📚 {concept} is an interesting topic! I'd love to explain it to you, but my AI features need an API key to work. Ask your parent to add the Gemini API key! 🌟"
        
        prompt = f"""
        Explain this concept to a 9-year-old Class 4 student: {concept}
        
        Make it:
        - Simple (like explaining to a friend)
        - Fun (use emojis and excitement)
        - Memorable (use an analogy or story)
        - Short (3-4 sentences maximum)
        
        Start with "Great question!" or "Here's something cool!"
        """
        
        return self.generate_response(prompt, temperature=0.9)
    
    def get_motivation(self) -> str:
        """Get a motivational message for the student"""
        if not self.is_available:
            messages = [
                "🌟 You're doing great! Keep learning every day!",
                "💪 Every expert was once a beginner. Keep going!",
                "📚 The more you read, the more you know!"
            ]
            import random
            return random.choice(messages)
        
        prompt = """
        Give a short, encouraging motivational message for a Class 4 student.
        Use emojis, be positive. Keep it to 1 sentence.
        """
        
        return self.generate_response(prompt, temperature=1.0)
    
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
