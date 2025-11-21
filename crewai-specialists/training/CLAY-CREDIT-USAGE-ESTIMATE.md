# Clay.com Credit Usage Estimates
**WalterSignal CrewAI Specialists**

**Created:** 2025-11-13
**API Key:** Stored in 1Password (`clay_api_key`)
**Environment:** DGX `.env` configured

---

## Credit Pricing Reference

### Clay Credit Costs (Standard)
- **1 Credit = $0.05**
- **20 Credits = $1.00**
- **Credits purchased in packs** (500, 1000, 5000, etc.)

### Common Enrichments

| Enrichment Type | Credits per Row | Cost per Row | Notes |
|----------------|----------------|--------------|-------|
| **Find Company** | 1 credit | $0.05 | Basic firmographics (name, industry, size, revenue) |
| **Enrich Company** | 1-2 credits | $0.05-$0.10 | Detailed data (employees, funding, tech stack) |
| **Find People** | 1 credit | $0.05 | Per person found (not per company) |
| **Enrich Person** | 1 credit | $0.05 | LinkedIn profile enrichment |
| **Work Email (single)** | 1 credit | $0.05 | Single provider email verification |
| **Work Email (waterfall)** | 2-3 credits | $0.10-$0.15 | Tries multiple providers (Prospeo → DropContact → Hunter) |
| **Phone Number** | 1-2 credits | $0.05-$0.10 | US landline + mobile |
| **LinkedIn Profile URL** | 1 credit | $0.05 | Find profile from name + company |
| **LinkedIn Posts** | 1 credit | $0.05 | Recent posts/activity |
| **Technologies (BuiltWith)** | 1 credit | $0.05 | Tech stack detection |
| **Funding Data (Crunchbase)** | 1 credit | $0.05 | Latest funding rounds |
| **Claygent (AI Agent)** | 5-10 credits | $0.25-$0.50 | Web research, scraping, analysis |
| **Screenshot** | 1 credit | $0.05 | Website screenshot capture |
| **Lighthouse Score** | 1 credit | $0.05 | Performance/accessibility metrics |

---

## Use Case 1: Lead Enrichment for Marketing Crew

### Workflow
1. Import 100 companies (domains)
2. Find Company data
3. Find People (3-5 decision makers per company)
4. Email waterfall enrichment
5. LinkedIn profile enrichment
6. Tech stack detection
7. Recent funding check

### Credit Calculation (Per Lead)

| Step | Enrichment | Credits | Cost |
|------|-----------|---------|------|
| 1 | Find Company | 1 | $0.05 |
| 2 | Find People (avg 3 contacts) | 3 | $0.15 |
| 3 | Email Waterfall (3 contacts) | 9 | $0.45 |
| 4 | LinkedIn URL (3 contacts) | 3 | $0.15 |
| 5 | Enrich LinkedIn (3 contacts) | 3 | $0.15 |
| 6 | Technologies (BuiltWith) | 1 | $0.05 |
| 7 | Funding Data | 1 | $0.05 |
| **Total per Company** | **21 credits** | **$1.05** |

### Monthly Estimate

**Scenario: 500 companies/month**
- Credits needed: 500 × 21 = **10,500 credits**
- Cost: **$525/month**
- Plus subscription: $149/month
- **Total: $674/month**

**Cost per fully-enriched lead:** $1.05

**ROI Comparison:**
- Manual research (SDR): 20 min × $50/hr = $16.67 per lead
- Clay automation: $1.05 per lead
- **Savings: $15.62 per lead (94% reduction)**
- **Monthly savings (500 leads): $7,810**

---

## Use Case 2: Competitor Intelligence for Research Crew

### Workflow
1. 20 competitor domains (monitored monthly)
2. Company profile enrichment
3. Funding rounds tracking
4. Tech stack analysis
5. Hiring signals (Claygent job board scrape)
6. Recent news (Claygent Google News)
7. Web traffic estimates

### Credit Calculation (Per Competitor)

| Step | Enrichment | Credits | Cost |
|------|-----------|---------|------|
| 1 | Enrich Company (detailed) | 2 | $0.10 |
| 2 | Funding Rounds | 1 | $0.05 |
| 3 | Tech Stack | 1 | $0.05 |
| 4 | Claygent: Job Postings Scrape | 8 | $0.40 |
| 5 | Claygent: Recent News | 8 | $0.40 |
| 6 | Web Traffic (SimilarWeb) | 1 | $0.05 |
| **Total per Competitor** | **21 credits** | **$1.05** |

### Monthly Estimate

**Scenario: 20 competitors × 4 refreshes/month**
- Credits needed: 20 × 21 × 4 = **1,680 credits**
- Cost: **$84/month**
- Plus subscription: $149/month
- **Total: $233/month**

**Cost per competitor intelligence refresh:** $1.05

**Value:**
- Replaces manual competitive research (4 hours/month per analyst)
- Automated alerts on funding, hiring, product changes
- Research Crew gets rich, up-to-date context

---

## Use Case 3: Website Audit Data for Design Crew

