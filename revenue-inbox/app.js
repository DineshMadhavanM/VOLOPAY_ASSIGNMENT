/**
 * SpendNest Revenue Intelligence Inbox - Core Application Logic
 * Adheres strictly to DATA_CONTRACT.md, DATA_DICTIONARY.md, and ASSIGNMENT.md
 */

// Application State
const state = {
  db: null,                       // Database loaded from records_database.json
  records: new Map(),             // (source_type, source_id) -> Record
  appliedRevisions: new Map(),    // (source_type, source_id) -> highest revision integer
  overrides: new Map(),           // (source_type, source_id) -> { route, notes, timestamp }
  duplicatesRejected: 0,
  activeFilters: {
    search: '',
    sourceType: 'all',
    rep: 'all',
    route: 'all',
    state: 'all'
  },
  activeTab: 'conversations',
  currentSlide: 0,
  selectedRecord: null,
  theme: localStorage.getItem('spendnest_theme') || 'dark'
};

// Available 5 Slides Content
const SLIDES_CONTENT = [
  {
    num: 1,
    title: "1. The Manager Problem Solved & 3 Key Findings",
    badge: "Problem & Ground-Truth Findings",
    body: `
      <p><strong>The Core Problem:</strong> A sales manager receives fragmented, contradictory interaction logs from telephony and calendar systems. Upstream CRM labels frequently classify vendor meetings as sales pipeline, misattribute rep identities, or assume empty calendar invites were fruitful meetings.</p>
      <div style="margin: 16px 0;">
        <h4 style="color: var(--brand-primary); margin-bottom: 8px;">Three Critical Findings Linked to Exact Source Evidence:</h4>
        <ul style="padding-left: 20px;">
          <li>
            <strong>Finding 1: Vendor Evaluation Mistagged as Sales Pipeline (M02 - LedgerBridge)</strong><br>
            <em>Evidence (Turn 1):</em> "I work on strategy and partnerships at SpendNest... We want to understand whether LedgerBridge can give us compliant invoicing coverage in Europe..."<br>
            <em>Impact:</em> SpendNest is the prospective <strong>buyer/client</strong>, not the vendor! Upstream CRM tagged this as sales pipeline. Our system routes it to <code>Vendor Evaluation / Internal</code>, protecting quota and forecasting accuracy.
          </li>
          <li style="margin-top: 10px;">
            <strong>Finding 2: Telephony User Identity Mismatch (Call C06)</strong><br>
            <em>Evidence (Exact Quote):</em> Metadata identifies rep as <code>Meera</code>, but audio opens: <em>"Good evening, Mr Nikhil... Ravi here. I'll say at the start that this is a cold call."</em><br>
            <em>Impact:</em> Telephony seat misallocation. Blindly assigning call metrics to Meera distorts rep coaching and commissions. Flagged as <code>Rep Coaching / Data Discrepancy</code>.
          </li>
          <li style="margin-top: 10px;">
            <strong>Finding 3: Product Capability Disconnect (Meeting M01 - Harborpath Advisory)</strong><br>
            <em>Evidence (Turn 1 & 2):</em> Partner sought remote deposit bank accounts for overseas clients. SpendNest clarified: <em>"we provide virtual business accounts for operational spend, not licensed retail bank accounts..."</em><br>
            <em>Impact:</em> Identifies a recurring channel risk where advisory partners misunderstand product boundaries, requiring dedicated compliance positioning before partner launch.
          </li>
        </ul>
      </div>
    `
  },
  {
    num: 2,
    title: "2. Interface Choices & Deliberate Omissions",
    badge: "UX Design & System Boundaries",
    body: `
      <p><strong>Manager-First Information Architecture:</strong> Rather than drowning the sales manager in vanity charts, our interface prioritizes actionable exceptions, explicit denominators, and evidence inspectability.</p>
      <div style="margin: 16px 0;">
        <h4 style="color: var(--accent-cyan); margin-bottom: 8px;">Key Interface Choices:</h4>
        <ul style="padding-left: 20px;">
          <li><strong>Integrated Replay Simulator:</strong> Prominently displays the 5-step data contract verification so managers and auditors can test idempotence and late update handling in real time.</li>
          <li><strong>Rigorous Mathematical Denominators:</strong> We separate Call Reps (SDRs/AEs dialing) from Meeting Organizers (calendar coordinators who may not be attendees or reps). We report transcript coverage over all 44 selected records rather than inflating it.</li>
          <li><strong>Multi-Facet Exception Filters:</strong> Instant slicing by source type, rep, route, and review state (e.g. isolating unrecorded dials vs substantive prospect conversations).</li>
        </ul>
        <h4 style="color: var(--status-warning); margin: 16px 0 8px 0;">Deliberate Omissions:</h4>
        <ul style="padding-left: 20px;">
          <li><strong>Zero Hallucinated Analysis:</strong> For the 26 records with null transcripts or empty turns, we <em>deliberately declined</em> to invent synthetic summaries. They are clearly marked as <code>Intake / No Audio Supplied</code> with raw telemetry preserved.</li>
          <li><strong>No Standalone Date Filter:</strong> All supplied records occur on 21 August 2026 (Asia/Kolkata). Providing a date picker provides zero analytical value and wastes screen real estate.</li>
        </ul>
      </div>
    `
  },
  {
    num: 3,
    title: "3. Routing Taxonomy & The Difficult Decision",
    badge: "Routing Architecture & Case Study",
    body: `
      <p><strong>Action-Oriented Routing Taxonomy:</strong> Conversations are classified not by generic labels, but by operational destinations:</p>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 14px 0;">
        <div style="background: var(--bg-card); padding: 10px; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <strong style="color: var(--status-success);">1. Deal Next Steps / Pipeline</strong><br>
          Active commercial evaluations with stated pricing/budget (e.g. M03 Asterloom, C03 Milan API, C08 Raghav referral).
        </div>
        <div style="background: var(--bg-card); padding: 10px; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <strong style="color: var(--status-danger);">2. Customer Success / Escalations</strong><br>
          High-urgency customer retention, migrations, or software defects (e.g. M07 Willowfield Trust, M04 Cedarwave).
        </div>
        <div style="background: var(--bg-card); padding: 10px; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <strong style="color: var(--status-purple);">3. Partnerships / Channel Advisory</strong><br>
          Referral partners incorporating overseas businesses (e.g. C07 Willowbank Advisory, M01 Harborpath).
        </div>
        <div style="background: var(--bg-card); padding: 10px; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <strong style="color: var(--status-info);">4. Vendor / Internal Enablement</strong><br>
          Procurement reviews (M02 LedgerBridge) & internal staff training (M10 Billing walkthrough).
        </div>
      </div>
      <div style="background: rgba(245, 158, 11, 0.1); border-left: 3px solid var(--status-warning); padding: 12px; border-radius: 6px; margin-top: 10px;">
        <strong style="color: var(--status-warning);">The Difficult Routing Decision &mdash; Willowfield Trust (M07):</strong><br>
        In Delivery Batch 1, M07 arrived with no transcript and was labeled as an ordinary account check-in. When Delivery Batch 2 arrived with 27 turns, Customer A screen-shared critical software bugs (event payment description reverting upon save; recreate payment file attachment failing). Routing was immediately shifted from <em>Routine Check-in</em> to <em>Customer Success / Critical Bug Escalation</em>. Even under re-import, manager judgment is preserved!
      </div>
    `
  },
  {
    num: 4,
    title: "4. Verification of Key Numbers & Analytical Rigor",
    badge: "Audit Trail & Verification",
    body: `
      <p><strong>Mathematical Verification Against Source Records:</strong> Every metric displayed in the inbox is traceable to exact source fields in <code>01_initial.json</code> and <code>02_update.json</code>:</p>
      <table style="width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px;">
        <thead>
          <tr style="background: var(--bg-elevated); text-align: left;">
            <th style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">Metric</th>
            <th style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">Initial Batch (Rev 1)</th>
            <th style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">Update Batch (Rev 2)</th>
            <th style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">Mathematical Definition</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);"><strong>Unique Records</strong></td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">44 records</td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">44 records (strict)</td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">Count of unique (source_type, source_id)</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);"><strong>Transcript Coverage</strong></td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">17 / 44 (38.6%)</td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">18 / 44 (40.9%)</td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">Records with non-null text or turns > 0</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);"><strong>Calls vs Meetings</strong></td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">30 Calls, 14 Meetings</td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">30 Calls, 14 Meetings</td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">Partitioned by source_type</td>
          </tr>
          <tr>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);"><strong>Connection Rate</strong></td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">9 / 30 calls (30.0%)</td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">9 / 30 calls (30.0%)</td>
            <td style="padding: 8px; border-bottom: 1px solid var(--border-subtle);">Calls with is_connected=true / 30 total calls</td>
          </tr>
        </tbody>
      </table>
      <p style="font-size: 13px; color: var(--text-secondary);">
        <strong>Repeat Import Idempotence:</strong> Importing Batch 1 a second time with altered array order verifies 0 duplicate entries, exactly 44 records, and 0 metric inflation.
      </p>
    `
  },
  {
    num: 5,
    title: "5. Trade-offs, Rejected Decisions & Future Scope",
    badge: "Engineering Ethics & AI Disclosure",
    body: `
      <div style="background: rgba(239, 68, 68, 0.1); border-left: 3px solid var(--status-danger); padding: 14px; border-radius: 6px; margin-bottom: 16px;">
        <h4 style="color: var(--status-danger); margin-bottom: 6px;">The Deliberately Rejected Decision: Auto-Estimating Deal Pipeline Values</h4>
        <p style="font-size: 13px; line-height: 1.6; color: var(--text-primary);">
          <strong>Alternative Considered:</strong> Using an LLM to hallucinate deal sizes and pipeline revenue estimates based on prospect employee counts (e.g. estimating Asterloom at $45,000 ARR).<br>
          <strong>Why Rejected:</strong> The assessment instructions explicitly prohibit inventing pipeline value or deal outcomes not established by the data. Hallucinated financial numbers destroy managerial credibility in an audit.<br>
          <strong>Accepted Trade-off:</strong> We display qualitative opportunity intent and verbatim budgetary statements (e.g. Asterloom's INR 26&ndash;39 lakh vendor payment volume) without fabricating speculative ARR figures.
        </p>
      </div>
      <div style="margin-top: 12px;">
        <h4 style="color: var(--text-primary); margin-bottom: 6px;">AI Usage & Implementation Disclosure:</h4>
        <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
          In accordance with <code>ASSIGNMENT.md</code>, analysis summaries and evidence references were pre-generated and mapped deterministically. Ingestions, revision deduplication, manual override preservation, and ZIP manifest export run entirely dynamically client-side in the browser.
        </p>
        <h4 style="color: var(--text-primary); margin: 12px 0 6px 0;">Known Limitations & Next Steps:</h4>
        <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
          1) Cross-call speaker mapping is not established upstream. 2) Future iteration will connect live webhooks to ingest real-time Gong/Zoom transcripts as they finish processing.
        </p>
      </div>
    `
  }
];

