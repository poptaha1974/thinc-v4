# MVP Scope — THINC Campaign Analyzer v1

The first connected product release should be small, measurable, and commercially useful.

---

## 1. MVP name

**THINC Campaign Analyzer v1**

---

## 2. Core promise

Input product + campaign reality data. Output:

1. Real CPA.
2. Profitability.
3. Attribution gap.
4. THINC score.
5. Kill / Fix / Scale decision.
6. Practical recommendations.
7. Blind spots.

---

## 3. Included in MVP

### Backend / `thinc-v4`

- FastAPI service skeleton.
- Campaign analysis endpoint.
- Founder readiness endpoint.
- Theory Registry summary endpoint.
- Integration status endpoint.
- Shared schema models.
- Guardrails for impossible numbers.

### Frontend / `admatch-insights`

- API client.
- Demo data separated from route components.
- README explaining demo vs live mode.
- Integration plan for THINC API.

### Documentation

- Architecture.
- Data model.
- API contract.
- Roadmap.
- Legal guardrails.

---

## 4. Excluded from MVP

- Real Meta OAuth.
- Shopify OAuth.
- WhatsApp Business API production connection.
- Payment processing.
- User accounts.
- Multi-tenant database.
- PDF report generation.
- Full Academy LMS.
- Automated campaign editing.

These are v2+.

---

## 5. Success criteria

The MVP is successful when:

1. `admatch-insights` can call `thinc-v4` locally.
2. A campaign can be analyzed from the frontend.
3. The result returns real CPA, net profit, THINC score, and decision.
4. Static data is labeled as demo data.
5. The same campaign input returns the same result in API and UI.
6. No page implies live integration before real connection exists.

---

## 6. Minimum input form

The first form needs only:

### Product

- Product name.
- Cost.
- Price.
- Inventory units.

### Campaign

- Campaign name.
- Spend.
- Meta leads.
- Confirmed orders.
- Delivered orders.
- Returned orders.

### Economics

- Shipping success cost.
- Shipping return cost.
- Packaging cost.
- Overhead.
- VAT rate.

---

## 7. Minimum output screen

- Meta CPA.
- Real CPA.
- Attribution gap.
- Confirmation rate.
- Delivery rate.
- Net profit.
- ROAS.
- ROI.
- THINC score.
- Decision.
- Blind spots.
- Recommendations.

---

## 8. Decision labels

Allowed decision values:

```text
KILL
FIX
SCALE
```

Do not introduce new decision labels before the frontend and API contract are updated.

---

## 9. Risk labels

Allowed risk labels:

```text
low
medium
high
critical
```

---

## 10. Demo campaign to use

The current demo campaign can remain:

```text
Karohat Ramadan
```

But it must live in a demo data module and be labeled as mock/demo data.
