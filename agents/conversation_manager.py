from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

from agents.persona_detector import PersonaDetector
from agents.response_generator import ResponseGenerator


class ConversationState(Enum):
    IDLE = "idle"
    AWAITING_COMPANY = "awaiting_company"
    RESEARCHING = "researching"
    PRESENTING_RESULTS = "presenting_results"
    CLARIFYING = "clarifying"
    EDITING = "editing"
    EXPORTING = "exporting"


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)


@dataclass
class ConversationContext:
    current_company: Optional[str] = None
    state: ConversationState = ConversationState.IDLE
    pending_clarification: Optional[Dict] = None
    research_results: Optional[Dict] = None
    account_plan: Optional[Dict] = None
    user_preferences: Dict = field(default_factory=dict)
    mentioned_companies: List[str] = field(default_factory=list)


class ConversationManager:
    def __init__(self):
        self.persona_detector = PersonaDetector()
        self.response_generator = ResponseGenerator()
        self.context = ConversationContext()
        self.history: List[Message] = []
        self.max_history = 50
    
    def process_user_message(self, message: str) -> Dict[str, Any]:
        self.add_message("user", message)
        
        persona = self.persona_detector.analyze_message(message)
        
        result = self._determine_action(message, persona)
        
        if result.get("response"):
            self.add_message("assistant", result["response"], {
                "persona": persona,
                "state": self.context.state.value,
            })
        
        return result
    
    def _determine_action(self, message: str, persona: str) -> Dict[str, Any]:
        from utils.validators import (
            detect_input_intent, 
            extract_company_mentions,
            is_input_too_long
        )
        
        if is_input_too_long(message):
            return {
                "response": self._handle_long_input(persona),
                "action": "validation_error",
                "persona": persona,
            }
        
        if self.context.state == ConversationState.CLARIFYING:
            return self._handle_clarification(message, persona)
        
        intent = detect_input_intent(message)
        
        if intent == "command":
            companies = extract_company_mentions(message)
            
            if companies:
                return self._start_research(companies[0], persona)
            else:
                return {
                    "response": self.response_generator.generate(
                        "clarification",
                        persona,
                        count=0,
                        suggestion="Could you specify the company name?"
                    ),
                    "action": "request_company",
                    "persona": persona,
                }
        
        elif intent == "question":
            return self._handle_question(message, persona)
        
        elif intent == "clarification":
            return self._handle_clarification(message, persona)
        
        elif intent == "feedback":
            return self._handle_feedback(message, persona)
        
        else:
            companies = extract_company_mentions(message)
            
            if companies:
                return self._start_research(companies[0], persona)
            else:
                return {
                    "response": self.response_generator.generate(
                        "clarification",
                        persona,
                        suggestion="I can help you research companies. What company would you like to explore?"
                    ),
                    "action": "request_guidance",
                    "persona": persona,
                }
    
    def _start_research(self, company: str, persona: str) -> Dict[str, Any]:
        self.context.current_company = company
        self.context.state = ConversationState.RESEARCHING
        
        if company not in self.context.mentioned_companies:
            self.context.mentioned_companies.append(company)
        
        response = self.response_generator.generate(
            "acknowledgment",
            persona,
            company=company
        )
        
        return {
            "response": response,
            "action": "start_research",
            "company": company,
            "persona": persona,
        }
    
    def _handle_question(self, message: str, persona: str) -> Dict[str, Any]:
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["how", "what can", "help", "do"]):
            response = self._explain_capabilities(persona)
            return {
                "response": response,
                "action": "explain_capabilities",
                "persona": persona,
            }
        
        if self.context.current_company and any(
            word in message_lower for word in ["tell me", "what about", "more about"]
        ):
            return {
                "response": f"I can provide more details about {self.context.current_company}. Which aspect interests you? (e.g., financials, team, opportunities)",
                "action": "request_specific_info",
                "persona": persona,
            }
        
        return {
            "response": "I'm here to help you research companies. Could you ask your question in a different way, or tell me which company you'd like to explore?",
            "action": "clarify_question",
            "persona": persona,
        }
    
    def _handle_clarification(self, message: str, persona: str) -> Dict[str, Any]:
        if not self.context.pending_clarification:
            return self._determine_action(message, persona)
        
        clarification_type = self.context.pending_clarification.get("type")
        
        if clarification_type == "company_selection":
            self.context.state = ConversationState.RESEARCHING
            self.context.pending_clarification = None
            
            return {
                "response": "Great! Starting research...",
                "action": "research_confirmed",
                "persona": persona,
            }
        
        return {
            "response": "Thank you for clarifying. Let me proceed...",
            "action": "clarification_received",
            "persona": persona,
        }
    
    def _handle_feedback(self, message: str, persona: str) -> Dict[str, Any]:
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["thanks", "great", "perfect", "excellent"]):
            responses = {
                "confused": "You're welcome! Let me know if you need anything else.",
                "efficient": "Glad to help.",
                "chatty": "Aw, thanks! Happy to help! 😊 Anything else I can do for you?",
                "technical": "Acknowledgment received. Standing by for next request.",
                "neutral": "You're welcome! Let me know how I can help further.",
            }
            return {
                "response": responses.get(persona, responses["neutral"]),
                "action": "positive_feedback",
                "persona": persona,
            }
        
        if any(word in message_lower for word in ["wrong", "incorrect", "bad", "not good"]):
            return {
                "response": "I apologize for the error. How can I correct this for you?",
                "action": "negative_feedback",
                "persona": persona,
            }
        
        return {
            "response": "Thank you for your feedback!",
            "action": "feedback_received",
            "persona": persona,
        }
    
    def _handle_long_input(self, persona: str) -> str:
        responses = {
            "confused": "That's a lot of information! Could you summarize what you need in a sentence or two?",
            "efficient": "Input too long. Please provide concise request.",
            "chatty": "Whoa, that's quite a bit! 😅 Can you give me the key points in a shorter version?",
            "technical": "Input exceeds optimal length. Please provide summarized query (< 500 words).",
            "neutral": "Your message is quite long. Could you summarize your main request?",
        }
        return responses.get(persona, responses["neutral"])
    
    def _explain_capabilities(self, persona: str) -> str:
        explanations = {
            "confused": (
                "I can help you research companies! Just tell me a company name, "
                "and I'll gather information about them including news, financials, "
                "team members, and create an account plan. Easy!"
            ),
            "efficient": (
                "Capabilities: Company research, news aggregation, financial analysis, "
                "SWOT analysis, account plan generation, PDF/DOCX export."
            ),
            "chatty": (
                "Great question! I'm like your research assistant buddy! 🤓 "
                "I can look up any company, find the latest news, check out their "
                "team, analyze their financials, and create a full account plan. "
                "Plus, I can export everything to PDF or Word when you're done!"
            ),
            "technical": (
                "System capabilities:\n"
                "• Multi-source data aggregation (APIs, web scraping, documents)\n"
                "• Real-time news monitoring\n"
                "• Financial analysis and metrics extraction\n"
                "• SWOT framework generation\n"
                "• Account plan templating and export (PDF/DOCX)\n"
                "• Conversation state management with context retention"
            ),
            "neutral": (
                "I can research companies and generate account plans. "
                "I gather data from multiple sources including news, company websites, "
                "and databases. I can also help you analyze the information and export "
                "it in various formats."
            ),
        }
        return explanations.get(persona, explanations["neutral"])
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.history.append(message)
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_conversation_summary(self) -> str:
        if not self.history:
            return "No conversation yet."
        
        summary_parts = []
        
        if self.context.mentioned_companies:
            summary_parts.append(
                f"Companies discussed: {', '.join(self.context.mentioned_companies)}"
            )
        
        if self.context.current_company:
            summary_parts.append(f"Current focus: {self.context.current_company}")
        
        user_messages = sum(1 for m in self.history if m.role == "user")
        summary_parts.append(f"Messages exchanged: {user_messages}")
        
        persona = self.persona_detector.get_persona()
        summary_parts.append(f"Communication style: {persona}")
        
        return " | ".join(summary_parts)
    
    def reset(self):
        self.persona_detector.reset()
        self.context = ConversationContext()
        self.history = []
    
    def get_persona(self) -> str:
        return self.persona_detector.get_persona()
    
    def get_state(self) -> ConversationState:
        return self.context.state
    
    def set_state(self, state: ConversationState):
        self.context.state = state
    
    def get_history(self, limit: Optional[int] = None) -> List[Message]:
        if limit:
            return self.history[-limit:]
        return self.history
