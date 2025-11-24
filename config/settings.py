import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
EXPORTS_DIR = BASE_DIR / "exports"
TEMP_DIR = BASE_DIR / "temp"

EXPORTS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "")
BRANDFETCH_API_KEY = os.getenv("BRANDFETCH_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENCORPORATES_API_KEY = os.getenv("OPENCORPORATES_API_KEY", "")
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")

APP_ENV = os.getenv("APP_ENV", "development")
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./account_plans.db")

SCRAPING_CONFIG = {
    "user_agent": os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ),
    "download_delay": int(os.getenv("SCRAPING_DELAY", "2")),
    "respect_robots_txt": os.getenv("RESPECT_ROBOTS_TXT", "True").lower() == "true",
    "concurrent_requests": 8,
    "timeout": 30,
}

CONVERSATION_CONFIG = {
    "max_history": 50,
    "context_window": 10,
    "typing_delay": 0.5,
    "status_update_interval": 2,
}

ACCOUNT_PLAN_SECTIONS = [
    "overview",
    "team",
    "financials",
    "swot",
    "opportunities",
    "risks"
]

SOURCE_PRIORITIES = {
    "linkedin": 11,
    "brandfetch": 10,
    "opencorporates": 9,
    "hunter": 8,
    "company_website": 7,
    "newsapi": 6,
    "web_scraping": 4,
}

EXPORT_CONFIG = {
    "pdf_font": "Helvetica",
    "pdf_font_size": 12,
    "docx_template": None,
    "include_metadata": True,
    "include_sources": True,
}

ERROR_MESSAGES = {
    "api_unavailable": "The {service} service is temporarily unavailable. Using alternative sources.",
    "invalid_company": "I couldn't find a company named '{company}'. Could you check the spelling?",
    "rate_limit": "I've hit a rate limit for {service}. Continuing with cached data.",
    "network_error": "I'm experiencing network issues. Retrying in {seconds} seconds...",
    "invalid_input": "I didn't understand that. Could you rephrase or provide more details?",
}

STATUS_MESSAGES = {
    "initializing": "🔄 Initializing research...",
    "searching_web": "🔍 Searching web sources...",
    "fetching_news": "📰 Fetching latest news...",
    "enriching_data": "✨ Enriching company data...",
    "analyzing": "🧠 Analyzing information...",
    "generating_plan": "📋 Generating account plan...",
    "complete": "✅ Research complete!",
}

PERSONA_KEYWORDS = {
    "confused": ["um", "uh", "maybe", "i think", "not sure", "confused", "help", "don't know"],
    "efficient": ["quick", "summary", "bullet points", "key facts", "just", "only", "brief"],
    "chatty": ["actually", "by the way", "so like", "you know", "i mean", "pretty", "kinda"],
    "technical": ["api", "metrics", "data", "analysis", "specifically", "details", "technical"],
}

FEATURES = {
    "openai_summaries": bool(OPENAI_API_KEY),
    "text_to_speech": True,
    "pdf_export": True,
    "docx_export": True,
    "analytics": True,
    "feedback_widget": True,
}
