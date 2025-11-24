# Conversational Company Research Assistant & Account Plan Generator

## 🎯 Overview

An intelligent, conversational Streamlit application that conducts comprehensive company research and generates actionable account plans through natural dialogue. This agent prioritizes user experience, transparency, and adaptability across diverse interaction patterns.

## 🌟 Key Features

### 1. **Conversational Agent Interface**
- **Multi-turn dialogue**: Natural conversation flow with context retention
- **Persistent state**: Conversation history maintained via Streamlit session_state
- **Adaptive responses**: Agent adjusts to user style (confused, efficient, chatty, edge-case)

### 2. **Comprehensive Data Research**
The agent aggregates company intelligence from multiple sources:

- **Web Scraping**: Custom Scrapy spiders for company websites, news articles, and public data
- **News APIs**: Real-time headlines via NewsAPI/GNews
- **Company Enrichment**: Hunter.io API for email patterns and org data (FREE: 25/month)
- **Brand Information**: Brandfetch API for logos, colors, social links (FREE: 100/month)
- **Legal Registry**: OpenCorporates for official company information
- **Document Parsing**: Extract insights from uploaded PDFs/documents
- **LinkedIn Data**: Public profile information (respecting ToS)

### 3. **Intelligent Account Plan Generation**
Automatically generates and organizes:
- **Company Overview**: Mission, products, market position
- **Leadership Team**: Key executives and decision-makers
- **Financials**: Revenue, funding, growth metrics
- **SWOT Analysis**: Strengths, weaknesses, opportunities, threats
- **Opportunities**: Strategic engagement points
- **Risk Assessment**: Potential challenges and mitigation

### 4. **Transparency & Agentic Behavior**
- **Real-time status updates**: "Researching company news...", "Analyzing financials..."
- **Conflict resolution**: "Found two different revenue figures—would you like me to investigate further?"
- **Proactive suggestions**: "I notice this is a SaaS company. Should I focus on recurring revenue metrics?"
- **Editable sections**: Users can correct, update, or regenerate any part of the plan

### 5. **Export & Sharing**
- **Multiple formats**: PDF, Word (DOCX)
- **Professional formatting**: Clean, business-ready output
- **Optional**: Shareable links, email distribution

### 6. **Accessibility Features**
- **Text-to-Speech**: Read sections aloud via gTTS/pyttsx3
- **Voice input**: (Future enhancement)
- **Keyboard navigation**: Full accessibility support

### 7. **Robust Error Handling**
- API timeout recovery
- Invalid input validation with helpful prompts
- Graceful degradation when sources are unavailable
- Clear, actionable error messages

## 🏗️ Architecture & Design Decisions

### Technology Stack

**Frontend/UI: Streamlit**
- *Why*: Rapid development, native Python integration, excellent for conversational UIs
- *Tradeoff*: Less control than React but faster iteration for data apps

**Scraping: Scrapy**
- *Why*: Industrial-strength, respects robots.txt, excellent for modular multi-source scraping
- *Tradeoff*: Steeper learning curve than BeautifulSoup but better for production

**APIs: NewsAPI, Hunter.io, Brandfetch, OpenCorporates**
- *Why*: All offer genuine FREE tiers (not just trials) - Hunter (25/mo), Brandfetch (100/mo)
- *Tradeoff*: Rate limits require intelligent caching and fallback strategies
- *Alternative to Clearbit*: Hunter.io provides domain/email data, Brandfetch provides brand assets

**AI: OpenAI GPT (Optional)**
- *Why*: High-quality summarization and analysis
- *Tradeoff*: Cost per request; fallback to rule-based summaries available

**Export: python-docx, ReportLab**
- *Why*: Native Python libraries for professional document generation
- *Tradeoff*: Complex formatting requires more code than templates

**Database: SQLite**
- *Why*: Zero-config, perfect for local drafts and history
- *Tradeoff*: Not suitable for multi-user production (upgrade to PostgreSQL if needed)

