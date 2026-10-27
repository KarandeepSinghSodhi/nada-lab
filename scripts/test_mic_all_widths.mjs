import { Browser } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function testWidth(width) {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width, height: 900 });

  try {
    await page.goto('http://127.0.0.1:8000/');
    await new Promise(r => setTimeout(r, 1200));

    const shifts = await page.eval(() => {
      const selectors = [
        '.sadhana-guidance-bar',
        '.raga-pakad-bar',
        '.ui-pane-bar',
        '.ui-live-tracker',
        '.tracker-top-grid',
        '.tracker-note-card',
        '.tracker-gauge-card',
        '.tracker-profile-card',
        '.tracker-wave-container',
        '.tracker-wave-musician-strip',
        '.ui-heatmap-container',
        '.ui-scrubber-row',
        '.ui-ab-looper-bar',
        '.ui-diagnostic-pane',
        '.ui-drill-box',
        '.ui-canvas-grid',
        '#shruti-canvas'
      ];

      const getHeights = () => {
        const res = {};
        selectors.forEach(sel => {
          const el = document.querySelector(sel);
          res[sel] = el ? el.getBoundingClientRect().height : 0;
        });
        return res;
      };

      // State A: Unvoiced / Breath
      const ornamentEl = document.getElementById('ui-ornament-tag');
      const readoutEl = document.getElementById('ui-cursor-readout');
      const sthirataEl = document.getElementById('ui-sthirata-pill');
      const headlineEl = document.getElementById('ui-diag-headline');
      const detailEl = document.getElementById('ui-diag-detail');
      const drillEl = document.getElementById('ui-drill-text');
      const kpi1 = document.getElementById('wave-musician-kpi-1');
      const kpi2 = document.getElementById('wave-musician-kpi-2');
      const kpi3 = document.getElementById('wave-musician-kpi-3');
      const holdTimerEl = document.getElementById('live-hold-timer');
      const swaraEl = document.getElementById('live-swara-val');

      if (readoutEl) readoutEl.textContent = 'Listening for voice... (sing into microphone)';
      if (ornamentEl) ornamentEl.textContent = 'Status: Unvoiced / Breath';
      if (sthirataEl) {
        sthirataEl.textContent = 'Sur Sthirata: --';
        sthirataEl.className = 'ui-pill ui-sthirata-pill';
      }
      if (kpi1) kpi1.textContent = 'Signal: Ambient Standby';
      if (kpi2) kpi2.textContent = 'Tonic: 146.8 Hz';
      if (kpi3) kpi3.textContent = 'Acoustic Phase Locked';
      if (holdTimerEl) holdTimerEl.textContent = 'Hold: 0.0s';
      if (swaraEl) swaraEl.textContent = 'Sa';

      const unvoicedHeights = getHeights();

      // State B: Meend Voiced
      if (readoutEl) readoutEl.textContent = 'Live Mic · C(t) = +386.3 cents · v(t) = +412 c/s';
      if (ornamentEl) ornamentEl.textContent = 'Detected: Meend Glide (412 c/s)';
      if (sthirataEl) {
        sthirataEl.textContent = 'Sur Sthirata: Stable (±8.4c)';
        sthirataEl.className = 'ui-pill ui-sthirata-pill is-stable';
      }
      if (headlineEl) headlineEl.textContent = 'Continuous Meend Transition';
      if (detailEl) detailEl.textContent = 'Voice is gliding smoothly across shruti horizontals without staircase stepping.';
      if (drillEl) drillEl.textContent = 'Decelerate slightly as you arrive on the target swara to land with centered resonance.';
      if (kpi1) kpi1.textContent = 'Vocal Formant: Open Akar';
      if (kpi2) kpi2.textContent = 'Sa Tonic: 146.8 Hz';
      if (kpi3) kpi3.textContent = 'Intonation: 22-Shruti Natural Consonance';
      if (holdTimerEl) holdTimerEl.textContent = 'Hold: 3.4s (Best: 5.2s)';
      if (swaraEl) swaraEl.textContent = 'Shuddha Ga';

      const meendHeights = getHeights();

      // State C: Andolan Voiced
      if (ornamentEl) ornamentEl.textContent = 'Detected: Andolan (Oscillation ±32c)';
      if (headlineEl) headlineEl.textContent = 'Deliberate Microtonal Andolan';
      if (detailEl) detailEl.textContent = 'Oscillation measured around target shruti with authentic classical swing amplitude.';

      const andolanHeights = getHeights();

      const diffs = [];
      selectors.forEach(sel => {
        const u = unvoicedHeights[sel] || 0;
        const m = meendHeights[sel] || 0;
        const a = andolanHeights[sel] || 0;
        if (Math.abs(u - m) > 1 || Math.abs(m - a) > 1 || Math.abs(u - a) > 1) {
          diffs.push({
            selector: sel,
            unvoiced: u,
            meend: m,
            andolan: a,
            maxDiff: Math.max(Math.abs(u - m), Math.abs(m - a), Math.abs(u - a))
          });
        }
      });

      return diffs;
    });

    console.log(`=== Viewport Width: ${width}px ===`);
    if (shifts.length === 0) {
      console.log('No height shifts detected between unvoiced, meend, and andolan states.');
    } else {
      console.log(`Detected ${shifts.length} shifting elements:`);
      shifts.forEach(s => {
        console.log(`  ${s.selector}: unvoiced=${s.unvoiced.toFixed(1)}px, meend=${s.meend.toFixed(1)}px, andolan=${s.andolan.toFixed(1)}px (Delta: ${s.maxDiff.toFixed(1)}px)`);
      });
    }
  } catch (err) {
    console.error('Error:', err);
  } finally {
    await browser.close();
  }
}

async function runAll() {
  for (const w of [1440, 1200, 1024, 768]) {
    await testWidth(w);
  }
}

runAll();
