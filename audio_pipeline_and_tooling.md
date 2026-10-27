# Audio Engineering, Signal Processing & Pipeline Tooling

*Technical implementation guide for source separation, pitch extraction, microtonal calibration, ornament feature detection, and notation pipelines.*

---

## Table of Contents
1. [Vocal Isolation & Source Separation](#1-vocal-isolation--source-separation)
   - [BS-Roformer & Mel-Band Roformer](#bs-roformer--mel-band-roformer)
   - [HT-Demucs v4](#ht-demucs-v4)
   - [Solving Classical Bleed: Drone & Percussion Leakage](#solving-classical-bleed-drone--percussion-leakage)
2. [Continuous Fundamental Frequency ($F_0$) Extraction](#2-continuous-fundamental-frequency-f_0-extraction)
   - [CREPE & torchcrepe](#crepe--torchcrepe)
   - [RMVPE (Robust Multiscale Vocal Pitch Estimation)](#rmvpe-robust-multiscale-vocal-pitch-estimation)
   - [Spotify Basic Pitch](#spotify-basic-pitch)
   - [Pitch Extraction Tool Comparison Matrix](#pitch-extraction-tool-comparison-matrix)
3. [Tonal Normalization & 22-Shruti Microtonal Calibration](#3-tonal-normalization--22-shruti-microtonal-calibration)
   - [Converting Hertz to Cents Relative to Tonic ($Sa$)](#converting-hertz-to-cents-relative-to-tonic-sa)
   - [Traditional 22-Shruti Mathematical Ratios vs. 12-TET](#traditional-22-shruti-mathematical-ratios-vs-12-tet)
4. [Algorithmic Feature Extraction for Ornaments](#4-algorithmic-feature-extraction-for-ornaments)
   - [Rule-Based Heuristic Classifiers](#rule-based-heuristic-classifiers)
   - [Feature Detection Math](#feature-detection-math)
   - [Pakad Matching via Dynamic Time Warping (DTW)](#pakad-matching-via-dynamic-time-warping-dtw)
5. [Export & Transcription Formats](#5-export--transcription-formats)
   - [Sargam Text Format with Diacritics](#sargam-text-format-with-diacritics)
   - [High-Resolution MIDI with 14-Bit Pitch Bend](#high-resolution-midi-with-14-bit-pitch-bend)
6. [Cross-Link Navigation](#6-cross-link-navigation)

---

## 1. Vocal Isolation & Source Separation

The precision of pitch estimation, microtonal intonation, and ornament detection depends on a clean vocal track. In classical Indian recordings, the tanpura drone, harmonium, and tabla strokes severely interfere with naive pitch trackers.

```
┌─────────────────┐       ┌────────────────────────┐       ┌───────────────────────────┐
│  Raw Polyphonic │  ───► │   BS-Roformer / UVR5   │  ───► │  Clean Vocal Stem         │
│  Audio Mix      │       │   Ensemble Separation  │       │  (Tanpura & Tabla Free)   │
└─────────────────┘       └────────────────────────┘       └─────────────┬─────────────┘
                                                                         │
                                                                         ▼
                                                           ┌───────────────────────────┐
                                                           │  CREPE / RMVPE F0 Curve   │
                                                           │  (Time, Freq, Confidence) │
                                                           └─────────────┬─────────────┘
                                                                         │
                                                                         ▼
                                                           ┌───────────────────────────┐
                                                           │  Tonic (Sa) Normalization │
                                                           │  & 22-Shruti Cent Grid    │
                                                           └───────────────────────────┘
```

### BS-Roformer & Mel-Band Roformer
* **Repository:** [lucidrains/bs-roformer](https://github.com/lucidrains/bs-roformer) / [Anjok07/ultimatevocalremovergui](https://github.com/Anjok07/ultimatevocalremovergui)
* **Architecture:** Band-Split Rotary Position Embedding Transformer.
* **Performance:** Currently represents the state-of-the-art in vocal isolation on the Music Demixing Challenge (MDX) benchmarks (SDR > 12.5 dB).
* **Advantage for Indian Vocals:** Captures high-frequency harmonics of vocal tract resonances while preserving delicate transients in rapid *taans* and subtle ornament micro-glides.

### HT-Demucs v4
* **Repository:** [facebookresearch/demucs](https://github.com/facebookresearch/demucs)
* **Architecture:** Hybrid Transformer-Conformer Demucs operating in both temporal and spectral domains.
* **Role:** Ideal for extracting distinct accompaniment stems (drums/percussion stem for Tabla tala analysis; other stems for melodic accompaniment).

### Solving Classical Bleed: Drone & Percussion Leakage
1. **Tanpura Drone Suppression:** The tanpura creates dense, continuous spectral lines at $Sa_1$, $Sa_2$, and $Pa$ across octaves. An adaptive notch filter centered at the detected drone peaks removes stationary hum prior to vocal pitch extraction.
2. **Tabla Transients:** Fast tabla strokes (*Dha*, *Dhin*) introduce broad vertical energy spikes in spectrograms. Spectral masking filters these transient bursts using transient-steady-state separation before F0 analysis.

---

## 2. Continuous Fundamental Frequency ($F_0$) Extraction

```
           Frequency (Hz)
                ▲
                │      .-''''-.                 <--- Meend (continuous slide)
                │    .'        '.
                │   /            \
       Pa  ────┼───'              \             <--- Stationary plateau (Nyasa)
                │                  \
       Ga(k)───┼                    \   /\/\/\  <--- Andolan / Vibrato
                │                     \/
       Sa  ────┴────────────────────────────────► Time (s)
```

### CREPE & torchcrepe
* **Repository:** [marl/crepe](https://github.com/marl/crepe) & [maxrmorrison/torchcrepe](https://github.com/maxrmorrison/torchcrepe)
* **Architecture:** Deep convolutional neural network trained on synthetic and real vocal audio to output a pitch salience distribution over 360 cents-spaced bins.
* **Characteristics:** Extremely robust to noise and background harmonics; outputs both $F_0$ (in Hz) and instantaneous confidence score for voiced/unvoiced boundary detection.

### RMVPE (Robust Multiscale Vocal Pitch Estimation)
* **Repository:** [Dream-High/RMVPE](https://github.com/Dream-High/RMVPE)
* **Architecture:** Multi-scale feature extractor with bidirectional recurrent layers; widely adopted as the default pitch estimator in RVC.
* **Advantage:** Low latency, high computational speed, and superior stability when tracking rapid pitch bends and slides without octave-jumping errors.

### Spotify Basic Pitch
* **Repository:** [spotify/basic-pitch](https://github.com/spotify/basic-pitch)
* **Architecture:** Lightweight neural network for polyphonic and monophonic instrument/voice transcription.
* **Advantage:** Directly outputs note boundaries along with continuous frame-level pitch bend trajectories; ideal for generating notation and MIDI files.

### Pitch Extraction Tool Comparison Matrix

| Tool | Algorithm / Model | Latency | Pitch Jumps / Octave Errors | Microtonal Glide Accuracy |
|---|---|---|---|---|
| **torchcrepe** | Deep CNN (360 bins) | Medium (GPU recommended) | Very Low | Excellent (sub-cent precision) |
| **RMVPE** | Multiscale ConvNet | Very Fast (Real-time capable) | Lowest | Exceptional on rapid taans |
| **Basic Pitch** | Lightweight CNN | Fast | Low | High (outputs note-events + bends) |
| **pYIN (Librosa)** | Probabilistic YIN | Slow (CPU only) | Moderate | Moderate (smoothing can blunt kans) |

---

## 3. Tonal Normalization & 22-Shruti Microtonal Calibration

### Converting Hertz to Cents Relative to Tonic ($Sa$)
In Indian Classical Music, absolute frequency in Hertz is meaningless without the artist's chosen tonic ($Sa$). Every frequency $f$ (in Hz) is mapped to cents relative to $f_{Sa}$:

$$\text{Cents}(f) = 1200 \times \log_2\left(\frac{f}{f_{Sa}}\right)$$

Where:
* $\text{Cents} = 0$: Fundamental tonic ($Sa$, Madhya Saptak)
* $\text{Cents} = 702$: Pure Just Fifth ($Pa$)
* $\text{Cents} = 1200$: Taar Saptak Sa (Octave higher)
* Negative cents map into Mandra Saptak (Lower octave).

### Traditional 22-Shruti Mathematical Ratios vs. 12-TET

| Shruti Index | Swara Name | Bhatkhande Notation | Frequency Ratio ($f / f_{Sa}$) | Pure Cents (Just Intonation) | 12-TET Piano Cents | Deviation from Piano |
|---|---|---|---|---|---|---|
| **0** | **Shadja (Sa)** | **S** | $1/1$ | **0.0** | 0.0 | 0.0 |
| 1 | Tivratara Rishabh | r₁ | $256/243$ | 90.2 | 100.0 | -9.8 |
| **2** | **Komal Rishabh (Re)** | **r₂** | $16/15$ | **111.7** | 100.0 | +11.7 |
| 3 | Trishruti Rishabh | R₁ | $10/9$ | 182.4 | 200.0 | -17.6 |
| **4** | **Shuddha Rishabh (Re)** | **R₂** | $9/8$ | **203.9** | 200.0 | +3.9 |
| 5 | Tivratara Gandhar | g₁ | $32/27$ | 294.1 | 300.0 | -5.9 |
| **6** | **Komal Gandhar (Ga)** | **g₂** | $6/5$ | **315.6** | 300.0 | +15.6 |
| 7 | Shuddha Gandhar | G₁ | $5/4$ | 386.3 | 400.0 | -13.7 |
| **8** | **Tivra Gandhar (Ga)** | **G₂** | $81/64$ | **407.8** | 400.0 | +7.8 |
| **9** | **Shuddha Madhyam (Ma)**| **M₁** | $4/3$ | **498.0** | 500.0 | -2.0 |
| 10 | Ekashruti Madhyam | M₂ | $27/20$ | 519.5 | 500.0 | +19.5 |
| 11 | Tivra Madhyam | m₁ | $45/32$ | 590.2 | 600.0 | -9.8 |
| **12** | **Tivratara Madhyam (Ma)**| **m₂** | $729/512$ | **611.7** | 600.0 | +11.7 |
| **13** | **Pancham (Pa)** | **P** | $3/2$ | **702.0** | 700.0 | +2.0 |
| 14 | Tivratara Dhaivat | d₁ | $128/81$ | 792.2 | 800.0 | -7.8 |
| **15** | **Komal Dhaivat (Dha)** | **d₂** | $8/5$ | **813.7** | 800.0 | +13.7 |
| 16 | Trishruti Dhaivat | D₁ | $5/3$ | 884.4 | 900.0 | -15.6 |
| **17** | **Shuddha Dhaivat (Dha)**| **D₂** | $27/16$ | **905.9** | 900.0 | +5.9 |
| 18 | Tivratara Nishad | n₁ | $16/9$ | 996.1 | 1000.0 | -3.9 |
| **19** | **Komal Nishad (Ni)** | **n₂** | $9/5$ | **1017.6** | 1000.0 | +17.6 |
| 20 | Shuddha Nishad | N₁ | $15/8$ | 1088.3 | 1100.0 | -11.7 |
| **21** | **Tivra Nishad (Ni)** | **N₂** | $243/128$ | **1109.8** | 1100.0 | +9.8 |
| **22** | **Taar Shadja (Sa')** | **S'** | $2/1$ | **1200.0** | 1200.0 | 0.0 |

---

## 4. Algorithmic Feature Extraction for Ornaments

### Rule-Based Heuristic Classifiers
The pitch curve $C(t)$ in cents and energy envelope $E(t)$ in decibels are segmented into regions of interest:

```
                          Pitch Contour C(t)
                                  │
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
   Oscillatory Analysis                            Glide / Step Analysis
(Zero-crossings & FFT of dC/dt)                   (Duration & Magnitude ΔC)
          │                                               │
    ┌─────┴───────────────┐                         ┌─────┴───────────────────┐
    ▼                     ▼                         ▼                         ▼
Vibrato               Gamak & Andolan              Meend                     Kan (Grace)
(4–8 Hz,              (1–3 Hz, slow swing          (Monotonic slide,         (Duration < 80ms,
 ±30–100 cents)        or heavy RMS pulse)          span ≥ 2 swaras)          instant jump)
```

### Feature Detection Math
1. **First Derivative (Pitch Velocity):**
   $$v(t) = \frac{dC}{dt}$$
   Used to detect inflection points, slides, and note attack sharpness.
2. **Second Derivative (Pitch Acceleration):**
   $$a(t) = \frac{d^2C}{dt^2}$$
   Spikes in $a(t)$ indicate *khatka* (sharp jerks) and *murki* boundaries.
3. **Oscillation Rate & Depth:**
   Computed via sliding window autocorrelation or spectral peak of $C(t) - \text{trend}(C(t))$:
   * **Vibrato:** Rate $\in [4.5, 7.5]\text{ Hz}$, Depth $\in [30, 90]\text{ cents}$.
   * **Andolan:** Rate $\in [1.0, 3.0]\text{ Hz}$, Depth $\in [80, 220]\text{ cents}$ (e.g., oscillating komal Ga in Darbari or komal Dha in Bhairav).
   * **Gamak:** Rate $\in [2.5, 5.0]\text{ Hz}$ with synchronized periodic bursts in the loudness envelope $E(t)$.
4. **Meend Characterization:**
   * Monotonicity check: $\text{sign}(v(t))$ is constant over duration $\tau > 150\text{ ms}$.
   * Pitch distance: $|\Delta C| \ge 180\text{ cents}$.
   * Curve trajectory fitted with low-order polynomial or cubic spline.
5. **Kan (Sparsh Swara):**
   * Pre-onset or post-offset pitch transient with duration $\Delta t \in [20, 80]\text{ ms}$.
   * Rapid transition velocity $|v(t)| > 3500\text{ cents/s}$.

### Pakad Matching via Dynamic Time Warping (DTW)
Ragas are identified through characteristic phrases (*pakad* / *chalan*). Because performers sing phrases at different speeds and with personal ornaments, standard string matching fails.
* **Continuous Subsequence DTW:** Compares the normalized vocal pitch contour against indexed reference curves of canonical pakads stored in the Knowledge Base.
* **Distance Metric:** Microtonally weighted Euclidean distance with penalty relaxation for natural vibrato fluctuations.

---

## 5. Export & Transcription Formats

### Sargam Text Format with Diacritics
The system exports parsed melody in standardized Bhatkhande sargam notation:
* **Lower Octave (Mandra):** Dot below (e.g., $\text{Ṇ}$, $\text{Ḍ}$, $\text{P̣}$)
* **Middle Octave (Madhya):** Standard letter ($\text{S}$, $\text{R}$, $\text{G}$, $\text{M}$, $\text{P}$, $\text{D}$, $\text{N}$)
* **Upper Octave (Taar):** Dot above (e.g., $\text{Ṡ}$, $\text{Ṙ}$, $\text{Ġ}$)
* **Komal Swaras:** Underlined or lowercase (e.g., $\underline{\text{R}}$, $\underline{\text{G}}$ or $r$, $g$)
* **Tivra Madhyam:** Vertical tick above ($\text{M'}$ or $m$)
* **Meend Glide:** Arc or hyphen ($\text{P}\frown\text{G}$ or $\text{P-G}$)
* **Kan Grace Note:** Superscript ($^{\text{P}}\text{D}$)

### High-Resolution MIDI with 14-Bit Pitch Bend
Standard MIDI note-on/off events cannot convey meends or andolans. Song Lab formats exports with continuous 14-bit pitch bend messages:
* **Pitch Bend Range:** Configured to $\pm 12$ semitones ($\pm 1200$ cents) or $\pm 2$ semitones.
* **Frame Rate:** Pitch bend points sampled at 100 Hz (10 ms intervals).
* **Formula:**
  $$\text{PitchBendValue} = \text{clamp}\left(8192 + \frac{\Delta \text{Cents}}{\text{MaxRangeCents}} \times 8191, 0, 16383\right)$$
This enables DAWs (Logic Pro, Ableton, Cubase, FL Studio) to accurately play back authentic Indian classical ornamentation using modern MPE (MIDI Polyphonic Expression) synthesizers.

---

## 6. Cross-Link Navigation

* 📖 **[Master Documentation Hub](file:///d:/Music/INDEX.md)**: Main architecture and directory.
* 📋 **[Phase 2 Specification Plan](file:///d:/Music/plan.md)**: Design goals for ornament detection, raga intelligence, AI analyst.
* 🎶 **[Indian Classical MIR & Raga Intelligence](file:///d:/Music/indian_classical_mir_ecosystem.md)**: CompMusic, Saraga, compIAM, Essentia, and raga datasets.
* 🤖 **[Generative Music AI & Suno Compendium](file:///d:/Music/generative_music_ai.md)**: Suno, YuE, MusicGen, AudioCraft, and singing voice conversion.
