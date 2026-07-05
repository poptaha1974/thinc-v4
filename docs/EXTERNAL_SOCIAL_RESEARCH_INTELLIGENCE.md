# External Social Research & Daily Intelligence Engine

This layer allows THINC v4.0 to ingest external social, economic, political-context, price, news, search, and cultural signals affecting Egyptian society on a daily basis.

It does not replace campaign data. It adds context around campaign data.

---

## 1. Purpose

The model should not only learn from:

- Meta Ads,
- WhatsApp objections,
- orders,
- delivery,
- returns.

It should also understand the environment around the customer:

- daily price movement,
- inflation pressure,
- exchange-rate anxiety,
- fuel and transport changes,
- political and social mood,
- public events,
- search trends,
- category demand,
- competitor movement,
- regulation,
- social norms and family concerns,
- news cycles and cultural moments.

---

## 2. New module

```text
src/thinc_v4/external_social_research.py
```

---

## 3. API routes

```text
services/api/external_research_routes.py
services/api/research_app.py
```

Standalone runtime:

```bash
uvicorn services.api.research_app:app --reload --port 8002
```

Endpoints:

```text
GET  /health
GET  /api/external-research/options
POST /api/external-research/daily-egypt-intelligence
```

---

## 4. Supported research source types

- Official statistics.
- Central bank releases.
- Government releases.
- News.
- Economic analysis.
- Social analysis.
- Search trends.
- Price monitoring.
- Social media trends.
- Think tanks.
- International organizations.
- Internal observations.
- Manual research notes.

---

## 5. Egyptian research domains

The engine can classify observations into:

- inflation and prices,
- exchange rate,
- interest rates,
- employment and income,
- consumer confidence,
- family and social norms,
- religious seasonality,
- political context,
- regulation and law,
- competitor market,
- product category trend,
- channel behavior,
- cultural moment,
- supply chain,
- general sentiment.

---

## 6. Commercial implications

Each observation can translate into one or more implications:

- price sensitivity,
- trust requirement,
- delivery risk,
- offer repositioning,
- category demand up,
- category demand down,
- channel shift,
- cashflow pressure,
- social risk,
- brand tone adjustment,
- no action.

---

## 7. Example input

```json
{
  "intelligence_date": "2026-07-06",
  "observations": [
    {
      "domain": "inflation_prices",
      "summary": "Food and transport prices are rising in public discussion.",
      "evidence": "Multiple news and price-monitoring notes show upward pressure.",
      "direction": "up",
      "evidence_strength": "high",
      "market_impact": "high",
      "commercial_implications": ["price_sensitivity", "offer_repositioning"],
      "affected_segments": ["middle_mainstream", "value_sensitive"],
      "affected_categories": ["household", "gifts", "beauty"],
      "source": {
        "title": "Daily price context note",
        "source_name": "Manual Research Desk",
        "source_type": "manual_research_note",
        "reliability_score": 7
      }
    }
  ]
}
```

---

## 8. Example output

The engine returns:

- confidence score,
- top signals,
- behavior shifts,
- commercial risks,
- commercial opportunities,
- recommended weight updates,
- campaign guidance,
- research gaps,
- required human review,
- source audit.

---

## 9. Source reliability rules

The engine scores sources based on:

- source type,
- reliability score,
- evidence strength,
- citation availability,
- whether the source is official, journalistic, analytical, internal, or manual.

Political-context signals require extra caution.

---

## 10. Political-context handling

Political signals must never become manipulative persuasion instructions.

They are used only to adjust:

- brand tone,
- risk caution,
- timing,
- public mood sensitivity,
- message neutrality,
- and escalation to human review.

Example safe use:

```text
Public mood is tense. Avoid aggressive urgency, jokes, or polarizing language.
```

Unsafe use:

```text
Exploit political fear to sell more.
```

The second pattern is prohibited.

---

## 11. Daily intelligence workflow

```text
Google / News / Official Data / Trends / Price Feeds / Social Listening
                    ↓
ResearchObservation objects
                    ↓
Source audit + reliability scoring
                    ↓
Daily Egypt Intelligence
                    ↓
Behavior shift + commercial risk/opportunity
                    ↓
Adaptive Market Learning Engine
                    ↓
Updated weights + experiments + human review
```

---

## 12. How this connects to Adaptive Learning

External research does not directly change the model.

It produces contextual signals that feed the Adaptive Market Learning Engine.

The Adaptive Engine then compares:

```text
External signal + campaign prediction + actual market outcome
```

Only repeated validated patterns should become permanent model updates.

---

## 13. Example: inflation context

If prices rise:

The engine may increase:

- price sensitivity,
- offer value framing,
- cashflow pressure caution.

Campaign guidance:

```text
Avoid cheap positioning. Frame offers as smart value, durability, savings, practical use, and reduced risk.
```

---

## 14. Example: trust anxiety

If news/social signals indicate rising scam fear:

The engine may increase:

- trust requirement,
- social proof,
- exchange policy visibility.

Campaign guidance:

```text
Move reviews, real photos, exchange policy, and delivery proof earlier in the creative and WhatsApp flow.
```

---

## 15. Example: political/social tension

If public mood is tense:

The engine may increase:

- political context caution,
- brand tone sensitivity,
- human review requirement.

Campaign guidance:

```text
Use calm, practical, non-polarizing language. Avoid jokes, aggressive scarcity, and fear-based pressure.
```

---

## 16. Recommended future connectors

This module currently defines the intelligence contract.

Future connector implementation can use:

- Google Programmable Search API,
- compliant SERP provider,
- Google Trends export workflow,
- RSS/news API,
- CAPMAS data/manual feed,
- CBE data/manual feed,
- price-monitoring spreadsheets,
- internal WhatsApp/call-center tagging,
- competitor monitoring sheet,
- social listening tools.

---

## 17. Operating standard

```text
One article = weak signal.
Multiple credible sources = strong signal.
Official data + market behavior = validated signal.
Validated repeated signal = model update candidate.
```

---

## 18. Strategic value

This layer makes THINC sensitive to daily Egyptian reality:

- price pressure,
- economic stress,
- public mood,
- family behavior,
- search demand,
- news cycles,
- social trends,
- category movement,
- and political-context caution.

It turns THINC into a living market intelligence system rather than a closed framework.
