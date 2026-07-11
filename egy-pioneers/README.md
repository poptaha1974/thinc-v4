# Egy Pioneers — Lead Qualification & Sales Automation System

> **نظام ذكاء اصطناعي متكامل لتصنيف العملاء وأتمتة المبيعات لأكاديمية Egy Pioneers**
>
> Inventor / Owner: **Dr. Ehab Taha (الدكتور إيهاب طه)**
> Version: 1.0 — Created July 11, 2026

---

## Component Status

| Component | Status | Details |
|---|---|---|
| n8n Workflow | ✅ Active | 10 nodes, fully automated |
| Claude AI Classification | ✅ Working | HOT / WARM / COLD scoring |
| Google Sheets | ✅ Working | Auto-populates HOT leads |
| Meta CAPI Pixel Feedback | ✅ Working | SHA-256 hashed, HOT only |
| FunnelFast CRM | ✅ Ready | Tags + Pipeline (needs real contacts) |
| WhatsApp Number Verify | ⏳ Pending | Cooldown 24–72 h |

---

## System Architecture

```
WhatsApp Message → FunnelFast Bot → Webhook → n8n Workflow
                                                    │
                                                    ▼
                                          Claude AI Analysis
                                          (HOT/WARM/COLD)
                                                    │
                                          ┌─────────┴─────────┐
                                          │  HOT Lead?         │
                                          │  Score >= 70       │
                                          └─────────┬─────────┘
                                                    │ YES
                                    ┌───────────────┼───────────────┐
                                    │               │               │
                                    ▼               ▼               ▼
                            Google Sheets    Hash User Data    FunnelFast
                            (HOT Leads)           │           (Tags + Pipeline)
                                                  ▼
                                           Meta CAPI
                                     (Pixel Feedback — HOT only)
```

---

## Key IDs & Configuration

> ⚠️ **Never commit real access tokens or API keys.** Store secrets in n8n credential store or environment variables only.