### Conversation Management Strategy

The agent employs a **state-machine approach** with conversational memory:

1. **Context Tracking**: Maintains user intent, mentioned companies, and clarification needs
2. **Turn Management**: Detects questions, commands, confirmations, and tangents
3. **Adaptive Response**: Matches user communication style:
   - **Confused users**: Ask clarifying questions, provide examples
   - **Efficient users**: Direct answers, minimal fluff
   - **Chatty users**: Engage naturally, track topic changes
   - **Edge cases**: Validate inputs, suggest alternatives

4. **Transparency Loop**:
   ```
   User Request → Agent Acknowledgment → Status Updates → Results → Verification
   ```

### Edge Case Handling

**Scenario: Ambiguous Company Name**
- Agent asks: "I found 3 companies named 'Apple'. Did you mean Apple Inc. (tech), Apple Records (music), or Apple Bank?"

**Scenario: API Failure**
- Agent notifies: "NewsAPI is temporarily unavailable. I'll proceed with web scraping and cached data."

**Scenario: Conflicting Data**
- Agent presents: "Source A says $500M revenue; Source B says $450M. Would you like me to prioritize the more recent source?"

**Scenario: Out-of-Scope Request**
- Agent responds: "I specialize in company research. For personal profiles, I recommend LinkedIn directly."

## 🧪 Testing & Demo Scenarios

### Test Persona 1: Confused User
```
User: "um i need info on that tech company"
Agent: "I'd be happy to help! Could you tell me the company name? For example, 'Microsoft' or 'Salesforce'."
User: "the one that makes iphones"
Agent: "Got it! You're looking for Apple Inc. Let me gather comprehensive information..."
```

### Test Persona 2: Efficient User
```
User: "Research Stripe, focus on recent funding and competitive position"
Agent: "Researching Stripe - prioritizing funding data and competitive analysis. One moment..."
[Returns structured data in 30 seconds]
```

### Test Persona 3: Chatty User
```
User: "Hey! So I'm thinking about Shopify, they're pretty cool right? My friend works there actually..."
Agent: "Shopify is indeed impressive! Let me pull together their latest company data. Should I include info about their workplace culture since you have a connection there?"
```

### Test Persona 4: Edge Case User
```
User: [Pastes 5000 word essay]
Agent: "I received a large input. Could you summarize what you need in a sentence or two? For example: 'Research [Company] and focus on [specific areas]'."

User: "Analyze xyzzqwert123"
Agent: "I couldn't find a company named 'xyzzqwert123'. Could you double-check the spelling or provide more context?"
```

## 📦 Installation & Setup

### 1. Clone and Setup Environment
```bash
# Navigate to project directory
cd "d:\Company AI"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys
```bash
# Copy template
cp .env.template .env