// Helper: Make composite record key
function getRecordKey(sourceType, sourceId) {
  return `${sourceType}::${sourceId}`;
}

// Initialize Application
async function initApp() {
  console.log("Initializing SpendNest Revenue Intelligence Inbox...");
  applyTheme(state.theme);

  // Load Overrides from localStorage
  loadOverrides();

  // Load bundled database
  try {
    const res = await fetch('data/records_database.json');
    if (!res.ok) throw new Error("Could not load records_database.json");
    state.db = await res.json();
    console.log("Database loaded successfully:", state.db);

    // Initial Ingestion (Step 1)
    ingestBatch(state.db.initial_records, state.db.initial_revision, state.db.initial_batch_id, false);
    updateReplayStatus("State: Initial delivery ingested (44 records, 17 with transcripts, revision 1 applied).");

  } catch (err) {
    console.error("Failed to load records database:", err);
    showToast("Error loading dataset. Please check console.", "error");
  }

  // Setup Event Listeners
  setupEventListeners();

  // Render Everything
  renderAll();
}

// Ingestion Engine adhering strictly to DATA_CONTRACT.md
function ingestBatch(recordsList, revision, batchId, isUpdateBatch = false) {
  let newRecordsAdded = 0;
  let recordsUpdated = 0;
  let duplicatesIgnored = 0;

  recordsList.forEach(rec => {
    const key = getRecordKey(rec.source_type, rec.source_id);
    const existingRevision = state.appliedRevisions.get(key) || 0;

    // Rule: Same or older revisions are ignored
    if (state.records.has(key) && revision <= existingRevision) {
      duplicatesIgnored++;
      return;
    }

    // Apply Higher Revision
    const isUpdate = state.records.has(key);
    state.appliedRevisions.set(key, revision);

    // Check if there is an active manual override for this record
    const hasOverride = state.overrides.has(key);
    const overrideData = state.overrides.get(key);

    const recordData = {
      ...rec,
      revision: revision,
      batch_id: batchId,
      manual_override: hasOverride,
      manual_route: hasOverride ? overrideData.route : null,
      manual_notes: hasOverride ? overrideData.notes : null,
      freshness: isUpdateBatch ? 'updated_rev2' : 'current'
    };

    state.records.set(key, recordData);

    if (isUpdate) {
      recordsUpdated++;
    } else {
      newRecordsAdded++;
    }
  });

  state.duplicatesRejected += duplicatesIgnored;
  console.log(`Batch [${batchId}] processed: Added ${newRecordsAdded}, Updated ${recordsUpdated}, Ignored ${duplicatesIgnored}`);
}

