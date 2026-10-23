import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Initialize 16:9 widescreen presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Obsidian FinTech Theme Palette
BG_COLOR = RGBColor(11, 15, 25)         # #0b0f19 Deep Space
CARD_BG = RGBColor(19, 26, 43)          # #131a2b Elevated Surface
CARD_BORDER = RGBColor(37, 48, 77)      # #25304d Border Subtle
TEXT_PRIMARY = RGBColor(248, 250, 252)  # #f8fafc Pure White
TEXT_SECONDARY = RGBColor(148, 163, 184)# #94a3b8 Muted Grey
ACCENT_CYAN = RGBColor(6, 182, 212)     # #06b6d4 Vibrant Cyan
ACCENT_INDIGO = RGBColor(99, 102, 241)  # #6366f1 Brand Indigo
ACCENT_EMERALD = RGBColor(16, 185, 129) # #10b981 Success Green
ACCENT_AMBER = RGBColor(245, 158, 11)   # #f59e0b Warning Amber
ACCENT_ROSE = RGBColor(239, 68, 68)     # #ef4444 Danger Red

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, badge_text, title_text):
    # Badge Pill
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f"VOLOPAY EVALUATION  •  {badge_text.upper()}"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # Title
    tx_box2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
    tf2 = tx_box2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_PRIMARY

def add_footer(slide, current_num):
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.4))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"SpendNest Revenue Intelligence Inbox  •  Candidate: Dinesh Madhavan M  •  Live: https://volopay-assignment-inqe.onrender.com  •  Slide {current_num} of 5"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_SECONDARY

def add_card(slide, left, top, width, height, border_color=CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape

# ==============================================================================
# SLIDE 1: The Manager Problem & Three Main Findings
# ==============================================================================
s1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s1)
add_header(s1, "Slide 1 • Problem Context & Ground-Truth Evidence", "1. The Manager Problem Solved & 3 Key Source Findings")
add_footer(s1, 1)

# Left Summary Card: Problem Context
add_card(s1, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.0))
tb_prob = s1.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(11.333), Inches(0.9))
tf_prob = tb_prob.text_frame
tf_prob.word_wrap = True
p = tf_prob.paragraphs[0]
p.text = "The Manager Problem:"
p.font.bold = True
p.font.size = Pt(12)
p.font.color.rgb = ACCENT_INDIGO
p2 = tf_prob.add_paragraph()
p2.text = "A sales manager receives fragmented telephony and calendar logs from multiple sources where labels contradict reality, background dials inflate activity counts, and vendor procurement discussions are misclassified as inbound sales leads."
p2.font.size = Pt(11)
p2.font.color.rgb = TEXT_PRIMARY

# 3 Column Cards for the 3 Key Findings
col_w = Inches(3.75)
gap = Inches(0.24)
top_y = Inches(2.65)
card_h = Inches(4.05)

findings = [
    (
        "Finding 1: Vendor Misclassified as Sales Pipeline",
        "Meeting M02 — LedgerBridge",
        "Turn 1: 'I work on strategy and partnerships at SpendNest... We want to understand whether LedgerBridge can give us compliant invoicing coverage in Europe...'",
        "SpendNest is the buyer! Upstream CRM tagged this as sales pipeline. Our system routes it to Vendor Evaluation / Internal, protecting quota and forecasting integrity.",
        ACCENT_INDIGO
    ),
    (
        "Finding 2: Telephony User Identity Mismatch",
        "Call C06 — Meera vs. Ravi",
        "Verbatim Spoken Audio: 'Good evening, Mr Nikhil... Ravi here. I'll say at the start that this is a cold call.'",
        "Telephony metadata attributes the dial to Meera, but spoken audio is Ravi. Flagged as Rep Coaching / Discrepancy Alert to prevent coaching and commission misallocation.",
        ACCENT_AMBER
    ),
    (
        "Finding 3: Channel Capability Disconnect",
        "Meeting M01 — Harborpath Advisory",
        "Turn 1 & 2: Partner seeks remote bank account opening. SpendNest clarifies: 'we provide virtual business accounts for spend, not licensed retail bank accounts...'",
        "Channel partner expectation risk. Routed to Partnerships with requirement to supply compliance positioning collateral before onboarding overseas clients.",
        ACCENT_CYAN
    )
]

