with open('d:/Music/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

redundant_block = """    // Initialize sub-controls for default profile
    renderInstrumentSubControls('voice');
    const hintEl = document.getElementById('tracker-profile-hint');

    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        const inst = btn.getAttribute('data-inst') || 'voice';
        activeInstrumentProfile = inst;

        if (hintEl) {
          if (inst === 'flute') {
            hintEl.textContent = 'Bansuri Flute mode: Pure air column resonance & Taar overblowing tracking';
          } else if (inst === 'string') {
            hintEl.textContent = 'String mode: Plucked attack & sympathetic jawari overtones active';
          } else {
            hintEl.textContent = 'Voice mode: Standard Gayaki formant detection & vowel resonance';
          }
        }

        // Trigger wave canvas start if not already active
        ensureWaveAnalyser();
      });
    });

    // Start wave canvas on initial load"""

clean_block = """    // Initialize sub-controls for default profile
    renderInstrumentSubControls('voice');

    // Start wave canvas on initial load"""

if redundant_block in text:
    text = text.replace(redundant_block, clean_block, 1)
    with open('d:/Music/app.js', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(text)
    print("SUCCESS: Removed redundant listener in initInstrumentProfiles!")
else:
    print("WARNING: redundant_block exact match not found, looking for partial match...")
    idx = text.find('function initInstrumentProfiles')
    print(text[idx:idx+800])
