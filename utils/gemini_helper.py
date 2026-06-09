"""
LLM Helper Module - Supports Groq, Mistral, or OpenAI-compatible APIs
"""

import streamlit as st
import os
from openai import OpenAI

class LLMHelper:
    def __init__(self):
        self.client = None
        self.model = "llama-3.3-70b-versatile"  # Groq's Llama 3.3 70B model
        self.is_available = False
        self.initialize_client()
    
    def initialize_client(self):
        """Initialize the Groq/OpenAI compatible client"""
        try:
            # Get API key from Streamlit secrets or environment
            api_key = (
                os.getenv('GROQ_API_KEY') or 
                st.secrets.get("GROQ_API_KEY", "")
            )
            
            if not api_key:
                st.warning("⚠️ GROQ_API_KEY not found. Please add it to Streamlit Secrets.")
                self.is_available = False
                return False
            
            # Initialize Groq client (OpenAI-compatible)
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            
            # Test the connection
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Say OK"}],
                max_tokens=5
            )
            
            if test_response:
                self.is_available = True
                st.success("✅ AI Assistant is ready (powered by Groq/Llama)!")
                return True
                
        except ImportError:
            st.error("❌ OpenAI package not installed. Run: pip install openai")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
        
        self.is_available = False
        return False
    
    def generate_response(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate a response using Groq's Llama model"""
        if not self.is_available or not self.client:
            return self.get_fallback_response(prompt)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a friendly AI tutor for a 9-year-old. Use simple words, emojis, and be encouraging."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"🤖 Error: {str(e)[:100]}"
    
    def get_fallback_response(self, prompt: str) -> str:
        """Fallback when AI is unavailable"""
        return "🌟 AI assistant is ready! Please add your GROQ_API_KEY to Streamlit Secrets."

# Create singleton
@st.cache_resource
def get_llm_helper():
    return LLMHelper()

if 'llm_helper' not in st.session_state:
    st.session_state.llm_helper = get_llm_helper()
