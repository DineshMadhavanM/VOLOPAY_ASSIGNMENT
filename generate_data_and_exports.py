import json
import os
import csv
from datetime import datetime

# Define base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'candidate', 'data')
EXPORT_DIR = os.path.join(BASE_DIR, 'exports')
APP_DATA_DIR = os.path.join(BASE_DIR, 'revenue-inbox', 'src', 'data')
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'revenue-inbox', 'data'), exist_ok=True)

# 1. Load initial and update data
with open(os.path.join(DATA_DIR, '01_initial.json'), 'r', encoding='utf-8') as f:
    initial_batch = json.load(f)

with open(os.path.join(DATA_DIR, '02_update.json'), 'r', encoding='utf-8') as f:
    update_batch = json.load(f)

print(f"Loaded initial batch: {len(initial_batch['records'])} records")
print(f"Loaded update batch: {len(update_batch['records'])} records")

# Detailed analysis definitions for all 18 conversations + intake records
CONVERSATION_ANALYSIS = {
    "C01": {
        "title": "Harborlight Advisory Outreach",
        "company": "Harborlight Advisory",
        "contact": "Pranav",
        "rep": "Arun",
        "route": "Low Priority / Rejected",
        "secondary_routes": ["Outbound Hygiene"],
        "summary": "Cold outbound outreach to outsourced finance firm. Contact was irritated by cold outreach, asked how details were obtained, and stated their finance operations are already fully automated.",
        "why_it_matters": "Clear rejection of cold outreach; further unprompted contact risks negative brand impression.",
        "evidence": "Arun: 'We work with outsourced finance leadership firms and—no, I asked why you have called me... Our processes are already very automated. We have a fairly advanced setup, so I don\\'t think this is something we need.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C01 verbatim quote",
        "limitations": "Does not prove whether other decision-makers exist at the firm or what specific ERP they use.",
        "next_steps": "Remove Pranav and Harborlight Advisory from active outbound calling sequence.",
        "owner": "Arun",
        "deal_intent": "None",
        "category": "low_priority",
        "folder": "low_priority"
    },
    "C02": {
        "title": "Fernhaven Group Reception Call",
        "company": "Fernhaven Group",
        "contact": "Kavya (Receptionist) / Leela (Target)",
        "rep": "Arun",
        "route": "Low Priority / Voicemail",
        "secondary_routes": ["Gatekeeper"],
        "summary": "Outbound call to Fernhaven Group. Receptionist Kavya advised that Leela is out of office and routed the caller to her voicemail.",
        "why_it_matters": "No substantive contact made; telephone attempt resulted in voicemail routing.",
        "evidence": "Kavya: 'It looks as though she isn\\'t in the office today. Would you like to leave a message with me, or would you prefer her voicemail? Her voicemail would be fine, thank you.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C02 verbatim quote",
        "limitations": "Does not establish whether Leela is interested in spend software or will return the message.",
        "next_steps": "Log voicemail and follow up via email with introductory collateral early next week.",
        "owner": "Arun",
        "deal_intent": "Unknown",
        "category": "low_priority",
        "folder": "low_priority"
    },
    "C03": {
        "title": "Developer API Access Follow-Up",
        "company": "Milan's Development Team",
        "contact": "Milan",
        "rep": "Kiran",
        "route": "Deal Next Steps / Pipeline",
        "secondary_routes": ["Pricing Negotiation"],
        "summary": "Follow-up discussion regarding developer API access and event notifications. Milan was travelling outdoors with poor reception; indicated pricing sensitivity and asked for an email follow-up before speaking Monday/Tuesday.",
        "why_it_matters": "Active technical evaluation delayed by pricing concerns. Clear opportunity to re-engage with structured packaging.",
        "evidence": "Milan: 'We did ask about some developer functionality, but it isn\\'t essential enough for us to spend much on it... Could we do this by email? Or call on Monday... Something like \"Developer access and event notifications — follow-up\".'",
        "evidence_type": "quote",
        "evidence_ref": "Call C03 verbatim quote",
        "limitations": "Audio quality was degraded; exact team budget was not stated during this call.",
        "next_steps": "Send email with requested subject line containing developer tier options; schedule follow-up call for Monday.",
        "owner": "Kiran",
        "deal_intent": "Moderate - Price Sensitive",
        "category": "deals",
        "folder": "deals"
    },
    "C04": {
        "title": "Lanternpath Media Voicemail",
        "company": "Lanternpath Media",
        "contact": "Ritesh",
        "rep": "Arun",
        "route": "Low Priority / Voicemail",
        "secondary_routes": ["Process Hygiene"],
        "summary": "Arun left a voicemail for Ritesh following up on an expense platform proposal after initial materials were sent to an incorrect email address.",
        "why_it_matters": "Highlights operational delay due to email bounce; deal momentum stalled pending prospect contact.",
        "evidence": "Arun: 'My understanding is that our information first went to the wrong email address. We subsequently used the corrected address you gave us, and I hope you have now had a chance to see it.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C04 verbatim quote",
        "limitations": "Prospect did not answer; cannot verify if Ritesh received the resent proposal or intends to evaluate.",
        "next_steps": "Check email tracking metrics for the resent proposal; re-attempt phone contact if unopened in 48 hours.",
        "owner": "Arun",
        "deal_intent": "Pending Prospect Contact",
        "category": "low_priority",
        "folder": "low_priority"
    },
    "C05": {
        "title": "Multi-Store Retail StoreHarbor Inquiry",
        "company": "Retail Group (contact05)",
        "contact": "contact05",
        "rep": "Meera",
        "route": "Deal Next Steps / Nurture",
        "secondary_routes": ["Competitor Displacement"],
        "summary": "Introductory sales pitch for store expense cards and vendor management. Contact reported existing usage of StoreHarbor and other tools, but agreed to receive a presentation at contact05@example.com.",
        "why_it_matters": "StoreHarbor incumbent identified. Prospect is open to comparative collateral for future consideration.",
        "evidence": "Prospect: 'There are several. One is StoreHarbor, and we use others too. What I suggest is that you send me your presentation. If we ever decide to change the providers we already have, we could consider it then.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C05 verbatim quote",
        "limitations": "No active RFP or timeline; displacement probability is long-term.",
        "next_steps": "Send competitive battlecard highlighting SpendNest advantages over StoreHarbor to contact05@example.com.",
        "owner": "Meera",
        "deal_intent": "Low - Nurture",
        "category": "deals",
        "folder": "deals"
    },
    "C06": {
        "title": "Retail Chain Discovery & Rep Identity Mismatch",
        "company": "Retail Chain (120+ stores)",
        "contact": "Mr. Nikhil",
        "rep": "Meera (Metadata) / Ravi (Spoken)",
        "route": "Low Priority / Competitor Installed",
        "secondary_routes": ["Rep Coaching / Data Discrepancy"],
        "summary": "Cold outbound call to a 120-store retail business. Nikhil explained they have extensive existing automation and full head-office visibility. CRITICAL: Rep metadata lists Meera, but caller introduces himself as 'Ravi'.",
        "why_it_matters": "1) Prospect has mature in-house/integrated ERP tooling. 2) Operational CRM mismatch: rep metadata does not match the actual speaker.",
        "evidence": "Caller: 'Good evening, Mr Nikhil... Ravi here. I\\'ll say at the start that this is a cold call.' Nikhil: 'We have quite a lot of automation, with a mixed model where needed... Head office manages it, and we have full visibility.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C06 verbatim quote",
        "limitations": "Exact software platforms used at head office were not disclosed.",
        "next_steps": "1) Audit VOIP/CRM user seat mapping for Ravi vs Meera. 2) Log 120-store account as automated in CRM.",
        "owner": "Ravi / Meera",
        "deal_intent": "None",
        "category": "low_priority",
        "folder": "low_priority"
    },
    "C07": {
        "title": "Willowbank Advisory Overseas Incorporation Partnership",
        "company": "Willowbank Advisory",
        "contact": "Mr. Aditya",
        "rep": "Dev",
        "route": "Partnership / Channel Advisory",
        "secondary_routes": ["Virtual Business Accounts"],
        "summary": "Partnership inquiry with Willowbank Advisory regarding virtual business accounts for newly incorporated overseas companies. Aditya confirmed they refer clients to digital providers and asked for a proposal via messaging app.",
        "why_it_matters": "High-leverage channel partnership potential for recurring overseas client incorporation referrals.",
        "evidence": "Aditya: 'Yes, that is something we normally do... could you message me on our chat app and send whatever proposal you have?... Once you\\'ve received them, could I call on Monday... Yes, that\\'s fine.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C07 verbatim quote",
        "limitations": "Referral commission model and compliance restrictions are not yet defined.",
        "next_steps": "Dev to send partner one-pager via messaging app; calendar discovery call for Monday.",
        "owner": "Dev",
        "deal_intent": "Channel Partnership",
        "category": "partnerships",
        "folder": "partnerships"
    },
    "C08": {
        "title": "Fulfillment Operations Lead Referral",
        "company": "Fulfillment Operations Co",
        "contact": "Mr. Raghav",
        "rep": "Meera",
        "route": "Deal Next Steps / Pipeline",
        "secondary_routes": ["Stakeholder Referral"],
        "summary": "Cold call regarding branch expenses and payables. Raghav directed Meera to the colleague handling people operations and frontline locations at contact08@example.com.",
        "why_it_matters": "Direct referral to internal business unit owner who may be exploring an expense management tool.",
        "evidence": "Raghav: 'The colleague handling our people operations also deals with frontline processes and the locations. I think we may have been looking at a solution... send him a proposal and say you spoke with me... contact08@example.com.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C08 verbatim quote",
        "limitations": "Raghav could not confirm budget or current stage of internal discussions.",
        "next_steps": "Meera to email people operations lead at contact08@example.com referencing conversation with Raghav.",
        "owner": "Meera",
        "deal_intent": "Moderate - Qualified Lead",
        "category": "deals",
        "folder": "deals"
    },
    "C09": {
        "title": "Multi-Store Retail Lead with Communication Boundary",
        "company": "Multi-Store Chain (130 locations)",
        "contact": "Mr. Vedant",
        "rep": "Meera",
        "route": "Deal Next Steps / Nurture",
        "secondary_routes": ["Rep Coaching / Boundary Adherence"],
        "summary": "Outbound discovery call. Prospect operates 130 stores and uses in-house software. Vedant suggested reaching out to business head Mr. Rishabh via professional networking, but explicitly forbade mentioning his name.",
        "why_it_matters": "Valid executive target identified (Mr. Rishabh), but rep must strictly respect the boundary not to use Vedant's name.",
        "evidence": "Vedant: 'Our central team handles this. If you want to speak to somebody about it, you can find our business head, Mr Rishabh, on a professional networking site... No, please don\\'t use my name.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C09 verbatim quote",
        "limitations": "Does not guarantee Mr. Rishabh will take a cold meeting; in-house software is entrenched.",
        "next_steps": "Connect with Mr. Rishabh on LinkedIn without referencing Vedant. Coach rep on respecting contact boundaries.",
        "owner": "Meera",
        "deal_intent": "Low - Cold Target",
        "category": "deals",
        "folder": "deals"
    },
    "C10": {
        "title": "Former Meadowbrick Contact Outreach",
        "company": "Meadowbrick (Former) / Manufacturing Co",
        "contact": "Mr. Aniket",
        "rep": "Meera",
        "route": "Low Priority / Gatekeeper",
        "secondary_routes": ["Rep Coaching / Boundary Adherence"],
        "summary": "Meera reached Aniket, who stated he no longer works at Meadowbrick and is now in manufacturing. He agreed to receive a messaging brief but emphatically declined any follow-up phone calls.",
        "why_it_matters": "Stale contact record for Meadowbrick in CRM. Rep pushed for a follow-up call after contact requested messaging only, prompting irritation.",
        "evidence": "Aniket: 'Why don\\'t you just send me a brief on the messaging app? I\\'ll look at it and come back to you... Would a follow-up call on Monday or Tuesday... No. I said I will contact you if there is anything to discuss.'",
        "evidence_type": "quote",
        "evidence_ref": "Call C10 verbatim quote",
        "limitations": "No commercial opportunity established; contact has low patience for sales calls.",
        "next_steps": "Update Meadowbrick CRM record. Send brief on chat; do NOT schedule an unsolicited follow-up call.",
        "owner": "Meera",
        "deal_intent": "None",
        "category": "low_priority",
        "folder": "low_priority"
    },
    "M01": {
        "title": "Harborpath Advisory Channel Discussion",
        "company": "Harborpath Advisory",
        "contact": "Partner A",
        "rep": "Team member A (SpendNest)",
        "organizer": "team06@example.com",
        "route": "Partnership / Channel Advisory",
        "secondary_routes": ["Compliance Boundary"],
        "summary": "Advisory partner sought remote bank account setup for clients. SpendNest clarified it provides virtual accounts and corporate cards for operational spending, not primary deposit bank accounts. Partner agreed to review client-facing compliance collateral.",
        "why_it_matters": "Strong referral channel provided product scope is clearly delineated so partner does not misinform prospective clients.",
        "evidence": "Turn 1: 'My understanding was that you help people open bank accounts remotely...' Turn 2: 'Yes, with one important boundary: we provide virtual business accounts for operational spend, not licensed retail bank accounts...' Turn 26: 'We need clear client-facing documentation explaining what the account can and cannot do before we send anyone over.'",
        "evidence_type": "turns",
        "evidence_ref": "M01 Turn 1, Turn 2, Turn 26",
        "limitations": "No formal referral agreement signed; partner's client volume is not quantified.",
        "next_steps": "Prepare and dispatch compliance positioning document for Harborpath Advisory's onboarding team.",
        "owner": "Team member A",
        "deal_intent": "Channel Partnership",
        "category": "partnerships",
        "folder": "partnerships"
    },
    "M02": {
        "title": "LedgerBridge European Invoicing Vendor Review",
        "company": "LedgerBridge",
        "contact": "Partner A & B (LedgerBridge)",
        "rep": "Team member A (SpendNest Strategy)",
        "organizer": "team07@example.com",
        "route": "Vendor Evaluation / Internal",
        "secondary_routes": ["Exclude from Sales Pipeline"],
        "summary": "SpendNest strategy team met with LedgerBridge to evaluate their software for compliant European e-invoicing coverage for SpendNest's accounts receivable expansion. SpendNest is the buyer in this conversation.",
        "why_it_matters": "CRITICAL REVENUE INTELLIGENCE FINDING: Stored calendar meetings often get mistagged as sales opportunities. This is a vendor procurement evaluation and must be excluded from pipeline.",
        "evidence": "Turn 1: 'I work on strategy and partnerships at SpendNest. We serve businesses with cards and accounts payable, and we are developing accounts receivable. We want to understand whether LedgerBridge can give us compliant invoicing coverage in Europe...'",
        "evidence_type": "turns",
        "evidence_ref": "M02 Turn 1, Turn 36",
        "limitations": "Technical API integration timeline and pricing quotes are still under internal review.",
        "next_steps": "Strategy team to review LedgerBridge technical docs and compliance pricing; route meeting to Internal Ops.",
        "owner": "Team member A (Strategy)",
        "deal_intent": "Vendor Procurement (Not Sales)",
        "category": "internal_vendor",
        "folder": "internal_vendor"
    },
    "M03": {
        "title": "Asterloom Systems Enterprise Deal Review",
        "company": "Asterloom Systems",
        "contact": "Customer A & Customer B (Finance)",
        "rep": "Team member A (SpendNest)",
        "organizer": "team08@example.com",
        "route": "Deal Next Steps / Pipeline",
        "secondary_routes": ["Enterprise Opportunity"],
        "summary": "In-depth enterprise sales discussion with Asterloom Systems. Customer has ~65 employees, monthly vendor payments of INR 26–39 lakh, and requires corporate cards with dual-approval workflows and finance review before ERP sync. Awaiting proposal for CFO review.",
        "why_it_matters": "Highest-value qualified sales opportunity in the current extract. Clear budget, operational pain point, and decision-maker involvement.",
        "evidence": "Turn 1: 'My finance colleague is joining today because we need to understand how this would actually work, and then revisit the price.' Turn 34: 'We are roughly 65 employees... The external team processes vendor payments manually and it is expensive... perhaps INR 26–39 lakh a month.' Turn 36: 'Send the details first. We need time with the CFO and will tell you if another call is needed.'",
        "evidence_type": "turns",
        "evidence_ref": "M03 Turn 1, Turn 34, Turn 36",
        "limitations": "CFO has not yet signed off; pricing discount expectations may arise.",
        "next_steps": "Send detailed corporate cards proposal and ERP sync workflow document for CFO review.",
        "owner": "Team member A",
        "deal_intent": "High - Enterprise Opportunity",
        "category": "deals",
        "folder": "deals"
    },
    "M04": {
        "title": "Cedarwave Distribution Migration & Credit Line",
        "company": "Cedarwave Distribution",
        "contact": "Customer A & Customer B",
        "rep": "Team member A (SpendNest)",
        "organizer": "team09@example.com",
        "route": "Customer Success / Account Migration",
        "secondary_routes": ["Corporate Credit Integration"],
        "summary": "Migration planning for Cedarwave Distribution. Customer experiences acceptance issues with legacy prepaid cards and holds an existing bank corporate credit line of INR 1.3 crore. They wish to connect bank cards into SpendNest rather than only using prepaid. Also requested assistance resolving department user structures.",
        "why_it_matters": "Strategic customer retention and expansion. Account retention hinges on supporting their bank credit line feed and fixing department allocation.",
        "evidence": "Turn 2: 'Much of your usage is physical-card spending. We have seen acceptance problems with the existing programme and are proposing a move to a different provider...' Turn 22: 'We already have a corporate credit line of about INR 1.3 crore... If your platform can sit in between, we should understand that route.' Turn 30: 'There is also the earlier issue with moving users between departments.'",
        "evidence_type": "turns",
        "evidence_ref": "M04 Turn 2, Turn 22, Turn 30",
        "limitations": "Bank-issued card transaction feed integration requires network agreement and partner bank feasibility check.",
        "next_steps": "1) Confirm bank credit card feed eligibility with program team. 2) Schedule hands-on session to reorganize department user mappings.",
        "owner": "Team member A",
        "deal_intent": "Customer Retention & Migration",
        "category": "customer_success",
        "folder": "customer_success"
    },
    "M06": {
        "title": "Mapletrail Services Finance Workflow Discovery",
        "company": "Mapletrail Services",
        "contact": "Customer A (Finance Branch Lead)",
        "rep": "Team member A (SpendNest Finance)",
        "organizer": "team10@example.com",
        "route": "Product Discovery / Research",
        "secondary_routes": ["AR Module Feedback"],
        "summary": "Product discovery interview with branch finance lead at Mapletrail Services (software testing, 65 people in finance). Explored branch-level expense approvals and upcoming accounts receivable module requirements.",
        "why_it_matters": "Valuable product feedback for SpendNest's upcoming AR invoicing release.",
        "evidence": "Turn 1: 'Good to speak after connecting professionally. I work on finance at SpendNest, and part of my interest is how finance teams spend their time... We have expense workflows and are also working on receivables automation.' Turn 4: 'Roughly 65 people at the main office...'",
        "evidence_type": "turns",
        "evidence_ref": "M06 Turn 1, Turn 4",
        "limitations": "Not an active commercial purchasing evaluation.",
        "next_steps": "Document feedback into Product team backlog; follow up when AR beta release is ready.",
        "owner": "Team member A",
        "deal_intent": "Product Research",
        "category": "internal_vendor",
        "folder": "internal_vendor"
    },
    "M07": {
        "title": "Willowfield Trust Software Bug Escalation",
        "company": "Willowfield Trust",
        "contact": "Customer A",
        "rep": "Team member A (SpendNest)",
        "organizer": "team09@example.com",
        "route": "Customer Success / Bug Escalation",
        "secondary_routes": ["Engineering Escalation", "Difficult Routing Decision"],
        "summary": "In the initial batch, this record had no usable transcript. In the update batch (Revision 2), 27 turns were supplied showing Customer A screen-sharing two critical software bugs: 1) payment description changes reverting upon save, and 2) attachment upload failing during 'Recreate payment' workflow.",
        "why_it_matters": "DIFFICULT ROUTING CASE: Before the update, appeared as an ordinary check-in. Once late transcript arrived, revealed urgent customer-facing product bugs requiring immediate engineering escalation.",
        "evidence": "Turn 2: 'The first one is editing the description. I am changing this event-payment description to a short reference and clicking Save changes. Now look at the displayed description again.' Turn 3: 'The field still shows the earlier wording. So the change is not appearing after you save, is that right?' Turn 8: 'Next is Recreate payment... When I go through this route, I cannot upload a document.'",
        "evidence_type": "turns",
        "evidence_ref": "M07 Turn 2, Turn 3, Turn 8, Turn 27",
        "limitations": "Root cause unknown; requires developer debugging of payment form state persistence.",
        "next_steps": "File high-priority bug tickets with engineering; provide customer with status update by EOD.",
        "owner": "Team member A",
        "deal_intent": "Customer Retention - At Risk",
        "category": "customer_success",
        "folder": "customer_success"
    },
    "M09": {
        "title": "Brookmint Holdings & Northkite Setup Walkthrough",
        "company": "Brookmint Holdings / Northkite Equipment",
        "contact": "Customer A",
        "rep": "Team member A (SpendNest Support)",
        "organizer": "team11@example.com",
        "route": "Customer Onboarding / Support",
        "secondary_routes": ["Multi-Entity Access"],
        "summary": "Support onboarding session to resolve expired workspace invitation for Brookmint Holdings and address entity account access for Northkite Equipment. Rep sent fresh reset link and verified access.",
        "why_it_matters": "Ensures post-sale onboarding activation for multi-entity corporate customer.",
        "evidence": "Turn 1: 'The invitation for Brookmint Holdings did not work when I tried it. It may have expired...' Turn 2: 'There are two things to cover: getting you into Brookmint Holdings and the accounting issue you reported for Northkite Equipment.'",
        "evidence_type": "turns",
        "evidence_ref": "M09 Turn 1, Turn 2",
        "limitations": "Routine onboarding troubleshooting; no upsell potential identified.",
        "next_steps": "Verify customer successfully logs in and provisions team members across both entities.",
        "owner": "Team member A",
        "deal_intent": "Onboarding",
        "category": "customer_success",
        "folder": "customer_success"
    },
    "M10": {
        "title": "Internal Billing Workflow Training",
        "company": "SpendNest Internal Operations",
        "contact": "Team member B (Operations Trainee)",
        "rep": "Team member A (Billing Trainer)",
        "organizer": "team12@example.com",
        "route": "Internal Enablement / Training",
        "secondary_routes": ["Exclude from Sales Pipeline"],
        "summary": "Internal training session reviewing invoice generation, back-office administrator permissions, and billing clearing mechanisms for internal team members.",
        "why_it_matters": "Must be routed internally and excluded from customer pipeline or CRM activity metrics.",
        "evidence": "Turn 2: 'I do not think the optional attendee is joining. We can wait for the trainer to return.' Turn 3: 'Yesterday we covered the subscription side of billing. Any questions before I show the remaining part, how invoices are generated and cleared?'",
        "evidence_type": "turns",
        "evidence_ref": "M10 Turn 2, Turn 3",
        "limitations": "Purely internal operations enablement.",
        "next_steps": "Provide trainee with sandbox credentials for back-office billing simulator.",
        "owner": "Team member A",
        "deal_intent": "Internal Training",
        "category": "internal_vendor",
        "folder": "internal_vendor"
    }
}

