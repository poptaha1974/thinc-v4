# THINC API Service

This service connects the THINC v4 core engine to external clients such as `admatch-insights`.

---

## Run locally

```bash
python -m pip install -e '.[dev]'
uvicorn services.api.main:app --reload
```

Then open:

```text
http://localhost:8000/docs
```

---

## Main endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Service health |
| `GET /api/theories/summary` | Theory Registry summary |
| `POST /api/campaign/analyze` | Real CPA + profit + THINC decision |
| `POST /api/founder/readiness` | Founder OS score |
| `GET /api/integrations/status` | Demo/live integration state |

---

## Design rule

The frontend may visualize numbers, but this API owns the decision logic.

No frontend screen should claim a campaign is `SCALE`, `FIX`, or `KILL` unless this service returns that decision.
