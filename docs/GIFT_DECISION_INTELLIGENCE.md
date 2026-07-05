# Gift Decision Intelligence Layer

This layer strengthens THINC v4.0 for Egyptian ecommerce gift positioning and closes the main remaining blind spots after the Egyptian Social-Cultural Intelligence Engine.

It is designed for offers such as:

```text
هدايا عملية محترمة تحت 1000 جنيه
```

---

## 1. Why this layer exists

The previous social-cultural engine understands:

- generations,
- life stages,
- occasions,
- family influence,
- embarrassment risk,
- price-band meaning,
- packaging expectations,
- and trust signals.

This layer goes further and evaluates the full commercial decision:

```text
هل هذا المنتج، بهذه الفئة السعرية، مناسب لهذه المناسبة، لهذه العلاقة، في هذه المنطقة، بهذا الموسم، وبهذا مستوى الثقة والتوصيل؟
```

---

## 2. Blind spots closed

### 2.1 Product-to-Occasion Fit

Not every product fits every occasion.

Example:

| Product | Birthday | Mother's Day | Manager | Engagement |
|---|---|---|---|---|
| Mug / Tumbler | Strong | Medium | Safe | Weak |
| Beauty box | Strong | Strong | Risky | Strong |
| Office accessory | Medium | Weak | Strong | Weak |
| Leather wallet | Strong | Medium | Strong | Strong |

The engine scores whether the product naturally fits the occasion and relationship.

---

### 2.2 Buyer / Recipient / Payer Split

Gift commerce often involves more than one decision-maker:

| Role | Example |
|---|---|
| Buyer | The person chatting on WhatsApp |
| Recipient | The person receiving the gift |
| Payer | The person paying |
| Influencer | Mother, wife, sister, friend, manager |

The engine explicitly recognizes these roles so the message does not speak to the wrong person.

---

### 2.3 Gender & Relationship Safety

The model classifies gift safety:

- Safe neutral.
- Practical safe.
- Personal.
- Romantic.
- Formal.
- Risky / misunderstood.

This prevents socially risky recommendations such as giving a personal romantic gift to a colleague or manager.

---

### 2.4 Geography & Class Lens

The engine now recognizes:

- Greater Cairo.
- Alexandria.
- Delta.
- Upper Egypt.
- Canal Cities.
- New Cities.
- Coastal / seasonal areas.
- Mixed national audience.

And social class signals:

- value-sensitive,
- middle mainstream,
- aspirational,
- premium-leaning,
- corporate.

---

### 2.5 Calendar & Seasonality

The engine supports:

- Ramadan.
- Eid.
- Mother's Day.
- Valentine.
- Graduation season.
- Back to school.
- Wedding season.
- Year-end corporate gifts.
- Summer visits.
- Always-on gifting.

It returns seasonality guidance such as when to start campaigns and which angle to emphasize.

---

### 2.6 Packaging Quality Index

Packaging is not an add-on in gift commerce. It is part of the product.

The engine uses `packaging_score` as one of the main scoring factors.

A low packaging score reduces the decision score because it raises embarrassment risk.

---

### 2.7 Trust & Scam Fear Layer

The engine checks:

- real product photos,
- reviews,
- exchange policy,
- trust score,
- visible proof,
- and whether the product looks like the ad.

This addresses the Egyptian ecommerce fear:

```text
هيوصل؟ هيطلع زي الصورة؟ هعرف أبدل؟ ده محل حقيقي؟
```

---

### 2.8 Delivery Urgency Layer

A gift loses value if it arrives late.

The engine checks urgency:

- same day,
- next day,
- 2-3 days,
- week plus,
- not time-sensitive.

If the occasion is near, it raises delivery risk and recommends realistic delivery promises.

---

### 2.9 Objection Library by Social Context

The engine generates objections such as:

- مش عارف هتعجبه ولا لا.
- مش هتبان بسيطة؟
- ينفع تتغلف؟
- ينفع أبدلها؟
- محتاجها بسرعة، هتلحق توصل؟
- تنفع لمدير/مدرس من غير ما تبان مبالغ فيها؟
- تنفع لحماتي ومتبانش قليلة؟

---

### 2.10 Repeat Occasion CRM

The engine outputs CRM follow-ups:

- record the occasion,
- record the relationship,
- record the budget,
- record taste preference,
- remind the customer before the next similar occasion.

This turns one-time gift purchases into a memory-based repeat purchase engine.

---

## 3. API endpoints

### `GET /api/gift-intelligence/options`

Returns available:

- geographies,
- social class signals,
- recipient gender contexts,
- relationships,
- buyer roles,
- product categories,
- gift safety classes,
- seasons,
- delivery urgency levels,
- occasions,
- price bands,
- completeness checklist.

### `POST /api/gift-intelligence/evaluate`

Evaluates a full gift decision.

Input includes:

- product profile,
- occasion,
- relationship,
- recipient gender,
- geography,
- class signal,
- buyer role,
- season,
- delivery urgency,
- exchange policy,
- real photos,
- reviews,
- personalization,
- whether buyer knows recipient taste.

Output includes:

- score,
- risk level,
- product occasion fit,
- safety verdict,
- positioning,
- recommended angle,
- blind spots,
- recommendations,
- objections,
- WhatsApp replies,
- CRM follow-ups,
- next best actions.

---

## 4. Completeness checklist

The model now checks:

1. Product-to-Occasion Fit Matrix.
2. Buyer / Recipient / Payer Split.
3. Gender & Relationship Safety.
4. Geography & Class Lens.
5. Seasonality Window.
6. Packaging Quality Score.
7. Trust & Scam Fear Signals.
8. Delivery Urgency Risk.
9. Objection Library.
10. WhatsApp Replies.
11. CRM Repeat Occasion Follow-up.
12. Stock Readiness.
13. Margin Score.
14. Real Photos / Reviews / Exchange Policy.
15. Whether the message communicates smart value, not cheapness.

---

## 5. Strategic principle

The strongest gift positioning is not:

```text
منتجات أقل من 1000 جنيه
```

It is:

```text
هدايا عملية محترمة تحت 1000 جنيه، مختارة حسب المناسبة والعلاقة والميزانية، بتغليف يليق ويقلل حيرة الاختيار.
```

---

## 6. Remaining caution

No model can permanently remove every unknown.

The correct standard is:

```text
No known critical blind spot remains unmodeled for the current MVP scope.
```

But the model must still be validated with:

- actual product data,
- campaign data,
- WhatsApp objections,
- delivery performance,
- returns,
- repeat purchase,
- and customer feedback.
