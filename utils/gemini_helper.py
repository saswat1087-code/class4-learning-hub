"""
Gemini AI Helper Module - DEBUG VERSION
This version will show you exactly what's wrong
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
        
        # DEBUG: Show what we're doing
        st.info("🔧 Initializing AI Assistant...")
        
        try:
            # Try to get API key from multiple sources
            self.api_key = (
                os.getenv('GEMINI_API_KEY') or 
                (st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, 'secrets') else "") or
                self.load_api_key_from_file()
            )
            
            # DEBUG: Check if we found a key
            if self.api_key:
                st.write(f"✅ API Key found! Length: {len(self.api_key)} characters")
                st.write(f"📝 First 10 chars: {self.api_key[:10]}...")
                st.write(f"📝 Last 5 chars: ...{self.api_key[-5:]}")
            else:
                st.error("❌ NO API KEY FOUND in any source!")
                st.write("Checked sources:")
                st.write(f"  - Environment variable: {'Yes' if os.getenv('GEMINI_API_KEY') else 'No'}")
                st.write(f"  - Streamlit secrets: {'Yes' if hasattr(st, 'secrets') and st.secrets.get('GEMINI_API_KEY') else 'No'}")
                st.write(f"  - .env file: {'Yes' if self.load_api_key_from_file() else 'No'}")
                self.is_available = False
                return False
            
            # Try to import the package
            st.info("📦 Importing google.generativeai...")
            import google.generativeai as genai
            st.success("✅ Package imported successfully!")
            
            # Configure the API key
            st.info("🔑 Configuring API key...")
            genai.configure(api_key=self.api_key)
            st.success("✅ API key configured!")
            
            # Initialize the model
            st.info("🤖 Creating model instance...")
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            st.success("✅ Model created!")
            
            # Test the connection
            st.info("🔄 Testing connection to Gemini API...")
            try:
                test_response = self.model.generate_content("Say 'OK'")
                if test_response and test_response.text:
                    st.success(f"✅ Test successful! Response: {test_response.text}")
                    self.is_available = True
                    return True
                else:
                    st.error("❌ Test failed: Empty response")
                    self.is_available = False
                    return False
            except Exception as test_error:
                st.error(f"❌ Test failed: {str(test_error)}")
                self.is_available = False
                return False
                
        except ImportError as e:
            self.is_available = False
            st.error(f"❌ Import Error: {str(e)}")
            st.info("Run: pip install google-generativeai")
            return False
        except Exception as e:
            self.is_available = False
            st.error(f"❌ General Error: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            return False
    
    def load_api_key_from_file(self) -> str:
        """Load API key from .env file manually"""
        try:
            env_path = os.path.join(os.getcwd(), '.env')
            st.write(f"Looking for .env at: {env_path}")
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('GEMINI_API_KEY='):
                            key = line.split('=')[1].strip().strip('"').strip("'")
                            return key
        except Exception as e:
            st.write(f"Error reading .env: {e}")
        return ""
    
    def generate_response(self, prompt: str, use_cache: bool = True, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Generate a response from Gemini AI"""
        if not self.is_available or not self.model:
            return "🤖 AI Assistant is not available. Please check the errors above."
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': temperature,
                    'max_output_tokens': max_tokens,
                }
            )
            return response.text if response and response.text else "I couldn't generate a response."
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_fallback_response(self, prompt: str) -> str:
        return "AI Assistant is initializing. Please wait or check the debug messages above."
    
    def summarize_content(self, content: str, for_child: bool = True) -> str:
        if not self.is_available:
            return "AI not available. Check debug messages above."
        prompt = f"Summarize this for a 9-year-old: {content}"
        return self.generate_response(prompt)
    
    def create_quiz_questions(self, content: str, num_questions: int = 5, difficulty: str = "easy") -> List[Dict]:
        return []
    
    def explain_concept(self, concept: str) -> str:
        if not self.is_available:
            return "AI not available."
        return self.generate_response(f"Explain {concept} to a 9-year-old")
    
    def get_motivation(self) -> str:
        return "🌟 Keep learning! 🌟"

# Create a singleton instance
@st.cache_resource
def get_gemini_helper():
    return GeminiHelper()

if 'gemini_helper' not in st.session_state:
    st.session_state.gemini_helper = get_gemini_helper()
