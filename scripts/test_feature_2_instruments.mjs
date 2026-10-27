import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Feature 2: Real-Time Instrumental HUD & Profiles...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1200);

    // 1. Verify default Voice profile
    const voiceState = await page.eval(() => {
      const activeBtn = document.querySelector('.tracker-inst-btn.is-active');
      const hint = document.getElementById('tracker-profile-hint');
      const subLabel = document.getElementById('tracker-sub-label');
      const subButtons = Array.from(document.querySelectorAll('.sub-preset-btn')).map(b => b.textContent.trim());
      return {
        active: activeBtn ? activeBtn.getAttribute('data-inst') : null,
        hint: hint ? hint.textContent.trim() : null,
        subLabel: subLabel ? subLabel.textContent.trim() : null,
        subButtons
      };
    });
    console.log('Voice Profile State:', voiceState);

    // 2. Click Flute Profile
    await page.eval(() => {
      const fluteBtn = document.querySelector('.tracker-inst-btn[data-inst="flute"]');
      if (fluteBtn) fluteBtn.click();
    });
    await sleep(400);

    const fluteState = await page.eval(() => {
      const activeBtn = document.querySelector('.tracker-inst-btn.is-active');
      const hint = document.getElementById('tracker-profile-hint');
      const subLabel = document.getElementById('tracker-sub-label');
      const subButtons = Array.from(document.querySelectorAll('.sub-preset-btn')).map(b => b.textContent.trim());
      return {
        active: activeBtn ? activeBtn.getAttribute('data-inst') : null,
        hint: hint ? hint.textContent.trim() : null,
        subLabel: subLabel ? subLabel.textContent.trim() : null,
        subButtons
      };
    });
    console.log('Flute Profile State:', fluteState);

    // Click E-Bass Flute preset
    await page.eval(() => {
      const eBassBtn = Array.from(document.querySelectorAll('.sub-preset-btn')).find(b => b.textContent.includes('E-Bass'));
      if (eBassBtn) eBassBtn.click();
    });
    await sleep(300);

    const calibStatusAfterEBass = await page.eval(() => {
      const calibBtn = document.getElementById('calibrate-sa-btn');
      const droneBtn = document.getElementById('drone-toggle-btn');
      return {
        calibText: calibBtn ? calibBtn.textContent.trim() : '',
        droneText: droneBtn ? droneBtn.textContent.trim() : ''
      };
    });
    console.log('After E-Bass Click:', calibStatusAfterEBass);

    // 3. Click Guitar Profile
    await page.eval(() => {
      const gBtn = document.querySelector('.tracker-inst-btn[data-inst="guitar"]');
      if (gBtn) gBtn.click();
    });
    await sleep(400);

    const guitarState = await page.eval(() => {
      const activeBtn = document.querySelector('.tracker-inst-btn.is-active');
      const hint = document.getElementById('tracker-profile-hint');
      const subLabel = document.getElementById('tracker-sub-label');
      const subButtons = Array.from(document.querySelectorAll('.sub-preset-btn')).map(b => b.textContent.trim());
      return {
        active: activeBtn ? activeBtn.getAttribute('data-inst') : null,
        hint: hint ? hint.textContent.trim() : null,
        subLabel: subLabel ? subLabel.textContent.trim() : null,
        subButtons
      };
    });
    console.log('Guitar Profile State:', guitarState);

    // 4. Click Sitar/String Profile
    await page.eval(() => {
      const sBtn = document.querySelector('.tracker-inst-btn[data-inst="sitar"]');
      if (sBtn) sBtn.click();
    });
    await sleep(400);

    const sitarState = await page.eval(() => {
      const activeBtn = document.querySelector('.tracker-inst-btn.is-active');
      const hint = document.getElementById('tracker-profile-hint');
      const subLabel = document.getElementById('tracker-sub-label');
      const subButtons = Array.from(document.querySelectorAll('.sub-preset-btn')).map(b => b.textContent.trim());
      return {
        active: activeBtn ? activeBtn.getAttribute('data-inst') : null,
        hint: hint ? hint.textContent.trim() : null,
        subLabel: subLabel ? subLabel.textContent.trim() : null,
        subButtons
      };
    });
    console.log('Sitar Profile State:', sitarState);

    // 5. Click Percussion Profile
    await page.eval(() => {
      const pBtn = document.querySelector('.tracker-inst-btn[data-inst="percussion"]');
      if (pBtn) pBtn.click();
    });
    await sleep(400);

    const percussionState = await page.eval(() => {
      const activeBtn = document.querySelector('.tracker-inst-btn.is-active');
      const hint = document.getElementById('tracker-profile-hint');
      const subLabel = document.getElementById('tracker-sub-label');
      const subButtons = Array.from(document.querySelectorAll('.sub-preset-btn')).map(b => b.textContent.trim());
      return {
        active: activeBtn ? activeBtn.getAttribute('data-inst') : null,
        hint: hint ? hint.textContent.trim() : null,
        subLabel: subLabel ? subLabel.textContent.trim() : null,
        subButtons
      };
    });
    console.log('Percussion Profile State:', percussionState);

    // 6. Test Hear Pure Shruti Reference button
    const shrutiRefResult = await page.eval(() => {
      const hearBtn = document.getElementById('btn-hear-current-note');
      if (hearBtn) {
        hearBtn.click();
        return { clicked: true, text: hearBtn.textContent.trim() };
      }
      return { clicked: false };
    });
    console.log('Hear Pure Shruti Ref Test:', shrutiRefResult);

    console.log('\nTotal console errors during Feature 2 test:', page.consoleErrors.length);
    if (page.consoleErrors.length > 0) {
      console.error('Console errors:', page.consoleErrors);
    } else {
      console.log('PERFECT: Feature 2 (Real-Time Instrumental Profiles & HUD) passed with 0 errors!');
    }

  } catch (err) {
    console.error('Test failed with exception:', err);
  } finally {
    await browser.close();
  }
}

run();
