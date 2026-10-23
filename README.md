# SpendNest — Revenue Intelligence Inbox

A comprehensive, executive sales management web application built for the **Volopay Interview Process**.

SpendNest Revenue Intelligence Inbox ingests, normalizes, routes, and audits 44 call and meeting interaction records from Friday, 21 August 2026 (Asia/Kolkata). It enforces the strict data contract of `DATA_CONTRACT.md`, supports idempotent batch replays, preserves manager routing overrides across late-arriving transcripts, and produces structured exports with machine-readable manifests (`manifest.json` and `manifest.csv`).

---

## 1. Quick Startup Instructions

The application is completely self-contained and requires **zero external dependencies**.

### Option A: Local Node Server (Recommended)
```bash
# Navigate to the application directory
cd revenue-inbox

# Start the dev server (starts on http://localhost:3000)
npm run dev
# or
node server.js
```
Open your browser at **`http://localhost:3000`**.

### Option B: Direct Offline Browser Open
Simply double-click `revenue-inbox/index.html` in your file explorer to open it directly in Google Chrome, Microsoft Edge, or Safari. All styles, icons, datasets, and the JSZip bundling engine run completely offline!

### Option C: Live Deployed Application
The application is live and hosted on Render:
**👉 [https://volopay-assignment-inqe.onrender.com](https://volopay-assignment-inqe.onrender.com)**

---

## 2. Replay Test Demonstration (Contract Verification)

Under `DATA_CONTRACT.md`, the inbox implements an interactive top toolbar with 5 dedicated replay buttons:

| Step | Action Button | Verified Behavior |
| :--- | :--- | :--- |
| **Step 1** | `1. Initial Import (Rev 1)` | Ingests `01_initial.json`. Ingests 44 unique records (30 calls, 14 meetings). Exactly 17 have usable transcripts. |
| **Step 2** | `2. Test Idempotence (Repeat)` | Re-ingests the initial batch with shuffled record order. **Strictly idempotent**: record count stays exactly 44; 44 duplicate records safely rejected; zero metric inflation. |
| **Step 3** | `3. Apply Route Override (M07)` | Simulates manager human judgment: overrides `M07`'s route to `Customer Success / Bug Escalation`. Stored in persistent `localStorage` with a visible yellow `OVERRIDE` badge. |
| **Step 4** | `4. Ingest Late Update (Rev 2)` | Ingests `02_update.json`. Meeting `M07` is updated to Revision 2 with 27 turns. Total unique records remains 44. Usable transcript coverage increases from 17 to 18 (40.9%). |
| **Step 5** | `5. Replay & Preserve Override` | Re-imports `01_initial.json` (Rev 1). Because `M07` is already at Rev 2, Rev 1 is safely ignored. **The manager's manual route override survives intact**. |

*Note: You can also click **"Upload JSON"** to upload any arbitrary test batch JSON file.*

---

## 3. Metric Definitions & Mathematical Denominators

All headline metrics follow the strict guidelines of `DATA_DICTIONARY.md`:

1. **Selected Interactions (Total: 44)**:
   - *Denominator*: Unique `(source_type, source_id)` pairs occurring on the local date of 21 August 2026 in Asia/Kolkata.
   - *Split*: 30 Calls (10 with audio transcript, 20 short background dials) and 14 Meetings (7 with initial transcripts, 1 arriving late in Rev 2, 6 unrecorded or cancelled).
2. **Transcript Coverage (17/44 -> 18/44)**:
   - *Formula*: `Records with non-blank transcript or turns > 0 / Total selected records (44)`.
   - *Initial Batch*: 17 / 44 (38.6%).
   - *Post-Update Batch*: 18 / 44 (40.9%).
3. **Connection Rate vs. Substantive Conversation**:
   - *Source-Reported Connection Rate*: 9 / 30 calls (30.0%) had `is_connected: true`.
   - *Substantive Dialogue Rate*: Exactly 8 calls contained multi-turn prospect conversations (C01, C03, C05, C06, C07, C08, C09, C10), while C02 and C04 terminated in gatekeeper voicemails.
4. **Call Reps vs. Meeting Organisers**:
   - Call records attribute dial activity to caller reps (`Arun`, `Meera`, `Leela`, `Dev`, `Kiran`).
   - Meeting records attribute calendar creation to `organizer_email` (`team06`, `team07`, etc.). An organizer is **not** assumed to be an attendee or AE.

---

## 4. The Three Key Findings (Linked to Source Evidence)

1. **Finding 1: Vendor Procurement Mistagged as Sales Opportunity (Meeting M02)**
   - *Source Reference*: M02, Turn 1: *"I work on strategy and partnerships at SpendNest. We serve businesses with cards and accounts payable, and we are developing accounts receivable. We want to understand whether LedgerBridge can give us compliant invoicing coverage in Europe..."*
   - *Product Impact*: Calendar title was `LedgerBridge / SpendNest discussion`. Upstream CRM mistagged it as an inbound sales lead. Our system routes it to `Vendor Evaluation / Internal`, excluding it from the sales pipeline and rep quota.
2. **Finding 2: Telephony User Identity Mismatch (Call C06)**
   - *Source Reference*: Call C06 verbatim opening quote: *"Good evening, Mr Nikhil... Ravi here. I'll say at the start that this is a cold call."*
   - *Product Impact*: Payload metadata specifies `rep_name: "Meera"`, but spoken audio is Ravi. Flagged as `Rep Coaching / Telephony Discrepancy` to prevent rep commission misallocation.
3. **Finding 3: Partner Capability Disconnect (Meeting M01 - Harborpath Advisory)**
   - *Source Reference*: M01, Turn 1 & Turn 2: Partner asks about remote bank accounts for overseas clients. SpendNest team member clarifies they offer operational virtual spend accounts and cards, not licensed retail deposit accounts.
   - *Product Impact*: Routed to `Partnership / Channel Advisory` with an explicit flag to deliver compliance positioning documentation before onboarding partner clients.

---

## 5. The Difficult Routing Decision: Willowfield Trust (M07)

- **Initial State**: In Delivery Batch 1, M07 arrived with null turns and `unavailable_reason: Transcript withheld in initial delivery batch`. It was provisionally routed to `Intake / Pending Transcript`.
- **Update State**: Delivery Batch 2 provided Revision 2 with 27 turns. During screen-share, Customer A demonstrated two severe bugs:
  1. *Turn 2 & 3*: Editing event payment descriptions reverts upon clicking "Save changes".
  2. *Turn 8*: Document upload fails when recreating a payment.
- **Decision**: Shifted immediately from routine check-in to `Customer Success / Bug Escalation`. A manager override applied at this step survives batch replays and browser refreshes.

---

## 6. The Deliberately Rejected Decision

- **Proposal**: Using an LLM to auto-infer deal sizes and ARR pipeline figures based on prospect company descriptions (e.g., guessing Asterloom is a $50k deal).
- **Why Rejected**: The prompt and data dictionary explicitly state: *"Do not invent pipeline value, deal outcomes or account links that the data does not establish."* Guessing financial figures creates phantom forecasts that deceive leadership.
- **Accepted Trade-off**: We display qualitative opportunity intent and verbatim financial evidence (e.g. Asterloom's INR 26–39 lakh monthly vendor volume) without inventing speculative ARR numbers.

---

## 7. Export Structure & Manifest

Exports are pre-generated in the repository under `exports/` and can also be downloaded dynamically as a ZIP archive from the in-app **Export Center**:

```
exports/
├── manifest.json                  # Machine-readable JSON manifest
├── manifest.csv                   # Machine-readable CSV manifest
├── daily_brief_2026-08-21.md      # Executive sales manager brief
├── deals/                         # 5 active pipeline opportunities (M03, C03, C05, C08, C09)
├── customer_success/              # 3 retention & escalations (M07, M04, M09)
├── partnerships/                  # 2 channel partnerships (M01, C07)
├── internal_vendor/               # 3 vendor / training records (M02, M06, M10)
├── low_priority/                  # 5 gatekeeper / voicemails (C01, C02, C04, C06, C10)
└── intake_unreviewed/             # 26 records with no audio supplied (B01-B20, M05, M08, M11-M14)
```

---

## 8. Implementation Details & Time Spent

- **Runtime vs. Pre-generated**: Analysis evidence and structured citations were pre-generated and mapped deterministically to avoid runtime hallucination. Ingestion, revision handling, deduplication, override persistence, and ZIP packaging run dynamically in the client browser.
- **Time Spent**: ~7 hours total (2.5h dataset parsing & contract modeling, 2.5h web application & design system, 2h documentation, manifest generation, and slide deck preparation).
- **Known Limitations**: Cross-call speaker identity is not unified upstream. Future work would include real-time telephony webhook synchronization.

---

## 9. Submission & Evaluation Compliance Checklist

This project strictly adheres to all instructions in `candidate/ASSIGNMENT.md`, `DATA_CONTRACT.md`, and `SUBMISSION_CHECKLIST.md`:

| Requirement | Implementation in SpendNest | Verified |
| :--- | :--- | :---: |
| **Working Local App** | Runs instantly via `node server.js` or direct offline browser open (`index.html`) on `http://localhost:3000`. | ✅ |
| **Zero Credentials / No API Keys** | Self-contained client-side application. No private credentials, authentication barriers, or external API keys needed. | ✅ |
| **Idempotency Replay (Step 2)** | Replaying initial batch adds 0 duplicate records; rejected records count = 44. | ✅ |
| **Preserved Manual Override (Step 3 & 5)** | Changing route (e.g., M07 to Bug Escalation) survives late update batches (Rev 2) and browser reloads via `localStorage`. | ✅ |
| **Late Update Handling (Step 4)** | Meeting M07 late transcript updates in place; usable coverage jumps from 17/44 to 18/44 (40.9%) without creating duplicate records. | ✅ |
| **Denominators & No Fake Summaries** | Strict mathematical denominators for all metrics; 26 records without audio are transparently categorized as `Intake / No Audio Supplied`. | ✅ |
| **Five Slides Presentation** | Available as `slides/presentation.pptx` (generated via `python generate_pptx.py`) and readable in `slides/slides.html` / `slides/SLIDES.md`. | ✅ |
| **Export Manifest & ZIP** | Export Center packages `manifest.json`, `manifest.csv`, `processed_interactions.json`, `executive_brief.md`, and categorized folders into a downloadable ZIP archive. | ✅ |
