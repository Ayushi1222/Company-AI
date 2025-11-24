import logging
from typing import Dict, Optional
import requests

from config.settings import HUNTER_API_KEY
from utils.error_handlers import APIError, handle_errors, retry_with_backoff

logger = logging.getLogger(__name__)


class HunterClient:
    
    def __init__(self, api_key: str = HUNTER_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.hunter.io/v2"
        self.enabled = bool(api_key)
    
    @handle_errors("Failed to fetch data from Hunter.io")
    def get_domain_info(self, domain: str) -> Optional[Dict]:
        if not self.enabled:
            logger.warning("Hunter.io API key not configured")
            return None
        
        domain = domain.replace("http://", "").replace("https://", "").split("/")[0]
        
        params = {
            "domain": domain,
            "api_key": self.api_key
        }
        
        def api_call():
            response = requests.get(
                f"{self.base_url}/domain-search",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        
        try:
            data = retry_with_backoff(api_call, max_retries=3)
            
            if data.get("data"):
                logger.info(f"Successfully fetched data from Hunter.io for {domain}")
                return self._format_company_data(data["data"], domain)
            return None
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"Domain not found in Hunter.io: {domain}")
                return None
            raise APIError(f"Hunter.io API error: {str(e)}")
        except Exception as e:
            logger.error(f"Hunter.io request failed: {str(e)}")
            return None
    
    def _format_company_data(self, data: Dict, domain: str) -> Dict:
        return {
            "name": data.get("organization", ""),
            "domain": domain,
            "employees": data.get("emails_count"),
            "email_pattern": data.get("pattern", ""),
            "emails_found": data.get("emails", []),
            "social_media": {
                "twitter": data.get("twitter", ""),
                "facebook": data.get("facebook", ""),
                "linkedin": data.get("linkedin", ""),
            },
            "source": "Hunter.io",
            "raw_data": data,
        }
    
    def search_by_name(self, company_name: str) -> Optional[Dict]:
        if not self.enabled:
            return None
        
        name_lower = company_name.lower().replace(" ", "").replace(",", "").replace(".", "")
        
        common_patterns = [
            f"{name_lower}.com",
            f"{name_lower}.io",
            f"{name_lower}.co",
        ]
        
        for domain in common_patterns:
            try:
                result = self.get_domain_info(domain)
                if result:
                    return result
            except:
                continue
        
        return None
