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

## Error contract

Invalid enum values (occasion, domain, cohort, signal type, …) are coerced by
`_enum_from_value`, which raises `ValueError` listing the valid values. All apps
install `services.api.errors.install_error_handlers`, so those become:

```json
HTTP 422
{"detail": "Invalid value 'x'. Valid values: …", "error": "invalid_input"}
```

Without the handler FastAPI reported a client mistake as `500 Internal Server
Error` and swallowed the helpful message.

## Type checking

`services` is inside the MyPy strict scope (`files` in `pyproject.toml`), with the
`pydantic.mypy` plugin enabled so model constructors are understood.

## Tests

```bash
pytest tests/services -q
```