# Generate rich records
records_dict = {}

# Process initial records
for r in initial_batch['records']:
    key = (r['source_type'], r['source_id'])
    records_dict[key] = {
        "batch_id": initial_batch['batch_id'],
        "revision": initial_batch['revision'],
        "source_type": r['source_type'],
        "source_id": r['source_id'],
        "record_ref": r.get('record_ref', ''),
        "payload": r.get('payload', {}),
        "transcript_payload": r.get('transcript_payload'),
        "manual_override": False,
        "manual_route": None,
        "manual_notes": None,
        "freshness": "current"
    }

# Function to evaluate analysis and route
def get_record_analysis(rec):
    ref = rec['record_ref']
    st = rec['source_type']
    p = rec['payload']
    tp = rec['transcript_payload']

    # Check if in known conversations
    if ref in CONVERSATION_ANALYSIS:
        # Special check for M07 before update
        if ref == "M07" and rec['revision'] < 2:
            return {
                "route": "Intake / Pending Transcript",
                "secondary_routes": ["Unreviewed"],
                "processing_state": "Pending Transcript",
                "summary": "Meeting scheduled with Willowfield Trust. No audio or transcript supplied in initial batch; transcript withheld upstream.",
                "why_it_matters": "Meeting occurred but content cannot be reviewed until transcript payload is delivered.",
                "evidence": "Source unavailable_reason: Transcript withheld in initial delivery batch.",
                "evidence_type": "system",
                "evidence_ref": "M07 rev 1 unavailable_reason",
                "limitations": "No transcript turns present in revision 1.",
                "next_steps": "Awaiting update batch delivery.",
                "owner": "Team member A",
                "deal_intent": "Unknown",
                "category": "intake_unreviewed",
                "folder": "intake_unreviewed"
            }
        base = CONVERSATION_ANALYSIS[ref].copy()
        base['processing_state'] = "Analysed"
        return base
    
    # Otherwise it is a background call or unrecorded meeting
    if st == 'call':
        dur = p.get('duration_seconds', 0)
        rep = p.get('rep_name') or p.get('rep_email') or 'Unknown'
        to_phone = p.get('to_number', 'Unknown')
        is_conn = p.get('is_connected', False)
        return {
            "title": f"Background Call ({ref})",
            "company": f"Dialed Number {to_phone}",
            "contact": to_phone,
            "rep": rep,
            "route": "Intake / No Audio Supplied",
            "secondary_routes": ["Short Dial"],
            "processing_state": "No Audio",
            "summary": f"Short {p.get('direction', 'outbound')} call of {dur}s by {rep}. No audio recording or transcript supplied in delivery dataset.",
            "why_it_matters": "Activity logged in telephony system but lacks substantive conversational evidence.",
            "evidence": f"Telemetry: duration={dur}s, direction={p.get('direction')}, is_connected={is_conn}",
            "evidence_type": "telemetry",
            "evidence_ref": f"{ref} Call Metadata",
            "limitations": "Upstream transcript is null. Connection flag is machine-reported and not verified by speech.",
            "next_steps": "No analytical action required. Stored as historical call volume.",
            "owner": rep,
            "deal_intent": "None",
            "category": "intake_unreviewed",
            "folder": "intake_unreviewed"
        }
    else:
        title = p.get('title', 'Calendar Meeting')
        org = p.get('organizer_email', 'Unknown')
        reason = tp.get('unavailable_reason') if tp else 'No transcript payload'
        rec_status = p.get('recording_status', 'unknown')
        return {
            "title": title,
            "company": title.split(' - ')[-1] if ' - ' in title else title,
            "contact": org,
            "rep": org,
            "organizer": org,
            "route": "Intake / No Audio Supplied",
            "secondary_routes": [rec_status],
            "processing_state": "No Audio",
            "summary": f"Meeting '{title}' organised by {org}. Status: {rec_status}. {reason}",
            "why_it_matters": "Calendar event occurred or was scheduled, but no speech transcript is available for evaluation.",
            "evidence": f"Recording status: {rec_status}. Unavailable reason: {reason}",
            "evidence_type": "system",
            "evidence_ref": f"{ref} Meeting Metadata",
            "limitations": "No transcript turns supplied in dataset.",
            "next_steps": "Verify with meeting organiser whether recording took place outside bot integration.",
            "owner": org,
            "deal_intent": "None",
            "category": "intake_unreviewed",
            "folder": "intake_unreviewed"
        }

