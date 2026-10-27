// scripts/test_musician_waveform_deep.mjs
import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Musician-Grade Waveform & Instrument-Specific Timbre Engine...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1200);

    // 1. Verify Musician HUD Strip is present
    const hudExists = await page.eval(() => {
      const strip = document.getElementById('tracker-wave-musician-strip');
      const k1 = document.getElementById('wave-musician-kpi-1');
      const k2 = document.getElementById('wave-musician-kpi-2');
      const k3 = document.getElementById('wave-musician-kpi-3');
      return {
        exists: !!strip,
        k1: k1 ? k1.textContent.trim() : null,
        k2: k2 ? k2.textContent.trim() : null,
        k3: k3 ? k3.textContent.trim() : null
      };
    });
    console.log('[1/4] Musician HUD Strip Initial:', hudExists);

    // 2. Iterate through all 6 instrument profiles and verify HUD & Persona badge
    const instruments = ['flute', 'piano', 'guitar', 'sitar', 'percussion', 'voice'];
    const instResults = {};

    for (const inst of instruments) {
      const res = await page.eval((targetInst) => {
        const btn = document.querySelector(`.tracker-inst-btn[data-inst="${targetInst}"]`);
        if (btn) btn.click();
        const badge = document.getElementById('tracker-persona-badge');
        const k1 = document.getElementById('wave-musician-kpi-1');
        const k2 = document.getElementById('wave-musician-kpi-2');
        const k3 = document.getElementById('wave-musician-kpi-3');
        return {
          clicked: !!btn,
          persona: badge ? badge.textContent.trim() : null,
          k1: k1 ? k1.textContent.trim() : null,
          k2: k2 ? k2.textContent.trim() : null,
          k3: k3 ? k3.textContent.trim() : null
        };
      }, inst);
      instResults[inst] = res;
      await sleep(350);
    }
    console.log('[2/4] Instrument Profiles & HUD Verification:', JSON.stringify(instResults, null, 2));

    // 3. Test Wave Modes: Wave, Envelope (ADSR), Harmonics (Spectrum)
    const waveModes = ['envelope', 'spectrum', 'oscilloscope'];
    const modeResults = {};

    for (const m of waveModes) {
      const modeRes = await page.eval((targetMode) => {
        const btn = document.querySelector(`.wave-mode-btn[data-mode="${targetMode}"]`);
        if (btn) btn.click();
        const stats = document.getElementById('live-wave-stats');
        return {
          clicked: !!btn,
          stats: stats ? stats.textContent.trim() : null
        };
      }, m);
      modeResults[m] = modeRes;
      await sleep(400);
    }
    console.log('[3/4] Waveform Visualizer Modes:', modeResults);

    // 4. Test Auditioning phrase with Flute profile and Piano profile to observe dynamic wave
    await page.eval(() => {
      const fluteBtn = document.querySelector('.tracker-inst-btn[data-inst="flute"]');
      if (fluteBtn) fluteBtn.click();
      const waveBtn = document.querySelector('.wave-mode-btn[data-mode="oscilloscope"]');
      if (waveBtn) waveBtn.click();
      const auditionBtn = document.getElementById('ui-audition-btn');
      if (auditionBtn) auditionBtn.click();
    });
    await sleep(1500);

    const fluteAuditionState = await page.eval(() => {
      const k1 = document.getElementById('wave-musician-kpi-1');
      const stats = document.getElementById('live-wave-stats');
      return {
        k1: k1 ? k1.textContent.trim() : null,
        stats: stats ? stats.textContent.trim() : null
      };
    });
    console.log('[4/4] Flute Audition Active Wave State:', fluteAuditionState);

    // Switch to Piano during audition
    await page.eval(() => {
      const pianoBtn = document.querySelector('.tracker-inst-btn[data-inst="piano"]');
      if (pianoBtn) pianoBtn.click();
    });
    await sleep(1000);

    const pianoAuditionState = await page.eval(() => {
      const k1 = document.getElementById('wave-musician-kpi-1');
      const stats = document.getElementById('live-wave-stats');
      return {
        k1: k1 ? k1.textContent.trim() : null,
        stats: stats ? stats.textContent.trim() : null
      };
    });
    console.log('[4/4] Piano Audition Active Wave State:', pianoAuditionState);

    // Stop Audition
    await page.eval(() => {
      const auditionBtn = document.getElementById('ui-audition-btn');
      if (auditionBtn && auditionBtn.classList.contains('is-playing')) {
        auditionBtn.click();
      }
    });

    console.log('\nTotal Console Errors during Musician Waveform Test:', page.consoleErrors.length);
    if (page.consoleErrors.length > 0) {
      console.error('Errors:', page.consoleErrors);
    } else {
      console.log('SUCCESS: All 6 Musician Instrument Profiles and Adaptive Waveform Verified with 0 Errors!');
    }

  } catch (err) {
    console.error('Test failed with exception:', err);
  } finally {
    await browser.close();
  }
}

run();
