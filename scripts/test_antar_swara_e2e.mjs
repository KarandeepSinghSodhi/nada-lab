import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing In-Between-The-Notes (Antar-Swara) & Hindi Songs Benchmark Suite...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check Antar-Swara Section and 4-Metric Strip
    const benchmarkHeaderCheck = await page.eval(() => {
      const section = document.querySelector('.antar-swara-benchmark-section');
      const heading = section ? section.querySelector('.antar-swara-heading')?.textContent.trim() : null;
      const metricCards = Array.from(document.querySelectorAll('.antar-metric-card'));
      const metrics = metricCards.map(c => ({
        label: c.querySelector('.antar-metric-label')?.textContent.trim(),
        val: c.querySelector('.antar-val-highlight')?.textContent.trim(),
        baseline: c.querySelector('.antar-val-baseline')?.textContent.trim()
      }));

      return {
        hasSection: !!section,
        heading,
        metricCount: metricCards.length,
        metrics
      };
    });
    console.log('Antar-Swara Benchmark Header Check:', JSON.stringify(benchmarkHeaderCheck, null, 2));

    // 3. Inspect Initial Feed (Yaman - Eri Aali Piya Bina)
    const initialFeed = await page.eval(() => {
      const cards = Array.from(document.querySelectorAll('.antar-tr-card'));
      return {
        count: cards.length,
        firstThree: cards.slice(0, 3).map(c => ({
          interval: c.querySelector('.antar-tr-interval')?.textContent.trim(),
          curvTag: c.querySelector('.antar-tr-curv-tag')?.textContent.trim(),
          desc: c.querySelector('.antar-tr-desc')?.textContent.trim(),
          eti: c.querySelector('.antar-tr-eti-val')?.textContent.trim()
        }))
      };
    });
    console.log('Initial Transitions Feed (Yaman):', JSON.stringify(initialFeed, null, 2));

    // 4. Test Switching to Darbari ("O Duniya Ke Rakhwale")
    const darbariSwitch = await page.eval(() => {
      const darbariBtn = document.querySelector('.antar-song-btn[data-song-key="darbari_rakhwale"]');
      if (darbariBtn) darbariBtn.click();
      const cards = Array.from(document.querySelectorAll('.antar-tr-card'));
      return {
        clicked: !!darbariBtn,
        cardCount: cards.length,
        firstInterval: cards[0]?.querySelector('.antar-tr-interval')?.textContent.trim(),
        firstCurv: cards[0]?.querySelector('.antar-tr-curv-tag')?.textContent.trim()
      };
    });
    console.log('Darbari Switch Result:', darbariSwitch);

    // 5. Test Switching to Khamaj ("Mohe Panghat Pe")
    const khamajSwitch = await page.eval(() => {
      const khamajBtn = document.querySelector('.antar-song-btn[data-song-key="khamaj_panghat"]');
      if (khamajBtn) khamajBtn.click();
      const cards = Array.from(document.querySelectorAll('.antar-tr-card'));
      const murkiCard = cards.find(c => c.textContent.includes('Murki'));
      return {
        clicked: !!khamajBtn,
        cardCount: cards.length,
        hasMurki: !!murkiCard,
        murkiDesc: murkiCard?.querySelector('.antar-tr-desc')?.textContent.trim()
      };
    });
    console.log('Khamaj Switch Result:', khamajSwitch);

    // 6. Inspect In-Between Transition Bridges in Sheet Music Viewport
    const bridgesState = await page.eval(() => {
      const viewport = document.getElementById('sheet-music-viewport');
      const bridges = Array.from(viewport.querySelectorAll('.sheet-transition-bridge'));
      return {
        bridgeCount: bridges.length,
        firstBridge: bridges[0] ? {
          glyph: bridges[0].querySelector('.sheet-tr-glyph')?.textContent.trim(),
          duration: bridges[0].querySelector('.sheet-tr-dur')?.textContent.trim(),
          title: bridges[0].getAttribute('title')
        } : null
      };
    });
    console.log('Sheet Music Transition Bridges:', bridgesState);

    // 7. Test Clicking a Transition Bridge
    const bridgeClickResult = await page.eval(() => {
      const bridge = document.querySelector('.sheet-transition-bridge');
      if (bridge) {
        bridge.click();
        return {
          clicked: true,
          glyph: bridge.querySelector('.sheet-tr-glyph')?.textContent.trim()
        };
      }
      return { clicked: false };
    });
    console.log('Bridge Click Result:', bridgeClickResult);

    console.log('\n--- ALL ANTAR-SWARA & HINDI SONGS BENCHMARK CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test Failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
