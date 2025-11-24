# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### 1. Setup Environment

```powershell
# Navigate to project directory
cd "D:\Company AI"

# Virtual environment is already created!
# Activate it:
.\venv\Scripts\Activate.ps1

# All dependencies are already installed!
```

### 2. Configure API Keys (Optional)

The app works without API keys but with limited functionality. For full features:

1. Copy `.env.template` to `.env` (or edit the existing `.env`)
2. Add your API keys:

```bash
# Get free API keys from:
NEWSAPI_KEY=your_key_here           # https://newsapi.org/ (free: 100 req/day)
HUNTER_API_KEY=your_key_here        # https://hunter.io/ (free: 25 searches/month)
BRANDFETCH_API_KEY=your_key_here    # https://brandfetch.com/ (free: 100 req/month)
OPENAI_API_KEY=your_key_here        # https://openai.com/ (optional, for AI summaries)
```

**Note:** The app will work even without API keys - it will use web scraping and cached data!

### 3. Run the Application

```powershell
# Option 1: Use the run script
.\run_app.ps1

# Option 2: Run directly
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 4. Try Your First Research

1. Type in the chat: **"Research Microsoft"**
2. Watch the agent gather data from multiple sources
3. Review the generated account plan
4. Export as PDF or Word document!

## 🎭 Test Different User Personas

### Confused User Mode
```
Type: "um i need info on that tech company"
The agent will ask clarifying questions and guide you step-by-step.
```

### Efficient User Mode
```
Type: "Research Stripe, focus on financials"
The agent will be concise and direct.
```

### Chatty User Mode
```
Type: "Hey! So I'm thinking about researching Shopify, they're pretty cool right?"
The agent will be conversational and engaging.
```

### Technical User Mode
```
Type: "Analyze Salesforce with focus on ARR, tech stack, and competitive moat"
The agent will provide detailed technical data.
```

## 📊 Features to Explore

1. **Multi-Source Research**
   - Type any company name
   - Agent aggregates data from multiple APIs and web sources
   - Handles conflicting data intelligently

2. **Interactive Account Plan**
   - Six comprehensive sections (Overview, Team, Financials, SWOT, Opportunities, Risks)
   - Editable content (feature coming soon)
   - Professional formatting

3. **Export Options**
   - PDF export with professional styling
   - Word DOCX export for easy editing
   - Timestamped filenames

4. **Conversational Intelligence**
   - Agent adapts to your communication style
   - Asks clarifying questions when needed
   - Provides status updates during research

5. **Error Handling**
   - Graceful API fallbacks
   - Clear error messages
   - Helpful suggestions

## 🔧 Troubleshooting

### App won't start?
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Verify streamlit is installed
pip list | Select-String streamlit

# If not installed
pip install streamlit
```

### Import errors?
```powershell
# Reinstall all dependencies
pip install -r requirements.txt
```

### API not working?
- The app works without API keys!
- Check `.env` file for correct key format
- Verify API key validity on provider websites
- Check API rate limits (free tiers have limits)

### Port already in use?
```powershell
# Run on different port
streamlit run app.py --server.port 8502
```

## 📖 Usage Examples

### Example 1: Basic Company Research
```
You: "Research Tesla"
Agent: "Researching Tesla. I'll gather information from multiple sources..."
[30 seconds later]
Agent: "Research complete for Tesla! Review the account plan below."
[Account plan displayed with tabs]
```

### Example 2: Specific Focus Area
```
You: "Find info about Stripe, especially their funding"
Agent: "Researching Stripe - prioritizing funding data..."
[Results include detailed financial section]
```

### Example 3: Handling Ambiguity
```
You: "Research Apple"
Agent: "I found 3 companies named 'Apple'. Did you mean Apple Inc. (tech), Apple Records (music), or Apple Bank?"
You: "The tech company"
Agent: "Got it! Researching Apple Inc..."
```

### Example 4: Follow-up Questions
```
You: "Research Shopify"
[Research completes]
You: "Tell me more about their leadership team"
Agent: "Here's detailed information about Shopify's leadership..."
```

## 🎯 Pro Tips

1. **Be Specific**: "Research Salesforce with focus on enterprise segment" works better than just "Salesforce"

2. **Provide Domains**: If available, mention the domain: "Research stripe.com"

3. **Upload Documents**: Use the file uploader (sidebar) to extract company info from PDFs

4. **Check Sources**: Expand "Research Data Summary" to see which sources provided data

5. **Handle Conflicts**: If the agent finds conflicting data, it will ask for your input

6. **Export Early**: Generate your export before starting a new research to avoid losing data

7. **Use Reset Wisely**: "New Conversation" button clears everything - export first!

## 🏗️ Architecture Overview

```
User Input → Persona Detection → Intent Analysis → Action Routing
                                                          ↓
                                                 Research Orchestration
                                                          ↓
                                    ┌────────────────────┴────────────────────┐
                                    ↓                    ↓                    ↓
                              NewsAPI/GNews      Hunter.io/Brandfetch   OpenCorporates
                                    ↓                    ↓                    ↓
                                    └────────────────────┬────────────────────┘
                                                         ↓
                                                 Data Aggregation
                                                         ↓
                                                 Conflict Resolution
                                                         ↓
                                                Account Plan Generation
                                                         ↓
                                                 Present to User
                                                         ↓
                                                Export (PDF/DOCX)
```

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Testing Scenarios**: See `TESTING.md`
- **API Configuration**: See `.env.template`
- **Code Structure**: Browse the `/agents`, `/research`, `/account_plan` folders

## 🤝 Need Help?

1. Check the sidebar "❓ Help & Examples" in the app
2. Review error messages - they're designed to be helpful!
3. Look at `TESTING.md` for expected behaviors
4. Check logs for detailed error information

## 🎉 Have Fun!

This agent is designed to be:
- **Intelligent**: Adapts to how you communicate
- **Transparent**: Shows you what it's doing
- **Helpful**: Guides you when you're stuck
- **Robust**: Handles errors gracefully

Try breaking it! The best way to learn is to experiment with different queries, personas, and edge cases.

---

**Ready to start?** Run `streamlit run app.py` and begin researching! 🚀
