# LinkedIn API Integration Guide

## Overview

The LinkedIn API integration allows the application to fetch:
- **Employee count** and employee count ranges
- **Company ID** and vanity name (e.g., "microsoft" from linkedin.com/company/microsoft)
- **LinkedIn profile URL**
- Company description, industry, and specialties
- Founded date and website information
- Follower count and page statistics

## Getting LinkedIn API Access

### Step 1: Create a LinkedIn Developer Account

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Sign in with your LinkedIn account
3. Click on "Create App"

### Step 2: Create a New App

1. Fill in the application details:
   - **App name**: Company Research Assistant (or your preferred name)
   - **LinkedIn Page**: Associate with your company page (required)
   - **App logo**: Upload a logo (optional)
   - **Legal agreement**: Accept the terms

2. Click "Create app"

### Step 3: Get API Credentials

1. Once the app is created, go to the "Auth" tab
2. Note your:
   - **Client ID**
   - **Client Secret**

### Step 4: Request API Products

1. Go to the "Products" tab
2. Request access to:
   - **Sign In with LinkedIn** (usually auto-approved)
   - **Marketing Developer Platform** (for company data - requires approval)

**Note**: The Marketing Developer Platform requires approval and may take several days.

### Step 5: Get Access Token

#### Option A: Using OAuth 2.0 Flow (Recommended)

1. Set up the OAuth redirect URI in your app settings
2. Use the authorization code flow to get an access token
3. Store the access token securely

#### Option B: Generate Access Token Manually (for testing)

1. Use the LinkedIn OAuth 2.0 Playground: https://www.linkedin.com/developers/tools/oauth
2. Select scopes: `r_organization_social`, `r_basicprofile`, `r_organization_admin`
3. Generate and copy the access token

**Important**: Access tokens expire after 60 days. You'll need to implement a refresh token flow for production.

### Step 6: Add Credentials to .env

Open your `.env` file and add:

```properties
# LinkedIn API Configuration
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
LINKEDIN_ACCESS_TOKEN=your_access_token_here
```

## Web Scraping for LinkedIn & Twitter IDs

The application also **automatically extracts LinkedIn and Twitter IDs** from company websites without requiring API access:

### What Gets Extracted:

1. **LinkedIn**:
   - Company page URL (e.g., https://linkedin.com/company/microsoft)
   - Vanity name (e.g., "microsoft")
   - If LinkedIn API is configured, fetches full company data

2. **Twitter/X**:
   - Profile URL (e.g., https://twitter.com/Microsoft)
   - Handle (e.g., @Microsoft)
   - Twitter ID (e.g., "Microsoft")

3. **Other Social Media**:
   - Facebook page ID
   - Instagram handle
   - YouTube channel URL

### How It Works:

The web scraper automatically:
1. Visits the company website
2. Searches for social media links in the HTML
3. Extracts and parses the URLs
4. Stores LinkedIn vanity names and Twitter handles
5. If LinkedIn API is enabled, uses the vanity name to fetch full company data

## Usage Examples

### Example 1: With LinkedIn API Configured

```python
from research.linkedin_api import LinkedInClient

client = LinkedInClient()

# Get company by vanity name
company = client.get_company_by_vanity_name("microsoft")
print(f"Employees: {company['employee_count']}")
print(f"LinkedIn URL: {company['linkedin_url']}")
```

### Example 2: Web Scraping Only (No API Keys Needed)

```python
from research.web_scraper import SimpleWebScraper

scraper = SimpleWebScraper()

# Scrape company website
data = scraper.scrape_company_website("microsoft.com")
print(f"LinkedIn ID: {data['social_media']['linkedin_id']}")
print(f"Twitter Handle: {data['social_media']['twitter_handle']}")
```

### Example 3: Full Integration (Used by Application)

The application automatically:
1. Tries LinkedIn API first (if configured)
2. Scrapes company website for social media links
3. If LinkedIn vanity name found, fetches data via API
4. Consolidates all data from multiple sources

## Data Retrieved

### From LinkedIn API:

```json
{
  "source": "linkedin",
  "company_name": "Microsoft",
  "linkedin_id": "1035",
  "vanity_name": "microsoft",
  "linkedin_url": "https://www.linkedin.com/company/microsoft",
  "employee_count": 221000,
  "employee_count_range": "10001+",
  "description": "Every company has a mission...",
  "industry": ["Computer Software"],
  "specialties": ["Business Software", "Developer Tools"],
  "website": "https://www.microsoft.com",
  "founded": {"year": 1975},
  "follower_count": 20500000
}
```

### From Web Scraping:

```json
{
  "social_media": {
    "linkedin_url": "https://www.linkedin.com/company/microsoft",
    "linkedin_id": "microsoft",
    "linkedin_vanity_name": "microsoft",
    "twitter_url": "https://twitter.com/Microsoft",
    "twitter_id": "Microsoft",
    "twitter_handle": "@Microsoft",
    "facebook_url": "https://www.facebook.com/Microsoft",
    "instagram_url": "https://www.instagram.com/microsoft"
  }
}
```

## API Limitations

### LinkedIn API:

- **Rate Limits**: Varies by product tier
  - Free tier: Very limited (not officially supported)
  - Partner tier: Higher limits but requires approval
  
- **Access Requirements**: 
  - Marketing Developer Platform access needed for company data
  - Requires LinkedIn page association
  - May require business verification

- **Token Expiration**: 
  - Access tokens expire after 60 days
  - Requires refresh token implementation for production

### Recommendations:

1. **For Development**: Use web scraping to extract LinkedIn/Twitter IDs
2. **For Production**: Apply for LinkedIn Marketing Developer Platform
3. **Best Approach**: Combine both - scrape for IDs, use API when available

## Troubleshooting

### Issue: "LinkedIn API not enabled"
**Solution**: Check that `LINKEDIN_ACCESS_TOKEN` is set in `.env`

### Issue: "401 Unauthorized"
**Solution**: 
- Access token may be expired (regenerate)
- Check that your app has the correct API products enabled
- Verify scopes in your access token

### Issue: "Company not found"
**Solution**:
- Try using the LinkedIn vanity name instead of company name
- Verify the company page exists on LinkedIn
- Check that the vanity name is correct (case-insensitive)

### Issue: "Rate limit exceeded"
**Solution**:
- Wait before making more requests
- Consider upgrading to a higher API tier
- Implement caching to reduce API calls

## Testing

Test the LinkedIn integration:

```python
# Test in Python console
from research.linkedin_api import get_linkedin_data

# Test with company name
data = get_linkedin_data("Microsoft")
print(data)

# Test with vanity name
data = get_linkedin_data("", vanity_name="microsoft")
print(data)
```

Test web scraping:

```python
from research.web_scraper import SimpleWebScraper

scraper = SimpleWebScraper()
data = scraper.scrape_company_website("stripe.com")
print(data['social_media'])
```

## Summary

✅ **LinkedIn API**: Best for employee counts and verified company data (requires approval)
✅ **Web Scraping**: Works immediately for LinkedIn/Twitter IDs (no API keys needed)
✅ **Hybrid Approach**: The app uses both automatically for maximum coverage

The application works great even without LinkedIn API access - web scraping provides LinkedIn and Twitter IDs instantly!
