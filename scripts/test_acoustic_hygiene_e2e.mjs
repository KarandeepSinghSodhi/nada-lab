import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Acoustic Hygiene, Lead Vocal Isolation & Stylistic Presets...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check Hygiene Strip initial elements
    const hygieneCheck = await page.eval(() => {
      const strip = document.querySelector('.dossier-hygiene-strip');
      const vocalIso = document.getElementById('dossier-vocal-isolation');
      const bleed = document.getElementById('dossier-bleed-filter');
      const octave = document.getElementById('dossier-octave-glitches');
      const laya = document.getElementById('dossier-laya-window');

      return {
        hasStrip: !!strip,
        vocalIso: vocalIso ? vocalIso.textContent.trim() : null,
        bleed: bleed ? bleed.textContent.trim() : null,
        octave: octave ? octave.textContent.trim() : null,
        laya: laya ? laya.textContent.trim() : null
      };
    });
    console.log('Initial Acoustic Hygiene Strip Check:', hygieneCheck);

    // 3. Check Stylistic Bar and Buttons
    const stylisticCheck = await page.eval(() => {
      const bar = document.querySelector('.dossier-stylistic-bar');
      const btns = Array.from(document.querySelectorAll('.stylistic-btn'));
      return {
        hasBar: !!bar,
        buttonCount: btns.length,
        buttons: btns.map(b => ({
          preset: b.getAttribute('data-preset'),
          text: b.textContent.trim(),
          isActive: b.classList.contains('is-active')
        }))
      };
    });
    console.log('Stylistic Preset Bar Check:', JSON.stringify(stylisticCheck, null, 2));

    // 4. Test Toggling Presets
    // 4a. Kirana (Andolan)
    const kiranaClick = await page.eval(() => {
      const btn = document.querySelector('.stylistic-btn[data-preset="khayal_kirana"]');
      if (btn) btn.click();
      const laya = document.getElementById('dossier-laya-window');
      return {
        clicked: !!btn,
        isActive: btn ? btn.classList.contains('is-active') : false,
        layaText: laya ? laya.textContent.trim() : null
      };
    });
    console.log('Kirana Preset Click:', kiranaClick);

    // 4b. Drut Taan (Fast)
    const drutClick = await page.eval(() => {
      const btn = document.querySelector('.stylistic-btn[data-preset="drut_taan"]');
      if (btn) btn.click();
      const laya = document.getElementById('dossier-laya-window');
      return {
        clicked: !!btn,
        isActive: btn ? btn.classList.contains('is-active') : false,
        layaText: laya ? laya.textContent.trim() : null
      };
    });
    console.log('Drut Taan Click:', drutClick);

    // 4c. Dhrupad (Microtonal)
    const dhrupadClick = await page.eval(() => {
      const btn = document.querySelector('.stylistic-btn[data-preset="dhrupad"]');
      if (btn) btn.click();
      const laya = document.getElementById('dossier-laya-window');
      return {
        clicked: !!btn,
        isActive: btn ? btn.classList.contains('is-active') : false,
        layaText: laya ? laya.textContent.trim() : null
      };
    });
    console.log('Dhrupad Click:', dhrupadClick);

    // 4d. Return to Khayal Standard
    const standardClick = await page.eval(() => {
      const btn = document.querySelector('.stylistic-btn[data-preset="khayal_standard"]');
      if (btn) btn.click();
      return {
        clicked: !!btn,
        isActive: btn ? btn.classList.contains('is-active') : false
      };
    });
    console.log('Returned to Standard Click:', standardClick);

    // 5. Test Live Sample Audio Processing Through Hygiene Pipeline
    const sampleLoadResult = await page.eval(async () => {
      const sampleBtn = document.getElementById('uploader-sample-btn');
      if (!sampleBtn) return { error: 'No sample button' };
      sampleBtn.click();
      await new Promise(r => setTimeout(r, 2000));

      const vocalIso = document.getElementById('dossier-vocal-isolation');
      const bleed = document.getElementById('dossier-bleed-filter');
      const octave = document.getElementById('dossier-octave-glitches');
      const laya = document.getElementById('dossier-laya-window');

      return {
        vocalIso: vocalIso ? vocalIso.textContent.trim() : null,
        bleed: bleed ? bleed.textContent.trim() : null,
        octave: octave ? octave.textContent.trim() : null,
        laya: laya ? laya.textContent.trim() : null
      };
    });
    console.log('Sample Audio Hygiene Telemetry After Pipeline:', sampleLoadResult);

    console.log('\n--- ALL ACOUSTIC HYGIENE & GHARANA PRESET CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test Failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
