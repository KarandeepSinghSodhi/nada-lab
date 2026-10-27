with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace toggleTanpuraDrone and updateActiveDroneFrequencies with authentic Jawari engine
old_drone_code = """  function toggleTanpuraDrone() {
    const btn = document.getElementById('drone-toggle-btn');
    const ctx = ensureAudioContext();
    if (!ctx) return;

    if (isDronePlaying && droneNodes) {
      droneNodes.masterGain.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.08);
      setTimeout(function () {
        if (droneNodes) {
          droneNodes.oscs.forEach(function (o) {
            try { o.stop(); } catch (e) {}
          });
          droneNodes = null;
        }
      }, 150);
      isDronePlaying = false;
      if (btn) btn.classList.remove('is-playing');
      updateDroneButtonLabel();
      return;
    }

    const saFreq = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
    const freqs = getDroneFrequencies(saFreq, currentDroneTuning);
    const masterGain = ctx.createGain();
    masterGain.gain.setValueAtTime(0.001, ctx.currentTime);
    masterGain.gain.setTargetAtTime(0.14, ctx.currentTime, 0.15);
    masterGain.connect(ctx.destination);

    const oscs = [];
    freqs.forEach(function (f, idx) {
      const osc = ctx.createOscillator();
      const filter = ctx.createBiquadFilter();
      const g = ctx.createGain();

      osc.type = idx % 2 === 0 ? 'sawtooth' : 'triangle';
      osc.frequency.setValueAtTime(f + (idx - 1.5) * 0.18, ctx.currentTime);

      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(680 + idx * 140, ctx.currentTime);
      filter.Q.setValueAtTime(3.2, ctx.currentTime);

      g.gain.setValueAtTime(0.24, ctx.currentTime);

      osc.connect(filter);
      filter.connect(g);
      g.connect(masterGain);
      osc.start();
      oscs.push(osc);
    });

    droneNodes = { masterGain: masterGain, oscs: oscs };
    isDronePlaying = true;
    if (btn) btn.classList.add('is-playing');
    updateDroneButtonLabel();
  }"""

