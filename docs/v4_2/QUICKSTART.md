# THINC™ v4.2 — Media Test Protocol Engine

## ما الجديد؟

الإصدار v4.2 يضيف طبقة **Media Test Protocol Engine** فوق Creative Intelligence، وتقوم تلقائيًا بـ:

- اختيار هدف الحملة حسب مسار البيع: Website / WhatsApp / Instagram DM / Messenger / Lead Form.
- حساب `Break-even Delivered CPA` و`Target Delivered CPA` و`Target Purchase CPA`.
- بناء مراحل اختبار الزوايا والـHooks والمونتاج والعرض والـCTA.
- حساب مدة كل مرحلة والميزانية لكل Variant.
- إنشاء قواعد `Soft Stop` و`Hard Stop`.
- منع الـScale قبل تحقق Delivered Orders وربح موجب.
- فرض بوابة `Market Signal Triangulation` قبل الاختبار والـScale.
- فرض مسارَي Niche Family Tree: الاكتشاف من السوق للمنتج، والتحقق العكسي من المنتج للسوق.
- منع القرار العام `PASS` لو مسار النيتش أو نقطة الالتقاء أو الاقتصاديات ناقصة.
- فصل الوصول بالمتصفح/الملف عن الربط الآلي الذي ما زال `PENDING_INTEGRATION`.

## 1) تشغيل الاختبارات

```bash
python THINC_v4_2_Media_Test_Protocol_Master_Framework.py --test
```

الناتج المتوقع في هذه الحزمة:

```json
{
  "total": 44,
  "passed": 44,
  "failed": 0,
  "success_rate": 100.0,
  "v3_status": "not_available"
}
```

واختبارات البوابة السلوكية المستقلة:

```bash
python -m unittest discover -s tests -v
```

آخر تشغيل موثق لهذه الحزمة بعد دمج Niche Family Tree: `41/41` اختبارًا سلوكيًا وحوكميًا ناجحًا، بالإضافة إلى `44/44` اختبارًا مدمجًا. اعتمد دائمًا على ناتج التشغيل الحالي عند أي تعديل جديد.

`v3_status = not_available` يعني أن ملف v3.1 التابع غير موجود بجوار الملف في بيئة الاختبار الحالية، وليس فشلًا في اختبارات v4.2.

## 2) تشغيل مثال Media Protocol جاهز

```bash
python THINC_v4_2_Media_Test_Protocol_Master_Framework.py --media-example
```

## 3) الاختبار ببياناتك من JSON

عدّل الملف:

```text
THINC_v4_2_media_input_template.json
```

ثم شغّل:

```bash
python thinc_v4_2_media_runner.py THINC_v4_2_media_input_template.json --output my_media_plan.json
```

## أهم الحقول

### Economics

- `selling_price`: سعر البيع.
- `product_cost`: تكلفة المنتج.
- `packaging_cost`: التغليف.
- `company_shipping_cost`: الشحن الذي تتحمله الشركة.
- `collection_fees`: رسوم التحصيل.
- `expected_return_cost_per_order`: متوسط تكلفة المرتجعات موزعًا على الطلبات.
- `variable_operations_cost`: تكلفة تشغيل متغيرة لكل طلب.
- `confirmation_rate_pct`: نسبة تأكيد الطلبات.
- `delivery_rate_from_confirmed_pct`: نسبة التسليم من الطلبات المؤكدة.
- `safety_margin_pct`: هامش أمان لا يُستهلك في الإعلانات.

### Config

- `sales_channel`: `website` أو `whatsapp` أو `instagram_dm` أو `messenger` أو `lead_form`.
- `total_daily_budget`: إجمالي الميزانية اليومية للاختبار.
- `pixel_ready`: هل الـPixel يعمل؟
- `capi_ready`: هل Conversions API جاهزة؟
- `purchase_event_configured`: هل Purchase Event مضبوط؟
- `sales_messaging_objective_available`: هل Sales لمراسلات WhatsApp ظاهر داخل الحساب؟
- `evidence_mode`: `lean` أو `standard` أو `conservative`.
- `decision_stage`: `pre_test_research` أو `controlled_test` أو `scale`.

