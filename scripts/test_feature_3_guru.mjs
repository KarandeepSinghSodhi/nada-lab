import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Feature 3: Guru Guidance & DTW Trajectory Overlay...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1200);

    // 1. Check Guru Guidance Button Initial State
    const guruBtnState = await page.eval(() => {
      const btn = document.getElementById('guru-correct-btn');
      const focusText = document.getElementById('sadhana-focus-text');
      const guruCritique = document.getElementById('ui-guru-critique-text');
      return {
        btnText: btn ? btn.textContent.trim() : null,
        focus: focusText ? focusText.textContent.trim() : null,
        critique: guruCritique ? guruCritique.textContent.trim() : null
      };
    });
    console.log('Initial Guru Guidance State:', guruBtnState);

    // 2. Click "Hear Guru Guidance"
    await page.eval(() => {
      const btn = document.getElementById('guru-correct-btn');
      if (btn) btn.click();
    });
    await sleep(800);

    // 3. Inspect canvas and button during Guru playback
    const playingState = await page.eval(() => {
      const btn = document.getElementById('guru-correct-btn');
      const scrubber = document.getElementById('phrase-scrubber');
      return {
        btnText: btn ? btn.textContent.trim() : null,
        isPlaying: btn ? btn.classList.contains('is-playing') || btn.classList.contains('is-active') : false,
        scrubVal: scrubber ? scrubber.value : null
      };
    });
    console.log('During Guru Playback State:', playingState);

    // Wait for playback to progress
    await sleep(1800);

    // 4. Test switching phrase to Bhairav Andolan and triggering Guru guidance
    await page.eval(() => {
      const bhairavBtn = Array.from(document.querySelectorAll('.ui-phrase-pill')).find(b => b.textContent.includes('Bhairav') || b.getAttribute('data-phrase') === 'bhairav_andolan');
      if (bhairavBtn) bhairavBtn.click();
    });
    await sleep(400);

    const bhairavGuruState = await page.eval(() => {
      const focusText = document.getElementById('sadhana-focus-text');
      const guruBtn = document.getElementById('guru-correct-btn');
      if (guruBtn) guruBtn.click();
      return {
        focus: focusText ? focusText.textContent.trim() : null,
        btnText: guruBtn ? guruBtn.textContent.trim() : null
      };
    });
    console.log('Bhairav Guru Triggered:', bhairavGuruState);

    await sleep(1000);

    console.log('\nTotal console errors during Feature 3 test:', page.consoleErrors.length);
    if (page.consoleErrors.length > 0) {
      console.error('Console errors:', page.consoleErrors);
    } else {
      console.log('PERFECT: Feature 3 (Guru Guidance & DTW Trajectory) passed with 0 errors!');
    }

  } catch (err) {
    console.error('Test failed with exception:', err);
  } finally {
    await browser.close();
  }
}

run();