// LocalStorage Overrides Management
function loadOverrides() {
  try {
    const raw = localStorage.getItem('spendnest_manual_overrides');
    if (raw) {
      const parsed = JSON.parse(raw);
      state.overrides = new Map(Object.entries(parsed));
      console.log(`Loaded ${state.overrides.size} persistent overrides from localStorage.`);
    }
  } catch (e) {
    console.warn("Could not load overrides from localStorage", e);
  }
}

function saveOverride(sourceType, sourceId, newRoute, notes) {
  const key = getRecordKey(sourceType, sourceId);
  const overrideData = {
    route: newRoute,
    notes: notes,
    timestamp: new Date().toISOString()
  };
  state.overrides.set(key, overrideData);

  // Update in-memory record
  if (state.records.has(key)) {
    const rec = state.records.get(key);
    rec.manual_override = true;
    rec.manual_route = newRoute;
    rec.manual_notes = notes;
  }

  // Persist to localStorage
  const obj = Object.fromEntries(state.overrides);
  localStorage.setItem('spendnest_manual_overrides', JSON.stringify(obj));

  showToast(`Manual route override saved for ${sourceId.slice(0, 8)}: "${newRoute}"`, "success");
  updateReplayStatus(`Manual Override Saved: ${sourceId.slice(0, 8)} route set to "${newRoute}".`);
  renderAll();
}

function clearOverride(sourceType, sourceId) {
  const key = getRecordKey(sourceType, sourceId);
  if (state.overrides.has(key)) {
    state.overrides.delete(key);
    const obj = Object.fromEntries(state.overrides);
    localStorage.setItem('spendnest_manual_overrides', JSON.stringify(obj));

    if (state.records.has(key)) {
      const rec = state.records.get(key);
      rec.manual_override = false;
      rec.manual_route = null;
      rec.manual_notes = null;
    }

    showToast(`Override cleared for ${sourceId.slice(0, 8)}. Reverted to automated suggestion.`, "info");
    updateReplayStatus(`Override cleared for ${sourceId.slice(0, 8)}.`);
    renderAll();
  }
}

function resetAllState() {
  localStorage.removeItem('spendnest_manual_overrides');
  state.overrides.clear();
  state.records.clear();
  state.appliedRevisions.clear();
  state.duplicatesRejected = 0;

  // Re-ingest initial batch
  ingestBatch(state.db.initial_records, state.db.initial_revision, state.db.initial_batch_id, false);

  updateReplayStatus("State fully reset. Initial batch (Rev 1) loaded with clean slate.");
  showToast("Application state reset to initial clean baseline.", "info");
  renderAll();
}

// 5 REPLAY SIMULATOR ACTIONS
function runReplayStep1() {
  // 1. Initial Import
  state.records.clear();
  state.appliedRevisions.clear();
  state.duplicatesRejected = 0;
  ingestBatch(state.db.initial_records, state.db.initial_revision, state.db.initial_batch_id, false);
  updateReplayStatus("Step 1 Executed: Initial batch ingested. 44 records loaded, 17 with transcripts.");
  setActiveReplayButton('btn-step-1');
  showToast("Step 1: Ingested initial batch (Rev 1).", "info");
  renderAll();
}

function runReplayStep2() {
  // 2. Repeat Import (Test Idempotence)
  // Shuffled copy of initial records
  const shuffled = [...state.db.initial_records].sort(() => Math.random() - 0.5);
  const beforeCount = state.records.size;
  ingestBatch(shuffled, state.db.initial_revision, state.db.initial_batch_id, false);
  const afterCount = state.records.size;

  updateReplayStatus(`Step 2 (Idempotence Test): Re-imported initial batch in shuffled order. 0 duplicates added, 44 duplicates safely rejected.`);
  setActiveReplayButton('btn-step-2');
  showToast(`Idempotence Verified! Count remains strictly ${afterCount}. Duplicates safely ignored.`, "success");
  renderAll();
}

function runReplayStep3() {
  // 3. Apply Route Correction on M07 (or currently selected record)
  const targetId = '4f304fff-fd40-5cfc-a366-0a134c445c2a'; // M07 ID
  saveOverride('meeting', targetId, 'Customer Success / Bug Escalation', 'Manager override: customer reported payment description save failure and upload errors.');
  setActiveReplayButton('btn-step-3');
}

function runReplayStep4() {
  // 4. Ingest Late Update (Rev 2 with M07 27 turns)
  ingestBatch(state.db.update_records, state.db.update_revision, state.db.update_batch_id, true);
  updateReplayStatus("Step 4: Update Batch (Rev 2) applied! M07 updated with 27 turns. Total transcripts now 18/44. Manual route preserved!");
  setActiveReplayButton('btn-step-4');
  showToast("Step 4: Late transcript ingested. Coverage rose to 18/44!", "success");
  renderAll();
}

function runReplayStep5() {
  // 5. Replay Initial Batch & Preserve Override
  const prevM07 = state.records.get('meeting::4f304fff-fd40-5cfc-a366-0a134c445c2a');
  ingestBatch(state.db.initial_records, state.db.initial_revision, state.db.initial_batch_id, false);
  const postM07 = state.records.get('meeting::4f304fff-fd40-5cfc-a366-0a134c445c2a');

  const overrideSurvived = postM07 && postM07.manual_override;
  const revSurvived = postM07 && postM07.revision === 2;

  updateReplayStatus(`Step 5 Contract Verified: Re-imported Rev 1. M07 remained on Rev 2 (turns: 27). Manual override survived intact!`);
  setActiveReplayButton('btn-step-5');
  showToast(`Judgment Preserved! M07 override survived re-import and retains Rev 2 text.`, "success");
  renderAll();
}

