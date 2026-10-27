# scripts/patch_tala_studio_sound.py
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        <!-- TAB PANEL 4: TALA & METRONOME STUDIO -->
        <div class="studio-tab-panel is-hidden" id="tab-panel-tala" role="tabpanel" aria-labelledby="tab-btn-tala">
          <div class="tala-studio-header">
            <span class="tala-studio-badge">RHYTHM &amp; METER ENGINE</span>
            <h3 class="tala-studio-title">Tala, Laya &amp; Tabla Metronome Workspace</h3>
            <p class="tala-studio-sub">
              Master classical rhythm with authentic synthesized tabla bols, visual matra cycles, Sam/Khali markers, and live tempo detection.
            </p>
          </div>

          <div class="tala-studio-card" data-ui="tala-studio">
<!-- Interactive Tala & Laya Metronome Grid -->
              <div class="ui-tala-container">
                <div class="ui-tala-header">
                  <div class="ui-tala-select-group">
                    <label for="ui-tala-select" class="ui-tala-label">Tala Cycle</label>
                    <select id="ui-tala-select" class="ui-tala-select">
                      <option value="teentaal">Teentaal (16 Matras · 4+4+4+4)</option>
                      <option value="jhaptal">Jhaptal (10 Matras · 2+3+2+3)</option>
                      <option value="rupak">Rupak (7 Matras · 3+2+2)</option>
                      <option value="keharwa">Keharwa (8 Matras · 4+4)</option>
                      <option value="dadra">Dadra (6 Matras · 3+3)</option>
                      <option value="aditala">Adi Tala (8 Aksharas · 4+2+2)</option>
                    </select>
                  </div>
                  <div class="ui-tempo-group">
                    <label for="ui-tempo-slider" class="ui-tala-label">Laya Tempo: <span id="ui-tempo-val">84 BPM</span></label>
                    <input type="range" id="ui-tempo-slider" min="40" max="220" value="84" class="ui-tempo-slider">
                  </div>
                  <button type="button" id="tala-toggle-btn" class="ui-tala-btn">Start Tala Metronome</button>
                </div>'''

replacement = '''        <!-- TAB PANEL 4: TALA & METRONOME STUDIO -->
        <div class="studio-tab-panel is-hidden" id="tab-panel-tala" role="tabpanel" aria-labelledby="tab-btn-tala">
          <div class="tala-studio-header">
            <div class="tala-badge-row">
              <span class="tala-studio-badge">RHYTHM &amp; METER ENGINE</span>
              <span class="tala-persona-pill">Designed for: All Musicians · Percussionists, Vocalists &amp; Instrumentalists</span>
            </div>
            <h3 class="tala-studio-title">Tala, Laya &amp; Acoustic Tabla Metronome Workspace</h3>
            <p class="tala-studio-sub">
              Master classical rhythm with authentic physical-modeled tabla strokes (Bāyān &amp; Dāyān tuned to root Sa), Carnatic mridangam, visual matra cycles, and Sam/Khali markers.
            </p>
          </div>

          <div class="tala-studio-card" data-ui="tala-studio">
<!-- Interactive Tala & Laya Metronome Grid -->
              <div class="ui-tala-container">
                <div class="ui-tala-header">
                  <div class="ui-tala-select-group">
                    <label for="ui-tala-select" class="ui-tala-label">Tala Cycle</label>
                    <select id="ui-tala-select" class="ui-tala-select">
                      <option value="teentaal">Teentaal (16 Matras · 4+4+4+4)</option>
                      <option value="jhaptal">Jhaptal (10 Matras · 2+3+2+3)</option>
                      <option value="rupak">Rupak (7 Matras · 3+2+2)</option>
                      <option value="keharwa">Keharwa (8 Matras · 4+4)</option>
                      <option value="dadra">Dadra (6 Matras · 3+3)</option>
                      <option value="aditala">Adi Tala (8 Aksharas · 4+2+2)</option>
                    </select>
                  </div>
                  <div class="ui-tala-select-group">
                    <label for="ui-tala-sound-select" class="ui-tala-label">Sound Timbre</label>
                    <select id="ui-tala-sound-select" class="ui-tala-select">
                      <option value="tabla">Acoustic Tabla (Bāyān &amp; Dāyān tuned to Sa)</option>
                      <option value="mridangam">Carnatic Mridangam (Thoppi &amp; Valanthalai)</option>
                      <option value="woodblock">Studio Woodblock (Crisp Click)</option>
                      <option value="bell">Temple Bell / Ghanti (Meditative)</option>
                    </select>
                  </div>
                  <div class="ui-tempo-group">
                    <label for="ui-tempo-slider" class="ui-tala-label">Laya Tempo: <span id="ui-tempo-val">84 BPM · Madhya Laya</span></label>
                    <input type="range" id="ui-tempo-slider" min="40" max="220" value="84" class="ui-tempo-slider">
                  </div>
                  <div class="ui-tala-action-group">
                    <button type="button" id="tala-toggle-btn" class="ui-tala-btn">Start Tala Metronome</button>
                    <span id="tala-sa-tuning-pill" class="tala-tuning-pill" title="Physical Dāyān right-drum resonant pitch coupled directly to your active root Sa">Dāyān: Sa = 146.8 Hz</span>
                  </div>
                </div>'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
replacement_lf = replacement.replace('\r\n', '\n')

if target_lf in text_lf:
    new_text = text_lf.replace(target_lf, replacement_lf).replace('\n', '\r\n')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('SUCCESS: Patched index.html for Tala sound options!')
else:
    print('ERROR: Target string not found')
