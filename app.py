import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Class 4 Learning Hub | AI-Powered Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import utilities (using updated imports)
from utils.data_manager import data_manager
from utils.groq_helper import get_groq_helper

# Initialize helpers
groq_helper = get_groq_helper()

# Rest of your app.py remains the same...
# (Keep your existing app.py content, just remove any references to gemini_helper)

st.title("Class 4 Learning Hub")
st.write("Welcome! Your AI-powered learning platform is ready.")