new_drone_code = """  let tanpuraPluckTimer = null;
  let tanpuraStringIdx = 0;
  let tanpuraActiveOscs = [];

  function pluckTanpuraString(ctx, freq, stringIdx, stringName) {
    if (!ctx || !isDronePlaying || !droneNodes || !droneNodes.masterGain) return;
    const now = ctx.currentTime;

    // Pulse visual indicator if present
    const indicators = document.querySelectorAll('.tanpura-string-pip');
    if (indicators.length > 0) {
      indicators.forEach(function (ind, idx) {
        if (idx === stringIdx) {
          ind.classList.add('is-plucked');
          setTimeout(function () { ind.classList.remove('is-plucked'); }, 700);
        }
      });
    }

    // Miraj Jawari bridge harmonic series (1st, 2nd, 3rd, 4th, and 5th natural Ga overtone)
    const harmonics = [
      { mult: 1.0, gain: 0.28, decay: 3.2 },
      { mult: 2.0, gain: 0.18, decay: 2.8 },
      { mult: 3.0, gain: 0.12, decay: 2.2 },
      { mult: 4.0, gain: 0.08, decay: 1.8 },
      { mult: 5.0, gain: 0.05, decay: 1.4 } // 5th harmonic (pure Shuddha Ga overtone)
    ];

    harmonics.forEach(function (h) {
      try {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        const filter = ctx.createBiquadFilter();

        // Subtle micro-detune (+-0.4 cents) for acoustic air shimmer
        const detuneCents = (Math.random() - 0.5) * 0.8;
        osc.type = stringIdx === 3 ? 'triangle' : 'sawtooth';
        osc.frequency.setValueAtTime(freq * h.mult * Math.pow(2, detuneCents / 1200), now);

        filter.type = 'lowpass';
        filter.Q.setValueAtTime(2.8, now);
        // Jawari thread grazing acoustic envelope
        filter.frequency.setValueAtTime(450, now);
        filter.frequency.exponentialRampToValueAtTime(stringIdx === 3 ? 1400 : 2200, now + 0.035);
        filter.frequency.exponentialRampToValueAtTime(320, now + h.decay);

        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.linearRampToValueAtTime(h.gain, now + 0.025);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + h.decay);

        osc.connect(filter);
        filter.connect(gain);
        gain.connect(droneNodes.masterGain);

        osc.start(now);
        osc.stop(now + h.decay + 0.1);
        tanpuraActiveOscs.push(osc);

        setTimeout(function () {
          const idx = tanpuraActiveOscs.indexOf(osc);
          if (idx !== -1) tanpuraActiveOscs.splice(idx, 1);
        }, (h.decay + 0.2) * 1000);
      } catch (err) {
        // Safe ignore
      }
    });
  }

  function toggleTanpuraDrone() {
    const btn = document.getElementById('drone-toggle-btn');
    const ctx = ensureAudioContext();
    if (!ctx) return;

    if (isDronePlaying) {
      // Stop Tanpura Drone
      isDronePlaying = false;
      if (tanpuraPluckTimer) {
        clearTimeout(tanpuraPluckTimer);
        tanpuraPluckTimer = null;
      }
      if (droneNodes && droneNodes.masterGain) {
        droneNodes.masterGain.gain.setTargetAtTime(0.0001, ctx.currentTime, 0.08);
      }
      tanpuraActiveOscs.forEach(function (o) {
        try { o.stop(); } catch (e) {}
      });
      tanpuraActiveOscs.length = 0;
      droneNodes = null;

      if (btn) btn.classList.remove('is-playing');
      updateDroneButtonLabel();
      return;
    }

    // Start Authentic 4-String Jawari Plucking Loop
    isDronePlaying = true;
    const masterGain = ctx.createGain();
    masterGain.gain.setValueAtTime(0.24, ctx.currentTime);
    masterGain.connect(ctx.destination);
    droneNodes = { masterGain: masterGain, oscs: [] };

    tanpuraStringIdx = 0;
    function scheduleNextPluck() {
      if (!isDronePlaying || !droneNodes) return;
      const baseSa = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
      const freqs = getDroneFrequencies(baseSa, currentDroneTuning);
      
      // Strings: 0: Pa/Ma/Ni, 1: Jodi 1 (Sa'), 2: Jodi 2 (Sa' with +0.4c unison detune), 3: Kharaj Sa
      const stringNames = [
        currentDroneTuning === 'ma' ? 'Ma' : (currentDroneTuning === 'ni' ? 'Ni' : 'Pa'),
        "Sa'",
        "Sa'",
        'Sa'
      ];

      pluckTanpuraString(ctx, freqs[tanpuraStringIdx], tanpuraStringIdx, stringNames[tanpuraStringIdx]);

      tanpuraStringIdx = (tanpuraStringIdx + 1) % 4;
      const intervalMs = tanpuraStringIdx === 0 ? 1450 : 1080;
      tanpuraPluckTimer = setTimeout(scheduleNextPluck, intervalMs);
    }

    scheduleNextPluck();
    if (btn) btn.classList.add('is-playing');
    updateDroneButtonLabel();
  }"""

if old_drone_code in text:
    text = text.replace(old_drone_code, new_drone_code, 1)
    print("Replaced toggleTanpuraDrone with authentic Jawari engine")
else:
    print("old_drone_code not found")

# Replace updateActiveDroneFrequencies
old_update = """  function updateActiveDroneFrequencies() {
    if (!droneNodes || !audioCtx) return;
    const baseSa = userCustomSaHz || (PHRASE_LIBRARY[currentPhraseKey] && PHRASE_LIBRARY[currentPhraseKey].saHz) || 146.83;
    const freqs = getDroneFrequencies(baseSa, currentDroneTuning);
    const now = audioCtx.currentTime;
    droneNodes.oscs.forEach(function (osc, idx) {
      if (idx < freqs.length) {
        osc.frequency.setTargetAtTime(freqs[idx] + (idx - 1.5) * 0.18, now, 0.08);
      }
    });
  }"""

new_update = """  function updateActiveDroneFrequencies() {
    // In authentic Jawari plucking engine, frequency updates automatically take effect on the next string pluck
    updateDroneButtonLabel();
  }"""

if old_update in text:
    text = text.replace(old_update, new_update, 1)
    print("Replaced updateActiveDroneFrequencies")
else:
    print("old_update not found")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated app.js with Jawari Tanpura engine")
