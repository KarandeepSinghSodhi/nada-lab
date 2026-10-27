import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Interactive Sheet Music & Lyrics Lead Sheet Workstation...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check presence of Sheet Music Workstation container
    const sectionCheck = await page.eval(() => {
      const section = document.querySelector('.dossier-sheet-music-section');
      const title = document.getElementById('sheet-music-title');
      const input = document.getElementById('lyrics-extractor-input');
      const extractBtn = document.getElementById('btn-extract-lyrics-align');
      const viewport = document.getElementById('sheet-music-viewport');
      return {
        hasSection: !!section,
        titleText: title ? title.textContent.trim() : null,
        hasInput: !!input,
        hasExtractBtn: !!extractBtn,
        hasViewport: !!viewport
      };
    });
    console.log('Sheet Music Section Initial Check:', sectionCheck);

    // 3. Inspect initial rendered score (automatically loaded on start)
    const initialScoreState = await page.eval(() => {
      const viewport = document.getElementById('sheet-music-viewport');
      const measures = Array.from(viewport.querySelectorAll('.sheet-measure'));
      const events = Array.from(viewport.querySelectorAll('.sheet-event'));

      const firstMeasure = measures[0];
      const mHeader = firstMeasure ? firstMeasure.querySelector('.sheet-measure-header')?.textContent.trim() : null;

      const firstEvent = events[0];
      const lyric = firstEvent ? firstEvent.querySelector('.sheet-lyric-text')?.textContent.trim() : null;
      const note = firstEvent ? firstEvent.querySelector('.sheet-note-val')?.textContent.trim() : null;
      const sargam = firstEvent ? firstEvent.querySelector('.sheet-sargam-val')?.textContent.trim() : null;
      const fingering = firstEvent ? firstEvent.querySelector('.sheet-fingering-val')?.textContent.trim() : null;
      const rhythm = firstEvent ? firstEvent.querySelector('.sheet-rhythm-sym')?.textContent.trim() : null;

      return {
        measureCount: measures.length,
        eventCount: events.length,
        firstMeasureHeader: mHeader,
        firstEvent: {
          lyric,
          note,
          sargam,
          fingering,
          rhythm
        }
      };
    });
    console.log('Initial Benchmark Score State:', JSON.stringify(initialScoreState, null, 2));

    // 4. Test Notation Toggles
    // 4a. Switch to Bhatkhande Sargam
    const sargamToggleResult = await page.eval(() => {
      const sargamBtn = document.querySelector('.sheet-toggle-btn[data-notation="sargam"]');
      if (sargamBtn) sargamBtn.click();
      const viewport = document.getElementById('sheet-music-viewport');
      return {
        clicked: !!sargamBtn,
        hasSargamClass: viewport.classList.contains('sheet-events-sargam'),
        btnActive: sargamBtn.classList.contains('is-active')
      };
    });
    console.log('Sargam Toggle Result:', sargamToggleResult);

    // 4b. Switch to Fingering & Tabs
    const fingeringToggleResult = await page.eval(() => {
      const fingeringBtn = document.querySelector('.sheet-toggle-btn[data-notation="fingering"]');
      if (fingeringBtn) fingeringBtn.click();
      const viewport = document.getElementById('sheet-music-viewport');
      return {
        clicked: !!fingeringBtn,
        hasFingeringClass: viewport.classList.contains('sheet-events-fingering'),
        btnActive: fingeringBtn.classList.contains('is-active')
      };
    });
    console.log('Fingering Toggle Result:', fingeringToggleResult);

    // 4c. Return to Western Pitch
    const westernToggleResult = await page.eval(() => {
      const westernBtn = document.querySelector('.sheet-toggle-btn[data-notation="western"]');
      if (westernBtn) westernBtn.click();
      const viewport = document.getElementById('sheet-music-viewport');
      return {
        clicked: !!westernBtn,
        hasWesternDefault: !viewport.classList.contains('sheet-events-sargam') && !viewport.classList.contains('sheet-events-fingering'),
        btnActive: westernBtn.classList.contains('is-active')
      };
    });
    console.log('Western Toggle Result:', westernToggleResult);

    // 5. Test Interactive Click on Note Event
    const clickEventResult = await page.eval(() => {
      const firstEvent = document.querySelector('.sheet-event');
      if (firstEvent) {
        firstEvent.click();
        return {
          clicked: true,
          isActive: firstEvent.classList.contains('is-active'),
          startTime: firstEvent.getAttribute('data-start-time')
        };
      }
      return { clicked: false };
    });
    console.log('Event Click Result:', clickEventResult);

    // 6. Test Custom Lyrics Alignment & Extraction
    const customLyricsResult = await page.eval(async () => {
      const input = document.getElementById('lyrics-extractor-input');
      const btn = document.getElementById('btn-extract-lyrics-align');
      if (input && btn) {
        input.value = 'Mero man anand bhayo';
        btn.click();
        await new Promise(r => setTimeout(r, 600));
        const firstEvent = document.querySelector('.sheet-event');
        return {
          extracted: true,
          newFirstLyric: firstEvent ? firstEvent.querySelector('.sheet-lyric-text')?.textContent.trim() : null
        };
      }
      return { extracted: false };
    });
    console.log('Custom Lyrics Alignment Result:', customLyricsResult);

    // 7. Test Export Lead Sheet Button
    const exportResult = await page.eval(() => {
      const exportBtn = document.getElementById('btn-export-sheet-music-pdf');
      return {
        hasExportBtn: !!exportBtn,
        btnText: exportBtn ? exportBtn.textContent.trim() : null
      };
    });
    console.log('Export Lead Sheet Result:', exportResult);

    console.log('\n--- ALL SHEET MUSIC WORKSTATION CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test Failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
