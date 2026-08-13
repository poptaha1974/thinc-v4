# Adaptive Market Learning Engine

This layer makes THINC v4.0 adaptive instead of static.

The goal is not to claim that the model knows the market forever. The goal is to make the model detect when reality changes and generate controlled updates.

---

## 1. Core principle

```text
Prediction before campaign
        ↓
Actual result after campaign
        ↓
Gap analysis
        ↓
Behavior shift detection
        ↓
Weight update proposal
        ↓
Experiment recommendation
        ↓
Human review
        ↓
Updated model rule
```

---

## 2. What the engine learns from

The engine accepts signals from:

- campaign results,
- WhatsApp objections,
- competitor moves,
- supplier events,
- creative fatigue,
- profit leakage,
- post-purchase feedback,
- brand drift,
- ethics risk,
- cultural shift.

---

## 3. Human behavior shifts detected

The engine can detect shifts such as:

- price sensitivity increased,
- trust demand increased,
- delivery urgency increased,
- social proof demand increased,
- novelty fatigue,
- value-seeking increased,
- status signaling increased,
- channel migration,
- unknown shift.

---

## 4. Default adaptive weights

The model tracks strategic weights for:

- price sensitivity,
- trust weight,
- delivery urgency,
- social proof,
- packaging,
- creative freshness,
- supplier reliability,
- profit leakage,
- brand consistency,
- ethics guardrail.

These weights are not blindly changed. The engine proposes changes and requires human review for major updates.

---

## 5. Prediction vs actual

Input example:

```json
{
  "context_name": "Gift campaign - Mother's Day",
  "prediction": {
    "expected_score": 8.0,
    "expected_real_cpa": 120,
    "expected_conversion_rate": 12,
    "expected_delivery_rate": 80,
    "expected_net_profit": 15000,
    "expected_objections": ["السعر غالي", "ينفع تتغلف؟"]
  },
  "actual": {
    "actual_score": 5.8,
    "actual_real_cpa": 190,
    "actual_conversion_rate": 7,
    "actual_delivery_rate": 72,
    "actual_net_profit": 3000,
    "observed_objections": ["هتلحق توصل قبل عيد الأم؟", "هيطلع زي الصورة؟"],
    "refund_or_return_rate": 0.18
  }
}
```

The engine identifies where reality diverged from the model.

---

## 6. Adaptive output

The engine returns:

- learning score,
- severity,
- action,
- prediction gap summary,
- detected behavior shifts,
- proposed rule updates,
- experiments to run,
- blind spots discovered,
- human review notes,
- next observation plan.

---

## 7. Example actions

The engine may recommend:

- keep rule,
- watch,
- run experiment,
- update weight,
- update rule,
- escalate human review,
- pause scaling.

---

## 8. Example experiments

If trust demand increases:

```text
Test real photos, reviews, exchange policy, and unboxing proof stack.
```

If delivery urgency increases:

```text
Test city-limited fast delivery promise instead of national delivery promise.
```

If creative fatigue appears:

```text
Rotate first 3 seconds, hook, and UGC angle before changing the whole offer.
```

If price sensitivity increases:

```text
Test value framing vs discount framing while keeping the same product price.
```

---

## 9. API endpoints

A standalone API app was added:

```bash
uvicorn services.api.learning_app:app --reload --port 8001
```

Endpoints:

```text
GET  /health
GET  /api/adaptive-learning/options
POST /api/adaptive-learning/evaluate
```

Note: registering this router inside `services/api/main.py` requires adding:

```python
from services.api.adaptive_learning_routes import router as adaptive_learning_router
app.include_router(adaptive_learning_router)
```

The connector blocked the full `main.py` update during this session, so the standalone app is provided as a safe immediate runtime path.

---

## 10. Safety standard

The model should not auto-change permanent strategic rules from one weak signal.

Required standard:

```text
One campaign = observation.
Repeated pattern = hypothesis.
Repeated validated pattern = model update.
```

---

## 11. Final operating philosophy

The model should never say:

```text
I know the market forever.
```

It should say:

```text
I compare my prediction with market reality, detect drift, and update my assumptions under human review.
```

This turns THINC from a static framework into a learning commercial intelligence system.
