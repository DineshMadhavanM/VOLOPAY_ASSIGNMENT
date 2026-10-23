# SpendNest Revenue Intelligence Inbox — 5 Slide Presentation

---

## Slide 1: The Manager Problem Solved & 3 Key Findings
**Header**: Problem Definition & Ground-Truth Evidence  
**Context**: Reviewing 44 interaction records (30 calls, 14 meetings) from Friday, 21 August 2026 (Asia/Kolkata).

### The Manager Problem
A sales manager receives fragmented, contradictory interaction logs from telephony and calendar systems. Upstream CRM labels frequently classify vendor meetings as sales pipeline, misattribute rep identities, or assume empty calendar invites were fruitful meetings.

### Three Critical Findings Linked to Source Evidence
1. **Finding 1: Vendor Procurement Mistagged as Sales Pipeline (Meeting M02 - LedgerBridge)**
   - *Source Passage*: M02, Turn 1: *"I work on strategy and partnerships at SpendNest. We serve businesses with cards and accounts payable, and we are developing accounts receivable. We want to understand whether LedgerBridge can give us compliant invoicing coverage in Europe..."*
   - *Product Decision*: SpendNest is the prospective **buyer/client**, not the vendor! Upstream CRM tagged this as sales pipeline. Our system routes it to `Vendor Evaluation / Internal`, protecting quota and forecasting accuracy.
2. **Finding 2: Telephony User Identity Mismatch (Call C06)**
   - *Source Passage*: Call C06 opening verbatim quote: *"Good evening, Mr Nikhil... Ravi here. I'll say at the start that this is a cold call."*
   - *Product Decision*: Metadata specifies rep as `Meera`, but calling voice is Ravi. Flagged as `Rep Coaching / Data Discrepancy` to prevent rep commission and performance misallocation.
3. **Finding 3: Product Capability Disconnect (Meeting M01 - Harborpath Advisory)**
   - *Source Passage*: M01, Turn 1 & 2: Partner seeks remote bank account opening for overseas clients. SpendNest team member clarifies: *"we provide virtual business accounts for operational spend, not licensed retail bank accounts..."*
   - *Product Decision*: Routed to `Partnership / Channel Advisory` with an explicit requirement to deliver compliance positioning documentation before launching channel partner referrals.

---

## Slide 2: Interface Choices & Deliberate Omissions
**Header**: UX Design Philosophy & System Boundaries

### Key Interface Choices
- **Built-In Replay Simulator Toolbar**: Features 5 dedicated buttons to verify idempotent repeat imports, manual route overrides, and late-arriving update batches directly in the UI.
- **Batch JSON Contract Verification**: Evaluator-friendly JSON upload dropzone to verify arbitrary incoming batches against DATA_CONTRACT.md schema and idempotency rules.
- **Strict Mathematical Denominators**: We separate `Call Reps` (SDRs/AEs dialing) from `Meeting Organisers` (calendar coordinators who may not be attendees or reps) and measure transcript coverage against all 44 selected records.
- **Deep Evidence Drawer**: Allows clicking any interaction to inspect formatted turns, elapsed timecodes, verbatim quotes, honest limitations, and stated action owners.

### Deliberate Omissions
- **Zero Hallucinated Summaries**: For the 26 records with null transcripts or empty turns, we *deliberately declined* to invent synthetic summaries. They are transparently logged as `Intake / No Audio Supplied`.
- **No Standalone Date Filter**: All supplied records occur on 21 August 2026 (Asia/Kolkata). Providing a date picker provides zero analytical value and was omitted.

---

## Slide 3: Routing Taxonomy & The Difficult Case (M07)
**Header**: Routing Architecture & Case Study

### Routing Taxonomy (6 Action-Oriented Destinations)
1. **Deal Next Steps / Pipeline**: Active commercial evaluations (M03 Asterloom, C03 Milan API, C08 Raghav referral).
2. **Customer Success / Escalations**: Urgent customer bug escalations & migrations (M07 Willowfield Trust, M04 Cedarwave).
3. **Partnerships / Channel Advisory**: Referral partners incorporating overseas businesses (C07 Willowbank Advisory, M01 Harborpath).
4. **Vendor Evaluation / Internal**: Procurement reviews (M02 LedgerBridge) & internal training (M10 Billing walkthrough).
5. **Low Priority / Voicemail / Gatekeeper**: Gatekeeper transfers and voicemails (C01, C02, C04, C06, C10).
6. **Intake / Unreviewed**: Short dials & empty meetings awaiting audio (B01-B20, M05, M08, M11-M14).

### The Difficult Routing Decision: Willowfield Trust (M07)
- In Delivery Batch 1, M07 arrived with null turns and was provisionally labeled as a routine check-in.
- In Delivery Batch 2 (Rev 2), 27 turns were supplied showing Customer A screen-sharing critical software defects (payment description edits reverting upon save; recreate payment file upload failing).
- Routing was immediately shifted from *Routine Check-in* to *Customer Success / Bug Escalation*. Under our data contract, a manager override survives batch replays and browser reloads.

---

## Slide 4: Verification of Key Numbers & Analytical Rigor
**Header**: Audit Trail & Replay Verification

### Mathematical Proof Against `01_initial.json` and `02_update.json`
| Metric | Delivery Batch 1 (Rev 1) | Delivery Batch 2 (Rev 2) | Verification Methodology |
| :--- | :--- | :--- | :--- |
| **Unique Source Records** | 44 records | 44 records (strict) | Keyed strictly by `(source_type, source_id)`. |
| **Transcript Coverage** | 17 / 44 (38.6%) | 18 / 44 (40.9%) | M07 arrives in Rev 2 with 27 turns, raising coverage from 17 to 18. |
| **Calls vs. Meetings** | 30 Calls, 14 Meetings | 30 Calls, 14 Meetings | Partitioned strictly by `source_type`. |
| **Source Connection Rate** | 9 / 30 calls (30.0%) | 9 / 30 calls (30.0%) | Calls with `is_connected: true` / 30 total calls. Exactly 8 had prospect dialogue. |

### Repeat Import Idempotence Test
Ingesting Batch 1 a second time with shuffled array order results in exactly 44 records, 0 duplicate additions, and 44 rejected duplicates.

---

## Slide 5: Trade-offs, Rejected Decision & Next Steps
**Header**: Engineering Ethics & AI Disclosure

### The Deliberately Rejected Decision: Auto-Estimating Deal Pipeline ARR
- **Alternative Considered**: Using an LLM to hallucinate contract values based on prospect employee count (e.g. estimating Asterloom at $45,000 ARR).
- **Why Rejected**: The prompt strictly prohibits inventing pipeline value or deal outcomes. Speculative revenue figures destroy executive trust during audits.
- **Accepted Trade-off**: We report qualitative commercial intent and verbatim financial statements (e.g. Asterloom's INR 26–39 lakh monthly vendor spend) without guessing ARR.

### AI Implementation & Scope Disclosure
- **Pre-generated vs. Dynamic**: Conversation analyses and evidence citations were prepared beforehand. Batch ingestion, revision deduplication, manual override persistence, and ZIP manifest generation run completely dynamically client-side.
- **Approximate Time Spent**: ~7 hours total.
- **Known Limitations & Future Scope**: Cross-call speaker identity is not unified upstream. Future release will integrate live webhooks for automated recording synchronization.
