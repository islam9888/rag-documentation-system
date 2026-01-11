"""
RAG Indexer - Vector Store Management
"""
import logging
from pathlib import Path
from typing import Optional, List

import chromadb
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    Settings
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq

from src.config import config

logger = logging.getLogger(__name__)


class RAGIndexer:
    """Manages document indexing and vector store"""
    
    def __init__(
        self,
        docs_path: Optional[Path] = None,
        vectorstore_path: Optional[Path] = None
    ):
        self.docs_path = docs_path or config.paths.raw_docs_path
        self.vectorstore_path = vectorstore_path or config.paths.vectorstore_path
        
        self.documents = []
        self.index = None
        self.chroma_client = None
        self.collection = None
        
        self._setup_models()
    
    def _setup_models(self):
        """Initialize embedding and LLM models"""
        logger.info("Setting up embedding model...")
        
        # Embedding model
        embed_model = HuggingFaceEmbedding(
            model_name=config.models.embedding_model
        )
        
        # LLM
        llm = Groq(
            model=config.models.llm_model,
            api_key=config.groq_api_key
        )
        
        # Configure settings
        Settings.embed_model = embed_model
        Settings.llm = llm
        Settings.chunk_size = config.models.chunk_size
        Settings.chunk_overlap = config.models.chunk_overlap
        
        logger.info("Models configured successfully")
    
    def load_documents(self) -> List:
        """
        Load documents from directory
        
        Returns:
            List of loaded documents
        """
        logger.info(f"Loading documents from {self.docs_path}")
        
        if not self.docs_path.exists():
            raise FileNotFoundError(f"Documents path not found: {self.docs_path}")
        
        try:
            reader = SimpleDirectoryReader(
                input_dir=str(self.docs_path),
                required_exts=[".txt"]
            )
            self.documents = reader.load_data()
            
            logger.info(f"Loaded {len(self.documents)} documents")
            return self.documents
            
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            raise
    
    def build_index(self, force_rebuild: bool = False) -> VectorStoreIndex:
        """
        Build or load vector store index
        
        Args:
            force_rebuild: Force rebuild even if index exists
            
        Returns:
            VectorStoreIndex instance
        """
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.vectorstore_path)
        )
        
        # Check if collection exists
        existing_collections = [c.name for c in self.chroma_client.list_collections()]
        collection_exists = "docs" in existing_collections
        
        if collection_exists and not force_rebuild:
            logger.info("Loading existing vector store...")
            self.collection = self.chroma_client.get_collection("docs")
            
            vector_store = ChromaVectorStore(chroma_collection=self.collection)
            self.index = VectorStoreIndex.from_vector_store(vector_store)
            
            logger.info("Vector store loaded successfully")
        else:
            if collection_exists:
                logger.info("Deleting existing collection for rebuild...")
                self.chroma_client.delete_collection("docs")
            
            logger.info("Building new vector store (this may take several minutes)...")
            
            # Load documents if not already loaded
            if not self.documents:
                self.load_documents()
            
            # Create new collection
            self.collection = self.chroma_client.get_or_create_collection("docs")
            
            # Build index
            vector_store = ChromaVectorStore(chroma_collection=self.collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            self.index = VectorStoreIndex.from_documents(
                self.documents,
                storage_context=storage_context,
                show_progress=True
            )
            
            logger.info("Vector store built and saved successfully")
        
        return self.index
    
    def get_stats(self) -> dict:
        """Get indexer statistics"""
        stats = {
            'documents_loaded': len(self.documents),
            'index_built': self.index is not None,
            'vectorstore_path': str(self.vectorstore_path)
        }
        
        if self.collection:
            stats['collection_count'] = self.collection.count()
        
        return stats