for idx, (title, subtitle, passage, impact, accent) in enumerate(findings):
    c_left = Inches(0.8) + idx * (col_w + gap)
    add_card(s1, c_left, top_y, col_w, card_h, border_color=accent)
    tb = s1.shapes.add_textbox(c_left + Inches(0.15), top_y + Inches(0.15), col_w - Inches(0.3), card_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = subtitle.upper()
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = accent

    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_PRIMARY
    p_t.space_after = Pt(8)

    p_lbl1 = tf.add_paragraph()
    p_lbl1.text = "SOURCE PASSAGE EVIDENCE:"
    p_lbl1.font.size = Pt(9.5)
    p_lbl1.font.bold = True
    p_lbl1.font.color.rgb = TEXT_SECONDARY

    p_q = tf.add_paragraph()
    p_q.text = f'"{passage}"'
    p_q.font.size = Pt(10)
    p_q.font.italic = True
    p_q.font.color.rgb = TEXT_PRIMARY
    p_q.space_after = Pt(8)

    p_lbl2 = tf.add_paragraph()
    p_lbl2.text = "PRODUCT DECISION / IMPACT:"
    p_lbl2.font.size = Pt(9.5)
    p_lbl2.font.bold = True
    p_lbl2.font.color.rgb = accent

    p_imp = tf.add_paragraph()
    p_imp.text = impact
    p_imp.font.size = Pt(10)
    p_imp.font.color.rgb = TEXT_PRIMARY

# ==============================================================================
# SLIDE 2: Interface Choices & Deliberate Omissions
# ==============================================================================
s2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s2)
add_header(s2, "Slide 2 • UX Design Philosophy & Boundaries", "2. Interface Choices & Deliberate Omissions")
add_footer(s2, 2)

card_w2 = Inches(5.74)
top_y2 = Inches(1.5)
card_h2 = Inches(5.2)

# Left Column: Interface Choices
add_card(s2, Inches(0.8), top_y2, card_w2, card_h2, border_color=ACCENT_CYAN)
tb_c = s2.shapes.add_textbox(Inches(1.0), top_y2 + Inches(0.2), card_w2 - Inches(0.4), card_h2 - Inches(0.4))
tf_c = tb_c.text_frame
tf_c.word_wrap = True

p = tf_c.paragraphs[0]
p.text = "CORE INTERFACE CHOICES"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_CYAN
p.space_after = Pt(12)

choices = [
    ("Executive Left-Sidebar Navigation", "Consolidates Revenue Inbox, Contract Verification, Manager Daily Brief, and Export Center into an accessible SaaS layout."),
    ("Built-In 5-Step Contract Replay Simulator", "Interactive toolbar to test idempotent repeat batch imports, manual route overrides, and late-arriving update batches directly in the UI per DATA_CONTRACT.md."),
    ("Strict Mathematical Denominators", "Separates Call Reps (SDRs/AEs dialing) from Meeting Organizers (calendar coordinators). Transcript coverage explicitly calculated against all 44 selected records."),
    ("Slide-Out Deep Evidence Inspection Drawer", "Clicking any interaction slides out formatted dialogue turns with exact timecodes, verbatim evidence quotes, limitations, and assigned action owners.")
]

for title, desc in choices:
    p_title = tf_c.add_paragraph()
    p_title.text = f"• {title}"
    p_title.font.size = Pt(12)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_PRIMARY
    
    p_desc = tf_c.add_paragraph()
    p_desc.text = desc
    p_desc.font.size = Pt(10.5)
    p_desc.font.color.rgb = TEXT_SECONDARY
    p_desc.space_after = Pt(8)

