import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Raga Comparator, Diploma Print Engine & Alankar Generator End-to-End...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Test Conservatory Performance Diploma in Track Dossier
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    const diplomaCheck = await page.eval(() => {
      const diploma = document.getElementById('dossier-print-diploma');
      const mockData = {
        scale_and_key: { identified_raga: 'Yaman', thaat: 'Kalyan', tonic_hz: 146.8, tonic_note: 'D3' },
        tempo_and_meter: { bpm: 84.0, suggested_tala: 'Madhya Teentaal' },
        summary_scores: { intonation_accuracy_pct: 97.4, meend_fluidity_pct: 96.8, kan_recall_pct: 100.0, laya_synchrony_pct: 95.2 },
        dtw_comparison: { metrics: { alignment_score: 96.9 } },
        acoustic_hygiene: { vocal_isolation_score_pct: 99.4, lead_vocal_quality: 'Pristine Lead Vocal' },
        transcribed_notations: [
          { symbol: 'S', bhatkhande: 'S', shruti_name: 'Kshiti (1/1)', target_cents: 0.0, cents_deviation: 0.2 },
          { symbol: 'R', bhatkhande: 'R', shruti_name: 'Teevra Re (9/8)', target_cents: 203.9, cents_deviation: 1.1 },
          { symbol: 'G', bhatkhande: 'G', shruti_name: 'Raudri Ga (5/4)', target_cents: 386.3, cents_deviation: 1.8 }
        ],
        phrase_critiques: [
          {
            indian_classical_mode: {
              critique: 'Flawless microtonal intonation adhering strictly to Kalyan thaat.',
              prescriptive_drill: 'Sustain tonic Sa with tanpura overtones.'
            }
          }
        ]
      };

      if (typeof window.populateDossierPrintDiploma === 'function') {
        window.populateDossierPrintDiploma(mockData, 'Riyaz_Take_Master.wav', 3.5, 'Yaman');
      }

      const sealText = document.getElementById('diploma-grade-seal')?.textContent?.trim();
      const intoText = document.getElementById('diploma-intonation-val')?.textContent?.trim();
      const rows = document.querySelectorAll('#diploma-swara-tbody tr');

      return {
        hasDiploma: !!diploma,
        sealText,
        intoText,
        rowCount: rows.length,
        firstRowText: rows[0]?.textContent?.trim()
      };
    });
    console.log('Diploma Initial Check:', diplomaCheck);
    if (!diplomaCheck.hasDiploma || !diplomaCheck.sealText?.includes('DISTINCTION') || diplomaCheck.rowCount !== 3) {
      throw new Error('Conservatory Diploma did not render properly!');
    }

    // 2. Switch to Research & Literature Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-research');
      if (tab) tab.click();
    });
    await sleep(600);

    // 3. Test Head-to-Head Raga Comparator
    const compResult = await page.eval(async () => {
      const sel1 = document.getElementById('compare-raga-1');
      const sel2 = document.getElementById('compare-raga-2');
      const btn = document.getElementById('run-compare-btn');

      if (sel1) sel1.value = 'Yaman';
      if (sel2) sel2.value = 'Bhupali';

      // Click compare button
      btn?.click();
      await new Promise(r => setTimeout(r, 800));

      const resultBox = document.getElementById('raga-comp-result');
      const simText = resultBox?.querySelector('.comp-metric-val')?.textContent?.trim();
      const riskText = resultBox?.querySelector('.comp-risk-pill')?.textContent?.trim();
      const factorsCount = resultBox?.querySelectorAll('.comp-factors-ul li')?.length || 0;
      const adviceText = resultBox?.querySelector('.comp-advice-callout')?.textContent?.trim();

      return {
        hasResult: !resultBox?.classList.contains('is-empty'),
        simText,
        riskText,
        factorsCount,
        hasAdvice: !!adviceText
      };
    });
    console.log('Raga Comparator Result:', compResult);
    if (!compResult.hasResult || !compResult.simText?.includes('71.4%') || !compResult.riskText?.includes('High') || compResult.factorsCount < 2) {
      throw new Error('Raga comparator did not return expected comparison metrics!');
    }

    // 4. Test Alankar / Palta Generator
    const alankarResult = await page.eval(async () => {
      const genBtn = document.getElementById('generate-alankar-btn');
      genBtn?.click();
      await new Promise(r => setTimeout(r, 800));

      const aroha = document.getElementById('alankar-aroha-text')?.textContent?.trim();
      const avaroha = document.getElementById('alankar-avaroha-text')?.textContent?.trim();
      const advice = document.getElementById('alankar-advice-text')?.textContent?.trim();

      return {
        hasAroha: !!aroha && aroha.includes('Arohana'),
        hasAvaroha: !!avaroha && avaroha.includes('Avarohana'),
        hasAdvice: !!advice && advice.length > 10
      };
    });
    console.log('Alankar Generator Result:', alankarResult);
    if (!alankarResult.hasAroha || !alankarResult.hasAvaroha) {
      throw new Error('Alankar Generator failed to generate Palta drills!');
    }

    console.log('\n--- ALL RAGA COMPARATOR, DIPLOMA & ALANKAR CHECKS PASSED! ---');
  } finally {
    await browser.close();
  }
}

run().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
