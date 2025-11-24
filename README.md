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

- **LinkedIn API**: Official LinkedIn API integration for company profiles, employee counts, industry data, headquarters, founding year, and company type (requires OAuth tokens)
- **Web Scraping**: BeautifulSoup4-based scraper for company websites with social media link extraction (LinkedIn vanity names, Twitter handles)
- **News APIs**: Real-time headlines via NewsAPI (FREE: 100/day)
- **Company Enrichment**: Hunter.io API for email patterns and org data (FREE: 25/month)
- **Brand Information**: Brandfetch API for logos, colors, social links (FREE: 100/month)
- **Legal Registry**: OpenCorporates for official company information (optional, gracefully skipped if unavailable)
- **Smart Data Aggregation**: Prioritizes LinkedIn data, merges information from all sources, handles conflicts intelligently

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
- *Design*: Minimalist, clean UI with proper message spacing, simple CSS styling, no complex backgrounds

**Scraping: BeautifulSoup4**
- *Why*: Lightweight, perfect for targeted web scraping with social media link extraction
- *Features*: Extracts LinkedIn vanity names and Twitter handles from company websites
- *Tradeoff*: Less powerful than Scrapy but simpler and more reliable for single-page scraping

**APIs: LinkedIn, NewsAPI, Hunter.io, Brandfetch, OpenCorporates**
- *Why*: Mix of official APIs and free tiers - LinkedIn (official, requires OAuth), Hunter (25/mo FREE), Brandfetch (100/mo FREE), NewsAPI (100/day FREE)
- *Tradeoff*: Rate limits require intelligent caching and fallback strategies
- *Alternative to Clearbit*: Hunter.io provides domain/email data, Brandfetch provides brand assets, LinkedIn provides comprehensive company data
- *Sequential Processing*: Removed ThreadPoolExecutor to avoid Streamlit context issues, APIs called sequentially with proper error handling

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

Required API keys in `.env`:
```env
NEWSAPI_KEY=your_newsapi_key_here
HUNTER_API_KEY=your_hunter_key_here
BRANDFETCH_API_KEY=your_brandfetch_key_here
OPENAI_API_KEY=your_openai_key_here

LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

OPENCORPORATES_API_KEY=
```

**Note**: LinkedIn requires OAuth authentication. OpenCorporates is optional and will be gracefully skipped if not configured.

### 3. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🆕 Recent Updates & Improvements

### Version 1.0 - November 2025

**Major Enhancements:**
1. ✅ **LinkedIn API Integration**
   - Official LinkedIn API client with OAuth support
   - Extracts comprehensive company data from About section
   - Includes: founding year, industry, employee count, headquarters, company type
   - Retry logic with exponential backoff for reliability

2. ✅ **Enhanced Web Scraping**
   - BeautifulSoup4-based scraper with social media extraction
   - Automatically extracts LinkedIn vanity names from URLs
   - Extracts Twitter handles from company websites
   - Fallback mechanism when APIs are unavailable

3. ✅ **Smart Data Aggregation**
   - Prioritizes LinkedIn data over other sources
   - Intelligent merging of location/headquarters information
   - Conflict detection and resolution
   - Sequential API calls (no threading issues)

4. ✅ **Simplified, Clean UI**
   - Minimalist CSS with proper message spacing
   - Removed complex backgrounds and broken color values
   - Better chat message padding (1.5rem between messages)
   - Clean, professional appearance

5. ✅ **API Replacements**
   - Replaced Clearbit (deprecated) with Hunter.io + Brandfetch
   - All APIs use free tiers with graceful degradation
   - OpenCorporates made optional (skipped if unavailable)

6. ✅ **Code Quality**
   - All docstring comments removed for cleaner codebase
   - All hashtag comments removed
   - Improved error handling throughout
   - Fixed CSS syntax errors in PDF exporter

**Bug Fixes:**
- Fixed unterminated string literals in app.py
- Fixed incomplete HexColor values in pdf_exporter.py
- Resolved ThreadPoolExecutor context issues with Streamlit
- Fixed OpenCorporates 401 authentication errors
- Improved data retrieval reliability

## 🔧 Configuration

### API Keys (in .env)
- **NewsAPI**: Get free key at https://newsapi.org/ (100 requests/day)
- **Hunter.io**: Get free key at https://hunter.io/ (25 searches/month) - Replaces Clearbit
- **Brandfetch**: Get free key at https://brandfetch.com/ (100 requests/month) - For brand assets
- **LinkedIn API**: Requires OAuth setup at https://www.linkedin.com/developers/
  - Get Client ID and Client Secret
  - Obtain Access Token via OAuth 2.0 flow
  - Provides: company profiles, employee counts, headquarters, founding year, industry