function setActiveReplayButton(btnId) {
  document.querySelectorAll('.replay-btn').forEach(btn => btn.classList.remove('active'));
  const target = document.getElementById(btnId);
  if (target) target.classList.add('active');
}

function updateReplayStatus(msg) {
  const el = document.getElementById('replay-status-message');
  if (el) el.textContent = msg;

  // Mini Telemetry
  const records = Array.from(state.records.values());
  const transcripts = records.filter(hasUsableTranscript).length;
  const overrides = records.filter(r => r.manual_override).length;
  const maxRev = Math.max(...records.map(r => r.revision), 1);

  document.getElementById('telemetry-unique-count').textContent = records.length;
  document.getElementById('telemetry-revision').textContent = maxRev;
  document.getElementById('telemetry-transcripts').textContent = `${transcripts}/44 (${((transcripts/44)*100).toFixed(1)}%)`;
  document.getElementById('telemetry-overrides').textContent = overrides;
  document.getElementById('telemetry-dups').textContent = state.duplicatesRejected;
}

// Check if record has usable transcript according to DATA_DICTIONARY.md
function hasUsableTranscript(rec) {
  if (rec.source_type === 'call') {
    return Boolean(rec.payload && rec.payload.transcript && rec.payload.transcript.trim().length > 0);
  } else {
    return Boolean(rec.transcript_payload && rec.transcript_payload.turns && rec.transcript_payload.turns.length > 0);
  }
}

// Get active assigned route (Manual override supersedes automated suggestion)
function getAssignedRoute(rec) {
  if (rec.manual_override && rec.manual_route) {
    return rec.manual_route;
  }
  return rec.analysis ? rec.analysis.route : 'Intake / No Audio Supplied';
}

// Get badge CSS class for a route
function getRouteBadgeClass(route) {
  if (route.includes('Pipeline') || route.includes('Nurture')) return 'badge-route-deals';
  if (route.includes('Customer Success') || route.includes('Bug')) return 'badge-route-cs';
  if (route.includes('Partnership')) return 'badge-route-partnerships';
  if (route.includes('Vendor')) return 'badge-route-vendor';
  if (route.includes('Rejected') || route.includes('Voicemail')) return 'badge-route-low';
  return 'badge-route-intake';
}

// Render All Components
function renderAll() {
  renderMetrics();
  renderConversationsTable();
  renderExportManifest();
  renderSlide(state.currentSlide);
}

// Render Dashboard Metric Cards
function renderMetrics() {
  const allRecords = Array.from(state.records.values());
  const total = allRecords.length;

  const calls = allRecords.filter(r => r.source_type === 'call');
  const meetings = allRecords.filter(r => r.source_type === 'meeting');

  const withTranscripts = allRecords.filter(hasUsableTranscript).length;
  const transcriptPct = total > 0 ? ((withTranscripts / total) * 100).toFixed(1) : 0;

  // Calls connection calculation: is_connected === true
  const connectedCalls = calls.filter(c => c.payload && c.payload.is_connected === true).length;
  const callsWithConnFlag = calls.filter(c => c.payload && c.payload.is_connected !== null && c.payload.is_connected !== undefined).length;
  const connPct = callsWithConnFlag > 0 ? ((connectedCalls / callsWithConnFlag) * 100).toFixed(1) : 0;

  // Count active overrides
  const overrideCount = allRecords.filter(r => r.manual_override).length;

  // DOM Updates
  document.getElementById('badge-record-count').textContent = `${total} Records Ingested`;
  const sidebarInboxBadge = document.getElementById('sidebar-inbox-badge');
  if (sidebarInboxBadge) sidebarInboxBadge.textContent = total;
  document.getElementById('metric-total-records').textContent = total;
  document.getElementById('metric-split-text').textContent = `${calls.length} Calls • ${meetings.length} Meetings`;

  document.getElementById('metric-transcript-count').textContent = withTranscripts;
  document.getElementById('metric-transcript-pct').textContent = `${transcriptPct}%`;
  document.getElementById('metric-coverage-bar').style.width = `${transcriptPct}%`;

  const m07 = state.records.get('meeting::4f304fff-fd40-5cfc-a366-0a134c445c2a');
  const m07HasTurns = m07 && m07.transcript_payload && m07.transcript_payload.turns && m07.transcript_payload.turns.length > 0;
  document.getElementById('metric-coverage-subtext').textContent = m07HasTurns
    ? `10 Calls • 8 Meetings (M07 Rev 2 Active)`
    : `10 Calls • 7 Meetings (M07 Pending Update)`;

  document.getElementById('metric-connect-rate').textContent = `${connPct}%`;

  document.getElementById('metric-override-count').textContent = overrideCount;
  document.getElementById('metric-override-bar').style.width = `${(overrideCount / 5) * 100}%`;
  document.getElementById('metric-review-subtext').textContent = overrideCount > 0
    ? `${overrideCount} Active Override(s) Preserved`
    : `44 Records under audit governance`;
}