# Generate markdown files and export manifest
manifest_records = []
folder_categories = ["deals", "customer_success", "partnerships", "internal_vendor", "low_priority", "intake_unreviewed"]
for cat in folder_categories:
    os.makedirs(os.path.join(EXPORT_DIR, cat), exist_ok=True)

# Build state with update applied for final export
updated_records_dict = records_dict.copy()
for r in update_batch['records']:
    key = (r['source_type'], r['source_id'])
    if key in updated_records_dict:
        updated_records_dict[key]['revision'] = update_batch['revision']
        updated_records_dict[key]['payload'] = r.get('payload', {})
        updated_records_dict[key]['transcript_payload'] = r.get('transcript_payload')
        updated_records_dict[key]['batch_id'] = update_batch['batch_id']
        updated_records_dict[key]['freshness'] = "updated_rev2"

# Write out markdown files for each record
for key, rec in sorted(updated_records_dict.items(), key=lambda x: x[1]['record_ref']):
    ref = rec['record_ref']
    st = rec['source_type']
    sid = rec['source_id']
    rev = rec['revision']
    analysis = get_record_analysis(rec)
    
    cat = analysis['category']
    route = analysis['route']
    clean_title = "".join(c for c in rec['payload'].get('title', 'record') if c.isalnum() or c in (' ', '_', '-')).strip()
    clean_title = clean_title.replace(' ', '_')[:30]
    filename = f"{ref}_{st}_{clean_title}.md"
    rel_path = f"{cat}/{filename}"
    abs_path = os.path.join(EXPORT_DIR, cat, filename)

    # Markdown content
    md_content = f"""# Revenue Intelligence Analysis: {ref} ({st.upper()})

- **Record Reference**: {ref}
- **Source Type**: {st}
- **Source ID**: `{sid}`
- **Applied Revision**: {rev}
- **Primary Assigned Route**: {route}
- **Secondary Routes**: {", ".join(analysis.get('secondary_routes', []))}
- **Processing / Review State**: {analysis['processing_state']}
- **Manual Override**: {'Yes' if rec['manual_override'] else 'No'}
- **Analysis Freshness**: {rec['freshness']}
- **Assigned Owner**: {analysis.get('owner', 'Unassigned')}
- **Deal Intent**: {analysis.get('deal_intent', 'N/A')}

---

## 1. Executive Summary & Why It Matters
{analysis['summary']}

**Why it matters to sales management**:
{analysis['why_it_matters']}

---

## 2. Verified Source Evidence
> {analysis['evidence']}

- **Evidence Type**: {analysis['evidence_type']}
- **Source Reference**: {analysis['evidence_ref']}

---

## 3. What the Evidence Does NOT Establish (Boundaries & Honest Uncertainty)
{analysis['limitations']}

---

## 4. Next Steps & Actionable Ownership
- **Action**: {analysis['next_steps']}
- **Owner**: {analysis.get('owner', 'Unassigned')}
"""
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    manifest_records.append({
        "source_type": st,
        "source_id": sid,
        "record_ref": ref,
        "applied_revision": rev,
        "primary_route": route,
        "secondary_routes": "; ".join(analysis.get('secondary_routes', [])),
        "output_path": rel_path,
        "processing_state": analysis['processing_state'],
        "manual_override": rec['manual_override'],
        "analysis_freshness": rec['freshness'],
        "owner": analysis.get('owner', 'Unassigned'),
        "deal_intent": analysis.get('deal_intent', 'N/A')
    })

