target_file = r'd:\Music\app.js'

with open(target_file, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update CANONICAL_LYRICS_MAP
old_lyrics_map = """  const CANONICAL_LYRICS_MAP = {
    yaman_meend: "E-ri aa-li pi-ya bi-na sa-khi kal na pa-rat ghar aa-ve",
    yaman_varjya: "Ni-si di-na ta-da-pat chain na aa-ve",
    darbari_andolan: "A-no-kha laad-la khe-lan-ko maa-nge chaand",
    darbari_flat: "Haz-rat Khwa-ja sang khe-lie ho-ri",
    bhairav_flutter: "Jaa-go mo-han pya-re jaa-go nan-da la-la",
    real_vocal: "Baa-je re mu-ra-li-ya baa-je baan-su-ri"
  };"""

new_lyrics_map = """  const CANONICAL_LYRICS_MAP = {
    yaman_meend: "E-ri aa-li pi-ya bi-na sa-khi kal na pa-rat ghar aa-ve",
    yaman_eri_aali: "E-ri aa-li pi-ya bi-na sa-khi kal na pa-rat ghar aa-ve",
    yaman_varjya: "Ni-si di-na ta-da-pat chain na aa-ve",
    darbari_andolan: "A-no-kha laad-la khe-lan-ko maa-nge chaand",
    darbari_rakhwale: "O du-ni-ya ke rakh-waa-le su-no dard bha-re var-daan",
    darbari_flat: "Haz-rat Khwa-ja sang khe-lie ho-ri",
    bhairav_flutter: "Jaa-go mo-han pya-re jaa-go nan-da la-la",
    bhairav_jaago: "Jaa-go mo-han pya-re jaa-go nan-da la-la",
    real_vocal: "Baa-je re mu-ra-li-ya baa-je baan-su-ri",
    bhoopali_jyoti: "Jyo-ti ka-lash chhal-ke hue gu-laa-bi laal do na-yan",
    khamaj_panghat: "Mo-he pang-hat pe Nan-da-laal chhed ga-yo re",
    ahir_bhairav_poocho: "Poo-cho na kai-se mai-ne rain bi-tai",
    hamir_madhuban: "Ma-dhu-ban mein Ra-dhi-ka na-che re",
    sohini_kuhu_kuhu: "Ku-hu ku-hu bo-le ko-ya-li-ya kun-jan mein ko-ya-li-ya"
  };

  const CANONICAL_SONG_LEAD_SHEETS = {
    yaman_eri_aali: {
      title: "Eri Aali Piya Bina · Raga Yaman",
      raga: "Yaman",
      notes: [
        { sym: 'N,', wNote: 'B3', cents: -100.0, dev: -0.2, dur: 0.5, key: 59, tab: 'Str 2, Fret 0', flute: '●●●○○○' },
        { sym: 'R', wNote: 'D4', cents: 200.0, dev: +0.4, dur: 0.6, key: 62, tab: 'Str 2, Fret 3', flute: '●●○○○○' },
        { sym: 'G', wNote: 'E4', cents: 400.0, dev: -0.1, dur: 0.6, key: 64, tab: 'Str 1, Fret 0', flute: '●○○○○○' },
        { sym: "M'", wNote: 'F#4', cents: 600.0, dev: +0.8, dur: 0.6, key: 66, tab: 'Str 1, Fret 2', flute: '○○○○○○' },
        { sym: 'P', wNote: 'G4', cents: 700.0, dev: 0.0, dur: 0.8, key: 67, tab: 'Str 1, Fret 3', flute: '●●●●●●' },
        { sym: 'D', wNote: 'A4', cents: 900.0, dev: -0.3, dur: 0.6, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●○○' },
        { sym: 'N', wNote: 'B4', cents: 1100.0, dev: +0.2, dur: 0.7, key: 71, tab: 'Str 1, Fret 7', flute: '●●●○○○' },
        { sym: "S'", wNote: 'C5', cents: 1200.0, dev: 0.0, dur: 1.0, key: 72, tab: 'Str 1, Fret 8', flute: '●●○○○○' }
      ],
      transitions: [
        { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 200, peak_velocity_cents_sec: 1500, expressive_transition_index: 91.0, description: 'Expressive late scoop from Mandra Ni ascending into Shuddha Re.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Classic Gayaki S-curve meend gliding Re → Ga.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Smooth vocal portamento from Shuddha Ga into Tivra Ma.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Fluid microtonal bridge linking Tivra Ma into Pa.' },
        { transition_type: 'Kan Swara / Grace Touch Transition', curvature_name: 'Kan Touch (N)', glyph_text: 'Kan', kan_touch: { swara_symbol: 'N', swara_name: 'Shuddha Ni', touch_duration_ms: 55 }, duration_ms: 250, peak_velocity_cents_sec: 2150, expressive_transition_index: 97.0, description: 'Pa grazes Shuddha Ni for 55ms before resolving to Dha.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Continuous S-curve glide Dha → Ni.' },
        { transition_type: 'Meend / Concave Slide', curvature_name: 'Slide', glyph_text: 'Slide', duration_ms: 200, peak_velocity_cents_sec: 1200, expressive_transition_index: 90.5, description: 'Gentle early-release float connecting Shuddha Ni up to Taar Sa.' }
      ]
    },
    darbari_rakhwale: {
      title: "O Duniya Ke Rakhwale · Raga Darbari",
      raga: "Darbari Kanada",
      notes: [
        { sym: "S'", wNote: 'D5', cents: 1200.0, dev: 0.0, dur: 0.7, key: 74, tab: 'Str 1, Fret 10', flute: '●●○○○○' },
        { sym: 'd', wNote: 'Bb4', cents: 800.0, dev: -0.4, dur: 0.7, key: 70, tab: 'Str 1, Fret 6', flute: '●●●●◐○' },
        { sym: 'P', wNote: 'A4', cents: 700.0, dev: 0.0, dur: 0.8, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●●●' },
        { sym: 'g', wNote: 'F4', cents: 300.0, dev: -0.2, dur: 0.8, key: 65, tab: 'Str 1, Fret 1', flute: '●◐○○○○' },
        { sym: 'm', wNote: 'G4', cents: 500.0, dev: +0.2, dur: 0.6, key: 67, tab: 'Str 1, Fret 3', flute: '◐○○○○○' },
        { sym: 'R', wNote: 'E4', cents: 200.0, dev: +0.3, dur: 0.7, key: 64, tab: 'Str 1, Fret 0', flute: '●●○○○○' },
        { sym: 'S', wNote: 'D4', cents: 0.0, dev: 0.0, dur: 1.0, key: 62, tab: 'Str 2, Fret 3', flute: '●●●○○○' }
      ],
      transitions: [
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 300, peak_velocity_cents_sec: 1350, expressive_transition_index: 96.0, description: 'Majestic descent Taar Sa into oscillating Komal Dha.' },
        { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 250, peak_velocity_cents_sec: 1600, expressive_transition_index: 91.0, description: 'Late scoop landing firmly on Pa.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 350, peak_velocity_cents_sec: 1200, expressive_transition_index: 96.5, description: 'Descending meend from Pa into oscillating Komal Ga.' },
        { transition_type: 'Meend / Linear Ramp', curvature_name: 'Linear', glyph_text: 'Linear', duration_ms: 250, peak_velocity_cents_sec: 800, expressive_transition_index: 86.0, description: 'Steady linear glide Komal Ga to Shuddha Ma.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 250, peak_velocity_cents_sec: 1400, expressive_transition_index: 95.5, description: 'Resonant Gayaki descent Ma into Shuddha Re.' },
        { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 250, peak_velocity_cents_sec: 1550, expressive_transition_index: 91.0, description: 'Gravitational scoop resolving Re down into Sa.' }
      ]
    },
    bhoopali_jyoti: {
      title: "Jyoti Kalash Chhalke · Raga Bhoopali",
      raga: "Bhoopali",
      notes: [
        { sym: 'S', wNote: 'D4', cents: 0.0, dev: 0.0, dur: 0.6, key: 62, tab: 'Str 2, Fret 3', flute: '●●●○○○' },
        { sym: 'R', wNote: 'E4', cents: 200.0, dev: +0.2, dur: 0.6, key: 64, tab: 'Str 1, Fret 0', flute: '●●○○○○' },
        { sym: 'G', wNote: 'F#4', cents: 400.0, dev: 0.0, dur: 0.6, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' },
        { sym: 'P', wNote: 'A4', cents: 700.0, dev: 0.0, dur: 0.7, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●●●' },
        { sym: 'D', wNote: 'B4', cents: 900.0, dev: -0.2, dur: 0.6, key: 71, tab: 'Str 1, Fret 7', flute: '●●●●○○' },
        { sym: 'G', wNote: 'F#4', cents: 400.0, dev: 0.0, dur: 0.9, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' }
      ],
      transitions: [
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.0, description: 'Gentle S-curve glide Sa to Shuddha Re.' },
        { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 200, peak_velocity_cents_sec: 1500, expressive_transition_index: 91.0, description: 'Late scoop landing on Shuddha Ga.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1600, expressive_transition_index: 96.5, description: 'Pentatonic leap Ga to Pa.' },
        { transition_type: 'Kan Swara / Grace Touch Transition', curvature_name: 'Kan Touch (S\')', glyph_text: 'Kan', kan_touch: { swara_symbol: "S'", swara_name: 'Taar Sa', touch_duration_ms: 55 }, duration_ms: 250, peak_velocity_cents_sec: 2200, expressive_transition_index: 97.0, description: 'Pa touches Taar Sa for 55ms before landing on Dha.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 250, peak_velocity_cents_sec: 1450, expressive_transition_index: 95.5, description: 'Majestic descending meend Dha down to Ga.' }
      ]
    },
    ahir_bhairav_poocho: {
      title: "Poocho Na Kaise Maine · Raga Ahir Bhairav",
      raga: "Ahir Bhairav",
      notes: [
        { sym: 'S', wNote: 'D4', cents: 0.0, dev: 0.0, dur: 0.6, key: 62, tab: 'Str 2, Fret 3', flute: '●●●○○○' },
        { sym: 'r', wNote: 'Eb4', cents: 100.0, dev: -0.3, dur: 0.6, key: 63, tab: 'Str 2, Fret 4', flute: '●●◐○○○' },
        { sym: 'G', wNote: 'F#4', cents: 400.0, dev: +0.2, dur: 0.6, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' },
        { sym: 'm', wNote: 'G4', cents: 500.0, dev: 0.0, dur: 0.6, key: 67, tab: 'Str 1, Fret 3', flute: '◐○○○○○' },
        { sym: 'P', wNote: 'A4', cents: 700.0, dev: 0.0, dur: 0.6, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●●●' },
        { sym: 'D', wNote: 'B4', cents: 900.0, dev: -0.2, dur: 0.6, key: 71, tab: 'Str 1, Fret 7', flute: '●●●●○○' },
        { sym: 'n', wNote: 'C5', cents: 1000.0, dev: -0.4, dur: 0.6, key: 72, tab: 'Str 1, Fret 8', flute: '●●●◐○○' },
        { sym: 'D', wNote: 'B4', cents: 900.0, dev: 0.0, dur: 0.8, key: 71, tab: 'Str 1, Fret 7', flute: '●●●●○○' }
      ],
      transitions: [
        { transition_type: 'Gamak / Oscillatory Approach', curvature_name: 'Gamak', glyph_text: 'Gamak', duration_ms: 250, peak_velocity_cents_sec: 1800, expressive_transition_index: 91.0, description: 'Gamak oscillatory shake approaching Komal Re.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1450, expressive_transition_index: 96.0, description: 'Fluid glide Komal Re up to Shuddha Ga.' },
        { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 200, peak_velocity_cents_sec: 1500, expressive_transition_index: 91.5, description: 'Late scoop landing firmly on Shuddha Ma.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Continuous S-curve Ma to Pa.' },
        { transition_type: 'Meend / Linear Ramp', curvature_name: 'Linear', glyph_text: 'Linear', duration_ms: 200, peak_velocity_cents_sec: 950, expressive_transition_index: 87.0, description: 'Linear portamento Pa to Dha.' },
        { transition_type: 'Kan Swara / Grace Touch Transition', curvature_name: 'Kan Touch (S\')', glyph_text: 'Kan', kan_touch: { swara_symbol: "S'", swara_name: 'Taar Sa', touch_duration_ms: 55 }, duration_ms: 250, peak_velocity_cents_sec: 2150, expressive_transition_index: 97.0, description: 'Dha grazes Taar Sa before resolving to Komal Ni.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1380, expressive_transition_index: 95.5, description: 'Graceful descent Komal Ni resolving to Dha.' }
      ]
    },
    hamir_madhuban: {
      title: "Madhuban Mein Radhika · Raga Hamir",
      raga: "Hamir",
      notes: [
        { sym: 'P', wNote: 'A4', cents: 700.0, dev: 0.0, dur: 0.5, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●●●' },
        { sym: "M'", wNote: 'G#4', cents: 600.0, dev: +0.6, dur: 0.5, key: 68, tab: 'Str 1, Fret 4', flute: '○○○○○○' },
        { sym: 'P', wNote: 'A4', cents: 700.0, dev: 0.0, dur: 0.6, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●●●' },
        { sym: 'G', wNote: 'F#4', cents: 400.0, dev: -0.2, dur: 0.6, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' },
        { sym: 'm', wNote: 'G4', cents: 500.0, dev: +0.2, dur: 0.6, key: 67, tab: 'Str 1, Fret 3', flute: '◐○○○○○' },
        { sym: 'R', wNote: 'E4', cents: 200.0, dev: +0.3, dur: 0.6, key: 64, tab: 'Str 1, Fret 0', flute: '●●○○○○' },
        { sym: 'S', wNote: 'D4', cents: 0.0, dev: 0.0, dur: 0.9, key: 62, tab: 'Str 2, Fret 3', flute: '●●●○○○' }
      ],
      transitions: [
        { transition_type: 'Meend / Concave Slide', curvature_name: 'Slide', glyph_text: 'Slide', duration_ms: 150, peak_velocity_cents_sec: 1200, expressive_transition_index: 91.0, description: 'Rapid descending slide Pa into Tivra Ma.' },
        { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 200, peak_velocity_cents_sec: 1450, expressive_transition_index: 91.5, description: 'Late scoop Tivra Ma rebounding to Pa.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1500, expressive_transition_index: 96.0, description: 'Classic Hamir jump: Pa glides smoothly into Ga.' },
        { transition_type: 'Kan Swara / Grace Touch Transition', curvature_name: 'Kan Touch (P)', glyph_text: 'Kan', kan_touch: { swara_symbol: 'P', swara_name: 'Pa', touch_duration_ms: 50 }, duration_ms: 200, peak_velocity_cents_sec: 2100, expressive_transition_index: 97.0, description: 'Ga grazes Pa before landing firmly on Shuddha Ma.' },
        { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 200, peak_velocity_cents_sec: 1550, expressive_transition_index: 92.0, description: 'Resonant scoop Ma into Shuddha Re.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'S-curve glide Re resolving to Sa.' }
      ]
    },
    sohini_kuhu_kuhu: {
      title: "Kuhu Kuhu Bole Koyaliya · Raga Sohini",
      raga: "Sohini",
      notes: [
        { sym: 'S', wNote: 'D4', cents: 0.0, dev: 0.0, dur: 0.5, key: 62, tab: 'Str 2, Fret 3', flute: '●●●○○○' },
        { sym: 'G', wNote: 'F#4', cents: 400.0, dev: 0.0, dur: 0.5, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' },
        { sym: "M'", wNote: 'G#4', cents: 600.0, dev: +0.6, dur: 0.5, key: 68, tab: 'Str 1, Fret 4', flute: '○○○○○○' },
        { sym: 'D', wNote: 'B4', cents: 900.0, dev: -0.2, dur: 0.5, key: 71, tab: 'Str 1, Fret 7', flute: '●●●●○○' },
        { sym: 'N', wNote: 'C#5', cents: 1100.0, dev: +0.2, dur: 0.5, key: 73, tab: 'Str 1, Fret 9', flute: '●●●○○○' },
        { sym: "S'", wNote: 'D5', cents: 1200.0, dev: 0.0, dur: 0.7, key: 74, tab: 'Str 1, Fret 10', flute: '●●○○○○' },
        { sym: 'N', wNote: 'C#5', cents: 1100.0, dev: 0.0, dur: 0.5, key: 73, tab: 'Str 1, Fret 9', flute: '●●●○○○' },
        { sym: 'D', wNote: 'B4', cents: 900.0, dev: -0.2, dur: 0.5, key: 71, tab: 'Str 1, Fret 7', flute: '●●●●○○' },
        { sym: "M'", wNote: 'G#4', cents: 600.0, dev: +0.4, dur: 0.5, key: 68, tab: 'Str 1, Fret 4', flute: '○○○○○○' },
        { sym: 'G', wNote: 'F#4', cents: 400.0, dev: 0.0, dur: 0.8, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' }
      ],
      transitions: [
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1500, expressive_transition_index: 96.0, description: 'Pentatonic ascending leap Sa to Shuddha Ga.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.5, description: 'Sigmoidal S-Curve Meend Ga to Tivra Ma.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1450, expressive_transition_index: 96.5, description: 'Resonant Gayaki Meend Tivra Ma to Dha.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.0, description: 'Continuous S-curve glide Dha to Ni.' },
        { transition_type: 'Meend / Concave Slide', curvature_name: 'Slide', glyph_text: 'Slide', duration_ms: 200, peak_velocity_cents_sec: 1200, expressive_transition_index: 91.0, description: 'Concave float landing on Taar Sa.' },
        { transition_type: 'Kan Swara / Grace Touch Transition', curvature_name: 'Kan Touch (R\')', glyph_text: 'Kan', kan_touch: { swara_symbol: "R'", swara_name: 'Taar Re', touch_duration_ms: 55 }, duration_ms: 250, peak_velocity_cents_sec: 2200, expressive_transition_index: 97.0, description: 'Taar Sa touches Taar Re before descending into Ni.' },
        { transition_type: 'Murki / Rapid Microtonal Turn', curvature_name: 'Murki', glyph_text: 'Murki', duration_ms: 200, peak_velocity_cents_sec: 1800, expressive_transition_index: 93.0, description: 'Rapid circular embellishment Ni → Dha.' },
        { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 200, peak_velocity_cents_sec: 1400, expressive_transition_index: 96.0, description: 'Smooth Gayaki glide Dha to Tivra Ma.' },
        { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 200, peak_velocity_cents_sec: 1450, expressive_transition_index: 91.5, description: 'Convex scoop resolving into Ga.' }
      ]
    }
  };"""

if old_lyrics_map in js:
    js = js.replace(old_lyrics_map, new_lyrics_map)
    print("Updated CANONICAL_LYRICS_MAP and added CANONICAL_SONG_LEAD_SHEETS in app.js")
else:
    print("WARNING: old_lyrics_map not found in app.js")

# 2. Update generateBenchmarkLeadSheet
old_gen_fn = """  function generateBenchmarkLeadSheet(phraseKey, lyricsText) {
    const phrase = PHRASE_LIBRARY[phraseKey] || PHRASE_LIBRARY.yaman_meend;
    const baseSa = userCustomSaHz || phrase.saHz || 146.83;
    const lyrics = lyricsText || CANONICAL_LYRICS_MAP[phraseKey] || "Sa Re Ga Ma Pa Dha Ni Sa";
    const words = lyrics.split(/\s+/);
    const syllables = [];
    words.forEach(function (w) {
      if (w.includes('-')) {
        const parts = w.split('-');
        parts.forEach(function (p, i) {
          if (p) syllables.push(i < parts.length - 1 ? p + '-' : p);
        });
      } else {
        syllables.push(w);
      }
    });

    const mockNotes = [
      { sym: 'S', wNote: 'D4', cents: 0.0, dev: -0.2, dur: 0.6, key: 62, tab: 'Str 2, Fret 3', flute: '●●●○○○' },
      { sym: 'R', wNote: 'E4', cents: 203.9, dev: +0.4, dur: 0.6, key: 64, tab: 'Str 1, Fret 0', flute: '●●○○○○' },
      { sym: 'G', wNote: 'F#4', cents: 386.3, dev: -0.1, dur: 0.7, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' },
      { sym: "M'", wNote: 'G#4', cents: 590.2, dev: +0.8, dur: 0.6, key: 68, tab: 'Str 1, Fret 4', flute: '○○○○○○' },
      { sym: 'P', wNote: 'A4', cents: 702.0, dev: 0.0, dur: 0.8, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●●●' },
      { sym: 'D', wNote: 'B4', cents: 905.9, dev: -0.3, dur: 0.6, key: 71, tab: 'Str 1, Fret 7', flute: '●●●●○○' },
      { sym: 'N', wNote: 'C#5', cents: 1088.3, dev: +0.2, dur: 0.7, key: 73, tab: 'Str 1, Fret 9', flute: '●●●○○○' },
      { sym: "S'", wNote: 'D5', cents: 1200.0, dev: 0.0, dur: 1.0, key: 74, tab: 'Str 1, Fret 10', flute: '●●○○○○' }
    ];"""

new_gen_fn = """  function generateBenchmarkLeadSheet(phraseKey, lyricsText) {
    const phrase = PHRASE_LIBRARY[phraseKey] || PHRASE_LIBRARY.yaman_meend;
    const baseSa = userCustomSaHz || (phrase ? phrase.saHz : 146.83) || 146.83;
    const lyrics = lyricsText || CANONICAL_LYRICS_MAP[phraseKey] || "Sa Re Ga Ma Pa Dha Ni Sa";
    const words = lyrics.split(/\s+/);
    const syllables = [];
    words.forEach(function (w) {
      if (w.includes('-')) {
        const parts = w.split('-');
        parts.forEach(function (p, i) {
          if (p) syllables.push(i < parts.length - 1 ? p + '-' : p);
        });
      } else {
        syllables.push(w);
      }
    });

    const canonicalSong = CANONICAL_SONG_LEAD_SHEETS[phraseKey];
    const mockNotes = (canonicalSong && canonicalSong.notes) ? canonicalSong.notes : [
      { sym: 'S', wNote: 'D4', cents: 0.0, dev: -0.2, dur: 0.6, key: 62, tab: 'Str 2, Fret 3', flute: '●●●○○○' },
      { sym: 'R', wNote: 'E4', cents: 203.9, dev: +0.4, dur: 0.6, key: 64, tab: 'Str 1, Fret 0', flute: '●●○○○○' },
      { sym: 'G', wNote: 'F#4', cents: 386.3, dev: -0.1, dur: 0.7, key: 66, tab: 'Str 1, Fret 2', flute: '●○○○○○' },
      { sym: "M'", wNote: 'G#4', cents: 590.2, dev: +0.8, dur: 0.6, key: 68, tab: 'Str 1, Fret 4', flute: '○○○○○○' },
      { sym: 'P', wNote: 'A4', cents: 702.0, dev: 0.0, dur: 0.8, key: 69, tab: 'Str 1, Fret 5', flute: '●●●●●●' },
      { sym: 'D', wNote: 'B4', cents: 905.9, dev: -0.3, dur: 0.6, key: 71, tab: 'Str 1, Fret 7', flute: '●●●●○○' },
      { sym: 'N', wNote: 'C#5', cents: 1088.3, dev: +0.2, dur: 0.7, key: 73, tab: 'Str 1, Fret 9', flute: '●●●○○○' },
      { sym: "S'", wNote: 'D5', cents: 1200.0, dev: 0.0, dur: 1.0, key: 74, tab: 'Str 1, Fret 10', flute: '●●○○○○' }
    ];"""

if old_gen_fn in js:
    js = js.replace(old_gen_fn, new_gen_fn)
    print("Updated generateBenchmarkLeadSheet in app.js")
else:
    print("WARNING: old_gen_fn not found in app.js")

# In generateBenchmarkLeadSheet, use canonical transitions if available
old_trans_block = """    const mockTransitions = [
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 180, peak_velocity_cents_sec: 1420, expressive_transition_index: 96.5, description: 'Classic Gayaki S-curve meend gliding S → R' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 190, peak_velocity_cents_sec: 1380, expressive_transition_index: 95.0, description: 'Smooth portamento glide R → G' },
      { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 160, peak_velocity_cents_sec: 1650, expressive_transition_index: 91.5, description: 'Late scoop into Tivra Ma' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 175, peak_velocity_cents_sec: 1480, expressive_transition_index: 94.0, description: 'Resonant glide Tivra Ma → Pa' },
      { transition_type: 'Kan Swara / Grace Touch Transition', curvature_name: 'Kan Touch (N)', glyph_text: 'Kan', kan_touch: { swara_symbol: 'N', swara_name: 'Shuddha Ni', touch_duration_ms: 55 }, duration_ms: 220, peak_velocity_cents_sec: 2150, expressive_transition_index: 97.0, description: 'Masterful vocal inflection: Pa grazes Ni for 55ms before resolving to Dha' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 180, peak_velocity_cents_sec: 1390, expressive_transition_index: 95.5, description: 'Smooth Gayaki glide D → N' },
      { transition_type: 'Meend / Concave Slide', curvature_name: 'Slide', glyph_text: 'Slide', duration_ms: 210, peak_velocity_cents_sec: 1200, expressive_transition_index: 92.0, description: 'Gentle float resolving N into Taar Sa' }
    ];"""

new_trans_block = """    const mockTransitions = (canonicalSong && canonicalSong.transitions) ? canonicalSong.transitions : [
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 180, peak_velocity_cents_sec: 1420, expressive_transition_index: 96.5, description: 'Classic Gayaki S-curve meend gliding S → R' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 190, peak_velocity_cents_sec: 1380, expressive_transition_index: 95.0, description: 'Smooth portamento glide R → G' },
      { transition_type: 'Meend / Convex Scoop', curvature_name: 'Scoop', glyph_text: 'Scoop', duration_ms: 160, peak_velocity_cents_sec: 1650, expressive_transition_index: 91.5, description: 'Late scoop into Tivra Ma' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 175, peak_velocity_cents_sec: 1480, expressive_transition_index: 94.0, description: 'Resonant glide Tivra Ma → Pa' },
      { transition_type: 'Kan Swara / Grace Touch Transition', curvature_name: 'Kan Touch (N)', glyph_text: 'Kan', kan_touch: { swara_symbol: 'N', swara_name: 'Shuddha Ni', touch_duration_ms: 55 }, duration_ms: 220, peak_velocity_cents_sec: 2150, expressive_transition_index: 97.0, description: 'Masterful vocal inflection: Pa grazes Ni for 55ms before resolving to Dha' },
      { transition_type: 'Meend / S-Curve Glide', curvature_name: 'S-Glide', glyph_text: 'S-Meend', duration_ms: 180, peak_velocity_cents_sec: 1390, expressive_transition_index: 95.5, description: 'Smooth Gayaki glide D → N' },
      { transition_type: 'Meend / Concave Slide', curvature_name: 'Slide', glyph_text: 'Slide', duration_ms: 210, peak_velocity_cents_sec: 1200, expressive_transition_index: 92.0, description: 'Gentle float resolving N into Taar Sa' }
    ];"""

if old_trans_block in js:
    js = js.replace(old_trans_block, new_trans_block)
    print("Updated mockTransitions in generateBenchmarkLeadSheet")
else:
    print("WARNING: old_trans_block not found in app.js")

# 3. Add updateLiveLeadSheetFollower in handleIncomingPitchFrame
old_pitch_frame_end = """    detectLiveOrnamentAndDiagnostics(cents, saHz);
    updateLiveNoteTracker(data.pitch, cents, saHz, data.rms || 0);
    const curVel = liveVelocityHistory.length ? liveVelocityHistory[liveVelocityHistory.length - 1].vel : 0;
    computeAffectiveCoordinates(cents, curVel, data.rms || 0.05, data.pitch);
    renderRasaRadarCanvas();
    renderLivePitchCanvas();"""

new_pitch_frame_end = """    detectLiveOrnamentAndDiagnostics(cents, saHz);
    updateLiveNoteTracker(data.pitch, cents, saHz, data.rms || 0);
    updateLiveLeadSheetFollower(data.pitch, cents, saHz);
    const curVel = liveVelocityHistory.length ? liveVelocityHistory[liveVelocityHistory.length - 1].vel : 0;
    computeAffectiveCoordinates(cents, curVel, data.rms || 0.05, data.pitch);
    renderRasaRadarCanvas();
    renderLivePitchCanvas();"""

if old_pitch_frame_end in js:
    js = js.replace(old_pitch_frame_end, new_pitch_frame_end)
    print("Added updateLiveLeadSheetFollower call to handleIncomingPitchFrame in app.js")
else:
    print("WARNING: old_pitch_frame_end not found in app.js")

# 4. Implement updateLiveLeadSheetFollower and Bhatkhande modal functions
follower_and_bhatkhande_js = """
  /* =========================================================================
     LIVE MIC LEAD SHEET FOLLOWER (KARAOKE NOTE TRACKER & MEEND FEEDBACK)
     ========================================================================= */
  let lastSungLeadSheetIdx = -1;

  function updateLiveLeadSheetFollower(pitch, cents, saHz) {
    if (!currentLeadSheetScore || !currentLeadSheetScore.measures) return;
    const viewport = document.getElementById('sheet-music-viewport');
    const feedbackPill = document.getElementById('sheet-live-feedback');
    if (!viewport) return;

    if (!pitch || cents === null || isNaN(cents)) {
      viewport.querySelectorAll('.sheet-event.is-sung-active').forEach(function (el) {
        el.classList.remove('is-sung-active');
      });
      return;
    }

    const eventDoms = viewport.querySelectorAll('.sheet-event');
    if (eventDoms.length === 0) return;

    let allEvents = [];
    currentLeadSheetScore.measures.forEach(function (m) {
      (m.events || []).forEach(function (ev) { allEvents.push(ev); });
    });
    if (allEvents.length === 0) return;

    let bestIdx = -1;
    let minCentsDiff = 9999;
    const curVel = liveVelocityHistory.length ? liveVelocityHistory[liveVelocityHistory.length - 1].vel : 0;
    const absVel = Math.abs(curVel);

    allEvents.forEach(function (ev, idx) {
      let evTargetCents = 0;
      if (ev.frequency_hz && saHz > 0) {
        evTargetCents = 1200 * Math.log2(ev.frequency_hz / saHz);
        while (evTargetCents > 1150) evTargetCents -= 1200;
        while (evTargetCents < -150) evTargetCents += 1200;
      }
      let modUserCents = ((cents % 1200) + 1200) % 1200;
      let modTargetCents = ((evTargetCents % 1200) + 1200) % 1200;
      let diff = Math.abs(modUserCents - modTargetCents);
      if (diff > 600) diff = 1200 - diff;

      if (diff < minCentsDiff) {
        minCentsDiff = diff;
        bestIdx = idx;
      }
    });

    if (bestIdx !== -1 && minCentsDiff <= 85.0 && eventDoms[bestIdx]) {
      eventDoms.forEach(function (el, i) {
        if (i === bestIdx) {
          el.classList.add('is-sung-active');
          if (minCentsDiff <= 14.0) {
            el.classList.add('is-pure-tune');
            el.classList.remove('is-deviant');
          } else {
            el.classList.add('is-deviant');
            el.classList.remove('is-pure-tune');
          }
        } else {
          el.classList.remove('is-sung-active');
        }
      });

      const matchedEv = allEvents[bestIdx];
      if (feedbackPill && matchedEv) {
        const sign = minCentsDiff <= 14.0 ? 'Pure Tune' : (cents > 0 ? 'Sharp' : 'Flat');
        feedbackPill.textContent = 'Singing: ' + (matchedEv.syllable || '—') + ' (' + (matchedEv.note_sargam || matchedEv.note_western) + ') · ' + (minCentsDiff <= 14.0 ? 'In Pure Tune' : minCentsDiff.toFixed(1) + 'c ' + sign);
      }

      // Track transition bridge activation
      if (lastSungLeadSheetIdx !== -1 && lastSungLeadSheetIdx !== bestIdx) {
        const bridgeDoms = viewport.querySelectorAll('.sheet-transition-bridge');
        const bridgeIdx = Math.min(lastSungLeadSheetIdx, bestIdx);
        if (bridgeDoms[bridgeIdx] && absVel >= 160) {
          bridgeDoms[bridgeIdx].classList.add('is-meend-active');
          if (feedbackPill) {
            feedbackPill.textContent = 'Meend Locked: ' + allEvents[bridgeIdx].note_sargam + ' → ' + matchedEv.note_sargam + ' (' + Math.round(absVel) + ' c/s)';
          }
          setTimeout(function () {
            if (bridgeDoms[bridgeIdx]) bridgeDoms[bridgeIdx].classList.remove('is-meend-active');
          }, 800);
        }
      }

      lastSungLeadSheetIdx = bestIdx;
    }
  }

  /* =========================================================================
     BHATKHANDE CONSERVATORY SCORE MODAL VIEWER
     ========================================================================= */
  let activeBhatkhandeScoreData = null;

  async function openBhatkhandeScoreModal() {
    const modal = document.getElementById('bhatkhande-score-modal');
    const content = document.getElementById('bk-modal-content');
    const titleEl = document.getElementById('bk-modal-title');
    if (!modal || !content) return;

    modal.classList.remove('is-hidden');
    content.innerHTML = '<div class="notation-chip-placeholder">Formatting conservatory Bhatkhande score...</div>';

    try {
      const scoreToExport = currentLeadSheetScore || generateBenchmarkLeadSheet(activeBenchmarkSongKey || 'yaman_eri_aali');
      const res = await fetch('/api/export-sargam', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lead_sheet: scoreToExport })
      });

      if (res.ok) {
        const data = await res.json();
        activeBhatkhandeScoreData = data;
        if (data.bhatkhande_sheet && data.bhatkhande_sheet.html_score) {
          if (titleEl) titleEl.textContent = data.bhatkhande_sheet.title || 'Bhatkhande Classical Notation Score';
          content.innerHTML = 
            data.bhatkhande_sheet.html_score +
            '<div style="margin-top: 16px;"><span class="bk-header-tag">RAW ASCII CONSERVATORY TRANSCRIPT</span><pre class="bhatkhande-raw-pre">' +
            (data.bhatkhande_sheet.ascii_sheet || data.bhatkhande_line || '') +
            '</pre></div>';
          return;
        }
      }
      throw new Error('API offline');
    } catch (e) {
      // Local fallback renderer
      const songKey = activeBenchmarkSongKey || 'yaman_eri_aali';
      const score = currentLeadSheetScore || generateBenchmarkLeadSheet(songKey);
      content.innerHTML = 
        '<div class="bhatkhande-score-card">' +
          '<div class="bhatkhande-header-box">' +
            '<h3 class="bhatkhande-title">' + (score.title || 'Bhatkhande Classical Sargam Score') + '</h3>' +
            '<div class="bhatkhande-meta-row">' +
              '<span class="bk-meta-pill">Tala: Teentaal (16 Matras)</span>' +
              '<span class="bk-meta-pill">Tempo: ' + (score.tempo_bpm || 84) + ' BPM</span>' +
              '<span class="bk-meta-pill">Sam: + | Khali: 0 | Taali: 2, 3</span>' +
            '</div>' +
          '</div>' +
          '<div style="margin-top: 14px;"><span class="bk-header-tag">BHATKHANDE SWARAS & LYRICS</span>' +
          '<pre class="bhatkhande-raw-pre">' +
          'Swaras:  सा   रे   ग   म॑   प   ध   नि   सां |\\n' +
          'Lyrics:  E-   ri   aa-  li   pi-  ya  bi-  na  |\\n' +
          'Vibhag:  +    .    .    .    0    .   .    .   |' +
          '</pre></div>' +
        '</div>';
    }
  }

  function initBhatkhandeModalControls() {
    const exportBtn = document.getElementById('btn-export-bhatkhande-score');
    const closeBtn = document.getElementById('btn-close-bhatkhande');
    const backdrop = document.getElementById('bk-modal-backdrop');
    const copyBtn = document.getElementById('btn-copy-bhatkhande');
    const printBtn = document.getElementById('btn-print-bhatkhande');
    const modal = document.getElementById('bhatkhande-score-modal');

    if (exportBtn) {
      exportBtn.addEventListener('click', openBhatkhandeScoreModal);
    }

    function closeModal() {
      if (modal) modal.classList.add('is-hidden');
    }

    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (backdrop) backdrop.addEventListener('click', closeModal);

    if (copyBtn) {
      copyBtn.addEventListener('click', function () {
        const pre = document.querySelector('.bhatkhande-raw-pre');
        if (pre) {
          navigator.clipboard.writeText(pre.textContent).then(function () {
            copyBtn.textContent = '✓ Copied!';
            setTimeout(function () { copyBtn.textContent = '📋 Copy Text'; }, 1800);
          });
        }
      });
    }

    if (printBtn) {
      printBtn.addEventListener('click', function () {
        window.print();
      });
    }
  }
"""

if "function updateLiveLeadSheetFollower" not in js:
    # Insert follower and bhatkhande functions right before initSheetMusicControls
    js = js.replace("  function initSheetMusicControls() {", follower_and_bhatkhande_js + "\n  function initSheetMusicControls() {")
    print("Added updateLiveLeadSheetFollower and Bhatkhande modal functions to app.js")
else:
    print("Follower and Bhatkhande functions already present in app.js")

# In initAntarSwaraBenchmark, update Lead Sheet when clicking a song button
old_song_click = """    const songBtns = document.querySelectorAll('.antar-song-btn');
    songBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        const key = btn.getAttribute('data-song-key');
        if (key) {
          renderAntarSwaraTransitions(key);
        }
      });
    });"""

new_song_click = """    const songBtns = document.querySelectorAll('.antar-song-btn');
    songBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        const key = btn.getAttribute('data-song-key');
        if (key) {
          renderAntarSwaraTransitions(key);
          // Also synchronize the Lead Sheet workstation to this song!
          const songScore = generateBenchmarkLeadSheet(key);
          renderSheetMusicScore(songScore);
          const lyricsInput = document.getElementById('lyrics-extractor-input');
          if (lyricsInput && CANONICAL_LYRICS_MAP[key]) {
            lyricsInput.value = CANONICAL_LYRICS_MAP[key];
          }
        }
      });
    });"""

if old_song_click in js:
    js = js.replace(old_song_click, new_song_click)
    print("Synchronized song selection to Lead Sheet in initAntarSwaraBenchmark in app.js")
else:
    print("WARNING: old_song_click not found in app.js")

# Call initBhatkhandeModalControls in DOMContentLoaded
if "initBhatkhandeModalControls();" not in js:
    js = js.replace("initSheetMusicControls();", "initSheetMusicControls();\n    initBhatkhandeModalControls();")
    print("Added initBhatkhandeModalControls to DOMContentLoaded in app.js")

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js successfully.")
