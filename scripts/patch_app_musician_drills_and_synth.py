# scripts/patch_app_musician_drills_and_synth.py

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Musician-specific drill adaptor
drill_helper = '''  // Musician-Specific Drill & Pedagogical Adaptation Engine
  function getMusicianSpecificDrill(baseDrill, inst) {
    if (!baseDrill) return baseDrill;
    if (inst === 'flute') {
      return baseDrill
        .replace(/vocal drill|vocal phrase|vocal/gi, 'flute air drill')
        .replace(/throat|larynx/gi, 'embouchure')
        .replace(/sing on vowel "Aa"|sing/gi, 'blow on steady diaphragm air')
        + ' [Flute Tip: Keep embouchure relaxed to prevent sharp Taar register drift].';
    } else if (inst === 'piano') {
      return baseDrill
        .replace(/vocal drill|vocal phrase|vocal/gi, 'piano voicing drill')
        .replace(/throat|larynx/gi, 'touch and attack velocity')
        .replace(/singing|sing/gi, 'voicing')
        .replace(/tanpura breath/gi, 'sustain pedal ring')
        + ' [Piano Tip: Equal Temperament third is +13.7c sharp; soften your 3rd for pure Just acoustic harmony].';
    } else if (inst === 'guitar') {
      return baseDrill
        .replace(/vocal drill|vocal phrase|vocal/gi, 'guitar intonation drill')
        .replace(/throat|larynx/gi, 'fretting hand pressure')
        .replace(/singing|sing/gi, 'plucking')
        .replace(/glide/gi, 'string bend')
        + ' [Guitar Tip: Use the bend gauge to calibrate exact cent target without overshooting].';
    } else if (inst === 'sitar') {
      return baseDrill
        .replace(/vocal drill|vocal phrase|vocal/gi, 'sitar meend drill')
        .replace(/throat|larynx/gi, 'meend pulling hand')
        .replace(/singing|sing/gi, 'plucking')
        + ' [Sitar Tip: Pull the Baaj string steadily to excite the sympathetic Tarafdar strings].';
    } else if (inst === 'percussion') {
      return 'Percussion Laya Drill: Practice landing the compound stroke (Dhā) exactly on Sam at 84 BPM, synchronizing Bāyān wrist modulation with the soloist.';
    }
    return baseDrill;
  }

'''

target_synth = '''  function playCurrentNoteReference() {
    const ctx = ensureAudioContext();
    if (!ctx) return;

    const baseSa = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
    const targetHz = baseSa * Math.pow(2, lastTrackedShrutiRatioCents / 1200);
    const now = ctx.currentTime;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = activeInstrumentProfile === 'flute' ? 'triangle' : 'sine';
    osc.frequency.setValueAtTime(targetHz, now);

    gain.gain.setValueAtTime(0.001, now);
    gain.gain.linearRampToValueAtTime(0.18, now + 0.05);
    gain.gain.setValueAtTime(0.18, now + 0.9);
    gain.gain.exponentialRampToValueAtTime(0.0008, now + 1.2);

    const analyser = ensureWaveAnalyser();
    if (analyser) osc.connect(analyser);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 1.25);
  }'''

