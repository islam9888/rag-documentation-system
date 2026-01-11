"""
Script to build RAG index from documents
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.indexer import RAGIndexer
from src.utils import setup_logging

logger = setup_logging(log_level="INFO")


def main():
    """Build the RAG index"""
    print("="*60)
    print("🏗️  RAG INDEX BUILDER")
    print("="*60)
    
    # Setup config
    config.setup()
    print(f"\n📂 Documents: {config.paths.raw_docs_path}")
    print(f"📂 Vector store: {config.paths.vectorstore_path}")
    
    # Initialize indexer
    print("\n🔧 Initializing indexer...")
    indexer = RAGIndexer()
    
    # Load documents
    print("\n📚 Loading documents...")
    documents = indexer.load_documents()
    print(f"✅ Loaded {len(documents)} documents")
    
    # Show sample
    if documents:
        sample = documents[0]
        print(f"\n📄 Sample document:")
        print(f"   File: {sample.metadata.get('file_name', 'N/A')}")
        print(f"   Size: {len(sample.text):,} characters")
    
    # Build index
    print("\n🔨 Building vector store...")
    print("⏰ This may take 5-10 minutes...")
    
    index = indexer.build_index(force_rebuild=False)
    
    # Show stats
    stats = indexer.get_stats()
    print("\n" + "="*60)
    print("✅ INDEX BUILT SUCCESSFULLY!")
    print("="*60)
    print(f"\n📊 Statistics:")
    print(f"   Documents indexed: {stats['documents_loaded']}")
    print(f"   Collection count: {stats.get('collection_count', 'N/A')}")
    print(f"   Vector store: {stats['vectorstore_path']}")
    
    # Test query
    print("\n🧪 Testing with sample query...")
    query_engine = index.as_query_engine(similarity_top_k=3)
    response = query_engine.query("What is a Python decorator?")
    
    print(f"\n❓ Question: What is a Python decorator?")
    print(f"💬 Answer: {response.response[:200]}...")
    
    print("\n" + "="*60)
    print("🎉 All done! Index is ready to use.")
    print("="*60)


if __name__ == "__main__":
    main()