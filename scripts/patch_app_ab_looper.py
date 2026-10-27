# scripts/patch_app_ab_looper.py

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Normalize CRLF to LF
js = js.replace('\r\n', '\n')

ab_looper_code = '''
  /* =========================================================
     3C. A-B PRACTICE LOOPER & VARIABLE SPEED RIYAZ ENGINE
     ========================================================= */
  let loopPointASec = 0.0;
  let loopPointBSec = 2.2;
  let isLoopingAB = false;
  let abLoopTimeout = null;

  function initABLooper() {
    const btnSetA = document.getElementById('btn-set-loop-a');
    const btnSetB = document.getElementById('btn-set-loop-b');
    const btnToggleLoop = document.getElementById('btn-toggle-loop');
    const valA = document.getElementById('loop-a-val');
    const valB = document.getElementById('loop-b-val');
    const speedBtns = document.querySelectorAll('.ab-speed-btn');

    function getScrubberCurrentTime() {
      const phrase = PHRASE_LIBRARY[currentPhraseKey];
      const maxDuration = (phrase && phrase.audioBuffer) ? phrase.audioBuffer.duration : 2.2;
      return (scrubValue / 100.0) * maxDuration;
    }

    if (btnSetA) {
      btnSetA.addEventListener('click', function () {
        const t = Math.max(0, getScrubberCurrentTime());
        loopPointASec = Math.min(t, loopPointBSec - 0.1);
        if (valA) valA.textContent = loopPointASec.toFixed(1) + 's';
        if (typeof showToast === 'function') showToast('Loop Point A set to ' + loopPointASec.toFixed(2) + 's');
      });
    }

    if (btnSetB) {
      btnSetB.addEventListener('click', function () {
        const t = getScrubberCurrentTime();
        loopPointBSec = Math.max(t, loopPointASec + 0.1);
        if (valB) valB.textContent = loopPointBSec.toFixed(1) + 's';
        if (typeof showToast === 'function') showToast('Loop Point B set to ' + loopPointBSec.toFixed(2) + 's');
      });
    }

    speedBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        speedBtns.forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        const spd = parseFloat(btn.getAttribute('data-speed')) || 1.0;
        currentAuditionSpeed = spd;
        if (typeof showToast === 'function') showToast('Practice Speed: ' + spd + 'x');
      });
    });

    if (btnToggleLoop) {
      btnToggleLoop.addEventListener('click', function () {
        if (isLoopingAB) {
          stopABLoop();
        } else {
          startABLoop();
        }
      });
    }

    // Expose global window helper for Lead Sheet meend looping
    window.loopMeendTransition = function (startSec, endSec) {
      loopPointASec = Math.max(0, Number(startSec) || 0);
      loopPointBSec = Math.max(loopPointASec + 0.15, Number(endSec) || (loopPointASec + 0.6));
      if (valA) valA.textContent = loopPointASec.toFixed(1) + 's';
      if (valB) valB.textContent = loopPointBSec.toFixed(1) + 's';
      
      // Auto-set speed to 0.75x for clear listening
      speedBtns.forEach(function (b) {
        if (b.getAttribute('data-speed') === '0.75') {
          b.click();
        }
      });
      
      startABLoop();
      if (typeof showToast === 'function') {
        showToast('🔁 Looping Meend (' + loopPointASec.toFixed(2) + 's - ' + loopPointBSec.toFixed(2) + 's) at 0.75x');
      }
    };
  }

  function startABLoop() {
    isLoopingAB = true;
    const btnToggleLoop = document.getElementById('btn-toggle-loop');
    if (btnToggleLoop) {
      btnToggleLoop.classList.add('is-looping');
      btnToggleLoop.textContent = '⏹ Stop Loop';
    }
    runSingleLoopIteration();
  }

  function stopABLoop() {
    isLoopingAB = false;
    if (abLoopTimeout) {
      clearTimeout(abLoopTimeout);
      abLoopTimeout = null;
    }
    stopAudition();
    const btnToggleLoop = document.getElementById('btn-toggle-loop');
    if (btnToggleLoop) {
      btnToggleLoop.classList.remove('is-looping');
      btnToggleLoop.textContent = '🔁 Loop A-B';
    }
  }

  function runSingleLoopIteration() {
    if (!isLoopingAB) return;
    const phrase = PHRASE_LIBRARY[currentPhraseKey];
    const spd = currentAuditionSpeed || 1.0;
    const loopDuration = Math.max(0.1, (loopPointBSec - loopPointASec)) / spd;

    // Set scrubber to loop start point
    const maxDur = (phrase && phrase.audioBuffer) ? phrase.audioBuffer.duration : 2.2;
    scrubValue = Math.round((loopPointASec / maxDur) * 100);
    const scrubber = document.getElementById('phrase-scrubber');
    if (scrubber) scrubber.value = String(scrubValue);
    renderPhraseInspector();

    // Trigger phrase audio
    playAuditionPhrase();

    // Schedule next iteration
    abLoopTimeout = setTimeout(function () {
      if (isLoopingAB) {
        runSingleLoopIteration();
      }
    }, Math.round(loopDuration * 1000) + 120);
  }
'''

# 1. Add initABLooper call to DOMContentLoaded
dom_target = '    initWorkspaceModes();'
if dom_target in js and 'initABLooper();' not in js:
    js = js.replace(dom_target, dom_target + '\n    initABLooper();', 1)

# 2. Append A-B looper implementation before the end of IIFE
iife_end = '})();'
if iife_end in js and 'function initABLooper()' not in js:
    js = js.replace(iife_end, ab_looper_code + '\n' + iife_end, 1)

# 3. Add Loop Meend button to transition bridge in renderSheetMusicScore
bridge_target = '''          bridgeDiv.innerHTML = 
            '<span class="sheet-tr-glyph">' + glyph + '</span>' +
            '<span class="sheet-tr-dur">' + (tr.duration_ms || 120) + 'ms</span>' +
            kanHtml;'''

bridge_replacement = '''          bridgeDiv.innerHTML = 
            '<span class="sheet-tr-glyph">' + glyph + '</span>' +
            '<span class="sheet-tr-dur">' + (tr.duration_ms || 120) + 'ms</span>' +
            kanHtml +
            '<button type="button" class="sheet-loop-meend-btn" title="Loop this meend transition repeatedly for practice">🔁 Loop</button>';

          const loopBtn = bridgeDiv.querySelector('.sheet-loop-meend-btn');
          if (loopBtn) {
            loopBtn.addEventListener('click', function (e) {
              e.stopPropagation();
              if (typeof window.loopMeendTransition === 'function') {
                const s = tr.start_time || 0;
                const d = (tr.duration_ms || 300) / 1000.0;
                window.loopMeendTransition(s, s + d);
              }
            });
          }'''

if bridge_target in js:
    js = js.replace(bridge_target, bridge_replacement, 1)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js with A-B Looper engine and bridge loop button.")