# Right Column: Deliberate Omissions
add_card(s2, Inches(6.78), top_y2, card_w2, card_h2, border_color=ACCENT_AMBER)
tb_o = s2.shapes.add_textbox(Inches(7.0), top_y2 + Inches(0.2), card_w2 - Inches(0.4), card_h2 - Inches(0.4))
tf_o = tb_o.text_frame
tf_o.word_wrap = True

p = tf_o.paragraphs[0]
p.text = "DELIBERATE OMISSIONS (ENGINEERING DISCIPLINE)"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_AMBER
p.space_after = Pt(12)

omissions = [
    ("Zero Fabricated Summaries for Silent Records", "For the 26 records with null transcripts or empty turns, we deliberately refused to hallucinate synthetic summaries. They are logged honestly as 'Intake / No Audio Supplied'."),
    ("No Standalone Date Filter", "All supplied records fall on Friday, 21 August 2026 (Asia/Kolkata). Providing a date picker adds zero analytical value and was omitted per brief instructions."),
    ("No Speculative Pipeline / ARR Guessing", "The brief forbids inventing pipeline value that data does not establish. We show verified commercial volume (e.g. Asterloom INR 26-39L/mo) without guessing fictitious ARR."),
    ("No Authentication / Login Barriers", "In accordance with ASSIGNMENT.md line 86, we omitted passwords and external API keys so reviewers can evaluate the workspace instantly with zero configuration.")
]

for title, desc in omissions:
    p_title = tf_o.add_paragraph()
    p_title.text = f"✕ {title}"
    p_title.font.size = Pt(12)
    p_title.font.bold = True
    p_title.font.color.rgb = ACCENT_AMBER
    
    p_desc = tf_o.add_paragraph()
    p_desc.text = desc
    p_desc.font.size = Pt(10.5)
    p_desc.font.color.rgb = TEXT_SECONDARY
    p_desc.space_after = Pt(8)

# ==============================================================================
# SLIDE 3: Routing Architecture & The Difficult Case (M07)
# ==============================================================================
s3 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s3)
add_header(s3, "Slide 3 • Routing Taxonomy & Difficult Case", "3. Routing Taxonomy & The Difficult Case: Willowfield Trust (M07)")
add_footer(s3, 3)

# Left Column: 6 Routing Categories
add_card(s3, Inches(0.8), Inches(1.5), Inches(5.74), Inches(5.2), border_color=ACCENT_EMERALD)
tb_tax = s3.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.34), Inches(4.8))
tf_tax = tb_tax.text_frame
tf_tax.word_wrap = True

p = tf_tax.paragraphs[0]
p.text = "OPERATIONAL ROUTING TAXONOMY"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_EMERALD
p.space_after = Pt(10)

routes = [
    ("1. Deal Next Steps / Pipeline", "Active commercial evaluations with stated pricing/budget (M03 Asterloom, C03 Milan API, C08 Raghav referral)."),
    ("2. Customer Success / Bug Escalation", "Urgent software defects & account migrations (M07 Willowfield Trust, M04 Cedarwave)."),
    ("3. Partnerships / Channel Advisory", "Referral partners incorporating overseas businesses (C07 Willowbank Advisory, M01 Harborpath)."),
    ("4. Vendor & Internal Enablement", "Procurement reviews (M02 LedgerBridge) & internal staff training (M10 Billing walkthrough)."),
    ("5. Low Priority / Voicemail", "Gatekeeper transfers, voicemails, and short unreachables (C01, C02, C04, C06, C10)."),
    ("6. Intake / No Audio Supplied", "Short background dials & empty meetings awaiting audio (B01-B20, M05, M08, M11-M14).")
]

