import os
import requests
import logging
from typing import Dict, List, Optional
from functools import wraps

logger = logging.getLogger(__name__)


def retry_on_failure(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(1 * (attempt + 1))
            logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            return None
        return wrapper
    return decorator


def handle_api_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API error in {func.__name__}: {str(e)}")
            return None
    return wrapper


class LinkedInClient:
    
    def __init__(self):
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID', '')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET', '')
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
        self.base_url = "https://api.linkedin.com/v2"
        self.enabled = bool(self.access_token)
        
        if not self.enabled:
            logger.warning("LinkedIn API not configured - will be skipped")
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
    
    @retry_on_failure(max_retries=2)
    @handle_api_error
    def search_company(self, company_name: str) -> Optional[Dict]:
        if not self.enabled:
            logger.info("LinkedIn API not enabled")
            return None
        
        try:
            url = f"{self.base_url}/organizationalEntityAcls"
            params = {
                'q': 'roleAssignee',
                'projection': '(elements*(organizationalTarget~(localizedName,vanityName)))'
            }
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=10
            )
            
            if response.status_code == 401:
                logger.error("LinkedIn API authentication failed - check access token")
                return None
            
            response.raise_for_status()
            data = response.json()
            
            logger.info(f"LinkedIn search successful for: {company_name}")
            return self._parse_company_data(data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"LinkedIn API request failed: {str(e)}")
            return None
    
    @retry_on_failure(max_retries=2)
    @handle_api_error
    def get_company_by_vanity_name(self, vanity_name: str) -> Optional[Dict]:
        if not self.enabled:
            logger.info("LinkedIn API not enabled")
            return None
        
        try:
            url = f"{self.base_url}/organizations"
            params = {
                'q': 'vanityName',
                'vanityName': vanity_name
            }
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=10
            )
            
            if response.status_code == 401:
                logger.error("LinkedIn API authentication failed")
                return None
            
            response.raise_for_status()
            data = response.json()
            
            if data.get('elements'):
                org_data = data['elements'][0]
                return self._parse_organization_data(org_data, vanity_name)
            
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"LinkedIn API request failed: {str(e)}")
            return None
    
    @retry_on_failure(max_retries=2)
    @handle_api_error
    def get_company_stats(self, organization_id: str) -> Optional[Dict]:
        if not self.enabled:
            logger.info("LinkedIn API not enabled")
            return None
        
        try:
            url = f"{self.base_url}/organizationPageStatistics/{organization_id}"
            
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            
            if response.status_code == 401:
                logger.error("LinkedIn API authentication failed")
                return None
            
            response.raise_for_status()
            data = response.json()
            
            return {
                'follower_count': data.get('followerCount', 0),
                'employee_count_range': data.get('employeeCountRange', {}),
                'page_views': data.get('pageViews', 0)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"LinkedIn stats request failed: {str(e)}")
            return None
    
    def _parse_company_data(self, data: Dict) -> Dict:
        result = {
            'source': 'linkedin',
            'companies': []
        }
        
        elements = data.get('elements', [])
        for element in elements[:5]:
            target = element.get('organizationalTarget~', {})
            result['companies'].append({
                'name': target.get('localizedName', ''),
                'vanity_name': target.get('vanityName', ''),
                'linkedin_url': f"https://www.linkedin.com/company/{target.get('vanityName', '')}"
            })
        
        return result
    
    def _parse_organization_data(self, org_data: Dict, vanity_name: str) -> Dict:
        localized_name = org_data.get('localizedName', '')
        
        staff_count = org_data.get('staffCount', {})
        employee_range = staff_count.get('range', {})
        
        min_count = employee_range.get('start', 0)
        max_count = employee_range.get('end', 0)
        employee_count = (min_count + max_count) // 2 if max_count > 0 else min_count
        
        founded_on = org_data.get('foundedOn', {})
        founded_year = None
        if isinstance(founded_on, dict):
            founded_year = founded_on.get('year')
        
        locations = org_data.get('locations', [])
        headquarters = None
        if locations:
            hq = next((loc for loc in locations if loc.get('locationType') == 'HEADQUARTERS'), locations[0])
            if hq:
                hq_info = hq.get('address', {})
                headquarters = {
                    'city': hq_info.get('city', ''),
                    'state': hq_info.get('geographicArea', ''),
                    'country': hq_info.get('country', '')
                }
        
        description = org_data.get('description', {})
        if isinstance(description, dict):
            description = description.get('localized', {}).get('en_US', '')
        
        specialties = org_data.get('specialties', [])
        if isinstance(specialties, dict):
            specialties = specialties.get('localized', {}).get('en_US', [])
        
        industries = org_data.get('industries', [])
        industry_name = None
        if industries and len(industries) > 0:
            industry_name = industries[0]
        
        company_type = org_data.get('companyType', {})
        if isinstance(company_type, dict):
            company_type = company_type.get('localizedName', 'Private')
        
        return {
            'source': 'linkedin',
            'company_name': localized_name,
            'linkedin_id': org_data.get('id', ''),
            'vanity_name': vanity_name,
            'linkedin_url': f"https://www.linkedin.com/company/{vanity_name}",
            'employee_count': employee_count,
            'employee_count_range': f"{min_count}-{max_count}" if max_count > 0 else f"{min_count}+",
            'description': description,
            'industry': industry_name,
            'specialties': specialties,
            'website': org_data.get('website', ''),
            'founded': founded_year,
            'headquarters': headquarters,
            'company_type': company_type,
            'tagline': org_data.get('tagline', {}).get('localized', {}).get('en_US', '') if isinstance(org_data.get('tagline'), dict) else ''
        }
    
    def get_company_info(self, company_identifier: str) -> Optional[Dict]:
        if not self.enabled:
            return None
        
        logger.info(f"Fetching LinkedIn data for: {company_identifier}")
        
        clean_identifier = company_identifier.lower().replace(' ', '-').replace(',', '')
        
        result = self.get_company_by_vanity_name(clean_identifier)
        
        if result:
            org_id = result.get('linkedin_id')
            if org_id:
                stats = self.get_company_stats(org_id)
                if stats:
                    result.update(stats)
        
        return result


def get_linkedin_data(company_name: str, vanity_name: str = None) -> Optional[Dict]:
    client = LinkedInClient()
    
    if vanity_name:
        return client.get_company_by_vanity_name(vanity_name)
    else:
        return client.get_company_info(company_name)
