import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  console.log('Launching browser to test http://127.0.0.1:8000/ ...');
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  await page.goto('http://127.0.0.1:8000/');
  await sleep(1500);

  // 1. Evaluate runtime health & console errors
  console.log('\n--- 1. Checking Initial Page & Console Status ---');
  if (page.consoleErrors.length > 0) {
    console.error(`FAIL: ${page.consoleErrors.length} console error(s) occurred on page load!`);
    console.error(page.consoleErrors);
  } else {
    console.log('SUCCESS: Page loaded with 0 console errors!');
  }

  // 2. Test functional clicks on key buttons
  console.log('\n--- 2. Testing Real UI Clicks & State Changes ---');
  
  // Test A: Sample button
  const testSampleBtn = await page.eval(async () => {
    const btn = document.getElementById('uploader-sample-btn');
    if (!btn) return { success: false, reason: 'uploader-sample-btn not found' };
    btn.click();
    return { success: true, text: btn.textContent };
  });
  console.log('Test A (Try Sample Phrase Click):', testSampleBtn);
  await sleep(1500);

  // Check if dossier became visible
  const dossierState = await page.eval(() => {
    const el = document.getElementById('instant-track-dossier');
    const isVisible = el && !el.classList.contains('is-hidden');
    const title = el ? document.getElementById('dossier-file-name')?.textContent : null;
    const raga = el ? document.getElementById('dossier-raga-name')?.textContent : null;
    const notesCount = el ? document.querySelectorAll('#dossier-notations-list .notation-chip').length : 0;
    return { isVisible, title, raga, notesCount };
  });
  console.log('Instant Dossier after Sample Click:', dossierState);

  // Test B: Benchmark phrase buttons
  const testPhraseBtns = await page.eval(() => {
    const btns = Array.from(document.querySelectorAll('.ui-phrase-btn'));
    const results = [];
    btns.slice(0, 3).forEach(b => {
      b.click();
      results.push({
        phrase: b.getAttribute('data-phrase'),
        active: b.classList.contains('is-active'),
        badge: document.getElementById('ui-raga-badge')?.textContent
      });
    });
    return results;
  });
  console.log('Test B (Benchmark Phrase Buttons Click):', testPhraseBtns);

  // Test C: Classical / Western Mode Toggle
  const testModeToggle = await page.eval(() => {
    const btn = document.querySelector('.ui-mode-btn[data-mode="western"]');
    if (!btn) return { success: false, reason: 'not found' };
    btn.click();
    return {
      success: true,
      modeActive: btn.classList.contains('is-active'),
      tierName: document.getElementById('ui-tier-name')?.textContent
    };
  });
  console.log('Test C (Western/Classical Mode Toggle Click):', testModeToggle);

  // Test D: Instrument Profile Tabs
  const testInstrumentTabs = await page.eval(() => {
    const fluteTab = document.querySelector('.tracker-inst-btn[data-inst="flute"]');
    if (!fluteTab) return { success: false, reason: 'not found' };
    fluteTab.click();
    const activeProfile = fluteTab.classList.contains('is-active');
    const statusText = document.getElementById('live-tuning-status')?.textContent;
    return { success: true, activeProfile, statusText };
  });
  console.log('Test D (Flute Instrument Tab Click):', testInstrumentTabs);

  // Test E: Tanpura Drone Toggle
  const testDroneToggle = await page.eval(() => {
    const droneBtn = document.getElementById('drone-toggle-btn');
    if (!droneBtn) return { success: false, reason: 'not found' };
    droneBtn.click();
    return {
      success: true,
      droneActive: droneBtn.classList.contains('is-active'),
      btnText: droneBtn.textContent.trim()
    };
  });
  console.log('Test E (Tanpura Drone Toggle Click):', testDroneToggle);

  // Test F: Tala Metronome Toggle
  const testTalaToggle = await page.eval(() => {
    const talaBtn = document.getElementById('tala-toggle-btn');
    if (!talaBtn) return { success: false, reason: 'not found' };
    talaBtn.click();
    return {
      success: true,
      talaActive: talaBtn.classList.contains('is-active'),
      btnText: talaBtn.textContent.trim()
    };
  });
  console.log('Test F (Tala Metronome Toggle Click):', testTalaToggle);

  // Test G: Poster Row Click
  const testPosterRow = await page.eval(() => {
    const rows = Array.from(document.querySelectorAll('.poster-row'));
    return { count: rows.length, texts: rows.map(r => r.querySelector('.poster-name')?.textContent) };
  });
  console.log('Test G (Poster Rows available):', testPosterRow);

  console.log('\n--- Final Browser Errors Summary ---');
  console.log(`Total errors captured: ${page.consoleErrors.length}`);
  if (page.consoleErrors.length > 0) {
    console.log('Errors:', page.consoleErrors);
  }

  await browser.close();
}

run().catch(err => {
  console.error('Test execution failed:', err);
  process.exit(1);
});
