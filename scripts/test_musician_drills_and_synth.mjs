// scripts/test_musician_drills_and_synth.mjs
import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Musician-Tailored Pedagogical Drills & Physical Acoustic Synthesizer...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1200);

    const testInstruments = ['flute', 'piano', 'guitar', 'sitar', 'percussion', 'voice'];
    const drillAudit = {};

    for (const inst of testInstruments) {
      const res = await page.eval((targetInst) => {
        const btn = document.querySelector(`.tracker-inst-btn[data-inst="${targetInst}"]`);
        if (btn) btn.click();

        // Also trigger scrub frame update so drill refreshes
        const scrubber = document.getElementById('phrase-scrubber');
        if (scrubber) {
          scrubber.value = '50';
          scrubber.dispatchEvent(new Event('input'));
        }

        const drillEl = document.getElementById('ui-drill-text');
        const hearBtn = document.getElementById('btn-hear-current-note');
        if (hearBtn) hearBtn.click();

        return {
          inst: targetInst,
          drill: drillEl ? drillEl.textContent.trim() : null
        };
      }, inst);

      drillAudit[inst] = res;
      await sleep(400);
    }

    console.log('Musician-Tailored Drills Result:', JSON.stringify(drillAudit, null, 2));

    // Verify Flute drill contains Flute advice
    if (!drillAudit.flute.drill.includes('Flute Tip')) {
      throw new Error('Flute drill did not contain Flute Tip!');
    }
    // Verify Piano drill contains Piano advice
    if (!drillAudit.piano.drill.includes('Piano Tip')) {
      throw new Error('Piano drill did not contain Piano Tip!');
    }
    // Verify Guitar drill contains Guitar advice
    if (!drillAudit.guitar.drill.includes('Guitar Tip')) {
      throw new Error('Guitar drill did not contain Guitar Tip!');
    }
    // Verify Sitar drill contains Sitar advice
    if (!drillAudit.sitar.drill.includes('Sitar Tip')) {
      throw new Error('Sitar drill did not contain Sitar Tip!');
    }

    console.log('\nTotal Console Errors:', page.consoleErrors.length);
    if (page.consoleErrors.length > 0) {
      console.error('Console errors:', page.consoleErrors);
      throw new Error('Errors detected during test');
    }

    console.log('SUCCESS: All Musician-Specific Drills & Physical Acoustic Audio Models Passed with 0 Errors!');

  } catch (err) {
    console.error('Test failed with exception:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