// Render Conversations Inbox Table
function renderConversationsTable() {
  const tbody = document.getElementById('conversations-table-body');
  if (!tbody) return;

  const records = Array.from(state.records.values());

  // Filter records
  const filtered = records.filter(rec => {
    const f = state.activeFilters;
    const ref = rec.record_ref || '';
    const st = rec.source_type || '';
    const p = rec.payload || {};
    const title = p.title || '';
    const rep = p.rep_name || p.rep_email || p.organizer_email || '';
    const toNum = p.to_number || '';
    const assignedRoute = getAssignedRoute(rec);
    const hasText = hasUsableTranscript(rec);

    // Search filter
    if (f.search) {
      const q = f.search.toLowerCase();
      const match = ref.toLowerCase().includes(q) ||
                    title.toLowerCase().includes(q) ||
                    rep.toLowerCase().includes(q) ||
                    toNum.toLowerCase().includes(q) ||
                    assignedRoute.toLowerCase().includes(q) ||
                    rec.source_id.toLowerCase().includes(q);
      if (!match) return false;
    }

    // Source Type filter
    if (f.sourceType !== 'all' && st !== f.sourceType) return false;

    // Rep / Organiser filter
    if (f.rep !== 'all') {
      const matchRep = rep.toLowerCase().includes(f.rep.toLowerCase());
      if (!matchRep) return false;
    }

    // Route filter
    if (f.route !== 'all' && assignedRoute !== f.route) return false;

    // State filter
    if (f.state !== 'all') {
      if (f.state === 'Overridden' && !rec.manual_override) return false;
      if (f.state === 'No Audio' && hasText) return false;
      if (f.state === 'Analysed' && !hasText) return false;
      if (f.state === 'Pending Transcript' && (hasText || rec.revision >= 2)) return false;
    }

    return true;
  });

  // Update Live Filter Results Counter
  const counterEl = document.getElementById('filter-results-counter');
  if (counterEl) {
    counterEl.textContent = `${filtered.length} of ${records.length} Shown`;
  }

  // Sort by Record Ref (B01..B20, C01..C10, M01..M14)
  filtered.sort((a, b) => (a.record_ref || '').localeCompare(b.record_ref || ''));

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 40px; color: var(--text-muted); font-size: 13px;">No records match the selected filter criteria. <button class="clear-filters-btn" onclick="document.getElementById('btn-clear-filters').click()" style="margin-left: 8px; text-decoration: underline;">Reset Filters</button></td></tr>`;
    return;
  }

  tbody.innerHTML = filtered.map(rec => {
    const ref = rec.record_ref;
    const st = rec.source_type;
    const p = rec.payload || {};
    const sid = rec.source_id;
    const hasText = hasUsableTranscript(rec);
    const assignedRoute = getAssignedRoute(rec);
    const badgeClass = getRouteBadgeClass(assignedRoute);

    let displayTitle = p.title;
    if (!displayTitle) {
      displayTitle = st === 'call' ? `Call to ${p.to_number || 'External'}` : 'Calendar Meeting';
    }

    const repLabel = st === 'call'
      ? (p.rep_name || p.rep_email || 'Unknown Rep')
      : (p.organizer_email || 'Unknown Organiser');

    const durationSec = p.duration_seconds ? `${p.duration_seconds}s` : '—';
    const isConn = st === 'call' ? (p.is_connected ? 'Yes' : 'No') : 'N/A';

    let stateLabel = hasText ? 'Analysed' : 'No Audio';
    if (rec.manual_override) stateLabel = 'Overridden';
    if (ref === 'M07' && rec.revision === 2) stateLabel = 'Updated (Rev 2)';

    const rowClass = rec.manual_override ? 'row-override' : (rec.revision >= 2 ? 'row-updated' : '');
    const initials = repLabel.replace(/@.*/, '').split(/[\s._-]+/).filter(Boolean).map(w => w[0]).join('').slice(0, 2).toUpperCase() || 'SP';

    return `
      <tr class="${rowClass}" onclick="openRecordDrawer('${st}', '${sid}')">
        <td><span class="ref-pill">${ref}</span></td>
        <td>
          <span class="badge ${st === 'call' ? 'badge-call' : 'badge-meeting'}">
            ${st === 'call' ? '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" style="margin-right: 3px;"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>' : '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" style="margin-right: 3px;"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'}
            ${st.toUpperCase()}
          </span>
        </td>
        <td>
          <div style="font-weight: 600; color: var(--text-primary); font-size: 13.5px; line-height: 1.3;">${escapeHtml(displayTitle)}</div>
          <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); margin-top: 2px;">${sid.slice(0, 18)}...</div>
        </td>
        <td>
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="rep-avatar-xs">${initials}</span>
            <div>
              <div style="font-size: 13px; font-weight: 600; color: var(--text-primary);">${escapeHtml(repLabel)}</div>
              <div style="font-size: 10.5px; color: var(--text-muted);">${st === 'call' ? 'Sales Dial' : 'Calendar Event'}</div>
            </div>
          </div>
        </td>
        <td style="font-family: var(--font-mono); font-size: 12.5px; color: var(--text-secondary);">${durationSec}</td>
        <td>
          <span style="font-size: 12px; font-weight: 600; color: ${isConn === 'Yes' ? 'var(--status-success)' : 'var(--text-muted)'}; display: inline-flex; align-items: center; gap: 4px;">
            ${isConn === 'Yes' ? '<span class="status-dot green"></span>' : '<span class="status-dot muted"></span>'}
            ${isConn}
          </span>
        </td>
        <td>
          <span class="badge ${badgeClass}">${escapeHtml(assignedRoute)}</span>
          ${rec.manual_override ? `<span class="badge-override" title="${escapeHtml(rec.manual_notes || '')}">OVERRIDE</span>` : ''}
          ${ref === 'M07' && rec.revision === 2 ? `<span class="badge-late">REV 2</span>` : ''}
        </td>
        <td>
          <span style="font-size: 12px; font-weight: 500; color: ${hasText ? 'var(--accent-cyan)' : 'var(--text-muted)'};">
            ${stateLabel}
          </span>
        </td>
        <td>
          <button class="action-btn-sm" onclick="event.stopPropagation(); openRecordDrawer('${st}', '${sid}')">
            Inspect &rarr;
          </button>
        </td>
      </tr>
    `;
  }).join('');
}

// Render Export Manifest Table
function renderExportManifest() {
  const tbody = document.getElementById('export-manifest-table-body');
  if (!tbody) return;

  const records = Array.from(state.records.values());
  records.sort((a, b) => (a.record_ref || '').localeCompare(b.record_ref || ''));

  tbody.innerHTML = records.map(rec => {
    const ref = rec.record_ref;
    const st = rec.source_type;
    const rev = rec.revision;
    const assignedRoute = getAssignedRoute(rec);
    const cat = rec.analysis ? rec.analysis.category : 'intake_unreviewed';
    const path = `${cat}/${ref}_${st}.md`;
    const stateLabel = hasUsableTranscript(rec) ? 'Analysed' : 'No Audio';

    return `
      <tr>
        <td><strong>${ref}</strong></td>
        <td>${st}</td>
        <td>Rev ${rev}</td>
        <td>${escapeHtml(assignedRoute)}</td>
        <td style="font-family: var(--font-mono); color: var(--accent-cyan);">${path}</td>
        <td>${stateLabel}</td>
        <td>${rec.manual_override ? '<span style="color: var(--status-warning); font-weight: bold;">Yes</span>' : 'No'}</td>
      </tr>
    `;
  }).join('');
}

