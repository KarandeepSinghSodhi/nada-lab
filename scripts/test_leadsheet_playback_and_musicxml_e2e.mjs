import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Lead Sheet Audio Audition & MusicXML Export End-to-End...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Track Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check for button presence
    const btnCheck = await page.eval(() => {
      const playBtn = document.getElementById('btn-play-leadsheet');
      const xmlBtn = document.getElementById('btn-export-musicxml');
      const printBtn = document.getElementById('btn-export-sheet-music-pdf');
      return {
        hasPlayBtn: !!playBtn,
        playBtnText: playBtn ? playBtn.textContent.trim() : null,
        hasXmlBtn: !!xmlBtn,
        xmlBtnText: xmlBtn ? xmlBtn.textContent.trim() : null,
        hasPrintBtn: !!printBtn
      };
    });
    console.log('Lead Sheet Control Buttons Check:', btnCheck);
    if (!btnCheck.hasPlayBtn || !btnCheck.hasXmlBtn) {
      throw new Error('Buttons not found!');
    }

    // 3. Click "▶ Play Lead Sheet" to start melody playback
    const playClickResult = await page.eval(() => {
      const playBtn = document.getElementById('btn-play-leadsheet');
      playBtn.click();
      return {
        isPlaying: playBtn.classList.contains('is-playing'),
        btnText: playBtn.textContent.trim()
      };
    });
    console.log('Play Lead Sheet Click Result:', playClickResult);
    if (!playClickResult.isPlaying) {
      throw new Error('Play Lead Sheet failed to enter playing state!');
    }

    // Wait 600ms to allow event cycle
    await sleep(600);

    // Check that at least one event is highlighted as active
    const activeEventCheck = await page.eval(() => {
      const activeEvent = document.querySelector('.sheet-event.is-active');
      return {
        hasActiveEvent: !!activeEvent,
        lyric: activeEvent ? activeEvent.querySelector('.sheet-lyric-text')?.textContent.trim() : null,
        note: activeEvent ? activeEvent.querySelector('.sheet-note-val')?.textContent.trim() : null
      };
    });
    console.log('Active Event During Playback:', activeEventCheck);

    // Stop playback by clicking again
    const stopClickResult = await page.eval(() => {
      const playBtn = document.getElementById('btn-play-leadsheet');
      playBtn.click();
      return {
        isPlaying: playBtn.classList.contains('is-playing'),
        btnText: playBtn.textContent.trim()
      };
    });
    console.log('Stop Playback Click Result:', stopClickResult);
    if (stopClickResult.isPlaying) {
      throw new Error('Failed to stop playback!');
    }

    // 4. Test MusicXML endpoint directly via fetch in browser
    const xmlFetchResult = await page.eval(async () => {
      const resp = await fetch('/api/export-musicxml', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          notations: [
            { western_note: 'D4', symbol: 'S', frequency_hz: 293.7, start_time: 0.0, end_time: 0.5 },
            { western_note: 'E4', symbol: 'R', frequency_hz: 329.6, start_time: 0.5, end_time: 1.0 }
          ],
          lyrics: 'E-ri aa-li',
          tempo_bpm: 84.0,
          tonic_hz: 146.83,
          instrument: 'piano'
        })
      });
      const text = await resp.text();
      return {
        status: resp.status,
        contentType: resp.headers.get('content-type'),
        hasXmlDeclaration: text.includes('<?xml'),
        hasScorePartwise: text.includes('<score-partwise'),
        hasStepD: text.includes('<step>D</step>'),
        hasStepE: text.includes('<step>E</step>')
      };
    });
    console.log('MusicXML Fetch Check:', xmlFetchResult);
    if (xmlFetchResult.status !== 200 || !xmlFetchResult.hasScorePartwise) {
      throw new Error('MusicXML endpoint check failed!');
    }

    console.log('\n--- ALL LEAD SHEET PLAYBACK & MUSICXML TESTS PASSED! ---');
  } catch (err) {
    console.error('Test FAILED:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
