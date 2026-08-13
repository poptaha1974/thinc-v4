# Connected Product Roadmap

This roadmap converts the repositories into one coherent product ecosystem.

---

## Phase 0 — Current state

- `thinc-v4` has a strong core framework, theory registry, Streamlit dashboard, and identity protection.
- `admatch-insights` has a strong React dashboard prototype, but much of the data is static.
- `thinc-framework` is a legacy v2.1 reference.
- `gdp-dashboard` is a learning template.

---

## Phase 1 — Connect the components

### Goals

- Establish shared architecture.
- Add FastAPI service skeleton.
- Add frontend API client.
- Separate demo data from UI logic.
- Label static data clearly.

### Deliverables

- `docs/ARCHITECTURE.md`
- `docs/DATA_MODEL.md`
- `docs/API_CONTRACT.md`
- `services/api/main.py`
- `services/api/schemas.py`
- `admatch-insights/src/lib/thincApi.ts`
- `admatch-insights/src/data/demoCampaigns.ts`

---

## Phase 2 — Operational MVP

### Goals

- Make one end-to-end flow work:

```text
Campaign form → THINC API → Campaign analysis result → dashboard display
```

### Deliverables

- Campaign Analyzer screen.
- API error handling.
- Loading states.
- Demo/Live badge.
- Export JSON.
- Basic API tests.

---

## Phase 3 — Data ingestion

### Goals

- Add real data entry paths without overbuilding OAuth too early.

### Deliverables

- Manual CSV upload.
- Google Sheets import.
- Basic campaign data mapper.
- Data validation report.
- Integration status page.

---

## Phase 4 — Live integrations

### Goals

- Connect live systems carefully.

### Candidate integrations

- Meta Ads API.
- Shopify.
- WhatsApp Business.
- Shipping provider.
- n8n webhook.

### Guardrail

No card can display `connected` unless the backend confirms a live token, successful sync, and timestamp.

---

## Phase 5 — Academy OS

### Goals

- Convert the same system into a student operating environment.

### Deliverables

- Student project workspace.
- Persona builder.
- Founder readiness scoring.
- Weekly execution check-ins.
- Mentor review flow.
- Kill/Fix/Scale assignment reports.

---

## Phase 6 — Reports and IP protection

### Goals

- Make outputs exportable and legally clean.

### Deliverables

- PDF reports.
- Watermarked exports.
- Ownership notice in reports.
- Legal disclaimers.
- Versioned theory registry.

---

## Phase 7 — SaaS readiness

### Goals

- Turn the system into a robust platform.

### Deliverables

- Authentication.
- Roles and permissions.
- Database.
- Multi-tenant workspaces.
- Audit log.
- Billing.
- Backups.

---

## Strategic priority

Do not start with full SaaS infrastructure.

Start with:

```text
THINC Campaign Analyzer v1
```

Because it creates immediate commercial value and proves the core insight:

> Meta CPA is not enough. Real CPA + delivery reality + profit + behavioral fit drive the decision.
