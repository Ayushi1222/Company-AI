import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AccountPlanGenerator:
    def __init__(self):
        self.template_version = "1.0"
    
    def generate(self, research_data: Dict, user_notes: Optional[Dict] = None) -> Dict:
        consolidated = research_data.get("consolidated", {})
        news = research_data.get("news", [])
        
        plan = {
            "metadata": {
                "company_name": research_data.get("company_name", "Unknown"),
                "generated_date": datetime.now().isoformat(),
                "version": self.template_version,
                "sources": research_data.get("sources_used", []),
            },
            "sections": {
                "overview": self._generate_overview(consolidated, news),
                "team": self._generate_team(consolidated),
                "financials": self._generate_financials(consolidated),
                "swot": self._generate_swot(consolidated, news),
                "opportunities": self._generate_opportunities(consolidated, news),
                "risks": self._generate_risks(consolidated, news),
            },
            "user_notes": user_notes or {},
            "raw_research": research_data,
        }
        
        return plan
    
    def _generate_overview(self, data: Dict, news: list) -> Dict:
        company_name = data.get("name", "N/A")
        return {
            "title": "Company Overview",
            "content": {
                "company_name": company_name,
                "legal_name": data.get("legal_name", company_name),
                "domain": data.get("domain", "N/A"),
                "description": data.get("description", "No description available"),
                "founded": data.get("founded", "N/A"),
                "industry": data.get("industry", "N/A"),
                "status": data.get("status", "Active"),
                "employee_count": data.get("employees", "N/A"),
                "headquarters": self._format_location(data.get("location", {})),
                "recent_activity": self._summarize_news(news[:3]) if news else "No recent news",
            },
            "editable": True,
        }
    
    def _generate_team(self, data: Dict) -> Dict:
        leadership = data.get("leadership", [])
        
        return {
            "title": "Leadership Team",
            "content": {
                "executives": leadership if leadership else ["Information not available"],
                "key_decision_makers": "To be identified",
                "org_structure": "Research in progress",
                "linkedin_profiles": self._format_social(data.get("social_media", {})),
            },
            "editable": True,
        }
    
    def _generate_financials(self, data: Dict) -> Dict:
        return {
            "title": "Financial Information",
            "content": {
                "annual_revenue": data.get("revenue", "N/A"),
                "employee_count": data.get("employees", "N/A"),
                "funding_stage": "Research in progress",
                "investors": "Research in progress",
                "growth_metrics": "Research in progress",
                "public_private": "Private" if not data.get("ticker") else "Public",
                "ticker": data.get("ticker", "N/A"),
            },
            "editable": True,
        }
    
    def _generate_swot(self, data: Dict, news: list) -> Dict:
        return {
            "title": "SWOT Analysis",
            "content": {
                "strengths": self._identify_strengths(data, news),
                "weaknesses": self._identify_weaknesses(data, news),
                "opportunities": self._identify_opportunities(data, news),
                "threats": self._identify_threats(data, news),
            },
            "editable": True,
        }
    
    def _generate_opportunities(self, data: Dict, news: list) -> Dict:
        return {
            "title": "Engagement Opportunities",
            "content": {
                "strategic_fit": "Analyze alignment with our solutions",
                "pain_points": "Research current challenges from news and industry trends",
                "decision_drivers": "Identify key buying factors",
                "timing": "Assess readiness for engagement",
                "entry_points": self._suggest_entry_points(data, news),
            },
            "editable": True,
        }
    
    def _generate_risks(self, data: Dict, news: list) -> Dict:
        return {
            "title": "Risk Assessment",
            "content": {
                "competitive_risks": "Analyze competitive landscape",
                "financial_risks": self._assess_financial_risks(data),
                "timing_risks": "Evaluate market timing",
                "technical_risks": "Assess technical compatibility",
                "mitigation_strategies": self._suggest_mitigations(data, news),
            },
            "editable": True,
        }
    
    
    def _format_location(self, location: Dict) -> str:
        parts = []
        for key in ["city", "state", "country"]:
            if location.get(key):
                parts.append(location[key])
        return ", ".join(parts) if parts else "N/A"
    
    def _format_social(self, social: Dict) -> Dict:
        return {
            "linkedin": social.get("linkedin", "N/A"),
            "twitter": social.get("twitter", "N/A"),
        }
    
    def _summarize_news(self, articles: list) -> str:
        if not articles:
            return "No recent news"
        
        summaries = []
        for article in articles[:3]:
            title = article.get("title", "")
            date = article.get("published_at", "")
            if title:
                summaries.append(f"• {title} ({date[:10]})")
        
        return "\n".join(summaries) if summaries else "No recent news"
    
    def _identify_strengths(self, data: Dict, news: list) -> list:
        strengths = []
        
        if data.get("founded"):
            try:
                years = datetime.now().year - int(str(data["founded"])[:4])
                if years > 10:
                    strengths.append(f"Established company with {years}+ years experience")
            except:
                pass
        
        if data.get("employees"):
            strengths.append(f"Team of {data['employees']} employees")
        
        if data.get("technologies"):
            strengths.append(f"Modern tech stack: {', '.join(data['technologies'][:3])}")
        
        if not strengths:
            strengths = ["Strong market presence (details to be researched)"]
        
        return strengths
    
    def _identify_weaknesses(self, data: Dict, news: list) -> list:
        return [
            "Competitive pressure analysis needed",
            "Market position assessment required",
        ]
    
    def _identify_opportunities(self, data: Dict, news: list) -> list:
        opportunities = []
        
        if news:
            opportunities.append("Recent news indicates active growth phase")
        
        opportunities.extend([
            "Digital transformation initiatives",
            "Market expansion potential",
        ])
        
        return opportunities
    
    def _identify_threats(self, data: Dict, news: list) -> list:
        return [
            "Industry competition",
            "Economic factors",
            "Technology disruption",
        ]
    
    def _suggest_entry_points(self, data: Dict, news: list) -> list:
        return [
            "Executive outreach via LinkedIn",
            "Industry event participation",
            "Case study/whitepaper sharing",
        ]
    
    def _assess_financial_risks(self, data: Dict) -> str:
        if data.get("status") == "Active":
            return "Low - Company is active and operating"
        return "Requires assessment"
    
    def _suggest_mitigations(self, data: Dict, news: list) -> list:
        return [
            "Conduct thorough due diligence",
            "Start with pilot project",
            "Establish executive relationships",
        ]
    
    def update_section(self, plan: Dict, section: str, updates: Dict) -> Dict:
        if section in plan["sections"]:
            plan["sections"][section]["content"].update(updates)
            plan["sections"][section]["last_edited"] = datetime.now().isoformat()
        
        return plan
    
    def to_text(self, plan: Dict) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append(f"ACCOUNT PLAN: {plan['metadata']['company_name']}")
        lines.append(f"Generated: {plan['metadata']['generated_date'][:10]}")
        lines.append("=" * 60)
        lines.append("")
        
        for section_name, section in plan["sections"].items():
            lines.append(f"\n{section['title'].upper()}")
            lines.append("-" * 40)
            
            content = section["content"]
            if isinstance(content, dict):
                for key, value in content.items():
                    key_formatted = key.replace("_", " ").title()
                    if isinstance(value, list):
                        lines.append(f"\n{key_formatted}:")
                        for item in value:
                            lines.append(f"  • {item}")
                    else:
                        lines.append(f"\n{key_formatted}:")
                        lines.append(f"  {value}")
            else:
                lines.append(str(content))
            
            lines.append("")
        
        return "\n".join(lines)