# Edit .env with your actual API keys
notepad .env  # Windows
nano .env     # Linux/Mac
```

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔧 Configuration

### API Keys (in .env)
- **NewsAPI**: Get free key at https://newsapi.org/ (100 requests/day)
- **Hunter.io**: Get free key at https://hunter.io/ (25 searches/month) 
- **Brandfetch**: Get free key at https://brandfetch.com/ (100 requests/month)
- **OpenAI**: Optional, for AI-powered summaries
- **OpenCorporates**: Optional, for legal entity data

### Scraping Settings
Edit `config/scraper_config.py`:
```python
RESPECT_ROBOTS_TXT = True
DOWNLOAD_DELAY = 2  # seconds between requests
CONCURRENT_REQUESTS = 8
USER_AGENT = "Your custom user agent"
```

## 📁 Project Structure

```
Company AI/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.template                   # API key template
├── .env                           # Actual API keys (gitignored)
├── README.md                       # This file
│
├── agents/                         # Conversational agent logic
│   ├── __init__.py
│   ├── conversation_manager.py    # Dialogue flow and state management
│   ├── persona_detector.py        # Detect user communication style
│   └── response_generator.py      # Generate adaptive responses
│
├── research/                       # Data collection modules
│   ├── __init__.py
│   ├── news_api.py                # NewsAPI/GNews integration
│   ├── clearbit_api.py            # Clearbit enrichment
│   ├── opencorporates_api.py      # Company registry data
│   ├── pdf_parser.py              # Document extraction
│   └── data_aggregator.py         # Combine all sources
│
├── scrapers/                       # Scrapy spiders
│   ├── scrapy.cfg
│   ├── spiders/
│   │   ├── __init__.py
│   │   ├── company_spider.py      # Main company website scraper
│   │   ├── news_spider.py         # News article scraper
│   │   └── linkedin_spider.py     # LinkedIn public data
│   └── pipelines.py               # Data processing pipelines
│
├── account_plan/                   # Plan generation
│   ├── __init__.py
│   ├── generator.py               # Plan structure and logic
│   ├── sections.py                # Individual section generators
│   └── templates.py               # Output templates
│
├── export/                         # Document export
│   ├── __init__.py
│   ├── pdf_exporter.py            # PDF generation
│   └── docx_exporter.py           # Word document generation
│
├── database/                       # Local storage
│   ├── __init__.py
│   ├── models.py                  # SQLAlchemy models
│   └── crud.py                    # Database operations
│
├── utils/                          # Utilities
│   ├── __init__.py
│   ├── validators.py              # Input validation
│   ├── error_handlers.py          # Error handling
│   └── tts.py                     # Text-to-speech
│
└── config/                         # Configuration
    ├── __init__.py
    └── settings.py                # App settings
```

## 🎨 UI Components

### Chat Interface
- Message bubbles with timestamps
- User vs. Agent message distinction
- Status indicators (typing, processing, error)

### Account Plan Tabs
1. **Overview**: Company basics
2. **Team**: Leadership profiles
3. **Financials**: Revenue, funding, metrics
4. **SWOT**: Analysis framework
5. **Opportunities**: Sales/partnership angles
6. **Risks**: Challenges and mitigation

### Interactive Elements
- File uploader for PDFs
- Editable text areas for each section
- Regenerate buttons
- Export dropdown
- TTS playback controls

## 🔒 Best Practices & Ethics

### Web Scraping
- ✅ Respect robots.txt
- ✅ Rate limiting (2-3 seconds between requests)
- ✅ Identify with proper User-Agent
- ✅ Cache results to minimize requests
- ❌ Never scrape personal data without consent
- ❌ Don't overwhelm servers

### API Usage
- Implement exponential backoff on failures
- Cache responses when possible
- Monitor rate limits
- Provide fallback data sources

### Data Privacy
- Don't store sensitive user inputs long-term
- Encrypt API keys
- Allow users to delete their data
- Be transparent about data sources

## 🚀 Future Enhancements

- [ ] Multi-language support
- [ ] Voice input via Web Speech API
- [ ] Collaboration features (shared plans)
- [ ] Advanced analytics dashboard
- [ ] Integration with CRM systems (Salesforce, HubSpot)
- [ ] Email/Slack notifications
- [ ] Custom scraping templates per industry
- [ ] A/B testing different conversation strategies

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### Scrapy SSL errors
```bash
pip install 'scrapy[ssl]'
```

### Streamlit not loading
```bash
streamlit cache clear
```

### API rate limits
- Check your API key quotas
- Increase SCRAPING_DELAY in .env
- Consider upgrading API plans

## 📊 Analytics & Monitoring

The app tracks (stored locally in SQLite):
- Number of companies researched
- Most popular sections viewed
- Export frequency by format
- Average conversation length
- User satisfaction ratings

Access analytics via the "Analytics" tab in the sidebar.

## 📝 License

MIT License - Feel free to use and modify for your needs.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check the FAQ in the app sidebar
- Review test scenarios in this README

---

**Built with ❤️ for intelligent company research and account planning**