### Workflow
1. 50 prospect websites/month
2. Screenshot capture
3. Lighthouse performance score
4. Accessibility score
5. Tech stack detection
6. Competitor research (Claygent finds 3 competitors)

### Credit Calculation (Per Website)

| Step | Enrichment | Credits | Cost |
|------|-----------|---------|------|
| 1 | Screenshot | 1 | $0.05 |
| 2 | Lighthouse Score | 1 | $0.05 |
| 3 | Accessibility Score | 1 | $0.05 |
| 4 | Tech Stack | 1 | $0.05 |
| 5 | Claygent: Find 3 Competitors | 6 | $0.30 |
| **Total per Website** | **10 credits** | **$0.50** |

### Monthly Estimate

**Scenario: 50 websites/month**
- Credits needed: 50 × 10 = **500 credits**
- Cost: **$25/month**
- Plus subscription: $149/month
- **Total: $174/month**

**Cost per website audit data:** $0.50

**ROI Comparison:**
- Manual audit prep: 30 min × $75/hr = $37.50 per website
- Clay automation: $0.50 per website
- **Savings: $37.00 per website (99% reduction)**
- **Monthly savings (50 websites): $1,850**

---

## Use Case 4: TAM Building for Data Crew

### Workflow
1. Use "Find Companies" to source 5,000 ICP-matching companies
2. Enrich with firmographics
3. Find decision makers (1-2 per company for initial contact)
4. Light enrichment (no email verification yet, just validation)

### Credit Calculation (Per Company)

| Step | Enrichment | Credits | Cost |
|------|-----------|---------|------|
| 1 | Find Companies (included in plan) | 0 | $0.00 |
| 2 | Enrich Company | 1 | $0.05 |
| 3 | Find People (2 contacts) | 2 | $0.10 |
| 4 | Tech Stack | 1 | $0.05 |
| **Total per Company** | **4 credits** | **$0.20** |

### Quarterly TAM Build

**Scenario: 5,000 companies/quarter (updated quarterly)**
- Credits needed: 5,000 × 4 = **20,000 credits**
- Cost: **$1,000/quarter** = $333/month amortized
- Plus subscription: $149/month
- **Total: $482/month**

**Cost per TAM account:** $0.20

**Value:**
- Replaces manual list building (200+ hours)
- Rich segmentation data for Data Crew
- Territory planning with real-time firmographics

---

## Combined Monthly Usage (All Use Cases)

| Use Case | Companies | Credits | Cost |
|----------|-----------|---------|------|
| **Marketing Lead Enrichment** | 500 | 10,500 | $525 |
| **Competitor Intelligence** | 20 × 4 | 1,680 | $84 |
| **Website Audits** | 50 | 500 | $25 |
| **TAM Building** | 5,000/quarter | 6,667/month | $333 |
| **Total** | - | **19,347 credits** | **$967/month** |
| **Subscription** | - | - | $149 |
| **Grand Total** | - | - | **$1,116/month** |

---

## Cost Optimization Strategies

### 1. Bring Your Own API Keys (BYOK)

Clay allows you to connect your own enrichment provider API keys. This can reduce costs by 50-70%.

**Recommended BYOK Providers:**

| Provider | Service | Clay Credits Saved | Direct Cost | Net Savings |
|----------|---------|---------------------|-------------|-------------|
| **Prospeo** | Email finding | 1 credit ($0.05) | $0.01/email | $0.04 saved (80%) |
| **Phantombuster** | LinkedIn scraping | 1 credit ($0.05) | ~$0.02/profile | $0.03 saved (60%) |
| **BuiltWith** | Tech stack | 1 credit ($0.05) | Flat $295/mo | Break-even at 5,900 lookups/mo |
| **Hunter.io** | Email verification | 1 credit ($0.05) | $0.01/email | $0.04 saved (80%) |

**Optimized Lead Enrichment (500/month with BYOK):**
- Without BYOK: $525/month
- With BYOK (Prospeo + Phantombuster): ~$200/month
- **Savings: $325/month (62% reduction)**

### 2. Conditional Runs

Only run expensive enrichments on qualified leads:

```yaml
Example: ICP Filtering
- Find Company: Always run (1 credit)
- Calculate ICP Score: Formula (0 credits)
- Only enrich further if ICP_Score >= 7
  - Find People (3 credits)
  - Email Waterfall (9 credits)
  - LinkedIn (6 credits)
```

**Impact:**
- If 40% of companies are non-ICP: Skip 18 credits × 200 companies = 3,600 credits saved
- **Savings: $180/month**

### 3. Waterfall Optimization

Test provider success rates and reorder waterfall:

```yaml
Standard Waterfall (3 providers):
- Prospeo (success: 60%) → 1 credit
- DropContact (success: 20% of remaining) → 1 credit
- Hunter (success: 10% of remaining) → 1 credit
- Average credits used: 1.8 per email

Optimized Waterfall (best provider first):
- Prospeo (success: 60%) → 1 credit
- Hunter (success: 25% of remaining) → 1 credit
- Average credits used: 1.5 per email
```

**Impact on 500 leads × 3 contacts:**
- Standard: 1,500 × 1.8 = 2,700 credits
- Optimized: 1,500 × 1.5 = 2,250 credits
- **Savings: 450 credits = $22.50/month**

