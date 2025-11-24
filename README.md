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

### 🔐 How to Generate LinkedIn Access Token

LinkedIn uses OAuth 2.0. Follow these steps:

**1. Create LinkedIn App**
- Go to https://www.linkedin.com/developers/apps
- Click "Create app"
- Fill in: App name, LinkedIn Page, App logo
- Check "Sign In with LinkedIn" product
- Submit for verification

**2. Get Credentials**
- Go to "Auth" tab in your app
- Copy **Client ID** and **Client Secret**
- Add redirect URL: `http://localhost:8501/callback`

**3. Generate Access Token**

**Option A - Using OAuth Playground:**
```bash
# Authorization URL (paste in browser)
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8501/callback&scope=r_organization_social%20r_basicprofile%20r_1st_connections_size

# After authorization, you'll get a CODE in the URL
# Exchange code for token:
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d "grant_type=authorization_code" \
  -d "code=YOUR_CODE" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:8501/callback"
```

**Option B - Using Python:**
```python
import requests

# Step 1: Visit this URL in browser
auth_url = f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8501/callback&scope=r_organization_social"

# Step 2: After authorization, extract code from redirect URL
# Step 3: Exchange code for token
response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data={
    'grant_type': 'authorization_code',
    'code': 'CODE_FROM_STEP_2',
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'redirect_uri': 'http://localhost:8501/callback'
})

token = response.json()['access_token']
print(f"Access Token: {token}")
```

**4. Add to .env**
```env
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token_from_step_3
```

**Note**: LinkedIn access tokens expire after **60 days**. You'll need to regenerate them periodically.

**Required Scopes**:
- `r_organization_social` - Read organization data
- `r_basicprofile` - Read basic profile
- `r_1st_connections_size` - Read connection count

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
