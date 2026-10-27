import re

with open('d:/Music/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Helper function for extracting peaks from audioBuffer
helper_code = """
  function extractWaveformPeaks(audioBuffer, targetPoints) {
    targetPoints = targetPoints || 160;
    if (!audioBuffer) return [];
    try {
      const ch = audioBuffer.getChannelData(0);
      const step = Math.max(1, Math.floor(ch.length / targetPoints));
      const peaks = [];
      for (let i = 0; i < targetPoints; i++) {
        let max = 0;
        const start = i * step;
        const end = Math.min(ch.length, start + step);
        for (let j = start; j < end; j++) {
          const v = Math.abs(ch[j]);
          if (v > max) max = v;
        }
        peaks.push(Number(max.toFixed(3)));
      }
      return peaks;
    } catch (e) {
      return [];
    }
  }
"""

if 'function extractWaveformPeaks' not in text:
    # insert before applyAnalysisResults
    idx = text.find('function applyAnalysisResults')
    if idx != -1:
        text = text[:idx] + helper_code + '\n  ' + text[idx:]
        print('Inserted extractWaveformPeaks helper')

# 2. Store waveform_peaks in PHRASE_LIBRARY['custom_upload']
old_custom_lib = """    PHRASE_LIBRARY['custom_upload'] = {
      badge: 'Raga ' + (ragaId.identified_raga || targetRaga) + ' · Sa = ' + tonic.tonic_hz.toFixed(1) + ' Hz (' + (tonic.note_name || '') + ') · ' + duration.toFixed(1) + 's',
      saHz: tonic.tonic_hz,
      shrutis: shrutis,
      range: [Math.min(minC, -40), Math.max(maxC, 750)],
      ornamentTag: ornamentSummary,
      trajectory: trajectory,
      curveFn: curveFn,
      audioBuffer: audioBuffer,"""

new_custom_lib = """    const wfPeaks = (data.waveform_peaks && data.waveform_peaks.length > 0)
      ? data.waveform_peaks
      : extractWaveformPeaks(audioBuffer, 160);

    PHRASE_LIBRARY['custom_upload'] = {
      badge: 'Raga ' + (ragaId.identified_raga || targetRaga) + ' · Sa = ' + tonic.tonic_hz.toFixed(1) + ' Hz (' + (tonic.note_name || '') + ') · ' + duration.toFixed(1) + 's',
      saHz: tonic.tonic_hz,
      shrutis: shrutis,
      range: [Math.min(minC, -40), Math.max(maxC, 750)],
      ornamentTag: ornamentSummary,
      trajectory: trajectory,
      curveFn: curveFn,
      waveform_peaks: wfPeaks,
      audioBuffer: audioBuffer,"""

if old_custom_lib in text:
    text = text.replace(old_custom_lib, new_custom_lib, 1)
    print("Updated PHRASE_LIBRARY['custom_upload'] with waveform_peaks")
else:
    # try normalized
    print("old_custom_lib exact match not found, checking...")

# 3. In renderPhraseInspector, draw audio waveform peaks envelope underlay
old_render_canvas_start = """    const canvas = document.getElementById('shruti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#0e0e0e';
    ctx.fillRect(0, 0, w, h);

    const minC = phrase.range[0];
    const maxC = phrase.range[1];
    const padLeft = 24;
    const padRight = 24;
    const padTop = 28;
    const padBottom = 28;
    const plotW = w - padLeft - padRight;
    const plotH = h - padTop - padBottom;"""

new_render_canvas_start = """    const canvas = document.getElementById('shruti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width;
    const h = canvas.height;

    ctx.clearRect(0, 0, w, h);
    ctx.fillStyle = '#0e0e0e';
    ctx.fillRect(0, 0, w, h);

    const minC = phrase.range[0];
    const maxC = phrase.range[1];
    const padLeft = 24;
    const padRight = 24;
    const padTop = 28;
    const padBottom = 28;
    const plotW = w - padLeft - padRight;
    const plotH = h - padTop - padBottom;

    // Render Audio Waveform Silhouette Overlay
    const wf = phrase.waveform_peaks || (phrase.audioBuffer ? extractWaveformPeaks(phrase.audioBuffer, 160) : null);
    if (wf && wf.length > 0) {
      const midY = padTop + plotH * 0.5;
      const ampMax = plotH * 0.38;
      ctx.fillStyle = 'rgba(241, 241, 239, 0.08)';
      ctx.beginPath();
      for (let i = 0; i < wf.length; i++) {
        const x = padLeft + (i / (wf.length - 1)) * plotW;
        const hVal = Math.min(1.0, wf[i]) * ampMax;
        if (i === 0) ctx.moveTo(x, midY - hVal);
        else ctx.lineTo(x, midY - hVal);
      }
      for (let i = wf.length - 1; i >= 0; i--) {
        const x = padLeft + (i / (wf.length - 1)) * plotW;
        const hVal = Math.min(1.0, wf[i]) * ampMax;
        ctx.lineTo(x, midY + hVal);
      }
      ctx.closePath();
      ctx.fill();

      ctx.strokeStyle = 'rgba(241, 241, 239, 0.12)';
      ctx.lineWidth = 1;
      ctx.setLineDash([2, 4]);
      ctx.beginPath();
      ctx.moveTo(padLeft, midY);
      ctx.lineTo(w - padRight, midY);
      ctx.stroke();
      ctx.setLineDash([]);
    }"""

if old_render_canvas_start in text:
    text = text.replace(old_render_canvas_start, new_render_canvas_start, 1)
    print("Added waveform peaks canvas rendering to renderPhraseInspector")
else:
    print("old_render_canvas_start exact match not found")

with open('d:/Music/app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated app.js")
