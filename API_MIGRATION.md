# API Services Update - Clearbit Replacement

## 🔄 Why the Change?

Clearbit discontinued free account creation, making it unavailable for new users. We've replaced it with **two excellent free alternatives** that together provide even better coverage:

### New Services (100% FREE)

1. **Hunter.io** 🎯
   - **Free Tier**: 25 domain searches per month
   - **Provides**: Company email patterns, organization info, employee estimates, social media links
   - **Sign up**: https://hunter.io/users/sign_up
   - **Documentation**: https://hunter.io/api-documentation

2. **Brandfetch** 🎨
   - **Free Tier**: 100 requests per month  
   - **Provides**: Company logos, brand colors, descriptions, industry, social media
   - **Sign up**: https://brandfetch.com/ (API key in dashboard)
   - **Documentation**: https://docs.brandfetch.com/

## ✅ What Changed

### Code Updates
- ✅ Removed `clearbit_api.py`
- ✅ Added `hunter_api.py` - Email & org data
- ✅ Added `brandfetch_api.py` - Brand & visual data
- ✅ Updated `data_aggregator.py` to use new services
- ✅ Updated `.env` configuration
- ✅ Updated all documentation

### Data Coverage Comparison

| Feature | Clearbit | Hunter.io | Brandfetch | Coverage |
|---------|----------|-----------|------------|----------|
| Company Name | ✅ | ✅ | ✅ | ✅ Better |
| Domain | ✅ | ✅ | ✅ | ✅ Same |
| Logo | ✅ | ❌ | ✅ | ✅ Same |
| Description | ✅ | ❌ | ✅ | ✅ Same |
| Employee Count | ✅ | ✅ (approx) | ❌ | ✅ Same |
| Revenue | ✅ | ❌ | ❌ | ⚠️ Lost |
| Industry | ✅ | ❌ | ✅ | ✅ Same |
| Social Media | ✅ | ✅ | ✅ | ✅ Better |
| Email Patterns | ❌ | ✅ | ❌ | 🎉 NEW! |
| Brand Colors | ❌ | ❌ | ✅ | 🎉 NEW! |
| **Free Tier** | ❌ Gone | ✅ 25/mo | ✅ 100/mo | ✅ FREE! |

### What You Gain 🎉
- **Email Patterns**: Hunter.io shows company email formats (e.g., {first}.{last}@company.com)
- **Brand Assets**: Brandfetch provides high-quality logos and brand colors
- **Higher Limits**: 125 total free API calls vs Clearbit's discontinued free tier
- **Better Social Coverage**: Both services provide comprehensive social media links

### What You Lose ⚠️
- **Revenue Data**: Neither free service provides financial metrics
  - *Workaround*: Can be supplemented with OpenCorporates (for public companies) or manual research
- **Technology Stack**: Clearbit showed tech used by companies
  - *Workaround*: Can scrape from BuiltWith or Wappalyzer

## 🚀 Setup Instructions

### 1. Get Your Free API Keys

**Hunter.io:**
```
1. Visit: https://hunter.io/users/sign_up
2. Sign up with email
3. Verify your email
4. Go to API section in dashboard
5. Copy your API key
```

**Brandfetch:**
```
1. Visit: https://brandfetch.com/
2. Click "Get API Access" or "Sign Up"
3. Create free account
4. Go to API Dashboard
5. Copy your API key
```

### 2. Update Your .env File

```bash
# Remove this:
# CLEARBIT_API_KEY=...

# Add these:
HUNTER_API_KEY=your_hunter_key_here
BRANDFETCH_API_KEY=your_brandfetch_key_here
```

### 3. Test the Changes

Run the app and try researching a company:
```powershell
streamlit run app.py
```

Then type:
```
Research Stripe
```

You should see data from Hunter.io and Brandfetch in the sources used!

## 📊 Usage Tips

### Maximize Free Tier Value

**Hunter.io (25 searches/month):**
- Use for important prospects/leads
- Each domain search counts as 1 request
- Resets monthly
- Cache results for repeated lookups

**Brandfetch (100 requests/month):**
- Use liberally - higher limit
- Great for getting logos for reports
- Provides brand consistency data
- Perfect for pitch decks

### Best Practices

1. **Domain First**: Always try to provide domain name when researching
   ```
   "Research stripe.com" (better)
   vs
   "Research Stripe" (might miss API data)
   ```

2. **Cache Wisely**: The app caches API results automatically

3. **Combine Sources**: Hunter + Brandfetch + OpenCorporates + NewsAPI = comprehensive profile

4. **Monitor Limits**: Check your API dashboards monthly

## 🔧 Troubleshooting

### "No data from Hunter.io"
- ✅ Check API key is correct in `.env`
- ✅ Verify domain is correct (try with .com)
- ✅ Check you haven't hit monthly limit (25 searches)
- ✅ Some domains may not be in Hunter's database

### "No data from Brandfetch"
- ✅ Works without API key but limited
- ✅ Check domain format (no http://, just domain.com)
- ✅ Not all brands are in database (especially smaller companies)

### "Missing revenue data"
- ⚠️ **Expected**: Free APIs don't provide financial data
- 💡 **Solution**: Add OpenAI API key for AI-powered financial estimation from news
- 💡 **Alternative**: Manual research from company websites/press releases

## 📈 Migration Complete!

Your app now uses:
- ✅ Hunter.io for company/email data
- ✅ Brandfetch for brand assets
- ✅ NewsAPI for news (unchanged)
- ✅ OpenCorporates for legal data (unchanged)
- ✅ All with genuine FREE tiers!

## 🎉 Bonus Features

The new setup actually provides some features Clearbit didn't:

1. **Email Pattern Discovery**: Know how to reach people at companies
2. **Brand Consistency**: Get official logos and colors for presentations  
3. **Better Social Coverage**: More comprehensive social media link collection
4. **Higher API Limits**: 125 free calls vs Clearbit's now-unavailable tier

---

**Questions?** Check the updated documentation in `README.md` and `QUICKSTART.md`!
