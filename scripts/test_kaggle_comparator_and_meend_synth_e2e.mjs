import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Kaggle Baseline Comparator & Meend Synthesis End-to-End...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Track Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check Comparator Button
    const btnCheck = await page.eval(() => {
      const btn = document.getElementById('btn-open-kaggle-comparator');
      const modal = document.getElementById('kaggle-comparator-modal');
      return {
        hasBtn: !!btn,
        hasModal: !!modal,
        isModalHidden: modal?.classList.contains('is-hidden')
      };
    });
    console.log('Comparator Button Initial Check:', btnCheck);
    if (!btnCheck.hasBtn || !btnCheck.hasModal || !btnCheck.isModalHidden) {
      throw new Error('Comparator button or modal missing!');
    }

    // 3. Open Kaggle Comparator Modal
    const openCheck = await page.eval(async () => {
      const btn = document.getElementById('btn-open-kaggle-comparator');
      btn.click();
      await new Promise(r => setTimeout(r, 600));

      const modal = document.getElementById('kaggle-comparator-modal');
      const title = document.getElementById('kaggle-modal-title')?.textContent?.trim();
      const naiveCard = document.querySelector('.kaggle-panel-naive');
      const songlabCard = document.querySelector('.kaggle-panel-songlab');
      const btnKaggle = document.getElementById('btn-audition-kaggle-discrete');
      const btnSonglab = document.getElementById('btn-audition-songlab-meend');
      const samples = document.querySelectorAll('.kaggle-sample-item');
      const deltaBadges = document.querySelectorAll('.delta-gain-pill');

      return {
        isVisible: modal && !modal.classList.contains('is-hidden'),
        title,
        hasNaiveCard: !!naiveCard,
        hasSonglabCard: !!songlabCard,
        hasKaggleBtn: !!btnKaggle,
        hasSonglabBtn: !!btnSonglab,
        sampleCount: samples.length,
        badgeCount: deltaBadges.length
      };
    });
    console.log('Kaggle Comparator Modal Open Result:', openCheck);
    if (!openCheck.isVisible || !openCheck.hasNaiveCard || !openCheck.hasSonglabCard) {
      throw new Error('Kaggle Comparator Modal failed to render properly!');
    }

    // 4. Test Auditioning Naive Kaggle Quantized Beeps
    const kaggleAudio = await page.eval(() => {
      const btn = document.getElementById('btn-audition-kaggle-discrete');
      if (!btn) return { clicked: false };
      btn.click();
      return { clicked: true };
    });
    console.log('Audition Kaggle Discrete Beeps:', kaggleAudio);

    // 5. Test Auditioning Song Lab Continuous Gayaki Meend
    const songlabAudio = await page.eval(() => {
      const btn = document.getElementById('btn-audition-songlab-meend');
      if (!btn) return { clicked: false };
      btn.click();
      return { clicked: true };
    });
    console.log('Audition Song Lab Continuous Meend:', songlabAudio);

    // 6. Test Dismissing Modal
    const closeCheck = await page.eval(() => {
      const closeBtn = document.getElementById('btn-close-kaggle-comparator');
      closeBtn.click();
      const modal = document.getElementById('kaggle-comparator-modal');
      return { isHidden: modal?.classList.contains('is-hidden') };
    });
    console.log('Modal Close Result:', closeCheck);
    if (!closeCheck.isHidden) {
      throw new Error('Comparator modal failed to close!');
    }

    // 7. Test Lead Sheet Playback with Meend Synthesis
    const playbackCheck = await page.eval(async () => {
      const playBtn = document.getElementById('btn-play-leadsheet');
      playBtn.click();
      await new Promise(r => setTimeout(r, 600));

      const isPlaying = playBtn.classList.contains('is-playing');
      const activeEvent = document.querySelector('.sheet-event.is-active');

      playBtn.click(); // stop
      return {
        isPlaying,
        hasActiveEvent: !!activeEvent
      };
    });
    console.log('Lead Sheet Playback Check:', playbackCheck);
    if (!playbackCheck.isPlaying) {
      throw new Error('Lead sheet playback failed to start!');
    }

    console.log('\n--- ALL KAGGLE COMPARATOR & MEEND SYNTHESIS CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test Failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
