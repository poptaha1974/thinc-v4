# THINC API Contract v1

This contract connects `admatch-insights` to `thinc-v4`.

Base URL in development:

```text
http://localhost:8000
```

Frontend env variable:

```text
VITE_THINC_API_URL=http://localhost:8000
```

---

## 1. Health

### `GET /health`

Response:

```json
{
  "status": "ok",
  "service": "thinc-api",
  "engine": "THINC v4.0",
  "mode": "development"
}
```

---

## 2. Theory Registry Summary

### `GET /api/theories/summary`

Response:

```json
{
  "count": 50,
  "domains": {
    "Behavioral Economics": 8,
    "Decision Science": 7
  },
  "watermark": "THINC™ v4.0 — Invented by Dr. Ehab Taha"
}
```

---

## 3. Campaign Analysis

### `POST /api/campaign/analyze`

Request:

```json
{
  "product": {
    "name": "Karohat Air Fryer 5L",
    "cost": 245,
    "price": 500,
    "inventory_units": 500
  },
  "campaign": {
    "name": "Karohat Ramadan",
    "spend": 12450,
    "meta_leads": 327,
    "confirmed_orders": 127,
    "delivered_orders": 98,
    "returned_orders": 29
  },
  "economics": {
    "shipping_success_cost": 45,
    "shipping_return_cost": 25,
    "packaging_cost_per_order": 15,
    "overhead": 500,
    "vat_rate": 0.14
  }
}
```

Response:

```json
{
  "campaign_name": "Karohat Ramadan",
  "product_name": "Karohat Air Fryer 5L",
  "meta_cpa": 38.07,
  "real_cpa": 127.04,
  "confirmation_rate": 38.84,
  "delivery_rate": 77.17,
  "attribution_gap_pct": 233.69,
  "net_profit": 11055.9,
  "roas": 3.94,
  "roi": 0.42,
  "thinc_score": 6.8,
  "decision": "FIX",
  "risk_level": "medium",
  "blind_spots": [
    "Meta CPA is materially lower than Real CPA.",
    "Confirmation rate is below the safe threshold."
  ],
  "recommendations": [
    "Improve confirmation script before increasing spend.",
    "Test a stronger offer and proof stack."
  ]
}
```

---

## 4. Founder Readiness

### `POST /api/founder/readiness`

Request:

```json
{
  "execution_score": 7,
  "discipline_score": 6.5,
  "learning_speed_score": 8,
  "resilience_score": 7,
  "focus_score": 7,
  "financial_discipline_score": 6
}
```

Response:

```json
{
  "score": 6.95,
  "verdict": "جاهز للاختبار مع متابعة",
  "recommendations": [
    "لا تسمح للطالب بإطلاق حملة قبل فهم Break-even CPA."
  ]
}
```

---

## 5. Integration status

### `GET /api/integrations/status`

Response:

```json
{
  "items": [
    {
      "integration": "Meta Ads API",
      "mode": "demo",
      "connected": false,
      "last_sync_at": null,
      "message": "Demo data only. Live OAuth integration is pending."
    }
  ]
}
```

---

## 6. Frontend rule

`admatch-insights` must not present mock integrations as live connections.

Every screen using static data must show one of:

- `Demo Mode`
- `Mock Data`
- `Manual CSV`
- `Live API`

---

## 7. Error shape

All API errors should use:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Delivered orders cannot exceed confirmed orders.",
    "field": "campaign.delivered_orders"
  }
}
```
