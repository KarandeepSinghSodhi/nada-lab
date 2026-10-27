import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  await page.goto('http://127.0.0.1:8000/');
  await sleep(1500);

  // 1. Poster Row Click
  const posterClickResult = await page.eval(() => {
    const darbariRow = Array.from(document.querySelectorAll('.poster-row')).find(r => r.textContent.includes('DARBARI'));
    if (!darbariRow) return { success: false, reason: 'Darbari row not found' };
    darbariRow.click();
    return {
      success: true,
      rowActive: darbariRow.classList.contains('is-active'),
      inspectorBadge: document.getElementById('ui-raga-badge')?.textContent
    };
  });
  console.log('1. Poster Row Click Result:', posterClickResult);

  // 2. Sādhana vs Studio Workspace Mode Toggle
  const modeSwitchResult = await page.eval(() => {
    const studioBtn = document.getElementById('ws-mode-studio');
    if (!studioBtn) return { success: false, reason: 'ws-mode-studio not found' };
    studioBtn.click();
    const studioActive = studioBtn.classList.contains('is-active');
    const sadhanaBtn = document.getElementById('ws-mode-sadhana');
    sadhanaBtn.click();
    const sadhanaActive = sadhanaBtn.classList.contains('is-active');
    return { success: true, studioActive, sadhanaActive };
  });
  console.log('2. Workspace Mode Switch Result:', modeSwitchResult);

  // 3. Watch Demo Modal Click & Close
  const demoModalResult = await page.eval(() => {
    const demoBtn = document.getElementById('watch-demo-btn');
    if (!demoBtn) return { success: false, reason: 'watch-demo-btn not found' };
    demoBtn.click();
    const modal = document.getElementById('demo-video-modal');
    const isOpened = modal && modal.classList.contains('is-active');
    const closeBtn = document.getElementById('demo-modal-close');
    if (closeBtn) closeBtn.click();
    const isClosed = modal && !modal.classList.contains('is-active');
    return { success: true, isOpened, isClosed };
  });
  console.log('3. Demo Modal Result:', demoModalResult);

  // 4. Guided Tour Modal Click & Close
  const tutorialResult = await page.eval(() => {
    const tutBtn = document.getElementById('start-tutorial-btn');
    if (!tutBtn) return { success: false, reason: 'start-tutorial-btn not found' };
    tutBtn.click();
    const overlay = document.getElementById('tut-spotlight-overlay');
    const isOpened = overlay && overlay.classList.contains('is-active');
    const closeBtn = document.getElementById('tut-close-btn');
    if (closeBtn) closeBtn.click();
    const isClosed = overlay && !overlay.classList.contains('is-active');
    return { success: true, isOpened, isClosed };
  });
  console.log('4. Tutorial Modal Result:', tutorialResult);

  console.log('\nTotal console errors across all tests:', page.consoleErrors.length);
  await browser.close();
}

run().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
