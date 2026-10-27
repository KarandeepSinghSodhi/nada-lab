# scripts/patch_wave_musician_html.py

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''                  <canvas id="acoustic-wave-canvas" width="920" height="74" aria-label="Real-time acoustic sound wave oscilloscope"></canvas>
                </div>'''

replacement = '''                  <canvas id="acoustic-wave-canvas" width="920" height="74" aria-label="Real-time acoustic sound wave oscilloscope"></canvas>
                  <!-- Real-Time Musician Timbre & Diagnostic HUD Strip -->
                  <div class="tracker-wave-musician-strip" id="tracker-wave-musician-strip">
                    <span class="wave-musician-pill" id="wave-musician-kpi-1">Air Stability: 98% (Steady)</span>
                    <span class="wave-musician-pill" id="wave-musician-kpi-2">Octave: Madhya Saptak</span>
                    <span class="wave-musician-pill is-highlight" id="wave-musician-kpi-3">Timbre: Pure Bore Sine</span>
                  </div>
                </div>'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
replacement_lf = replacement.replace('\r\n', '\n')

if target_lf in text_lf:
    new_text = text_lf.replace(target_lf, replacement_lf).replace('\n', '\r\n')
    with open('index.html', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Patched index.html with tracker-wave-musician-strip!')
else:
    print('ERROR: Target not found in index.html')
