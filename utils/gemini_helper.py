"""
Gemini AI Helper Module
Handles all interactions with Google's Gemini AI for the Class 4 Learning Hub
"""

import streamlit as st
import os
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiHelper:
    """Helper class for managing Gemini AI interactions"""
    
    def __init__(self):
        """Initialize the Gemini client with API key management"""
        self.client = None
        self.api_key = None
        self.request_count = 0
        self.last_request_time = None
        self.cache = {}
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize the Gemini client with API key from various sources"""
        try:
            # Try to get API key from multiple sources
            self.api_key = (
                os.getenv('GEMINI_API_KEY') or 
                st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, 'secrets') else "" or
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
                return False
            
            # Import here to avoid dependency issues
            from google import genai
            
            # Initialize client
            self.client = genai.Client(api_key=self.api_key)
            
            # Test the connection
            test_response = self.test_connection()
            if test_response:
                st.success("✅ AI Assistant is ready to help!")
                return True
            else:
                st.error("❌ Failed to connect to AI service. Please check your API key.")
                return False
                
        except ImportError:
            st.error("❌ Google Generative AI package not installed. Run: pip install google-generativeai")
            return False
        except Exception as e:
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
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents="Say 'OK' if you're working."
            )
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
        if not self.client:
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
            if time_diff.total_seconds() < 0.1:  # 100ms between requests
                import time
                time.sleep(0.1)
        
        try:
            # Update rate limiting stats
            self.request_count += 1
            self.last_request_time = datetime.now()
            
            # Generate response with specified parameters
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
                config={
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                }
            )
            
            result = response.text if response else "I couldn't generate a response. Please try again."
            
            # Cache the result
            if use_cache:
                self.cache[cache_key] = (datetime.now(), result)
            
            # Limit cache size
            if len(self.cache) > 100:
                # Remove oldest 20 entries
                keys_to_remove = list(self.cache.keys())[:20]
                for key in keys_to_remove:
                    del self.cache[key]
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower():
                return "🔋 I've reached my daily limit! I'll be back tomorrow. Keep learning with the offline materials! 📚"
            elif "safety" in error_msg.lower():
                return "🤔 I need to be careful with that question. Could you ask it differently?"
            else:
                return f"🤖 I'm having a little trouble thinking right now. Let's try something else! (Error: {error_msg[:100]})"
    
    def get_fallback_response(self, prompt: str) -> str:
        """Provide fallback responses when AI is unavailable"""
        prompt_lower = prompt.lower()
        
        # Keyword-based fallback responses
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
            return "🤖 I'm your Exam Buddy! Right now I'm in basic mode. To get full AI tutoring:\n\n1. Get a free Gemini API key from Google AI Studio\n2. Add it to your .env file\n3. Restart the app\n\nThen I can answer any question, create quizzes, and help you study better! 🚀"
    
    def summarize_content(self, content: str, for_child: bool = True) -> str:
        """Summarize educational content for better understanding"""
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
            
            Start with "Here's what you need to know, [Student Name]!"
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
    
    def create_quiz_questions(
        self, 
        content: str, 
        num_questions: int = 5,
        difficulty: str = "easy"
    ) -> List[Dict]:
        """
        Create multiple choice quiz questions from content
        
        Returns:
            List of question dictionaries with keys: question, options, answer, explanation
        """
        prompt = f"""
        Create {num_questions} {difficulty} multiple choice questions for Class 4 students based on:
        
        {content}
        
        Format as JSON:
        {{
            "questions": [
                {{
                    "question": "What is ...?",
                    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                    "answer": "A",
                    "explanation": "Simple explanation for a 9-year-old"
                }}
            ]
        }}
        
        Make questions fun and engaging. Use emojis in questions. Ensure answers are clear.
        """
        
        response = self.generate_response(prompt, temperature=0.8)
        
        # Try to parse JSON response
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
                return data.get('questions', [])
        except:
            pass
        
        # Return empty list if parsing fails
        return []
    
    def explain_concept(self, concept: str) -> str:
        """Explain a concept in a child-friendly way"""
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
    
    def generate_study_tips(self, subject: str = None) -> str:
        """Generate study tips for a specific subject or general"""
        if subject:
            prompt = f"""
            Give 3 specific study tips for a Class 4 student learning {subject}.
            Make each tip:
            - Actionable (something they can do today)
            - Fun (add emojis)
            - Age-appropriate
            
            Format as bullet points with emojis.
            """
        else:
            prompt = """
            Give 5 general study tips for a Class 4 student.
            Make them:
            - Easy to remember
            - Fun (use emojis)
            - Practical for daily use
            
            Start with "Here are your study superpowers for today!"
            """
        
        return self.generate_response(prompt, temperature=0.8)
    
    def check_answer(self, question: str, user_answer: str, correct_answer: str) -> Dict:
        """
        Check if answer is correct and provide feedback
        
        Returns:
            Dictionary with keys: is_correct, feedback, points_earned
        """
        prompt = f"""
        Question: {question}
        Student's answer: {user_answer}
        Correct answer: {correct_answer}
        
        Analyze if the student is correct. Provide:
        1. Is it correct? (yes/no)
        2. Encouraging feedback (1 sentence)
        3. Points to award (5 if correct, 2 if incorrect but good try)
        
        Format as JSON: {{"is_correct": "yes/no", "feedback": "text", "points": number}}
        """
        
        response = self.generate_response(prompt, temperature=0.5)
        
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                result = json.loads(json_str)
                return {
                    'is_correct': result.get('is_correct', 'no').lower() == 'yes',
                    'feedback': result.get('feedback', 'Keep trying!'),
                    'points': result.get('points', 2)
                }
        except:
            pass
        
        # Default response
        return {
            'is_correct': False,
            'feedback': "Keep practicing! You'll get it next time! 🌟",
            'points': 2
        }
    
    def get_motivation(self) -> str:
        """Get a motivational message for the student"""
        prompt = """
        Give a short, encouraging motivational message for a Class 4 student who is studying.
        Use emojis, be positive, and make it feel like a high-five from a friend.
        Keep it to 1 sentence.
        """
        
        return self.generate_response(prompt, temperature=1.0)
    
    def create_flashcards(self, content: str, num_cards: int = 5) -> List[Tuple[str, str]]:
        """
        Create flashcards from content
        
        Returns:
            List of (term, definition) tuples
        """
        prompt = f"""
        Create {num_cards} flashcards for Class 4 students based on:
        
        {content}
        
        Format each flashcard as:
        TERM: [important word/concept]
        DEFINITION: [simple definition for 9-year-old]
        
        Separate each flashcard with "---"
        """
        
        response = self.generate_response(prompt)
        
        flashcards = []
        if "---" in response:
            cards = response.split("---")
            for card in cards[:num_cards]:
                if "TERM:" in card and "DEFINITION:" in card:
                    term = card.split("TERM:")[1].split("DEFINITION:")[0].strip()
                    definition = card.split("DEFINITION:")[1].strip()
                    flashcards.append((term, definition))
        
        return flashcards if flashcards else [("Keep practicing!", "You're doing great! 🌟")]
    
    def get_usage_stats(self) -> Dict:
        """Get AI usage statistics"""
        return {
            'total_requests': self.request_count,
            'cache_size': len(self.cache),
            'is_available': self.client is not None,
            'last_request': self.last_request_time
        }

# Create a singleton instance
@st.cache_resource
def get_gemini_helper():
    """Get or create the Gemini helper instance"""
    return GeminiHelper()

# For backwards compatibility
st.session_state.gemini_helper = get_gemini_helper()
