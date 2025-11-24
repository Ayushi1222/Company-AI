# Company Research Assistant & Account Plan Generator

AI-powered Streamlit app that researches companies from multiple sources and generates professional account plans in seconds.

## 🚀 Quick Start

```bash
# Setup
cd "d:\Company AI"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Configure API keys
cp .env.template .env
notepad .env  # Add your API keys

# Run
streamlit run app.py
```

## ✨ Features

- **Multi-source Research** - LinkedIn API, Hunter.io, Brandfetch, NewsAPI, Web Scraping
- **Smart Aggregation** - Prioritizes LinkedIn data, merges from 5+ sources
- **6-Section Account Plans** - Overview, Team, Financials, SWOT, Opportunities, Risks
- **Professional Exports** - PDF and DOCX formats
- **Conversational UI** - Adapts to your communication style
- **Clean Interface** - Minimalist design with proper spacing

## 🔑 API Keys Required

Get free API keys from:
- **NewsAPI**: https://newsapi.org/ (100/day FREE)
- **Hunter.io**: https://hunter.io/ (25/month FREE)
- **Brandfetch**: https://brandfetch.com/ (100/month FREE)
- **OpenAI**: https://platform.openai.com/ (Required for AI summaries)
- **LinkedIn**: https://www.linkedin.com/developers/ (Optional, OAuth required)
- **OpenCorporates**: Optional

Add to `.env`:
```env
NEWSAPI_KEY=your_key
HUNTER_API_KEY=your_key
BRANDFETCH_API_KEY=your_key
OPENAI_API_KEY=your_key
LINKEDIN_ACCESS_TOKEN=optional
OPENCORPORATES_API_KEY=optional
```

## � How It Works

1. **Input**: Type company name (e.g., "Research Microsoft")
2. **Research**: Fetches data from 5+ sources (5-10 seconds)
3. **Generate**: Creates 6-section account plan instantly
4. **Export**: Download as PDF or DOCX

### Data Sources (Priority Order)
1. LinkedIn API → Company profile, employees, HQ, founded
2. Hunter.io → Domain, email patterns
3. Brandfetch → Brand assets, social media
4. NewsAPI → Recent news articles
5. Web Scraper → Fallback extraction

## �️ Architecture

**Tech Stack**: Streamlit + OpenAI + LinkedIn API + Multi-source data aggregation

**Key Design Decisions**:
- Sequential API calls (no threading issues with Streamlit)
- LinkedIn data prioritized over other sources
- Graceful degradation when APIs fail
- SQLite for local storage
- BeautifulSoup4 for web scraping fallback

## 📁 Project Structure

```
├── app.py                     # Main Streamlit app
├── agents/                    # Conversation management
├── research/                  # APIs + web scraping
├── account_plan/              # Plan generation
├── export/                    # PDF/DOCX export
└── utils/                     # Helpers & validators
```

## 🎨 Account Plan Sections

1. **Overview** - Name, industry, founded, employees, HQ
2. **Team** - Leadership, executives
3. **Financials** - Revenue, funding, company type
4. **SWOT** - Strengths, weaknesses, opportunities, threats
5. **Opportunities** - Strategic fit, entry points
6. **Risks** - Competitive, financial, timing

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module errors | `pip install -r requirements.txt --upgrade` |
| "None" values | Add LinkedIn token or check company name |
| Slow (>30s) | Normal: 5-10s. Check internet/API keys |
| Export fails | `pip install reportlab python-docx --force-reinstall` |
| Cache issues | `streamlit cache clear` then reload browser |

---

##  GitHub Repository

**https://github.com/Ayushi1222/Company-AI**

```bash
# Clone
git clone https://github.com/Ayushi1222/Company-AI.git

# Update
git pull origin master
```

## 📞 Support & Contributing

- **Issues**: Open a GitHub issue
- **Questions**: Check TESTING.md for examples  
- **Contributions**: Fork → Branch → PR

---

**Built with ❤️ for intelligent company research and account planning**

**Version**: 1.0.0 | **Last Updated**: November 24, 2025 | **Author**: Ayushi1222