- **OpenAI**: Required for AI-powered summaries and account plan generation
- **OpenCorporates**: Optional, for legal entity data (gracefully skipped if not available)

### Feature Flags
Edit `config/settings.py`:
```python
FEATURES = {
    'text_to_speech': True,
    'pdf_export': True,
    'docx_export': True,
    'analytics': True,
    'linkedin_api': True,
    'web_scraping': True
}
```

## 🏛️ Architecture Deep Dive

### Data Flow Architecture

```
User Input → Conversation Manager → Research Orchestration
                                            ↓
                    ┌───────────────────────┴───────────────────────┐
                    ↓                       ↓                       ↓
              LinkedIn API          Hunter.io API           Brandfetch API
              (Priority 1)          (Priority 2)            (Priority 3)
                    ↓                       ↓                       ↓
              NewsAPI                 OpenCorporates          Web Scraper
              (Priority 4)            (Priority 5)            (Fallback)
                    ↓                       ↓                       ↓
                    └───────────────────────┬───────────────────────┘
                                            ↓
                                  Data Aggregator
                              (Smart Consolidation)
                                            ↓
                                  Account Plan Generator
                                            ↓
                              ┌─────────────┴─────────────┐
                              ↓                           ↓
                        Streamlit UI              Export (PDF/DOCX)
```

### Design Decisions & Rationale

#### 1. **Sequential API Calls vs. Parallel**
- **Decision**: Sequential processing (removed ThreadPoolExecutor)
- **Rationale**: Streamlit's context management conflicts with thread pools
- **Tradeoff**: Slower execution (~5-10s) but 100% reliable
- **Future**: Consider async/await pattern for Streamlit 1.30+

#### 2. **LinkedIn API Priority**
- **Decision**: LinkedIn data prioritized over all other sources
- **Rationale**: Most accurate, official company information
- **Implementation**: `SOURCE_PRIORITIES = {'linkedin': 5, 'hunter': 4, ...}`
- **Fallback**: Gracefully degrades to web scraping if API unavailable

#### 3. **BeautifulSoup4 vs. Scrapy**
- **Decision**: Switched from Scrapy to BeautifulSoup4
- **Rationale**: 
  - Simpler for single-page scraping
  - No middleware/pipeline complexity
  - Better integration with Streamlit
  - Easier social media link extraction
- **Tradeoff**: Less powerful for large-scale scraping

#### 4. **No Comment Policy**
- **Decision**: Removed all docstrings and hashtag comments
- **Rationale**: User preference for cleaner codebase
- **Maintained**: Function names remain self-documenting
- **Documentation**: Comprehensive README compensates

#### 5. **Error Handling Strategy**
- **Decision**: Graceful degradation with user notification
- **Implementation**:
  ```python
  try:
      linkedin_data = fetch_linkedin()
  except Exception as e:
      logger.error(f"LinkedIn failed: {e}")
      linkedin_data = None  # Continue with other sources
  ```
- **User Experience**: "LinkedIn unavailable, using 4 other sources..."

#### 6. **State Management**
- **Decision**: Streamlit session_state for all conversation context
- **Rationale**: Native, reliable, no external dependencies
- **Scope**: 
  - `session_state.messages` - chat history
  - `session_state.current_research` - latest company data
  - `session_state.current_plan` - generated account plan
  - `session_state.conversation_manager` - agent state

#### 7. **Export Format Support**
- **Decision**: Both PDF (ReportLab) and DOCX (python-docx)
- **Rationale**: 
  - PDF for read-only professional reports
  - DOCX for editable, customizable documents
- **Implementation**: Separate exporter classes with shared data model

#### 8. **Database Choice**
- **Decision**: SQLite with SQLAlchemy ORM
- **Rationale**: 
  - Zero-config, perfect for local development
  - Easy migration to PostgreSQL for production
  - ORM provides flexibility
- **Schema**: Conversations, AccountPlans, Analytics tables

### Performance Optimizations

1. **Caching Strategy**
   - Session-level caching for API responses
   - 5-minute cache for news articles
   - Persistent cache for company logos/brands

2. **Rate Limiting**
   - Built-in delays between API calls
   - Exponential backoff on failures
   - Request counting per session

3. **Lazy Loading**
   - Account plan sections generated on-demand
   - Export files created only when requested
   - Heavy computations deferred until needed

### Security Considerations

1. **API Key Protection**
   - `.env` file gitignored
   - Keys loaded via `os.getenv()`
   - No hardcoded credentials

