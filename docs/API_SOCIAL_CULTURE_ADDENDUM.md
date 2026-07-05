# API Addendum — Egyptian Social-Cultural Intelligence

This addendum documents the new social-cultural endpoints added after the initial API contract.

---

## 1. Options

### `GET /api/social-culture/options`

Returns available:

- Egyptian generational cohorts.
- Life stages.
- Gift occasions.
- Price bands.
- Blind-spot checklist.

---

## 2. Social profile

### `POST /api/social-culture/profile`

Request example:

```json
{
  "cohort": "جيل انتقال الإنترنت والموبايل — تقريبًا 1981-1996",
  "life_stage": "بداية شغل"
}
```

Response includes:

- dominant mindset.
- interests.
- buying style.
- family influence.
- status sensitivity.
- embarrassment triggers.
- trust signals.
- preferred channels.
- words to use.
- words to avoid.
- life-stage notes.

---

## 3. Gift social fit

### `POST /api/social-culture/gift-fit`

Request example:

```json
{
  "cohort": "جيل انتقال الإنترنت والموبايل — تقريبًا 1981-1996",
  "life_stage": "بداية شغل",
  "occasion": "عيد ميلاد",
  "price_band": "شكلها أغلى من سعرها — 600 إلى 1000 جنيه",
  "has_packaging": true,
  "has_exchange_policy": true,
  "has_social_proof": true,
  "is_practical": true,
  "looks_more_expensive_than_price": true,
  "has_clear_use_case": true
}
```

Response includes:

- score.
- risk level.
- positioning sentence.
- blind spots.
- recommendations.
- suggested hooks.

---

## 4. Strategic value

This API layer allows AdMatch Insights and THINC v4 to evaluate whether a product or gift offer fits Egyptian social expectations, not only numeric unit economics.

For gift positioning under 1000 EGP, this engine checks:

- whether the price band matches the occasion,
- whether packaging reduces embarrassment risk,
- whether the product has a clear use case,
- whether it looks more valuable than its price,
- whether social proof and exchange policy are strong enough,
- and whether the channel and words fit the intended generation and life stage.
