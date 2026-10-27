import re

with open('app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update phrase click handler to also call updateSadhanaFocus(key)
target_phrase_click = """        btn.classList.add('is-active');
        renderPhraseInspector();"""
replacement_phrase_click = """        btn.classList.add('is-active');
        updateSadhanaFocus(key);
        renderPhraseInspector();"""

assert target_phrase_click in code, "Target phrase click not found!"
code = code.replace(target_phrase_click, replacement_phrase_click, 1)

# 2. Update custom upload handler to also call updateSadhanaFocus('custom_upload')
target_upload = """    currentPhraseKey = 'custom_upload';
    document.querySelectorAll('.ui-phrase-btn').forEach(function (b) { b.classList.remove('is-active'); });
    scrubValue = 0;
    const scrubber = document.getElementById('phrase-scrubber');
    if (scrubber) scrubber.value = '0';
    renderPhraseInspector();"""
replacement_upload = """    currentPhraseKey = 'custom_upload';
    document.querySelectorAll('.ui-phrase-btn').forEach(function (b) { b.classList.remove('is-active'); });
    scrubValue = 0;
    const scrubber = document.getElementById('phrase-scrubber');
    if (scrubber) scrubber.value = '0';
    updateSadhanaFocus('custom_upload');
    renderPhraseInspector();"""

assert target_upload in code, "Target upload not found!"
code = code.replace(target_upload, replacement_upload, 1)

# 3. Add Sadhana & Tutorial functions before DOMContentLoaded
new_controllers = """
  /* =========================================================
     NĀDA LAB: WORKSPACE MODE (SĀDHANĀ vs. STUDIO LAB)
     ========================================================= */
  let currentWorkspaceMode = 'sadhana';

  const SADHANA_TIPS = {
    yaman_meend: {
      focus: 'Raga Yaman · Meend Glide (Re to Ga)',
      tip: 'Listen to the phrase, then start your mic and sing along with the tanpura drone. Watch your pitch line glide into Gandhar (5/4).'
    },
    yaman_varjya: {
      focus: 'Raga Yaman · Forbidden Shuddha Ma Violation',
      tip: 'Yaman exclusively takes Tivra Ma (45/32). Singing Shuddha Ma (4/3) triggers an immediate raga rule critique.'
    },
    darbari_andolan: {
      focus: 'Raga Darbari Kanada · 2.1 Hz Authentic Andolan',
      tip: 'Sing Komal Ga (6/5) with slow, heavy oscillations between 1.8 Hz and 2.4 Hz. Maintain steady breath support.'
    },
    darbari_flat: {
      focus: 'Raga Darbari Kanada · Flat Drift Deficit (-24c)',
      tip: 'Dropping below the microtonal Komal Dha (8/5) threshold flags an intonation deficit.'
    },
    bhairav_flutter: {
      focus: 'Raga Bhairav · Fast Flutter Deficit (6.0 Hz)',
      tip: 'Bhairav Komal Re requires gentle, deliberate andolan (1.5-2.5 Hz), never rapid western vibrato (>5 Hz).'
    },
    real_vocal: {
      focus: 'Saraga Classical Vocal Audio Plate',
      tip: 'Real studio vocal performance evaluated against continuous 22-shruti lattice and raga grammar rules.'
    },
    custom_upload: {
      focus: 'Custom Vocal File Inspection',
      tip: 'Offline YIN pitch analysis running locally in your browser with instant deficit diagnosis.'
    }
  };

  function updateSadhanaFocus(key) {
    const focusEl = document.getElementById('sadhana-focus-text');
    const tipEl = document.getElementById('sadhana-quick-tip');
    const item = SADHANA_TIPS[key] || SADHANA_TIPS.yaman_meend;
    if (focusEl) focusEl.textContent = item.focus;
    if (tipEl) tipEl.textContent = item.tip;
  }

  function initWorkspaceModes() {
    const sadhanaBtn = document.getElementById('ws-mode-sadhana');
    const studioBtn = document.getElementById('ws-mode-studio');

    function setMode(mode) {
      currentWorkspaceMode = mode;
      document.body.classList.remove('mode-sadhana', 'mode-studio');
      document.body.classList.add('mode-' + mode);

      if (sadhanaBtn && studioBtn) {
        if (mode === 'sadhana') {
          sadhanaBtn.classList.add('is-active');
          sadhanaBtn.setAttribute('aria-checked', 'true');
          studioBtn.classList.remove('is-active');
          studioBtn.setAttribute('aria-checked', 'false');
        } else {
          studioBtn.classList.add('is-active');
          studioBtn.setAttribute('aria-checked', 'true');
          sadhanaBtn.classList.remove('is-active');
          sadhanaBtn.setAttribute('aria-checked', 'false');
        }
      }
    }

    if (sadhanaBtn) sadhanaBtn.addEventListener('click', function () { setMode('sadhana'); });
    if (studioBtn) studioBtn.addEventListener('click', function () { setMode('studio'); });

    setMode('sadhana');
  }

  /* =========================================================
     NĀDA LAB: INTERACTIVE STEP-BY-STEP TUTORIAL CONTROLLER
     ========================================================= */
  const TUTORIAL_STEPS = [
    {
      targetSelector: '#drone-toggle-btn',
      title: 'Ground Your Ear with the Tanpura',
      desc: 'In Indian classical music, pitch is not fixed to piano keys. Every microtone lives relative to your movable Sa. Start the drone to anchor your vocal reference.',
      preferredPos: 'top'
    },
    {
      targetSelector: '.ui-phrase-selector',
      title: 'Select a Benchmark Phrase',
      desc: 'Choose from canonical classical benchmark phrases like Yaman Meend (glide) or Darbari Andolan (slow 2.1 Hz oscillation), or upload your own audio.',
      preferredPos: 'bottom'
    },
    {
      targetSelector: '#audition-phrase-btn',
      title: 'Audition or Sing Live',
      desc: 'Click "Audition Phrase" to hear the master vocal reference, or click "Start Live Mic" to sing with zero-latency microtonal pitch detection.',
      preferredPos: 'bottom'
    },
    {
      targetSelector: '#shruti-canvas',
      title: '22-Shruti Dynamic Canvas',
      desc: 'Watch your continuous pitch curve in real time. The horizontal lines are rational harmonic ratios (such as pure Shuddha Ga at 386.3 cents) rather than tempered piano semitones.',
      preferredPos: 'top'
    },
    {
      targetSelector: '.ui-diagnostic-pane',
      title: '1 Actionable Guru Critique',
      desc: 'No confusing walls of numbers. The Deficit Engine isolates your single most urgent fix and prescribes an instant vocal drill. Click "Hear Guru Correction" to listen to the master repair.',
      preferredPos: 'left'
    }
  ];

  let currentTutorialStep = 0;

  function initTutorialSystem() {
    const overlay = document.getElementById('tutorial-overlay');
    const spotlight = document.getElementById('tutorial-spotlight');
    const card = document.getElementById('tutorial-card');
    const stepBadge = document.getElementById('tut-step-badge');
    const titleEl = document.getElementById('tut-title');
    const descEl = document.getElementById('tut-desc');
    const prevBtn = document.getElementById('tut-prev-btn');
    const nextBtn = document.getElementById('tut-next-btn');
    const skipBtn = document.getElementById('tut-skip-btn');
    const closeBtn = document.getElementById('tut-close-btn');
    const startBtn = document.getElementById('start-tutorial-btn');

    if (!overlay || !spotlight || !card) return;

    function renderStep(index) {
      if (index < 0 || index >= TUTORIAL_STEPS.length) return;
      currentTutorialStep = index;
      const step = TUTORIAL_STEPS[index];
      const target = document.querySelector(step.targetSelector);

      if (!target) {
        if (index + 1 < TUTORIAL_STEPS.length) renderStep(index + 1);
        return;
      }

      target.scrollIntoView({ behavior: 'smooth', block: 'center' });

      setTimeout(function () {
        const rect = target.getBoundingClientRect();
        const padding = 8;
        spotlight.style.top = (rect.top - padding) + 'px';
        spotlight.style.left = (rect.left - padding) + 'px';
        spotlight.style.width = (rect.width + padding * 2) + 'px';
        spotlight.style.height = (rect.height + padding * 2) + 'px';

        if (stepBadge) stepBadge.textContent = 'Step ' + (index + 1) + ' of ' + TUTORIAL_STEPS.length;
        if (titleEl) titleEl.textContent = step.title;
        if (descEl) descEl.textContent = step.desc;

        let cardTop = rect.bottom + 16;
        let cardLeft = rect.left;

        if (cardTop + 240 > window.innerHeight) {
          cardTop = Math.max(16, rect.top - 240);
        }
        if (cardLeft + 360 > window.innerWidth) {
          cardLeft = Math.max(16, window.innerWidth - 380);
        }

        card.style.top = Math.max(16, cardTop) + 'px';
        card.style.left = Math.max(16, cardLeft) + 'px';

        if (prevBtn) prevBtn.disabled = (index === 0);
        if (nextBtn) {
          nextBtn.textContent = (index === TUTORIAL_STEPS.length - 1) ? 'Finish Tour' : 'Next Step →';
        }
      }, 200);
    }

    function startTutorial() {
      overlay.classList.remove('is-hidden');
      renderStep(0);
    }

    function endTutorial() {
      overlay.classList.add('is-hidden');
      try {
        localStorage.setItem('nada_tutorial_seen', 'true');
      } catch (e) {}
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        if (currentTutorialStep < TUTORIAL_STEPS.length - 1) {
          renderStep(currentTutorialStep + 1);
        } else {
          endTutorial();
        }
      });
    }

    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        if (currentTutorialStep > 0) renderStep(currentTutorialStep - 1);
      });
    }

    if (skipBtn) skipBtn.addEventListener('click', endTutorial);
    if (closeBtn) closeBtn.addEventListener('click', endTutorial);
    if (startBtn) startBtn.addEventListener('click', startTutorial);

    try {
      if (!localStorage.getItem('nada_tutorial_seen')) {
        setTimeout(function () { startTutorial(); }, 1200);
      }
    } catch (e) {}
  }
"""

target_dom_load = """  document.addEventListener('DOMContentLoaded', function () {
    initShowcaseTabs();"""

replacement_dom_load = new_controllers + """
  document.addEventListener('DOMContentLoaded', function () {
    initWorkspaceModes();
    initTutorialSystem();
    initShowcaseTabs();"""

assert target_dom_load in code, "Target DOMContentLoaded not found!"
code = code.replace(target_dom_load, replacement_dom_load, 1)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.js successfully!")
