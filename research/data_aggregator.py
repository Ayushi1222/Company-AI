import logging
from typing import Dict, Optional, List
from datetime import datetime
import concurrent.futures

from research.news_api import NewsAggregator
from research.hunter_api import HunterClient
from research.brandfetch_api import BrandfetchClient
from research.opencorporates_api import OpenCorporatesClient
from research.linkedin_api import LinkedInClient
from research.web_scraper import SimpleWebScraper
from config.settings import SOURCE_PRIORITIES

logger = logging.getLogger(__name__)


class DataAggregator:
    
    def __init__(self):
        self.news_aggregator = NewsAggregator()
        self.hunter = HunterClient()
        self.brandfetch = BrandfetchClient()
        self.opencorporates = OpenCorporatesClient()
        self.linkedin = LinkedInClient()
        self.web_scraper = SimpleWebScraper()
        
        self.last_research = None
        self.cache = {}
    
    def research_company(self, company_name: str, company_domain: Optional[str] = None,
                        include_news: bool = True, include_officers: bool = True) -> Dict:
        logger.info(f"Starting research for: {company_name}")
        
        results = {
            "company_name": company_name,
            "research_date": datetime.now().isoformat(),
            "sources_used": [],
            "data": {},
            "news": [],
            "conflicts": [],
            "status": "in_progress",
        }
        
        if not company_domain:
            name_clean = company_name.lower().replace(" ", "").replace(",", "")
            company_domain = f"{name_clean}.com"
            logger.info(f"No domain provided, trying: {company_domain}")
        
        if include_news:
            try:
                logger.info("Fetching news...")
                news_result = self._fetch_news(company_name)
                if news_result:
                    results["news"] = news_result
                    results["sources_used"].append("news")
                    logger.info(f"✓ Fetched {len(news_result)} news articles")
            except Exception as e:
                logger.warning(f"News fetch failed: {str(e)}")
                results["data"]["news"] = {"error": str(e)}
        
        if company_domain:
            try:
                logger.info("Fetching Hunter.io data...")
                hunter_result = self._fetch_hunter(company_domain)
                if hunter_result:
                    results["data"]["hunter"] = hunter_result
                    results["sources_used"].append("hunter")
                    logger.info("✓ Fetched Hunter.io data")
            except Exception as e:
                logger.warning(f"Hunter.io fetch failed: {str(e)}")
                results["data"]["hunter"] = {"error": str(e)}
        
        if company_domain:
            try:
                logger.info("Fetching Brandfetch data...")
                brandfetch_result = self._fetch_brandfetch(company_domain)
                if brandfetch_result:
                    results["data"]["brandfetch"] = brandfetch_result
                    results["sources_used"].append("brandfetch")
                    logger.info("✓ Fetched Brandfetch data")
            except Exception as e:
                logger.warning(f"Brandfetch fetch failed: {str(e)}")
                results["data"]["brandfetch"] = {"error": str(e)}
        
        if self.opencorporates.enabled:
            try:
                logger.info("Fetching OpenCorporates data...")
                oc_result = self._fetch_opencorporates(company_name)
                if oc_result:
                    results["data"]["opencorporates"] = oc_result
                    results["sources_used"].append("opencorporates")
                    logger.info("✓ Fetched OpenCorporates data")
            except Exception as e:
                logger.warning(f"OpenCorporates fetch failed: {str(e)}")
                results["data"]["opencorporates"] = {"error": str(e)}
        else:
            logger.info("OpenCorporates skipped (API key not configured)")
        
        if self.linkedin.enabled:
            try:
                logger.info("Fetching LinkedIn data...")
                linkedin_result = self._fetch_linkedin(company_name, company_domain)
                if linkedin_result:
                    results["data"]["linkedin"] = linkedin_result
                    results["sources_used"].append("linkedin")
                    logger.info("✓ Fetched LinkedIn data")
            except Exception as e:
                logger.warning(f"LinkedIn fetch failed: {str(e)}")
                results["data"]["linkedin"] = {"error": str(e)}
        else:
            logger.info("LinkedIn API skipped (API key not configured)")
        
        try:
            logger.info("Fetching social media links via web scraping...")
            web_data = self.web_scraper.scrape_company_website(company_domain)
            if web_data:
                results["data"]["web_scraping"] = web_data
                results["sources_used"].append("web_scraping")
                logger.info("✓ Fetched data via web scraping")
                
                if "linkedin" not in results["data"] and web_data.get("social_media", {}).get("linkedin_id"):
                    linkedin_vanity = web_data["social_media"]["linkedin_id"]
                    logger.info(f"Found LinkedIn ID from web scraping: {linkedin_vanity}")
                    if self.linkedin.enabled:
                        try:
                            linkedin_result = self.linkedin.get_company_by_vanity_name(linkedin_vanity)
                            if linkedin_result:
                                results["data"]["linkedin"] = linkedin_result
                                results["sources_used"].append("linkedin")
                                logger.info("✓ Fetched LinkedIn data using scraped vanity name")
                        except Exception as e:
                            logger.warning(f"LinkedIn fetch with vanity name failed: {str(e)}")
        except Exception as e:
            logger.warning(f"Web scraping failed: {str(e)}")
        
        if not results["data"] or all(isinstance(v, dict) and "error" in v for v in results["data"].values()):
            logger.info("No API data available, trying web scraping...")
            try:
                web_data = self.web_scraper.scrape_company_website(company_domain)
                if web_data:
                    results["data"]["web_scraping"] = web_data
                    results["sources_used"].append("web_scraping")
                    logger.info("✓ Fetched data via web scraping")
            except Exception as e:
                logger.warning(f"Web scraping failed: {str(e)}")
        
        results["consolidated"] = self._consolidate_data(results["data"])
        results["conflicts"] = self._detect_conflicts(results["data"])
        
        results["status"] = "complete"
        self.last_research = results
        
        return results
    
    def _fetch_news(self, company_name: str) -> List[Dict]:
        try:
            return self.news_aggregator.get_aggregated_news(
                company_name, days_back=30, limit=15
            )
        except Exception as e:
            logger.error(f"News fetch failed: {str(e)}")
            return []
    
    def _fetch_hunter(self, domain: str) -> Optional[Dict]:
        try:
            return self.hunter.get_domain_info(domain)
        except Exception as e:
            logger.error(f"Hunter.io fetch failed: {str(e)}")
            return None
    
    def _fetch_brandfetch(self, domain: str) -> Optional[Dict]:
        try:
            return self.brandfetch.get_brand_info(domain)
        except Exception as e:
            logger.error(f"Brandfetch fetch failed: {str(e)}")
            return None
    
    def _fetch_opencorporates(self, company_name: str) -> Optional[Dict]:
        try:
            return self.opencorporates.find_best_match(company_name)
        except Exception as e:
            logger.error(f"OpenCorporates fetch failed: {str(e)}")
            return None
    
    def _fetch_linkedin(self, company_name: str, domain: str = None) -> Optional[Dict]:
        try:
            result = self.linkedin.get_company_info(company_name)
            if result:
                return result
            
            if domain:
                domain_parts = domain.replace('www.', '').split('.')[0]
                result = self.linkedin.get_company_info(domain_parts)
                return result
            
            return None
        except Exception as e:
            logger.error(f"LinkedIn fetch failed: {str(e)}")
            return None
    
    def _consolidate_data(self, source_data: Dict) -> Dict:
        consolidated = {
            "name": None,
            "legal_name": None,
            "domain": None,
            "description": None,
            "founded": None,
            "employees": None,
            "revenue": None,
            "industry": None,
            "location": {},
            "status": None,
            "leadership": [],
            "social_media": {},
            "technologies": [],
        }
        
        for field in consolidated.keys():
            if field == "social_media":
                consolidated[field] = self._merge_social_media(source_data)
            else:
                value = self._get_field_by_priority(field, source_data)
                if value:
                    consolidated[field] = value
        
        return consolidated
    
    def _merge_social_media(self, source_data: Dict) -> Dict:
        social_media = {}
        
        for source, data in source_data.items():
            if not data or isinstance(data, dict) and "error" in data:
                continue
            
            if source == "linkedin":
                if data.get("linkedin_url"):
                    social_media["linkedin_url"] = data["linkedin_url"]
                if data.get("linkedin_id"):
                    social_media["linkedin_id"] = data["linkedin_id"]
                if data.get("vanity_name"):
                    social_media["linkedin_vanity_name"] = data["vanity_name"]
            
            elif source == "web_scraping" and data.get("social_media"):
                sm = data["social_media"]
                for key, value in sm.items():
                    if value and key not in social_media:
                        social_media[key] = value
            
            elif source == "brandfetch" and data.get("social_media"):
                sm = data["social_media"]
                for key, value in sm.items():
                    if value and key not in social_media:
                        social_media[key] = value
        
        return social_media
    
    def _get_field_by_priority(self, field: str, source_data: Dict) -> any:
        field_mappings = {
            "name": {
                "linkedin": "company_name",
                "brandfetch": "name",
                "hunter": "name",
                "opencorporates": "name",
                "web_scraping": "name",
            },
            "legal_name": {
                "opencorporates": "name",
            },
            "domain": {
                "hunter": "domain",
                "brandfetch": "domain",
                "linkedin": "website",
                "web_scraping": "domain",
            },
            "description": {
                "linkedin": "description",
                "brandfetch": "description",
                "web_scraping": "description",
            },
            "founded": {
                "linkedin": "founded",
                "opencorporates": "incorporation_date",
            },
            "employees": {
                "linkedin": "employee_count",
                "hunter": "employees",
            },
            "revenue": {},
            "industry": {
                "linkedin": "industry",
                "brandfetch": "industry",
            },
            "status": {
                "opencorporates": "status",
            },
            "social_media": {
                "linkedin": "linkedin_url",
                "brandfetch": "social_media",
                "web_scraping": "social_media",
            },
        }
        
        if field not in field_mappings:
            return None
        
        sorted_sources = sorted(
            source_data.keys(),
            key=lambda x: SOURCE_PRIORITIES.get(x, 0),
            reverse=True
        )
        
        for source in sorted_sources:
            if source not in source_data or not source_data[source]:
                continue
            
            if source not in field_mappings[field]:
                continue
            
            source_field = field_mappings[field][source]
            value = source_data[source].get(source_field)
            
            if value:
                return value
        
        return None
    
    def _detect_conflicts(self, source_data: Dict) -> List[Dict]:
        conflicts = []
        check_fields = ["name", "employees", "founded_year", "incorporation_date"]
        
        for field in check_fields:
            values = {}
            
            for source, data in source_data.items():
                if not data or isinstance(data, dict) and "error" in data:
                    continue
                
                value = data.get(field)
                if value:
                    values[source] = value
            
            if len(set(str(v) for v in values.values())) > 1:
                conflicts.append({
                    "field": field,
                    "values": values,
                    "description": f"Conflicting {field} values found",
                })
        
        return conflicts
    
    def get_summary(self, research_data: Dict) -> str:
        consolidated = research_data.get("consolidated", {})
        news = research_data.get("news", [])
        parts = []
        
        name = consolidated.get("name", "Unknown Company")
        parts.append(f"**{name}**")
        
        if consolidated.get("description"):
            parts.append(consolidated["description"])
        
        facts = []
        if consolidated.get("founded"):
            facts.append(f"Founded: {consolidated['founded']}")
        if consolidated.get("employees"):
            facts.append(f"Employees: {consolidated['employees']}")
        if consolidated.get("industry"):
            facts.append(f"Industry: {consolidated['industry']}")
        
        if facts:
            parts.append("\n**Key Facts:**\n" + "\n".join(f"• {fact}" for fact in facts))
        
        if news:
            parts.append(f"\n**Recent News:** {len(news)} articles found")
            parts.append("Latest: " + news[0].get("title", ""))
        
        return "\n\n".join(parts)
