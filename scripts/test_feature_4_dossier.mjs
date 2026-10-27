import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Feature 4: Track Dossier & Transcriptions Ribbon...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1200);

    // 1. Switch to Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(400);

    // 2. Click "Try Sample Phrase" in Dossier
    const loadSampleResult = await page.eval(() => {
      const sampleBtn = document.getElementById('uploader-sample-btn');
      if (sampleBtn) {
        sampleBtn.click();
        return { clicked: true, text: sampleBtn.textContent.trim() };
      }
      return { clicked: false };
    });
    console.log('Load Sample Result:', loadSampleResult);
    await sleep(1200);

    // 3. Inspect Dossier 4-Metric Strip
    const dossierMetrics = await page.eval(() => {
      const ragaName = document.getElementById('dossier-raga-name');
      const ragaMeta = document.getElementById('dossier-raga-meta');
      const tonicHz = document.getElementById('dossier-tonic-hz');
      const tonicNote = document.getElementById('dossier-tonic-note');
      const bpmVal = document.getElementById('dossier-bpm-val');
      const talaName = document.getElementById('dossier-tala-name');
      const accuracyVal = document.getElementById('dossier-accuracy-val');
      const notesCount = document.getElementById('dossier-notes-count');
      const critiqueText = document.getElementById('dossier-critique-text');
      const drillText = document.getElementById('dossier-drill-text');
      return {
        raga: ragaName ? ragaName.textContent.trim() : null,
        ragaMeta: ragaMeta ? ragaMeta.textContent.trim() : null,
        tonicHz: tonicHz ? tonicHz.textContent.trim() : null,
        tonicNote: tonicNote ? tonicNote.textContent.trim() : null,
        bpm: bpmVal ? bpmVal.textContent.trim() : null,
        tala: talaName ? talaName.textContent.trim() : null,
        accuracy: accuracyVal ? accuracyVal.textContent.trim() : null,
        notesCount: notesCount ? notesCount.textContent.trim() : null,
        critique: critiqueText ? critiqueText.textContent.trim() : null,
        drill: drillText ? drillText.textContent.trim() : null
      };
    });
    console.log('Dossier 4-Metric Strip & Critique:', dossierMetrics);

    // 4. Inspect Transcribed Notation Chips
    const notesResult = await page.eval(() => {
      const chips = Array.from(document.querySelectorAll('.notation-chip'));
      const chipDetails = chips.map(c => ({
        sargam: c.querySelector('.chip-swara')?.textContent.trim(),
        western: c.querySelector('.chip-western')?.textContent.trim(),
        cents: c.querySelector('.chip-cents')?.textContent.trim(),
        time: c.querySelector('.chip-time')?.textContent.trim()
      }));
      return {
        count: chips.length,
        firstThree: chipDetails.slice(0, 3)
      };
    });
    console.log('Transcribed Notes:', notesResult);

    // 5. Test clicking a note chip to audition and jump
    const clickNoteResult = await page.eval(() => {
      const chips = document.querySelectorAll('.notation-chip');
      if (chips.length > 2) {
        chips[2].click();
        const scrubber = document.getElementById('phrase-scrubber');
        return {
          clickedIdx: 2,
          scrubValue: scrubber ? scrubber.value : null
        };
      }
      return { clickedIdx: -1 };
    });
    console.log('Click Note Chip Result:', clickNoteResult);
    await sleep(600);

    // 6. Test JSON Export and Print PDF buttons
    const exportActions = await page.eval(() => {
      const jsonBtn = document.getElementById('btn-export-dossier-json');
      const printBtn = document.getElementById('btn-print-dossier-pdf');
      return {
        hasJsonBtn: !!jsonBtn,
        jsonBtnText: jsonBtn ? jsonBtn.textContent.trim() : null,
        hasPrintBtn: !!printBtn,
        printBtnText: printBtn ? printBtn.textContent.trim() : null
      };
    });
    console.log('Export Actions:', exportActions);

    console.log('\nTotal console errors during Feature 4 test:', page.consoleErrors.length);
    if (page.consoleErrors.length > 0) {
      console.error('Console errors:', page.consoleErrors);
    } else {
      console.log('PERFECT: Feature 4 (Track Dossier & Transcriptions) passed with 0 errors!');
    }

  } catch (err) {
    console.error('Test failed with exception:', err);
  } finally {
    await browser.close();
  }
}

run();
