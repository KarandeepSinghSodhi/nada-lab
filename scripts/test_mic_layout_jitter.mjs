import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1280, height: 800 });

  try {
    console.log('Loading http://127.0.0.1:8000/ ...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // Scroll to canvas
    await page.eval(() => {
      const el = document.getElementById('shruti-inspector') || document.querySelector('.ui-canvas-grid');
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
    });
    await sleep(300);

    const initialScrollY = await page.eval(() => window.scrollY);
    console.log('Initial scrollY at center:', initialScrollY);

    // Let's inspect the bounding rect of live elements before and after simulating voiced vs unvoiced frames
    const testResults = await page.eval(() => {
      const getSizes = () => ({
        scrollY: window.scrollY,
        paneBar: document.querySelector('.ui-pane-bar')?.getBoundingClientRect().height,
        trackerGrid: document.querySelector('.tracker-top-grid')?.getBoundingClientRect().height,
        noteCard: document.querySelector('.tracker-note-card')?.getBoundingClientRect().height,
        gaugeCard: document.querySelector('.tracker-gauge-card')?.getBoundingClientRect().height,
        waveStrip: document.querySelector('.tracker-wave-musician-strip')?.getBoundingClientRect().height,
        waveContainer: document.querySelector('.tracker-wave-container')?.getBoundingClientRect().height,
        liveTracker: document.querySelector('.ui-live-tracker')?.getBoundingClientRect().height,
        canvasTop: document.getElementById('shruti-canvas')?.getBoundingClientRect().top,
        diagPane: document.querySelector('.ui-diagnostic-pane')?.getBoundingClientRect().height
      });

      const initial = getSizes();

      // Trigger voiced note
      const swaraEl = document.getElementById('live-swara-val');
      const kpi3 = document.getElementById('wave-musician-kpi-3');
      const kpi1 = document.getElementById('wave-musician-kpi-1');
      const holdTimer = document.getElementById('live-hold-timer');
      const readoutEl = document.getElementById('ui-cursor-readout');

      // 1. Simulate voiced frame with long text
      if (readoutEl) readoutEl.textContent = 'Live Mic · C(t) = +386.3 cents · v(t) = +412 c/s';
      if (kpi1) kpi1.textContent = 'Vocal Formant: Open Akar';
      if (kpi3) kpi3.textContent = 'Intonation: 22-Shruti Natural Consonance';
      if (holdTimer) holdTimer.textContent = 'Hold: 3.2s (Best: 4.8s)';
      if (swaraEl) swaraEl.textContent = 'Shuddha Ga';

      const voiced = getSizes();

      // 2. Simulate unvoiced frame
      if (readoutEl) readoutEl.textContent = 'Listening for voice... (sing into microphone)';
      if (kpi1) kpi1.textContent = 'Signal: Ambient Standby';
      if (kpi3) kpi3.textContent = 'Acoustic Phase Locked';
      if (holdTimer) holdTimer.textContent = 'Hold: 0.0s';
      if (swaraEl) swaraEl.textContent = 'Sa';

      const unvoiced = getSizes();

      return { initial, voiced, unvoiced };
    });

    console.log('Initial sizes:', testResults.initial);
    console.log('Voiced sizes:', testResults.voiced);
    console.log('Unvoiced sizes:', testResults.unvoiced);

    const canvasDelta = testResults.voiced.canvasTop - testResults.unvoiced.canvasTop;
    const waveStripDelta = testResults.voiced.waveStrip - testResults.unvoiced.waveStrip;
    const noteCardDelta = testResults.voiced.noteCard - testResults.unvoiced.noteCard;
    const paneBarDelta = testResults.voiced.paneBar - testResults.unvoiced.paneBar;

    console.log('Deltas (Voiced vs Unvoiced):');
    console.log('  Canvas Top Shift:', canvasDelta, 'px');
    console.log('  Wave Strip Height Shift:', waveStripDelta, 'px');
    console.log('  Note Card Height Shift:', noteCardDelta, 'px');
    console.log('  Pane Bar Height Shift:', paneBarDelta, 'px');

  } catch (err) {
    console.error('Error running test:', err);
  } finally {
    await browser.close();
  }
}

run();
