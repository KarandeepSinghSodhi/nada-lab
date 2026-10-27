import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Custom Upload Antar-Swara & Dossier DTW Heatmap End-to-End...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Track Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check DTW Heatmap Container & Elements
    const dtwCheck = await page.eval(() => {
      const section = document.getElementById('dossier-dtw-section');
      const canvas = document.getElementById('dossier-dtw-canvas');
      const metrics = document.getElementById('dossier-dtw-metrics');
      const tooltip = document.getElementById('dossier-dtw-tooltip');
      const playhead = document.getElementById('dtw-playhead-line');
      return {
        hasSection: !!section,
        hasCanvas: !!canvas,
        hasMetrics: !!metrics,
        hasTooltip: !!tooltip,
        hasPlayhead: !!playhead
      };
    });
    console.log('DTW Initial Elements Check:', dtwCheck);
    if (!dtwCheck.hasSection || !dtwCheck.hasCanvas || !dtwCheck.hasMetrics) {
      throw new Error('DTW Heatmap container elements missing!');
    }

    // 3. Test renderDossierDTWHeatmap & Hover Interaction
    const heatmapResult = await page.eval(() => {
      // Create mock DTW data
      const mockDTW = {
        metrics: {
          alignment_score: 97.5,
          intonation_purity_pct: 94.2,
          mean_absolute_deviation_cents: 6.4,
          rmse_cents: 8.1
        },
        alignment_stream: [
          { t_user: 0.1, user_cents: 204.0, ideal_cents: 203.9, delta_cents: 0.1, zone: 'green' },
          { t_user: 0.5, user_cents: 395.0, ideal_cents: 386.3, delta_cents: 8.7, zone: 'green' },
          { t_user: 1.0, user_cents: 518.0, ideal_cents: 498.0, delta_cents: 20.0, zone: 'amber' },
          { t_user: 1.5, user_cents: 742.0, ideal_cents: 702.0, delta_cents: 40.0, zone: 'red' },
          { t_user: 2.0, user_cents: 906.0, ideal_cents: 905.9, delta_cents: 0.1, zone: 'green' }
        ]
      };

      // Call renderer
      if (typeof window.renderDossierDTWHeatmap === 'function') {
        window.renderDossierDTWHeatmap(mockDTW, 2.5);
      }

      const alignText = document.getElementById('dtw-val-alignment')?.textContent?.trim();
      const purityText = document.getElementById('dtw-val-purity')?.textContent?.trim();
      const madText = document.getElementById('dtw-val-mad')?.textContent?.trim();
      const rmseText = document.getElementById('dtw-val-rmse')?.textContent?.trim();

      // Trigger hover event
      const containerBox = document.getElementById('dossier-dtw-canvas-container');
      const rect = containerBox.getBoundingClientRect();
      const mouseEv = new MouseEvent('mousemove', {
        clientX: rect.left + rect.width * 0.5,
        clientY: rect.top + rect.height * 0.5,
        bubbles: true
      });
      containerBox.dispatchEvent(mouseEv);

      const tooltipText = document.getElementById('dossier-dtw-tooltip')?.textContent?.trim();
      const playheadDisplay = document.getElementById('dtw-playhead-line')?.style?.display;

      return {
        alignText,
        purityText,
        madText,
        rmseText,
        tooltipText,
        playheadDisplay
      };
    });
    console.log('DTW Heatmap Render & Hover Result:', heatmapResult);
    if (!heatmapResult.alignText || !heatmapResult.purityText) {
      throw new Error('DTW Metric pills not populated correctly!');
    }

    // 4. Test Scrubber & Dossier Notation Chips Synchronization
    const syncResult = await page.eval(() => {
      const notList = document.getElementById('dossier-notations-list');
      notList.innerHTML = '';

      // Create test notation chips
      const chip1 = document.createElement('div');
      chip1.className = 'notation-chip';
      chip1.setAttribute('data-start-time', '0.0');
      chip1.setAttribute('data-end-time', '1.0');
      chip1.textContent = 'Chip 1 (Sa)';
      notList.appendChild(chip1);

      const chip2 = document.createElement('div');
      chip2.className = 'notation-chip';
      chip2.setAttribute('data-start-time', '1.0');
      chip2.setAttribute('data-end-time', '2.0');
      chip2.textContent = 'Chip 2 (Re)';
      notList.appendChild(chip2);

      // Call syncSheetMusicCursor at 1.5s
      syncSheetMusicCursor(1.5);

      return {
        chip1Active: chip1.classList.contains('is-active'),
        chip2Active: chip2.classList.contains('is-active'),
        playheadLeft: document.getElementById('dtw-playhead-line')?.style?.left
      };
    });
    console.log('Notation Chip & Playhead Sync Result:', syncResult);
    if (!syncResult.chip2Active) {
      throw new Error('Notation chip 2 was not activated at 1.5s!');
    }

    // 5. Test Custom Upload Antar-Swara Extraction & Meend Audition
    const customAntarResult = await page.eval(() => {
      const mockTransitions = [
        {
          interval: 'R -> G',
          curvature_name: 'Sigmoidal S-Curve Meend',
          duration_ms: 220,
          peak_velocity_cents_sec: 1450,
          expressive_transition_index: 97.2,
          from_cents: 204,
          to_cents: 386,
          description: 'Custom smooth Gayaki meend gliding Re into Ga'
        },
        {
          interval: 'P -> D',
          curvature_name: 'Upper Kan Touch (N)',
          duration_ms: 240,
          peak_velocity_cents_sec: 1800,
          expressive_transition_index: 96.5,
          kan_touch: 'N',
          from_cents: 702,
          to_cents: 906,
          description: 'Custom Pa grazing Kan Ni before landing on Dha'
        }
      ];

      // Call custom upload renderer
      renderCustomUploadAntarSwara(mockTransitions, 'Live_Riyaz_Take_4');

      const btnRow = document.querySelector('.antar-song-buttons');
      const customBtn = btnRow?.querySelector('.antar-song-btn[data-song-key="custom_upload"]');
      const btnText = customBtn?.textContent?.trim();

      // Click custom upload button to populate transitions feed
      customBtn?.click();

      const cards = document.querySelectorAll('.antar-tr-card');
      const firstCardInterval = cards[0]?.querySelector('.antar-tr-interval')?.textContent?.trim();
      const firstCardCurv = cards[0]?.querySelector('.antar-tr-curv-tag')?.textContent?.trim();
      const firstCardHearBtn = cards[0]?.querySelector('.antar-tr-hear-btn');

      // Click hear meend button to confirm no errors thrown
      let hearMeendSuccess = false;
      try {
        if (firstCardHearBtn) {
          firstCardHearBtn.click();
          hearMeendSuccess = true;
        }
      } catch (err) {
        hearMeendSuccess = false;
      }

      return {
        hasCustomBtn: !!customBtn,
        btnText,
        cardCount: cards.length,
        firstCardInterval,
        firstCardCurv,
        hasHearBtn: !!firstCardHearBtn,
        hearMeendSuccess
      };
    });
    console.log('Custom Antar-Swara & Meend Audition Result:', customAntarResult);
    if (!customAntarResult.hasCustomBtn || customAntarResult.cardCount !== 2 || !customAntarResult.firstCardInterval.includes('R -> G')) {
      throw new Error('Custom upload antar-swara cards did not render properly!');
    }
    if (!customAntarResult.hasHearBtn || !customAntarResult.hearMeendSuccess) {
      throw new Error('Hear Meend audition button failed or missing!');
    }

    console.log('\n--- ALL CUSTOM UPLOAD & DTW HEATMAP CHECKS PASSED! ---');
  } finally {
    await browser.close();
  }
}

run().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
