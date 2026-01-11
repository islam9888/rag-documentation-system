"""
Configuration Management for RAG Documentation System
"""
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ModelConfig:
    """LLM and Embedding model configuration"""
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    llm_model: str = "llama-3.3-70b-versatile"
    chunk_size: int = 512
    chunk_overlap: int = 128
    similarity_top_k: int = 3


@dataclass
class PathConfig:
    """File and directory paths"""
    base_path: Path
    data_path: Path
    raw_docs_path: Path
    processed_path: Path
    vectorstore_path: Path
    
    @classmethod
    def from_base(cls, base_path: str):
        base = Path(base_path)
        return cls(
            base_path=base,
            data_path=base / "data",
            raw_docs_path=base / "data" / "raw_docs",
            processed_path=base / "data" / "processed",
            vectorstore_path=base / "vectorstore"
        )
    
    def create_directories(self):
        """Create all necessary directories"""
        for path in [self.data_path, self.raw_docs_path, 
                     self.processed_path, self.vectorstore_path]:
            path.mkdir(parents=True, exist_ok=True)


@dataclass
class ScraperConfig:
    """Web scraper configuration"""
    timeout: int = 10
    delay_between_requests: float = 0.5
    min_text_length: int = 200
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


class Config:
    """Main configuration class"""
    
    def __init__(self, base_path: Optional[str] = None):
        # API Keys
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        # Paths
        if base_path is None:
            base_path = os.getenv("BASE_PATH", "./rag_project")
        self.paths = PathConfig.from_base(base_path)
        
        # Models
        self.models = ModelConfig()
        
        # Scraper
        self.scraper = ScraperConfig()
    
    def setup(self):
        """Setup configuration (create directories, etc.)"""
        self.paths.create_directories()
        return self


# Default configuration instance
config = Config()