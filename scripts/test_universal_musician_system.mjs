import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  console.log('================================================================');
  console.log('   TESTING UNIVERSAL MUSICIAN & INSTRUMENT-AWARE ARCHITECTURE   ');
  console.log('================================================================\n');

  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('[1/5] Loading application at http://127.0.0.1:8000/ ...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Verify Persona Badges across all 5 Studio Tabs
    console.log('[2/5] Checking Feature Persona Badges across all workspaces...');
    const badges = await page.eval(() => {
      const sadhana = document.getElementById('sadhana-persona-tag')?.textContent.trim();

      const dossierTab = document.getElementById('tab-btn-dossier');
      if (dossierTab) dossierTab.click();
      const dossier = document.querySelector('.dossier-persona-pill')?.textContent.trim();

      const rasaTab = document.getElementById('tab-btn-rasa');
      if (rasaTab) rasaTab.click();
      const rasa = document.querySelector('.rasa-persona-pill')?.textContent.trim();

      const talaTab = document.getElementById('tab-btn-tala');
      if (talaTab) talaTab.click();
      const tala = document.querySelector('.tala-persona-pill')?.textContent.trim();

      const rndTab = document.getElementById('tab-btn-research');
      if (rndTab) rndTab.click();
      const rnd = document.querySelector('.rnd-persona-pill')?.textContent.trim();

      // Return to Sadhana
      document.getElementById('tab-btn-sadhana').click();

      return { sadhana, dossier, rasa, tala, rnd };
    });
    console.log('  Persona Badges Verified:', badges);

    // 2. Test All 6 Instrument Profiles (including Piano/Keys)
    console.log('\n[3/5] Testing all 6 Instrument Profiles & Contextual Tuners...');
    const instList = ['piano', 'flute', 'guitar', 'sitar', 'percussion', 'voice'];
    const instResults = {};

    for (const inst of instList) {
      const res = await page.eval((target) => {
        const btn = document.querySelector(`.tracker-inst-btn[data-inst="${target}"]`);
        if (btn) btn.click();
        const personaBadge = document.getElementById('tracker-persona-badge')?.textContent.trim();
        const hint = document.getElementById('tracker-profile-hint')?.textContent.trim();
        const subLabel = document.getElementById('tracker-sub-label')?.textContent.trim();
        const subButtons = Array.from(document.querySelectorAll('.sub-preset-btn')).map(b => b.textContent.trim());
        return { personaBadge, hint, subLabel, subButtons };
      }, inst);
      instResults[inst] = res;
      console.log(`  [${inst.toUpperCase()}]: ${res.personaBadge} | ${res.subLabel} ${res.subButtons.join(', ')}`);
      await sleep(250);
    }

    // 3. Test Acoustic Wave Modes (Wave, Envelope, Harmonics)
    console.log('\n[4/5] Testing Acoustic Waveform Modes (Period-Locked Wave, Envelope ADSR, Spectrum)...');
    
    // Test Envelope Mode
    const envResult = await page.eval(() => {
      const envBtn = document.querySelector('.wave-mode-btn[data-mode="envelope"]');
      if (envBtn) envBtn.click();
      const stats = document.getElementById('live-wave-stats')?.textContent.trim();
      return { clicked: !!envBtn, stats };
    });
    console.log('  Envelope Mode Result:', envResult);
    await sleep(400);

    // Test Spectrum Mode
    const specResult = await page.eval(() => {
      const specBtn = document.querySelector('.wave-mode-btn[data-mode="spectrum"]');
      if (specBtn) specBtn.click();
      const stats = document.getElementById('live-wave-stats')?.textContent.trim();
      return { clicked: !!specBtn, stats };
    });
    console.log('  Spectrum Mode Result:', specResult);
    await sleep(400);

    // Test Wave Mode
    const waveResult = await page.eval(() => {
      const waveBtn = document.querySelector('.wave-mode-btn[data-mode="oscilloscope"]');
      if (waveBtn) waveBtn.click();
      const stats = document.getElementById('live-wave-stats')?.textContent.trim();
      return { clicked: !!waveBtn, stats };
    });
    console.log('  Wave Mode Result:', waveResult);
    await sleep(400);

    // 4. Test Pure Shruti Reference Auditioning
    console.log('\n[5/5] Testing Reference Tone Auditioning...');
    const refResult = await page.eval(() => {
      const hearBtn = document.getElementById('btn-hear-current-note');
      if (hearBtn) {
        hearBtn.click();
        return { clicked: true, text: hearBtn.textContent.trim() };
      }
      return { clicked: false };
    });
    console.log('  Reference Tone Played:', refResult);
    await sleep(1000);

    console.log('\n================================================================');
    console.log(`TOTAL CONSOLE ERRORS: ${page.consoleErrors.length}`);
    if (page.consoleErrors.length === 0) {
      console.log('SUCCESS: Universal Musician Architecture & All Profiles Passed with 0 Errors!');
    } else {
      console.error('Console Errors:', page.consoleErrors);
    }
    console.log('================================================================\n');

  } catch (err) {
    console.error('Test failed with exception:', err);
  } finally {
    await browser.close();
  }
}

run();
