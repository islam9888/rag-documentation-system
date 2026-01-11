"""
Utility Functions for RAG System
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file to write logs to
        
    Returns:
        Configured logger instance
    """
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def validate_api_key(api_key: Optional[str]) -> bool:
    """
    Validate API key format
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not api_key:
        return False
    
    # Basic validation (Groq keys start with 'gsk_')
    if api_key.startswith('gsk_') and len(api_key) > 20:
        return True
    
    return False


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_project_root() -> Path:
    """Get project root directory"""
    return Path(__file__).parent.parent


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def export_chat_history(history: list, output_path: Path) -> Path:
    """
    Export chat history to text file
    
    Args:
        history: List of chat history dicts
        output_path: Path to save file
        
    Returns:
        Path to saved file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"chat_export_{timestamp}.txt"
    filepath = output_path / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        for i, item in enumerate(history, 1):
            f.write(f"## Q{i}: {item['question']}\n\n")
            f.write(f"{item['answer']}\n\n")
            
            if item.get('sources'):
                f.write("**Sources:**\n")
                for source in item['sources']:
                    f.write(f"- {source}\n")
            
            f.write("\n---\n\n")
    
    return filepath


def count_tokens_estimate(text: str) -> int:
    """
    Rough estimate of token count
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    # Rough estimation: ~4 characters per token
    return len(text) // 4


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to max length
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."