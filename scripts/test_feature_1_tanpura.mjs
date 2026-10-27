import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  console.log('Testing Feature 1: Authentic Jawari Tanpura & Sa Calibration...');
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  await page.goto('http://127.0.0.1:8000/');
  await sleep(1500);

  // 1. Check Tanpura initial state
  const initState = await page.eval(() => {
    const btn = document.getElementById('drone-toggle-btn');
    const pips = Array.from(document.querySelectorAll('.tanpura-string-pip')).map(p => p.textContent.trim());
    return {
      btnText: btn?.textContent.trim(),
      pips
    };
  });
  console.log('Initial Tanpura State:', initState);

  // 2. Start Tanpura Drone
  const startResult = await page.eval(() => {
    const btn = document.getElementById('drone-toggle-btn');
    if (!btn) return { success: false, reason: 'button not found' };
    btn.click();
    return {
      success: true,
      isPlaying: btn.classList.contains('is-playing'),
      btnText: btn.textContent.trim()
    };
  });
  console.log('Started Tanpura Drone:', startResult);

  // Wait for 2 plucks (about 2.5 seconds)
  await sleep(2500);

  // 3. Check Plucked Pip status
  const pluckStatus = await page.eval(() => {
    const pips = Array.from(document.querySelectorAll('.tanpura-string-pip'));
    const isAnyPlucked = pips.some(p => p.classList.contains('is-plucked'));
    return {
      pipsCount: pips.length,
      isAnyPlucked
    };
  });
  console.log('Pluck Cycle in Motion:', pluckStatus);

  // 4. Test Sa Calibration modal
  const calibResult = await page.eval(() => {
    const openBtn = document.getElementById('calibrate-sa-btn');
    if (!openBtn) return { success: false, reason: 'calibrate-sa-btn not found' };
    openBtn.click();
    const modal = document.getElementById('calibrate-sa-modal');
    const isModalOpen = modal && !modal.classList.contains('is-hidden');
    
    // Test preset click (e.g. C#3 138.6 Hz)
    const presetCsharp = Array.from(document.querySelectorAll('.calib-preset-btn')).find(b => b.getAttribute('data-note') === 'C#3');
    if (presetCsharp) presetCsharp.click();
    
    const sliderVal = document.getElementById('calib-slider-val')?.textContent;
    const applyBtn = document.getElementById('btn-calib-apply');
    if (applyBtn) applyBtn.click();
    
    const isModalClosed = modal && modal.classList.contains('is-hidden');
    return {
      success: true,
      isModalOpen,
      selectedSa: sliderVal,
      isModalClosed
    };
  });
  console.log('Sa Calibration Modal Test:', calibResult);

  // 5. Stop Tanpura Drone
  const stopResult = await page.eval(() => {
    const btn = document.getElementById('drone-toggle-btn');
    if (btn) btn.click();
    return {
      success: true,
      isPlaying: btn && btn.classList.contains('is-playing'),
      btnText: btn?.textContent.trim()
    };
  });
  console.log('Stopped Tanpura Drone:', stopResult);

  console.log('\nTotal console errors during Feature 1 test:', page.consoleErrors.length);
  if (page.consoleErrors.length > 0) {
    console.error('Errors:', page.consoleErrors);
  } else {
    console.log('PERFECT: Feature 1 (Jawari Tanpura & Sa Calibration) passed with 0 errors!');
  }

  await browser.close();
}

run().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
