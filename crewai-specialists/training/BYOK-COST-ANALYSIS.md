# BYOK Provider Cost Analysis
**Should You Add Direct Subscriptions vs Using Clay Credits?**

**Created:** 2025-11-13
**Question:** Does adding Crunchbase (or other provider) subscriptions reduce costs vs Clay credits?

---

## Quick Answer: It Depends on Volume

**Rule of thumb:**
- **Low volume (<100 lookups/month):** Use Clay credits (pay-per-use)
- **High volume (>200 lookups/month):** BYOK subscription saves money

---

## Crunchbase Pricing Analysis

### Option 1: Via Clay Credits

**Crunchbase Enrichment in Clay:**
- **1 credit per company** = $0.075/lookup
- Pay only for what you use
- No monthly minimum

**Monthly Cost Examples:**
- 50 companies: 50 credits = $3.75
- 100 companies: 100 credits = $7.50
- 200 companies: 200 credits = $15.00
- 500 companies: 500 credits = $37.50

---

### Option 2: Direct Crunchbase Subscription

**Crunchbase Pro:**
- **$49/month** (annual billing) or $99/month (monthly)
- Includes basic API access
- Limited to 10 free contacts/month
- Manual lookups only (not suitable for automation)

**Crunchbase Business:**
- **$199/month** (annual) or $299/month (monthly)
- Full API access for integrations
- Unlimited lookups
- Advanced filters and exports

**Crunchbase API (Data Enrichment):**
- **Custom pricing** (typically $500-2,000+/month)
- Full API access for automation
- Unlimited lookups
- Requires sales contact

---

### Break-Even Analysis

**Comparing Clay Credits vs Crunchbase Business ($199/month):**

| Monthly Lookups | Clay Cost | Crunchbase Cost | Savings with BYOK |
|----------------|-----------|-----------------|-------------------|
| 50 lookups | $3.75 | $199 | -$195.25 (Clay cheaper) |
| 100 lookups | $7.50 | $199 | -$191.50 (Clay cheaper) |
| 500 lookups | $37.50 | $199 | -$161.50 (Clay cheaper) |
| 1,000 lookups | $75.00 | $199 | -$124.00 (Clay cheaper) |
| 2,000 lookups | $150.00 | $199 | -$49.00 (Clay cheaper) |
| **2,650 lookups** | **$198.75** | **$199** | **~$0 (Break-even)** |
| 3,000 lookups | $225.00 | $199 | **+$26** (BYOK saves) |
| 5,000 lookups | $375.00 | $199 | **+$176** (BYOK saves) |

**Break-even point:** ~2,650 Crunchbase lookups/month

**Your current plan:** 2,000 Clay credits total = only ~200-400 credits allocated to Crunchbase
- **Verdict:** Stick with Clay credits (way below break-even)

---

## Other BYOK Providers Analysis

### Prospeo (Email Finding)

**Via Clay Credits:**
- 1 credit per email = $0.075/email

**Direct Prospeo Subscription:**
- **$49/month** for 1,000 emails = $0.049/email
- **$99/month** for 3,000 emails = $0.033/email

**Break-even:**
- $49 ÷ ($0.075 - $0.049) = 1,885 emails/month
- **If you enrich 600+ emails/month → BYOK saves money**

**Your current need:** 100-200 emails/month (10-20 packs × 10 leads × 1 email avg)
- **Verdict:** BYOK makes sense if you do 200+ leads/month ✅

---

### Phantombuster (LinkedIn Scraping)

**Via Clay Credits:**
- 1 credit per profile = $0.075/profile

**Direct Phantombuster:**
- **$30/month** for 1,000 profiles = $0.03/profile
- **$64/month** for 3,000 profiles = $0.021/profile

**Break-even:**
- $30 ÷ ($0.075 - $0.03) = 667 profiles/month
- **If you scrape 200+ LinkedIn profiles/month → BYOK saves money**

**Your current need:** 300-600 profiles/month (10-20 packs × 10 leads × 3 profiles avg)
- **Verdict:** BYOK makes sense ✅

---

### BuiltWith (Tech Stack)

**Via Clay Credits:**
- 1 credit per lookup = $0.075/lookup

