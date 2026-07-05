# Egyptian Social-Cultural Intelligence Engine

This document defines the missing cultural layer for THINC v4.0.

The existing Egyptianization layer adapts language by generation and skill level. This new layer adds social and cultural intelligence:

- local generational cohorts,
- life stages,
- gift occasions,
- family influence,
- social embarrassment risk,
- price-band meaning,
- trust signals,
- packaging expectations,
- religious and seasonal context,
- and channel behavior.

---

## 1. Why this layer matters

In Egyptian ecommerce, especially gifts and household products, customers do not buy by price and function alone.

They also ask:

- Will this look respectable?
- Will it embarrass me?
- Will my mother/wife/sister approve?
- Is it suitable for the occasion?
- Does it look more expensive than its price?
- Can I exchange it if the recipient does not like it?
- Can I trust this shop?
- Will it arrive before the occasion?

Without this layer, a product can look profitable numerically but fail socially.

---

## 2. New engine name

```python
EgyptianSocialCulturalEngine
```

Location:

```text
src/thinc_v4/egyptian_social_culture.py
```

---

## 3. Local generational cohorts

The model should not rely only on Western labels such as Gen X, Millennial, and Gen Z.

It now includes practical Egyptian labels:

| Cohort | Meaning |
|---|---|
| `INFTAH_SATELLITE` | جيل الانفتاح والفضائيات |
| `INTERNET_TRANSITION` | جيل انتقال الإنترنت والموبايل |
| `SOCIAL_NATIVE` | جيل السوشيال والموبايل |
| `POST_COVID_EARLY` | جيل ما بعد الكورونا والذكاء الاصطناعي |
| `MIXED_HOUSEHOLD` | جمهور عائلي مختلط القرار |

---

## 4. Life stages

A generation alone is not enough. A 29-year-old single employee does not buy like a 29-year-old parent.

Life stages:

- Student.
- Early career.
- Engaged.
- Newly married.
- Parent.
- Family decision maker.
- Business owner.
- Corporate buyer.

---

## 5. Gift occasions

The engine supports Egyptian social gift moments such as:

- birthday,
- Mother’s Day,
- engagement,
- wedding / katb ketab,
- anniversary,
- graduation,
- new baby,
- family visit,
- work colleague,
- manager / teacher,
- client appreciation,
- Ramadan / Eid,
- apology / thanks / courtesy.

Each occasion has:

- emotional job,
- acceptable price bands,
- packaging expectation,
- respectability rule,
- common anxieties,
- decision influencers,
- recommended message angles,
- sensitive angles to avoid.

---

## 6. Price bands

For gift positioning under 1000 EGP:

| Band | Meaning |
|---|---|
| `SYMBOLIC` | رمزية — أقل من 300 جنيه |
| `PRACTICAL` | عملية محترمة — 300 إلى 600 جنيه |
| `PREMIUM_AFFORDABLE` | شكلها أغلى من سعرها — 600 إلى 1000 جنيه |
| `ABOVE_POSITIONING` | خارج تموضع تحت الألف — أعلى من 1000 جنيه |

The key idea is:

> Under 1000 should mean smart value, not cheapness.

---

## 7. Social fit scoring

The engine evaluates whether a gift fits socially by checking:

- price band fit,
- packaging,
- exchange policy,
- social proof,
- practicality,
- perceived value,
- clear use case.

Output:

```json
{
  "score": 8.1,
  "risk_level": "low",
  "positioning_sentence": "هدايا عملية محترمة تحت 1000 جنيه...",
  "blind_spots": [],
  "recommendations": [],
  "suggested_hooks": []
}
```

---

## 8. Strategic use case: Gift shop under 1000 EGP

Positioning:

```text
هدايا عملية محترمة تحت 1000 جنيه، مختارة حسب المناسبة والميزانية، بتغليف يليق ويقلل حيرة الاختيار.
```

Main promise:

```text
قولنا المناسبة والميزانية، ونرشحلك هدية تليق من غير حيرة.
```

Category design:

```text
هدايا تحت الألف — شكلها حلو وتنفع بجد.
```

---

## 9. Added blind spots

The model now explicitly checks:

1. Social respectability.
2. Embarrassment risk.
3. Packaging quality.
4. Gift use case clarity.
5. Social proof.
6. Exchange policy.
7. Buyer vs recipient vs payer difference.
8. Religious and seasonal context.
9. Relationship sensitivity.
10. Channel fit by generation.
11. Geography / class nuance.
12. Whether the gift is too personal or socially safe.

---

## 10. Caution

These profiles are not deterministic labels.

They are decision-support heuristics that must be validated with:

- campaign data,
- WhatsApp conversations,
- store sales,
- call center objections,
- delivery and return data,
- and customer feedback.
