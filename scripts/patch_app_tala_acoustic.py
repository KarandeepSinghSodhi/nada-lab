# scripts/patch_app_tala_acoustic.py
import re

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''  function playTablaBolSynth(bol) {
    const ctx = ensureAudioContext();
    if (!ctx) return;
    const now = ctx.currentTime;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const filter = ctx.createBiquadFilter();

    if (bol === 'Dhā' || bol === 'Dhin') {
      // Bayan bass resonance (135 Hz down to 75 Hz) + open ring
      osc.type = 'sine';
      osc.frequency.setValueAtTime(138, now);
      osc.frequency.exponentialRampToValueAtTime(76, now + 0.16);
      gain.gain.setValueAtTime(0.42, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(360, now);
    } else if (bol === 'Ge' || bol === 'Ghe') {
      // Modulated Bayan slide
      osc.type = 'sine';
      osc.frequency.setValueAtTime(80, now);
      osc.frequency.linearRampToValueAtTime(120, now + 0.08);
      osc.frequency.exponentialRampToValueAtTime(70, now + 0.28);
      gain.gain.setValueAtTime(0.35, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.28);
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(300, now);
    } else if (bol === 'Tin' || bol === 'Tha') {
      // Dayan open bell stroke
      osc.type = 'sine';
      osc.frequency.setValueAtTime(388, now);
      gain.gain.setValueAtTime(0.28, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.24);
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(388, now);
      filter.Q.setValueAtTime(8.0, now);
    } else if (bol === 'Nā') {
      // Sharp Dayan rim tone
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(440, now);
      gain.gain.setValueAtTime(0.25, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.18);
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(440, now);
    } else {
      // Tā / Ka / Kat crisp dampened stroke
      osc.type = 'sine';
      osc.frequency.setValueAtTime(260, now);
      gain.gain.setValueAtTime(0.20, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
      filter.type = 'highpass';
      filter.frequency.setValueAtTime(220, now);
    }

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);
    osc.start(now);
    osc.stop(now + 0.35);
  }

  function tickTalaMetronome() {
    if (!isTalaPlaying) return;
    const sys = TALA_SYSTEMS[currentTalaKey] || TALA_SYSTEMS.teentaal;
    const bol = sys.bols[currentMatra];
    playTablaBolSynth(bol);

    // Update grid UI
    const cells = document.querySelectorAll('.matra-cell');
    cells.forEach(function (c, idx) {
      if (idx === currentMatra) {
        c.classList.add('is-active');
      } else {
        c.classList.remove('is-active');
      }
    });

    currentMatra = (currentMatra + 1) % sys.matras;
    const intervalMs = (60.0 / talaTempoBpm) * 1000.0;
    talaTimer = setTimeout(tickTalaMetronome, intervalMs);
  }'''

replacement = '''  let currentTalaSound = 'tabla'; // 'tabla', 'mridangam', 'woodblock', 'bell'
  let sharedNoiseBuffer = null;

  function getSharedNoiseBuffer(ctx) {
    if (!sharedNoiseBuffer || sharedNoiseBuffer.sampleRate !== ctx.sampleRate) {
      const bufferSize = ctx.sampleRate; // 1 second
      sharedNoiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = sharedNoiseBuffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }
    }
    return sharedNoiseBuffer;
  }

  function updateTalaTuningDisplay() {
    const pill = document.getElementById('tala-sa-tuning-pill');
    if (!pill) return;
    const rootSa = (typeof userCustomSaHz === 'number' && userCustomSaHz > 50) ? userCustomSaHz : 146.83;
    const dayanPitch = (rootSa < 180) ? rootSa * 2 : rootSa;
    pill.textContent = 'Dāyān: Sa = ' + rootSa.toFixed(1) + ' Hz (' + dayanPitch.toFixed(1) + ' Hz)';
  }

  function playTablaBolSynth(bol, isSam) {
    const ctx = ensureAudioContext();
    if (!ctx) return;
    const now = ctx.currentTime;
    const rootSa = (typeof userCustomSaHz === 'number' && userCustomSaHz > 50) ? userCustomSaHz : 146.83;
    const dayanPitch = (rootSa < 180) ? rootSa * 2 : rootSa;
    const samBoost = isSam ? 1.25 : 1.0;

    // 1. STUDIO WOODBLOCK MODE
    if (currentTalaSound === 'woodblock') {
      const freq = isSam ? 920 : 640;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, now);
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(freq, now);
      filter.Q.setValueAtTime(24.0, now);
      gain.gain.setValueAtTime((isSam ? 0.38 : 0.22) * samBoost, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + (isSam ? 0.045 : 0.030));
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.05);
      return;
    }

    // 2. TEMPLE BELL / GHANTI MODE
    if (currentTalaSound === 'bell') {
      const bellFreqs = isSam ? [270, 540, 764, 1080] : [540, 764, 1080];
      bellFreqs.forEach(function (f, idx) {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(f, now);
        const amp = (0.22 / (idx + 1)) * (isSam ? 1.3 : 1.0);
        gain.gain.setValueAtTime(amp, now);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + (isSam ? 1.2 : 0.75));
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 1.25);
      });
      return;
    }

    // Normalize bol for matching
    const rawBol = (bol || '').toLowerCase().trim();
    const cleanBol = rawBol.replace(/ā/g, 'a').replace(/ī/g, 'i').replace(/ū/g, 'u');

    // Helper: Transient Skin Strike Noise (Fingernail on parchment)
    function playTransientClick(gainVal, cutoffHz, duration) {
      try {
        const noiseSource = ctx.createBufferSource();
        noiseSource.buffer = getSharedNoiseBuffer(ctx);
        const noiseFilter = ctx.createBiquadFilter();
        noiseFilter.type = 'highpass';
        noiseFilter.frequency.setValueAtTime(cutoffHz || 3200, now);
        const noiseGain = ctx.createGain();
        noiseGain.gain.setValueAtTime(gainVal * samBoost, now);
        noiseGain.gain.exponentialRampToValueAtTime(0.0001, now + (duration || 0.012));
        noiseSource.connect(noiseFilter);
        noiseFilter.connect(noiseGain);
        noiseGain.connect(ctx.destination);
        noiseSource.start(now);
        noiseSource.stop(now + (duration || 0.015));
      } catch (err) {
        // Fallback gracefully
      }
    }

    // Helper: Bāyān Sub-bass sweep
    function playBayanBass(startHz, endHz, duration, gainVal, slideTime) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(startHz, now);
      osc.frequency.exponentialRampToValueAtTime(endHz, now + (slideTime || 0.16));
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(320, now);
      filter.Q.setValueAtTime(2.2, now);
      gain.gain.setValueAtTime(gainVal * samBoost, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + duration + 0.05);
    }

    // Helper: Dāyān Tuned Rim or Sur Bell Ring
    function playDayanTuned(freq, qVal, duration, gainVal, oscType) {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();
      osc.type = oscType || 'sine';
      osc.frequency.setValueAtTime(freq, now);
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(freq, now);
      filter.Q.setValueAtTime(qVal || 14.0, now);
      gain.gain.setValueAtTime(gainVal * samBoost, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + duration + 0.05);
    }

    // 3. CARNATIC MRIDANGAM MODE
    if (currentTalaSound === 'mridangam') {
      if (cleanBol === 'dhi' || (cleanBol === 'tha' && isSam)) {
        // Resonant Thoppi bass + Valanthalai
        playBayanBass(92, 64, 0.32, 0.48, 0.14);
        playDayanTuned(dayanPitch, 12.0, 0.22, 0.30, 'sine');
      } else if (cleanBol === 'mi' || cleanBol === 'jo' || cleanBol === 'nu') {
        // Bright metallic chapu strike
        playTransientClick(0.18, 3800, 0.010);
        playDayanTuned(dayanPitch * 1.5, 16.0, 0.20, 0.32, 'triangle');
      } else if (cleanBol === 'ka' || cleanBol === 'tha') {
        // Flat dampened slap on drum face
        playTransientClick(0.24, 2200, 0.015);
        playDayanTuned(210, 4.0, 0.045, 0.25, 'sine');
      } else {
        // Default Mridangam stroke
        playDayanTuned(dayanPitch, 10.0, 0.18, 0.28, 'sine');
      }
      return;
    }

    // 4. AUTHENTIC ACOUSTIC TABLA MODE (Default)
    if (cleanBol === 'dha') {
      // Compound stroke: Bāyān sub-bass sweep + Dāyān tuned rim click
      playBayanBass(136, 72, 0.34, 0.52, 0.18);
      playTransientClick(0.22, 3200, 0.012);
      playDayanTuned(dayanPitch, 16.0, 0.24, 0.40, 'triangle');
    } else if (cleanBol === 'dhin' || cleanBol === 'dhi') {
      // Singing compound stroke: Bāyān bass + Dāyān inner Sur ring (pure & sweet)
      playBayanBass(112, 68, 0.38, 0.46, 0.16);
      playDayanTuned(dayanPitch, 10.0, 0.30, 0.34, 'sine');
    } else if (cleanBol === 'ge' || cleanBol === 'ghe') {
      // Modulated Bāyān bass glide: palm wrist pressure pushes pitch up then down
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const filter = ctx.createBiquadFilter();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(78, now);
      osc.frequency.linearRampToValueAtTime(130, now + 0.06);
      osc.frequency.exponentialRampToValueAtTime(68, now + 0.30);
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(290, now);
      filter.Q.setValueAtTime(2.6, now);
      gain.gain.setValueAtTime(0.48 * samBoost, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.32);
      osc.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.35);
    } else if (cleanBol === 'na' || cleanBol === 'ta' || cleanBol === 'kinar') {
      // Sharp open Dāyān rim stroke on kinar / gajra
      playTransientClick(0.24, 3400, 0.010);
      playDayanTuned(dayanPitch, 18.0, 0.22, 0.38, 'triangle');
    } else if (cleanBol === 'tin' || cleanBol === 'ti' || cleanBol === 'tun' || cleanBol === 'tha') {
      // Pure open Dāyān Sur ring (resonant singing bell chime)
      playDayanTuned(dayanPitch, 8.0, 0.28, 0.32, 'sine');
    } else if (cleanBol === 'ka' || cleanBol === 'ke' || cleanBol === 'kat' || cleanBol === 'ki') {
      // Flat closed slap: dry, woody, non-resonant, quick damping
      playTransientClick(0.28, 1800, 0.020);
      playDayanTuned(175, 3.5, 0.040, 0.26, 'sine');
    } else {
      // General resonant stroke fallback
      playTransientClick(0.15, 2800, 0.010);
      playDayanTuned(dayanPitch, 12.0, 0.16, 0.28, 'sine');
    }
  }

  function tickTalaMetronome() {
    if (!isTalaPlaying) return;
    const sys = TALA_SYSTEMS[currentTalaKey] || TALA_SYSTEMS.teentaal;
    const bol = sys.bols[currentMatra];
    const isSam = (currentMatra === sys.samIndex);
    playTablaBolSynth(bol, isSam);

    // Update grid UI
    const cells = document.querySelectorAll('.matra-cell');
    cells.forEach(function (c, idx) {
      if (idx === currentMatra) {
        c.classList.add('is-active');
      } else {
        c.classList.remove('is-active');
      }
    });

    currentMatra = (currentMatra + 1) % sys.matras;
    const intervalMs = (60.0 / talaTempoBpm) * 1000.0;
    talaTimer = setTimeout(tickTalaMetronome, intervalMs);
  }'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
replacement_lf = replacement.replace('\r\n', '\n')

if target_lf in text_lf:
    new_text = text_lf.replace(target_lf, replacement_lf).replace('\n', '\r\n')
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('SUCCESS: Patched app.js with authentic tabla physical modeling!')
else:
    print('ERROR: Target string not found in app.js')
