import logging
from typing import Dict, List, Optional
import requests

from config.settings import OPENCORPORATES_API_KEY
from utils.error_handlers import APIError, handle_errors, retry_with_backoff

logger = logging.getLogger(__name__)


class OpenCorporatesClient:
    def __init__(self, api_key: str = OPENCORPORATES_API_KEY):
        self.api_key = api_key
        self.base_url = "https://api.opencorporates.com/v0.4"
        self.enabled = bool(api_key)
    
    @handle_errors("Failed to fetch data from OpenCorporates")
    def search_companies(self, 
                        name: str, 
                        jurisdiction: Optional[str] = None,
                        limit: int = 10) -> List[Dict]:
        if not self.enabled:
            logger.warning("OpenCorporates API key required but not configured")
            return []
        
        params = {
            "q": name,
            "per_page": limit,
            "api_token": self.api_key,
        }
        
        if jurisdiction:
            params["jurisdiction_code"] = jurisdiction
        
        def api_call():
            response = requests.get(
                f"{self.base_url}/companies/search",
                params=params,
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        
        try:
            data = retry_with_backoff(api_call, max_retries=3)
            
            companies = data.get("results", {}).get("companies", [])
            logger.info(f"Found {len(companies)} companies matching '{name}'")
            
            return [self._format_company(c.get("company", {})) for c in companies]
            
        except Exception as e:
            logger.error(f"OpenCorporates search failed: {str(e)}")
            raise APIError(f"OpenCorporates unavailable: {str(e)}")
    
    @handle_errors("Failed to fetch company details")
    def get_company_details(self, jurisdiction: str, company_number: str) -> Optional[Dict]:
        params = {}
        if self.api_key:
            params["api_token"] = self.api_key
        
        def api_call():
            response = requests.get(
                f"{self.base_url}/companies/{jurisdiction}/{company_number}",
                params=params,
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        
        try:
            data = retry_with_backoff(api_call, max_retries=3)
            company = data.get("results", {}).get("company", {})
            return self._format_company_detailed(company)
            
        except Exception as e:
            logger.error(f"OpenCorporates company details failed: {str(e)}")
            raise APIError(f"OpenCorporates unavailable: {str(e)}")
    
    def _format_company(self, data: Dict) -> Dict:
        return {
            "name": data.get("name", ""),
            "company_number": data.get("company_number", ""),
            "jurisdiction": data.get("jurisdiction_code", ""),
            "incorporation_date": data.get("incorporation_date", ""),
            "company_type": data.get("company_type", ""),
            "status": data.get("current_status", ""),
            "registered_address": data.get("registered_address_in_full", ""),
            "url": data.get("opencorporates_url", ""),
        }
    
    def _format_company_detailed(self, data: Dict) -> Dict:
        formatted = self._format_company(data)
        
        formatted.update({
            "dissolution_date": data.get("dissolution_date"),
            "branch": data.get("branch", ""),
            "previous_names": data.get("previous_names", []),
            "alternative_names": data.get("alternative_names", []),
            "agent_name": data.get("agent_name", ""),
            "agent_address": data.get("agent_address", ""),
            "registry_url": data.get("registry_url", ""),
            "industry_codes": data.get("industry_codes", []),
        })
        
        return formatted
    
    @handle_errors("Failed to fetch company officers")
    def get_company_officers(self, jurisdiction: str, company_number: str) -> List[Dict]:
        params = {}
        if self.api_key:
            params["api_token"] = self.api_key
        
        def api_call():
            response = requests.get(
                f"{self.base_url}/companies/{jurisdiction}/{company_number}/officers",
                params=params,
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        
        try:
            data = retry_with_backoff(api_call, max_retries=3)
            officers = data.get("results", {}).get("officers", [])
            
            return [self._format_officer(o.get("officer", {})) for o in officers]
            
        except Exception as e:
            logger.error(f"OpenCorporates officers request failed: {str(e)}")
            return []
    
    def _format_officer(self, data: Dict) -> Dict:
        return {
            "name": data.get("name", ""),
            "position": data.get("position", ""),
            "start_date": data.get("start_date", ""),
            "end_date": data.get("end_date"),
            "nationality": data.get("nationality", ""),
            "occupation": data.get("occupation", ""),
            "address": data.get("address", ""),
        }
    
    def find_best_match(self, company_name: str) -> Optional[Dict]:
        results = self.search_companies(company_name, limit=5)
        
        if not results:
            return None
        
        return results[0]
