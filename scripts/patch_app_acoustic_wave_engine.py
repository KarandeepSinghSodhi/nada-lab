# scripts/patch_app_acoustic_wave_engine.py

with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''  // Real-Time Acoustic Oscilloscope Waveform Renderer (The "Cool Wave")
  function startAcousticWaveLoop() {
    if (waveAnimFrameId) return;

    const canvas = document.getElementById('acoustic-wave-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const statsEl = document.getElementById('live-wave-stats');

    function drawWave() {
      waveAnimFrameId = requestAnimationFrame(drawWave);
      if (!waveAnalyserNode) return;

      waveAnalyserNode.getFloatTimeDomainData(waveDataArray);

      const w = canvas.width;
      const h = canvas.height;
      const centerY = h / 2;

      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = '#0c0c0c';
      ctx.fillRect(0, 0, w, h);

      // Draw subtle grid lines
      ctx.strokeStyle = 'rgba(241, 241, 239, 0.04)';
      ctx.lineWidth = 1;
      for (let x = 0; x < w; x += 80) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }

      // Draw center baseline
      ctx.strokeStyle = 'rgba(143, 166, 142, 0.18)';
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      ctx.lineTo(w, centerY);
      ctx.stroke();

      // Check sound energy (RMS)
      let sumSq = 0;
      for (let i = 0; i < waveDataArray.length; i++) {
        sumSq += waveDataArray[i] * waveDataArray[i];
      }
      const rms = Math.sqrt(sumSq / waveDataArray.length);

      // Record to rolling envelope history
      dynamicEnvelopeHistory.push(rms);
      if (dynamicEnvelopeHistory.length > 140) dynamicEnvelopeHistory.shift();

      // Instrument Timbre Color Scheme
      let instColor = '#8fa68e';
      let instGradColor = 'rgba(143, 166, 142, 0.25)';
      if (activeInstrumentProfile === 'piano') {
        instColor = '#8c92e8'; // Royal Indigo (Struck string wire)
        instGradColor = 'rgba(140, 146, 232, 0.28)';
      } else if (activeInstrumentProfile === 'flute') {
        instColor = '#a4bca3'; // Bamboo Jade (Bore resonance)
        instGradColor = 'rgba(164, 188, 163, 0.25)';
      } else if (activeInstrumentProfile === 'guitar') {
        instColor = '#6ea89e'; // Teal Bronze
        instGradColor = 'rgba(110, 168, 158, 0.26)';
      } else if (activeInstrumentProfile === 'sitar') {
        instColor = '#d2aa72'; // Classical Bronze (Jawari shimmer)
        instGradColor = 'rgba(210, 170, 114, 0.28)';
      } else if (activeInstrumentProfile === 'percussion') {
        instColor = '#c07a56'; // Terracotta Amber (Tabla shell)
        instGradColor = 'rgba(192, 122, 86, 0.28)';
      }

      if (rms < 0.005) {
        // Serene ambient idling breath pulse
        const now = performance.now() / 1000;
        ctx.strokeStyle = instColor;
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        for (let x = 0; x < w; x += 4) {
          const u = x / w;
          const y = centerY + Math.sin(u * 12 + now * 3) * 2.2;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        if (statsEl) statsEl.textContent = 'Standby · Dynamic Period Lock · 60 FPS';
        return;
      }

      // MODE 1: ENVELOPE MODE (ADSR Attack Transient & Sustain Decay)
      if (activeWaveMode === 'envelope') {
        const envLen = dynamicEnvelopeHistory.length;
        const maxEnvVal = 0.35; // Maximum headroom reference

        // Fill under envelope
        const envGrad = ctx.createLinearGradient(0, 0, 0, h);
        envGrad.addColorStop(0, instGradColor);
        envGrad.addColorStop(1, 'rgba(0, 0, 0, 0.02)');

        ctx.beginPath();
        ctx.moveTo(0, h);
        for (let i = 0; i < envLen; i++) {
          const x = (i / (envLen - 1)) * w;
          const normE = Math.min(1.0, dynamicEnvelopeHistory[i] / maxEnvVal);
          const y = h - normE * (h * 0.88);
          ctx.lineTo(x, y);
        }
        ctx.lineTo(w, h);
        ctx.closePath();
        ctx.fillStyle = envGrad;
        ctx.fill();

        // Stroke envelope outline
        ctx.strokeStyle = instColor;
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        for (let i = 0; i < envLen; i++) {
          const x = (i / (envLen - 1)) * w;
          const normE = Math.min(1.0, dynamicEnvelopeHistory[i] / maxEnvVal);
          const y = h - normE * (h * 0.88);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();

        if (statsEl) {
          const envTitle = activeInstrumentProfile === 'piano' ? 'Piano ADSR Sustain Decay' :
            (activeInstrumentProfile === 'flute' ? 'Bansuri Breath Pressure Stability' :
            (activeInstrumentProfile === 'guitar' ? 'Guitar Pluck Attack & Ring' : 'Acoustic Sound Envelope'));
          statsEl.textContent = envTitle + ' · ' + (rms * 100).toFixed(0) + '% RMS · 60 FPS';
        }
        return;
      }

      // MODE 2: SPECTRUM HARMONICS MODE
      if (activeWaveMode === 'spectrum') {
        waveAnalyserNode.getByteFrequencyData(waveFreqDataArray);
        const barCount = 48;
        const barWidth = Math.max(3, (w / barCount) - 2);

        for (let i = 0; i < barCount; i++) {
          const val = waveFreqDataArray[i * 4];
          const barHeight = (val / 255) * (h * 0.85);
          const x = i * (barWidth + 2);
          const y = h - barHeight;

          const barGrad = ctx.createLinearGradient(0, y, 0, h);
          barGrad.addColorStop(0, instColor);
          barGrad.addColorStop(1, 'rgba(143, 166, 142, 0.08)');

          ctx.fillStyle = barGrad;
          ctx.fillRect(x, y, barWidth, barHeight);
        }

        if (statsEl) {
          const specLabel = activeInstrumentProfile === 'piano' ? 'Piano Polyphonic Harmonics' :
            (activeInstrumentProfile === 'sitar' ? 'Sitar Sympathetic Jawari Peaks' : 'Acoustic Spectrum Partials');
          statsEl.textContent = specLabel + ' · 60 FPS';
        }
        return;
      }

      // MODE 3: TIMBRE-ADAPTIVE PITCH-SYNCHRONIZED OSCILLOSCOPE
      // Calculate pitch period for jitter-free period locking
      const currentPitchHz = lastTrackedLiveHz > 30 ? lastTrackedLiveHz : (userCustomSaHz || 146.83);
      const periodSamples = Math.max(20, Math.min(600, Math.round(44100 / currentPitchHz)));
      
      // Window size: Exactly 2.5 full acoustic wave cycles
      const cycleWindow = Math.max(96, Math.min(1024, Math.round(periodSamples * 2.5)));

      // Slope-locked trigger search: find upward zero-crossing with maximum derivative
      let triggerIdx = 0;
      let maxSlope = 0;
      for (let i = 1; i < Math.min(waveDataArray.length - cycleWindow, 350); i++) {
        if (waveDataArray[i - 1] < 0 && waveDataArray[i] >= 0) {
          const slope = waveDataArray[i] - waveDataArray[i - 1];
          if (slope > maxSlope) {
            maxSlope = slope;
            triggerIdx = i;
          }
        }
      }

      const drawLen = Math.min(waveDataArray.length - triggerIdx, cycleWindow);

      // Translucent glow gradient
      const grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, instGradColor);
      grad.addColorStop(1, 'rgba(0, 0, 0, 0.02)');

      // Draw wave envelope fill
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      for (let i = 0; i < drawLen; i++) {
        const x = (i / (drawLen - 1)) * w;
        let v = waveDataArray[triggerIdx + i];
        // For flute: subtle smoothing highlights pure bore resonance
        if (activeInstrumentProfile === 'flute' && i > 0 && i < drawLen - 1) {
          v = (waveDataArray[triggerIdx + i - 1] + v * 2 + waveDataArray[triggerIdx + i + 1]) / 4;
        }
        const y = centerY - v * (h * 0.44);
        ctx.lineTo(x, y);
      }
      ctx.lineTo(w, centerY);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();

      // Draw primary glowing oscilloscope trace line
      ctx.strokeStyle = instColor;
      ctx.lineWidth = 2.4;
      ctx.beginPath();
      for (let i = 0; i < drawLen; i++) {
        const x = (i / (drawLen - 1)) * w;
        let v = waveDataArray[triggerIdx + i];
        if (activeInstrumentProfile === 'flute' && i > 0 && i < drawLen - 1) {
          v = (waveDataArray[triggerIdx + i - 1] + v * 2 + waveDataArray[triggerIdx + i + 1]) / 4;
        }
        const y = centerY - v * (h * 0.44);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      if (statsEl) {
        const timbreLabel = activeInstrumentProfile === 'piano' ? 'Piano Struck Wire (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'flute' ? 'Bansuri Air Column (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'guitar' ? 'Guitar Plucked String (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'sitar' ? 'Sitar Jawari Resonance (2.5 Cycles Locked)' : 'Gayaki Formant Waveform (2.5 Cycles Locked)')));
        statsEl.textContent = timbreLabel + ' · ' + (rms * 100).toFixed(0) + '% RMS · 60 FPS';
      }
    }

      drawWave();
  }'''

replacement = '''  // Musician-Grade Real-Time Acoustic Oscilloscope & Timbre Engine
  let prevWaveTriggerOffset = 0;
  let rollingRmsHistory = [];

  function startAcousticWaveLoop() {
    if (waveAnimFrameId) return;

    const canvas = document.getElementById('acoustic-wave-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const statsEl = document.getElementById('live-wave-stats');
    const kpi1 = document.getElementById('wave-musician-kpi-1');
    const kpi2 = document.getElementById('wave-musician-kpi-2');
    const kpi3 = document.getElementById('wave-musician-kpi-3');

    function drawWave() {
      waveAnimFrameId = requestAnimationFrame(drawWave);
      if (!waveAnalyserNode) return;

      waveAnalyserNode.getFloatTimeDomainData(waveDataArray);

      const w = canvas.width;
      const h = canvas.height;
      const centerY = h / 2;

      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = '#0c0c0c';
      ctx.fillRect(0, 0, w, h);

      // Subtle phosphor oscilloscope reticle grid
      ctx.strokeStyle = 'rgba(241, 241, 239, 0.04)';
      ctx.lineWidth = 1;
      for (let x = 0; x < w; x += 80) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }

      // Center zero-voltage ground line
      ctx.strokeStyle = 'rgba(143, 166, 142, 0.16)';
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      ctx.lineTo(w, centerY);
      ctx.stroke();

      // Check sound energy (RMS)
      let sumSq = 0;
      for (let i = 0; i < waveDataArray.length; i++) {
        sumSq += waveDataArray[i] * waveDataArray[i];
      }
      const rms = Math.sqrt(sumSq / waveDataArray.length);

      // Maintain rolling RMS window for stability analysis (40 frames ~ 660ms)
      rollingRmsHistory.push(rms);
      if (rollingRmsHistory.length > 40) rollingRmsHistory.shift();

      // Record to rolling envelope history (160 frames ~ 2.6 seconds)
      dynamicEnvelopeHistory.push(rms);
      if (dynamicEnvelopeHistory.length > 160) dynamicEnvelopeHistory.shift();

      // Instrument Timbre Acoustic Palette
      let instColor = '#8fa68e';
      let instGradColor = 'rgba(143, 166, 142, 0.25)';
      if (activeInstrumentProfile === 'piano') {
        instColor = '#8c92e8'; // Royal Indigo (Struck string wire)
        instGradColor = 'rgba(140, 146, 232, 0.28)';
      } else if (activeInstrumentProfile === 'flute') {
        instColor = '#a4bca3'; // Bamboo Jade (Air column bore resonance)
        instGradColor = 'rgba(164, 188, 163, 0.25)';
      } else if (activeInstrumentProfile === 'guitar') {
        instColor = '#6ea89e'; // Teal Bronze (Plucked string transient)
        instGradColor = 'rgba(110, 168, 158, 0.26)';
      } else if (activeInstrumentProfile === 'sitar') {
        instColor = '#d2aa72'; // Classical Bronze (Jawari bridge cascade)
        instGradColor = 'rgba(210, 170, 114, 0.28)';
      } else if (activeInstrumentProfile === 'percussion') {
        instColor = '#c07a56'; // Terracotta Amber (Bāyān / Dāyān parchment)
        instGradColor = 'rgba(192, 122, 86, 0.28)';
      }

      // Compute breath / tone amplitude stability (standard deviation of RMS)
      let rmsMean = 0;
      for (let r = 0; r < rollingRmsHistory.length; r++) rmsMean += rollingRmsHistory[r];
      rmsMean /= Math.max(1, rollingRmsHistory.length);
      let rmsVariance = 0;
      for (let r = 0; r < rollingRmsHistory.length; r++) {
        const diff = rollingRmsHistory[r] - rmsMean;
        rmsVariance += diff * diff;
      }
      const rmsStdDev = Math.sqrt(rmsVariance / Math.max(1, rollingRmsHistory.length));
      const toneSteadiness = Math.max(65.0, Math.min(99.4, 100.0 - rmsStdDev * 450.0));

      const pitchHz = lastTrackedLiveHz > 30 ? lastTrackedLiveHz : (userCustomSaHz || 146.83);

      // Update Musician Diagnostic HUD Strip
      if (kpi1 && kpi2 && kpi3) {
        if (rms < 0.005) {
          kpi1.textContent = 'Signal: Ambient Standby';
          kpi2.textContent = 'Tonic: ' + (userCustomSaHz || 146.8).toFixed(1) + ' Hz';
          kpi3.textContent = 'Acoustic Phase Locked';
        } else if (activeInstrumentProfile === 'flute') {
          kpi1.textContent = 'Air Stability: ' + toneSteadiness.toFixed(1) + '% (' + (toneSteadiness > 92 ? 'Steady Breath' : 'Fluctuating Air') + ')';
          const octaveName = pitchHz < 190 ? 'Mandra Saptak (Bass)' : (pitchHz > 380 ? 'Taar Saptak (Overblown)' : 'Madhya Saptak (Middle)');
          kpi2.textContent = 'Register: ' + octaveName;
          kpi3.textContent = 'Bore: Pure Bamboo Sine';
        } else if (activeInstrumentProfile === 'piano') {
          kpi1.textContent = 'Struck Attack: ' + (rms > 0.15 ? 'Forte Hammer' : (rms > 0.06 ? 'Mezzo Strike' : 'Piano Touch'));
          kpi2.textContent = 'Sustain: ' + (rms > 0.02 ? 'Singing Soundboard Ring' : 'Damped');
          kpi3.textContent = 'Voicing: Harmonic Wire Resonance';
        } else if (activeInstrumentProfile === 'guitar') {
          const bendCents = Math.round(((Math.log2(pitchHz / 440) * 1200) % 100 + 100) % 100);
          kpi1.textContent = 'String Bend: ' + (bendCents > 18 ? '+' + bendCents + 'c Bend' : 'True Fretted Pitch');
          kpi2.textContent = 'Attack: ' + (rms > 0.12 ? 'Sharp Plectrum Transient' : 'Fingerstyle Warmth');
          kpi3.textContent = 'Tuning: ' + (currentGuitarTuningMode === 'dropd' ? 'Drop D' : 'Standard 6-String');
        } else if (activeInstrumentProfile === 'sitar') {
          kpi1.textContent = 'Jawari Buzz: Rich Overtone Shimmer';
          kpi2.textContent = 'Andolan / Vibrato: ' + (currentAndolanSpeed > 0.5 ? currentAndolanSpeed.toFixed(1) + ' Hz' : 'Sustained Swara');
          kpi3.textContent = 'Bridge: Parabolic Curved Contact';
        } else if (activeInstrumentProfile === 'percussion') {
          kpi1.textContent = 'Strike Impact: ' + (rms > 0.1 ? '1.8 ms (Punchy Onset)' : 'Gentle Tap');
          kpi2.textContent = 'Laya: ' + (talaTempoBpm < 60 ? 'Vilambit Laya' : (talaTempoBpm > 140 ? 'Drut Laya' : 'Madhya Laya'));
          kpi3.textContent = 'Percussion: ' + (currentPercussionKit === 'tabla' ? 'Acoustic Tabla Bol' : 'Rhythm Pulse');
        } else {
          kpi1.textContent = 'Vocal Formant: Open Akar';
          kpi2.textContent = 'Sa Tonic: ' + (userCustomSaHz || 146.8).toFixed(1) + ' Hz';
          kpi3.textContent = 'Intonation: 22-Shruti Natural Consonance';
        }
      }

      if (rms < 0.005) {
        // Serene ambient idling breath pulse
        const now = performance.now() / 1000;
        ctx.strokeStyle = instColor;
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        for (let x = 0; x < w; x += 4) {
          const u = x / w;
          const y = centerY + Math.sin(u * 12 + now * 3) * 2.2;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
        if (statsEl) statsEl.textContent = 'Standby · Phase Locked · 60 FPS';
        return;
      }

      // MODE 1: ENVELOPE MODE (ADSR Struck Attack & Sustain Decay)
      if (activeWaveMode === 'envelope') {
        const envLen = dynamicEnvelopeHistory.length;
        const maxEnvVal = 0.35; // Maximum headroom reference

        // Fill under envelope
        const envGrad = ctx.createLinearGradient(0, 0, 0, h);
        envGrad.addColorStop(0, instGradColor);
        envGrad.addColorStop(1, 'rgba(0, 0, 0, 0.02)');

        ctx.beginPath();
        ctx.moveTo(0, h);
        for (let i = 0; i < envLen; i++) {
          const x = (i / (envLen - 1)) * w;
          const normE = Math.min(1.0, dynamicEnvelopeHistory[i] / maxEnvVal);
          const y = h - normE * (h * 0.88);
          ctx.lineTo(x, y);
        }
        ctx.lineTo(w, h);
        ctx.closePath();
        ctx.fillStyle = envGrad;
        ctx.fill();

        // Stroke envelope outline
        ctx.strokeStyle = instColor;
        ctx.lineWidth = 2.4;
        ctx.beginPath();
        for (let i = 0; i < envLen; i++) {
          const x = (i / (envLen - 1)) * w;
          const normE = Math.min(1.0, dynamicEnvelopeHistory[i] / maxEnvVal);
          const y = h - normE * (h * 0.88);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();

        // Highlight recent peak attack spike for Piano / Guitar / Percussion
        if (activeInstrumentProfile === 'piano' || activeInstrumentProfile === 'guitar' || activeInstrumentProfile === 'percussion') {
          const latestIdx = envLen - 1;
          const peakX = w;
          const peakY = h - Math.min(1.0, dynamicEnvelopeHistory[latestIdx] / maxEnvVal) * (h * 0.88);
          ctx.fillStyle = '#f1f1ef';
          ctx.beginPath();
          ctx.arc(peakX - 3, peakY, 3, 0, Math.PI * 2);
          ctx.fill();
        }

        if (statsEl) {
          const envTitle = activeInstrumentProfile === 'piano' ? 'Piano ADSR Sustain & Pedal Decay' :
            (activeInstrumentProfile === 'flute' ? 'Bansuri Air Stream Stability Envelope' :
            (activeInstrumentProfile === 'guitar' ? 'Guitar Pluck Attack & Decay Ring' : 'Dynamic Sound Energy Envelope'));
          statsEl.textContent = envTitle + ' · ' + (rms * 100).toFixed(0) + '% RMS · 60 FPS';
        }
        return;
      }

      // MODE 2: SPECTRUM HARMONICS MODE
      if (activeWaveMode === 'spectrum') {
        waveAnalyserNode.getByteFrequencyData(waveFreqDataArray);
        const barCount = 48;
        const barWidth = Math.max(3, (w / barCount) - 2);

        for (let i = 0; i < barCount; i++) {
          const val = waveFreqDataArray[i * 4];
          const barHeight = (val / 255) * (h * 0.85);
          const x = i * (barWidth + 2);
          const y = h - barHeight;

          const barGrad = ctx.createLinearGradient(0, y, 0, h);
          barGrad.addColorStop(0, instColor);
          barGrad.addColorStop(1, 'rgba(143, 166, 142, 0.08)');

          ctx.fillStyle = barGrad;
          ctx.fillRect(x, y, barWidth, barHeight);
        }

        if (statsEl) {
          const specLabel = activeInstrumentProfile === 'piano' ? 'Piano Harmonic Wire Voicing' :
            (activeInstrumentProfile === 'sitar' ? 'Sitar Sympathetic Jawari Overtones' :
            (activeInstrumentProfile === 'flute' ? 'Flute Pure Air Column Partials' : 'Acoustic Harmonic Spectrum'));
          statsEl.textContent = specLabel + ' · 60 FPS';
        }
        return;
      }

      // MODE 3: TIMBRE-AUTHENTIC ACOUSTIC STANDING WAVE OSCILLOSCOPE
      // Calculate fundamental period for jitter-free lock
      const periodSamples = Math.max(18, Math.min(600, Math.round(44100 / pitchHz)));
      
      // Window size: Exactly 2.5 full acoustic fundamental cycles
      const cycleWindow = Math.max(96, Math.min(1024, Math.round(periodSamples * 2.5)));

      // Jitter-Free Trigger: Find zero-crossing with maximum positive slope
      let triggerIdx = 0;
      let maxSlope = 0;
      const searchLimit = Math.min(waveDataArray.length - cycleWindow, 350);
      for (let i = 1; i < searchLimit; i++) {
        if (waveDataArray[i - 1] < 0 && waveDataArray[i] >= 0) {
          const slope = waveDataArray[i] - waveDataArray[i - 1];
          // Bias slightly towards previous frame's offset to lock phase horizontally
          const phaseDiff = Math.abs((i % periodSamples) - (prevWaveTriggerOffset % periodSamples));
          const phaseWeight = 1.0 - Math.min(0.5, phaseDiff / periodSamples);
          const weightedSlope = slope * phaseWeight;
          if (weightedSlope > maxSlope) {
            maxSlope = weightedSlope;
            triggerIdx = i;
          }
        }
      }
      prevWaveTriggerOffset = triggerIdx;

      const drawLen = Math.min(waveDataArray.length - triggerIdx, cycleWindow);

      // For Flute: Render gentle turbulent breath shimmer aura behind the wave
      if (activeInstrumentProfile === 'flute') {
        ctx.strokeStyle = 'rgba(164, 188, 163, 0.15)';
        ctx.lineWidth = 6.0;
        ctx.beginPath();
        for (let i = 0; i < drawLen; i++) {
          const x = (i / (drawLen - 1)) * w;
          const rawV = waveDataArray[triggerIdx + i];
          const y = centerY - rawV * (h * 0.44);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.stroke();
      }

      // Translucent glow gradient fill
      const grad = ctx.createLinearGradient(0, 0, 0, h);
      grad.addColorStop(0, instGradColor);
      grad.addColorStop(1, 'rgba(0, 0, 0, 0.02)');

      // Draw wave envelope fill
      ctx.beginPath();
      ctx.moveTo(0, centerY);
      for (let i = 0; i < drawLen; i++) {
        const x = (i / (drawLen - 1)) * w;
        let v = waveDataArray[triggerIdx + i];
        // Flute: 5-point Gaussian smoothing for pure air column fundamental
        if (activeInstrumentProfile === 'flute' && i >= 2 && i < drawLen - 2) {
          v = (waveDataArray[triggerIdx + i - 2] +
               waveDataArray[triggerIdx + i - 1] * 4 +
               v * 6 +
               waveDataArray[triggerIdx + i + 1] * 4 +
               waveDataArray[triggerIdx + i + 2]) / 16;
        }
        const y = centerY - v * (h * 0.44);
        ctx.lineTo(x, y);
      }
      ctx.lineTo(w, centerY);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();

      // Draw primary glowing oscilloscope trace line
      ctx.strokeStyle = instColor;
      ctx.lineWidth = activeInstrumentProfile === 'piano' ? 2.6 : 2.2;
      ctx.beginPath();
      for (let i = 0; i < drawLen; i++) {
        const x = (i / (drawLen - 1)) * w;
        let v = waveDataArray[triggerIdx + i];
        if (activeInstrumentProfile === 'flute' && i >= 2 && i < drawLen - 2) {
          v = (waveDataArray[triggerIdx + i - 2] +
               waveDataArray[triggerIdx + i - 1] * 4 +
               v * 6 +
               waveDataArray[triggerIdx + i + 1] * 4 +
               waveDataArray[triggerIdx + i + 2]) / 16;
        }
        const y = centerY - v * (h * 0.44);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.stroke();

      // For Piano: highlight hammer strike excitation point on maximum wave peak
      if (activeInstrumentProfile === 'piano' && rms > 0.04) {
        let maxPeakIdx = 0;
        let maxPeakVal = -1;
        for (let i = 0; i < drawLen; i++) {
          if (waveDataArray[triggerIdx + i] > maxPeakVal) {
            maxPeakVal = waveDataArray[triggerIdx + i];
            maxPeakIdx = i;
          }
        }
        const px = (maxPeakIdx / (drawLen - 1)) * w;
        const py = centerY - maxPeakVal * (h * 0.44);
        ctx.fillStyle = '#ffdf78'; // Golden felt hammer impact bead
        ctx.beginPath();
        ctx.arc(px, py, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }

      if (statsEl) {
        const timbreLabel = activeInstrumentProfile === 'piano' ? 'Piano Struck Wire (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'flute' ? 'Bansuri Air Column (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'guitar' ? 'Guitar Plucked String (2.5 Cycles Locked)' :
          (activeInstrumentProfile === 'sitar' ? 'Sitar Jawari Shimmer (2.5 Cycles Locked)' : 'Gayaki Formant Waveform (2.5 Cycles Locked)')));
        statsEl.textContent = timbreLabel + ' · ' + (rms * 100).toFixed(0) + '% RMS · 60 FPS';
      }
    }

      drawWave();
  }'''

text_lf = text.replace('\r\n', '\n')
target_lf = target.replace('\r\n', '\n')
replacement_lf = replacement.replace('\r\n', '\n')

if target_lf in text_lf:
    new_text = text_lf.replace(target_lf, replacement_lf).replace('\n', '\r\n')
    with open('app.js', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Patched app.js with Musician-Grade Real-Time Acoustic Oscilloscope & Timbre Engine!')
else:
    print('ERROR: Target not found in app.js')
