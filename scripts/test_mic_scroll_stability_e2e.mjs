import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Live Mic Viewport Scroll Stability...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // Scroll to canvas inspector
    await page.eval(() => {
      const el = document.getElementById('shruti-inspector') || document.querySelector('.ui-canvas-grid');
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
    });
    await sleep(400);

    const initialScrollY = await page.eval(() => window.scrollY);
    console.log(`Initial window.scrollY centered on canvas: ${initialScrollY}px`);

    // Stream 100 simulated pitch frames (equivalent to 1 second of live singing)
    // with rapid alternation between singing notes, glides, pauses, and breath
    const scrollLog = [];

    for (let i = 0; i < 100; i++) {
      const scrollPos = await page.eval((frameIdx) => {
        const isVoiced = (frameIdx % 8) < 6;
        const fakePitch = isVoiced ? (196.0 + Math.sin(frameIdx * 0.2) * 50) : null;
        const data = {
          pitch: fakePitch,
          clarity: isVoiced ? 0.96 : 0.05,
          rms: isVoiced ? (0.05 + Math.abs(Math.sin(frameIdx * 0.1)) * 0.1) : 0.002
        };

        if (typeof window.handleIncomingPitchFrame === 'function') {
          window.handleIncomingPitchFrame(data);
        }

        return window.scrollY;
      }, i);

      scrollLog.push(scrollPos);
      await sleep(10);
    }

    const maxScroll = Math.max(...scrollLog);
    const minScroll = Math.min(...scrollLog);
    const drift = maxScroll - minScroll;

    console.log(`Scroll Positions Range: [${minScroll}px, ${maxScroll}px]`);
    console.log(`Max Viewport Drift during 100 pitch frames: ${drift}px`);

    if (drift !== 0) {
      throw new Error(`FAIL: Viewport shifted by ${drift}px during live mic input!`);
    }

    console.log('SUCCESS: Viewport remained 100% steady (0px drift) during live mic input!');

  } catch (err) {
    console.error('Error during test:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