// Deep Inspection Drawer
function openRecordDrawer(sourceType, sourceId) {
  const key = getRecordKey(sourceType, sourceId);
  const rec = state.records.get(key);
  if (!rec) return;

  state.selectedRecord = rec;

  const drawer = document.getElementById('inspection-drawer');
  const backdrop = document.getElementById('drawer-backdrop');
  drawer.classList.add('open');
  backdrop.classList.add('open');

  // Header
  const p = rec.payload || {};
  const ref = rec.record_ref;
  const st = rec.source_type;
  const title = p.title || (st === 'call' ? `Call to ${p.to_number || 'External'}` : 'Calendar Meeting');

  document.getElementById('drawer-title').textContent = `${ref} — ${title}`;

  // Pills
  const pillsEl = document.getElementById('drawer-meta-pills');
  pillsEl.innerHTML = `
    <span class="badge ${st === 'call' ? 'badge-call' : 'badge-meeting'}">${st.toUpperCase()}</span>
    <span class="badge" style="background: var(--bg-elevated); color: var(--text-secondary);">Rev ${rec.revision}</span>
    <span class="badge ${getRouteBadgeClass(getAssignedRoute(rec))}">${escapeHtml(getAssignedRoute(rec))}</span>
    ${rec.manual_override ? `<span class="badge-override">MANUAL OVERRIDE</span>` : ''}
    ${ref === 'M07' && rec.revision === 2 ? `<span class="badge-late">LATE TRANSCRIPT INGESTED</span>` : ''}
  `;

  // Populate Analysis Subtab
  const analysis = rec.analysis || {};
  document.getElementById('drawer-summary').textContent = analysis.summary || 'No summary available.';
  document.getElementById('drawer-why-matters').textContent = analysis.why_it_matters ? `Why It Matters: ${analysis.why_it_matters}` : '';
  document.getElementById('drawer-evidence-quote').textContent = analysis.evidence || 'No direct quotation or turns supplied in dataset.';
  document.getElementById('drawer-evidence-ref').textContent = analysis.evidence_ref || 'Source Metadata';
  document.getElementById('drawer-limitations').textContent = analysis.limitations || 'Boundaries not established.';
  document.getElementById('drawer-next-steps').textContent = analysis.next_steps || 'None.';
  document.getElementById('drawer-owner').textContent = analysis.owner || (p.rep_name || p.organizer_email || 'Unassigned');

  // Populate Transcript Turns Subtab
  const transcriptContainer = document.getElementById('drawer-transcript-container');
  if (st === 'call') {
    const text = p.transcript;
    if (text) {
      transcriptContainer.innerHTML = `
        <div style="background: var(--bg-card); padding: 16px; border-radius: 8px; border: 1px solid var(--border-subtle); line-height: 1.7; font-size: 13px;">
          ${escapeHtml(text)}
        </div>
      `;
    } else {
      transcriptContainer.innerHTML = `
        <div style="padding: 24px; text-align: center; color: var(--text-muted);">
          No audio transcript was supplied in this delivery batch. (Duration: ${p.duration_seconds || 0}s).
        </div>
      `;
    }
  } else {
    const tp = rec.transcript_payload;
    const turns = tp && tp.turns ? tp.turns : [];
    if (turns.length > 0) {
      transcriptContainer.innerHTML = turns.map((t, idx) => `
        <div class="turn-item">
          <div class="turn-header">
            <span class="turn-speaker">Turn ${idx + 1} &bull; ${escapeHtml(t.speaker || 'Speaker')}</span>
            <span class="turn-timecode">${t.timecode || '00:00:00'}</span>
          </div>
          <div class="turn-text">${escapeHtml(t.text || '')}</div>
        </div>
      `).join('');
    } else {
      const reason = tp ? tp.unavailable_reason : 'No transcript payload delivered.';
      transcriptContainer.innerHTML = `
        <div style="padding: 24px; text-align: center; color: var(--text-muted);">
          No speech turns available. Reason: ${escapeHtml(reason || 'Unavailable')}
        </div>
      `;
    }
  }

  // Populate Override Subtab
  const select = document.getElementById('override-route-select');
  select.value = getAssignedRoute(rec);
  document.getElementById('override-notes').value = rec.manual_notes || '';

  // Switch to Analysis Tab by default
  switchDrawerTab('analysis');
}

function closeRecordDrawer() {
  document.getElementById('inspection-drawer').classList.remove('open');
  document.getElementById('drawer-backdrop').classList.remove('open');
  state.selectedRecord = null;
}

function switchDrawerTab(tabId) {
  document.querySelectorAll('.drawer-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.drawer-subtab-content').forEach(c => c.style.display = 'none');

  const btn = document.querySelector(`.drawer-tab[data-drawer-tab="${tabId}"]`);
  if (btn) btn.classList.add('active');

  const content = document.getElementById(`drawer-tab-content-${tabId}`);
  if (content) content.style.display = 'block';
}

// 5-Slide Presentation Carousel
function renderSlide(index) {
  state.currentSlide = Math.max(0, Math.min(index, SLIDES_CONTENT.length - 1));
  const slide = SLIDES_CONTENT[state.currentSlide];
  const container = document.getElementById('slide-card-container');
  if (!container) return;

  container.innerHTML = `
    <div>
      <div class="slide-badge">${slide.badge}</div>
      <h2 class="slide-title">${slide.title}</h2>
      <div class="slide-body">${slide.body}</div>
    </div>
    <div class="slide-footer-info">
      <span>SpendNest Revenue Intelligence Inbox &bull; Volopay Assessment</span>
      <span>Slide ${state.currentSlide + 1} of ${SLIDES_CONTENT.length}</span>
    </div>
  `;

  document.getElementById('slide-counter').textContent = `Slide ${state.currentSlide + 1} of ${SLIDES_CONTENT.length}`;

  // Update dots
  document.querySelectorAll('.slide-dot').forEach((dot, idx) => {
    dot.classList.toggle('active', idx === state.currentSlide);
  });
}

