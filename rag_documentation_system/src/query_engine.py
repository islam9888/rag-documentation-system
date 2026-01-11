"""
Query Engine for RAG System
"""
import logging
from typing import List, Tuple, Optional, Dict
from datetime import datetime

from llama_index.core import VectorStoreIndex

from src.config import config

logger = logging.getLogger(__name__)


class QueryEngine:
    """Handles querying the RAG system"""
    
    def __init__(self, index: VectorStoreIndex):
        self.index = index
        self.engine = self._create_engine()
        self.query_history: List[Dict] = []
    
    def _create_engine(self):
        """Create query engine from index"""
        return self.index.as_query_engine(
            similarity_top_k=config.models.similarity_top_k
        )
    
    def query(
        self, 
        question: str,
        use_history: bool = False
    ) -> Tuple[str, List[str]]:
        """
        Query the RAG system
        
        Args:
            question: User question
            use_history: Include chat history in context
            
        Returns:
            Tuple of (answer, source_files)
        """
        try:
            # Build context with history if enabled
            context = self._build_context(question, use_history)
            
            # Query
            response = self.engine.query(context)
            answer = response.response
            
            # Extract sources
            sources = self._extract_sources(response)
            
            # Log query with timestamp
            self.query_history.append({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'question': question,
                'answer': answer,
                'sources': sources
            })
            
            logger.info(f"Query processed: {question[:50]}...")
            return answer, sources
            
        except Exception as e:
            logger.error(f"Query error: {e}")
            return f"Error processing query: {str(e)}", []
    
    def _build_context(self, question: str, use_history: bool) -> str:
        """Build context with optional history"""
        if not use_history or len(self.query_history) == 0:
            return question
        
        # Include last 2 Q&A pairs for context
        context = "Previous conversation:\n"
        for qa in self.query_history[-2:]:
            context += f"Q: {qa['question']}\n"
            context += f"A: {qa['answer'][:200]}...\n\n"
        
        context += f"Current question: {question}"
        return context
    
    def _extract_sources(self, response) -> List[str]:
        """Extract source filenames from response"""
        sources = []
        
        if hasattr(response, 'source_nodes'):
            for node in response.source_nodes:
                filename = node.metadata.get('file_name', 'Unknown')
                if filename not in sources:
                    sources.append(filename)
        
        return sources
    
    def format_response(
        self, 
        answer: str, 
        sources: List[str],
        include_sources: bool = True
    ) -> str:
        """
        Format response with sources
        
        Args:
            answer: Answer text
            sources: List of source files
            include_sources: Whether to include sources
            
        Returns:
            Formatted response string
        """
        formatted = answer
        
        if include_sources and sources:
            formatted += "\n\n📚 **Sources:**\n"
            for i, source in enumerate(sources[:3], 1):
                formatted += f"{i}. {source}\n"
        
        return formatted
    
    def clear_history(self):
        """Clear query history"""
        self.query_history = []
        logger.info("Query history cleared")
    
    def get_history(self) -> List[Dict]:
        """Get query history"""
        return self.query_history
