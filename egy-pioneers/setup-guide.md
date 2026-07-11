# Egy Pioneers — Setup Guide

> Step-by-step instructions to deploy the Lead Qualification & Sales Automation system.

---

## Prerequisites

Before you start, make sure you have active accounts and API access for:

| Service | URL | Needed For |
|---|---|---|
| n8n Cloud | [allhomz.app.n8n.cloud](https://allhomz.app.n8n.cloud) | Workflow execution |
| FunnelFast / GoHighLevel | [app.funnelfast.co](https://app.funnelfast.co) | CRM & webhook trigger |
| Meta Business Manager | [business.facebook.com](https://business.facebook.com) | CAPI pixel feedback |
| Google Account | [sheets.google.com](https://sheets.google.com) | HOT leads spreadsheet |
| OpenRouter | [openrouter.ai](https://openrouter.ai) | Claude AI API access |

---

## Step 1 — Import Workflow to n8n

### Option A — n8n UI (Recommended)

1. Open your n8n instance.
2. Go to **Workflows → Import from File**.
3. Select `egy-pioneers-workflow.json` from this directory.
4. Click **Import**.

### Option B — n8n REST API

```bash
curl -X POST "https://YOUR_N8N_INSTANCE/api/v1/workflows" \
  -H "X-N8N-API-KEY: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @egy-pioneers-workflow.json
```

Replace `YOUR_N8N_INSTANCE` and `YOUR_API_KEY` with your actual values.

---

## Step 2 — Create & Configure the Google Sheet

### Option A — Manual

1. Open [Google Sheets](https://sheets.google.com) and create a new spreadsheet.
2. Rename the default sheet tab to **HOT Leads**.
3. Add the following headers in row 1 (columns A–H):

   | A | B | C | D | E | F | G | H |
   |---|---|---|---|---|---|---|---|
   | التاريخ | الاسم | الرقم | الرسالة الأولى | التصنيف | نقاط الحرارة | الحالة | ملاحظات المبيعات |

4. Copy the spreadsheet ID from the URL bar and update it in the n8n Google Sheets node.

### Option B — Sheets API (CLI)

```bash
# Create spreadsheet
gws sheets spreadsheets create --json '{
  "properties": {"title": "Egy Pioneers - HOT Leads"},
  "sheets": [{"properties": {"title": "HOT Leads"}}]
}'

# Add Arabic headers
gws sheets spreadsheets values update --params '{
  "spreadsheetId": "SHEET_ID",
  "range": "HOT Leads!A1:H1",
  "valueInputOption": "RAW",
  "requestBody": {
    "values": [["التاريخ","الاسم","الرقم","الرسالة الأولى","التصنيف","نقاط الحرارة","الحالة","ملاحظات المبيعات"]]
  }
}'
```

### Share with n8n Service Account

If using a Google Service Account credential in n8n, share the spreadsheet with the service account email (Editor access).

---

## Step 3 — Generate Meta CAPI Access Token

> ⚠️ This token expires every **60 days**. Set a recurring calendar reminder.

1. Go to [Meta Events Manager](https://business.facebook.com/events_manager).
2. Select **Datasets** → click your pixel (ID: `1604627917208516`).
3. Click **Settings**.
4. Scroll to **Conversions API** → click **Generate access token**.
5. Copy the token (starts with `EAA…`).
6. In n8n, open **Node 9 (Meta CAPI)** and update the `access_token` query parameter in the credential or URL.

---

## Step 4 — Configure FunnelFast Webhook Trigger

1. In FunnelFast, go to **Automation → Workflows**.
2. Click **Create Workflow**.
3. Set the trigger to **Customer Replied**.
4. Add an action: **Webhook (HTTP Request)**.
5. Configure:
   - **URL:** `https://allhomz.app.n8n.cloud/webhook/egy-pioneers-lead`
   - **Method:** `POST`
   - **Content-Type:** `application/json`
   - **Body (mapped fields):**

     ```json
     {
       "contact_id":      "{{contact.id}}",
       "contact_name":    "{{contact.name}}",
       "phone":           "{{contact.phone}}",
       "message":         "{{message.body}}",
       "conversation_id": "{{conversation.id}}"
     }
     ```

6. Save and publish the workflow.

---

## Step 5 — Activate the n8n Workflow

### Option A — n8n UI

1. Open the imported workflow.
2. Toggle the **Active** switch in the top-right corner to ON.

### Option B — n8n REST API

```bash
curl -X POST "https://YOUR_N8N_INSTANCE/api/v1/workflows/WORKFLOW_ID/activate" \
  -H "X-N8N-API-KEY: YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

Replace `WORKFLOW_ID` with the value returned when you imported the workflow (e.g. `swr2aTOO9NZ5dvQE`).

---

## Step 6 — Test the Full Pipeline

Send a simulated HOT lead to the webhook:

```bash
curl -X POST "https://allhomz.app.n8n.cloud/webhook/egy-pioneers-lead" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id":      "REAL_CONTACT_ID",
    "contact_name":    "محمد أحمد",
    "phone":           "+201234567890",
    "message":         "عايز أسجل في الكورس بكام",
    "conversation_id": "REAL_CONV_ID"
  }'
```

**Expected response:**

```json
{ "status": "received" }
```

**Verify each output:**

| Check | Where to look |
|---|---|
| Claude classified as HOT | n8n execution log — Node 2 output |
| Sales note created | FunnelFast conversation thread |
| Tag added | FunnelFast contact → Tags |
| Pipeline card created | FunnelFast → Pipelines → New Lead |
| Row added to sheet | [Google Sheet](https://docs.google.com/spreadsheets/d/1v7uMgtMMVwQPBIE-9ZZcQ02PmeTx9c2NPAzQK3sPmx8/edit) |
| CAPI event received | Meta Events Manager → Test Events |

---

## Credentials Checklist

Before going live, confirm all credentials are set in n8n:

- [ ] **OpenRouter API Key** — used by Node 2 (Claude AI)
- [ ] **FunnelFast / GoHighLevel API Key** — used by Nodes 4, 5, 6
- [ ] **Google Sheets OAuth2 or Service Account** — used by Node 7
- [ ] **Meta CAPI Access Token** — used by Node 9 (refresh every 60 days)

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Webhook returns 404 | Workflow not active | Activate the workflow (Step 5) |
| Claude returns empty response | OpenRouter key invalid or quota exceeded | Check key in n8n credentials |
| Google Sheet not updating | Wrong Sheet ID or sharing permission | Re-share sheet with service account |
| Meta CAPI returns 400 | Token expired or missing `ph`/`fn` fields | Regenerate token (Step 3) |
| FunnelFast tags not applied | Wrong `contactId` mapping | Check FunnelFast webhook body mapping |
