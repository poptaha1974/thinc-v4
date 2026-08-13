# THINC Intelligence OS — Service Layer Docs

**Inventor / Author / Owner:** Dr. Ehab Taha (الدكتور إيهاب طه).

This folder documents the **service layer**: the FastAPI apps under
`services/api/` and the decision engines they expose. For the packaged THINC
engine itself see [`../v4_2/ARCHITECTURE.md`](../v4_2/ARCHITECTURE.md).

## Contract and shape

| Document | Covers |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | how the engine repo, the API, and the AdMatch frontend connect |
| [API_CONTRACT.md](API_CONTRACT.md) | endpoints, request/response shapes, error contract |
| [API_SOCIAL_CULTURE_ADDENDUM.md](API_SOCIAL_CULTURE_ADDENDUM.md) | the social-culture and gift-fit endpoints |
| [DATA_MODEL.md](DATA_MODEL.md) | entities and persisted fields |
| [MVP_SCOPE.md](MVP_SCOPE.md) | what is in and out of the first release |
| [ROADMAP.md](ROADMAP.md) | delivery sequence |
| [LEGAL_GUARDRAILS.md](LEGAL_GUARDRAILS.md) | ownership, attribution, and data-handling limits |

## Engines behind the endpoints

| Document | Engine |
|---|---|
| [GIFT_DECISION_INTELLIGENCE.md](GIFT_DECISION_INTELLIGENCE.md) | `thinc_v4.gift_decision_intelligence` |
| [EGYPTIAN_SOCIAL_CULTURAL_ENGINE.md](EGYPTIAN_SOCIAL_CULTURAL_ENGINE.md) | `thinc_v4.egyptian_social_culture` |
| [ADAPTIVE_MARKET_LEARNING.md](ADAPTIVE_MARKET_LEARNING.md) | `thinc_v4.adaptive_market_learning` |
| [EXTERNAL_SOCIAL_RESEARCH_INTELLIGENCE.md](EXTERNAL_SOCIAL_RESEARCH_INTELLIGENCE.md) | `thinc_v4.external_social_research` |

## Running and testing

```bash
uvicorn services.api.main:app --reload --port 8000            # Intelligence OS
uvicorn services.api.learning_app:app --reload --port 8001    # adaptive learning
uvicorn services.api.research_app:app --reload --port 8002    # external research

pytest tests/services -q
```

Invalid enum input returns `422` with `{"detail": ..., "error": "invalid_input"}`
via `services.api.errors`. `services` is inside the MyPy strict scope.

---
THINC™ — Invented by Dr. Ehab Taha (الدكتور إيهاب طه). © 2026 all rights reserved.
