import re
import validators
from typing import Tuple, Optional


def validate_company_name(name: str) -> Tuple[bool, Optional[str]]:
    if not name or not name.strip():
        return False, "Company name cannot be empty."
    
    name = " ".join(name.split())
    
    if len(name) < 2:
        return False, "Company name is too short. Please provide at least 2 characters."
    
    if len(name) > 200:
        return False, "Company name is too long. Please limit to 200 characters."
    
    suspicious_patterns = [
        r"<script", r"javascript:", r"--", r"';", r"DROP TABLE",
        r"<iframe", r"onerror=", r"onclick="
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, name, re.IGNORECASE):
            return False, "Invalid characters detected. Please use only standard text."
    
    return True, None


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    if not url or not url.strip():
        return False, "URL cannot be empty."
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if not validators.url(url):
        return False, "Please provide a valid URL (e.g., https://example.com)."
    
    return True, None


def validate_file_upload(file) -> Tuple[bool, Optional[str]]:
    if file is None:
        return False, "No file uploaded."
    
    max_size = 10 * 1024 * 1024
    if file.size > max_size:
        return False, "File too large. Maximum size is 10MB."
    
    allowed_extensions = ['.pdf', '.txt', '.doc', '.docx']
    file_ext = file.name[file.name.rfind('.'):].lower() if '.' in file.name else ''
    
    if file_ext not in allowed_extensions:
        return False, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
    
    return True, None


def sanitize_input(text: str, max_length: int = 5000) -> str:
    if not text:
        return ""
    
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)
    
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()


def detect_input_intent(text: str) -> str:
    text_lower = text.lower().strip()
    
    question_words = ['what', 'why', 'how', 'when', 'where', 'who', 'which', 'can you', 'could you']
    if any(text_lower.startswith(word) for word in question_words) or text_lower.endswith('?'):
        return 'question'
    
    command_words = ['research', 'find', 'get', 'analyze', 'generate', 'create', 'export', 'download']
    if any(word in text_lower for word in command_words):
        return 'command'
    
    clarification_words = ['yes', 'no', 'correct', 'exactly', 'right', 'wrong', 'not quite']
    if any(text_lower.startswith(word) for word in clarification_words):
        return 'clarification'
    
    feedback_words = ['thanks', 'thank you', 'good', 'great', 'perfect', 'excellent', 'bad', 'wrong']
    if any(word in text_lower for word in feedback_words):
        return 'feedback'
    
    return 'unknown'


def is_input_too_long(text: str, max_words: int = 500) -> bool:
    word_count = len(text.split())
    return word_count > max_words


def extract_company_mentions(text: str) -> list:
    companies = []
    
    pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|Corp|LLC|Ltd|Limited|Corporation))?\.?)\b'
    matches = re.findall(pattern, text)
    
    companies.extend(matches)
    
    return list(set(companies))
