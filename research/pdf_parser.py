import logging
from typing import Optional, Dict
import io

logger = logging.getLogger(__name__)


class PDFParser:
    def __init__(self):
        self.pypdf2_available = False
        self.pdfplumber_available = False
        
        try:
            import PyPDF2
            self.pypdf2_available = True
            logger.info("PyPDF2 available")
        except ImportError:
            logger.warning("PyPDF2 not available")
        
        try:
            import pdfplumber
            self.pdfplumber_available = True
            logger.info("pdfplumber available")
        except ImportError:
            logger.warning("pdfplumber not available")
    
    def extract_text(self, file_obj) -> Dict[str, any]:
        if not self.pypdf2_available and not self.pdfplumber_available:
            logger.error("No PDF parsing library available")
            return {
                "text": "",
                "page_count": 0,
                "error": "No PDF parsing library installed",
            }
        
        if self.pdfplumber_available:
            result = self._extract_with_pdfplumber(file_obj)
            if result.get("text"):
                return result
        
        if self.pypdf2_available:
            return self._extract_with_pypdf2(file_obj)
        
        return {
            "text": "",
            "page_count": 0,
            "error": "Failed to extract text",
        }
    
    def _extract_with_pypdf2(self, file_obj) -> Dict:
        try:
            import PyPDF2
            
            if isinstance(file_obj, bytes):
                file_obj = io.BytesIO(file_obj)
            
            reader = PyPDF2.PdfReader(file_obj)
            page_count = len(reader.pages)
            
            text_parts = []
            for page_num, page in enumerate(reader.pages):
                try:
                    text = page.extract_text()
                    if text:
                        text_parts.append(f"--- Page {page_num + 1} ---\n{text}")
                except Exception as e:
                    logger.warning(f"Failed to extract page {page_num + 1}: {str(e)}")
            
            full_text = "\n\n".join(text_parts)
            
            metadata = {}
            if reader.metadata:
                metadata = {
                    "title": reader.metadata.get("/Title", ""),
                    "author": reader.metadata.get("/Author", ""),
                    "subject": reader.metadata.get("/Subject", ""),
                    "creator": reader.metadata.get("/Creator", ""),
                }
            
            logger.info(f"Extracted {len(full_text)} characters from {page_count} pages using PyPDF2")
            
            return {
                "text": full_text,
                "page_count": page_count,
                "metadata": metadata,
                "method": "PyPDF2",
            }
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {str(e)}")
            return {
                "text": "",
                "page_count": 0,
                "error": str(e),
            }
    
    def _extract_with_pdfplumber(self, file_obj) -> Dict:
        try:
            import pdfplumber
            
            if isinstance(file_obj, bytes):
                file_obj = io.BytesIO(file_obj)
            
            with pdfplumber.open(file_obj) as pdf:
                page_count = len(pdf.pages)
                
                text_parts = []
                for page_num, page in enumerate(pdf.pages):
                    try:
                        text = page.extract_text()
                        if text:
                            text_parts.append(f"--- Page {page_num + 1} ---\n{text}")
                    except Exception as e:
                        logger.warning(f"Failed to extract page {page_num + 1}: {str(e)}")
                
                full_text = "\n\n".join(text_parts)
                
                metadata = pdf.metadata or {}
                
                logger.info(f"Extracted {len(full_text)} characters from {page_count} pages using pdfplumber")
                
                return {
                    "text": full_text,
                    "page_count": page_count,
                    "metadata": metadata,
                    "method": "pdfplumber",
                }
                
        except Exception as e:
            logger.error(f"pdfplumber extraction failed: {str(e)}")
            return {
                "text": "",
                "page_count": 0,
                "error": str(e),
            }
    
    def extract_company_mentions(self, text: str) -> list:
        import re
        
        pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|Corp|LLC|Ltd|Limited|Corporation))?\.?)\b'
        matches = re.findall(pattern, text)
        
        from collections import Counter
        counter = Counter(matches)
        
        return [name for name, count in counter.most_common(20) if count > 1]
