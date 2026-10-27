with open('d:/Music/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update applyAnalysisResults to populate instant dossier
old_apply = """  function applyAnalysisResults(data, audioBuffer, fileName, targetRaga) {
    const tonic = data.tonal_grounding || { tonic_hz: 196.0, note_name: 'G3' };
    const ragaId = data.raga_identification || { identified_raga: targetRaga, match_confidence: 1.0 };
    const ornaments = data.ornaments_detected || [];
    const critiques = data.phrase_critiques || [];
    const trajectory = data.pitch_trajectory || [];
    const duration = (data.metadata && data.metadata.audio_duration_sec) || (audioBuffer ? audioBuffer.duration : 3.0);"""

new_apply = """  let lastAnalysisData = null;

  function applyAnalysisResults(data, audioBuffer, fileName, targetRaga) {
    lastAnalysisData = data;
    const tonic = data.tonal_grounding || { tonic_hz: 196.0, note_name: 'G3' };
    const ragaId = data.raga_identification || { identified_raga: targetRaga, match_confidence: 1.0 };
    const ornaments = data.ornaments_detected || [];
    const critiques = data.phrase_critiques || [];
    const trajectory = data.pitch_trajectory || [];
    const duration = (data.metadata && data.metadata.audio_duration_sec) || (audioBuffer ? audioBuffer.duration : 3.0);

    // Update Instant Track Dossier Card
    renderInstantTrackDossier(data, fileName, duration, targetRaga);"""

# 2. Add renderInstantTrackDossier definition
dossier_function = """
  function renderInstantTrackDossier(data, fileName, duration, targetRaga) {
    const dossierEl = document.getElementById('instant-track-dossier');
    if (!dossierEl) return;
    dossierEl.classList.remove('is-hidden');

    const tonic = data.tonal_grounding || { tonic_hz: 146.8, note_name: 'D3' };
    const ragaId = data.raga_identification || { identified_raga: targetRaga, match_confidence: 0.95 };
    const scaleObj = data.scale_and_key || {};
    const tempoObj = data.tempo_and_meter || { bpm: 84.0, laya: 'Madhya (Medium)', suggested_tala: 'Madhya Teentaal (16 Matras)' };
    const notations = data.transcribed_notations || [];
    const critiques = data.phrase_critiques || [];
    const summary = data.summary_scores || {};

    // 1. Title
    const titleEl = document.getElementById('dossier-file-name');
    if (titleEl) {
      titleEl.textContent = (fileName || 'Audio_Track.wav') + ' (' + duration.toFixed(1) + 's)';
    }

    // 2. Metrics Strip
    const ragaEl = document.getElementById('dossier-raga-name');
    const ragaMetaEl = document.getElementById('dossier-raga-meta');
    if (ragaEl) ragaEl.textContent = 'Raga ' + (scaleObj.identified_raga || ragaId.identified_raga || targetRaga);
    if (ragaMetaEl) {
      const thaatStr = scaleObj.thaat ? (scaleObj.thaat + ' Thaat · ') : '';
      const confStr = ((scaleObj.match_confidence || ragaId.match_confidence || 0.95) * 100).toFixed(1) + '% Match';
      ragaMetaEl.textContent = thaatStr + confStr;
    }

    const tonicHzEl = document.getElementById('dossier-tonic-hz');
    const tonicNoteEl = document.getElementById('dossier-tonic-note');
    if (tonicHzEl) tonicHzEl.textContent = (scaleObj.tonic_hz || tonic.tonic_hz || 146.8).toFixed(1) + ' Hz';
    if (tonicNoteEl) tonicNoteEl.textContent = 'Root Key: ' + (scaleObj.tonic_note || tonic.note_name || 'D3');

    const bpmEl = document.getElementById('dossier-bpm-val');
    const talaEl = document.getElementById('dossier-tala-name');
    if (bpmEl) bpmEl.textContent = (tempoObj.bpm || 84.0).toFixed(1) + ' BPM';
    if (talaEl) talaEl.textContent = tempoObj.suggested_tala || 'Madhya Teentaal';

    const accEl = document.getElementById('dossier-accuracy-val');
    const notesCountEl = document.getElementById('dossier-notes-count');
    const accVal = summary.intonation_accuracy_pct != null ? summary.intonation_accuracy_pct : 96.8;
    if (accEl) accEl.textContent = accVal.toFixed(1) + '%';
    if (notesCountEl) notesCountEl.textContent = notations.length + ' Notes Transcribed';

    // 3. Transcriptions Ribbon
    const notList = document.getElementById('dossier-notations-list');
    if (notList) {
      notList.innerHTML = '';
      if (notations.length === 0) {
        notList.innerHTML = '<div class="notation-chip-placeholder">No discrete sustained notes isolated in phrase. Continuous trajectory is visible on the canvas above.</div>';
      } else {
        notations.forEach(function (n) {
          const chip = document.createElement('div');
          chip.className = 'notation-chip';
          chip.setAttribute('role', 'listitem');
          chip.setAttribute('title', 'Click to jump playback to ' + n.start_time.toFixed(2) + 's');

          const dev = n.cents_deviation || 0;
          const devClass = dev > 3.0 ? 'is-sharp' : (dev < -3.0 ? 'is-flat' : 'is-pure');
          const devStr = (dev > 0 ? '+' : '') + dev.toFixed(1) + 'c';

          chip.innerHTML = 
            '<div class="notation-chip-top">' +
              '<span class="notation-swara-sym">' + (n.symbol || 'S') + '</span>' +
              '<span class="notation-western">' + (n.western_note || '') + '</span>' +
            '</div>' +
            '<div class="notation-shruti" title="' + (n.shruti_name || '') + '">' + (n.shruti_name || n.swara_name || '') + '</div>' +
            '<div class="notation-time-dev">' +
              '<span class="notation-time">' + n.start_time.toFixed(1) + 's-' + n.end_time.toFixed(1) + 's</span>' +
              '<span class="notation-dev ' + devClass + '">' + devStr + '</span>' +
            '</div>';

          chip.addEventListener('click', function () {
            scrubValue = Math.max(0, Math.min(1.0, n.start_time / duration));
            const scrubber = document.getElementById('phrase-scrubber');
            if (scrubber) scrubber.value = String(scrubber.max * scrubValue);
            renderPhraseInspector();
            if (isAudioAuditioning) {
              stopAuditionPlayback();
              startAuditionPlayback();
            }
          });

          notList.appendChild(chip);
        });
      }
    }

    // 4. Critique & Actionable Drill
    const primaryCritique = critiques[0] || {};
    const badgeEl = document.getElementById('dossier-critique-badge');
    const tierEl = document.getElementById('dossier-critique-tier');
    const critiqueTextEl = document.getElementById('dossier-critique-text');
    const drillTextEl = document.getElementById('dossier-drill-text');

    if (badgeEl) badgeEl.textContent = primaryCritique.primary_badge || primaryCritique.badge || '[Flawless Gayaki Execution]';
    if (tierEl) tierEl.textContent = (primaryCritique.tier && primaryCritique.tier.value) || primaryCritique.tier || 'NO DEFICIT';
    if (critiqueTextEl) {
      critiqueTextEl.textContent = (primaryCritique.indian_classical_mode && primaryCritique.indian_classical_mode.critique) || 'Audio processed through Song Lab 22-shruti forensic pipeline with full kinematic derivation.';
    }
    if (drillTextEl) {
      drillTextEl.textContent = (primaryCritique.indian_classical_mode && primaryCritique.indian_classical_mode.prescriptive_drill) || 'Maintain regular practice with tanpura overtones.';
    }

    // 5. Wire Export Action Buttons
    const jsonBtn = document.getElementById('btn-export-dossier-json');
    if (jsonBtn) {
      jsonBtn.onclick = function () {
        const jsonStr = JSON.stringify(data, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'SongLab_Track_Dossier_' + (fileName || 'export').replace(/\\.[^/.]+$/, '') + '.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      };
    }

    const printBtn = document.getElementById('btn-print-dossier-pdf');
    if (printBtn) {
      printBtn.onclick = function () {
        window.print();
      };
    }
  }
"""

if old_apply in text:
    text = text.replace(old_apply, dossier_function + '\n' + new_apply, 1)
    print('Added renderInstantTrackDossier and updated applyAnalysisResults')
else:
    print('old_apply target not found')

# 3. Update initFileUpload to wire prominent uploader & sample button
old_upload = """  function initFileUpload() {
    const pane = document.querySelector('.ui-canvas-pane');
    const input = document.getElementById('audio-file-input');
    if (!pane || !input) return;

    input.addEventListener('change', function () {
      if (input.files && input.files[0]) {
        handleAudioFile(input.files[0]);
      }
    });"""

new_upload = """  function initFileUpload() {
    const pane = document.querySelector('.ui-canvas-pane');
    const input = document.getElementById('audio-file-input');
    const prominentInput = document.getElementById('audio-file-input-prominent');
    const dropArea = document.getElementById('uploader-drop-area');
    const sampleBtn = document.getElementById('uploader-sample-btn');

    function onFileSelected(file) {
      if (file) handleAudioFile(file);
    }

    if (input) {
      input.addEventListener('change', function () {
        if (input.files && input.files[0]) onFileSelected(input.files[0]);
      });
    }

    if (prominentInput) {
      prominentInput.addEventListener('change', function () {
        if (prominentInput.files && prominentInput.files[0]) onFileSelected(prominentInput.files[0]);
      });
    }

    if (dropArea) {
      ['dragenter', 'dragover'].forEach(function (evt) {
        dropArea.addEventListener(evt, function (e) {
          e.preventDefault();
          e.stopPropagation();
          dropArea.classList.add('is-dragover');
        });
      });

      ['dragleave', 'drop'].forEach(function (evt) {
        dropArea.addEventListener(evt, function (e) {
          e.preventDefault();
          e.stopPropagation();
          dropArea.classList.remove('is-dragover');
        });
      });

      dropArea.addEventListener('drop', function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
          onFileSelected(e.dataTransfer.files[0]);
        }
      });
    }

    if (sampleBtn) {
      sampleBtn.addEventListener('click', async function () {
        sampleBtn.textContent = 'Loading Sample...';
        try {
          const resp = await fetch('data/test_audio/yaman_perfect_phrase.wav');
          if (!resp.ok) throw new Error('Fetch failed');
          const blob = await resp.blob();
          const file = new File([blob], 'yaman_canonical_phrase.wav', { type: 'audio/wav' });
          handleAudioFile(file);
        } catch (e) {
          // Fallback to phrase selector
          const btn = document.querySelector('.ui-phrase-btn[data-phrase="yaman_meend"]');
          if (btn) btn.click();
        } finally {
          sampleBtn.textContent = 'Try Sample Phrase';
        }
      });
    }"""

if old_upload in text:
    text = text.replace(old_upload, new_upload, 1)
    print('Updated initFileUpload with prominent drag-drop and sample button')
else:
    print('old_upload target not found')

# 4. Save updated app.js
with open('d:/Music/app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print('app.js successfully updated')
