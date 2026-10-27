# Build tabbed index.html
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Locate boundaries
pipe_header_end = text.find('        <!-- 5-Panel Horizontal Accordion')
acc_start = pipe_header_end
acc_end = text.find('        <!-- Sādhanā Quick Status Bar')
sadhana_bar_start = acc_end
uploader_start = text.find('        <!-- UNIVERSAL 1-CLICK AUDIO TRACK UPLOADER -->')
dossier_start = text.find('        <!-- INSTANT TRACK INTELLIGENCE & COMPLETE REPORT CARD -->')
workbench_start = text.find('        <!-- THE LIVE THING: Interactive Phrase & Deficit Inspector -->')
pipeline_close = text.find('      </div>\n    </section>\n\n    <!-- CHAPTER 4: LIST')

# Extract components
accordion_html = text[acc_start:sadhana_bar_start].strip()
sadhana_bar_html = text[sadhana_bar_start:uploader_start].strip()
uploader_html = text[uploader_start:dossier_start].strip()
dossier_html = text[dossier_start:workbench_start].strip()

# Now extract inside workbench
wb_text = text[workbench_start:pipeline_close]

# In wb_text, find tala container
tala_start = wb_text.find('              <!-- Interactive Tala & Laya Metronome Grid -->')
tala_end = wb_text.find('            </div>\n\n            <div class="ui-diagnostic-pane">')
tala_html = wb_text[tala_start:tala_end].strip()

# In wb_text, find rasa panel
rasa_start = wb_text.find('              <!-- Real-Time Rasa & Emotion Radar (Valence-Arousal Affective Map) -->')
rasa_end = wb_text.find('              <dl class="ui-telemetry-grid">')
rasa_html = wb_text[rasa_start:rasa_end].strip()

# In wb_text, find analyst drawer
drawer_start = wb_text.find('              <button type="button" id="toggle-analyst-btn"')
# The drawer goes up to the end of diagnostic pane (before closing </div>\n          </div>\n        </div>)
drawer_end = wb_text.rfind('            </div>\n          </div>\n        </div>')
drawer_html = wb_text[drawer_start:drawer_end].strip()

# Clean workbench for Tab 1 (Sādhana): remove tala, rasa, and analyst drawer from it
clean_wb = wb_text[:tala_start] + wb_text[tala_end:rasa_start] + wb_text[rasa_end:drawer_start] + wb_text[drawer_end:]

# Build the 5 Studio Tab Navigation Bar
studio_tabs_nav = """        <!-- Musician Studio Workspaces Tab Bar -->
        <nav class="studio-tab-bar" role="tablist" aria-label="Musician Studio Workspaces" data-ui="studio-tabs">
          <button type="button" class="studio-tab is-active" role="tab" id="tab-btn-sadhana" aria-selected="true" data-tab-target="tab-panel-sadhana">
            <span class="studio-tab-badge">PRACTICE</span>
            <span class="studio-tab-label">S\u0101dhan\u0101 Studio</span>
          </button>
          <button type="button" class="studio-tab" role="tab" id="tab-btn-dossier" aria-selected="false" data-tab-target="tab-panel-dossier">
            <span class="studio-tab-badge">INTELLIGENCE</span>
            <span class="studio-tab-label">Track Dossier &amp; Notations</span>
          </button>
          <button type="button" class="studio-tab" role="tab" id="tab-btn-rasa" aria-selected="false" data-tab-target="tab-panel-rasa">
            <span class="studio-tab-badge">AESTHETICS</span>
            <span class="studio-tab-label">Rasa &amp; Emotion Lab</span>
          </button>
          <button type="button" class="studio-tab" role="tab" id="tab-btn-tala" aria-selected="false" data-tab-target="tab-panel-tala">
            <span class="studio-tab-badge">RHYTHM</span>
            <span class="studio-tab-label">Tala &amp; Metronome</span>
          </button>
          <button type="button" class="studio-tab" role="tab" id="tab-btn-research" aria-selected="false" data-tab-target="tab-panel-research">
            <span class="studio-tab-badge">RESEARCH</span>
            <span class="studio-tab-label">MIR Science &amp; RAG Lab</span>
          </button>
        </nav>"""