for title, desc in routes:
    p_title = tf_tax.add_paragraph()
    p_title.text = title
    p_title.font.size = Pt(11.5)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_PRIMARY
    
    p_desc = tf_tax.add_paragraph()
    p_desc.text = desc
    p_desc.font.size = Pt(10)
    p_desc.font.color.rgb = TEXT_SECONDARY
    p_desc.space_after = Pt(5)

# Right Column: The Difficult Case (M07)
add_card(s3, Inches(6.78), Inches(1.5), Inches(5.74), Inches(5.2), border_color=ACCENT_ROSE)
tb_m7 = s3.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.34), Inches(4.8))
tf_m7 = tb_m7.text_frame
tf_m7.word_wrap = True

p = tf_m7.paragraphs[0]
p.text = "THE DIFFICULT CASE: WILLOWFIELD TRUST (M07)"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_ROSE
p.space_after = Pt(10)

stages = [
    ("Delivery Batch 1 State (Revision 1)", "Arrived with null speech turns and unavailable_reason: 'Transcript withheld in initial delivery batch'. Provisionally assigned to Intake / Routine check-in."),
    ("Delivery Batch 2 Update (Revision 2)", "Arrived with 27 speech turns. During screen-share, Customer A demonstrated critical software bugs:\n• Turn 2 & 3: Editing event payment descriptions reverts upon clicking 'Save changes'.\n• Turn 8: Document upload fails when recreating a payment."),
    ("Manager Decision & Routing Shift", "Shifted immediately from routine check-in to 'Customer Success / Bug Escalation' with urgent engineering follow-up assigned to Arun."),
    ("Preserved Manual Override Contract", "Under DATA_CONTRACT.md, a manager's manual override applied in Step 3 survives Step 4 late updates, Step 5 batch replays, and full browser restarts via persistent localStorage.")
]

for title, desc in stages:
    p_title = tf_m7.add_paragraph()
    p_title.text = f"• {title}"
    p_title.font.size = Pt(11.5)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_PRIMARY
    
    p_desc = tf_m7.add_paragraph()
    p_desc.text = desc
    p_desc.font.size = Pt(10)
    p_desc.font.color.rgb = TEXT_SECONDARY
    p_desc.space_after = Pt(7)

# ==============================================================================
# SLIDE 4: Mathematical Audit Verification & Idempotence
# ==============================================================================
s4 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s4)
add_header(s4, "Slide 4 • Replay Tests & Data Contract Audit", "4. Mathematical Audit Verification of Key Numbers & Idempotence")
add_footer(s4, 4)

# 4 Key Number Grid Cards
card_w4 = Inches(2.78)
card_h4 = Inches(2.3)
top_y4 = Inches(1.5)

num_cards = [
    ("44 Total Records", "Unique (source_type, source_id)", "30 Calls & 14 Meetings occurring on local date 2026-08-21. Keyed strictly by composite tuple identity.", ACCENT_CYAN),
    ("17 ➔ 18 Transcripts", "Coverage Jump: 38.6% ➔ 40.9%", "Initial batch contains 17 usable transcripts. M07 update arrives in Rev 2, lifting coverage to 18 of 44 without duplicating records.", ACCENT_EMERALD),
    ("9 / 30 Calls Connected", "Reported Connection Rate: 30%", "Telephony reported 9 connected calls. However, audit reveals only 8 had substantive customer dialogue (C02/C04 hit voicemail).", ACCENT_AMBER),
    ("0 Duplicates / 44 Rejected", "Strict Replay Idempotence", "Re-ingesting initial batch in shuffled order safely ignores older/equal revisions. Zero duplicate records and zero count inflation.", ACCENT_INDIGO)
]

