# Shared Data Model — THINC Intelligence OS

This file defines the shared language between `thinc-v4` and `admatch-insights`.

The main risk this solves: every component calculating numbers differently.

---

## 1. Core entities

```text
Product
Campaign
Lead
Order
Delivery
Return
Persona
Assessment
Recommendation
IntegrationStatus
```

---

## 2. Product

```json
{
  "product_id": "karohat-air-fryer-5l",
  "name": "Karohat Air Fryer 5L",
  "category": "Home Appliances",
  "cost": 245,
  "price": 500,
  "min_competitor_price": 450,
  "max_competitor_price": 650,
  "inventory_units": 500,
  "positioning": "Quiet practical home upgrade",
  "target_market": "Egypt"
}
```

### Required fields

- `name`
- `cost`
- `price`

### Important derived metrics

- gross margin.
- contribution margin.
- break-even order count.
- safe CPA ceiling.

---

## 3. Campaign

```json
{
  "campaign_id": "karohat-ramadan-001",
  "name": "Karohat Ramadan",
  "channel": "Meta Ads",
  "objective": "Conversions",
  "spend": 12450,
  "meta_leads": 327,
  "confirmed_orders": 127,
  "delivered_orders": 98,
  "returned_orders": 29,
  "time_window_days": 30
}
```

### Required fields

- `spend`
- `meta_leads`
- `confirmed_orders`
- `delivered_orders`

### Derived metrics

- `meta_cpa = spend / meta_leads`
- `real_cpa = spend / delivered_orders`
- `confirmation_rate = confirmed_orders / meta_leads`
- `delivery_rate = delivered_orders / confirmed_orders`
- `attribution_gap = real_cpa / meta_cpa - 1`

---

## 4. Economics

```json
{
  "shipping_success_cost": 45,
  "shipping_return_cost": 25,
  "packaging_cost_per_order": 15,
  "overhead": 500,
  "vat_rate": 0.14
}
```

### Derived metrics

- revenue.
- COGS.
- ad spend.
- shipping costs.
- packaging costs.
- tax estimate.
- net profit.
- ROAS.
- ROI.

---

## 5. Assessment

```json
{
  "thinc_score": 7.4,
  "decision": "FIX",
  "grade": "B",
  "risk_level": "medium",
  "blind_spots": [
    "Meta CPA is misleading because delivery reality is weaker.",
    "Confirmation rate is below the safe threshold."
  ],
  "recommendations": [
    "Improve call center confirmation script.",
    "Test a stronger offer before increasing budget."
  ]
}
```

---

## 6. Decision rules v1

### SCALE

Allowed only when:

- net profit is positive.
- real CPA is below safe CPA ceiling.
- delivery rate is acceptable.
- attribution gap is not extreme.
- inventory can support scale.

### FIX

Used when:

- signal exists but one or more operational metrics are weak.
- product may work after improving offer, creative, call center, or delivery.

### KILL

Used when:

- negative economics persist.
- delivery reality destroys profit.
- product has no differentiation.
- campaign cannot reach safe CPA after testing.

---

## 7. Persona

```json
{
  "persona_id": "egyptian-home-manager-cairo",
  "segment": "Egyptian household buyer",
  "demographics": {
    "age_range": "28-45",
    "location": "Cairo / Giza / Alexandria",
    "income_band": "middle"
  },
  "behavioral": {
    "buying_style": "cautious but responsive to proof",
    "channel": "Facebook / WhatsApp"
  },
  "psychological": {
    "main_fear": "wasting money on poor quality",
    "main_desire": "safe practical upgrade"
  },
  "emotional": {
    "desired_feeling": "control and reassurance"
  },
  "triggers": ["cash on delivery", "social proof", "limited offer", "clear warranty"]
}
```

---

## 8. IntegrationStatus

```json
{
  "integration": "Meta Ads API",
  "mode": "demo",
  "connected": false,
  "last_sync_at": null,
  "message": "Demo data only. Live OAuth integration is pending."
}
```

Allowed modes:

- `demo`
- `manual_csv`
- `live_api`
- `error`

---

## 9. Naming consistency

Use these names everywhere:

| Concept | Canonical field |
|---|---|
| Meta leads | `meta_leads` |
| Confirmed orders | `confirmed_orders` |
| Delivered orders | `delivered_orders` |
| Real CPA | `real_cpa` |
| Meta CPA | `meta_cpa` |
| Attribution gap | `attribution_gap_pct` |
| THINC decision | `decision` |
| Product score | `thinc_score` |

---

## 10. Validation rules

- Counts cannot be negative.
- Spend cannot be negative.
- Price and cost must be positive.
- Delivered orders cannot exceed confirmed orders unless explicitly marked as data correction.
- Confirmed orders cannot exceed Meta leads unless source mismatch is declared.
- If delivered orders are zero, `real_cpa` must be `null`, not infinity in API responses.