# Write manifest.json
with open(os.path.join(EXPORT_DIR, 'manifest.json'), 'w', encoding='utf-8') as f:
    json.dump({
        "generated_at": datetime.now().isoformat(),
        "total_records": len(manifest_records),
        "contract_compliance": "DATA_CONTRACT.md rev 2",
        "manifest": manifest_records
    }, f, indent=2)

# Write manifest.csv
with open(os.path.join(EXPORT_DIR, 'manifest.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        "source_type", "source_id", "record_ref", "applied_revision", "primary_route",
        "secondary_routes", "output_path", "processing_state", "manual_override",
        "analysis_freshness", "owner", "deal_intent"
    ])
    writer.writeheader()
    writer.writerows(manifest_records)

# Write Daily Brief Markdown
daily_brief_content = """# Executive Sales Manager Brief: 21 August 2026 (Asia/Kolkata)

## 1. Executive Overview & Daily Metrics
Across all 44 selected interaction records on Friday, 21 August 2026:
- **Total Records Ingested**: 44 (30 Calls, 14 Meetings).
- **Usable Transcript Coverage**: 18 of 44 records (40.9%) have substantive conversational text (10 calls, 8 meetings post-M07 update).
- **Intake Records Without Audio**: 26 records (20 short background dials <31s, 6 unrecorded or empty meetings).
- **Source-Reported Connection Rate**: 9 of 30 calls reported `is_connected=true` (30.0%), but only 8 resulted in multi-turn dialogues with prospects.

---

## 2. Priority Deals & Commercial Pipeline
1. **Asterloom Systems (M03 - Enterprise Opportunity | Owner: Team member A)**
   - **Status**: High intent. Prospect has ~65 employees and monthly vendor invoice run rate of INR 26–39 lakh.
   - **Key Requirement**: Corporate cards with dual-approval rules and finance review prior to ERP synchronization.
   - **Action**: Deliver proposal and ERP security sync overview ahead of CFO review next week.
2. **Developer API Access Follow-Up (C03 - Technical Opportunity | Owner: Kiran)**
   - **Status**: Moderate intent, price sensitive. Contact Milan was travelling outdoors but asked for specific email follow-up.
   - **Action**: Email proposal titled *"Developer access and event notifications — follow-up"* and schedule call for Monday.
3. **Raghav Fulfillment Referral (C08 - Qualified Inbound | Owner: Meera)**
   - **Status**: Direct internal referral from Raghav to the people operations lead at `contact08@example.com`.
   - **Action**: Send proposal referencing conversation with Raghav.

---

## 3. Account Escalations & Customer Success
1. **Willowfield Trust (M07 - CRITICAL BUG ESCALATION | Owner: Team member A)**
   - **Status**: Customer screen-shared reproducible defects: event payment descriptions reverting after save; recreate payment file attachment failing.
   - **Action**: Escalate bug tickets to Core Engineering immediately. Provide status update to customer before EOD.
2. **Cedarwave Distribution (M04 - Card Migration & INR 1.3 Cr Credit Line | Owner: Team member A)**
   - **Status**: Customer struggling with prepaid acceptance issues and holds an INR 1.3 crore bank credit line.
   - **Action**: Confirm bank credit transaction feed feasibility and schedule a guided session to resolve department hierarchy errors.
3. **Brookmint Holdings / Northkite Equipment (M09 - Multi-Entity Setup | Owner: Team member A)**
   - **Status**: Resolved expired invitation link. Successfully validated multi-entity tenant access.

---

## 4. Partnerships & Channels
1. **Harborpath Advisory (M01 | Owner: Team member A)**: Clarified virtual spend accounts vs bank deposit accounts. Partner requested compliance collateral.
2. **Willowbank Advisory (C07 | Owner: Dev)**: Partnership exploration for overseas incorporated entities needing digital business accounts. Proposal to be messaged on chat before Monday follow-up.

---

## 5. Sales Hygiene, Coaching & Discrepancy Warnings
1. **CRITICAL REVENUE INTELLIGENCE FINDING (M02 - LedgerBridge)**:
   - Stored calendar title was 'LedgerBridge / SpendNest discussion'. Upstream CRM mistagged it as sales.
   - **Evidence**: SpendNest Strategy met with LedgerBridge to buy European e-invoicing compliance software.
   - **Resolution**: Route to `Internal / Vendor Evaluation`; exclude from sales rep quota and pipeline figures.
2. **CALLER METADATA MISMATCH (C06 - Meera vs Ravi)**:
   - Call record metadata identifies rep as `Meera`, but caller introduces himself as `Ravi`.
   - **Action**: Manager audit of telephony seat assignment to prevent rep commission misallocation.
3. **Boundary Adherence Coaching**:
   - **C09 (Vedant)**: Contact forbade using his name when contacting business head Mr. Rishabh. Rep must be coached on compliance.
   - **C10 (Aniket)**: Contact declined phone follow-up. Rep must respect messaging-only boundary.
"""

