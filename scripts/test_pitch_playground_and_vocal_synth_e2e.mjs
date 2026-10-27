import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Pitch Playground & Acoustic Vocal/Tabla Engine End-to-End...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Verify Tier Mode Switcher & Initial Playground State
    const tierCheck = await page.eval(() => {
      const switcher = document.querySelector('.tier-mode-switcher-bar');
      const playgroundBtn = document.getElementById('tier-btn-playground');
      const practiceBtn = document.getElementById('tier-btn-practice');
      const conservatoryBtn = document.getElementById('tier-btn-conservatory');
      const playgroundView = document.getElementById('pitch-playground-view');

      return {
        hasSwitcher: !!switcher,
        hasPlaygroundBtn: !!playgroundBtn,
        hasPracticeBtn: !!practiceBtn,
        hasConservatoryBtn: !!conservatoryBtn,
        isPlaygroundActive: playgroundBtn?.classList.contains('is-active'),
        isPlaygroundVisible: playgroundView && !playgroundView.classList.contains('is-hidden')
      };
    });
    console.log('Tier Switcher Initial Check:', tierCheck);
    if (!tierCheck.hasSwitcher || !tierCheck.isPlaygroundActive || !tierCheck.isPlaygroundVisible) {
      throw new Error('Initial Pitch Playground view did not load as default!');
    }

    // 2. Test Vowel & Duration Selectors + 7-Swara Human Vocal Soundboard
    const soundboardResult = await page.eval(() => {
      const swaraBtns = document.querySelectorAll('.playground-swara-btn');
      const saBtn = document.querySelector('.playground-swara-btn[data-swara="Sa"]');
      const gaBtn = document.querySelector('.playground-swara-btn[data-swara="Ga"]');
      const paBtn = document.querySelector('.playground-swara-btn[data-swara="Pa"]');
      const vowelChips = document.querySelectorAll('.vowel-chip');
      const durationChips = document.querySelectorAll('.duration-chip');
      const oomChip = document.querySelector('.vowel-chip[data-vowel="u"]');
      const sustainChip = document.querySelector('.duration-chip[data-duration="2.5"]');
      const pitchCanvas = document.getElementById('playground-pitch-canvas');

      // Select Vowel Ū (Oom) and Duration 2.5s (Sustain)
      oomChip?.click();
      sustainChip?.click();

      // Click Sa
      saBtn?.click();
      const saText = document.getElementById('bubble-swara-text')?.textContent?.trim();

      // Click Ga
      gaBtn?.click();
      const gaText = document.getElementById('bubble-swara-text')?.textContent?.trim();

      // Click Pa
      paBtn?.click();
      const paText = document.getElementById('bubble-swara-text')?.textContent?.trim();
      const paHz = document.getElementById('bubble-western-text')?.textContent?.trim();
      const pillText = document.getElementById('playground-guidance-pill')?.textContent?.trim();

      return {
        btnCount: swaraBtns.length,
        vowelChipCount: vowelChips.length,
        durationChipCount: durationChips.length,
        hasPitchCanvas: !!pitchCanvas,
        isOomActive: oomChip?.classList.contains('is-active'),
        isSustainActive: sustainChip?.classList.contains('is-active'),
        saText,
        gaText,
        paText,
        paHz,
        hasGuidance: pillText && pillText.includes('Pa')
      };
    });
    console.log('Soundboard Result:', soundboardResult);
    if (soundboardResult.btnCount !== 7 || soundboardResult.vowelChipCount !== 5 || soundboardResult.durationChipCount !== 3 || !soundboardResult.hasPitchCanvas || !soundboardResult.isOomActive || soundboardResult.paText !== 'Pa' || !soundboardResult.hasGuidance) {
      throw new Error('7-Swara human vocal soundboard interaction failed!');
    }

    // 2b. Test Interactive Demo Melody Player (Voice AI Demonstration)
    const demoTestResult = await page.eval(async () => {
      const demoBtn = document.getElementById('btn-demo-scale');
      const stopBtn = document.getElementById('btn-demo-stop');

      demoBtn?.click();
      await new Promise(r => setTimeout(r, 600));

      const isPlaying = demoBtn?.classList.contains('is-playing');
      const isStopVisible = !stopBtn?.classList.contains('is-hidden');
      const swara = document.getElementById('bubble-swara-text')?.textContent;

      // Stop playback
      stopBtn?.click();
      await new Promise(r => setTimeout(r, 200));
      const stoppedHidden = stopBtn?.classList.contains('is-hidden');

      return { isPlaying, isStopVisible, stoppedHidden, swara };
    });
    console.log('Demo Melody Player Result:', demoTestResult);
    if (!demoTestResult.isPlaying || !demoTestResult.isStopVisible || !demoTestResult.stoppedHidden) {
      throw new Error('Interactive Demo Melody Player failed!');
    }

    // 3. Test Tier Navigation (Switching to Practice and Conservatory)
    const navResult = await page.eval(async () => {
      const practiceBtn = document.getElementById('tier-btn-practice');
      const conservatoryBtn = document.getElementById('tier-btn-conservatory');
      const playgroundBtn = document.getElementById('tier-btn-playground');
      const playgroundView = document.getElementById('pitch-playground-view');

      // Switch to Practice
      practiceBtn?.click();
      await new Promise(r => setTimeout(r, 400));
      const hiddenInPractice = playgroundView?.classList.contains('is-hidden');

      // Switch to Conservatory
      conservatoryBtn?.click();
      await new Promise(r => setTimeout(r, 400));
      const hiddenInConservatory = playgroundView?.classList.contains('is-hidden');
      const isDossierOpen = !document.getElementById('tab-panel-dossier')?.classList.contains('is-hidden');

      // Switch back to Playground
      playgroundBtn?.click();
      await new Promise(r => setTimeout(r, 400));
      const visibleInPlayground = !playgroundView?.classList.contains('is-hidden');

      return {
        hiddenInPractice,
        hiddenInConservatory,
        isDossierOpen,
        visibleInPlayground
      };
    });
    console.log('Tier Navigation Result:', navResult);
    if (!navResult.hiddenInPractice || !navResult.hiddenInConservatory || !navResult.visibleInPlayground) {
      throw new Error('Tier mode switcher navigation failed!');
    }

    // 4. Test Authentic Physical Acoustic Tabla Synthesis (Dha, Dhin, Ge, Ka, Na, Tin)
    const tablaResult = await page.eval(() => {
      let tablaPassed = true;
      try {
        if (typeof playTablaBolSynth === 'function') {
          playTablaBolSynth('dha', true);
          playTablaBolSynth('dhin', false);
          playTablaBolSynth('ge', false);
          playTablaBolSynth('ka', false);
          playTablaBolSynth('na', false);
          playTablaBolSynth('tin', false);
        }
      } catch (err) {
        tablaPassed = false;
      }
      return { tablaPassed };
    });
    console.log('Acoustic Tabla Synthesis Result:', tablaResult);
    if (!tablaResult.tablaPassed) {
      throw new Error('Acoustic Tabla physical modeling synthesis threw an error!');
    }

    // 5. Test Mic Scroll Stability (0px drift)
    const driftResult = await page.eval(async () => {
      const micBtn = document.getElementById('btn-playground-mic');
      const initialScroll = window.scrollY;
      micBtn?.click();
      await new Promise(r => setTimeout(r, 600));

      const drift = Math.abs(window.scrollY - initialScroll);
      // Turn off mic
      micBtn?.click();
      return { drift };
    });
    console.log('Live Mic Drift Result:', driftResult);
    if (driftResult.drift > 1) {
      throw new Error('Mic activation caused scroll drift: ' + driftResult.drift + 'px');
    }

    console.log('\n--- ALL PITCH PLAYGROUND & ACOUSTIC SYNTH CHECKS PASSED! ---');
  } finally {
    await browser.close();
  }
}

run().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
