import re

with open("app.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update PHRASE_LIBRARY with guruCurveFn and analystBreakdown
new_phrase_library = """  const PHRASE_LIBRARY = {
    yaman_meend: {
      badge: 'Raga Yaman · Kalyan Thaat · Sa = 196.0 Hz (G3)',
      saHz: 196.0,
      shrutis: [
        { cents: 0, label: 'Sa (1/1)' },
        { cents: 203.91, label: 'Shuddha Re (9/8)' },
        { cents: 386.31, label: 'Shuddha Ga (5/4)' },
        { cents: 590.22, label: 'Tivra Ma (45/32)' }
      ],
      range: [-40, 640],
      ornamentTag: 'Detected: Meend (412 c/s)',
      curveFn: function (u) {
        if (u < 0.2) return 203.91;
        if (u < 0.65) {
          const p = (u - 0.2) / 0.45;
          const s = p * p * (3 - 2 * p);
          return 203.91 + (386.31 - 203.91) * s;
        }
        if (u < 0.85) {
          const p = (u - 0.65) / 0.2;
          const s = p * p * (3 - 2 * p);
          return 386.31 + (590.22 - 386.31) * s;
        }
        return 590.22;
      },
      guruCurveFn: function (u) {
        if (u < 0.2) return 203.91;
        if (u < 0.65) {
          const p = (u - 0.2) / 0.45;
          const s = p * p * (3 - 2 * p);
          return 203.91 + (386.31 - 203.91) * s;
        }
        if (u < 0.85) {
          const p = (u - 0.65) / 0.2;
          const s = p * p * (3 - 2 * p);
          return 386.31 + (590.22 - 386.31) * s;
        }
        return 590.22;
      },
      analystBreakdown: {
        ragaGrammar: 'Raga Yaman (Kalyan Thaat) uses Shuddha Re, Ga, Dha, Ni, and Tivra Ma. The tonic Sa is movable. In this phrase, the ascending movement begins on Rishabh (203.9c) and glides smoothly into Gandhar (386.3c) without discrete steps.',
        kinematics: 'Kinematic derivative v(t) = dC/dt is continuous at ~412 c/s without velocity spikes or staircase steps across the 450 ms glide from Re (203.9c) to Ga (386.3c).',
        sadhana: 'Sing with open throat on vowel "Aa", anchoring into the tanpura drone. Practice keeping the larynx stable as pitch glides through Tivra Ma.'
      },
      gayaki: {
        tier: 'TIER 2 · ORNAMENT INTEGRITY',
        score: '96.4%',
        headline: 'Smooth Linear Meend Verified',
        detail: 'Continuous glide from Shuddha Re (203.9c) to Shuddha Ga (386.3c) maintains steady Savitzky-Golay velocity without staircase stepping across intermediate semitones.',
        drill: 'Sustain Ni (1088.3c) on the tanpura breath, then execute a slow 650 ms glide into Re (203.9c) while keeping throat resonance open across Sa.',
        target: '386.3 cents (5/4)',
        measured: '386.1 cents (-0.2c)',
        velocity: '412.0 cents/sec',
        grammar: 'Zero Varjya Notes'
      },
      western: {
        tier: '12-TET PITCH GRID AUDIT',
        score: '82.1%',
        headline: 'Portamento Crosses 12-TET Bins',
        detail: 'In Western 12-TET mode, the 450 ms continuous glide spends 280 ms between D4 (200c) and E4 (400c), and lands 13.7 cents flatter than equal-tempered E4.',
        drill: 'For Western contemporary pop/jazz, shorten the transition to under 90 ms and raise the E4 target by +14 cents to match equal-tempered piano accompaniment.',
        target: '400.0 cents (12-TET)',
        measured: '386.1 cents (-13.9c)',
        velocity: '412.0 cents/sec',
        grammar: 'Chromatic Portamento'
      }
    },

    yaman_varjya: {
      badge: 'Raga Yaman · Kalyan Thaat · Sa = 196.0 Hz (G3)',
      saHz: 196.0,
      shrutis: [
        { cents: 203.91, label: 'Shuddha Re (9/8)' },
        { cents: 386.31, label: 'Shuddha Ga (5/4)' },
        { cents: 498.04, label: 'FORBIDDEN: Shuddha Ma (4/3)', forbidden: true },
        { cents: 590.22, label: 'Tivra Ma (45/32)' }
      ],
      range: [140, 660],
      ornamentTag: 'Alert: Varjya Swara at 498.0c',
      curveFn: function (u) {
        if (u < 0.28) return 203.91;
        if (u < 0.42) {
          const p = (u - 0.28) / 0.14;
          return 203.91 + (386.31 - 203.91) * p;
        }
        if (u < 0.58) return 386.31;
        if (u < 0.72) {
          const p = (u - 0.58) / 0.14;
          return 386.31 + (498.04 - 386.31) * p;
        }
        return 498.04;
      },
      guruCurveFn: function (u) {
        if (u < 0.25) return 203.91;
        if (u < 0.45) {
          const p = (u - 0.25) / 0.20;
          return 203.91 + (386.31 - 203.91) * p;
        }
        if (u < 0.65) return 386.31;
        if (u < 0.85) {
          const p = (u - 0.65) / 0.20;
          return 386.31 + (590.22 - 386.31) * p;
        }
        return 590.22;
      },
      analystBreakdown: {
        ragaGrammar: 'CRITICAL TIER 1 DEFICIT: Shuddha Ma (498.0 cents, ratio 4/3) was sustained for 420 ms. Shuddha Ma is strictly forbidden (Varjya) in pure Raga Yaman. Its presence breaks the Kalyan mood.',
        kinematics: 'Measured pitch plateaued at 498.0 cents with zero acceleration. In the Guru Correction, Shuddha Ma is eliminated; the phrase glides directly from Ga (386.3c) to Tivra Ma (590.2c).',
        sadhana: 'Practice the canonical triad: Gandhar (386c) -> Tivra Ma (590c) -> Pancham (702c). Hear Tivra Ma as a leading tone leaning upward into Pancham.'
      },
      gayaki: {
        tier: 'TIER 1 · STRUCTURAL RAGA VIOLATION',
        score: '61.8%',
        headline: 'Forbidden Shuddha Ma Detected',
        detail: 'Phrase dwells for 420 ms on Shuddha Ma (498.0 cents, ratio 4/3). Pure Raga Yaman strictly prohibits Shuddha Ma and requires Tivra Ma (590.2 cents, ratio 45/32).',
        drill: 'Anchor on Shuddha Ga (386.3c), hear the upper Pa (702.0c) in the tanpura, and approach Tivra Ma (590.2c) as a leading tone just 111.7 cents below Pa.',
        target: '590.2 cents (45/32)',
        measured: '498.0 cents (-92.2c)',
        velocity: '248.0 cents/sec',
        grammar: '1 Varjya Violation'
      },
      western: {
        tier: '12-TET PITCH GRID AUDIT',
        score: '98.2%',
        headline: 'Clean Perfect Fourth (500c)',
        detail: 'Western 12-TET mode scores this note as an accurate C4 perfect fourth (498.0c vs 500.0c) because it has no awareness of Kalyan Thaat raga grammar.',
        drill: 'Switch to Gayaki Mode when practicing Hindustani ragas so structural scale violations are caught before microtonal cent scoring.',
        target: '500.0 cents (12-TET)',
        measured: '498.0 cents (-2.0c)',
        velocity: '248.0 cents/sec',
        grammar: 'Lydian / Major Mix'
      }
    },

    darbari_andolan: {
      badge: 'Raga Darbari Kanada · Asavari Thaat · Sa = 146.8 Hz (D3)',
      saHz: 146.83,
      shrutis: [
        { cents: 203.91, label: 'Shuddha Re (9/8)' },
        { cents: 294.13, label: 'Atikomal Ga (32/27)' },
        { cents: 315.64, label: 'Komal Ga (6/5)' },
        { cents: 498.04, label: 'Shuddha Ma (4/3)' }
      ],
      range: [160, 540],
      ornamentTag: 'Detected: Andolan (2.1 Hz, ±38c)',
      curveFn: function (u) {
        if (u < 0.18) return 498.04;
        if (u < 0.28) {
          const p = (u - 0.18) / 0.10;
          return 498.04 - (498.04 - 294.13) * p;
        }
        const t = (u - 0.28) * 3.2;
        return 294.13 + 38.0 * Math.sin(2 * Math.PI * 2.1 * t);
      },
      guruCurveFn: function (u) {
        if (u < 0.18) return 498.04;
        if (u < 0.28) {
          const p = (u - 0.18) / 0.10;
          return 498.04 - (498.04 - 294.13) * p;
        }
        const t = (u - 0.28) * 3.2;
        return 294.13 + 38.0 * Math.sin(2 * Math.PI * 2.1 * t);
      },
      analystBreakdown: {
        ragaGrammar: 'PERFECT GAYAKI EXECUTION: Authentic Darbari Kanada (Asavari Thaat) Komal Ga oscillation confirmed. In Darbari, Komal Ga (32/27, 294.1c) must never be flat or static; it must swing with grave, slow majesty.',
        kinematics: 'Oscillation frequency measured at 2.1 Hz with a ±38 cent excursion, matching the authentic Darbari Andolan band (1.5 - 2.5 Hz). High-frequency wavelet energy (a1) is zero.',
        sadhana: 'Maintain this exact 2.1 Hz pendulum tempo. Focus on keeping the lower turning point centered on Shuddha Re without losing throat resonance.'
      },
      gayaki: {
        tier: 'TIER 2 · ORNAMENT INTEGRITY',
        score: '97.8%',
        headline: 'Authentic 2.1 Hz Darbari Andolan',
        detail: 'Slow, deliberate 2.1 Hz oscillation centered on Atikomal Ga (294.1 cents, 32/27) descending from Shuddha Ma with a 38-cent swing. Zero penalty applied to oscillation excursion.',
        drill: 'Maintain the 2.1 Hz pendulum tempo between Shuddha Ma resonance and Atikomal Ga without letting the oscillation accelerate past 3.5 Hz.',
        target: '294.1 cents (32/27)',
        measured: '294.4 cents (+0.3c)',
        velocity: '495.0 cents/sec',
        grammar: 'Darbari Pakad Match'
      },
      western: {
        tier: '12-TET PITCH GRID AUDIT',
        score: '71.4%',
        headline: 'Wide Pitch Instability Flagged',
        detail: 'A standard Western tuner misclassifies a 2.1 Hz ±38 cent Darbari Andolan around 294 cents as an unstable, flat minor third (300c) with excessive pitch wobble.',
        drill: 'In Western mode, vibrato is expected at 5.5 to 7.0 Hz centered at 300 cents. Use Gayaki Mode for authentic Darbari Kanada evaluation.',
        target: '300.0 cents (12-TET)',
        measured: '294.4 cents (±38c)',
        velocity: '495.0 cents/sec',
        grammar: 'Wide Oscillation'
      }
    },

    darbari_flat: {
      badge: 'Raga Darbari Kanada · Asavari Thaat · Sa = 146.8 Hz (D3)',
      saHz: 146.83,
      shrutis: [
        { cents: 203.91, label: 'Shuddha Re (9/8)' },
        { cents: 294.13, label: 'Target: Atikomal Ga (294.1c)' },
        { cents: 498.04, label: 'Shuddha Ma (4/3)' }
      ],
      range: [180, 520],
      ornamentTag: 'Deficit: -24.2c Flat Shruti Drift',
      curveFn: function (u) {
        if (u < 0.2) return 498.04;
        if (u < 0.35) {
          const p = (u - 0.2) / 0.15;
          return 498.04 - (498.04 - 269.9) * p;
        }
        return 269.9 + 5.0 * Math.sin(2 * Math.PI * 1.8 * u);
      },
      guruCurveFn: function (u) {
        if (u < 0.18) return 498.04;
        if (u < 0.28) {
          const p = (u - 0.18) / 0.10;
          return 498.04 - (498.04 - 294.13) * p;
        }
        const t = (u - 0.28) * 3.2;
        return 294.13 + 38.0 * Math.sin(2 * Math.PI * 2.1 * t);
      },
      analystBreakdown: {
        ragaGrammar: 'STRUCTURAL TIER 2 DEFICIT: The sustained tone collapsed to 269.9 cents with no Andolan. Holding Komal Ga flat without oscillation strips Darbari Kanada of its gravity and raga bhāva.',
        kinematics: 'Oscillation depth is only ±5 cents (essentially static). Guru Correction introduces the mandatory 2.1 Hz, ±38 cent oscillation centered on 294.1 cents.',
        sadhana: 'Engage diaphragmatic breath support. Allow the pitch to oscillate gently between 294.1 cents and 203.9 cents at 2 beats per second.'
      },
      gayaki: {
        tier: 'TIER 3 · MICROTONAL SHRUTI DRIFT',
        score: '68.5%',
        headline: 'Atikomal Ga Settled -24.2 Cents Flat',
        detail: 'Steady-state segment after descending from Ma collapses to 269.9 cents instead of holding the 32/27 Pythagorean minor third at 294.1 cents.',
        drill: 'Listen to the fifth harmonic of the Pa string in the tanpura and raise your Komal Ga posture by 24 cents without tensing the larynx.',
        target: '294.1 cents (32/27)',
        measured: '269.9 cents (-24.2c)',
        velocity: '118.0 cents/sec',
        grammar: 'Scale Valid / Intonation Low'
      },
      western: {
        tier: '12-TET PITCH GRID AUDIT',
        score: '64.0%',
        headline: 'Minor Third -30.1 Cents Flat',
        detail: 'Sustained pitch settles at 269.9 cents, falling 30.1 cents below the equal-tempered minor third (300.0 cents).',
        drill: 'Support diaphragmatic airflow on the descent from fourth to minor third to prevent pitch sag at phrase endings.',
        target: '300.0 cents (12-TET)',
        measured: '269.9 cents (-30.1c)',
        velocity: '118.0 cents/sec',
        grammar: 'Flat Sustained Note'
      }
    },

    bhairav_flutter: {
      badge: 'Raga Bhairav · Bhairav Thaat · Sa = 146.8 Hz (D3)',
      saHz: 146.83,
      shrutis: [
        { cents: 0, label: 'Sa (1/1)' },
        { cents: 90.22, label: 'Atikomal Re (256/243)' },
        { cents: 111.73, label: 'Komal Re (16/15)' },
        { cents: 386.31, label: 'Shuddha Ga (5/4)' }
      ],
      range: [-30, 420],
      ornamentTag: 'Alert: 6.0 Hz Vibrato Flutter',
      curveFn: function (u) {
        if (u < 0.2) return 0;
        const t = (u - 0.2) * 3.0;
        return 90.22 + 34.0 * Math.sin(2 * Math.PI * 6.0 * t);
      },
      guruCurveFn: function (u) {
        if (u < 0.2) return 0;
        if (u < 0.5) return 90.22;
        const t = (u - 0.5) * 2.0;
        return 90.22 + 24.0 * Math.sin(2 * Math.PI * 2.2 * t);
      },
      analystBreakdown: {
        ragaGrammar: 'MICROTONAL TIER 3 DEFICIT: Western 6.0 Hz laryngeal flutter detected on Komal Re. Raga Bhairav (Bhairav Thaat) demands solemn sthirata (steady held tone) or slow, deep Andolan touching Sa.',
        kinematics: 'Wavelet analysis shows strong 6.0 Hz periodicity (a1 scale). Guru Correction replaces this with pure sthirata followed by a slow, solemn 2.2 Hz pulse.',
        sadhana: 'Practice holding Sa dead-steady for 4 seconds on breath. Then slide to Atikomal Re (90.2 cents) without shaking the vocal cords. Let the tone ring pure.'
      },
      gayaki: {
        tier: 'TIER 2 · ORNAMENT INTEGRITY',
        score: '66.2%',
        headline: '6.0 Hz Western Vibrato on Komal Re',
        detail: 'Oscillation on Bhairav Atikomal Re (90.2 cents) runs at 6.0 Hz, crossing the 5.5 Hz Gayaki flutter threshold. Authentic Bhairav Andolan requires a slow 1.8 to 3.2 Hz swing.',
        drill: 'First hold a dead-straight Nabhi (navel-supported) tone at 90.2 cents for 3 seconds, then introduce a slow 2 Hz pulse from Sa.',
        target: '1.8 to 3.2 Hz Rate',
        measured: '6.0 Hz Flutter Rate',
        velocity: '1280.0 cents/sec',
        grammar: 'Style Mismatch'
      },
      western: {
        tier: '12-TET PITCH GRID AUDIT',
        score: '94.8%',
        headline: 'Balanced 6.0 Hz Classical Vibrato',
        detail: 'In Western Contemporary mode, a 6.0 Hz modulation with ±34 cent extent is rewarded as an even, healthy vocal vibrato.',
        drill: 'Center the vibrato carrier +10 cents higher if matching a 100-cent equal-tempered minor second on keyboard.',
        target: '5.5 to 7.0 Hz Rate',
        measured: '6.0 Hz (±34 cents)',
        velocity: '1280.0 cents/sec',
        grammar: 'Optimal Western Vibrato'
      }
    },

    real_vocal: {
      badge: 'Saraga Concert Archive · Real Human Vocal · Sa = 161.5 Hz',
      saHz: 161.5,
      shrutis: [
        { cents: 0, label: 'Sa (0.0c)' },
        { cents: 203.91, label: 'Shuddha Re (203.9c)' },
        { cents: 315.64, label: 'Komal Ga (315.6c)' },
        { cents: 498.04, label: 'Shuddha Ma (498.0c)' }
      ],
      range: [-40, 550],
      ornamentTag: 'Detected: Kan + Meend + Andolan',
      curveFn: function (u) {
        if (u < 0.08) return 498.04;
        if (u < 0.45) {
          const p = (u - 0.08) / 0.37;
          const s = p * p * (3 - 2 * p);
          return 315.64 - (315.64 - 203.91) * s + 12 * Math.sin(p * Math.PI * 3);
        }
        if (u < 0.78) {
          const p = (u - 0.45) / 0.33;
          return 203.91 + 26 * Math.sin(2 * Math.PI * 2.6 * p * 1.4);
        }
        const p = (u - 0.78) / 0.22;
        return 203.91 * (1 - p);
      },
      guruCurveFn: function (u) {
        if (u < 0.08) return 498.04;
        if (u < 0.45) {
          const p = (u - 0.08) / 0.37;
          const s = p * p * (3 - 2 * p);
          return 315.64 - (315.64 - 203.91) * s;
        }
        if (u < 0.78) {
          const p = (u - 0.45) / 0.33;
          return 203.91 + 20 * Math.sin(2 * Math.PI * 2.2 * p * 1.4);
        }
        const p = (u - 0.78) / 0.22;
        return 203.91 * (1 - p);
      },
      analystBreakdown: {
        ragaGrammar: 'Saraga Indian Classical Vocal Archive: Features authentic Khayal vocalization with microtonal touches of Shuddha Ma, Komal Ga, and Re.',
        kinematics: 'Savitzky-Golay filtering extracts smooth Meends and Kan grace notes. Real-time factor is 0.06x on standard CPU.',
        sadhana: 'Shadow the vocal trajectory using the frame scrubber to observe how the singer glides continuously between swaras.'
      },
      gayaki: {
        tier: 'TIER 2 · CONCERT ARCHIVE TELEMETRY',
        score: '93.7%',
        headline: 'Kan Prefix into Descending Meend',
        detail: 'Authentic human vocal recording (161.5 Hz tonic) opens with a 75 ms Kan touch on Ma (498c), glides smoothly across Komal Ga into Re, and resolves to Sa.',
        drill: 'Notice how the vocalist touches Ma for 75 ms before descending on Komal Ga; replicate this Kan prefix to establish raga identity immediately.',
        target: '161.5 Hz Movable Sa',
        measured: '93.7% Voiced Frames',
        velocity: '540.0 cents/sec',
        grammar: 'Authentic Gayaki Contour'
      },
      western: {
        tier: '12-TET PITCH GRID AUDIT',
        score: '79.5%',
        headline: 'Continuous Microtonal Inflections',
        detail: 'Human classical phrasing spends 64% of voiced frames in deliberate inter-note glides and microtonal inflections outside static 12-TET semitone boxes.',
        drill: 'Compare Gayaki and Western modes on this recording to see why static cent-error graders fail on expressive Indian vocal lines.',
        target: '12-TET Nearest Bin',
        measured: '±18.4c Dynamic Swing',
        velocity: '540.0 cents/sec',
        grammar: 'Expressive Microtonality'
      }
    }
  };"""

# Replace PHRASE_LIBRARY
pattern = r"  const PHRASE_LIBRARY = \{.*?\n  \};\n\n  /\* ==="
match = re.search(pattern, code, flags=re.DOTALL)
if not match:
    print("Could not find PHRASE_LIBRARY in app.js")
    exit(1)

code = code[:match.start()] + new_phrase_library + "\n\n  /* ===" + code[match.end():]
print("PHRASE_LIBRARY updated successfully.")

with open("app.js", "w", encoding="utf-8") as f:
    f.write(code)
