with open('d:/Music/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx_start = html.find('<div class="tracker-profile-header">')
idx_pills_end = html.find('</div>\n                      <!-- Dynamic Contextual', idx_start)
if idx_pills_end == -1:
    idx_pills_end = html.find('</div>', html.find('<div class="tracker-profile-pills">'))

print("Found index:", idx_start, idx_pills_end)

new_block = """<div class="tracker-profile-header">
                        <div class="tracker-title-col">
                          <span class="tracker-profile-title">Universal Instrument Engine</span>
                          <span class="tracker-persona-badge" id="tracker-persona-badge">Designed for: Vocalists &amp; Classical Singers</span>
                        </div>
                        <span class="tracker-signal-badge" id="live-signal-meter">Signal: Idle</span>
                      </div>
                      <div class="tracker-profile-pills">
                        <button type="button" class="tracker-inst-btn is-active" data-inst="voice" title="Vocal Gayaki, Formants &amp; 22-Shruti Pitch Profile">Voice</button>
                        <button type="button" class="tracker-inst-btn" data-inst="piano" title="Piano &amp; Keyboard Struck Wire, Polyphony &amp; Sustain Decay Profile">Piano/Keys</button>
                        <button type="button" class="tracker-inst-btn" data-inst="guitar" title="Guitar Strumming, Chords &amp; String Bend Profile">Guitar/Bass</button>
                        <button type="button" class="tracker-inst-btn" data-inst="flute" title="Bansuri &amp; Wind Instrument Bore Resonance Profile">Wind/Flute</button>
                        <button type="button" class="tracker-inst-btn" data-inst="sitar" title="Violin, Cello, Sitar &amp; Fretless String Profile">Violin/Sitar</button>
                        <button type="button" class="tracker-inst-btn" data-inst="percussion" title="Tabla, Dholak &amp; Percussion Onset Profile">Percussion</button>
                      </div>"""

# Find end of pills
pills_start = html.find('<div class="tracker-profile-pills">', idx_start)
pills_end = html.find('</div>', pills_start) + 6

old_part = html[idx_start:pills_end]
print("Old part:")
print(old_part)

html = html[:idx_start] + new_block + html[pills_end:]

with open('d:/Music/index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(html)
print("SUCCESS: Updated tracker profile header and pills with Piano/Keys and Persona Badge!")
