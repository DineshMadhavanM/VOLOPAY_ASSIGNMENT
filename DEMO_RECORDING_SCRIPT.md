# 3-Minute Narrated Screen Recording Script

**Assessment**: Revenue Intelligence Inbox (SpendNest)  
**Total Target Duration**: 180 seconds (3:00)  
**Format**: Continuous single-take screen capture with spoken voice narration.

---

### Timeline Overview
- `00:00 - 00:40` (40s): Executive Overview, Manager Problem & Headline Metrics
- `00:40 - 01:25` (45s): Useful Manager Workflow & The Difficult Routing Decision (M07 & M02)
- `01:25 - 02:35` (70s): The 5-Step Replay & Idempotence Test (Duplicate rejection & Preserved Override)
- `02:35 - 03:00` (25s): Export Manifest, Deliberately Rejected Decision & Conclusion

---

### [00:00 – 00:40] Executive Overview & Metric Definitions

**Visual Action**:
1. Open the application at `http://localhost:3000` in your browser.
2. Slowly move cursor over the top navigation and the 5 metric cards.
3. Hover over the tooltip icon on **"Transcript Coverage"** and **"Selected Records"**.

**Spoken Narration (Speak naturally and clearly)**:
> *"Hello, I'm presenting the Revenue Intelligence Inbox for SpendNest, built for a sales manager who needs to quickly review interaction logs, detect exceptions, and make operational decisions.*
>
> *Looking at our dashboard for Friday, 21 August 2026, we've ingested 44 total interactions: 30 calls and 14 meetings. Notice that our usable transcript coverage is 17 of 44 records, or 38.6%. We don't inflate this number: 20 background calls and 6 meetings have no audio supplied, so we clearly label them as unreviewed rather than fabricating fake summaries.*
>
> *We also carefully distinguish Call Reps from Meeting Organizers—an organizer like team08 is not automatically an AE or an attendee, and a telephony 'connected' flag is not proof of a conversation."*

---

### [00:40 – 01:25] Useful Manager Workflow & Difficult Routing Decision

**Visual Action**:
1. Click on the **"Manager Brief"** tab to show the daily synthesis for 21 August 2026.
2. Point out the **Critical Metadata Warning for C06** (Meera vs. Ravi).
3. Switch back to the **"Inbox"** tab.
4. Click on row **"M02"** to open the Deep Inspection Drawer. Point to the Turn 1 quote showing LedgerBridge is a vendor evaluation. Close the drawer.
5. Highlight row **"M07" (Willowfield Trust)** in the inbox table.

**Spoken Narration**:
> *"Here in the Manager Brief, the inbox surfaces high-priority alerts. For example, in Call C06, the telephony metadata lists Meera as the rep, but in the actual call audio, the rep introduces himself as Ravi. Our system flags this discrepancy immediately to avoid rep commission errors.*
>
> *Next, let's look at a critical routing decision: Meeting M02 with LedgerBridge. Upstream CRM systems misclassified this as a sales meeting, but when we inspect Turn 1, SpendNest's strategy team was actually evaluating LedgerBridge to buy European e-invoicing software—so our inbox routes it to Internal Vendor Evaluation.*
>
> *Now, notice our difficult routing case: Meeting M07 with Willowfield Trust. In our initial batch, M07 has no transcript and appears to be a routine check-in. Let's see what happens during our data replay."*

---

### [01:25 – 02:35] The 5-Step Replay & Idempotence Test

**Visual Action**:
1. Scroll to the top **Replay Simulator Toolbar**.
2. Point cursor to the record count: `44 Records Ingested`.
3. Click button **"2. Test Idempotence (Repeat)"**. Watch the log message: `0 duplicates added, 44 duplicates safely rejected`.
4. Click button **"3. Apply Route Override (M07)"**. Point to the yellow **"MANUAL OVERRIDE"** badge appearing on M07.
5. Click button **"4. Ingest Late Update (Rev 2)"**. Watch transcript coverage rise from `17/44` to `18/44`, and point to the cyan **"REV 2"** badge on M07.
6. Click on M07 to open the drawer: show the 27 turns where Customer A screen-shares payment bugs.
7. Close the drawer and click button **"5. Replay & Preserve Override"**. Show that the lower revision was ignored and the manual override survived.

**Spoken Narration**:
> *"Now let's demonstrate our 5-step data contract test.*
>
> *First, watch our record count: 44. I now click 'Test Idempotence' to re-import the initial batch in shuffled order. The count stays strictly 44—zero duplicates created, and 44 duplicates rejected.*
>
> *Next, as a manager, I make a manual route correction on M07: I change its route to 'Customer Success / Bug Escalation' and save it. It is now tagged with a persistent Manual Override badge.*
>
> *Now, I import Delivery Batch 2 containing M07's revision 2. Watch our transcript coverage: it jumps from 17 to 18, and M07 gains 27 turns. Opening the inspection drawer, we see Customer A screen-sharing critical software defects where event payment descriptions revert upon saving.*
>
> *Most importantly, my manual route override survived completely! If I re-import Revision 1 or refresh the browser, the lower revision is safely ignored and my judgment remains intact."*

---

### [02:35 – 03:00] Export Manifest, Rejected Decision & Conclusion

**Visual Action**:
1. Click on the **"Export Center"** tab.
2. Point cursor to the manifest preview table showing `manifest.json` and `manifest.csv`.
3. Click **"Download Complete Export Archive (.zip)"** to show real-time ZIP generation.
4. Conclude on the clean UI.

**Spoken Narration**:
> *"Finally, in our Export Center, every interaction is exported into organized markdown files along with a machine-readable manifest in both JSON and CSV.*
>
> *One decision we considered and deliberately rejected was having an AI guess pipeline deal values from company names. We rejected this because hallucinating revenue numbers damages executive trust. Instead, we provide verified source evidence for every recommendation.*
>
> *Thank you for reviewing the SpendNest Revenue Intelligence Inbox."*
