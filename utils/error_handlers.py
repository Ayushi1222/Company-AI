import traceback
import logging
from typing import Optional, Callable, Any
from functools import wraps
import streamlit as st

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResearchError(Exception):
    pass


class APIError(ResearchError):
    pass


class ScrapingError(ResearchError):
    pass


class ValidationError(ResearchError):
    pass


class ExportError(ResearchError):
    pass


def handle_errors(user_message: str = "An error occurred", log_error: bool = True):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except ValidationError as e:
                if log_error:
                    logger.warning(f"Validation error in {func.__name__}: {str(e)}")
                st.error(f"❌ {str(e)}")
                return None
            except APIError as e:
                if log_error:
                    logger.error(f"API error in {func.__name__}: {str(e)}")
                st.warning(f"⚠️ {user_message}: {str(e)}")
                return None
            except ScrapingError as e:
                if log_error:
                    logger.error(f"Scraping error in {func.__name__}: {str(e)}")
                st.warning(f"⚠️ {user_message}: {str(e)}")
                return None
            except ExportError as e:
                if log_error:
                    logger.error(f"Export error in {func.__name__}: {str(e)}")
                st.error(f"❌ Export failed: {str(e)}")
                return None
            except Exception as e:
                if log_error:
                    logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
                    logger.error(traceback.format_exc())
                st.error(f"❌ {user_message}. Please try again or contact support.")
                return None
        return wrapper
    return decorator


def safe_api_call(func: Callable, fallback: Any = None, 
                  error_message: Optional[str] = None) -> Any:
    try:
        return func()
    except Exception as e:
        logger.error(f"API call failed: {str(e)}")
        if error_message:
            st.warning(f"⚠️ {error_message}")
        return fallback


def retry_with_backoff(func: Callable, max_retries: int = 3, 
                       initial_delay: float = 1.0) -> Any:
    import time
    
    delay = initial_delay
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
    
    logger.error(f"All {max_retries} attempts failed")
    raise last_exception


def display_error_with_details(error: Exception, show_details: bool = False):
    error_type = type(error).__name__
    
    friendly_messages = {
        "ConnectionError": "I'm having trouble connecting to the internet. Please check your connection.",
        "Timeout": "The request is taking too long. Please try again.",
        "KeyError": "I'm missing some expected data. This might be a temporary issue.",
        "ValueError": "I received unexpected data. Please try rephrasing your request.",
        "FileNotFoundError": "I couldn't find the requested file.",
    }
    
    message = friendly_messages.get(error_type, "Something went wrong")
    st.error(f"❌ {message}")
    
    if show_details:
        with st.expander("Technical Details"):
            st.code(f"{error_type}: {str(error)}")
            st.code(traceback.format_exc())


def log_user_action(action: str, details: Optional[dict] = None):
    log_entry = f"User action: {action}"
    if details:
        log_entry += f" | Details: {details}"
    logger.info(log_entry)


def validate_api_keys() -> dict:
    from config.settings import (
        NEWSAPI_KEY, HUNTER_API_KEY, BRANDFETCH_API_KEY, OPENAI_API_KEY
    )
    
    status = {
        "newsapi": bool(NEWSAPI_KEY),
        "hunter": bool(HUNTER_API_KEY),
        "brandfetch": bool(BRANDFETCH_API_KEY),
        "openai": bool(OPENAI_API_KEY),
    }
    
    return status


def show_missing_api_keys_warning():
    status = validate_api_keys()
    missing = [name for name, configured in status.items() if not configured]
    
    if missing:
        st.warning(
            f"⚠️ Some API keys are not configured: {', '.join(missing)}. "
            f"The app will work with limited functionality. "
            f"Please add keys to your .env file for full features."
        )
