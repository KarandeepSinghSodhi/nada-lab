import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Navigating to http://127.0.0.1:8000/...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(2000);

    // Scroll down to the canvas inspector workbench so user is viewing the canvas
    await page.eval(() => {
      const inspector = document.getElementById('shruti-inspector') || document.querySelector('.ui-canvas-grid');
      if (inspector) {
        inspector.scrollIntoView({ behavior: 'instant', block: 'center' });
      }
    });
    await sleep(500);

    const initialScrollY = await page.eval(() => window.scrollY);
    console.log('Initial scrollY:', initialScrollY);

    // Now simulate live pitch frames arriving at 50Hz for 3 seconds
    // Alternating between voiced and unvoiced
    const scrollPositions = [];
    const heightChanges = [];

    for (let frame = 0; frame < 60; frame++) {
      const result = await page.eval((f) => {
        const isVoiced = (f % 10) < 7; // 7 frames voiced, 3 frames unvoiced
        const pitch = isVoiced ? (196.0 * Math.pow(2, ((f % 20) * 20) / 1200)) : null; // varying pitch
        const data = {
          pitch: pitch,
          clarity: isVoiced ? 0.95 : 0.1,
          rms: isVoiced ? 0.08 : 0.002
        };

        const gridBefore = document.querySelector('.ui-canvas-grid')?.getBoundingClientRect();
        const diagBefore = document.querySelector('.ui-diagnostic-pane')?.getBoundingClientRect();
        const liveTrackerBefore = document.querySelector('.ui-live-tracker')?.getBoundingClientRect();

        // Call the app's handler directly
        if (typeof window.handleIncomingPitchFrame === 'function') {
          window.handleIncomingPitchFrame(data);
        }

        const gridAfter = document.querySelector('.ui-canvas-grid')?.getBoundingClientRect();
        const diagAfter = document.querySelector('.ui-diagnostic-pane')?.getBoundingClientRect();
        const liveTrackerAfter = document.querySelector('.ui-live-tracker')?.getBoundingClientRect();

        return {
          scrollY: window.scrollY,
          diagHeightDiff: (diagAfter?.height || 0) - (diagBefore?.height || 0),
          trackerHeightDiff: (liveTrackerAfter?.height || 0) - (liveTrackerBefore?.height || 0),
          gridTopDiff: (gridAfter?.top || 0) - (gridBefore?.top || 0)
        };
      }, frame);

      scrollPositions.push(result.scrollY);
      if (Math.abs(result.diagHeightDiff) > 0.5 || Math.abs(result.trackerHeightDiff) > 0.5 || Math.abs(result.gridTopDiff) > 0.5) {
        heightChanges.push({ frame, ...result });
      }
      await sleep(50);
    }

    console.log('Final scrollY:', scrollPositions[scrollPositions.length - 1]);
    console.log('Height / Layout shifts detected:', heightChanges.length);
    if (heightChanges.length > 0) {
      console.log('Sample shifts:', heightChanges.slice(0, 5));
    }

  } catch (err) {
    console.error('Error during test:', err);
  } finally {
    await browser.close();
  }
}

run();