# TAB PANEL 1: SĀDHANA PRACTICE STUDIO
panel_sadhana = f"""        <!-- TAB PANEL 1: S\u0100DHAN\u0100 PRACTICE STUDIO -->
        <div class="studio-tab-panel is-active" id="tab-panel-sadhana" role="tabpanel" aria-labelledby="tab-btn-sadhana">
{sadhana_bar_html}

{clean_wb}
        </div>"""

# TAB PANEL 2: TRACK DOSSIER & NOTATIONS
panel_dossier = f"""        <!-- TAB PANEL 2: TRACK DOSSIER & NOTATIONS (1-CLICK UPLOADER) -->
        <div class="studio-tab-panel is-hidden" id="tab-panel-dossier" role="tabpanel" aria-labelledby="tab-btn-dossier">
{uploader_html}

{dossier_html}
        </div>"""

# TAB PANEL 3: PHRASE-LEVEL RASA & AESTHETIC EMOTION STUDIO
panel_rasa = f"""        <!-- TAB PANEL 3: RASA & AESTHETIC EMOTION STUDIO (PHRASE-LEVEL) -->
        <div class="studio-tab-panel is-hidden" id="tab-panel-rasa" role="tabpanel" aria-labelledby="tab-btn-rasa">
          <div class="rasa-studio-header">
            <span class="rasa-studio-badge">NAVARASA &amp; AESTHETIC MUSICOLOGY</span>
            <h3 class="rasa-studio-title">Phrase-Level Affective Contour &amp; Aesthetic Resonance</h3>
            <p class="rasa-studio-sub">
              Emotion in Indian Classical Music does not arise from an isolated note; it unfolds through the <em>chalan</em> (melodic movement), sustained <em>Nyasa</em> resting points, pitch velocity, and raga grammar.
            </p>
          </div>

          <div class="rasa-studio-grid" data-ui="rasa-studio">
            <!-- Left: Hero Rasa Card & Musicological Treatise Analysis -->
            <div class="rasa-hero-col">
              <div class="rasa-hero-card">
                <div class="rasa-hero-header">
                  <span class="rasa-hero-pill" id="rasa-primary-pill">Primary Rasa: Shanta (Peace)</span>
                  <span class="rasa-hero-secondary" id="rasa-secondary-pill">Secondary: Shringara (Devotion)</span>
                </div>
                <h4 class="rasa-hero-name" id="rasa-hero-name">Shanta Rasa \u00b7 \u0936\u093e\u0928\u094d\u0924 \u0930\u0938</h4>
                <p class="rasa-hero-desc" id="rasa-hero-desc">
                  Serenity, twilight contemplation, and devotional surrender. Grounded resting on Shadja (Sa) and Shuddha Gandhar (5/4) with zero kinetic jerk dissolves psychic restlessness.
                </p>
              </div>

              <div class="rasa-treatise-box">
                <span class="rasa-treatise-lbl">CANONICAL MUSICOLOGICAL CRITIQUE</span>
                <p class="rasa-treatise-text" id="rasa-treatise-text">
                  Bharata Muni's <em>Natya Shastra</em> and Sarangadeva's <em>Sangita Ratnakara</em> classify the unfolding contour and prolonged nyasa grounding as the definitive generators of authentic bhava.
                </p>
                <div class="rasa-treatise-citations" id="rasa-citations-row">
                  <span class="treatise-citation-chip">Natya Shastra, Ch. 29</span>
                  <span class="treatise-citation-chip">Sangita Ratnakara, Prakarana 7</span>
                  <span class="treatise-citation-chip">Brihaddeshi, Sloka 312</span>
                </div>
              </div>

              <!-- 4-Metric Kinematic & Nyasa Strip -->
              <div class="rasa-metrics-grid">
                <div class="rasa-kpi-cell">
                  <span class="rasa-kpi-lbl">Valence (Pleasure)</span>
                  <span class="rasa-kpi-val" id="rasa-kpi-valence">+0.68</span>
                  <span class="rasa-kpi-sub">Harmonic Consonance</span>
                </div>
                <div class="rasa-kpi-cell">
                  <span class="rasa-kpi-lbl">Arousal (Energy)</span>
                  <span class="rasa-kpi-val" id="rasa-kpi-arousal">0.36</span>
                  <span class="rasa-kpi-sub">Vilambit Meditation</span>
                </div>
                <div class="rasa-kpi-cell">
                  <span class="rasa-kpi-lbl">Kinetic Velocity</span>
                  <span class="rasa-kpi-val" id="rasa-kpi-velocity">142 c/s</span>
                  <span class="rasa-kpi-sub">Gentle Meend Glides</span>
                </div>
                <div class="rasa-kpi-cell">
                  <span class="rasa-kpi-lbl">Sustained Nyasa</span>
                  <span class="rasa-kpi-val" id="rasa-kpi-nyasa">Ga, Pa, Sa</span>
                  <span class="rasa-kpi-sub">Resting Swaras</span>
                </div>
              </div>
            </div>

            <!-- Right: 2D Circumplex Valence vs Arousal Radar Canvas -->
            <div class="rasa-radar-col">
              <div class="rasa-canvas-card">
                <div class="rasa-canvas-header">
                  <span class="rasa-canvas-title">2D Valence-Arousal Affective Map</span>
                  <span class="rasa-quadrant-badge" id="rasa-quadrant-badge">Serene / Contemplative (4th Quadrant)</span>
                </div>
                <div class="rasa-canvas-wrap">
                  <canvas id="rasa-radar-canvas" width="460" height="260" aria-label="Real-time 2D Valence and Arousal emotional circumplex map showing Navarasa aesthetic zones"></canvas>
                </div>
                <div class="rasa-canvas-legend">
                  <span class="rasa-zone-tag zone-shanta">Shanta (Peace)</span>
                  <span class="rasa-zone-tag zone-karuna">Karuna (Pathos)</span>
                  <span class="rasa-zone-tag zone-veera">Veera (Heroism)</span>
                  <span class="rasa-zone-tag zone-shringara">Shringara (Devotion)</span>
                </div>
              </div>
            </div>
          </div>
        </div>"""

