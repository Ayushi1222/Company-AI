import re
from typing import Dict, List
from config.settings import PERSONA_KEYWORDS


class PersonaDetector:
    def __init__(self):
        self.persona_scores = {
            "confused": 0,
            "efficient": 0,
            "chatty": 0,
            "technical": 0,
        }
        self.message_count = 0
        self.current_persona = "neutral"
    
    def analyze_message(self, message: str) -> str:
        message_lower = message.lower()
        self.message_count += 1
        
        message_persona_scores = {persona: 0 for persona in self.persona_scores.keys()}
        
        for persona, keywords in PERSONA_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    message_persona_scores[persona] += 1
        
        message_persona_scores.update(self._analyze_structure(message))
        
        decay_factor = 0.7
        for persona in self.persona_scores:
            self.persona_scores[persona] = (
                self.persona_scores[persona] * decay_factor + 
                message_persona_scores[persona]
            )
        
        self.current_persona = self._determine_persona()
        
        return self.current_persona
    
    def _analyze_structure(self, message: str) -> Dict[str, float]:
        scores = {"confused": 0, "efficient": 0, "chatty": 0, "technical": 0}
        
        word_count = len(message.split())
        
        if word_count < 10:
            scores["efficient"] += 2
        elif word_count > 50:
            scores["chatty"] += 2
        
        question_count = message.count("?")
        if question_count > 2:
            scores["confused"] += 2
        elif question_count == 1 and word_count < 15:
            scores["efficient"] += 1
        
        if "..." in message or re.search(r'\bum\b|\buh\b|\ber\b', message.lower()):
            scores["confused"] += 2
        
        technical_terms = [
            "api", "metric", "data", "analysis", "kpi", "revenue", 
            "valuation", "pipeline", "conversion", "roi"
        ]
        technical_count = sum(1 for term in technical_terms if term in message.lower())
        scores["technical"] += technical_count
        
        if message.count("!") > 1:
            scores["chatty"] += 1
        
        casual_markers = ["lol", "haha", "btw", "tbh", "omg", "yeah"]
        if any(marker in message.lower() for marker in casual_markers):
            scores["chatty"] += 2
        
        return scores
    
    def _determine_persona(self) -> str:
        if self.message_count < 2:
            return "neutral"
        
        max_score = max(self.persona_scores.values())
        
        if max_score < 2:
            return "neutral"
        
        for persona, score in self.persona_scores.items():
            if score == max_score:
                return persona
        
        return "neutral"
    
    def get_persona(self) -> str:
        return self.current_persona
    
    def get_persona_description(self) -> str:
        descriptions = {
            "confused": "Needs guidance - I'll provide clear explanations and ask clarifying questions",
            "efficient": "Prefers brevity - I'll be concise and direct",
            "chatty": "Enjoys conversation - I'll be friendly and engaging",
            "technical": "Wants details - I'll provide in-depth technical information",
            "neutral": "Adapting to your style...",
        }
        return descriptions.get(self.current_persona, "Analyzing communication style...")
    
    def reset(self):
        self.persona_scores = {persona: 0 for persona in self.persona_scores.keys()}
        self.message_count = 0
        self.current_persona = "neutral"
    
    def get_adaptation_tips(self) -> List[str]:
        tips = {
            "confused": [
                "Ask clarifying questions",
                "Provide examples",
                "Break down complex concepts",
                "Offer step-by-step guidance",
                "Check for understanding",
            ],
            "efficient": [
                "Get straight to the point",
                "Use bullet points",
                "Minimize small talk",
                "Provide actionable information",
                "Avoid lengthy explanations",
            ],
            "chatty": [
                "Be conversational and warm",
                "Acknowledge their comments",
                "Use friendly language",
                "Allow for tangents",
                "Show personality",
            ],
            "technical": [
                "Provide detailed data",
                "Include metrics and numbers",
                "Explain methodologies",
                "Reference sources",
                "Use technical terminology",
            ],
            "neutral": [
                "Maintain balanced tone",
                "Adapt based on next inputs",
                "Be helpful and clear",
            ],
        }
        return tips.get(self.current_persona, [])
