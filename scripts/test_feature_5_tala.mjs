// scripts/test_feature_5_tala.mjs
import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Feature 5: Dedicated Tala & Acoustic Tabla Metronome Studio...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1200);

    // 1. Switch to Tala Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-tala');
      if (tab) tab.click();
    });
    await sleep(400);

    // 2. Check dropdown options for Tala Cycles
    const dropdownOptions = await page.eval(() => {
      const select = document.getElementById('ui-tala-select');
      if (!select) return [];
      return Array.from(select.options).map(o => ({ value: o.value, text: o.text }));
    });
    console.log('Tala Options:', dropdownOptions);

    // 3. Check Sound Timbre options
    const soundOptions = await page.eval(() => {
      const select = document.getElementById('ui-tala-sound-select');
      if (!select) return [];
      return Array.from(select.options).map(o => ({ value: o.value, text: o.text }));
    });
    console.log('Sound Timbre Options:', soundOptions);

    // 4. Verify Dāyān Sa Tuning Pill
    const tuningPillText = await page.eval(() => {
      const pill = document.getElementById('tala-sa-tuning-pill');
      return pill ? pill.textContent.trim() : null;
    });
    console.log('Dāyān Sa Tuning Pill Initial:', tuningPillText);

    // 5. Test Laya Tempo Slider (Vilambit, Madhya, Drut)
    const tempoChecks = await page.eval(() => {
      const slider = document.getElementById('ui-tempo-slider');
      const label = document.getElementById('ui-tempo-val');
      const results = {};

      // Vilambit (< 60)
      slider.value = '52';
      slider.dispatchEvent(new Event('input'));
      results.vilambit = label ? label.textContent.trim() : null;

      // Madhya (60 - 140)
      slider.value = '84';
      slider.dispatchEvent(new Event('input'));
      results.madhya = label ? label.textContent.trim() : null;

      // Drut (> 140)
      slider.value = '160';
      slider.dispatchEvent(new Event('input'));
      results.drut = label ? label.textContent.trim() : null;

      return results;
    });
    console.log('Tempo Laya Checks:', tempoChecks);

    // 6. Test Metronome with Authentic Tabla sound
    await page.eval(() => {
      const select = document.getElementById('ui-tala-sound-select');
      if (select) {
        select.value = 'tabla';
        select.dispatchEvent(new Event('change'));
      }
      const talaSelect = document.getElementById('ui-tala-select');
      if (talaSelect) {
        talaSelect.value = 'teentaal';
        talaSelect.dispatchEvent(new Event('change'));
      }
    });

    const startMetronomeResult = await page.eval(() => {
      const btn = document.getElementById('tala-toggle-btn');
      if (btn) {
        btn.click();
        return { clicked: true, text: btn.textContent.trim() };
      }
      return { clicked: false };
    });
    console.log('Start Metronome (Tabla):', startMetronomeResult);
    await sleep(2000);

    // 7. Switch Timbre live during playback: Mridangam
    await page.eval(() => {
      const select = document.getElementById('ui-tala-sound-select');
      if (select) {
        select.value = 'mridangam';
        select.dispatchEvent(new Event('change'));
      }
    });
    await sleep(1500);

    // 8. Switch Timbre live during playback: Studio Woodblock
    await page.eval(() => {
      const select = document.getElementById('ui-tala-sound-select');
      if (select) {
        select.value = 'woodblock';
        select.dispatchEvent(new Event('change'));
      }
    });
    await sleep(1500);

    // 9. Switch Timbre live during playback: Temple Bell
    await page.eval(() => {
      const select = document.getElementById('ui-tala-sound-select');
      if (select) {
        select.value = 'bell';
        select.dispatchEvent(new Event('change'));
      }
    });
    await sleep(1500);

    // Stop Metronome
    const stopResult = await page.eval(() => {
      const btn = document.getElementById('tala-toggle-btn');
      if (btn) {
        btn.click();
        return { stopped: true, text: btn.textContent.trim() };
      }
      return { stopped: false };
    });
    console.log('Stop Metronome:', stopResult);

    console.log('\nTotal console errors during Feature 5 test:', page.consoleErrors.length);
    if (page.consoleErrors.length > 0) {
      console.error('Console errors:', page.consoleErrors);
    } else {
      console.log('PERFECT: Feature 5 (Tala & Acoustic Tabla Studio) passed with 0 errors!');
    }

  } catch (err) {
    console.error('Test failed with exception:', err);
  } finally {
    await browser.close();
  }
}

run();
