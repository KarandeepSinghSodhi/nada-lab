# scripts/patch_heatmap_and_raga_listeners.py

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_html = '''              <canvas id="shruti-canvas" width="920" height="280" aria-label="Continuous pitch trajectory C(t) and velocity derivative dC/dt plotted across rational shruti horizontals"></canvas>
              <div class="ui-scrubber-row">'''

replacement_html = '''              <canvas id="shruti-canvas" width="920" height="280" aria-label="Continuous pitch trajectory C(t) and velocity derivative dC/dt plotted across rational shruti horizontals"></canvas>
              
              <!-- Interactive Intonation Error Heatmap Ribbon -->
              <div class="ui-heatmap-container" data-ui="error-heatmap">
                <div class="heatmap-header">
                  <span class="heatmap-title">INTONATION ERROR HEATMAP · CLICK HOTSPOT TO JUMP</span>
                  <div class="heatmap-legend">
                    <span class="legend-chip legend-green">&lt;15c Pure</span>
                    <span class="legend-chip legend-yellow">15-30c Drift</span>
                    <span class="legend-chip legend-red">&gt;30c Deficit</span>
                  </div>
                </div>
                <div class="ui-heatmap-strip" id="ui-heatmap-strip" role="slider" aria-label="Timeline deviation heatmap" tabindex="0"></div>
              </div>

              <div class="ui-scrubber-row">'''

if target_html in html and 'ui-heatmap-container' not in html:
    html = html.replace(target_html, replacement_html, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html with Intonation Heatmap Strip.")
else:
    print("Heatmap already present or target not found.")

# 2. Append styles to styles.css
heatmap_css = '''
/* Intonation Error Heatmap Ribbon */
.ui-heatmap-container {
  background: rgba(18, 18, 20, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 4px;
  padding: 6px 10px;
  margin-top: 6px;
  margin-bottom: 6px;
}

.heatmap-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 5px;
}

.heatmap-title {
  font-size: 9px;
  font-weight: 600;
  color: #a1a1aa;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.heatmap-legend {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-chip {
  font-size: 9px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 3px;
}

.legend-chip::before {
  content: "";
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.legend-green {
  color: #86efac;
}
.legend-green::before {
  background: #22c55e;
}

.legend-yellow {
  color: #fde047;
}
.legend-yellow::before {
  background: #eab308;
}

.legend-red {
  color: #fca5a5;
}
.legend-red::before {
  background: #ef4444;
}

.ui-heatmap-strip {
  display: flex;
  height: 12px;
  width: 100%;
  border-radius: 2px;
  overflow: hidden;
  cursor: pointer;
  background: #27272a;
}

.heatmap-cell {
  flex: 1;
  height: 100%;
  transition: opacity 0.1s ease;
}

.heatmap-cell:hover {
  opacity: 0.75;
  transform: scaleY(1.3);
}

.heatmap-cell.is-current {
  outline: 2px solid #fff;
  z-index: 2;
}
'''

with open('styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

if '.ui-heatmap-container' not in css:
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css.rstrip() + '\n' + heatmap_css + '\n')
    print("Appended heatmap styles to styles.css.")
