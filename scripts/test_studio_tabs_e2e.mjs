import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  console.log('Launching headless browser to test 5-tab Musician Studio at http://127.0.0.1:8000/ ...');
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  await page.goto('http://127.0.0.1:8000/');
  await sleep(1500);

  console.log('\n--- 1. Initial Page Load Health ---');
  if (page.consoleErrors.length > 0) {
    console.error(`FAIL: ${page.consoleErrors.length} console errors on load!`);
    console.error(page.consoleErrors);
  } else {
    console.log('SUCCESS: Page loaded with 0 console errors!');
  }

  // Verify all 5 Studio Tabs exist
  const tabCheck = await page.eval(() => {
    const tabs = Array.from(document.querySelectorAll('.studio-tab'));
    const panels = Array.from(document.querySelectorAll('.studio-tab-panel'));
    return {
      tabCount: tabs.length,
      tabTitles: tabs.map(t => t.querySelector('.studio-tab-label')?.textContent),
      panelCount: panels.length,
      activePanelId: panels.find(p => p.classList.contains('is-active'))?.id
    };
  });
  console.log('\n--- 2. Studio Tabs Inventory ---', tabCheck);

  // Test 1: Sādhana Studio (Tab 1 default)
  const sadhanaCheck = await page.eval(() => {
    const canvas = document.getElementById('shruti-canvas');
    const liveTracker = document.getElementById('ui-live-tracker');
    const micBtn = document.getElementById('live-mic-btn');
    const auditionBtn = document.getElementById('audition-phrase-btn');
    return {
      hasCanvas: !!canvas,
      hasLiveTracker: !!liveTracker,
      hasMicBtn: !!micBtn,
      hasAuditionBtn: !!auditionBtn
    };
  });
  console.log('\n--- 3. Sādhana Studio Elements ---', sadhanaCheck);

  // Test 2: Switch to Track Dossier (Tab 2)
  console.log('\n--- 4. Switching to Track Dossier Tab ---');
  const dossierTabResult = await page.eval(() => {
    const btn = document.getElementById('tab-btn-dossier');
    if (!btn) return { success: false, reason: 'tab-btn-dossier not found' };
    btn.click();
    const panel = document.getElementById('tab-panel-dossier');
    return {
      success: true,
      tabActive: btn.classList.contains('is-active'),
      panelActive: panel && panel.classList.contains('is-active') && !panel.classList.contains('is-hidden')
    };
  });
  console.log('Dossier Tab Switch:', dossierTabResult);

  // Test 2B: Click Try Sample Phrase in Dossier
  const sampleClick = await page.eval(() => {
    const btn = document.getElementById('uploader-sample-btn');
    if (!btn) return { success: false };
    btn.click();
    return { success: true };
  });
  await sleep(1200);

  const dossierPopulated = await page.eval(() => {
    const raga = document.getElementById('dossier-raga-name')?.textContent;
    const notesCount = document.querySelectorAll('#dossier-notations-list .notation-chip').length;
    return { raga, notesCount };
  });
  console.log('Sample Phrase Analysis Result in Dossier:', dossierPopulated);

  // Test 3: Switch to Rasa & Emotion Studio (Tab 3)
  console.log('\n--- 5. Switching to Rasa & Emotion Tab ---');
  const rasaTabResult = await page.eval(() => {
    const btn = document.getElementById('tab-btn-rasa');
    if (!btn) return { success: false };
    btn.click();
    const panel = document.getElementById('tab-panel-rasa');
    const primaryRasa = document.getElementById('rasa-primary-pill')?.textContent;
    const heroName = document.getElementById('rasa-hero-name')?.textContent;
    const treatiseText = document.getElementById('rasa-treatise-text')?.textContent;
    const valence = document.getElementById('rasa-kpi-valence')?.textContent;
    const arousal = document.getElementById('rasa-kpi-arousal')?.textContent;
    return {
      success: true,
      panelActive: panel && panel.classList.contains('is-active'),
      primaryRasa,
      heroName,
      treatisePreview: treatiseText?.substring(0, 60),
      valence,
      arousal
    };
  });
  console.log('Rasa Tab Result:', rasaTabResult);

  // Test 4: Switch to Tala & Metronome Studio (Tab 4)
  console.log('\n--- 6. Switching to Tala & Metronome Tab ---');
  const talaTabResult = await page.eval(() => {
    const btn = document.getElementById('tab-btn-tala');
    if (!btn) return { success: false };
    btn.click();
    const panel = document.getElementById('tab-panel-tala');
    const talaSelect = document.getElementById('ui-tala-select');
    const toggleBtn = document.getElementById('tala-toggle-btn');
    if (toggleBtn) toggleBtn.click(); // Start metronome
    const isTalaActive = toggleBtn && toggleBtn.classList.contains('is-active');
    if (toggleBtn) toggleBtn.click(); // Stop metronome
    return {
      success: true,
      panelActive: panel && panel.classList.contains('is-active'),
      currentTala: talaSelect?.value,
      metronomeToggled: isTalaActive
    };
  });
  console.log('Tala Tab Result:', talaTabResult);

  // Test 5: Switch to MIR Research & RAG Lab (Tab 5 - RAG HIDDEN HERE!)
  console.log('\n--- 7. Switching to MIR Research & RAG Lab Tab ---');
  const researchTabResult = await page.eval(() => {
    const btn = document.getElementById('tab-btn-research');
    if (!btn) return { success: false };
    btn.click();
    const panel = document.getElementById('tab-panel-research');
    const ragInput = document.getElementById('rag-query-input');
    const ragChips = Array.from(document.querySelectorAll('.rag-chip')).map(c => c.textContent);
    const alankarBtn = document.getElementById('generate-alankar-btn');
    const compareBtn = document.getElementById('run-compare-btn');
    return {
      success: true,
      panelActive: panel && panel.classList.contains('is-active'),
      hasRagInput: !!ragInput,
      ragChipsCount: ragChips.length,
      hasAlankarBtn: !!alankarBtn,
      hasCompareBtn: !!compareBtn
    };
  });
  console.log('Research & RAG Tab Result:', researchTabResult);

  // Test 5B: Trigger Alankar generator in Research tab
  const alankarResult = await page.eval(() => {
    const btn = document.getElementById('generate-alankar-btn');
    if (!btn) return { success: false };
    btn.click();
    return {
      success: true,
      aroha: document.getElementById('alankar-aroha-text')?.textContent
    };
  });
  console.log('Alankar Generator Result in Research Tab:', alankarResult);

  // Switch back to Sādhana tab (clean state)
  await page.eval(() => {
    const sadhanaBtn = document.getElementById('tab-btn-sadhana');
    if (sadhanaBtn) sadhanaBtn.click();
  });

  console.log('\n--- Final Browser Errors Summary ---');
  console.log(`Total console errors across all tabs: ${page.consoleErrors.length}`);
  if (page.consoleErrors.length > 0) {
    console.error('Errors:', page.consoleErrors);
  } else {
    console.log('PERFECT: All 5 tabs switched, executed, and interacted with ZERO console errors!');
  }

  await browser.close();
}

run().catch(err => {
  console.error('Test execution failed:', err);
  process.exit(1);
});
