# scripts/patch_ab_looper.py
import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_html = '''              <div class="ui-scrubber-row">
                <label for="phrase-scrubber" class="ui-scrub-label">Scrub Trajectory Frame (10 ms hop)</label>
                <input type="range" id="phrase-scrubber" min="0" max="100" value="42" class="ui-scrubber">
                <span id="ui-ornament-tag" class="ui-ornament-pill">Detected: Meend (412 c/s)</span>
              </div>'''

replacement_html = '''              <div class="ui-scrubber-row">
                <label for="phrase-scrubber" class="ui-scrub-label">Scrub Trajectory Frame (10 ms hop)</label>
                <input type="range" id="phrase-scrubber" min="0" max="100" value="42" class="ui-scrubber">
                <span id="ui-ornament-tag" class="ui-ornament-pill">Detected: Meend (412 c/s)</span>
              </div>

              <!-- A-B Practice Looper & Variable Speed Riyaz Controller -->
              <div class="ui-ab-looper-bar" data-ui="ab-looper">
                <div class="ab-looper-points">
                  <button type="button" id="btn-set-loop-a" class="ab-btn" title="Set loop start point A to current scrubber position">
                    [A] <span id="loop-a-val">0.0s</span>
                  </button>
                  <button type="button" id="btn-set-loop-b" class="ab-btn" title="Set loop end point B to current scrubber position">
                    [B] <span id="loop-b-val">2.2s</span>
                  </button>
                  <button type="button" id="btn-toggle-loop" class="ab-btn ab-loop-btn" title="Toggle continuous A-B phrase looping for intensive practice">
                    🔁 Loop A-B
                  </button>
                </div>
                <div class="ab-looper-speed-group" role="radiogroup" aria-label="Practice Playback Speed">
                  <span class="ab-speed-label">Speed:</span>
                  <button type="button" class="ab-speed-btn" data-speed="0.5" title="50% Speed (Slow Practice / Vilambit)">0.5x</button>
                  <button type="button" class="ab-speed-btn" data-speed="0.75" title="75% Speed (Medium Practice / Madhya)">0.75x</button>
                  <button type="button" class="ab-speed-btn is-active" data-speed="1.0" title="100% Speed (Performance Speed / Drut)">1.0x</button>
                </div>
              </div>'''

if target_html in html:
    html = html.replace(target_html, replacement_html, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html with A-B Looper controls.")
else:
    print("target_html not found in index.html")

# 2. Append styles to styles.css
looper_css = '''
/* A-B Practice Looper & Variable Speed Bar */
.ui-ab-looper-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  background: rgba(24, 24, 27, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 8px 12px;
  margin-top: 8px;
}

.ab-looper-points {
  display: flex;
  align-items: center;
  gap: 6px;
}

.ab-btn {
  background: #27272a;
  color: #e4e4e7;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 3px;
  font-family: inherit;
  font-size: 11px;
  font-weight: 500;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.ab-btn:hover {
  background: #3f3f46;
  border-color: rgba(255, 255, 255, 0.25);
}

.ab-btn.ab-loop-btn {
  background: #1e3a2b;
  color: #86efac;
  border-color: rgba(134, 239, 172, 0.3);
}

.ab-btn.ab-loop-btn:hover {
  background: #274d39;
  border-color: rgba(134, 239, 172, 0.5);
}

.ab-btn.ab-loop-btn.is-looping {
  background: #14532d;
  color: #4ade80;
  border-color: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.3);
}

.ab-looper-speed-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.ab-speed-label {
  font-size: 11px;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-right: 4px;
}

.ab-speed-btn {
  background: transparent;
  color: #a1a1aa;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  font-family: inherit;
  font-size: 11px;
  padding: 4px 8px;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.ab-speed-btn:hover {
  background: #27272a;
  color: #f4f4f5;
}

.ab-speed-btn.is-active {
  background: #3f3f46;
  color: #f4f4f5;
  border-color: #71717a;
  font-weight: 600;
}

/* Loop this Meend Button in Transition Bridge */
.sheet-loop-meend-btn {
  display: inline-block;
  background: rgba(34, 197, 94, 0.15);
  color: #86efac;
  border: 1px solid rgba(134, 239, 172, 0.3);
  border-radius: 2px;
  font-size: 9px;
  padding: 1px 5px;
  margin-top: 3px;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.sheet-loop-meend-btn:hover {
  background: rgba(34, 197, 94, 0.35);
  color: #fff;
}
'''

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.ui-ab-looper-bar' not in css:
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css.rstrip() + '\n' + looper_css + '\n')
    print("Appended looper styles to styles.css.")
else:
    print("Looper styles already present in styles.css.")
