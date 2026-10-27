import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Interactive Multi-Stem Solo/Mute Mixer...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check Stem Mixer bar presence
    const mixerCheck = await page.eval(() => {
      const bar = document.getElementById('dossier-stem-mixer-bar');
      const btnMix = document.getElementById('stem-btn-mix');
      const btnVocal = document.getElementById('stem-btn-vocal');
      const btnAccomp = document.getElementById('stem-btn-accomp');
      const btnPlay = document.getElementById('btn-play-active-stem');

      return {
        hasBar: !!bar,
        hasMix: !!btnMix,
        hasVocal: !!btnVocal,
        hasAccomp: !!btnAccomp,
        hasPlay: !!btnPlay,
        activeStem: btnMix?.classList.contains('is-active') ? 'mix' : null
      };
    });
    console.log('Stem Mixer Initial Check:', mixerCheck);
    if (!mixerCheck.hasBar || !mixerCheck.hasVocal) {
      throw new Error('Stem mixer bar not found!');
    }

    // 3. Test Clicking Solo Vocal
    const vocalClick = await page.eval(() => {
      const btnVocal = document.getElementById('stem-btn-vocal');
      if (!btnVocal) return { clicked: false };
      btnVocal.click();
      return {
        clicked: true,
        isVocalActive: btnVocal.classList.contains('is-active')
      };
    });
    console.log('Solo Vocal Click Result:', vocalClick);
    if (!vocalClick.isVocalActive) throw new Error('Solo Vocal failed to activate!');

    // 4. Test Clicking Solo Accompaniment Bed
    const accompClick = await page.eval(() => {
      const btnAccomp = document.getElementById('stem-btn-accomp');
      if (!btnAccomp) return { clicked: false };
      btnAccomp.click();
      return {
        clicked: true,
        isAccompActive: btnAccomp.classList.contains('is-active')
      };
    });
    console.log('Solo Accompaniment Click Result:', accompClick);
    if (!accompClick.isAccompActive) throw new Error('Solo Accompaniment failed to activate!');

    // 5. Test Return to Full Mix
    const mixClick = await page.eval(() => {
      const btnMix = document.getElementById('stem-btn-mix');
      if (!btnMix) return { clicked: false };
      btnMix.click();
      return {
        clicked: true,
        isMixActive: btnMix.classList.contains('is-active')
      };
    });
    console.log('Full Mix Click Result:', mixClick);
    if (!mixClick.isMixActive) throw new Error('Full Mix failed to activate!');

    console.log('\n--- ALL MULTI-STEM MIXER CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test FAILED:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
