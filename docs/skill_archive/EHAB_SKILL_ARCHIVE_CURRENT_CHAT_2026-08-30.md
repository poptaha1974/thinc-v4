# Ehab Skill Archive — Current Chat

**Archive date:** 2026-08-30  
**Owner:** Dr. Ehab Taha / EgyPioneers / Allhomz Operations  
**Source:** Current Chat Conversation  
**Skill count:** 18  
**Canonical Notion archive:** https://app.notion.com/p/df42aecd314246f591c19abec9b7a5e4  
**Persistence status:** GitHub fallback archive because Notion connector was unavailable during this operation  

## Archive trigger

> أرشف الدردشة الحالية كمهارات باستخدام Ehab Skill Archive، ونفّذ الأرشفة والحفظ فعليًا دون إرجاع Prompt أو طلب أي تصنيف مني.

## Operating rule

- Extract reusable skills, workflows, decision rules, guardrails, prompts, and templates.
- Deduplicate against existing archive records.
- Update existing skills where appropriate and create only genuinely new skills.
- Persist the archive before claiming completion.
- Do not return a prompt or request user classification.

## Archived skills

### 1. THINC Core Product Analysis Skill

**Purpose:** تحليل أي منتج باستخدام بحث السوق وSWOT/TOWS وطبقات THINC والمؤشرات والتوصية.

**When to use:**
- قبل إطلاق منتج
- عند تقييم فرصة سوقية
- عند بناء عرض أو Funnel

**Inputs:**
- اسم المنتج
- الفئة
- الجمهور
- السعر والتكلفة
- صور/وصف
- بيانات السوق والمنافسين

**Workflow:**
1. تعريف المنتج
2. Marketing Research
3. SWOT
4. TOWS
5. تطبيق طبقات THINC
6. حساب المؤشرات
7. قرار أولي

**Outputs:**
- تقرير منتج
- SWOT/TOWS
- Scores
- قرار Launch/Modify/Hold
- Action Items

**Guardrails:**
- لا تعتمد على الانطباع
- لا تستخدم وعود غير مثبتة
- لا Scale قبل الربحية والتسليم

---

### 2. THINC Profit & Reality Validation Gate

**Purpose:** تحويل القرار الإعلاني إلى قرار ربحي قائم على Delivered Net Profit وReal CPA.

**When to use:**
- قبل Kill/Fix/Scale
- عند مقارنة حملات
- عند حساب Break-even

**Inputs:**
- Ad Spend
- Orders
- Confirmed
- Delivered
- NDR
- COGS
- Shipping
- Packaging
- Failed delivery loss
- Operational leakage

**Workflow:**
1. حساب Meta CPA
2. حساب Delivered CPA
3. حساب Net Profit
4. تطبيق Hard Financial Gate
5. إخراج القرار

**Outputs:**
- Real CPA
- Delivered Net Profit
- Safe CPA
- Kill/Fix/Scale

**Guardrails:**
- Composite Score لا يتجاوز Hard Financial Gate
- NDR=19% يدخل في حسابات Allhomz ما لم يتم تحديثه

---

### 3. THINC Campaign Event Ladder Skill

**Purpose:** تنظيم أحداث Meta/CAPI وضمان أن Purchase يمثل Delivered + Paid.

**When to use:**
- تصميم Tracking
- مراجعة CAPI
- اختيار Optimization Event

**Inputs:**
- Event map
- Order lifecycle
- Confirmation process
- Delivery/payment status

**Workflow:**
1. ViewContent
2. AddToCart
3. InitiateCheckout
4. OrderPlaced
5. ConfirmedOrder
6. DeliveredPurchase

**Outputs:**
- Event Map
- Quality Event Recommendation
- Tracking Risks

**Guardrails:**
- IC تشخيص مؤقت
- Purchase = Delivered + Paid فقط
- لا ترسل Purchase عند OrderPlaced في COD

---

### 4. Karseell Demand Probe Skill

**Purpose:** تحليل Karseell كحالة Haircare مصرية مع التركيز على الثقة والأصالة والربحية.

