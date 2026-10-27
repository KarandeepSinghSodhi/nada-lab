# scripts/patch_leadsheet_playback_and_musicxml.py

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_html = '''                <button type="button" id="btn-export-sheet-music-pdf" class="sheet-export-btn" title="Export printable Lead Sheet with Lyrics and Notes">
                  Print / Export Lead Sheet
                </button>'''

replacement_html = '''                <button type="button" id="btn-play-leadsheet" class="sheet-export-btn sheet-play-btn" title="Playback entire Lead Sheet melody with active instrument tone">
                  ▶ Play Lead Sheet
                </button>
                <button type="button" id="btn-export-musicxml" class="sheet-export-btn" title="Export standard MusicXML (.xml) for MuseScore, Sibelius, Finale, Dorico">
                  Export MusicXML (.xml)
                </button>
                <button type="button" id="btn-export-sheet-music-pdf" class="sheet-export-btn" title="Export printable Lead Sheet with Lyrics and Notes">
                  Print / Export Lead Sheet
                </button>'''

if target_html in html:
    html = html.replace(target_html, replacement_html, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html with MusicXML and Play Lead Sheet buttons.")
else:
    print("target_html not found in index.html")

# 2. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target_js = '''    const printBtn = document.getElementById('btn-export-sheet-music-pdf');
    if (printBtn) {
      printBtn.addEventListener('click', function () {
        window.print();
      });
    }'''

replacement_js = '''    const printBtn = document.getElementById('btn-export-sheet-music-pdf');
    if (printBtn) {
      printBtn.addEventListener('click', function () {
        window.print();
      });
    }

    // MusicXML Export Handler
    const musicXmlBtn = document.getElementById('btn-export-musicxml');
    if (musicXmlBtn) {
      musicXmlBtn.addEventListener('click', async function () {
        if (!currentLeadSheetScore) {
          if (typeof showToast === 'function') showToast('No lead sheet extracted yet to export');
          return;
        }
        try {
          const resp = await fetch('/api/export-musicxml', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              notations: (typeof lastPipelineResult !== 'undefined' && lastPipelineResult?.transcribed_notations) || [],
              lyrics: document.getElementById('lyrics-extractor-input')?.value || '',
              tempo_bpm: currentLeadSheetScore.tempo_bpm || 84.0,
              tonic_hz: currentLeadSheetScore.tonic_hz || 146.83,
              phrase_key: activePhraseKey || 'yaman_meend',
              instrument: activeInstrumentProfile || 'piano'
            })
          });
          if (!resp.ok) throw new Error('MusicXML export failed');
          const blob = await resp.blob();
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = (activePhraseKey || 'songlab_phrase') + '_leadsheet.musicxml';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
          if (typeof showToast === 'function') showToast('Downloaded MusicXML for MuseScore / Sibelius!');
        } catch (err) {
          console.error(err);
          if (typeof showToast === 'function') showToast('Failed to export MusicXML');
        }
      });
    }

    // Lead Sheet Sequential Audio Playback
    const playLeadSheetBtn = document.getElementById('btn-play-leadsheet');
    let isPlayingLeadSheet = false;
    let leadSheetPlayTimeout = null;
    if (playLeadSheetBtn) {
      playLeadSheetBtn.addEventListener('click', function () {
        if (isPlayingLeadSheet) {
          clearTimeout(leadSheetPlayTimeout);
          isPlayingLeadSheet = false;
          playLeadSheetBtn.textContent = '▶ Play Lead Sheet';
          playLeadSheetBtn.classList.remove('is-playing');
          document.querySelectorAll('.sheet-event').forEach(function (e) { e.classList.remove('is-active'); });
          return;
        }
        if (!currentLeadSheetScore || !currentLeadSheetScore.measures) {
          if (typeof showToast === 'function') showToast('No lead sheet loaded to play');
          return;
        }
        const allEvents = [];
        currentLeadSheetScore.measures.forEach(function (m) {
          (m.events || []).forEach(function (ev) { allEvents.push(ev); });
        });
        if (allEvents.length === 0) return;

        isPlayingLeadSheet = true;
        playLeadSheetBtn.textContent = '⏹ Stop Playback';
        playLeadSheetBtn.classList.add('is-playing');

        let evIdx = 0;
        function playNext() {
          if (!isPlayingLeadSheet || evIdx >= allEvents.length) {
            isPlayingLeadSheet = false;
            playLeadSheetBtn.textContent = '▶ Play Lead Sheet';
            playLeadSheetBtn.classList.remove('is-playing');
            document.querySelectorAll('.sheet-event').forEach(function (e) { e.classList.remove('is-active'); });
            return;
          }
          const ev = allEvents[evIdx];
          const eventElements = document.querySelectorAll('.sheet-event');
          eventElements.forEach(function (e) { e.classList.remove('is-active'); });
          if (eventElements[evIdx]) {
            eventElements[evIdx].classList.add('is-active');
            eventElements[evIdx].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
          }
          if (ev.frequency_hz && typeof playSynthesizedInstrumentTone === 'function') {
            const durationSec = Math.max(0.18, (ev.duration_ms || 400) / 1000.0);
            playSynthesizedInstrumentTone(ev.frequency_hz, activeInstrumentProfile || 'piano', durationSec);
          }
          const waitMs = Math.max(220, ev.duration_ms || 500);
          evIdx++;
          leadSheetPlayTimeout = setTimeout(playNext, waitMs);
        }
        playNext();
      });
    }'''

if target_js in js:
    js = js.replace(target_js, replacement_js, 1)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Updated app.js with MusicXML and Play Lead Sheet logic.")
else:
    print("target_js not found in app.js")
