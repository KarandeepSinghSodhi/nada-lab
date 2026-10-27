import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing 8-Song Benchmark Expansion, Bhatkhande Score, & Live Mic Follower...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // Switch to Dossier tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 1. Verify all 8 benchmark song buttons are present
    const songsCheck = await page.eval(() => {
      const btns = document.querySelectorAll('.antar-song-btn');
      const songKeys = Array.from(btns).map(b => b.getAttribute('data-song-key'));
      return {
        count: btns.length,
        songKeys: songKeys
      };
    });
    console.log('Benchmark Song Buttons Check:', songsCheck);
    if (songsCheck.count < 8) {
      throw new Error(`Expected at least 8 benchmark songs, got ${songsCheck.count}`);
    }

    // 2. Test Clicking Bhoopali Song (Jyoti Kalash Chhalke)
    const bhoopaliClick = await page.eval(() => {
      const btn = document.querySelector('.antar-song-btn[data-song-key="bhoopali_jyoti"]');
      if (!btn) return { clicked: false };
      btn.click();

      const feedCards = document.querySelectorAll('.antar-tr-card');
      const sheetTitle = document.getElementById('sheet-music-title')?.textContent || '';
      const sheetEvents = document.querySelectorAll('.sheet-event');

      return {
        clicked: true,
        feedCardCount: feedCards.length,
        sheetTitle: sheetTitle,
        sheetEventCount: sheetEvents.length,
        firstLyric: sheetEvents[0]?.querySelector('.sheet-lyric-text')?.textContent || ''
      };
    });
    console.log('Bhoopali Song Click Result:', bhoopaliClick);
    if (!bhoopaliClick.clicked || bhoopaliClick.feedCardCount === 0 || !bhoopaliClick.sheetTitle.includes('Jyoti Kalash Chhalke')) {
      throw new Error('Bhoopali benchmark activation failed!');
    }

    // 3. Test Clicking Ahir Bhairav (Poocho Na Kaise)
    const ahirClick = await page.eval(() => {
      const btn = document.querySelector('.antar-song-btn[data-song-key="ahir_bhairav_poocho"]');
      if (!btn) return { clicked: false };
      btn.click();

      const sheetTitle = document.getElementById('sheet-music-title')?.textContent || '';
      const sheetEvents = document.querySelectorAll('.sheet-event');

      return {
        clicked: true,
        sheetTitle: sheetTitle,
        sheetEventCount: sheetEvents.length,
        firstLyric: sheetEvents[0]?.querySelector('.sheet-lyric-text')?.textContent || ''
      };
    });
    console.log('Ahir Bhairav Song Click Result:', ahirClick);
    if (!ahirClick.clicked || !ahirClick.sheetTitle.includes('Poocho Na Kaise')) {
      throw new Error('Ahir Bhairav benchmark activation failed!');
    }

    // 4. Test Bhatkhande Score Modal
    const bhatkhandeCheck = await page.eval(async () => {
      const exportBtn = document.getElementById('btn-export-bhatkhande-score');
      if (!exportBtn) return { hasBtn: false };
      exportBtn.click();

      // Wait a moment for modal render
      await new Promise(r => setTimeout(r, 600));

      const modal = document.getElementById('bhatkhande-score-modal');
      const isVisible = modal && !modal.classList.contains('is-hidden');
      const title = document.getElementById('bk-modal-title')?.textContent || '';
      const hasMeasures = document.querySelectorAll('.bhatkhande-measure').length > 0;
      const hasRawPre = !!document.querySelector('.bhatkhande-raw-pre');

      // Close modal
      const closeBtn = document.getElementById('btn-close-bhatkhande');
      if (closeBtn) closeBtn.click();

      return {
        hasBtn: true,
        isVisible: isVisible,
        title: title,
        hasMeasures: hasMeasures,
        hasRawPre: hasRawPre
      };
    });
    console.log('Bhatkhande Score Check:', bhatkhandeCheck);
    if (!bhatkhandeCheck.hasBtn || !bhatkhandeCheck.isVisible) {
      throw new Error('Bhatkhande score export failed!');
    }

    // 5. Test Live Mic Pitch Follower (Karaoke Highlighting on Lead Sheet)
    const followerCheck = await page.eval(() => {
      // Switch back to Yaman
      const yamanBtn = document.querySelector('.antar-song-btn[data-song-key="yaman_eri_aali"]');
      if (yamanBtn) yamanBtn.click();

      // Click Start Live Mic button or set live active
      const micBtn = document.getElementById('live-mic-btn');
      if (micBtn) {
        micBtn.classList.add('is-active');
      }

      // Simulate a pitch frame corresponding to note 'R' (Re = 200c, ~164.8 Hz at D3)
      if (typeof window.handleIncomingPitchFrame === 'function') {
        window.__mockMicActive = true;
        window.handleIncomingPitchFrame({
          pitch: 164.8,
          clarity: 0.98,
          rms: 0.08
        });
      }

      const activeEvents = document.querySelectorAll('.sheet-event.is-sung-active');
      const feedbackText = document.getElementById('sheet-live-feedback')?.textContent || '';

      return {
        hasActiveSungEvent: activeEvents.length > 0,
        activeEventCount: activeEvents.length,
        feedbackText: feedbackText
      };
    });
    console.log('Live Mic Pitch Follower Check:', followerCheck);
    if (!followerCheck.hasActiveSungEvent) {
      throw new Error('Live mic sheet music follower note highlight failed!');
    }

    console.log('\n--- ALL BENCHMARK, BHATKHANDE & FOLLOWER CHECKS PASSED! ---');

  } catch (err) {
    console.error('Error running test:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