**When to use:**
- تحليل Karseell
- تدريب الطلاب
- مراجعة حملة Beauty/Haircare

**Inputs:**
- بيانات المنتج
- الأسعار
- المخزون
- Pixel
- Proof Stack
- Unit economics

**Workflow:**
1. بحث السوق
2. SWOT/TOWS
3. THINC scoring
4. Trust analysis
5. Financial gates
6. Conditional GO

**Outputs:**
- MODIFY/CONDITIONAL GO
- بوابات إطلاق
- زوايا آمنة
- قائمة مخاطر

**Guardrails:**
- لا ادعاء نتيجة سحرية
- تحقق من Pixel والسعر والمخزون
- اعتمد Matured Delivered Net Profit

---

### 5. Egyptian Social-Cultural Intelligence Skill

**Purpose:** فهم الأجيال ومراحل الحياة والأعراف والتقاليد وتأثير العائلة والإحراج والثقة.

**When to use:**
- بناء Persona
- صياغة رسالة مصرية
- تقييم عرض اجتماعي

**Inputs:**
- الجيل
- مرحلة الحياة
- المنطقة
- المناسبة
- العلاقة
- السعر

**Workflow:**
1. تحديد cohort
2. تحديد life stage
3. تحليل family influence
4. تحليل status/embarrassment
5. تحديد trust signals
6. اختيار اللغة

**Outputs:**
- Social profile
- Words to use/avoid
- Trust builders
- Risk flags

**Guardrails:**
- Heuristics وليست أحكامًا قطعية
- تحتاج تحققًا من بيانات السوق

---

### 6. Gift Decision Intelligence Skill

**Purpose:** تقييم المنتج كهدية حسب المناسبة والعلاقة والسعر والتغليف والتوصيل والـCRM.

**When to use:**
- متاجر الهدايا
- تموضع هدايا تحت 1000
- ترشيح منتجات حسب المناسبة

**Inputs:**
- المنتج
- المناسبة
- العلاقة
- المستلم
- الدافع
- السعر
- التغليف
- التوصيل

**Workflow:**
1. Product-to-Occasion Fit
2. Buyer/Recipient/Payer split
3. Safety
4. Seasonality
5. Packaging
6. Trust
7. Delivery urgency
8. Objections
9. CRM

**Outputs:**
- Gift Fit Score
- Risk Level
- Positioning
- Hooks
- WhatsApp replies
- CRM follow-ups

**Guardrails:**
- تجنب الهدايا الشخصية في السياقات الرسمية
- لا تعد بتوصيل غير مضمون
- تحت الألف = قيمة ذكية لا رخص

---

### 7. Adaptive Market Learning Skill

**Purpose:** جعل THINC يتعلم من الفرق بين التوقع والنتيجة الفعلية وتغير سلوك البشر.

**When to use:**
- بعد نضج نتائج حملة
- عند ظهور اعتراضات جديدة
- عند تغير السوق

**Inputs:**
- Prediction
- Actual outcome
- Signals
- Current weights

**Workflow:**
1. Gap analysis
2. Behavior shift detection
3. Weight update proposal
4. Experiment design
5. Human review

**Outputs:**
- Learning Score
- Severity
- Actions
- Experiments
- Rule update candidates

**Guardrails:**
- حملة واحدة = ملاحظة
- تكرار = فرضية
- تحقق متكرر = تحديث
- لا تعديل دائم دون Human Review

---

### 8. External Social Research & Daily Intelligence Skill

**Purpose:** إدخال الأخبار والمقالات والتحليلات الاقتصادية والاجتماعية واتجاهات الأسعار والبحث اليومي.

**When to use:**
- قبل قرارات إطلاق
- عند قراءة مزاج السوق
- عند تغير الأسعار أو الأحداث

**Inputs:**
- News
- Official data
- Economic/social analysis
- Search trends
- Price monitoring
- Internal observations

**Workflow:**
1. جمع observations
2. Source audit
3. Confidence scoring
4. Commercial implications
5. Feed adaptive learning

**Outputs:**
- Top signals
- Behavior shifts
- Risks/opportunities
- Weight updates
- Campaign guidance