2. **Input Validation**
   - Company name sanitization
   - Domain validation
   - File upload size limits

3. **Web Scraping Ethics**
   - User-Agent identification
   - Rate limiting (2-3s delays)
   - Respect robots.txt
   - No personal data scraping

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
│   ├── news_api.py                # NewsAPI integration
│   ├── hunter_api.py              # Hunter.io for email/domain data
│   ├── brandfetch_api.py          # Brandfetch for brand assets
│   ├── linkedin_api.py            # LinkedIn API client with retry logic
│   ├── opencorporates_api.py      # Company registry data (optional)
│   ├── web_scraper.py             # BeautifulSoup4 scraper with social media extraction
│   ├── pdf_parser.py              # Document extraction
│   └── data_aggregator.py         # Smart multi-source data consolidation
│

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

### Common Issues & Solutions

#### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

#### Streamlit not loading
```bash
streamlit cache clear
streamlit run app.py --server.port 8501
```

#### API rate limits exceeded
- Check your API key quotas at provider dashboards
- Wait for rate limit reset (usually 24 hours)
- Consider upgrading API plans for higher limits

#### LinkedIn API 401 errors
- Verify your access token is valid and not expired
- Re-authenticate via LinkedIn OAuth flow
- Check Client ID and Client Secret are correct
- Token typically expires after 60 days

#### "None" values in company info
- Ensure LinkedIn API is configured with valid access token
- Check that company exists on LinkedIn
- Try using company domain instead of name
- Web scraper will attempt fallback extraction

#### CSS/UI rendering issues
```bash
# Clear Streamlit cache
streamlit cache clear

# Hard reload browser
Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
```

#### Data aggregation taking too long
- Normal: 5-10 seconds for sequential API calls
- If > 30 seconds, check internet connection
- Some APIs (OpenCorporates) may timeout - this is normal
- Check terminal for specific API errors

#### Export button not working
```bash
# Reinstall export dependencies
pip install reportlab python-docx --force-reinstall
```

#### Web scraping fails
- Check if website is accessible in browser
- Some sites block automated requests
- Try different company domain
- LinkedIn API should work as primary source

### Debug Mode

Enable verbose logging in `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs in terminal for detailed error messages.

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

## 📦 GitHub Repository

This project is hosted at: **https://github.com/Ayushi1222/Company-AI**

### Initial Setup
```bash
cd "d:\Company AI"

# Initialize git (already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Company Research Assistant with LinkedIn API integration"

# Add remote
git remote add origin https://github.com/Ayushi1222/Company-AI.git

# Push to GitHub
git push -u origin master
```

### Keeping Up to Date
```bash
# Pull latest changes
git pull origin master

# Make changes, then commit and push
git add .
git commit -m "Your commit message"
git push origin master
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Test all API integrations thoroughly
- Update README for new features
- Ensure backward compatibility
- Add error handling for external dependencies

## 📞 Support

For issues or questions:
- Open a GitHub issue
- Check the FAQ in the app sidebar
- Review test scenarios in this README

---

## 🚀 Quick Start Commands

```bash
# Clone and setup
git clone https://github.com/Ayushi1222/Company-AI.git
cd Company-AI
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure
cp .env.template .env
notepad .env  # Add your API keys

# Run
streamlit run app.py

# Access
# Open browser to http://localhost:8501
```

## 📋 API Key Checklist

- [ ] NewsAPI key (Required) - https://newsapi.org/
- [ ] Hunter.io key (Required) - https://hunter.io/
- [ ] Brandfetch key (Required) - https://brandfetch.com/
- [ ] OpenAI key (Required) - https://platform.openai.com/
- [ ] LinkedIn OAuth (Optional but recommended) - https://www.linkedin.com/developers/
- [ ] OpenCorporates key (Optional) - https://opencorporates.com/

## 📞 Support & Resources

- **GitHub Issues**: https://github.com/Ayushi1222/Company-AI/issues
- **Documentation**: This README
- **API Docs**: 
  - LinkedIn: https://docs.microsoft.com/en-us/linkedin/
  - Hunter.io: https://hunter.io/api-documentation/v2
  - Brandfetch: https://docs.brandfetch.com/
  - NewsAPI: https://newsapi.org/docs

## 🏆 Acknowledgments

- Streamlit for the amazing framework
- OpenAI for GPT integration
- All API providers for their generous free tiers
- The open-source community

---

**Built with ❤️ for intelligent company research and account planning**

**Version**: 1.0.0 | **Last Updated**: November 24, 2025 | **Author**: Ayushi1222
