# -*- coding: utf-8 -*-
"""Karseell Daily Monitor - THINC v4 EV-based decision engine.

Pulls META + Shopify data, computes EV/CPA per THINC v4, and posts a
daily report to Slack. All tokens are read from environment variables
(GitHub secrets) and are never printed or logged.

Required for LIVE data: META_ACCESS_TOKEN, META_AD_ACCOUNT_ID,
META_CAMPAIGN_ID, SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN.
Required always: SLACK_BOT_TOKEN, SLACK_CHANNEL_ID.

If META/Shopify secrets are missing, posts an 'awaiting credentials'
status instead of crashing.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import urllib.error
import urllib.parse
import urllib.request

EGYPT_TZ_OFFSET = 3
BREAK_EVEN_EGP = 290.0
TARGET_CPA_EGP = 200.0
KILL_MULTIPLIER = 3.0
MIN_CONVERSIONS_FOR_JUDGMENT = 50
SLACK_API_URL = "https://slack.com/api/chat.postMessage"


def _env(name, default=""):
    return os.environ.get(name, default).strip()


def _http_get_json(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _today_egypt():
    now = dt.datetime.utcnow() + dt.timedelta(hours=EGYPT_TZ_OFFSET)
    return now


def fetch_meta_insights():
    """Return dict of META metrics, or None if creds missing/failed."""
    token = _env("META_ACCESS_TOKEN")
    account = _env("META_AD_ACCOUNT_ID")
    campaign = _env("META_CAMPAIGN_ID")
    if not token or not account:
        return None
    base = "https://graph.facebook.com/v19.0"
    node = campaign if campaign else account
    fields = "spend,impressions,reach,frequency,clicks,cpm,actions"
    params = urllib.parse.urlencode({
        "fields": fields,
        "date_preset": "today",
        "access_token": token,
    })
    url = base + "/" + node + "/insights?" + params
    try:
        data = _http_get_json(url)
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
        return None
    rows = data.get("data") or []
    if not rows:
        return {"spend": 0.0, "impressions": 0, "reach": 0,
                "frequency": 0.0, "clicks": 0, "cpm": 0.0, "purchases": 0}
    row = rows[0]
    purchases = 0
    for act in row.get("actions") or []:
        if act.get("action_type") == "purchase":
            purchases = int(float(act.get("value", 0)))
    return {
        "spend": float(row.get("spend", 0)),
        "impressions": int(float(row.get("impressions", 0))),
        "reach": int(float(row.get("reach", 0))),
        "frequency": float(row.get("frequency", 0)),
        "clicks": int(float(row.get("clicks", 0))),
        "cpm": float(row.get("cpm", 0)),
        "purchases": purchases,
    }


def fetch_shopify_orders():
    """Return count of paid+fulfilled orders today, or None if creds missing."""
    store = _env("SHOPIFY_STORE_URL")
    token = _env("SHOPIFY_ACCESS_TOKEN")
    if not store or not token:
        return None
    store = store.replace("https://", "").replace("http://", "").strip("/")
    today = _today_egypt().strftime("%Y-%m-%d")
    params = urllib.parse.urlencode({
        "status": "any",
        "financial_status": "paid",
        "created_at_min": today + "T00:00:00",
    })
    url = "https://" + store + "/admin/api/2024-01/orders.json?" + params
    headers = {"X-Shopify-Access-Token": token}
    try:
        data = _http_get_json(url, headers=headers)
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError):
        return None
    orders = data.get("orders") or []
    paid_fulfilled = 0
    for o in orders:
        if o.get("financial_status") == "paid" and o.get("fulfillment_status") == "fulfilled":
            paid_fulfilled += 1
    return paid_fulfilled


def thinc_v4_decision(spend, conversions):
    """Return (status_emoji, status_text, recommendation) per THINC v4."""
    if conversions <= 0:
        cpa = None
    else:
        cpa = spend / conversions
    kill_threshold = KILL_MULTIPLIER * TARGET_CPA_EGP
    if conversions < MIN_CONVERSIONS_FOR_JUDGMENT:
        rec = ("Learning Phase - "
               + str(conversions) + "/" + str(MIN_CONVERSIONS_FOR_JUDGMENT)
               + " conversions. Do not judge yet - this is learning capital.")
        if cpa is None:
            return (":large_yellow_circle:", "Learning (0 conv)", rec)
        return (":large_yellow_circle:", "Learning", rec)
    if cpa is not None and cpa > kill_threshold:
        return (":red_circle:", "KILL",
                "CPA " + str(round(cpa)) + " EGP > kill threshold "
                + str(round(kill_threshold)) + " EGP. Stop the campaign.")
    if cpa is not None and cpa <= BREAK_EVEN_EGP:
        return (":large_green_circle:", "Profitable",
                "CPA " + str(round(cpa)) + " EGP below break-even "
                + str(round(BREAK_EVEN_EGP)) + " EGP. Scale +15-20%.")
    return (":red_circle:", "Above break-even",
            "CPA above break-even. Hold and optimize before scaling.")


def build_report(meta, shopify_orders):
    """Build the Slack report text. Handles missing creds gracefully."""
    date_str = _today_egypt().strftime("%Y-%m-%d %H:%M")
    header = ":bar_chart: *Karseell Daily Monitor - " + date_str + " (Cairo)*"
    sep = "---------------------------------"
    if meta is None:
        return (header + "\n" + sep
                + "\n:warning: *Awaiting credentials* - META secrets not set."
                + "\nAdd META_ACCESS_TOKEN + META_AD_ACCOUNT_ID (and optional "
                + "META_CAMPAIGN_ID) in repo Actions secrets to enable live data."
                + "\nThe pipeline is live and will report real numbers once "
                + "credentials are added.")
    spend = meta["spend"]
    if shopify_orders is not None:
        conversions = shopify_orders
        conv_label = "Shopify Paid+Fulfilled"
    else:
        conversions = meta["purchases"]
        conv_label = "Meta Purchases"
    emoji, status, rec = thinc_v4_decision(spend, conversions)
    if conversions > 0:
        cpa_str = str(round(spend / conversions)) + " EGP"
    else:
        cpa_str = "n/a (0 conv)"
    lines = [
        header,
        sep,
        ":moneybag: Spend: " + str(round(spend, 2)) + " EGP | "
        + ":eye: Impressions: " + str(meta["impressions"])
        + " | :loudspeaker: Reach: " + str(meta["reach"])
        + " (Freq " + str(round(meta["frequency"], 2)) + ")",
        ":computer_mouse: Link Clicks: " + str(meta["clicks"])
        + " | :chart_with_upwards_trend: CPM: " + str(round(meta["cpm"], 2)) + " EGP",
        ":shopping_trolley: " + conv_label + ": " + str(conversions),
        ":dart: CPA: " + cpa_str + " | :scales: Break-even: "
        + str(round(BREAK_EVEN_EGP)) + " EGP | Status: " + emoji + " " + status,
        sep,
        ":pushpin: *Recommendation:* " + rec,
    ]
    if shopify_orders is None and meta["purchases"] == 0:
        lines.append(":warning: COD note: Meta may show 0 Purchase while "
                     "Shopify has confirmed sales - expected in COD.")
    return "\n".join(lines)


def post_to_slack(text):
    """Post message to Slack. Token read from env, never logged."""
    token = _env("SLACK_BOT_TOKEN")
    channel = _env("SLACK_CHANNEL_ID")
    if not token or not channel:
        print("ERROR: SLACK_BOT_TOKEN or SLACK_CHANNEL_ID missing.")
        return False
    payload = json.dumps({"channel": channel, "text": text}).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json; charset=utf-8",
    }
    req = urllib.request.Request(SLACK_API_URL, data=payload,
                                 headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as exc:
        print("ERROR: Slack request failed: " + type(exc).__name__)
        return False
    if not result.get("ok"):
        print("ERROR: Slack API error: " + str(result.get("error")))
        return False
    print("Report posted to Slack successfully.")
    return True


def main():
    meta = fetch_meta_insights()
    shopify_orders = fetch_shopify_orders()
    report = build_report(meta, shopify_orders)
    ok = post_to_slack(report)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
