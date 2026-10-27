with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix getAudioContext -> ensureAudioContext
old_synth = """  function playTablaBolSynth(bol) {
    const ctx = getAudioContext();"""

new_synth = """  function playTablaBolSynth(bol) {
    const ctx = ensureAudioContext();"""

if old_synth in text:
    text = text.replace(old_synth, new_synth, 1)
    print("Fixed getAudioContext in playTablaBolSynth")
else:
    print("old_synth not found")

# 2. Fix hintEl in initInstrumentProfiles
old_hint = """    // Initialize sub-controls for default profile
    renderInstrumentSubControls('voice');

    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        const inst = btn.getAttribute('data-inst') || 'voice';
        activeInstrumentProfile = inst;

        if (hintEl) {"""

new_hint = """    // Initialize sub-controls for default profile
    renderInstrumentSubControls('voice');
    const hintEl = document.getElementById('tracker-profile-hint');

    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        const inst = btn.getAttribute('data-inst') || 'voice';
        activeInstrumentProfile = inst;

        if (hintEl) {"""

if old_hint in text:
    text = text.replace(old_hint, new_hint, 1)
    print("Fixed hintEl in initInstrumentProfiles")
else:
    print("old_hint not found")

# 3. Add initPosterRows function
poster_fn = """
  function initPosterRows() {
    const posterRows = document.querySelectorAll('.poster-row');
    const ragaToPhraseKey = {
      'BHAIRAV': 'bhairav_gamak',
      'DARBARI': 'darbari_andolan',
      'YAMAN': 'yaman_meend',
      'TODI': 'todi_komal_ga',
      'BAGESHREE': 'bageshri_meend',
      'BHAIRAVI': 'bhairavi_nyasa'
    };

    posterRows.forEach(function (row) {
      row.setAttribute('role', 'button');
      row.setAttribute('tabindex', '0');
      const nameEl = row.querySelector('.poster-name');
      const ragaName = nameEl ? nameEl.textContent.trim().toUpperCase() : '';

      function activateRow() {
        posterRows.forEach(function (r) { r.classList.remove('is-active'); });
        row.classList.add('is-active');

        // 1. If matching phrase button exists, click it
        const phraseKey = ragaToPhraseKey[ragaName];
        let matchedBtn = null;
        if (phraseKey) {
          matchedBtn = document.querySelector('.ui-phrase-btn[data-phrase="' + phraseKey + '"]');
        }
        if (matchedBtn) {
          matchedBtn.click();
        } else {
          const allBtns = Array.from(document.querySelectorAll('.ui-phrase-btn'));
          const found = allBtns.find(function (b) { return b.textContent.toUpperCase().includes(ragaName); });
          if (found) found.click();
        }

        // 2. Update target raga select dropdown
        const ragaSelect = document.getElementById('ui-target-raga-select');
        if (ragaSelect) {
          const capName = ragaName.charAt(0) + ragaName.slice(1).toLowerCase();
          for (let i = 0; i < ragaSelect.options.length; i++) {
            if (ragaSelect.options[i].value.toLowerCase() === capName.toLowerCase()) {
              ragaSelect.selectedIndex = i;
              ragaSelect.dispatchEvent(new Event('change'));
              break;
            }
          }
        }

        // 3. Smooth scroll up to canvas inspector
        const inspectorSection = document.getElementById('shruti-inspector') || document.querySelector('.ui-canvas-pane');
        if (inspectorSection) {
          inspectorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }

      row.addEventListener('click', activateRow);
      row.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activateRow();
        }
      });
    });
  }
"""

if 'function initPosterRows' not in text:
    idx = text.find('document.addEventListener(\x27DOMContentLoaded\x27')
    text = text[:idx] + poster_fn + '\n  ' + text[idx:]
    print("Inserted initPosterRows definition")

old_dom_load = """    checkApiStatus();
    renderPhraseInspector();
    initScrollChoreography();"""

new_dom_load = """    checkApiStatus();
    initPosterRows();
    renderPhraseInspector();
    initScrollChoreography();"""

if old_dom_load in text:
    text = text.replace(old_dom_load, new_dom_load, 1)
    print("Called initPosterRows in DOMContentLoaded")
else:
    print("old_dom_load not found")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated app.js")
