import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Continuous Pitch Ribbon & Riyaz Sing-Along Scorecard...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Switch to Track Dossier Tab
    await page.eval(() => {
      const tab = document.getElementById('tab-btn-dossier');
      if (tab) tab.click();
    });
    await sleep(600);

    // 2. Check Ribbon Toolbar & Controls
    const toolbarCheck = await page.eval(() => {
      const toolbar = document.querySelector('.sheet-ribbon-toolbar');
      const toggleBtn = document.getElementById('btn-toggle-pitch-ribbon');
      const evalBtn = document.getElementById('btn-evaluate-take');
      const legend = document.getElementById('sheet-ribbon-legend');
      const scorecard = document.getElementById('leadsheet-riyaz-scorecard');

      return {
        hasToolbar: !!toolbar,
        hasToggleBtn: !!toggleBtn,
        hasEvalBtn: !!evalBtn,
        hasLegend: !!legend,
        hasScorecard: !!scorecard,
        isScorecardHidden: scorecard?.classList.contains('is-hidden')
      };
    });
    console.log('Pitch Ribbon Toolbar Initial Check:', toolbarCheck);
    if (!toolbarCheck.hasToolbar || !toolbarCheck.hasToggleBtn || !toolbarCheck.hasEvalBtn) {
      throw new Error('Pitch ribbon toolbar or buttons missing!');
    }

    // 3. Check SVG Pitch Ribbon in Measures
    const ribbonCheck = await page.eval(() => {
      const canvases = document.querySelectorAll('.sheet-pitch-ribbon-canvas');
      const targetPaths = document.querySelectorAll('.ribbon-target-path');
      const sungPaths = document.querySelectorAll('.ribbon-sung-path');

      return {
        canvasCount: canvases.length,
        targetPathCount: targetPaths.length,
        sungPathCount: sungPaths.length,
        firstTargetPath: targetPaths[0]?.getAttribute('d')?.slice(0, 30),
        firstSungPath: sungPaths[0]?.getAttribute('d')?.slice(0, 30)
      };
    });
    console.log('SVG Pitch Ribbon Check:', ribbonCheck);
    if (ribbonCheck.canvasCount < 2 || ribbonCheck.targetPathCount < 2) {
      throw new Error('SVG pitch ribbon not rendered across measures!');
    }

    // 4. Test Toggling Pitch Ribbon OFF and ON
    const toggleResult = await page.eval(() => {
      const btn = document.getElementById('btn-toggle-pitch-ribbon');
      btn.click();
      const firstCanvas = document.querySelector('.sheet-pitch-ribbon-canvas');
      const isOff = firstCanvas?.classList.contains('is-hidden');
      const textOff = btn.textContent.trim();

      // Toggle back on
      btn.click();
      const isOn = !firstCanvas?.classList.contains('is-hidden');
      const textOn = btn.textContent.trim();

      return { isOff, textOff, isOn, textOn };
    });
    console.log('Toggle Pitch Ribbon Result:', toggleResult);
    if (!toggleResult.isOff || !toggleResult.isOn) {
      throw new Error('Pitch ribbon toggle failed!');
    }

    // 5. Test Evaluating Practice Take
    const evalResult = await page.eval(async () => {
      const evalBtn = document.getElementById('btn-evaluate-take');
      evalBtn.click();
      // Wait for async evaluation
      await new Promise(r => setTimeout(r, 600));

      const scorecard = document.getElementById('leadsheet-riyaz-scorecard');
      const isVisible = scorecard && !scorecard.classList.contains('is-hidden');
      const title = document.getElementById('scorecard-song-title')?.textContent?.trim();
      const overall = document.getElementById('scorecard-overall-badge')?.textContent?.trim();
      const intonation = document.getElementById('scorecard-intonation-val')?.textContent?.trim();
      const meend = document.getElementById('scorecard-meend-val')?.textContent?.trim();
      const kan = document.getElementById('scorecard-kan-val')?.textContent?.trim();
      const laya = document.getElementById('scorecard-laya-val')?.textContent?.trim();
      const feedback = document.getElementById('scorecard-feedback-text')?.textContent?.trim();

      return {
        isVisible,
        title,
        overall,
        intonation,
        meend,
        kan,
        laya,
        feedbackExcerpt: feedback?.slice(0, 60)
      };
    });
    console.log('Practice Take Evaluation Result:', evalResult);
    if (!evalResult.isVisible || !evalResult.overall || !evalResult.intonation) {
      throw new Error('Riyaz Scorecard did not display evaluation properly!');
    }

    // 6. Test Dismissing Scorecard
    const closeResult = await page.eval(() => {
      const closeBtn = document.getElementById('btn-close-scorecard');
      closeBtn.click();
      const scorecard = document.getElementById('leadsheet-riyaz-scorecard');
      return { isHidden: scorecard?.classList.contains('is-hidden') };
    });
    console.log('Scorecard Close Result:', closeResult);
    if (!closeResult.isHidden) {
      throw new Error('Scorecard failed to close!');
    }

    // 7. Test Evaluation on a different song (Darbari Kanada)
    const darbariEval = await page.eval(async () => {
      const darbariBtn = document.querySelector('.antar-song-btn[data-song-key="darbari_rakhwale"]');
      if (darbariBtn) darbariBtn.click();
      await new Promise(r => setTimeout(r, 400));

      const evalBtn = document.getElementById('btn-evaluate-take');
      evalBtn.click();
      await new Promise(r => setTimeout(r, 600));

      const scorecard = document.getElementById('leadsheet-riyaz-scorecard');
      const title = document.getElementById('scorecard-song-title')?.textContent?.trim();
      const overall = document.getElementById('scorecard-overall-badge')?.textContent?.trim();

      return {
        isVisible: scorecard && !scorecard.classList.contains('is-hidden'),
        title,
        overall
      };
    });
    console.log('Darbari Kanada Take Evaluation:', darbariEval);
    if (!darbariEval.isVisible || (!darbariEval.title.includes('Darbari') && !darbariEval.title.includes('Rakhwale'))) {
      throw new Error('Darbari evaluation failed!');
    }

    console.log('\n--- ALL PITCH RIBBON & RIYAZ SCORECARD CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test Failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