### 4. Batch Processing & Scheduling

Run enrichments during off-peak hours or in batches to avoid rate limit charges:

- Process 100 leads/day instead of 500 in one shot
- Use Clay's scheduling features
- Monitor error rates and re-run failed enrichments separately

### 5. Data Freshness Strategy

Not all data needs real-time updates:

| Data Type | Refresh Frequency | Reasoning |
|-----------|------------------|-----------|
| Company firmographics | Quarterly | Changes slowly |
| Contact emails | On-demand | Needed only when reaching out |
| Tech stack | Quarterly | Changes slowly |
| Funding data | Monthly | Important for timing outreach |
| LinkedIn posts | Weekly | For personalization insights |
| Competitor intel | Weekly | Track competitive moves |

**Impact:**
- Reduces redundant enrichments
- Focus credits on high-value, time-sensitive data

---

## Optimized Monthly Budget

With all optimization strategies applied:

| Use Case | Standard Credits | Optimized Credits | Standard Cost | Optimized Cost |
|----------|-----------------|------------------|---------------|----------------|
| **Marketing Leads** | 10,500 | 5,000 | $525 | $250 |
| **Competitor Intel** | 1,680 | 1,400 | $84 | $70 |
| **Website Audits** | 500 | 400 | $25 | $20 |
| **TAM Building** | 6,667 | 5,000 | $333 | $250 |
| **Total Credits** | 19,347 | **11,800** | $967 | **$590** |
| **Subscription** | - | - | $149 | $149 |
| **Grand Total** | - | - | $1,116 | **$739/month** |

**Savings with optimization: $377/month (34% reduction)**

---

## Credit Purchase Recommendations

### Month 1-2 (Pilot Phase)
- **Credit Pack:** 1,000 credits ($50)
- **Expected Usage:** 500-800 credits (testing workflows)
- **Buffer:** 200-500 credits for experimentation

### Month 3-4 (Scale-Up)
- **Credit Pack:** 5,000 credits ($250)
- **Expected Usage:** 3,000-4,000 credits/month
- **Allows:** Full marketing + competitor workflows

### Month 5+ (Production)
- **Credit Pack:** 10,000 credits ($500) OR 20,000 credits ($1,000)
- **Expected Usage:** 10,000-12,000 credits/month
- **Economies of Scale:** Bulk purchase discounts

### Credit Monitoring
- Set up budget alerts in Clay dashboard
- Monitor credit burn rate weekly
- Adjust enrichment strategies based on ROI per credit

---

## ROI Summary

### Total Monthly Investment
- **Optimized Clay costs:** $739/month
- **Alternative (manual research):**
  - 500 leads × 20 min × $50/hr = $8,333
  - 20 competitor analyses × 2 hrs × $75/hr = $3,000
  - 50 website audits × 30 min × $75/hr = $1,875
  - TAM building (one-time): $15,000/quarter = $5,000/month
  - **Total manual cost: $18,208/month**

### Net Savings
- **$18,208 - $739 = $17,469/month**
- **Annual savings: $209,628**
- **ROI: 2,263% (23.6x return)**

### Efficiency Gains
- **Time savings:** 350+ hours/month (manual research eliminated)
- **Data quality:** 80%+ find rate (vs 50-60% manual)
- **Consistency:** 100% of leads get same enrichment depth
- **Scalability:** Process 10x volume with same effort

---

## Next Steps

### Immediate (Week 1)
1. ✅ API key stored in 1Password and DGX `.env`
2. [ ] Purchase initial 1,000 credit pack ($50)
3. [ ] Create "Lead_Enrichment_Pilot" table
4. [ ] Test enrichment workflow on 50 leads
5. [ ] Measure actual credit usage vs. estimates

### Week 2-3
1. [ ] Connect BYOK providers (Prospeo, Phantombuster)
2. [ ] Build conditional run formulas for ICP filtering
3. [ ] Set up Google Sheets export automation
4. [ ] Integrate with Marketing Crew (read CSV workflow)

### Week 4+
1. [ ] Scale to 500 leads/month
2. [ ] Add Competitor Intelligence workflow
3. [ ] Monitor monthly credit burn and optimize
4. [ ] Purchase 5,000 credit pack based on actual usage

---

## Credit Usage Tracking Template

```csv
Date,Use_Case,Leads_Processed,Credits_Used,Cost,Notes
2025-11-13,Marketing_Pilot,50,1050,$52.50,Initial test run
2025-11-14,Marketing_Pilot,50,980,$49.00,Optimized waterfall
2025-11-15,Competitor_Intel,20,420,$21.00,Monthly refresh
2025-11-16,Website_Audit,10,100,$5.00,Design crew prep
```

**Track weekly and adjust strategies to stay under budget.**

---

## Document Metadata

**Version:** 1.0
**Last Updated:** 2025-11-13
**API Key Location:** 1Password `clay_api_key` + DGX `.env`
**Owner:** Mike Finneran
**Review Frequency:** Weekly (during pilot), Monthly (production)

**Next Review:** 2025-11-20 (after Week 1 pilot)