**Direct BuiltWith:**
- **$295/month** for unlimited lookups
- Includes historical data and alerts

**Break-even:**
- $295 ÷ $0.075 = **3,933 lookups/month**

**Your current need:** 100-200 lookups/month
- **Verdict:** Clay credits way cheaper (don't use BYOK) ❌

---

### Hunter.io (Email Verification)

**Via Clay Credits:**
- 1 credit per verification = $0.075/email

**Direct Hunter.io:**
- **$49/month** for 1,000 verifications = $0.049/email
- **$99/month** for 3,000 verifications = $0.033/email

**Break-even:**
- Similar to Prospeo: ~650 emails/month

**Your current need:** 100-200 emails/month
- **Verdict:** Borderline - BYOK worth it if you hit 150+/month

---

## Recommended BYOK Strategy

### Your Current Volume (10-20 packs/month)

**Lead Volume:** 100-200 leads/month
**Lookups per lead:**
- Company data: 1
- Contacts: 3
- Emails: 3
- LinkedIn: 6
- Tech stack: 1
- Crunchbase funding: 1

**Total lookups/month:**
- 150 leads × 15 lookups = 2,250 lookups

**Provider Breakdown:**
- Email finding: 450 lookups
- LinkedIn: 900 lookups
- Tech stack: 150 lookups
- Crunchbase: 150 lookups
- Company data: 150 lookups

---

### Cost Comparison: Clay Only vs BYOK Mix

**Option A: All Clay Credits**

| Provider | Lookups | Credits | Cost |
|----------|---------|---------|------|
| All enrichments | 2,250 | 2,250 | $168.75 |

**Problem:** Exceeds your 2,000 credit budget!

---

**Option B: BYOK for High-Volume Providers**

| Provider | Lookups | Method | Cost |
|----------|---------|--------|------|
| **Prospeo (email)** | 450 | BYOK $49/mo | $49.00 |
| **Phantombuster (LinkedIn)** | 900 | BYOK $64/mo | $64.00 |
| **Company data** | 150 | Clay credits | $11.25 |
| **Tech stack** | 150 | Clay credits | $11.25 |
| **Crunchbase** | 150 | Clay credits | $11.25 |
| **Total** | 2,250 | Mixed | **$146.75/month** |

**Clay credits used:** 450 credits (well within 2,000 limit)

---

**Option C: Aggressive BYOK**

| Provider | Lookups | Method | Cost |
|----------|---------|--------|------|
| **Prospeo (email)** | 450 | BYOK $49/mo | $49.00 |
| **Phantombuster (LinkedIn)** | 900 | BYOK $30/mo | $30.00 |
| **Hunter (verification)** | 450 | BYOK $49/mo | $49.00 |
| **Company data** | 150 | Clay credits | $11.25 |
| **Tech stack** | 150 | Clay credits | $11.25 |
| **Crunchbase** | 150 | Clay credits | $11.25 |
| **Total** | 2,250 | Mixed | **$161.75/month** |

**Clay credits used:** 450 credits
**Additional BYOK:** $128/month (Prospeo + Phantom + Hunter)

---

## Crunchbase Specific Recommendation

### Should You Add Crunchbase Subscription?

**Your Usage:** ~150 Crunchbase lookups/month (10-20 packs)

**Cost via Clay:** 150 credits = $11.25/month

**Cost via BYOK:**
- Crunchbase Business: $199/month
- Crunchbase API: $500+/month

**Break-even:** Need 2,650+ lookups/month

**Verdict:** ❌ **Do NOT subscribe to Crunchbase**
- You'd need to do 176+ packs/month to break even
- Your 2k credit limit caps you at ~40 packs max
- Clay credits are 17x cheaper for your volume

---

## Final BYOK Recommendations

### Phase 1: Start with These (Worth It Now)

**1. Prospeo - $49/month** ✅
- Break-even: 650 emails
- Your volume: 450 emails
- **Savings:** Not yet, but will save $5/month at 200 leads

**2. Phantombuster - $30/month** ✅
- Break-even: 400 profiles
- Your volume: 900 profiles
- **Savings:** $37.50/month immediately**

**Total Phase 1 BYOK:** $79/month
**Immediate savings:** $37.50/month (from Phantombuster)

---

### Phase 2: Add When You Hit 300+ Leads/Month

**3. Hunter.io - $49/month**
- Add when doing 650+ email verifications
- At 300 leads/month = 900 emails
- **Savings:** $18/month**

**Total Phase 2 BYOK:** $128/month
**Savings at 300 leads:** $55/month

---

### Never Add (Not Worth It at Your Scale)

**❌ Crunchbase** - Need 2,650+ lookups/month (you do ~150)
**❌ BuiltWith** - Need 3,900+ lookups/month (you do ~150)
**❌ Apollo** - Enterprise pricing, Clay cheaper for small volumes
**❌ ZoomInfo** - Too expensive, Clay has better coverage

---

## Cost Summary Table

### Your Current Costs (150 leads/month)

| Scenario | Clay Credits | BYOK Subs | Total Monthly | Cost per 10 Leads |
|----------|-------------|-----------|---------------|-------------------|
| **All Clay** | $168.75 (exceeds budget!) | $0 | $168.75 | $11.25 |
| **Phase 1 BYOK** | $56.25 | $79 | $135.25 | $9.00 |
| **Phase 2 BYOK** | $33.75 | $128 | $161.75 | $10.78 |

**Recommendation:** Phase 1 BYOK (Prospeo + Phantombuster)
- **Cost per 10 leads: $9.00**
- Clay credits: 750 of 2,000 used (plenty of headroom)
- Can scale to 260+ leads/month before hitting credit limit

---

## Updated Pricing Model (With Phase 1 BYOK)

### Your Actual Cost Per 10 Leads

| Enrichment | Method | Cost |
|-----------|--------|------|
| Company data | Clay | $0.75 (10 credits) |
| Find people (3) | Clay | $2.25 (30 credits) |
| **Email (3)** | **Prospeo BYOK** | **$1.47** (3 × $0.049) |
| **LinkedIn (6)** | **Phantom BYOK** | **$1.80** (6 × $0.03) |
| Tech stack | Clay | $0.75 (10 credits) |
| Crunchbase | Clay | $0.75 (10 credits) |
| **Total** | **Mixed** | **$7.77** |

**Round to $8 per 10 leads** (includes BYOK fixed costs amortized)

---

## Updated Client Pricing (With BYOK Phase 1)

### Recommended Price: $49 per 10 leads

**Your Economics:**
- Cost: $8.00
- Revenue: $49.00
- **Profit: $41.00 (84% margin)**

**Monthly at 150 leads (15 packs):**
- Revenue: $735
- Costs: $120 (variable) + $150 (Clay) + $79 (BYOK) = $349
- **Profit: $386/month**

**Monthly at 250 leads (25 packs):**
- Revenue: $1,225
- Costs: $200 (variable) + $150 (Clay) + $79 (BYOK) = $429
- **Profit: $796/month**

---

## Action Plan

### Immediate (Week 1)
- [ ] Sign up for **Phantombuster $30/month** (saves money immediately)
- [ ] Test BYOK integration with Clay
- [ ] Verify cost = $8/10 leads with BYOK

### Month 2
- [ ] Monitor email volume
- [ ] If doing 200+ leads/month, add **Prospeo $49/month**
- [ ] Track savings

### Month 3+
- [ ] At 300+ leads/month, add **Hunter.io $49/month**
- [ ] DO NOT add Crunchbase (not worth it until 1,000+ leads/month)

### Never
- ❌ Crunchbase subscription (use Clay credits)
- ❌ BuiltWith subscription (use Clay credits)
- ❌ Any provider where break-even > your monthly volume

---

## Document Metadata

**Version:** 1.0
**Last Updated:** 2025-11-13
**Recommended BYOK:** Phantombuster ($30) + Prospeo ($49) = $79/month
**Crunchbase Verdict:** ❌ Not worth it (use Clay credits at $11.25/month)
**Updated Cost per 10 Leads:** $8.00 (with Phase 1 BYOK)
**Updated Pricing:** $49 per 10 leads (84% margin)

**Next Review:** When monthly volume hits 250+ leads
