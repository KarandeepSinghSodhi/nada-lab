# -*- coding: utf-8 -*-
"""
Script to add Circadian Engine JS into app.js
"""

with open("app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. State variable
circadian_state = "  let currentCircadianData = null;"

# 2. Function implementation
circadian_func = """  /* =========================================================
     8E. CIRCADIAN SAMAY CHAKRA BIO-CLOCK SUBSYSTEM
     Coupled with 8 Praharas & Neuro-Endocrine Circadian Phases
     ========================================================= */

  const LOCAL_PRAHARA_FALLBACK = [
    { num: 1, name: "Pratham Prahara (Dawn)", raga: "Bhairav", tuning: "pa", v: -0.45, a: -0.20, phase: "Cortisol Awakening Response (CAR)", rationale: "Komal Re (112c) and Dha (814c) provide solemn grounding without sensory shock." },
    { num: 2, name: "Dwitiya Prahara (Morning)", raga: "Todi", tuning: "pa", v: 0.35, a: 0.40, phase: "Peak Cognitive Vigilance", rationale: "Sharp ascending intervals and Tivra Ma tension stimulate active alertness." },
    { num: 3, name: "Tritiya Prahara (Midday)", raga: "Shuddha Sarang", tuning: "pa", v: 0.50, a: 0.10, phase: "Solar Zenith & Metabolic Peak", rationale: "Dual Madhyams mirror the transition from morning ascendancy to afternoon declination." },
    { num: 4, name: "Chaturtha Prahara (Afternoon)", raga: "Bhimpalasi", tuning: "pa", v: 0.20, a: -0.15, phase: "Post-Prandial Relaxation", rationale: "Soft Komal Ga and Ni create tender release from midday fatigue." },
    { num: 5, name: "Panchama Prahara (Twilight)", raga: "Marwa", tuning: "ni", v: -0.30, a: 0.25, phase: "Twilight Pineal Melatonin Onset", rationale: "Tivra Ma (590c) and Komal Re (112c) create threshold sunset tension." },
    { num: 6, name: "Shashtha Prahara (Early Night)", raga: "Yaman", tuning: "pa", v: 0.75, a: -0.30, phase: "Serotonin-Melatonin Transition", rationale: "Luminous Shuddha Ga (5/4) and Ni (15/8) anchor into Sa-Pa drone, inducing nocturnal peace." },
    { num: 7, name: "Saptama Prahara (Midnight)", raga: "Darbari Kanada", tuning: "ma", v: -0.25, a: -0.60, phase: "Slow-Wave Deep Sleep Regeneration", rationale: "Mandra Saptak resonance and slow 2.1 Hz andolans produce meditative trance." },
    { num: 8, name: "Ashtama Prahara (Brahma Muhurta)", raga: "Bhairavi", tuning: "pa", v: 0.10, a: -0.40, phase: "Pre-Dawn Circadian Reset", rationale: "Fluid Re/Ga/Dha/Ni modal freedom unlocks pre-dawn universal stillness." }
  ];

  function getLocalCircadianFallback(hour) {
    if (hour >= 6 && hour < 9) return LOCAL_PRAHARA_FALLBACK[0];
    if (hour >= 9 && hour < 12) return LOCAL_PRAHARA_FALLBACK[1];
    if (hour >= 12 && hour < 15) return LOCAL_PRAHARA_FALLBACK[2];
    if (hour >= 15 && hour < 18) return LOCAL_PRAHARA_FALLBACK[3];
    if (hour >= 18 && hour < 21) return LOCAL_PRAHARA_FALLBACK[4];
    if (hour >= 21 && hour < 24) return LOCAL_PRAHARA_FALLBACK[5];
    if (hour >= 0 && hour < 3) return LOCAL_PRAHARA_FALLBACK[6];
    return LOCAL_PRAHARA_FALLBACK[7];
  }

  async function initCircadianEngine() {
    const tagEl = document.getElementById('ui-circadian-tag');
    const syncBtn = document.getElementById('btn-circadian-sync');
    const focusText = document.getElementById('sadhana-focus-text');
    const tipText = document.getElementById('sadhana-quick-tip');
    const ragaSelect = document.getElementById('ui-target-raga-select');

    const now = new Date();
    const hr = now.getHours();
    const mn = now.getMinutes();

    try {
      const res = await fetch(API_BASE + '/api/circadian-raga?hour=' + hr + '&minute=' + mn);
      if (res.ok) {
        currentCircadianData = await res.json();
      } else {
        throw new Error('API offline');
      }
    } catch (e) {
      const fb = getLocalCircadianFallback(hr);
      currentCircadianData = {
        prahara_number: fb.num,
        prahara_name: fb.name,
        recommended_raga: fb.raga,
        drone_tuning: fb.tuning,
        target_valence: fb.v,
        target_arousal: fb.a,
        biological_phase: fb.phase,
        acoustic_rationale: fb.rationale
      };
    }

    if (tagEl && currentCircadianData) {
      tagEl.textContent = 'Circadian: Prahara ' + currentCircadianData.prahara_number + ' · ' + currentCircadianData.recommended_raga;
    }

    if (syncBtn) {
      syncBtn.addEventListener('click', function () {
        if (!currentCircadianData) return;
        const targetRaga = currentCircadianData.recommended_raga;

        if (ragaSelect) {
          ragaSelect.value = targetRaga;
        }

        // Auto-set drone tuning
        if (currentCircadianData.drone_tuning) {
          setDroneTuning(currentCircadianData.drone_tuning, true);
        }

        // Set affective radar target
        currentValence = currentCircadianData.target_valence;
        currentArousal = currentCircadianData.target_arousal;
        renderRasaRadarCanvas();

        // Update guidance text
        if (focusText) {
          focusText.textContent = targetRaga + ' · ' + currentCircadianData.prahara_name;
        }
        if (tipText) {
          tipText.textContent = currentCircadianData.biological_phase + ': ' + currentCircadianData.acoustic_rationale;
        }

        // Update dwell
        renderSwaraDwellAnalysis(null, targetRaga);
        renderPhraseInspector();

        syncBtn.textContent = 'Synced (' + targetRaga + ')';
        setTimeout(function () {
          syncBtn.textContent = 'Sync Solar Hour';
        }, 2200);
      });
    }
  }
"""

# Insert before DOMContentLoaded
dom_anchor = "  document.addEventListener('DOMContentLoaded', function () {"
if dom_anchor in content:
    content = content.replace(dom_anchor, circadian_func + "\n\n" + dom_anchor, 1)
    print("Circadian engine JS added before DOMContentLoaded.")
else:
    print("Warning: dom_anchor not found!")

# Add initCircadianEngine to DOMContentLoaded
old_inits = "    renderRasaRadarCanvas();"
new_inits = "    renderRasaRadarCanvas();\n    initCircadianEngine();"

if old_inits in content:
    content = content.replace(old_inits, new_inits, 1)
    print("initCircadianEngine added to DOMContentLoaded.")
else:
    print("Warning: old_inits not found!")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(content)

print("app.js updated successfully with Circadian Bio-Clock!")
