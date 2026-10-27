import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Riyaz Multi-Take Progression Strip End-to-End...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Track Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check Take Strip in Scorecard
    const stripCheck = await page.eval(() => {
      const strip = document.getElementById('scorecard-take-strip');
      const container = document.getElementById('take-pills-container');
      return {
        hasStrip: !!strip,
        hasContainer: !!container
      };
    });
    console.log('Take Strip Initial Check:', stripCheck);
    if (!stripCheck.hasStrip || !stripCheck.hasContainer) {
      throw new Error('Scorecard take strip missing!');
    }

    // 3. Evaluate First Take (Take 1: Yaman)
    const take1Result = await page.eval(async () => {
      const evalBtn = document.getElementById('btn-evaluate-take');
      evalBtn.click();
      await new Promise(r => setTimeout(r, 600));

      const pills = document.querySelectorAll('.take-pill');
      const title = document.getElementById('scorecard-song-title')?.textContent?.trim();
      const overall = document.getElementById('scorecard-overall-badge')?.textContent?.trim();

      return {
        pillCount: pills.length,
        firstPillText: pills[0]?.textContent?.trim(),
        title,
        overall
      };
    });
    console.log('Take 1 Result:', take1Result);
    if (take1Result.pillCount < 1 || !take1Result.firstPillText.includes('Take 1')) {
      throw new Error('Take 1 not registered properly!');
    }

    // 4. Evaluate Second Take (Take 2: Darbari Kanada)
    const take2Result = await page.eval(async () => {
      const darbariBtn = document.querySelector('.antar-song-btn[data-song-key="darbari_rakhwale"]');
      if (darbariBtn) darbariBtn.click();
      await new Promise(r => setTimeout(r, 400));

      const evalBtn = document.getElementById('btn-evaluate-take');
      evalBtn.click();
      await new Promise(r => setTimeout(r, 600));

      const pills = document.querySelectorAll('.take-pill');
      const title = document.getElementById('scorecard-song-title')?.textContent?.trim();

      return {
        pillCount: pills.length,
        pillTexts: Array.from(pills).map(p => p.textContent.trim()),
        title
      };
    });
    console.log('Take 2 Result:', take2Result);
    if (take2Result.pillCount < 2) {
      throw new Error('Take 2 was not added to progression strip!');
    }

    // 5. Test Clicking Take 1 to restore past scorecard
    const clickTake1 = await page.eval(() => {
      const pills = document.querySelectorAll('.take-pill');
      pills[0].click();
      const title = document.getElementById('scorecard-song-title')?.textContent?.trim();
      const isActive = pills[0].classList.contains('is-active');

      return {
        title,
        isActive
      };
    });
    console.log('Click Take 1 Result:', clickTake1);
    if (!clickTake1.isActive || !clickTake1.title.includes('Take 1')) {
      throw new Error('Restoring Take 1 failed!');
    }

    // 6. Test Clicking Take 2 to restore Take 2
    const clickTake2 = await page.eval(() => {
      const pills = document.querySelectorAll('.take-pill');
      pills[1].click();
      const title = document.getElementById('scorecard-song-title')?.textContent?.trim();
      const isActive = pills[1].classList.contains('is-active');

      return {
        title,
        isActive
      };
    });
    console.log('Click Take 2 Result:', clickTake2);
    if (!clickTake2.isActive || !clickTake2.title.includes('Take 2')) {
      throw new Error('Restoring Take 2 failed!');
    }

    console.log('\n--- ALL RIYAZ TAKE PROGRESSION CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test Failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
