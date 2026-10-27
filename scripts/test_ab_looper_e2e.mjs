import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Interactive A-B Looper & Variable Speed Riyaz Engine...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Check A-B Looper Bar presence
    const looperCheck = await page.eval(() => {
      const bar = document.querySelector('.ui-ab-looper-bar');
      const btnA = document.getElementById('btn-set-loop-a');
      const btnB = document.getElementById('btn-set-loop-b');
      const btnToggle = document.getElementById('btn-toggle-loop');
      const valA = document.getElementById('loop-a-val');
      const valB = document.getElementById('loop-b-val');
      const speedBtns = Array.from(document.querySelectorAll('.ab-speed-btn')).map(b => b.textContent.trim());

      return {
        hasBar: !!bar,
        hasBtnA: !!btnA,
        hasBtnB: !!btnB,
        hasToggle: !!btnToggle,
        valA: valA ? valA.textContent.trim() : null,
        valB: valB ? valB.textContent.trim() : null,
        speeds: speedBtns
      };
    });
    console.log('Looper Bar Initial State:', looperCheck);
    if (!looperCheck.hasBar || !looperCheck.hasToggle) {
      throw new Error('Looper Bar not found!');
    }

    // 2. Test Speed Selector
    const speedSelect = await page.eval(() => {
      const btn05 = document.querySelector('.ab-speed-btn[data-speed="0.5"]');
      if (btn05) btn05.click();
      return {
        is05Active: btn05 ? btn05.classList.contains('is-active') : false
      };
    });
    console.log('Speed 0.5x Selection:', speedSelect);
    if (!speedSelect.is05Active) throw new Error('Speed selector failed!');

    // 3. Test Loop Toggle
    const toggleStart = await page.eval(() => {
      const btnToggle = document.getElementById('btn-toggle-loop');
      btnToggle.click();
      return {
        isLooping: btnToggle.classList.contains('is-looping'),
        btnText: btnToggle.textContent.trim()
      };
    });
    console.log('Loop Toggle Start:', toggleStart);
    if (!toggleStart.isLooping) throw new Error('Failed to start looping!');

    await sleep(500);

    const toggleStop = await page.eval(() => {
      const btnToggle = document.getElementById('btn-toggle-loop');
      btnToggle.click();
      return {
        isLooping: btnToggle.classList.contains('is-looping'),
        btnText: btnToggle.textContent.trim()
      };
    });
    console.log('Loop Toggle Stop:', toggleStop);
    if (toggleStop.isLooping) throw new Error('Failed to stop looping!');

    // 4. Test Lead Sheet Meend Loop Button
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    const bridgeLoopCheck = await page.eval(() => {
      const loopBtn = document.querySelector('.sheet-loop-meend-btn');
      if (loopBtn) {
        loopBtn.click();
        const mainToggle = document.getElementById('btn-toggle-loop');
        return {
          hasLoopBtn: true,
          mainIsLooping: mainToggle ? mainToggle.classList.contains('is-looping') : false
        };
      }
      return { hasLoopBtn: false };
    });
    console.log('Lead Sheet Meend Loop Check:', bridgeLoopCheck);

    // Stop loop if running
    await page.eval(() => {
      const btnToggle = document.getElementById('btn-toggle-loop');
      if (btnToggle && btnToggle.classList.contains('is-looping')) {
        btnToggle.click();
      }
    });

    console.log('\n--- ALL A-B PRACTICE LOOPER CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test FAILED:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
