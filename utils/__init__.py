"""
Utils Package Initialization
Makes utility modules easily importable throughout the application
"""

from utils.data_manager import DataManager, get_data_manager, data_manager
from utils.groq_helper import GroqHelper, get_groq_helper

# For backwards compatibility with existing code that expects gemini_helper
# This creates an alias so old code still works
try:
    from utils.groq_helper import GroqHelper as GeminiHelper
    from utils.groq_helper import get_groq_helper as get_gemini_helper
except ImportError:
    pass

# Package metadata
__version__ = "2.0.0"
__author__ = "Class 4 Learning Hub"
__description__ = "Utility modules for Class 4 Learning Platform"

# Convenience function to initialize all utilities
def initialize_utilities():
    """
    Initialize all utility modules and ensure they're ready for use
    Returns tuple of (data_manager, groq_helper)
    """
    try:
        # Initialize data manager
        dm = get_data_manager()
        
        # Initialize groq helper
        gh = get_groq_helper()
        
        return dm, gh
    except Exception as e:
        print(f"Error initializing utilities: {e}")
        return None, None

# Export commonly used functions and classes
__all__ = [
    'DataManager',
    'get_data_manager',
    'data_manager',
    'GroqHelper',
    'get_groq_helper',
    'GeminiHelper',  # Alias for compatibility
    'get_gemini_helper',  # Alias for compatibility
    'initialize_utilities'
]