with open(os.path.join(EXPORT_DIR, 'daily_brief_2026-08-21.md'), 'w', encoding='utf-8') as f:
    f.write(daily_brief_content)

print(f"Successfully generated {len(manifest_records)} analysis files, manifest.json, manifest.csv, and daily_brief_2026-08-21.md in {EXPORT_DIR}")

# Also build records_database.json for the frontend app
full_database = {
    "generated_at": datetime.now().isoformat(),
    "initial_batch_id": initial_batch['batch_id'],
    "initial_revision": initial_batch['revision'],
    "update_batch_id": update_batch['batch_id'],
    "update_revision": update_batch['revision'],
    "initial_records": [
        {
            "source_type": r['source_type'],
            "source_id": r['source_id'],
            "record_ref": r.get('record_ref', ''),
            "revision": 1,
            "payload": r.get('payload', {}),
            "transcript_payload": r.get('transcript_payload'),
            "analysis": get_record_analysis({
                "record_ref": r.get('record_ref', ''),
                "source_type": r['source_type'],
                "payload": r.get('payload', {}),
                "transcript_payload": r.get('transcript_payload'),
                "revision": 1
            })
        }
        for r in initial_batch['records']
    ],
    "update_records": [
        {
            "source_type": r['source_type'],
            "source_id": r['source_id'],
            "record_ref": r.get('record_ref', ''),
            "revision": update_batch['revision'],
            "payload": r.get('payload', {}),
            "transcript_payload": r.get('transcript_payload'),
            "analysis": get_record_analysis({
                "record_ref": r.get('record_ref', ''),
                "source_type": r['source_type'],
                "payload": r.get('payload', {}),
                "transcript_payload": r.get('transcript_payload'),
                "revision": update_batch['revision']
            })
        }
        for r in update_batch['records']
    ],
    "conversations_library": CONVERSATION_ANALYSIS,
    "daily_brief": daily_brief_content
}

with open(os.path.join(BASE_DIR, 'revenue-inbox', 'data', 'records_database.json'), 'w', encoding='utf-8') as f:
    json.dump(full_database, f, indent=2)

print("Export and database generation complete!")
