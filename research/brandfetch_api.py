import logging
from typing import Dict, Optional
import requests

from config.settings import BRANDFETCH_API_KEY
from utils.error_handlers import APIError, handle_errors, retry_with_backoff

logger = logging.getLogger(__name__)


class BrandfetchClient:
    
    def __init__(self, api_key: str = BRANDFETCH_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.brandfetch.io/v2"
        self.enabled = True
    
    @handle_errors("Failed to fetch data from Brandfetch")
    def get_brand_info(self, domain: str) -> Optional[Dict]:
        domain = domain.replace("http://", "").replace("https://", "").split("/")[0]
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        def api_call():
            response = requests.get(
                f"{self.base_url}/brands/{domain}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        
        try:
            data = retry_with_backoff(api_call, max_retries=3)
            logger.info(f"Successfully fetched brand data for {domain}")
            return self._format_brand_data(data, domain)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"Brand not found: {domain}")
                return None
            raise APIError(f"Brandfetch API error: {str(e)}")
        except Exception as e:
            logger.error(f"Brandfetch request failed: {str(e)}")
            return None
    
    def _format_brand_data(self, data: Dict, domain: str) -> Dict:
        social_links = {}
        for link in data.get("links", []):
            link_type = link.get("name", "").lower()
            link_url = link.get("url", "")
            if link_type in ["twitter", "linkedin", "facebook", "instagram"]:
                social_links[link_type] = link_url
        
        logos = []
        for logo in data.get("logos", []):
            for format_data in logo.get("formats", []):
                if format_data.get("format") == "png":
                    logos.append(format_data.get("src", ""))
                    break
        
        colors = []
        for color in data.get("colors", []):
            colors.append(color.get("hex", ""))
        
        return {
            "name": data.get("name", ""),
            "domain": domain,
            "description": data.get("description", ""),
            "logo": logos[0] if logos else "",
            "logos": logos,
            "colors": colors,
            "social_media": social_links,
            "industry": data.get("industry", ""),
            "website": data.get("domain", domain),
            "source": "Brandfetch",
            "raw_data": data,
        }
    
    def search_by_name(self, company_name: str) -> Optional[Dict]:
        name_lower = company_name.lower().replace(" ", "").replace(",", "")
        
        common_patterns = [
            f"{name_lower}.com",
            f"{name_lower}.io",
            f"{name_lower}.co",
        ]
        
        for domain in common_patterns:
            try:
                result = self.get_brand_info(domain)
                if result:
                    return result
            except:
                continue
        
        return None
