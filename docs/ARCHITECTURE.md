# THINC Intelligence OS — Connected Architecture

**Owner:** Dr. Ehab Taha  
**Primary engine:** `poptaha1974/thinc-v4`  
**Primary frontend:** `poptaha1974/admatch-insights`

This document turns the existing repositories into a connected product architecture instead of separate prototypes.

> **Scope.** This file covers the *service layer* (the FastAPI Intelligence OS
> under `services/api/` and its engines). For the layout of the packaged THINC
> engine itself, see [`docs/v4_2/ARCHITECTURE.md`](v4_2/ARCHITECTURE.md).

---

## 1. Product thesis

THINC Intelligence OS is a connected operating system for Egyptian and Arab ecommerce execution.

It connects:

1. Product selection.
2. Campaign economics.
3. Meta Ads attribution gaps.
4. Call center confirmation quality.
5. Delivery reality.
6. Persona and offer design.
7. Kill / Fix / Scale decisions.
8. Academy student execution tracking.

The system must not stay as a theory registry or a static dashboard. It must convert behavioral theory and operational data into executable commercial decisions.

---

## 2. Repository roles

| Repository | Role | Decision |
|---|---|---|
| `thinc-v4` | Core Python engine + API + Streamlit internal dashboard | Main source of truth |
| `admatch-insights` | React/TanStack commercial dashboard | Product frontend |
| `thinc-framework` | Legacy THINC v2.1 reference | Archive / migration reference |
| `gdp-dashboard` | Streamlit learning template | Student training asset only |

---

## 3. Target architecture

```text
Meta Ads / Shopify / WhatsApp / Shipping / Manual CSV
                  ↓
          AdMatch Insights Frontend
                  ↓
          THINC API Service / FastAPI
                  ↓
        THINC v4 Core Engine
                  ↓
Score + Real CPA + Profit + Persona + Kill/Fix/Scale
                  ↓
Dashboard + Reports + Advisor + Academy Outputs
```

---

## 4. Component boundaries

### 4.1 `thinc-v4`

Owns:

- Theory Registry.
- THINC scoring.
- Founder OS.
- Academy OS.
- Egyptianization.
- Real CPA calculations.
- Kill / Fix / Scale decision rules.
- API contracts.
- Streamlit internal dashboard.

Does **not** own:

- Complex browser UI.
- User authentication UI.
- Frontend routing.
- Long-term React state.

### 4.2 `admatch-insights`

Owns:

- User interface.
- Campaign tables.
- Funnel visualization.
- Planner screen.
- Advisor chat shell.
- API client calls to THINC API.
- Demo mode vs live mode labeling.

Does **not** own:

- Final scoring logic.
- Theory Registry.
- Kill / Fix / Scale decision engine.
- Proprietary THINC methodology logic.

---

## 5. Operating modes

### Demo Mode

Used for sales demos, student training, and UI review.

Rules:

- All cards must show `Demo Mode` or `Mock Data` where applicable.
- No card should imply live connection unless the API confirms it.
- Demo campaign numbers must live in separate `data/` files.

### Live Mode

Used after API integrations are configured.

Rules:

- Data comes from authenticated connectors, CSV uploads, or backend ingestion.
- Dashboard must show last sync time.
- Failed integration must show clear error state.

---

## 6. MVP system flow

### Campaign analysis flow

1. User enters or imports product + campaign data.
2. Frontend sends `CampaignAnalysisRequest` to THINC API.
3. THINC API calculates:
   - Meta CPA.
   - Real CPA.
   - confirmation rate.
   - delivery rate.
   - net profit.
   - ROAS.
   - risk flags.
4. THINC API returns:
   - `decision`: `KILL`, `FIX`, or `SCALE`.
   - `thinc_score`.
   - recommendations.
   - blind spots.
5. Frontend displays result and allows export.

---

## 7. Integration principle

The frontend may visualize numbers, but the backend must own the meaning.

Wrong:

```text
Frontend calculates scattered decisions independently.
```

Right:

```text
Frontend sends normalized data → THINC API returns decision and reasoning.
```

---

## 8. Immediate build priorities

1. Stabilize `thinc-v4` package and tests.
2. Add FastAPI endpoints around the core engine.
3. Add `thincApi.ts` client in `admatch-insights`.
4. Move all demo dashboard data into dedicated demo data files.
5. Add clear Demo/Live mode labels.
6. Add legal guardrails for academy promises.
7. Create a shared data model before adding real integrations.

---

## 9. Non-negotiable guardrails

- Do not claim live integration when data is static.
- Do not claim guaranteed sales, jobs, insurance, or income.
- Do not remove THINC ownership, attribution, or watermark.
- Do not duplicate scoring logic in multiple places.
- Do not scale a campaign based only on Meta CPA; Real CPA and delivery reality must be included.