| Item | Value |
|---|---|
| n8n Workflow ID | `swr2aTOO9NZ5dvQE` |
| Webhook URL | `https://allhomz.app.n8n.cloud/webhook/egy-pioneers-lead` |
| Google Sheet ID | `1v7uMgtMMVwQPBIE-9ZZcQ02PmeTx9c2NPAzQK3sPmx8` |
| Meta Pixel ID | `1604627917208516` |
| Ad Account | `1337470373886269` |
| FunnelFast Location ID | `uDktXedAxUk7WuUq693w` |
| Pipeline ID | `QnXMQbBGOhcMfVLsyJqH` |
| Pipeline Stage (New Lead) | `c0b9f77f-1e12-4a7e-8c3d-5f6a7b8c9d0e` |
| Google Sheet Link | [Open Sheet](https://docs.google.com/spreadsheets/d/1v7uMgtMMVwQPBIE-9ZZcQ02PmeTx9c2NPAzQK3sPmx8/edit) |

---

## Workflow Nodes (10 Total)

### Node 1 — FunnelFast Webhook

Entry point. Receives POST requests from FunnelFast automation when a customer sends a WhatsApp message.

```json
{
  "type": "n8n-nodes-base.webhook",
  "path": "egy-pioneers-lead",
  "httpMethod": "POST",
  "responseMode": "responseNode"
}
```

Expected payload fields: `contact_id`, `contact_name`, `phone`, `message`, `conversation_id`.

---

### Node 2 — Claude AI Lead Analysis

Calls Claude Sonnet via OpenRouter API to classify the incoming message.

**Model:** `anthropic/claude-sonnet-4`

**System Prompt (Arabic):**

```
أنت خبير تصنيف عملاء لأكاديمية تعليمية مصرية (Egy Pioneers).
صنّف العميل بناءً على رسالته:

HOT  (70-100): يسأل عن السعر، المواعيد، طريقة التسجيل، أو يقول "عايز أسجل"
WARM (40-69):  يسأل أسئلة عامة عن المحتوى أو الكورس بدون نية شراء واضحة
COLD (0-39):   رسالة عامة، سبام، أو غير مهتم

أجب بـ JSON فقط:
{"classification":"HOT|WARM|COLD","score":0-100,"reason":"...","suggested_action":"..."}
```

**Response schema:**

```json
{
  "classification": "HOT",
  "score": 85,
  "reason": "العميل سأل عن السعر وطريقة التسجيل",
  "suggested_action": "تواصل فوري — عميل جاهز للشراء"
}
```

---

### Node 3 — Is HOT Lead? (If Node)

Routes execution: HOT leads continue to nodes 4–9, others skip to node 10.

```json
{
  "conditions": {
    "string": [
      {
        "value1": "={{ $json.choices[0].message.content }}",
        "operation": "contains",
        "value2": "\"HOT\""
      }
    ]
  }
}
```

---

### Node 4 — Send HOT Alert to Sales

Posts an internal note inside the FunnelFast conversation so the sales team is immediately notified.

```
POST https://services.leadconnectorhq.com/conversations/{conversationId}/messages
Authorization: ******
Body: { "type": "Note", "message": "🔥 HOT LEAD — يحتاج متابعة فورية" }
```

---

### Node 5 — Tag Contact as HOT

Adds CRM tags to the contact record for segmentation.

```
POST https://services.leadconnectorhq.com/contacts/{contactId}/tags
Authorization: ******
Body: { "tags": ["HOT-Lead", "Egy-Pioneers-Campaign"] }
```

---

### Node 6 — Create Pipeline Opportunity

Creates an opportunity card in the sales pipeline.

```
POST https://services.leadconnectorhq.com/opportunities/
Authorization: ******
Body:
{
  "pipelineId": "QnXMQbBGOhcMfVLsyJqH",
  "stageId":    "c0b9f77f-1e12-4a7e-8c3d-5f6a7b8c9d0e",
  "contactId":  "{contactId}",
  "name":       "HOT Lead - {contact_name}"
}
```

---

### Node 7 — Add to HOT Leads Sheet (Google Sheets)

Appends one row per HOT lead to the tracking spreadsheet.

```json
{
  "operation": "append",
  "documentId": "1v7uMgtMMVwQPBIE-9ZZcQ02PmeTx9c2NPAzQK3sPmx8",
  "sheetName": "HOT Leads",
  "columns": {
    "التاريخ":        "={{ $now.format('YYYY-MM-DD HH:mm') }}",
    "الاسم":          "={{ $('FunnelFast Webhook').item.json.body.contact_name }}",
    "الرقم":          "={{ $('FunnelFast Webhook').item.json.body.phone }}",
    "الرسالة الأولى": "={{ $('FunnelFast Webhook').item.json.body.message }}",
    "التصنيف":        "HOT",
    "نقاط الحرارة":   "={{ $json.choices[0].message.content }}",
    "الحالة":         "جديد - محتاج متابعة"
  }
}
```

---

### Node 8 — Hash User Data (Code Node)

Hashes PII with SHA-256 before sending to Meta CAPI, as required by the Conversions API spec.

```javascript
const crypto = require('crypto');

const phone = ($('FunnelFast Webhook').item.json.body.phone ||
               $('FunnelFast Webhook').item.json.body.contact_phone || '')
               .replace('+', '');
const name  = ($('FunnelFast Webhook').item.json.body.contact_name ||
               $('FunnelFast Webhook').item.json.body.contactName  || '')
               .split(' ')[0].toLowerCase();

const phoneHash   = crypto.createHash('sha256').update(phone).digest('hex');
const nameHash    = crypto.createHash('sha256').update(name).digest('hex');
const countryHash = crypto.createHash('sha256').update('eg').digest('hex');

return [{
  json: {
    data: [
      {
        event_name:    "Lead",
        event_time:    Math.floor(Date.now() / 1000),
        action_source: "system_generated",
        user_data: {
          ph:      [phoneHash],
          fn:      [nameHash],
          country: [countryHash]
        },
        custom_data: {
          lead_classification: "HOT",
          source:              "WhatsApp_Campaign_Egy_Pioneers",
          content_name:        "Egy Pioneers Course"
        }
      }
    ]
  }
}];
```

---

### Node 9 — Meta CAPI — HOT Lead Feedback

Sends the hashed event to the Meta Conversions API to train the pixel on high-intent customers.

```
POST https://graph.facebook.com/v18.0/1604627917208516/events?access_token={META_CAPI_TOKEN}
Content-Type: application/json
Body: {{ JSON.stringify($('Hash User Data').item.json) }}
```

---

### Node 10 — Respond to Webhook

Always runs last. Returns an acknowledgement to FunnelFast so the webhook does not time out.

```json
{ "status": "received" }
```

---

## Important Notes

1. **Meta CAPI Token Expiry** — The access token expires every 60 days. Set a calendar reminder to regenerate it: *Events Manager → Datasets → academy pixel → Settings → Generate access token*.

2. **HOT-Only Pixel Feedback** — Only leads with score ≥ 70 are sent to Meta CAPI. This teaches the pixel to find more high-intent audiences and avoids polluting the dataset with cold traffic.

3. **SHA-256 Hashing** — All user PII (phone, first name, country) is hashed before transmission to Meta, as required by the [Meta Conversions API spec](https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/customer-information-parameters).

4. **`continueOnFail: true`** — Every node is configured with this flag. If one integration fails (e.g. Google Sheets is temporarily unavailable), the rest of the pipeline still runs.

5. **OpenRouter Fallback** — Claude AI is accessed via OpenRouter. If `anthropic/claude-sonnet-4` is unavailable, configure `openai/gpt-4o-mini` as a fallback. Estimated cost: ~$0.001 per classification.

---

## Pending Tasks

| Task | ETA | Action Required |
|---|---|---|
| Verify WhatsApp 01025073479 | 24–72 h | Try again after cooldown |
| Change campaign number | After verify | Update in Meta Ads Manager |
| Monitor first real leads | Ongoing | Check Google Sheet & Events Manager |

---

## Related Files

| File | Purpose |
|---|---|
| `egy-pioneers-workflow.json` | Full n8n workflow — import directly into n8n |
| `README.md` | This file — project overview |
| `setup-guide.md` | Step-by-step setup instructions |
