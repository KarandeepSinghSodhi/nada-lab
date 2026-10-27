with open('app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add updatePhraseRasaDisplay and initStudioTabs before DOMContentLoaded
code_to_insert = """
  /* =========================================================
     MUSICIAN STUDIO WORKSPACE TABS & PHRASE-LEVEL RASA
     ========================================================= */

  function updatePhraseRasaDisplay(rasaData, ragaName) {
    const primaryPill = document.getElementById('rasa-primary-pill');
    const secondaryPill = document.getElementById('rasa-secondary-pill');
    const heroName = document.getElementById('rasa-hero-name');
    const heroDesc = document.getElementById('rasa-hero-desc');
    const treatiseText = document.getElementById('rasa-treatise-text');
    const valEl = document.getElementById('rasa-kpi-valence');
    const aroEl = document.getElementById('rasa-kpi-arousal');
    const velEl = document.getElementById('rasa-kpi-velocity');
    const nyasaEl = document.getElementById('rasa-kpi-nyasa');
    const quadrantBadge = document.getElementById('rasa-quadrant-badge');

    if (!primaryPill) return;

    const RAGA_RASA_MAP = {
      'Yaman': {
        primary: 'Shanta',
        secondary: 'Shringara',
        devanagari: '\\u0936\\u093e\\u0928\\u094d\\u0924 \\u0930\\u0938',
        desc: 'Serenity, twilight contemplation, and devotional surrender. Grounded resting on Shadja (Sa) and Shuddha Gandhar (5/4) with zero kinetic jerk dissolves psychic restlessness.',
        treatise: 'In Sangita Ratnakara (Prakarana 7), Sarangadeva establishes that concordant just-intonation intervals in Kalyan thaat evoke Shanta Rasa (equanimity and tranquil repose).',
        valence: '+0.68',
        arousal: '0.36',
        velocity: '142 c/s',
        nyasa: 'Ga, Pa, Sa',
        quadrant: 'Serene / Contemplative (4th Quadrant)'
      },
      'Darbari Kanada': {
        primary: 'Karuna',
        secondary: 'Veera',
        devanagari: '\\u0915\\u0930\\u0941\\u0923 \\u0930\\u0938',
        desc: 'Profound majesty, meditative gravity (Gambhira), and sublime pathos. Slow 2.1 Hz andolan on Atikomal Ga (32/27) evokes deep introspective yearning.',
        treatise: 'Natya Shastra Ch. 29 classifies oscillating and flattened swaras as prime vehicles for Karuna (pathos and compassionate longing).',
        valence: '-0.38',
        arousal: '0.34',
        velocity: '118 c/s',
        nyasa: 'Komal Ga, Dha, Sa',
        quadrant: 'Sublime Pathos / Longing (3rd Quadrant)'
      },
      'Bhairav': {
        primary: 'Bhakti',
        secondary: 'Shanta',
        devanagari: '\\u092d\\u0915\\u094d\\u0924\\u093f \\u0930\\u0938',
        desc: 'Dawn devotion, awe, and spiritual awakening. Heavy gamak oscillation on Komal Re (256/243) and Komal Dha embodies morning reverence.',
        treatise: 'Brihaddeshi classifies Bhairav as the archetypal dawn meditation, invoking divine reverie and profound sacred stillness.',
        valence: '+0.25',
        arousal: '0.42',
        velocity: '210 c/s',
        nyasa: 'Komal Re, Dha, Sa',
        quadrant: 'Devotional Awe (1st Quadrant)'
      },
      'Todi': {
        primary: 'Karuna',
        secondary: 'Vairagya',
        devanagari: '\\u0915\\u0930\\u0941\\u0923 \\u090f\\u0935\\u0902 \\u0935\\u0948\\u0930\\u093e\\u0917\\u094d\\u092f',
        desc: 'Intense yearning, solitude, and ascetic detachment. Atikomal Gandhar and Komal Rishabh create an unmatched poignant ache.',
        treatise: 'Sangita Parijata describes Todi as capable of enchanting wild antelopes through the sheer purity of its ascetic longing.',
        valence: '-0.55',
        arousal: '0.45',
        velocity: '135 c/s',
        nyasa: 'Komal Ga, Re, Dha',
        quadrant: 'Ascetic Longing (3rd Quadrant)'
      },
      'Bageshri': {
        primary: 'Shringara',
        secondary: 'Karuna',
        devanagari: '\\u0936\\u0943\\u0902\\u0917\\u093e\\u0930 (\\u0935\\u093f\\u092a\\u094d\\u0930\\u0932\\u0902\\u092d)',
        desc: 'Midnight longing, poignant separation (Vipralambha), and tender intimacy. Centered on Madhyam (4/3) and Komal Nishad.',
        treatise: 'Natya Shastra identifies Madhyam-prominent ragas with night-time devotion and the sweet ache of lovers parted by distance.',
        valence: '+0.35',
        arousal: '0.32',
        velocity: '128 c/s',
        nyasa: 'Ma, Komal Ni, Sa',
        quadrant: 'Tender Yearning (4th Quadrant)'
      },
      'Bhairavi': {
        primary: 'Shanta',
        secondary: 'Karuna',
        devanagari: '\\u0936\\u093e\\u0928\\u094d\\u0924 \\u0930\\u0938',
        desc: 'Universal resolution, peaceful fulfillment, and unconditional surrender. Incorporates all 12 swaras in harmonious reconciliation.',
        treatise: 'Traditional concert performance concludes with Bhairavi as the ultimate resolution of all emotional tension into peace.',
        valence: '+0.52',
        arousal: '0.38',
        velocity: '150 c/s',
        nyasa: 'Pa, Sa, Komal Ga',
        quadrant: 'Universal Resolution (4th Quadrant)'
      }
    };

    const target = ragaName || (document.getElementById('ui-target-raga-select') && document.getElementById('ui-target-raga-select').value) || 'Yaman';
    const fallback = RAGA_RASA_MAP[target] || RAGA_RASA_MAP['Yaman'];

    if (rasaData) {
      primaryPill.textContent = 'Primary Rasa: ' + (rasaData.phrase_level_rasa || fallback.primary);
      secondaryPill.textContent = 'Secondary: ' + (rasaData.secondary_rasa || fallback.secondary);
      heroName.textContent = (rasaData.phrase_level_rasa || fallback.primary) + ' Rasa';
      heroDesc.textContent = rasaData.raga_ethos || fallback.desc;
      treatiseText.textContent = rasaData.musicological_critique || fallback.treatise;
      valEl.textContent = (rasaData.valence >= 0 ? '+' : '') + Number(rasaData.valence || 0.68).toFixed(2);
      aroEl.textContent = Number(rasaData.arousal || 0.36).toFixed(2);
      if (rasaData.kinetic_profile) {
        velEl.textContent = Math.round(rasaData.kinetic_profile.avg_pitch_velocity_cents_sec || 140) + ' c/s';
      }
      if (rasaData.nyasa_resting_swaras && rasaData.nyasa_resting_swaras.length > 0) {
        nyasaEl.textContent = rasaData.nyasa_resting_swaras.slice(0, 3).join(', ');
      }
      if (quadrantBadge) {
        quadrantBadge.textContent = rasaData.circumplex_quadrant || fallback.quadrant;
      }
    } else {
      primaryPill.textContent = 'Primary Rasa: ' + fallback.primary;
      secondaryPill.textContent = 'Secondary: ' + fallback.secondary;
      heroName.textContent = fallback.primary + ' Rasa';
      heroDesc.textContent = fallback.desc;
      treatiseText.textContent = fallback.treatise;
      valEl.textContent = fallback.valence;
      aroEl.textContent = fallback.arousal;
      velEl.textContent = fallback.velocity;
      nyasaEl.textContent = fallback.nyasa;
      if (quadrantBadge) {
        quadrantBadge.textContent = fallback.quadrant;
      }
    }
  }

  function initStudioTabs() {
    const tabs = document.querySelectorAll('.studio-tab');
    const panels = document.querySelectorAll('.studio-tab-panel');

    function switchStudioTab(targetPanelId) {
      tabs.forEach(function (t) {
        const isMatch = t.getAttribute('data-tab-target') === targetPanelId;
        t.classList.toggle('is-active', isMatch);
        t.setAttribute('aria-selected', isMatch ? 'true' : 'false');
      });

      panels.forEach(function (p) {
        const isMatch = p.id === targetPanelId;
        p.classList.toggle('is-active', isMatch);
        p.classList.toggle('is-hidden', !isMatch);
      });

      // Special handling when activating specific tabs
      if (targetPanelId === 'tab-panel-rasa') {
        renderRasaRadarCanvas();
        updatePhraseRasaDisplay(null);
      } else if (targetPanelId === 'tab-panel-tala') {
        const gridEl = document.getElementById('tala-matra-grid');
        if (gridEl && gridEl.children.length === 0) {
          renderTalaMatraGrid();
        }
      }
    }

    tabs.forEach(function (btn) {
      btn.addEventListener('click', function () {
        const targetId = btn.getAttribute('data-tab-target');
        if (targetId) switchStudioTab(targetId);
      });
    });

    window.switchStudioTab = switchStudioTab;
  }
"""

if 'function initStudioTabs' not in text:
    idx = text.find('document.addEventListener(\'DOMContentLoaded\'')
    text = text[:idx] + code_to_insert + '\n  ' + text[idx:]
    print("Inserted initStudioTabs and updatePhraseRasaDisplay")

# 2. Update applyAnalysisResults to update rasa display and switch to dossier tab
old_apply = "renderInstantTrackDossier(data, fileName, duration, targetRaga);"
new_apply = """renderInstantTrackDossier(data, fileName, duration, targetRaga);
    updatePhraseRasaDisplay(data.phrase_rasa_profile, targetRaga);
    if (window.switchStudioTab) {
      window.switchStudioTab('tab-panel-dossier');
    }"""

if old_apply in text:
    text = text.replace(old_apply, new_apply, 1)
    print("Updated applyAnalysisResults with rasa update and tab switch")

# 3. Call initStudioTabs in DOMContentLoaded
old_dom = "initPosterRows();"
new_dom = "initPosterRows();\n    initStudioTabs();"

if old_dom in text and "initStudioTabs();" not in text:
    text = text.replace(old_dom, new_dom, 1)
    print("Added initStudioTabs call to DOMContentLoaded")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated app.js successfully")
