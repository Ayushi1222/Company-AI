# Quick Start Guide

## 🚀 Setup & Run (5 Minutes)

### 1. Environment Setup
```bash
cd "d:\Company AI"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys (.env file)
```env
NEWSAPI_KEY=get_from_newsapi.org
HUNTER_API_KEY=get_from_hunter.io
BRANDFETCH_API_KEY=get_from_brandfetch.com
OPENAI_API_KEY=required_for_AI_summaries

LINKEDIN_CLIENT_ID=optional
LINKEDIN_CLIENT_SECRET=optional
LINKEDIN_ACCESS_TOKEN=optional

OPENCORPORATES_API_KEY=optional_skip_if_empty
```

**Get Free API Keys:**
- NewsAPI: https://newsapi.org/ (100/day FREE)
- Hunter.io: https://hunter.io/ (25/month FREE)
- Brandfetch: https://brandfetch.com/ (100/month FREE)
- OpenAI: https://platform.openai.com/ (Pay-per-use)

### 3. Run Application
```bash
streamlit run app.py
```
Open browser → `http://localhost:8501`

---

## 📋 Important Info

### What It Does
- Researches companies from multiple sources (LinkedIn, News, Web)
- Generates account plans (Overview, Team, Financials, SWOT, Opportunities, Risks)
- Exports to PDF/DOCX
- Adapts to your conversation style

### Data Sources Priority
1. **LinkedIn API** (best data: founded, industry, employees, HQ)
2. **Hunter.io** (domain, email patterns)
3. **Brandfetch** (logos, brand assets)
4. **NewsAPI** (recent news)
5. **Web Scraping** (fallback)

### Response Time
- Research: 5-10 seconds
- Account Plan: Instant
- Export: 2-3 seconds

---

## 🧪 Quick Test

### Test 1: Simple Research
```
You: "Research Microsoft"
Expected: Account plan generated in ~10 seconds
```

### Test 2: Specific Request
```
You: "Analyze Google, focus on AI products"
Expected: Detailed account plan with AI focus
```

### Test 3: Export
```
Click "Export as PDF" or "Export as DOCX"
Expected: Download professional report
```

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "None" values | Add LinkedIn API token or wait for web scraping |
| Slow response | Normal (5-10s for multiple API calls) |
| API errors | Check .env keys, some APIs optional |
| Module not found | `pip install -r requirements.txt` |

---

## 📝 Testing Checklist

### Must Test
- [ ] Company research completes successfully
- [ ] Account plan displays all 6 sections
- [ ] PDF export works
- [ ] DOCX export works
- [ ] Chat history maintained

### Optional Test
- [ ] LinkedIn data appears (if API configured)
- [ ] News articles loaded (if NewsAPI key valid)
- [ ] Multiple companies in same session

---

## 🔑 Key Features

1. **Multi-source aggregation** - Combines 5+ data sources
2. **Smart fallbacks** - Works even if some APIs fail
3. **Clean UI** - Simple, professional interface
4. **Adaptive conversation** - Detects your style
5. **Professional exports** - PDF & DOCX ready to share

---

## 💬 Sample Conversations

### Example 1: Basic Research
```
You: "Research Microsoft"
Bot: "Researching Microsoft. I'll gather information from multiple sources..."
Bot: "✅ Research complete for Microsoft! Review the account plan below."
→ Account plan shows: Overview, Team, Financials, SWOT, Opportunities, Risks
```

### Example 2: Specific Focus
```
You: "Analyze Tesla, focus on recent news"
Bot: "On it. Analyzing Tesla with emphasis on recent activity..."
Bot: "✅ Research complete! Check the Recent Activity section for latest news."
```

### Example 3: Export
```
You: "Export Microsoft plan as PDF"
→ Click "Export as PDF" button
→ professional_report.pdf downloads
```

---

## 🐛 Common Issues

**"None" or "N/A" in results:**
- Missing API keys → Add to .env
- LinkedIn not configured → Add token or use web scraping
- Company not found → Try domain name instead

**Slow performance:**
- Normal: 5-10 seconds (sequential API calls)
- Check terminal for specific API timeouts

**Import errors:**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📊 Expected Output

### Account Plan Structure:
1. **Overview** - Name, industry, founded, employees, HQ
2. **Team** - Leadership, executives, LinkedIn profiles
3. **Financials** - Revenue, funding, company type
4. **SWOT** - Strengths, weaknesses, opportunities, threats
5. **Opportunities** - Strategic fit, entry points
6. **Risks** - Competitive, financial, timing risks

### Export Formats:
- **PDF**: Professional, read-only report
- **DOCX**: Editable Word document

---

**That's it! Start with `streamlit run app.py` and type a company name.** 🚀