**Guardrails:**
- مقال واحد = weak signal
- مصادر متعددة = strong signal
- السياسة سياق Tone/Risk فقط لا تلاعب

---

### 9. THINC Student Training & Booklet Skill

**Purpose:** تحويل THINC إلى مادة تعليمية عملية للطلاب والطالبات.

**When to use:**
- بناء كتيب
- تصميم منهج
- شرح النموذج
- إعداد أمثلة وتمارين

**Inputs:**
- مكونات THINC
- أمثلة منتجات
- Workflows
- SWOT/TOWS
- قواعد الأخلاق

**Workflow:**
1. تبسيط المفاهيم
2. شرح المكونات
3. أمثلة
4. قوالب
5. Checklists
6. تمارين

**Outputs:**
- Student booklet
- Catalog
- Word/PDF
- Templates
- Onboarding plan

**Guardrails:**
- لا تبسيط يفسد المعنى
- وضح حدود النموذج
- فرق بين النظرية والبيانات الفعلية

---

### 10. GitHub PR & CI Governance Skill

**Purpose:** حوكمة الدمج ومنع Merge قبل نجاح CI ومراجعة الكود الفعلية.

**When to use:**
- مراجعة PR
- عند فشل CI
- قبل Merge

**Inputs:**
- PR metadata
- Workflow runs
- Tests
- Review evidence

**Workflow:**
1. تحقق من access
2. فرق بين mergeable وready
3. افحص CI
4. تحقق من tests
5. code-level audit
6. قرار merge

**Outputs:**
- Merge readiness
- Blockers
- Checklist
- NO/Conditional YES/YES

**Guardrails:**
- mergeable=true لا يعني ready
- Access Failure Report ليس code review
- PR #5 لا يدمج قبل CI passing

---

### 11. Notion Documentation & Decision Archive Skill

**Purpose:** توثيق القرارات والتحديثات التشغيلية في Notion بشكل منظم.

**When to use:**
- بعد قرار مهم
- بعد تطوير محرك
- عند إنشاء كتيب أو SOP

**Inputs:**
- Summary
- Changes
- Links
- Risks
- Next steps

**Workflow:**
1. تحديد الصفحة
2. منع التكرار
3. تحديث أو إنشاء
4. إضافة الروابط
5. تسجيل القرار

**Outputs:**
- Notion page
- Decision record
- Operational archive

**Guardrails:**
- لا تدعي حفظًا لم يتم
- احفظ الروابط والمصدر
- تجنب كسر المحتوى القديم

---

### 12. THINC Custom GPT Packaging Skill

**Purpose:** تحويل THINC إلى Custom GPT دائم مع Instructions وKnowledge وحماية IP.

**When to use:**
- إنشاء GPT خاص
- تثبيت Trigger Rules
- نشر Knowledge package

**Inputs:**
- Instructions
- Reference files
- Bootstrap
- Framework code
- Theory registry

**Workflow:**
1. Define identity
2. Write instructions
3. Upload knowledge
4. Enable tools
5. Test preview
6. Set privacy

**Outputs:**
- THINC v4 Strategic Commerce Consultant
- Knowledge package
- Test cases

**Guardrails:**
- Only me أولًا
- حافظ على الملكية
- اختبر NDR/Watermark/Financial gate

---

### 13. Access-Limited Audit Classification Skill

**Purpose:** تمييز المراجعة الفعلية من Access Failure Report أو assessment محدود الصلاحيات.

**When to use:**
- عندما يذكر المراجع 404 أو عدم الوصول
- عند تقييم قيمة تقرير مراجعة

**Inputs:**
- Reviewer access evidence
- Diff visibility
- Test visibility
- CI visibility

**Workflow:**
1. تحقق من الوصول
2. صنف التقرير
3. افصل النتيجة عن سببها
4. حدد evidence gaps
5. اطلب audit حقيقي

**Outputs:**
- Audit classification
- Evidence limitations
- Authoritative/non-authoritative verdict

**Guardrails:**
- لا تسمِّه code review بلا diff/code
- لا ترفض conclusion صحيحًا لمجرد ضعف الدليل
- وضح عدم اليقين

