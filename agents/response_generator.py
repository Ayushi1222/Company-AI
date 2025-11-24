import random
from typing import Dict, List, Optional
from datetime import datetime


class ResponseGenerator:
    def __init__(self):
        self.response_templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        return {
            "greeting": {
                "confused": [
                    "Hi! I'm here to help you research companies. What company would you like to learn about?",
                    "Hello! Let's get started. Which company should we research together?",
                ],
                "efficient": [
                    "Ready to research. Which company?",
                    "Hello! Company name?",
                ],
                "chatty": [
                    "Hey there! 👋 I'm excited to help you research companies and create awesome account plans! Which company caught your interest?",
                    "Hi! Great to meet you! I'm your company research assistant. Tell me, which company should we dive into?",
                ],
                "technical": [
                    "Company Research Assistant initialized. Please provide the target company name for analysis.",
                    "Ready to conduct comprehensive company analysis. Input company identifier.",
                ],
                "neutral": [
                    "Hello! I'm your Company Research Assistant. I can help you research companies and generate detailed account plans. Which company would you like to explore?",
                ],
            },
            "acknowledgment": {
                "confused": [
                    "Got it! Let me research {company} for you. This will take a moment...",
                    "Perfect! I'll look into {company}. Give me just a moment to gather information...",
                ],
                "efficient": [
                    "Researching {company}...",
                    "On it. Analyzing {company}...",
                ],
                "chatty": [
                    "Awesome! {company} is a great choice! Let me dive in and gather all the juicy details... 🔍",
                    "Ooh, {company}! I love researching them. Give me a moment to pull together everything...",
                ],
                "technical": [
                    "Initiating data collection for {company}. Sources: Web scraping, APIs, public databases.",
                    "Processing {company} research request. Aggregating multi-source intelligence...",
                ],
                "neutral": [
                    "Researching {company}. I'll gather information from multiple sources...",
                ],
            },
            "clarification": {
                "confused": [
                    "I found {count} companies with similar names. Could you help me identify which one?",
                    "Just to make sure I have the right company - did you mean {suggestion}?",
                ],
                "efficient": [
                    "{count} matches found. Which one?",
                    "Confirm: {suggestion}?",
                ],
                "chatty": [
                    "Hmm, I'm seeing {count} different companies with that name! Want to help me pick the right one?",
                    "Quick question - I want to make sure I'm looking at the right company. Is it {suggestion}?",
                ],
                "technical": [
                    "Query returned {count} entities. Disambiguation required. Primary match: {suggestion}",
                    "Multiple results detected. Please specify: {suggestion}",
                ],
                "neutral": [
                    "I found {count} companies matching that name. Which one would you like to research?",
                ],
            },
            "error": {
                "confused": [
                    "I'm having trouble finding information about {company}. Could you double-check the spelling or provide more details?",
                    "Hmm, I couldn't locate {company}. Can you tell me more about them? Maybe their industry or location?",
                ],
                "efficient": [
                    "Company not found: {company}. Check spelling?",
                    "{company} - no results. Alternative name?",
                ],
                "chatty": [
                    "Uh oh! I'm not finding anything for {company}. Maybe there's a typo? Or perhaps they go by a different name?",
                    "Hmm, {company} isn't showing up in my searches. Could you give me a bit more to go on?",
                ],
                "technical": [
                    "Search returned null results for entity: {company}. Verify identifier or provide alternate query.",
                    "No matching records for {company} in data sources. Suggestion: validate company name or use domain.",
                ],
                "neutral": [
                    "I couldn't find information about {company}. Please check the name and try again.",
                ],
            },
            "api_failure": {
                "confused": [
                    "I'm having a temporary issue with {service}, but don't worry - I'll use other sources to get you the information.",
                    "The {service} service isn't responding right now. Let me try a different approach...",
                ],
                "efficient": [
                    "{service} unavailable. Using alternative sources.",
                    "{service} down. Proceeding with other data.",
                ],
                "chatty": [
                    "Oops! {service} is being a bit moody right now, but no worries - I've got backup sources! 💪",
                    "So {service} decided to take a coffee break, but I've got plenty of other ways to get what you need!",
                ],
                "technical": [
                    "{service} API returned error code. Falling back to cached data and alternative endpoints.",
                    "Service interruption: {service}. Implementing fallback strategy.",
                ],
                "neutral": [
                    "The {service} service is temporarily unavailable. I'll use alternative data sources.",
                ],
            },
            "progress": {
                "confused": [
                    "I'm gathering information from {source}. Almost done!",
                    "Still working on it... currently checking {source}...",
                ],
                "efficient": [
                    "{source} - in progress",
                    "Fetching from {source}...",
                ],
                "chatty": [
                    "Making progress! Just pulled some great data from {source}... 📊",
                    "Looking good! I'm getting awesome info from {source}...",
                ],
                "technical": [
                    "Data extraction: {source} (Progress: {percent}%)",
                    "Processing {source} dataset...",
                ],
                "neutral": [
                    "Retrieving data from {source}...",
                ],
            },
            "completion": {
                "confused": [
                    "All done! I've created your account plan for {company}. Take a look and let me know if you want me to explore anything in more detail.",
                    "Here's your complete research on {company}! Feel free to ask me questions about any section.",
                ],
                "efficient": [
                    "{company} research complete. Review below.",
                    "Done. Account plan ready.",
                ],
                "chatty": [
                    "Woohoo! 🎉 I've finished researching {company}! Check out what I found - it's pretty interesting!",
                    "And we're done! I've put together a comprehensive account plan for {company}. What do you think?",
                ],
                "technical": [
                    "Data aggregation complete for {company}. Analysis compiled across {source_count} sources.",
                    "Research process completed. Account plan generated with {data_points} data points.",
                ],
                "neutral": [
                    "Research complete for {company}. Your account plan is ready below.",
                ],
            },
        }
    
    def generate(self, 
                 response_type: str, 
                 persona: str = "neutral", 
                 **kwargs) -> str:
        templates = self.response_templates.get(response_type, {}).get(persona, [])
        
        if not templates:
            templates = self.response_templates.get(response_type, {}).get("neutral", [])
        
        if not templates:
            return self._generate_fallback(response_type, **kwargs)
        
        template = random.choice(templates)
        
        try:
            response = template.format(**kwargs)
        except KeyError:
            response = template
        
        return response
    
    def _generate_fallback(self, response_type: str, **kwargs) -> str:
        fallbacks = {
            "greeting": "Hello! How can I help you today?",
            "acknowledgment": "Processing your request...",
            "clarification": "Could you provide more information?",
            "error": "Something went wrong. Please try again.",
            "progress": "Working on it...",
            "completion": "Task completed.",
        }
        return fallbacks.get(response_type, "I'm processing your request.")
    
    def generate_status_update(self, 
                              status: str, 
                              persona: str = "neutral",
                              **kwargs) -> str:
        status_messages = {
            "searching": self.generate("progress", persona, source="web sources", **kwargs),
            "api_call": self.generate("progress", persona, source=kwargs.get("api", "API"), **kwargs),
            "analyzing": "🧠 Analyzing data..." if persona == "chatty" else "Analyzing data...",
            "generating": "📋 Creating account plan..." if persona == "chatty" else "Generating plan...",
        }
        
        return status_messages.get(status, "Processing...")
    
    def generate_conflict_resolution(self,
                                    field: str,
                                    values: List[str],
                                    sources: List[str],
                                    persona: str = "neutral") -> str:
        intros = {
            "confused": f"I found different information about {field}. Let me show you what I have:",
            "efficient": f"Conflict in {field} data:",
            "chatty": f"Hey, so I'm seeing different info for {field}. Want to help me figure out which is correct?",
            "technical": f"Data inconsistency detected in field: {field}",
            "neutral": f"I found conflicting information for {field}:",
        }
        
        intro = intros.get(persona, intros["neutral"])
        
        conflicts = "\n".join([
            f"• {value} (from {source})" 
            for value, source in zip(values, sources)
        ])
        
        outros = {
            "confused": "\nWhich one seems right to you, or should I dig deeper?",
            "efficient": "\nSelect preferred source or request re-validation.",
            "chatty": "\nWhat do you think? Should I investigate further or go with one of these?",
            "technical": "\nAction required: Specify preferred source or initiate validation protocol.",
            "neutral": "\nWhich would you like me to use, or should I research further?",
        }
        
        outro = outros.get(persona, outros["neutral"])
        
        return f"{intro}\n\n{conflicts}\n{outro}"
    
    def generate_suggestion(self,
                          suggestion_type: str,
                          persona: str = "neutral",
                          **kwargs) -> str:
        suggestions = {
            "deep_dive": {
                "confused": "Would you like me to explain any of these sections in more detail?",
                "efficient": "Request deep dive on specific sections?",
                "chatty": "Want me to dig deeper into any particular area? I can find more details!",
                "technical": "Additional analysis available. Specify focus areas for detailed investigation.",
                "neutral": "Would you like more detailed information on any section?",
            },
            "export": {
                "confused": "You can download this plan as a PDF or Word document when you're ready!",
                "efficient": "Export options: PDF, DOCX",
                "chatty": "Looking good! Want to save this as a PDF or Word doc to share with your team?",
                "technical": "Export functionality available: PDF (ReportLab) / DOCX (python-docx)",
                "neutral": "You can export this plan as PDF or Word document.",
            },
        }
        
        return suggestions.get(suggestion_type, {}).get(persona, "")
