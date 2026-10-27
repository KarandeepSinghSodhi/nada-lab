with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

tala_start = text.find('              <!-- Interactive Tala & Laya Metronome Grid -->')
tala_end = text.find('            </div>\n\n            <div class="ui-diagnostic-pane">')
print('Tala indices:', tala_start, tala_end)

rasa_start = text.find('              <!-- Real-Time Rasa & Emotion Radar (Valence-Arousal Affective Map) -->')
rasa_end = text.find('              <dl class="ui-telemetry-grid">')
print('Rasa indices:', rasa_start, rasa_end)

drawer_start = text.find('              <div id="analyst-drawer"')
drawer_end = text.find('            </div>\n          </div>\n        </div>')
print('Drawer indices:', drawer_start, drawer_end)