### Market Evidence

كل سجل داخل `market_evidence` يستخدم نفس العقد سواء تم جمعه بالمتصفح أو رُفع من ملف:

- `source`: `google_trends` أو `meta_ad_library` أو `marketplace` أو `first_party_campaign`.
- `status`: `COLLECTED` أو `NOT_COLLECTED` أو `STALE` أو `INVALID` أو `NOT_APPLICABLE`.
- `query`, `country`, `timeframe`, `collected_at`, `collection_method`.
- `source_reference`, `summary`, `metrics` لإثبات المصدر والتفسير.

حدود حداثة الدليل الافتراضية:

| المصدر | أقصى عمر |
|---|---:|
| Google Trends | 7 أيام |
| Meta Ad Library | 3 أيام |
| Marketplace | 3 أيام |
| First-party campaign عند Scale | يوم واحد |

القالب المرفق **مثال صناعي للـSchema فقط**، ولذلك تشغيله كما هو يرجع `HOLD_FOR_RESEARCH` ويصنّف سجلاته `INVALID`. لازم تستبدل كل سجل بنتيجة فعلية حديثة قبل أن تسمح البوابة بقرار `PASS`.

### Niche Validation

لا يكفي تمرير `market_evidence`. أضف `niche_validation` ويتضمن:

- `discovery_path`: Market وNiche وMicro-Niche وPersona وProblem/JTBD وProduct.
- `reverse_validation_path`: نفس المستويات من Product إلى Market.
- `product_solves_problem` و`persona_matches_problem`.
- `offer_strength`: `strong` أو `weak`.
- `economics_viable`.
- `critical_risks` و`unresolved_evidence`.

لو الحقل ناقص، التقرير العام يرجع `INCOMPLETE` حتى لو كانت بوابة السوق `PASS`.

## منطق القرار

```text
Market → Niche → Micro-Niche → Persona → Problem/JTBD → Product
↕ Convergence
Product → Problem/JTBD → Persona → Micro-Niche → Niche → Market
→ Market Signal Gate + Product Economics + Critical Risks
→ Campaign Objective
→ Angle Test
→ Hook Test
→ Editing Test
→ Offer & CTA Test
→ Winner Validation
→ Delivered Profit Gate
→ Kill / Fix / Iterate / Scale
```

لو `niche_validation` غير موجود، القرار الأعلى `INCOMPLETE`. ولو مسار النيتش كامل لكن `market_evidence` ناقصة، القرار يصبح `HOLD_FOR_RESEARCH`. وفي مرحلة `scale`، اكتمال الأدلة لا يلغي فيتو الاقتصاديات: عدد Delivered Orders وDelivered CPA وDelivery Rate لازم يمروا حدود `ScalePolicy` الحالية.

احتفظ دائمًا بالفصل بين:

- `market_signal_gate.decision`: نتيجة مكوّن البحث.
- `media_protocol_decision`: نتيجة مكوّن الميديا والـScale.
- `niche_validation.strategic_decision`: قرار ملاءمة المنتج/العميل/العرض.
- `decision`: القرار العام بعد بوابة الاكتمال والفيتو.

## حالة الوصول للمصادر

- `BROWSER_ASSISTED_AVAILABLE`: متاح الآن لجمع النتائج وتوثيقها.
- `FILE_INGESTION_AVAILABLE`: متاح الآن لـJSON/CSV الموثق.
- `AUTOMATED_PROVIDER_PENDING`: لا يوجد ربط آلي كامل حاليًا.
- وجود API key وحده لا يغيّر حالة البوابة ولا يُنتج Evidence.

## تنبيه تشغيلي

مسميات الخيارات داخل Meta Ads Manager قد تختلف حسب الحساب والمنطقة وتحديثات المنصة. المحرك يسجل الـfallback المناسب ولا يغيّر الـKPI النهائي: **Delivered Profit + Delivered CPA**.
