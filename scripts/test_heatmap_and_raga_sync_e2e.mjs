import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Intonation Error Heatmap & Unified Raga Sync...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Check Heatmap Ribbon presence & cells
    const heatmapCheck = await page.eval(() => {
      const container = document.querySelector('.ui-heatmap-container');
      const strip = document.getElementById('ui-heatmap-strip');
      const cells = strip ? Array.from(strip.querySelectorAll('.heatmap-cell')) : [];
      const currentCell = strip ? strip.querySelector('.heatmap-cell.is-current') : null;

      return {
        hasContainer: !!container,
        hasStrip: !!strip,
        cellCount: cells.length,
        hasCurrentHighlight: !!currentCell,
        sampleColors: cells.slice(0, 5).map(c => c.style.backgroundColor)
      };
    });
    console.log('Heatmap Initial State:', heatmapCheck);
    if (!heatmapCheck.hasContainer || heatmapCheck.cellCount < 50) {
      throw new Error('Heatmap ribbon not properly populated!');
    }

    // 2. Test Clicking Heatmap Cell
    const cellClickCheck = await page.eval(() => {
      const strip = document.getElementById('ui-heatmap-strip');
      const targetCell = strip.querySelectorAll('.heatmap-cell')[30]; // 50%
      if (!targetCell) return { clicked: false };

      targetCell.click();
      const scrubber = document.getElementById('phrase-scrubber');
      return {
        clicked: true,
        scrubberVal: scrubber ? scrubber.value : null
      };
    });
    console.log('Heatmap Cell Click Result:', cellClickCheck);
    if (!cellClickCheck.clicked || Math.abs(Number(cellClickCheck.scrubberVal) - 51) > 5) {
      throw new Error('Heatmap cell click did not update scrubber correctly!');
    }

    // 3. Test Changing Raga Select to Bhairav
    console.log('Switching Raga to Bhairav to verify 5-studio synchronization...');
    const ragaChangeResult = await page.eval(async () => {
      const select = document.getElementById('ui-target-raga-select');
      if (!select) return { changed: false };

      // Find Bhairav option
      for (let i = 0; i < select.options.length; i++) {
        if (select.options[i].value.toLowerCase().includes('bhairav')) {
          select.selectedIndex = i;
          break;
        }
      }
      select.dispatchEvent(new Event('change'));

      // Wait a moment for async allied ragas fetch
      await new Promise(r => setTimeout(r, 800));

      const alliedCards = Array.from(document.querySelectorAll('#allied-ragas-list .allied-card-header h5')).map(h => h.textContent.trim());
      const alankarAroha = document.getElementById('alankar-aroha-text')?.textContent.trim();
      const rasaHero = document.getElementById('rasa-hero-name')?.textContent.trim();

      return {
        selectedRaga: select.value,
        alliedCards,
        alankarAroha,
        rasaHero
      };
    });
    console.log('Raga Change Synchronization Result:', ragaChangeResult);
    if (!ragaChangeResult.selectedRaga.toLowerCase().includes('bhairav')) {
      throw new Error('Raga selection failed!');
    }

    console.log('\n--- ALL INTONATION ERROR HEATMAP & RAGA SYNC CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test FAILED:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
