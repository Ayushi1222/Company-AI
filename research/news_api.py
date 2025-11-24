import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests

from config.settings import NEWSAPI_KEY, GNEWS_API_KEY
from utils.error_handlers import APIError, handle_errors, retry_with_backoff

logger = logging.getLogger(__name__)


class NewsAPIClient:
    def __init__(self, api_key: str = NEWSAPI_KEY):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
        self.enabled = bool(api_key)
    
    @handle_errors("Failed to fetch news from NewsAPI")
    def search_company_news(self, 
                           company: str, 
                           days_back: int = 30,
                           limit: int = 10) -> List[Dict]:
        if not self.enabled:
            logger.warning("NewsAPI key not configured")
            return []
        
        to_date = datetime.now()
        from_date = to_date - timedelta(days=days_back)
        
        params = {
            "q": company,
            "from": from_date.strftime("%Y-%m-%d"),
            "to": to_date.strftime("%Y-%m-%d"),
            "sortBy": "relevancy",
            "pageSize": limit,
            "apiKey": self.api_key,
            "language": "en",
        }
        
        def api_call():
            response = requests.get(
                f"{self.base_url}/everything",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        
        try:
            data = retry_with_backoff(api_call, max_retries=3)
            
            if data.get("status") != "ok":
                raise APIError(f"NewsAPI error: {data.get('message', 'Unknown error')}")
            
            articles = data.get("articles", [])
            logger.info(f"Fetched {len(articles)} articles from NewsAPI for {company}")
            
            return self._format_articles(articles)
            
        except Exception as e:
            logger.error(f"NewsAPI request failed: {str(e)}")
            raise APIError(f"NewsAPI unavailable: {str(e)}")
    
    def _format_articles(self, articles: List[Dict]) -> List[Dict]:
        formatted = []
        for article in articles:
            formatted.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "published_at": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "author": article.get("author", "Unknown"),
                "content": article.get("content", ""),
            })
        return formatted


class GNewsClient:
    def __init__(self, api_key: str = GNEWS_API_KEY):
        self.api_key = api_key
        self.base_url = "https://gnews.io/api/v4"
        self.enabled = bool(api_key)
    
    @handle_errors("Failed to fetch news from GNews")
    def search_company_news(self,
                           company: str,
                           days_back: int = 30,
                           limit: int = 10) -> List[Dict]:
        if not self.enabled:
            logger.warning("GNews API key not configured")
            return []
        
        from_date = datetime.now() - timedelta(days=days_back)
        
        params = {
            "q": company,
            "lang": "en",
            "max": limit,
            "from": from_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "apikey": self.api_key,
        }
        
        def api_call():
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        
        try:
            data = retry_with_backoff(api_call, max_retries=3)
            
            articles = data.get("articles", [])
            logger.info(f"Fetched {len(articles)} articles from GNews for {company}")
            
            return self._format_articles(articles)
            
        except Exception as e:
            logger.error(f"GNews request failed: {str(e)}")
            raise APIError(f"GNews unavailable: {str(e)}")
    
    def _format_articles(self, articles: List[Dict]) -> List[Dict]:
        formatted = []
        for article in articles:
            formatted.append({
                "title": article.get("title", ""),
                "description": article.get("description", ""),
                "url": article.get("url", ""),
                "published_at": article.get("publishedAt", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "author": "Unknown",
                "content": article.get("content", ""),
                "image": article.get("image", ""),
            })
        return formatted


class NewsAggregator:
    def __init__(self):
        self.newsapi = NewsAPIClient()
        self.gnews = GNewsClient()
    
    def get_company_news(self,
                        company: str,
                        days_back: int = 30,
                        limit: int = 20) -> Dict[str, List[Dict]]:
        results = {
            "newsapi": [],
            "gnews": [],
        }
        
        try:
            if self.newsapi.enabled:
                results["newsapi"] = self.newsapi.search_company_news(
                    company, days_back, limit
                )
        except Exception as e:
            logger.warning(f"NewsAPI failed: {str(e)}")
        
        try:
            if self.gnews.enabled:
                results["gnews"] = self.gnews.search_company_news(
                    company, days_back, limit
                )
        except Exception as e:
            logger.warning(f"GNews failed: {str(e)}")
        
        return results
    
    def get_aggregated_news(self,
                           company: str,
                           days_back: int = 30,
                           limit: int = 20) -> List[Dict]:
        all_results = self.get_company_news(company, days_back, limit * 2)
        
        all_articles = []
        for source_articles in all_results.values():
            all_articles.extend(source_articles)
        
        unique_articles = self._deduplicate(all_articles)
        
        unique_articles.sort(
            key=lambda x: x.get("published_at", ""),
            reverse=True
        )
        
        return unique_articles[:limit]
    
    def _deduplicate(self, articles: List[Dict]) -> List[Dict]:
        seen_urls = set()
        seen_titles = set()
        unique = []
        
        for article in articles:
            url = article.get("url", "")
            title = article.get("title", "").lower()
            
            if url and url in seen_urls:
                continue
            
            if title and title in seen_titles:
                continue
            
            seen_urls.add(url)
            seen_titles.add(title)
            unique.append(article)
        
        return unique