# TAB PANEL 4: TALA & METRONOME STUDIO
panel_tala = f"""        <!-- TAB PANEL 4: TALA & METRONOME STUDIO -->
        <div class="studio-tab-panel is-hidden" id="tab-panel-tala" role="tabpanel" aria-labelledby="tab-btn-tala">
          <div class="tala-studio-header">
            <span class="tala-studio-badge">RHYTHM &amp; METER ENGINE</span>
            <h3 class="tala-studio-title">Tala, Laya &amp; Tabla Metronome Workspace</h3>
            <p class="tala-studio-sub">
              Master classical rhythm with authentic synthesized tabla bols, visual matra cycles, Sam/Khali markers, and live tempo detection.
            </p>
          </div>

          <div class="tala-studio-card" data-ui="tala-studio">
{tala_html}
          </div>
        </div>"""

# TAB PANEL 5: MIR RESEARCH & RAG LAB (RAG IS HIDDEN HERE!)
# Note: remove the <div id="analyst-drawer" class="analyst-drawer is-hidden"> wrapper so it is permanently visible inside its own research tab!
cleaned_drawer = drawer_html.replace('class="analyst-drawer is-hidden"', 'class="analyst-drawer"').replace('<button type="button" id="toggle-analyst-btn" class="ui-analyst-btn">Open AI Classical Analyst Breakdown</button>', '')

panel_research = f"""        <!-- TAB PANEL 5: MIR RESEARCH & RAG LAB (RAG HIDDEN AWAY HERE) -->
        <div class="studio-tab-panel is-hidden" id="tab-panel-research" role="tabpanel" aria-labelledby="tab-btn-research">
          <div class="research-studio-header">
            <span class="research-studio-badge">COMPUTATIONAL MUSICOLOGY &amp; LITERATURE</span>
            <h3 class="research-studio-title">Raga Knowledge Graph, MIR Science &amp; RAG Lab</h3>
            <p class="research-studio-sub">
              Scholarly research engine backed by 672 indexed musicology papers, 56-raga confusion matrices, algorithmic alankars, and continuous pitch bend MIDI export.
            </p>
          </div>

          <div class="research-studio-card" data-ui="research-lab">
{cleaned_drawer}
          </div>
        </div>"""

# Assemble new pipeline content
new_pipeline_body = f"""
{accordion_html}

{studio_tabs_nav}

{panel_sadhana}

{panel_dossier}

{panel_rasa}

{panel_tala}

{panel_research}
"""

new_html = text[:pipe_header_end] + new_pipeline_body + text[pipeline_close:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Successfully generated tabbed index.html!")
