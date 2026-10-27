// Prototype of Authentic 4-String Cyclic Plucking Tanpura with Jawari Overtones
function createJawariTanpuraEngine(audioCtx) {
  let isRunning = false;
  let timerId = null;
  let currentStringIdx = 0;
  let masterGain = null;

  function pluckString(freq, stringType) {
    if (!audioCtx || audioCtx.state !== 'running') return;
    const now = audioCtx.currentTime;

    // Harmonic ratios for authentic Miraj Jawari bridge grazing:
    // Fundamental, 2nd (8ve), 3rd (8ve+5th), 4th (2 8ves), 5th (natural Gandhar overtone!)
    const harmonics = [
      { mult: 1.0, gain: 0.28, decay: 2.8 },
      { mult: 2.0, gain: 0.18, decay: 2.4 },
      { mult: 3.0, gain: 0.12, decay: 2.0 },
      { mult: 4.0, gain: 0.08, decay: 1.6 },
      { mult: 5.0, gain: 0.05, decay: 1.2 } // Natural Ga overtone
    ];

    harmonics.forEach(function (h) {
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      const filter = audioCtx.createBiquadFilter();

      // Subtle random detune (+-0.4 cents) for acoustic organic shimmer
      const detuneCents = (Math.random() - 0.5) * 0.8;
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(freq * h.mult * Math.pow(2, detuneCents / 1200), now);

      filter.type = 'lowpass';
      filter.Q.setValueAtTime(2.5, now);
      // Jawari attack: filter sweeps up then relaxes
      filter.frequency.setValueAtTime(450, now);
      filter.frequency.exponentialRampToValueAtTime(1800, now + 0.04);
      filter.frequency.exponentialRampToValueAtTime(350, now + h.decay);

      gain.gain.setValueAtTime(0.0001, now);
      gain.gain.linearRampToValueAtTime(h.gain, now + 0.025);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + h.decay);

      osc.connect(filter);
      filter.connect(gain);
      gain.connect(masterGain);

      osc.start(now);
      osc.stop(now + h.decay + 0.1);
    });
  }

  return {
    start: function (saHz, tuningType) {
      this.stop();
      isRunning = true;
      masterGain = audioCtx.createGain();
      masterGain.gain.setValueAtTime(0.22, audioCtx.currentTime);
      masterGain.connect(audioCtx.destination);

      let firstStringFreq;
      if (tuningType === 'ma') {
        firstStringFreq = saHz * (4.0 / 3.0); // Shuddha Ma
      } else if (tuningType === 'ni') {
        firstStringFreq = saHz * (15.0 / 16.0); // Mandra Ni
      } else {
        firstStringFreq = saHz * (3.0 / 2.0); // Pancham (default)
      }

      // 4 Strings: 1. First String (Pa/Ma/Ni), 2. Jodi 1 (Sa'), 3. Jodi 2 (Sa'), 4. Kharaj (Sa)
      const stringFreqs = [
        firstStringFreq,
        saHz * 2.0, // Jodi 1 (middle octave)
        saHz * 2.0 * Math.pow(2, 0.4 / 1200), // Jodi 2 with unison micro-shimmer (+0.4c)
        saHz // Kharaj deep fundamental
      ];

      currentStringIdx = 0;
      function tick() {
        if (!isRunning) return;
        const f = stringFreqs[currentStringIdx];
        pluckString(f, currentStringIdx);
        currentStringIdx = (currentStringIdx + 1) % 4;
        const delay = currentStringIdx === 0 ? 1400 : 1050; // slightly longer breath pause after Kharaj Sa
        timerId = setTimeout(tick, delay);
      }
      tick();
    },
    stop: function () {
      isRunning = false;
      if (timerId) clearTimeout(timerId);
      timerId = null;
      if (masterGain) {
        masterGain.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.1);
        masterGain = null;
      }
    }
  };
}
