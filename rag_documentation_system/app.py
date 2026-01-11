"""
Hugging Face Spaces Entry Point
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the Gradio app
from app.gradio_app import main

if __name__ == "__main__":
    main()
