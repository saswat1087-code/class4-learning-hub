"""
Utils Package Initialization
Makes utility modules easily importable throughout the application
"""

from utils.data_manager import DataManager, get_data_manager, data_manager
from utils.gemini_helper import GeminiHelper, get_gemini_helper

# Package metadata
__version__ = "1.0.0"
__author__ = "Class 4 Learning Hub"
__description__ = "Utility modules for Class 4 Learning Platform"

# Convenience function to initialize all utilities
def initialize_utilities():
    """
    Initialize all utility modules and ensure they're ready for use
    Returns tuple of (data_manager, gemini_helper)
    """
    try:
        # Initialize data manager
        dm = get_data_manager()
        
        # Initialize gemini helper
        gh = get_gemini_helper()
        
        return dm, gh
    except Exception as e:
        print(f"Error initializing utilities: {e}")
        return None, None

# Export commonly used functions and classes
__all__ = [
    'DataManager',
    'get_data_manager',
    'data_manager',
    'GeminiHelper',
    'get_gemini_helper',
    'initialize_utilities'
]

# Package-level docstring
"""
Class 4 Learning Hub - Utility Modules
======================================

This package contains helper modules for:
- data_manager: Handles user progress tracking, achievements, and data persistence
- gemini_helper: Manages AI interactions with Google's Gemini API

Usage:
    from utils import data_manager, gemini_helper
    
    # Track progress
    data_manager.award_points(50, "Completed quiz!")
    
    # Get AI help
    response = gemini_helper.generate_response("Explain photosynthesis")
"""