for idx, (headline, formula, sub, accent) in enumerate(num_cards):
    c_left = Inches(0.8) + idx * (card_w4 + Inches(0.2))
    add_card(s4, c_left, top_y4, card_w4, card_h4, border_color=accent)
    tb = s4.shapes.add_textbox(c_left + Inches(0.12), top_y4 + Inches(0.15), card_w4 - Inches(0.24), card_h4 - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = headline
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = accent

    p_f = tf.add_paragraph()
    p_f.text = formula
    p_f.font.size = Pt(10.5)
    p_f.font.bold = True
    p_f.font.color.rgb = TEXT_PRIMARY
    p_f.space_after = Pt(4)

    p_s = tf.add_paragraph()
    p_s.text = sub
    p_s.font.size = Pt(9.5)
    p_s.font.color.rgb = TEXT_SECONDARY

# Bottom Card: 5-Step Replay Verification Table
add_card(s4, Inches(0.8), Inches(4.05), Inches(11.733), Inches(2.65), border_color=CARD_BORDER)
tb_rep = s4.shapes.add_textbox(Inches(1.0), Inches(4.15), Inches(11.333), Inches(2.45))
tf_rep = tb_rep.text_frame
tf_rep.word_wrap = True

p = tf_rep.paragraphs[0]
p.text = "DATA_CONTRACT.md 5-STEP REPLAY AUDIT TRAIL"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO
p.space_after = Pt(6)

steps = [
    ("Step 1 (Initial Import)", "Ingests 01_initial.json. Establishes baseline: 44 unique records, 17 usable transcripts (38.6% coverage)."),
    ("Step 2 (Repeat Idempotence)", "Re-imports 01_initial.json in shuffled order. Strict idempotency confirmed: 0 new records, 44 duplicates safely rejected."),
    ("Step 3 (Manual Route Correction)", "Simulates manager judgment: route for M07 changed to 'Customer Success / Bug Escalation' with yellow badge."),
    ("Step 4 (Ingest Late Update)", "Ingests 02_update.json. M07 updated to Rev 2 with 27 turns. Coverage jumps 17 ➔ 18. Total records remains exactly 44."),
    ("Step 5 (Preserve Judgment)", "Re-imports Rev 1. Because M07 is already at Rev 2, Rev 1 is safely ignored. Manager's manual override survives intact.")
]

for title, desc in steps:
    p_st = tf_rep.add_paragraph()
    p_st.text = f"• {title}: "
    p_st.font.size = Pt(10.5)
    p_st.font.bold = True
    p_st.font.color.rgb = TEXT_PRIMARY
    p_st.text += desc
    p_st.space_after = Pt(3)

# ==============================================================================
# SLIDE 5: Trade-offs, AI Usage & Next Steps
# ==============================================================================
s5 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(s5)
add_header(s5, "Slide 5 • Ethics, AI Usage & Product Evolution", "5. Trade-offs, Rejected Decision & System Limitations")
add_footer(s5, 5)

card_w5 = Inches(5.74)
top_y5 = Inches(1.5)
card_h5 = Inches(5.2)

# Left Column: Deliberately Rejected Decision
add_card(s5, Inches(0.8), top_y5, card_w5, card_h5, border_color=ACCENT_ROSE)
tb_rej = s5.shapes.add_textbox(Inches(1.0), top_y5 + Inches(0.2), card_w5 - Inches(0.4), card_h5 - Inches(0.4))
tf_rej = tb_rej.text_frame
tf_rej.word_wrap = True

p = tf_rej.paragraphs[0]
p.text = "THE DELIBERATELY REJECTED DECISION"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_ROSE
p.space_after = Pt(10)

p_alt = tf_rej.add_paragraph()
p_alt.text = "Alternative Considered:"
p_alt.font.size = Pt(11)
p_alt.font.bold = True
p_alt.font.color.rgb = TEXT_PRIMARY
p_alt2 = tf_rej.add_paragraph()
p_alt2.text = "Using an LLM to guess deal ARR values from company names and employee estimates (e.g. projecting Asterloom as a $45,000 ARR deal)."
p_alt2.font.size = Pt(10.5)
p_alt2.font.color.rgb = TEXT_SECONDARY
p_alt2.space_after = Pt(8)

p_why = tf_rej.add_paragraph()
p_why.text = "Why It Was Rejected:"
p_why.font.size = Pt(11)
p_why.font.bold = True
p_why.font.color.rgb = ACCENT_ROSE
p_why2 = tf_rej.add_paragraph()
p_why2.text = "The brief explicitly mandates: 'Do not invent pipeline value, deal outcomes or account links that the data does not establish.' Hallucinating speculative financial numbers damages executive trust and misleads sales leadership."
p_why2.font.size = Pt(10.5)
p_why2.font.color.rgb = TEXT_SECONDARY
p_why2.space_after = Pt(8)

p_tr = tf_rej.add_paragraph()
p_tr.text = "Accepted Trade-off & Product Result:"
p_tr.font.size = Pt(11)
p_tr.font.bold = True
p_tr.font.color.rgb = ACCENT_EMERALD
p_tr2 = tf_rej.add_paragraph()
p_tr2.text = "We display qualitative commercial intent alongside verbatim financial statements (e.g., Asterloom's INR 26-39 lakh monthly vendor spend) without guessing synthetic revenue."
p_tr2.font.size = Pt(10.5)
p_tr2.font.color.rgb = TEXT_SECONDARY

# Right Column: AI Usage Disclosure & Future Roadmap
add_card(s5, Inches(6.78), top_y5, card_w5, card_h5, border_color=ACCENT_INDIGO)
tb_ai = s5.shapes.add_textbox(Inches(7.0), top_y5 + Inches(0.2), card_w5 - Inches(0.4), card_h5 - Inches(0.4))
tf_ai = tb_ai.text_frame
tf_ai.word_wrap = True

p = tf_ai.paragraphs[0]
p.text = "AI DISCLOSURE, TIME SPENT & ROADMAP"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT_INDIGO
p.space_after = Pt(10)

ai_points = [
    ("Pre-Generated vs. Dynamic Runtime Operations", "Conversation analyses, route rationales, and evidence quotes were prepared beforehand to guarantee factual citations and eliminate runtime hallucination. Ingestion deduplication, revision handling, override persistence, and ZIP packaging run dynamically in the client browser."),
    ("Approximate Hours Spent (~7 Hours Total)", "• Data Contract & Record Modeling: 2.5 hours\n• Web Dashboard & Design System: 2.5 hours\n• Manifest & ZIP Export Engine: 1.0 hour\n• Verification, Documentation & Slides: 1.0 hour"),
    ("Known System Limitations", "Cross-call speaker identity is not unified upstream. An organizer email is not automatically confirmed as an attendee or quota-carrying salesperson."),
    ("Future Improvements (Next Iteration)", "1. Real-time telephony webhook ingestion for live Gong/Zoom calls.\n2. Bi-directional CRM sync for automated override persistence.")
]

for title, desc in ai_points:
    p_t = tf_ai.add_paragraph()
    p_t.text = f"• {title}"
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_PRIMARY
    
    p_d = tf_ai.add_paragraph()
    p_d.text = desc
    p_d.font.size = Pt(9.8)
    p_d.font.color.rgb = TEXT_SECONDARY
    p_d.space_after = Pt(6)

# Save presentations
output_dir = os.path.dirname(os.path.abspath(__file__))
pptx_path = os.path.join(output_dir, 'slides', 'presentation.pptx')
prs.save(pptx_path)
print(f"Presentation saved to: {pptx_path}")

# Copy to revenue-inbox/slides for in-app viewer
inbox_slides_dir = os.path.join(output_dir, 'revenue-inbox', 'slides')
if os.path.exists(inbox_slides_dir):
    prs.save(os.path.join(inbox_slides_dir, 'presentation.pptx'))
    print(f"Presentation copied to: {inbox_slides_dir}")
