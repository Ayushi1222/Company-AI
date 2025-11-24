import logging
from typing import Dict, Optional
import requests
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class SimpleWebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timeout = 10
    
    def scrape_company_website(self, domain: str) -> Optional[Dict]:
        if not domain.startswith('http'):
            url = f'https://{domain}'
        else:
            url = domain
        
        try:
            logger.info(f"Scraping website: {url}")
            response = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'name': self._extract_company_name(soup, domain),
                'description': self._extract_description(soup),
                'title': self._extract_title(soup),
                'social_media': self._extract_social_links(soup),
                'domain': domain,
                'url': response.url,
                'source': 'web_scraping',
            }
            
            logger.info(f"Successfully scraped basic info from {domain}")
            return data
            
        except Exception as e:
            logger.error(f"Web scraping failed for {domain}: {str(e)}")
            return None
    
    def _extract_company_name(self, soup: BeautifulSoup, domain: str) -> str:
        og_title = soup.find('meta', property='og:site_name')
        if og_title and og_title.get('content'):
            return og_title['content']
        
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            for suffix in [' - ', ' | ', ' – ']:
                if suffix in title_text:
                    title_text = title_text.split(suffix)[0]
            return title_text
        
        return domain.split('.')[0].title()
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']
        
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content']
        
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 100:
                return text[:500]
        
        return "Description not available"
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        title = soup.find('title')
        if title:
            return title.get_text().strip()
        return ""
    
    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        social_media = {}
        
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            href_lower = href.lower()
            
            if 'twitter.com' in href_lower or 'x.com' in href_lower:
                social_media['twitter_url'] = href
                twitter_match = re.search(r'(?:twitter\.com|x\.com)/([a-zA-Z0-9_]+)', href)
                if twitter_match:
                    social_media['twitter_id'] = twitter_match.group(1)
                    social_media['twitter_handle'] = f"@{twitter_match.group(1)}"
            
            elif 'linkedin.com/company' in href_lower:
                social_media['linkedin_url'] = href
                linkedin_match = re.search(r'linkedin\.com/company/([a-zA-Z0-9\-_]+)', href)
                if linkedin_match:
                    social_media['linkedin_id'] = linkedin_match.group(1)
                    social_media['linkedin_vanity_name'] = linkedin_match.group(1)
            
            elif 'facebook.com' in href_lower:
                social_media['facebook_url'] = href
                fb_match = re.search(r'facebook\.com/([a-zA-Z0-9\.\-_]+)', href)
                if fb_match:
                    social_media['facebook_id'] = fb_match.group(1)
            
            elif 'instagram.com' in href_lower:
                social_media['instagram_url'] = href
                ig_match = re.search(r'instagram\.com/([a-zA-Z0-9\._]+)', href)
                if ig_match:
                    social_media['instagram_id'] = ig_match.group(1)
            
            elif 'youtube.com' in href_lower:
                social_media['youtube_url'] = href
        
        return social_media
    
    def extract_linkedin_from_url(self, url: str) -> Optional[str]:
        if not url:
            return None
        
        match = re.search(r'linkedin\.com/company/([a-zA-Z0-9\-_]+)', url)
        if match:
            return match.group(1)
        return None
    
    def extract_twitter_from_url(self, url: str) -> Optional[str]:
        if not url:
            return None
        
        match = re.search(r'(?:twitter\.com|x\.com)/([a-zA-Z0-9_]+)', url)
        if match:
            return match.group(1)
        return None
    
    def extract_emails(self, text: str) -> list:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text)
