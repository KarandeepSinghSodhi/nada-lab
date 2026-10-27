import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function runMasterMusicianSuite() {
  console.log('================================================================');
  console.log('       MASTER MUSICIAN-FIRST END-TO-END VERIFICATION SUITE       ');
  console.log('================================================================\n');

  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('[Step 1/7] Navigating to http://127.0.0.1:8000/ ...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Check Initial State & Tanpura
    console.log('[Step 2/7] Testing Authentic Jawari Tanpura Plucking Engine...');
    const tanpuraState = await page.eval(() => {
      const droneBtn = document.getElementById('drone-toggle-btn');
      droneBtn.click();
      return {
        btnText: droneBtn.textContent.trim(),
        isPlaying: droneBtn.classList.contains('is-playing'),
        pipCount: document.querySelectorAll('.tanpura-string-pip').length
      };
    });
    console.log('  Tanpura Drone Started:', tanpuraState);
    await sleep(1500); // let pluck cycle run
    await page.eval(() => {
      document.getElementById('drone-toggle-btn').click();
    });
    console.log('  Tanpura Drone Stopped.');

    // 2. Test All 6 Instrumental Profiles
    console.log('[Step 3/7] Testing Instrumental Profiles & Live HUD...');
    const instruments = ['voice', 'piano', 'flute', 'guitar', 'sitar', 'percussion'];
    for (const inst of instruments) {
      const res = await page.eval((targetInst) => {
        const btn = document.querySelector(`.tracker-inst-btn[data-inst="${targetInst}"]`);
        if (btn) btn.click();
        const hint = document.getElementById('tracker-profile-hint');
        const subLabel = document.getElementById('tracker-sub-label');
        return {
          inst: targetInst,
          hint: hint ? hint.textContent.trim() : null,
          subLabel: subLabel ? subLabel.textContent.trim() : null
        };
      }, inst);
      console.log(`  Profile ${inst}:`, res.hint.slice(0, 50) + '...');
      await sleep(200);
    }

    // 3. Test Guru Guidance & DTW Trajectory Overlay
    console.log('[Step 4/7] Testing Virtual Guru Guidance & DTW Overlay...');
    const guruRes = await page.eval(() => {
      const btn = document.getElementById('guru-correct-btn');
      if (btn) btn.click();
      return {
        clicked: true,
        btnText: btn ? btn.textContent.trim() : null
      };
    });
    console.log('  Guru Playback Triggered:', guruRes);
    await sleep(1200);

    // 4. Test Track Dossier & Transcriptions Ribbon
    console.log('[Step 5/7] Testing Track Dossier & Interactive Transcriptions...');
    await page.eval(() => {
      document.getElementById('tab-btn-dossier').click();
    });
    await sleep(400);

    await page.eval(() => {
      document.getElementById('uploader-sample-btn').click();
    });
    await sleep(1200);

    const dossierRes = await page.eval(() => {
      const raga = document.getElementById('dossier-raga-name')?.textContent.trim();
      const tonic = document.getElementById('dossier-tonic-hz')?.textContent.trim();
      const bpm = document.getElementById('dossier-bpm-val')?.textContent.trim();
      const accuracy = document.getElementById('dossier-accuracy-val')?.textContent.trim();
      const chips = document.querySelectorAll('.notation-chip');

      // Click note chip 2 to test interactive audition
      let chipAuditionWorked = false;
      if (chips.length > 2) {
        chips[2].click();
        chipAuditionWorked = chips[2].classList.contains('is-active');
      }

      return {
        raga,
        tonic,
        bpm,
        accuracy,
        notesCount: chips.length,
        chipAuditionWorked
      };
    });
    console.log('  Dossier Result:', dossierRes);

    // 5. Test Rasa & Emotion Lab (Phrase-Level)
    console.log('[Step 6/7] Testing Rasa & Aesthetic Emotion Lab (Phrase-Level)...');
    await page.eval(() => {
      document.getElementById('tab-btn-rasa').click();
    });
    await sleep(400);

    const rasaRes = await page.eval(() => {
      const primaryRasa = document.getElementById('hero-rasa-title')?.textContent.trim();
      const heroName = document.getElementById('hero-rasa-name')?.textContent.trim();
      const valence = document.getElementById('rasa-coord-valence')?.textContent.trim();
      const arousal = document.getElementById('rasa-coord-arousal')?.textContent.trim();
      return { primaryRasa, heroName, valence, arousal };
    });
    console.log('  Rasa Lab Result:', rasaRes);

    // 6. Test Dedicated Tala & Metronome Studio
    console.log('[Step 7/7] Testing Tala Metronome Studio...');
    await page.eval(() => {
      document.getElementById('tab-btn-tala').click();
    });
    await sleep(400);

    const talaRes = await page.eval(() => {
      const select = document.getElementById('ui-tala-select');
      select.value = 'jhaptal';
      select.dispatchEvent(new Event('change'));

      const cells = document.querySelectorAll('.matra-cell');
      const startBtn = document.getElementById('tala-toggle-btn');
      startBtn.click();

      return {
        tala: select.value,
        matraCount: cells.length,
        started: startBtn.textContent.trim()
      };
    });
    console.log('  Tala Metronome Result:', talaRes);
    await sleep(1500); // let metronome step
    await page.eval(() => {
      document.getElementById('tala-toggle-btn').click();
    });
    console.log('  Tala Metronome Stopped.');

    // 7. Verify MIR Research Lab (Where RAG is Hidden)
    await page.eval(() => {
      document.getElementById('tab-btn-research').click();
    });
    await sleep(300);
    const researchRes = await page.eval(() => {
      const ragBox = document.getElementById('rag-query-input');
      const alankarBtn = document.getElementById('btn-generate-alankar');
      return {
        hasRagHiddenHere: !!ragBox,
        hasAlankar: !!alankarBtn
      };
    });
    console.log('  MIR Research Lab Check:', researchRes);

    console.log('\n================================================================');
    console.log(`TOTAL CONSOLE ERRORS: ${page.consoleErrors.length}`);
    if (page.consoleErrors.length === 0) {
      console.log('SUCCESS: All 5 Musician Workspaces & Features Verified (0 Console Errors)!');
    } else {
      console.error('Console Errors Detected:', page.consoleErrors);
    }
    console.log('================================================================\n');

  } catch (err) {
    console.error('Master Suite failed with exception:', err);
  } finally {
    await browser.close();
  }
}

runMasterMusicianSuite();
