# THINC v4.1 Creative QA Gate — Editorial Binding

Read this reference whenever the edit is destined for a paid Meta placement inside THINC
(Reels, Feed, Stories, ads for the Egyptian market). It binds the editing operating system
to the blocking gate defined in `docs/v4_1/THINC-v4.1-Creative-QA-Gate-v1.0.md`.
That document is the source of truth for thresholds; this file only says how an editor
must work so the gate can be answered.

## Where editing sits in the path

```
المرحلة 3 ← جاهزية التوريد والشحن
المرحلة 4 ← 🔒 Creative QA Gate — PRE-LAUNCH   (blocking; the edit is judged here)
المرحلة 5 ← اختبار العرض / Reality Validation
المرحلة 6 ← إطلاق الحملة بميزانية تجريبية
المرحلة 7 ← 🔍 Post-Launch Health Check (48h)  (the edit is re-judged here)
المرحلة 8 ← قرار Scale / Pause / Iterate
```

The gate is blocking. An edit that cannot answer every pre-launch item is not "ready with
notes" — it is not ready. Say so plainly instead of shipping a conditional pass.

## 1. Pre-launch: edit so the gate can be answered

Add a **Gate readiness** block to the output contract (between *Delivery/QC* and
*Exact next action*). Answer each row with `PASS`, `FAIL`, or `NOT_COLLECTED` — never
with an optimistic guess, and never by describing a moment you have not seen.

| Gate section | What the edit must make true | Evidence you cite |
|---|---|---|
| أ. Hook (first 3s) | offer or problem legible **muted**; no intro, logo, black frame, or fade-in on frame 1 | the actual first-3s frames, plus the 5-viewer muted test when it has been run |
| ب. Hold | a new idea, image, or piece of evidence at least every ~3s through second 15; one CTA in the last 3–5s | the time-coded paper edit |
| ج. Technical specs | aspect ratio, resolution, file size, on-screen text share, safe zones, duration | the exported file's real properties, reopened and checked |
| د. Expected quality ranking | ad matches the landing page; provenance-backed social proof; single CTA; original (not recycled) footage | the proof ladder level and the rights/usage status |

Rules that keep the answers honest:

- The muted hook test is a **viewer** test, not an editor's opinion. If it has not been run,
  the row is `NOT_COLLECTED` and the gate is not passed — it is pending.
- Technical rows are answered from the reopened export, not from the export dialog.
- "Original, non-recycled" is a claim about the asset's history. If you cannot establish it,
  mark it `NOT_COLLECTED` rather than assuming.
- A failed hook row sends the work back to reshooting the first 3 seconds, not to adding a
  transition, a zoom, or a louder track.

## 2. Post-launch: read the signal, then make the editorial fix

At 24h and 48h the gate reports a traffic-light row per signal. Each red signal maps to one
editorial cause and one first fix; do not respond to a stage-1 failure with a stage-3 fix.

| Failing signal | What it says about the edit | First editorial fix |
|---|---|---|
| Hook Rate red | the first 3 seconds do not earn the fourth | reshoot/re-select the opening from a different hook mechanism — anomaly, pain, identity, demonstration, comparison |
| Hook fine, Hold Rate red | seconds 4–15 stall: repetition or delayed proof | move the strongest credible proof earlier; cut duplicated beats; change information, not cut speed |
| Hook + Hold fine, CTR red | the story never bridges to one concrete action | rebuild the offer/CTA passage; one CTA, tied to the payoff |
| Hook + Hold + CTR fine, CPM red | not an editorial failure | hand back to audience/overlap work; do not re-cut a working creative to fix delivery cost |
| Frequency red | the creative is exhausted, not wrong | produce a new **angle** — changed tension, promise, proof, or objection; a new song or caption colour is not an angle |
| Quality ranking red | ad-to-landing-page mismatch or thin proof | re-align the claim, the shown product, and the page; raise the proof ladder level |

## 3. Thresholds are scoped, not universal

Every number in the gate — hook rate, hold rate, CTR, CPM, CPC, frequency — is a
**benchmark for the Egyptian market in EGP, revised quarterly from actual campaign data**.
Cite them as that. Do not restate them as general editing rules, do not carry them into a
brief for another market or platform, and do not invent a threshold the gate does not
define. This is the same discipline as the skill's standing rule against numeric recipes:
a number is usable when it names its source, its market, and its date.

## 4. Evidence vocabulary

Use the THINC status words where the gate expects them, alongside the skill's own labels:

- `COLLECTED` / `NOT_COLLECTED` / `STALE` — the state of a measurement.
- `HOLD_FOR_RESEARCH` — a decision cannot be made because evidence is missing or stale.
  Missing evidence never scores as zero, and never as a pass.
- **Observed / Inference / Hypothesis / Missing** — the state of anything you say about the
  footage itself.

An edit brief that mixes these correctly can be audited later. One that flattens them into
confident prose cannot.