---

### 14. CI Failure Triage & Merge Readiness Skill

**Purpose:** تحليل فشل GitHub Actions وتحويله إلى خطة إصلاح قبل الدمج.

**When to use:**
- CI failed
- PR blocked
- قبل إعادة تشغيل workflow

**Inputs:**
- Workflow run
- Jobs
- Logs
- First real error
- Repository state

**Workflow:**
1. حدد job الفاشل
2. استخرج أول error
3. صنف lint/type/test/import/build
4. اصلح السبب الجذري
5. rerun CI
6. verify

**Outputs:**
- Root cause
- Patch plan
- Rerun checklist
- Merge readiness

**Guardrails:**
- لا تخلط conflict مع CI
- لا تدمج قبل passing
- وثّق الدليل

---

### 15. GitHub Audit Prompt Engineering Skill

**Purpose:** صياغة Prompt مراجعة شامل لـGitHub Copilot/Codex/Agent يغطي التقنية والربحية والأخلاق.

**When to use:**
- طلب full audit
- مراجعة PR كبير
- توجيه agent داخل repo

**Inputs:**
- Repo/PR
- Changed files
- Business rules
- Safety constraints
- Output format

**Workflow:**
1. حدد read-only
2. حدد الملفات
3. حدد domains
4. حدد severity
5. حدد required output
6. حدد final merge question

**Outputs:**
- Audit prompt طويل
- PR comment مختصر
- Review checklist

**Guardrails:**
- لا تسمح بتعديل قبل review
- اطلب evidence
- افصل blockers عن follow-ups

---

### 16. Ehab Skill Archive Trigger & Upsert Skill

**Purpose:** تنفيذ أمر أرشفة الدردشة إلى مهارات قابلة لإعادة الاستخدام دون طلب تصنيف من المستخدم.

**When to use:**
- عند كتابة عبارة الأرشفة المعتمدة
- عند طلب حفظ الدردشة كمهارات

**Inputs:**
- Current conversation
- Existing archive records
- Project context

**Workflow:**
1. استخراج skills/workflows/decisions/guardrails/templates
2. Deduplicate
3. Update existing
4. Create new
5. Persist
6. Verify save

**Outputs:**
- Skill records
- Archive manifest
- Save confirmation

**Guardrails:**
- لا ترجع Prompt
- لا تطلب تصنيف
- لا تدعي حفظًا قبل التنفيذ
- استخدم fallback persistent archive إذا تعطل Notion

---

### 17. Living Egyptian Market Intelligence Orchestration Skill

**Purpose:** تنسيق محركات THINC في حلقة واحدة من البحث الخارجي إلى التعلم إلى القرار التجاري.

**When to use:**
- تشغيل THINC كنظام يومي
- ربط research بالحملات
- بناء operating loop

**Inputs:**
- Daily research
- Campaign data
- WhatsApp objections
- Delivery/profit data
- Current weights

**Workflow:**
1. Collect
2. Source scoring
3. Daily intelligence
4. Adaptive learning
5. Commercial recommendation
6. Decision log

**Outputs:**
- Daily Egypt intelligence
- Updated experiments
- Campaign guidance
- Decision record

**Guardrails:**
- لا update من signal واحد
- Net Profit gate
- Human review للسياقات الحساسة

---

### 18. THINC Repository Integration Architecture Skill

**Purpose:** تنظيم thinc-v4 كمحرك وAdMatch كواجهة وFastAPI كطبقة ربط مع Demo/Live separation.

**When to use:**
- تصميم المنظومة
- دمج الريبوهات
- تحديد boundaries

**Inputs:**
- Repositories
- Modules
- API contracts
- Data model
- Integration status

**Workflow:**
1. Assign repo roles
2. Define shared schema
3. Build API boundaries
4. Separate demo/live
5. Document roadmap

**Outputs:**
- Architecture blueprint
- Data model
- API contract
- MVP scope

**Guardrails:**
- لا تكرر scoring في frontend
- لا تدعي integrations حية
- لا تلوث PR غير جاهز بتغييرات أرشيف
