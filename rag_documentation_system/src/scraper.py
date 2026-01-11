"""
Document Scraper for RAG System
"""
import requests
import trafilatura
import time
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from tqdm import tqdm
from datetime import datetime

from src.config import config

logger = logging.getLogger(__name__)


class DocumentScraper:
    """Web scraper for documentation websites"""
    
    def __init__(self, save_path: Optional[Path] = None):
        self.save_path = save_path or config.paths.raw_docs_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': config.scraper.user_agent
        })
        self.results: List[Dict] = []
    
    def scrape_url(self, url: str) -> Optional[str]:
        """
        Scrape a single URL and extract clean text
        
        Args:
            url: URL to scrape
            
        Returns:
            Extracted text or None if failed
        """
        try:
            response = self.session.get(url, timeout=config.scraper.timeout)
            response.raise_for_status()
            
            # Extract clean text using trafilatura
            text = trafilatura.extract(response.text)
            
            if text and len(text) > config.scraper.min_text_length:
                return text
            
            logger.warning(f"Text too short for {url}: {len(text) if text else 0} chars")
            return None
            
        except requests.Timeout:
            logger.error(f"Timeout scraping {url}")
        except requests.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)[:100]}")
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {str(e)[:100]}")
        
        return None
    
    def save_document(self, text: str, filename: str) -> Path:
        """
        Save document to disk
        
        Args:
            text: Document text
            filename: Filename to save as
            
        Returns:
            Path to saved file
        """
        filepath = self.save_path / filename
        filepath.write_text(text, encoding='utf-8')
        return filepath
    
    def scrape_multiple(
        self, 
        urls: List[str], 
        prefix: str = "doc"
    ) -> List[Dict]:
        """
        Scrape multiple URLs with progress tracking
        
        Args:
            urls: List of URLs to scrape
            prefix: Filename prefix
            
        Returns:
            List of results with metadata
        """
        results = []
        
        logger.info(f"Starting to scrape {len(urls)} URLs with prefix '{prefix}'")
        
        for idx, url in enumerate(tqdm(urls, desc=f"Scraping {prefix}"), 1):
            text = self.scrape_url(url)
            
            if text:
                filename = f"{prefix}_{idx:03d}.txt"
                filepath = self.save_document(text, filename)
                
                result = {
                    'url': url,
                    'filename': filename,
                    'length': len(text),
                    'filepath': str(filepath),
                    'scraped_at': datetime.now().isoformat()
                }
                results.append(result)
                logger.debug(f"Saved {filename} ({len(text)} chars)")
            
            # Rate limiting
            time.sleep(config.scraper.delay_between_requests)
        
        self.results.extend(results)
        logger.info(f"Scraped {len(results)}/{len(urls)} documents successfully")
        
        return results
    
    def save_metadata(self, additional_info: Optional[Dict] = None) -> Path:
        """
        Save scraping metadata to JSON
        
        Args:
            additional_info: Additional metadata to include
            
        Returns:
            Path to metadata file
        """
        metadata = {
            'scrape_date': datetime.now().isoformat(),
            'total_documents': len(self.results),
            'documents': self.results
        }
        
        if additional_info:
            metadata.update(additional_info)
        
        metadata_path = self.save_path / 'metadata.json'
        metadata_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        logger.info(f"Metadata saved to {metadata_path}")
        return metadata_path
    
    def get_stats(self) -> Dict:
        """Get scraping statistics"""
        if not self.results:
            return {}
        
        sizes = [doc['length'] for doc in self.results]
        return {
            'total_docs': len(self.results),
            'total_chars': sum(sizes),
            'avg_size': sum(sizes) // len(sizes),
            'min_size': min(sizes),
            'max_size': max(sizes)
        }