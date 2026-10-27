# scripts/patch_riyaz_scorecard.py

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Tala Sync button to ab-looper-points
looper_target = '''                  <button type="button" id="btn-toggle-loop" class="ab-btn ab-loop-btn" title="Toggle continuous A-B phrase looping for intensive practice">
                    🔁 Loop A-B
                  </button>'''

looper_replacement = '''                  <button type="button" id="btn-toggle-loop" class="ab-btn ab-loop-btn" title="Toggle continuous A-B phrase looping for intensive practice">
                    🔁 Loop A-B
                  </button>
                  <button type="button" id="btn-sync-tala-metronome" class="ab-btn ab-tala-btn" title="Synchronize authentic acoustic Tala metronome with phrase playback">
                    ⏱️ Tala: OFF
                  </button>'''

if looper_target in html and 'btn-sync-tala-metronome' not in html:
    html = html.replace(looper_target, looper_replacement, 1)

# Add Riyaz Scorecard HUD below ui-drill-box
drill_target = '''              <div class="ui-drill-box">
                <p class="ui-drill-heading">Prescribed Vocal Drill</p>
                <p id="ui-drill-text" class="ui-drill-body">
                  Sustain Ni (1088.3c) on the tanpura breath, then execute a slow 650 ms glide into Re (203.9c) while keeping throat resonance open across Sa.
                </p>
              </div>'''

scorecard_html = '''              <div class="ui-drill-box">
                <p class="ui-drill-heading">Prescribed Vocal Drill</p>
                <p id="ui-drill-text" class="ui-drill-body">
                  Sustain Ni (1088.3c) on the tanpura breath, then execute a slow 650 ms glide into Re (203.9c) while keeping throat resonance open across Sa.
                </p>
              </div>

              <!-- Riyaz Mastery Scorecard & Multi-Take Progression -->
              <div class="ui-riyaz-scorecard" data-ui="riyaz-scorecard">
                <div class="scorecard-header">
                  <div class="scorecard-badge-row">
                    <span class="scorecard-badge">RIYAZ MASTERY HUD</span>
                    <span class="scorecard-grade" id="riyaz-grade-badge">A+ · Master</span>
                  </div>
                  <span class="scorecard-take-count" id="riyaz-take-label">Take #1 · Benchmark</span>
                </div>

                <div class="scorecard-metrics-grid">
                  <div class="scorecard-cell">
                    <span class="scorecard-lbl">Shruti Precision</span>
                    <span class="scorecard-val" id="metric-shruti-prec">94.8%</span>
                    <span class="scorecard-sub">±15c Rational Ratio</span>
                  </div>
                  <div class="scorecard-cell">
                    <span class="scorecard-lbl">Sthirata (Stability)</span>
                    <span class="scorecard-val" id="metric-sthirata">91.2%</span>
                    <span class="scorecard-sub">&lt;6c Sustained Jitter</span>
                  </div>
                  <div class="scorecard-cell">
                    <span class="scorecard-lbl">Meend Fluidity</span>
                    <span class="scorecard-val" id="metric-meend-fluid">96.0%</span>
                    <span class="scorecard-sub">C² Continuous Kinematics</span>
                  </div>
                  <div class="scorecard-cell">
                    <span class="scorecard-lbl">Laya &amp; Rhythm</span>
                    <span class="scorecard-val" id="metric-laya-sync">92.5%</span>
                    <span class="scorecard-sub">Matra Temporal Lock</span>
                  </div>
                </div>

                <!-- Progressive Take History Strip -->
                <div class="scorecard-history-strip" id="riyaz-history-strip">
                  <span class="history-strip-title">Take History:</span>
                  <div class="history-chips" id="riyaz-history-chips">
                    <span class="history-chip is-active" data-take="1">Take 1: 94%</span>
                  </div>
                  <span class="history-delta-badge" id="riyaz-delta-badge">+0.0% Baseline</span>
                </div>
              </div>'''

if drill_target in html and 'ui-riyaz-scorecard' not in html:
    html = html.replace(drill_target, scorecard_html, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html with Riyaz Scorecard HUD and Tala Sync button.")

# 2. Append styles to styles.css
scorecard_css = '''
/* Riyaz Mastery Scorecard & Multi-Take Progression */
.ui-riyaz-scorecard {
  background: rgba(18, 18, 20, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 12px 14px;
  margin-top: 10px;
}

.scorecard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.scorecard-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.scorecard-badge {
  font-size: 10px;
  font-weight: 600;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.scorecard-grade {
  font-size: 11px;
  font-weight: 700;
  color: #4ade80;
  background: rgba(74, 222, 128, 0.12);
  border: 1px solid rgba(74, 222, 128, 0.3);
  padding: 2px 7px;
  border-radius: 3px;
}

.scorecard-take-count {
  font-size: 11px;
  color: #71717a;
}

.scorecard-metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-bottom: 10px;
}

@media (max-width: 640px) {
  .scorecard-metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.scorecard-cell {
  background: rgba(39, 39, 42, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 3px;
  padding: 6px 8px;
  display: flex;
  flex-direction: column;
}

.scorecard-lbl {
  font-size: 10px;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 2px;
}

.scorecard-val {
  font-size: 15px;
  font-weight: 700;
  color: #f4f4f5;
  font-family: inherit;
}

.scorecard-sub {
  font-size: 9px;
  color: #71717a;
  margin-top: 1px;
}

.scorecard-history-strip {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.history-strip-title {
  font-size: 10px;
  color: #71717a;
  text-transform: uppercase;
}

.history-chips {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-wrap: wrap;
}

.history-chip {
  font-size: 10px;
  padding: 2px 7px;
  border-radius: 3px;
  background: #27272a;
  color: #d4d4d8;
  border: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.history-chip:hover {
  background: #3f3f46;
  color: #fff;
}

.history-chip.is-active {
  background: #14532d;
  color: #86efac;
  border-color: #22c55e;
}

.history-delta-badge {
  font-size: 10px;
  font-weight: 600;
  color: #22c55e;
  background: rgba(34, 197, 94, 0.12);
  padding: 2px 6px;
  border-radius: 3px;
  margin-left: auto;
}

/* Tala Sync Button in Looper */
.ab-btn.ab-tala-btn.is-active {
  background: #432b12;
  color: #fde047;
  border-color: #eab308;
}
'''

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.ui-riyaz-scorecard' not in css:
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css.rstrip() + '\n' + scorecard_css + '\n')
    print("Appended Riyaz Scorecard styles to styles.css.")
