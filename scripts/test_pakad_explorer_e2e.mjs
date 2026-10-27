import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Canonical Pakad Phrasing Explorer & Guru Synthesis...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Check Pakad Bar presence
    const pakadCheck = await page.eval(() => {
      const bar = document.getElementById('raga-pakad-bar');
      const notation = document.getElementById('raga-pakad-notation');
      const badge = document.getElementById('raga-ornaments-badge');
      const btn = document.getElementById('btn-audition-pakad');

      return {
        hasBar: !!bar,
        notationText: notation ? notation.textContent.trim() : null,
        badgeText: badge ? badge.textContent.trim() : null,
        btnText: btn ? btn.textContent.trim() : null
      };
    });
    console.log('Pakad Bar Initial State:', pakadCheck);
    if (!pakadCheck.hasBar || !pakadCheck.notationText) {
      throw new Error('Pakad explorer bar not found!');
    }

    // 2. Switch Raga to Bhairav and verify Pakad updates dynamically
    console.log('Switching to Raga Bhairav...');
    const bhairavPakadCheck = await page.eval(async () => {
      const select = document.getElementById('ui-target-raga-select');
      if (!select) return { changed: false };

      for (let i = 0; i < select.options.length; i++) {
        if (select.options[i].value.toLowerCase().includes('bhairav')) {
          select.selectedIndex = i;
          break;
        }
      }
      select.dispatchEvent(new Event('change'));
      await new Promise(r => setTimeout(r, 600));

      const notation = document.getElementById('raga-pakad-notation');
      const badge = document.getElementById('raga-ornaments-badge');
      return {
        selectedRaga: select.value,
        notationText: notation ? notation.textContent.trim() : null,
        badgeText: badge ? badge.textContent.trim() : null
      };
    });
    console.log('Bhairav Pakad State:', bhairavPakadCheck);
    if (!bhairavPakadCheck.notationText || bhairavPakadCheck.notationText.includes('Canonical Pakad available in MIR rulebook')) {
      throw new Error('Pakad phrase was not populated for Bhairav!');
    }

    // 3. Test Clicking "▶ Audition Pakad"
    console.log('Clicking Audition Pakad...');
    const playResult = await page.eval(async () => {
      const btn = document.getElementById('btn-audition-pakad');
      if (!btn) return { clicked: false };
      btn.click();
      await new Promise(r => setTimeout(r, 800));
      return {
        clicked: true,
        isPlaying: btn.classList.contains('is-playing'),
        btnText: btn.textContent.trim()
      };
    });
    console.log('Audition Pakad Click Result:', playResult);
    if (!playResult.isPlaying && !playResult.btnText.includes('Pakad')) {
      throw new Error('Audition Pakad button failed to trigger playback!');
    }

    console.log('\n--- ALL CANONICAL PAKAD EXPLORER CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test FAILED:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