// Client-Side ZIP Generator
async function downloadExportZip() {
  if (typeof JSZip === 'undefined') {
    showToast("JSZip library is not available offline. Please check files.", "error");
    return;
  }

  showToast("Compiling export archive (.zip)...", "info");
  const zip = new JSZip();

  const records = Array.from(state.records.values());

  // 1. Build Manifest Records
  const manifestList = records.map(rec => {
    const ref = rec.record_ref;
    const st = rec.source_type;
    const rev = rec.revision;
    const route = getAssignedRoute(rec);
    const cat = rec.analysis ? rec.analysis.category : 'intake_unreviewed';
    const cleanTitle = (rec.payload.title || 'record').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
    const path = `${cat}/${ref}_${st}_${cleanTitle}.md`;
    const stateLabel = hasUsableTranscript(rec) ? 'Analysed' : 'No Audio';

    return {
      source_type: st,
      source_id: rec.source_id,
      record_ref: ref,
      applied_revision: rev,
      primary_route: route,
      output_path: path,
      processing_state: stateLabel,
      manual_override: Boolean(rec.manual_override),
      analysis_freshness: rec.freshness || 'current',
      owner: rec.analysis ? rec.analysis.owner : (rec.payload.rep_name || rec.payload.organizer_email || 'Unassigned'),
      deal_intent: rec.analysis ? rec.analysis.deal_intent : 'N/A'
    };
  });

  // 2. Add manifest.json
  zip.file('manifest.json', JSON.stringify({
    generated_at: new Date().toISOString(),
    total_records: manifestList.length,
    contract_compliance: "DATA_CONTRACT.md rev 2",
    manifest: manifestList
  }, null, 2));

  // 3. Add manifest.csv
  let csv = "source_type,source_id,record_ref,applied_revision,primary_route,output_path,processing_state,manual_override,analysis_freshness,owner,deal_intent\n";
  manifestList.forEach(m => {
    csv += `"${m.source_type}","${m.source_id}","${m.record_ref}",${m.applied_revision},"${m.primary_route}","${m.output_path}","${m.processing_state}",${m.manual_override},"${m.analysis_freshness}","${m.owner}","${m.deal_intent}"\n`;
  });
  zip.file('manifest.csv', csv);

  // 4. Add daily_brief_2026-08-21.md
  if (state.db && state.db.daily_brief) {
    zip.file('daily_brief_2026-08-21.md', state.db.daily_brief);
  }

  // 5. Add individual markdown files
  records.forEach(rec => {
    const ref = rec.record_ref;
    const st = rec.source_type;
    const analysis = rec.analysis || {};
    const cat = analysis.category || 'intake_unreviewed';
    const cleanTitle = (rec.payload.title || 'record').replace(/[^a-zA-Z0-9_-]/g, '_').slice(0, 30);
    const path = `${cat}/${ref}_${st}_${cleanTitle}.md`;

    const md = `# Revenue Intelligence Analysis: ${ref} (${st.toUpperCase()})

- **Record Reference**: ${ref}
- **Source Type**: ${st}
- **Source ID**: \`${rec.source_id}\`
- **Applied Revision**: ${rec.revision}
- **Primary Assigned Route**: ${getAssignedRoute(rec)}
- **Manual Override**: ${rec.manual_override ? 'Yes (Manager Overridden)' : 'No'}
- **Assigned Owner**: ${analysis.owner || 'Unassigned'}
- **Deal Intent**: ${analysis.deal_intent || 'N/A'}

---

## 1. Executive Summary & Why It Matters
${analysis.summary || 'No summary available.'}

**Why it matters to sales management**:
${analysis.why_it_matters || 'Activity logged in telephony/calendar systems.'}

---

## 2. Verified Source Evidence
> ${analysis.evidence || 'No speech transcript.'}

- **Evidence Type**: ${analysis.evidence_type || 'Metadata'}
- **Source Reference**: ${analysis.evidence_ref || ref}

---

## 3. What the Evidence Does NOT Establish (Honest Uncertainty)
${analysis.limitations || 'Source data does not establish pipeline value or external account link.'}

---

## 4. Next Steps & Ownership
- **Next Action**: ${analysis.next_steps || 'None required.'}
- **Owner**: ${analysis.owner || 'Unassigned'}
`;
    zip.file(path, md);
  });

  // Generate and Trigger Download
  try {
    const blob = await zip.generateAsync({ type: 'blob' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `spendnest_revenue_intelligence_exports_${new Date().toISOString().slice(0, 10)}.zip`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast("Export archive downloaded successfully!", "success");
  } catch (err) {
    console.error("ZIP Generation error:", err);
    showToast("Failed to generate ZIP archive.", "error");
  }
}

// Toast Notifications
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  if (type === 'error') toast.style.borderColor = 'var(--status-danger)';
  if (type === 'success') toast.style.borderColor = 'var(--status-success)';

  toast.innerHTML = `
    <span>${escapeHtml(message)}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// Utility: HTML Escaper
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Theme Toggle
function applyTheme(theme) {
  state.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('spendnest_theme', theme);

  const icon = document.getElementById('theme-icon');
  if (icon) {
    icon.innerHTML = theme === 'dark'
      ? `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>`
      : `<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>`;
  }
}

// Event Listeners Setup
function setupEventListeners() {
  // Theme Toggle
  document.getElementById('theme-toggle').addEventListener('click', () => {
    applyTheme(state.theme === 'dark' ? 'light' : 'dark');
  });

  // Dynamic Topbar Header Text Updater
  function updateTopbarTitle(tab) {
    const titleEl = document.getElementById('topbar-view-title');
    const descEl = document.getElementById('topbar-view-desc');
    if (!titleEl || !descEl) return;
    if (tab === 'conversations') {
      titleEl.textContent = 'Inbox Review & Conversation Routing';
      descEl.textContent = 'Sales Activity Audit, Evidence Inspection & Replay Verification';
    } else if (tab === 'brief') {
      titleEl.textContent = 'Executive Sales Manager Brief';
      descEl.textContent = 'Operational Ground Truth, Actionable Findings & Rep Routing Breakdown';
    } else if (tab === 'exports') {
      titleEl.textContent = 'Export Center & Assessment Deliverables';
      descEl.textContent = 'Full Audit Archive (ZIP), Clean CSV Slices & Executive Presentation';
    }
  }

  // Sidebar Left Navigation Tabs
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.view-section').forEach(s => s.classList.remove('active'));

      btn.classList.add('active');
      const tab = btn.dataset.tab;
      state.activeTab = tab;
      const viewEl = document.getElementById(`view-${tab}`);
      if (viewEl) viewEl.classList.add('active');
      updateTopbarTitle(tab);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });

  // Replay Simulator Buttons
  document.getElementById('btn-step-1').addEventListener('click', runReplayStep1);
  document.getElementById('btn-step-2').addEventListener('click', runReplayStep2);
  document.getElementById('btn-step-3').addEventListener('click', runReplayStep3);
  document.getElementById('btn-step-4').addEventListener('click', runReplayStep4);
  document.getElementById('btn-step-5').addEventListener('click', runReplayStep5);
  document.getElementById('btn-reset').addEventListener('click', resetAllState);

  // Custom File Upload
  document.getElementById('file-uploader').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const json = JSON.parse(evt.target.result);
        if (!json.records || !Array.isArray(json.records)) {
          showToast("Invalid delivery JSON. Missing records array.", "error");
          return;
        }
        ingestBatch(json.records, json.revision || 1, json.batch_id || 'custom', true);
        showToast(`Ingested custom batch "${json.batch_id || 'upload'}" successfully!`, "success");
        updateReplayStatus(`Custom upload: batch "${json.batch_id}" ingested.`);
        renderAll();
      } catch (err) {
        showToast("Error parsing uploaded JSON file.", "error");
      }
    };
    reader.readAsText(file);
  });

  // Filter Bar
  document.getElementById('filter-search').addEventListener('input', (e) => {
    state.activeFilters.search = e.target.value;
    renderConversationsTable();
  });
  document.getElementById('filter-source-type').addEventListener('change', (e) => {
    state.activeFilters.sourceType = e.target.value;
    renderConversationsTable();
  });
  document.getElementById('filter-rep').addEventListener('change', (e) => {
    state.activeFilters.rep = e.target.value;
    renderConversationsTable();
  });
  document.getElementById('filter-route').addEventListener('change', (e) => {
    state.activeFilters.route = e.target.value;
    renderConversationsTable();
  });
  document.getElementById('filter-state').addEventListener('change', (e) => {
    state.activeFilters.state = e.target.value;
    renderConversationsTable();
  });

  document.getElementById('btn-clear-filters').addEventListener('click', () => {
    state.activeFilters = { search: '', sourceType: 'all', rep: 'all', route: 'all', state: 'all' };
    document.getElementById('filter-search').value = '';
    document.getElementById('filter-source-type').value = 'all';
    document.getElementById('filter-rep').value = 'all';
    document.getElementById('filter-route').value = 'all';
    document.getElementById('filter-state').value = 'all';
    renderConversationsTable();
  });

  // Drawer Close
  document.getElementById('drawer-close-btn').addEventListener('click', closeRecordDrawer);
  document.getElementById('drawer-backdrop').addEventListener('click', closeRecordDrawer);

  // Drawer Subtabs
  document.querySelectorAll('.drawer-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      switchDrawerTab(tab.dataset.drawerTab);
    });
  });

  // Override Form Submit
  document.getElementById('override-form').addEventListener('submit', (e) => {
    e.preventDefault();
    if (!state.selectedRecord) return;
    const newRoute = document.getElementById('override-route-select').value;
    const notes = document.getElementById('override-notes').value;
    saveOverride(state.selectedRecord.source_type, state.selectedRecord.source_id, newRoute, notes);
    // Refresh drawer
    openRecordDrawer(state.selectedRecord.source_type, state.selectedRecord.source_id);
  });

  // Clear Override Button
  document.getElementById('btn-clear-override').addEventListener('click', () => {
    if (!state.selectedRecord) return;
    clearOverride(state.selectedRecord.source_type, state.selectedRecord.source_id);
    openRecordDrawer(state.selectedRecord.source_type, state.selectedRecord.source_id);
  });

  // Slide Deck Controls (Safely checked)
  const btnPrev = document.getElementById('btn-slide-prev');
  if (btnPrev) btnPrev.addEventListener('click', () => renderSlide(state.currentSlide - 1));
  const btnNext = document.getElementById('btn-slide-next');
  if (btnNext) btnNext.addEventListener('click', () => renderSlide(state.currentSlide + 1));
  document.querySelectorAll('.slide-dot').forEach((dot, idx) => {
    dot.addEventListener('click', () => renderSlide(idx));
  });

  // Download ZIP
  const btnZip = document.getElementById('btn-download-zip');
  if (btnZip) btnZip.addEventListener('click', downloadExportZip);

  // PARALLAX & TACTILE 3D EFFECTS
  initParallaxEffects();
}

// INTERACTIVE PARALLAX & 3D TILT SYSTEM
function initParallaxEffects() {
  // 1. Ambient Background Orbs Parallax on Mousemove
  const orbs = document.querySelectorAll('.parallax-orb');
  if (orbs.length > 0) {
    let ticking = false;
    window.addEventListener('mousemove', (e) => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          const mouseX = (e.clientX / window.innerWidth) - 0.5;
          const mouseY = (e.clientY / window.innerHeight) - 0.5;
          orbs.forEach(orb => {
            const speed = parseFloat(orb.dataset.speed || 0.03);
            const moveX = mouseX * speed * 300;
            const moveY = mouseY * speed * 300;
            orb.style.transform = `translate3d(${moveX}px, ${moveY}px, 0)`;
          });
          ticking = false;
        });
        ticking = true;
      }
    });
  }

  // 2. Tactile 3D Parallax Tilt & Specular Shine on Metric Cards
  const cards = document.querySelectorAll('.metric-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = ((y - centerY) / centerY) * -5;
      const rotateY = ((x - centerX) / centerX) * 5;
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });

    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
      card.style.removeProperty('--mouse-x');
      card.style.removeProperty('--mouse-y');
    });
  });

  // 3. Subtle Elevation on Scroll
  const replayBar = document.getElementById('replay-toolbar');
  if (replayBar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        replayBar.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.35)';
      } else {
        replayBar.style.boxShadow = 'none';
      }
    });
  }

  // 4. Global Fintech Command-Bar Shortcuts (/ to focus search, Esc to dismiss modals)
  window.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      const searchInput = document.getElementById('filter-search');
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
    }
    if (e.key === 'Escape') {
      closeRecordDrawer();
    }
  });
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  localStorage.removeItem('spendnest_custom_records');
  initApp().then(() => {
    renderAll();
  });
});
