import { Browser, sleep } from 'file:///C:/Users/karan/.gemini/config/skills/design-taste-frontend/scripts/lib/cdp.mjs';

async function run() {
  const browser = await Browser.launch({ headless: true });
  const page = await browser.newPage({ width: 1440, height: 900 });

  try {
    console.log('Testing Riyaz Mastery Scorecard & Multi-Take Progression...');
    await page.goto('http://127.0.0.1:8000/');
    await sleep(1500);

    // 1. Check Scorecard HUD presence
    const scorecardCheck = await page.eval(() => {
      const card = document.querySelector('.ui-riyaz-scorecard');
      const grade = document.getElementById('riyaz-grade-badge');
      const prec = document.getElementById('metric-shruti-prec');
      const sth = document.getElementById('metric-sthirata');
      const meend = document.getElementById('metric-meend-fluid');
      const laya = document.getElementById('metric-laya-sync');
      const chips = Array.from(document.querySelectorAll('.history-chip')).map(c => c.textContent.trim());
      const delta = document.getElementById('riyaz-delta-badge');

      return {
        hasCard: !!card,
        grade: grade ? grade.textContent.trim() : null,
        prec: prec ? prec.textContent.trim() : null,
        sth: sth ? sth.textContent.trim() : null,
        meend: meend ? meend.textContent.trim() : null,
        laya: laya ? laya.textContent.trim() : null,
        chips: chips,
        delta: delta ? delta.textContent.trim() : null
      };
    });
    console.log('Scorecard Initial State:', scorecardCheck);
    if (!scorecardCheck.hasCard || !scorecardCheck.grade) {
      throw new Error('Riyaz Scorecard HUD not found!');
    }

    // 2. Test Tala Sync Button in A-B Looper
    const talaSyncCheck = await page.eval(() => {
      const btn = document.getElementById('btn-sync-tala-metronome');
      if (!btn) return { hasBtn: false };
      btn.click();
      const isActiveAfterClick = btn.classList.contains('is-active');
      const textAfterClick = btn.textContent.trim();
      btn.click(); // toggle back off
      return {
        hasBtn: true,
        isActiveAfterClick,
        textAfterClick
      };
    });
    console.log('Tala Sync Button Check:', talaSyncCheck);
    if (!talaSyncCheck.hasBtn || !talaSyncCheck.isActiveAfterClick) {
      throw new Error('Tala Sync Button toggle failed!');
    }

    // 3. Trigger Audition Phrase and let it finish to generate Take 2
    console.log('Auditioning phrase to record progressive Take 2...');
    await page.eval(() => {
      const btn = document.getElementById('audition-phrase-btn');
      if (btn) btn.click();
    });
    await sleep(2500);

    // Verify Take 2 was recorded and chips updated
    const take2Check = await page.eval(() => {
      const chips = Array.from(document.querySelectorAll('.history-chip')).map(c => c.textContent.trim());
      const delta = document.getElementById('riyaz-delta-badge');
      const takeLbl = document.getElementById('riyaz-take-label');
      return {
        chipCount: chips.length,
        chips: chips,
        delta: delta ? delta.textContent.trim() : null,
        takeLbl: takeLbl ? takeLbl.textContent.trim() : null
      };
    });
    console.log('Progressive Riyaz Take 2 Check:', take2Check);
    if (take2Check.chipCount < 2) {
      throw new Error('Take 2 was not added to history chips!');
    }

    console.log('\n--- ALL RIYAZ MASTERY SCORECARD CHECKS PASSED! ---');
  } catch (err) {
    console.error('Test FAILED:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

run();
