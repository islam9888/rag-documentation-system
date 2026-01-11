"""
Document Scraper Script
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.scraper import DocumentScraper
from src.utils import setup_logging

logger = setup_logging(log_level="INFO")


# Documentation URLs
PYTHON_URLS = [
    "https://docs.python.org/3/tutorial/introduction.html",
    "https://docs.python.org/3/tutorial/controlflow.html",
    "https://docs.python.org/3/tutorial/datastructures.html",
    # Add more from your original list...
]

FASTAPI_URLS = [
    "https://fastapi.tiangolo.com/",
    "https://fastapi.tiangolo.com/tutorial/first-steps/",
    # Add more...
]

LANGCHAIN_URLS = [
    "https://python.langchain.com/docs/get_started/introduction",
    # Add more...
]

LLAMAINDEX_URLS = [
    "https://docs.llamaindex.ai/en/stable/",
    # Add more...
]


def main():
    """Scrape all documentation"""
    print("="*60)
    print("🕷️  DOCUMENTATION SCRAPER")
    print("="*60)
    
    # Setup
    config.setup()
    scraper = DocumentScraper()
    
    # Scrape each source
    print("\n📘 Scraping Python docs...")
    python_results = scraper.scrape_multiple(PYTHON_URLS, prefix="python")
    
    print("\n⚡ Scraping FastAPI docs...")
    fastapi_results = scraper.scrape_multiple(FASTAPI_URLS, prefix="fastapi")
    
    print("\n🦜 Scraping LangChain docs...")
    langchain_results = scraper.scrape_multiple(LANGCHAIN_URLS, prefix="langchain")
    
    print("\n🦙 Scraping LlamaIndex docs...")
    llamaindex_results = scraper.scrape_multiple(LLAMAINDEX_URLS, prefix="llamaindex")
    
    # Save metadata
    metadata_info = {
        'sources': {
            'python': len(python_results),
            'fastapi': len(fastapi_results),
            'langchain': len(langchain_results),
            'llamaindex': len(llamaindex_results)
        }
    }
    scraper.save_metadata(metadata_info)
    
    # Stats
    stats = scraper.get_stats()
    print("\n" + "="*60)
    print("✅ SCRAPING COMPLETE!")
    print("="*60)
    print(f"\n📊 Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value:,}")


if __name__ == "__main__":
    main()
