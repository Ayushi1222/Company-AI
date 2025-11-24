"""
Demo script showcasing different user personas interacting with the assistant.

This script demonstrates how the conversational agent adapts to different
communication styles and handles various edge cases.
"""

# Test Scenarios for the Conversational Company Research Assistant

## Test Persona 1: Confused User
"""
User: "um i need info on that tech company"
Expected Agent Behavior:
- Ask clarifying questions
- Provide examples
- Be patient and helpful

Agent: "I'd be happy to help! Could you tell me the company name? For example, 'Microsoft' or 'Salesforce'."

User: "the one that makes iphones"
Agent: "Got it! You're looking for Apple Inc. Let me gather comprehensive information..."
[Proceeds with research]
"""

## Test Persona 2: Efficient User
"""
User: "Research Stripe, focus on recent funding and competitive position"
Expected Agent Behavior:
- Direct and concise responses
- Minimal small talk
- Quick execution

Agent: "Researching Stripe - prioritizing funding data and competitive analysis. One moment..."
[Returns structured data quickly]
[Presents key findings in bullet points]
"""

## Test Persona 3: Chatty User
"""
User: "Hey! So I'm thinking about Shopify, they're pretty cool right? My friend works there actually..."
Expected Agent Behavior:
- Conversational and warm
- Acknowledge comments
- Engage naturally

Agent: "Shopify is indeed impressive! Let me pull together their latest company data. Should I include info about their workplace culture since you have a connection there?"

User: "Yeah that would be awesome! Also what do you think about their stock lately?"
Agent: "I'll add culture info! As for stock - I focus on company research rather than investment advice, but I can show you their recent financial performance and growth metrics if that helps?"
"""

## Test Persona 4: Edge Case User
"""
Scenario A: Extremely long input
User: [Pastes 5000 word essay about various tech companies]
Expected Agent Behavior:
- Politely truncate/summarize
- Request clarification
- Stay helpful

Agent: "I received a large input. Could you summarize what you need in a sentence or two? For example: 'Research [Company] and focus on [specific areas]'."

Scenario B: Invalid company name
User: "Analyze xyzzqwert123"
Agent: "I couldn't find a company named 'xyzzqwert123'. Could you double-check the spelling or provide more context?"

Scenario C: Ambiguous company name
User: "Research Apple"
Agent: "I found 3 companies named 'Apple'. Did you mean Apple Inc. (tech company), Apple Records (music), or Apple Bank (financial)?"
"""

## Test Persona 5: Technical User
"""
User: "I need a comprehensive analysis of Salesforce including their ARR, customer acquisition costs, competitive moat, and technology stack. Focus on enterprise segment."

Expected Agent Behavior:
- Detailed technical responses
- Include metrics and data
- Professional terminology

Agent: "Initiating comprehensive Salesforce analysis. Data sources: Clearbit (firmographic), NewsAPI (market intelligence), web scraping (tech stack). Processing..."

[Returns detailed report with:]
- ARR: $31.35B (FY2024)
- Technology Stack: [List of technologies]
- Competitive Analysis: [Detailed breakdown]
- Enterprise Metrics: [Specific data points]
"""

## Edge Case Handling Examples

### 1. API Failure Scenario
"""
User: "Research Tesla"
[NewsAPI times out]

Agent Response (Confused User): "I'm having a temporary issue with the news service, but don't worry - I'll use other sources to get you the information."

Agent Response (Efficient User): "NewsAPI unavailable. Using alternative sources."

Agent Response (Technical User): "NewsAPI timeout detected. Falling back to web scraping + Clearbit. Estimated completion: 15s."
"""

### 2. Conflicting Data Scenario
"""
[During research, finds CEO name differs between sources]

Agent Response (Confused User):
"I found different information about the CEO. Let me show you what I have:
• Elon Musk (from company website, updated 2024)
• Elon Musk (from Clearbit, cached 2023)

Both sources agree - looks good! Proceeding with Elon Musk."

Agent Response (Technical User):
"Data inconsistency detected in field: CEO
• Source A (company_website): Elon Musk [Priority: 8, Fresh: 2024-11-24]
• Source B (clearbit): Elon Musk [Priority: 10, Cached: 2023-06-15]
Auto-resolved: Using Source B due to higher priority."
"""

### 3. Empty Results Scenario
"""
User: "Find information about Acme Corporation"
[No results found]

Agent Response (Confused User):
"Hmm, I'm not finding anything for 'Acme Corporation'. This could mean:
- The company name might be spelled differently
- It might be a very new or private company
- It could be operating under a different legal name

Could you provide more details like their website or what industry they're in?"

Agent Response (Efficient User):
"No results for 'Acme Corporation'. Verify spelling or provide domain/URL?"
"""

## Conversation Flow Test

### Full Interaction Example (Adaptive Agent)
"""
User: "hi"
Agent: "Hello! I'm your Company Research Assistant. I can help you research companies and generate detailed account plans. Which company would you like to explore?"

User: "um... i'm not sure exactly what you do?"
[Agent detects confusion, adjusts response style]
Agent: "No problem! I make it easy to research companies. Just tell me a company name (like 'Netflix' or 'Zoom'), and I'll:
1. Find the latest news about them
2. Get their company info (size, location, leadership)
3. Create a professional account plan you can download

Want to try it with a company you're curious about?"

User: "ok let's try Netflix"
Agent: "Perfect! Netflix is a great choice. Let me gather information for you. This will take about 30 seconds..."
[Shows progress indicators]
[Research completes]
Agent: "All done! I've created your account plan for Netflix. Take a look and let me know if you want me to explore anything in more detail. You can also download it as a PDF or Word document!"

User: "thanks! this is really helpful"
Agent: "You're welcome! Let me know if you need anything else."
"""

## Testing Checklist

Run through these scenarios to validate the agent:

□ Confused user gets clarifying questions
□ Efficient user gets direct, brief responses  
□ Chatty user gets conversational, friendly responses
□ Technical user gets detailed, data-driven responses
□ Long input is handled gracefully
□ Invalid company names produce helpful error messages
□ Ambiguous queries trigger clarification requests
□ API failures are transparently communicated with fallbacks
□ Conflicting data is detected and resolved (or user is asked)
□ Empty results provide actionable next steps
□ Persona detection adapts within 2-3 messages
□ Status updates are shown during long operations
□ Account plans are generated correctly
□ Export functionality works for both PDF and DOCX
□ Conversation history is maintained across interactions
□ Reset functionality clears state properly

## Performance Benchmarks

Target response times:
- Simple query processing: < 500ms
- Company research (all sources): 15-30 seconds
- Account plan generation: < 5 seconds
- PDF export: < 3 seconds
- DOCX export: < 2 seconds

User experience goals:
- Persona detection accuracy: > 80% by 3rd message
- API fallback success rate: > 95%
- User satisfaction (subjective): "Helpful and adaptive"
