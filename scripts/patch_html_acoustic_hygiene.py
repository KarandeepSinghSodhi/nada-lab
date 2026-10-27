from pathlib import Path

p = Path("index.html")
content = p.read_text(encoding="utf-8")
content_norm = content.replace("\r\n", "\n")

target = """              <span class="dossier-metric-val" id="dossier-accuracy-val">96.8%</span>
              <span class="dossier-metric-sub" id="dossier-notes-count">8 Notes Transcribed</span>
            </div>
          </div>

          <!-- INTERACTIVE SHEET MUSIC & LEAD SHEET WORKSTATION -->"""

replacement = """              <span class="dossier-metric-val" id="dossier-accuracy-val">96.8%</span>
              <span class="dossier-metric-sub" id="dossier-notes-count">8 Notes Transcribed</span>
            </div>
          </div>

          <!-- ACOUSTIC HYGIENE & VOCAL ISOLATION TELEMETRY -->
          <div class="dossier-hygiene-strip" data-ui="dossier-hygiene-strip">
            <div class="hygiene-chip">
              <span class="hygiene-chip-lbl">Vocal Isolation (HPSS)</span>
              <span class="hygiene-chip-val" id="dossier-vocal-isolation">99.1% · Pristine Lead Vocal</span>
            </div>
            <div class="hygiene-chip">
              <span class="hygiene-chip-lbl">Accompaniment Filter</span>
              <span class="hygiene-chip-val" id="dossier-bleed-filter">0.9% Tabla/Harmonium filtered</span>
            </div>
            <div class="hygiene-chip">
              <span class="hygiene-chip-lbl">Octave Jumps Repaired</span>
              <span class="hygiene-chip-val" id="dossier-octave-glitches">0 Fry Glitches Rectified</span>
            </div>
            <div class="hygiene-chip">
              <span class="hygiene-chip-lbl">Adaptive Laya &amp; Window</span>
              <span class="hygiene-chip-val" id="dossier-laya-window">Madhya · 110ms min swara</span>
            </div>
          </div>

          <!-- GHARANA & STYLISTIC PRESET SELECTOR -->
          <div class="dossier-stylistic-bar" data-ui="dossier-stylistic-bar">
            <span class="stylistic-bar-label">Gharana &amp; Stylistic Preset:</span>
            <div class="stylistic-btn-group" role="radiogroup" aria-label="Gharana and stylistic preset">
              <button type="button" class="stylistic-btn is-active" data-preset="khayal_standard" title="Khayal standard Gayaki with balanced ornamentation">Khayal Standard</button>
              <button type="button" class="stylistic-btn" data-preset="khayal_kirana" title="Kirana gharana: deep slow Andolan on Komal swaras &amp; long meends">Kirana (Andolan)</button>
              <button type="button" class="stylistic-btn" data-preset="khayal_gwalior" title="Gwalior gharana: crisp sthira swara landing &amp; structural precision">Gwalior (Sthira)</button>
              <button type="button" class="stylistic-btn" data-preset="thumri_light" title="Thumri / Ghazal: brisk kan touch inflections and rapid khatkas">Thumri (Kan &amp; Murki)</button>
              <button type="button" class="stylistic-btn" data-preset="dhrupad" title="Dhrupad: strict 22-shruti microtones, heavy gamaks, minimal vibrato">Dhrupad (Microtonal)</button>
              <button type="button" class="stylistic-btn" data-preset="drut_taan" title="Drut taans: high-speed 16th note runs (60ms window)">Drut Taan (Fast)</button>
            </div>
          </div>

          <!-- INTERACTIVE SHEET MUSIC & LEAD SHEET WORKSTATION -->"""

assert target in content_norm, "target not found"
content_norm = content_norm.replace(target, replacement, 1)

p.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Injected Acoustic Hygiene & Gharana bar into index.html")
