import logging
from typing import Dict, Optional
import requests

from config.settings import CLEARBIT_API_KEY
from utils.error_handlers import APIError, handle_errors, retry_with_backoff

logger = logging.getLogger(__name__)


class ClearbitClient:
    def __init__(self, api_key: str = CLEARBIT_API_KEY):
        self.api_key = api_key
        self.base_url = "https://company.clearbit.com/v2"
        self.enabled = bool(api_key)
    
    @handle_errors("Failed to fetch data from Clearbit")
    def enrich_company(self, domain: str) -> Optional[Dict]:
        if not self.enabled:
            logger.warning("Clearbit API key not configured")
            return None
        
        domain = domain.replace("http://", "").replace("https://", "").split("/")[0]
        
        params = {"domain": domain}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        def api_call():
            response = requests.get(
                f"{self.base_url}/companies/find",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        
        try:
            data = retry_with_backoff(api_call, max_retries=3)
            logger.info(f"Successfully enriched data for {domain}")
            return self._format_company_data(data)
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"Company not found in Clearbit: {domain}")
                return None
            raise APIError(f"Clearbit API error: {str(e)}")
        except Exception as e:
            logger.error(f"Clearbit request failed: {str(e)}")
            raise APIError(f"Clearbit unavailable: {str(e)}")
    
    def _format_company_data(self, data: Dict) -> Dict:
        return {
            "name": data.get("name", ""),
            "legal_name": data.get("legalName", ""),
            "domain": data.get("domain", ""),
            "description": data.get("description", ""),
            "founded_year": data.get("foundedYear"),
            "employees": data.get("metrics", {}).get("employees"),
            "employees_range": data.get("metrics", {}).get("employeesRange"),
            "annual_revenue": data.get("metrics", {}).get("annualRevenue"),
            "estimated_revenue": data.get("metrics", {}).get("estimatedAnnualRevenue"),
            "industry": data.get("category", {}).get("industry", ""),
            "sector": data.get("category", {}).get("sector", ""),
            "tags": data.get("tags", []),
            "technology": data.get("tech", []),
            "location": {
                "city": data.get("geo", {}).get("city", ""),
                "state": data.get("geo", {}).get("state", ""),
                "country": data.get("geo", {}).get("country", ""),
                "street": data.get("geo", {}).get("streetName", ""),
            },
            "logo": data.get("logo", ""),
            "website": data.get("url", ""),
            "linkedin": data.get("linkedin", {}).get("handle", ""),
            "twitter": data.get("twitter", {}).get("handle", ""),
            "facebook": data.get("facebook", {}).get("handle", ""),
            "phone": data.get("phone", ""),
            "type": data.get("type", ""),
            "ticker": data.get("ticker", ""),
            "parent_domain": data.get("parent", {}).get("domain", ""),
            "ultimate_parent": data.get("ultimateParent", {}).get("domain", ""),
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
            f"{name_lower}.net",
        ]
        
        for domain in common_patterns:
            try:
                result = self.enrich_company(domain)
                if result:
                    return result
            except:
                continue
        
        logger.warning(f"Could not find domain for company: {company_name}")
        return None
    
    def get_technologies(self, domain: str) -> list:
        data = self.enrich_company(domain)
        if data:
            return data.get("technology", [])
        return []
    
    def get_employee_range(self, domain: str) -> Optional[str]:
        data = self.enrich_company(domain)
        if data:
            return data.get("employees_range")
        return None
