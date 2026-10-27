# scripts/patch_app_tala_events.py

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    if (slider) {
      slider.addEventListener('input', function () {
        talaTempoBpm = parseInt(slider.value, 10);
        const layaLabel = talaTempoBpm < 60 ? 'Vilambit' : (talaTempoBpm > 140 ? 'Drut' : 'Madhya');
        if (tempoVal) tempoVal.textContent = talaTempoBpm + ' BPM (' + layaLabel + ')';
        if (tempoVal) tempoVal.textContent = talaTempoBpm + ' BPM';
      });
    }

    if (btn) {
      btn.addEventListener('click', toggleTalaMetronome);
    }

    renderTalaGridUI();
  }'''

replacement = '''    if (slider) {
      slider.addEventListener('input', function () {
        talaTempoBpm = parseInt(slider.value, 10);
        const layaLabel = talaTempoBpm < 60 ? 'Vilambit' : (talaTempoBpm > 140 ? 'Drut' : 'Madhya');
        if (tempoVal) tempoVal.textContent = talaTempoBpm + ' BPM · ' + layaLabel + ' Laya';
      });
    }

    const soundSelect = document.getElementById('ui-tala-sound-select');
    if (soundSelect) {
      soundSelect.addEventListener('change', function () {
        currentTalaSound = soundSelect.value;
      });
    }

    if (btn) {
      btn.addEventListener('click', toggleTalaMetronome);
    }

    updateTalaTuningDisplay();
    renderTalaGridUI();
  }'''

# Also add updateTalaTuningDisplay() to applyInstrumentTonic and slider apply
target2 = '''    const calibOpenBtn = document.getElementById('calibrate-sa-btn');
    if (calibOpenBtn) {
      calibOpenBtn.textContent = 'Sa: ' + hz.toFixed(1) + ' Hz (' + note + ')';
      calibOpenBtn.classList.add('is-calibrated');
    }'''

replacement2 = '''    const calibOpenBtn = document.getElementById('calibrate-sa-btn');
    if (calibOpenBtn) {
      calibOpenBtn.textContent = 'Sa: ' + hz.toFixed(1) + ' Hz (' + note + ')';
      calibOpenBtn.classList.add('is-calibrated');
    }
    updateTalaTuningDisplay();'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
replacement_lf = replacement.replace('\r\n', '\n')
target2_lf = target2.replace('\r\n', '\n')
replacement2_lf = replacement2.replace('\r\n', '\n')

if target_lf in text_lf and target2_lf in text_lf:
    new_text = text_lf.replace(target_lf, replacement_lf).replace(target2_lf, replacement2_lf).replace('\n', '\r\n')
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('SUCCESS: Patched app.js with Tala events & dynamic tuning sync!')
else:
    print('ERROR: Targets not found in app.js')