replacement_synth = drill_helper + '''  function playCurrentNoteReference() {
    const ctx = ensureAudioContext();
    if (!ctx) return;

    const baseSa = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
    const targetHz = baseSa * Math.pow(2, lastTrackedShrutiRatioCents / 1200);
    const now = ctx.currentTime;
    const analyser = ensureWaveAnalyser();

    // 1. PIANO STRUCK WIRE ACOUSTIC MODEL
    if (activeInstrumentProfile === 'piano') {
      const pianoPartials = [
        { mult: 1.0, gain: 0.28, decay: 2.2 },
        { mult: 2.0, gain: 0.16, decay: 1.4 },
        { mult: 3.0, gain: 0.09, decay: 0.8 },
        { mult: 4.0, gain: 0.05, decay: 0.4 }
      ];
      pianoPartials.forEach(function (p) {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(targetHz * p.mult, now);
        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.linearRampToValueAtTime(p.gain, now + 0.004);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + p.decay);
        if (analyser) osc.connect(analyser);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + p.decay + 0.05);
      });
      return;
    }

    // 2. FLUTE PURE BORE AIR-COLUMN MODEL
    if (activeInstrumentProfile === 'flute') {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(targetHz, now);
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(0.24, now + 0.06);
      gain.gain.setValueAtTime(0.24, now + 1.1);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.5);
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(targetHz * 2.5, now);
      if (analyser) osc.connect(analyser);
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 1.55);
      return;
    }

    // 3. GUITAR PLUCKED STRING MODEL
    if (activeInstrumentProfile === 'guitar') {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(targetHz, now);
      const filter = ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(targetHz * 5, now);
      filter.frequency.exponentialRampToValueAtTime(targetHz * 1.5, now + 0.5);
      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(0.26, now + 0.005);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.4);
      if (analyser) osc.connect(analyser);
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 1.45);
      return;
    }

    // 4. SITAR / STRING JAWARI RESONANCE MODEL
    if (activeInstrumentProfile === 'sitar') {
      const sitarPartials = [
        { mult: 1.0, gain: 0.22, decay: 1.8 },
        { mult: 2.0, gain: 0.14, decay: 1.4 },
        { mult: 3.0, gain: 0.10, decay: 1.1 },
        { mult: 4.0, gain: 0.08, decay: 0.9 },
        { mult: 5.0, gain: 0.05, decay: 0.7 }
      ];
      sitarPartials.forEach(function (p) {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(targetHz * p.mult, now);
        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.linearRampToValueAtTime(p.gain, now + 0.012);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + p.decay);
        if (analyser) osc.connect(analyser);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + p.decay + 0.05);
      });
      return;
    }

    // 5. PERCUSSION TUNED DAYAN BELL MODEL
    if (activeInstrumentProfile === 'percussion') {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(targetHz, now);
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(targetHz, now);
      filter.Q.setValueAtTime(14.0, now);
      gain.gain.setValueAtTime(0.35, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.45);
      if (analyser) osc.connect(analyser);
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.50);
      return;
    }

    // 6. VOCAL GAYAKI FORMANT MODEL (Default)
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(targetHz, now);
    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(Math.min(targetHz * 2, 800), now);
    filter.Q.setValueAtTime(4.0, now);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.linearRampToValueAtTime(0.20, now + 0.04);
    gain.gain.setValueAtTime(0.20, now + 0.85);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.2);
    if (analyser) osc.connect(analyser);
    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 1.25);
  }'''

# Also update drill display in renderPhraseInspector:
target_drill_inspector = '''    if (drillEl) drillEl.textContent = modeData.drill;'''
replacement_drill_inspector = '''    if (drillEl) drillEl.textContent = getMusicianSpecificDrill(modeData.drill, activeInstrumentProfile);'''

# Also update drill display in renderFullAnalysisDossier:
target_drill_dossier = '''    if (drillTextEl) {
      drillTextEl.textContent = (primaryCritique.indian_classical_mode && primaryCritique.indian_classical_mode.prescriptive_drill) || 'Maintain regular practice with tanpura overtones.';
    }'''

replacement_drill_dossier = '''    if (drillTextEl) {
      const rawDrill = (primaryCritique.indian_classical_mode && primaryCritique.indian_classical_mode.prescriptive_drill) || 'Maintain regular practice with tanpura overtones.';
      drillTextEl.textContent = getMusicianSpecificDrill(rawDrill, activeInstrumentProfile);
    }'''

text_lf = text.replace('\r\n', '\n')
target_synth_lf = target_synth.replace('\r\n', '\n')
replacement_synth_lf = replacement_synth.replace('\r\n', '\n')
target_drill_inspector_lf = target_drill_inspector.replace('\r\n', '\n')
replacement_drill_inspector_lf = replacement_drill_inspector.replace('\r\n', '\n')
target_drill_dossier_lf = target_drill_dossier.replace('\r\n', '\n')
replacement_drill_dossier_lf = replacement_drill_dossier.replace('\r\n', '\n')

if target_synth_lf in text_lf and target_drill_inspector_lf in text_lf and target_drill_dossier_lf in text_lf:
    new_text = text_lf.replace(target_synth_lf, replacement_synth_lf).replace(target_drill_inspector_lf, replacement_drill_inspector_lf).replace(target_drill_dossier_lf, replacement_drill_dossier_lf).replace('\n', '\r\n')
    with open('app.js', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Patched app.js with Musician-Specific Drills and Physical Acoustic Sound Models!')
else:
    print('ERROR: One or more targets not found in app.js')
