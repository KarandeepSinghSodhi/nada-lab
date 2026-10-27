# Deep Research Compendium: Papers, Algorithms & Benchmarks in Indian Art Music MIR

*Authoritative academic bibliography, mathematical algorithms, benchmark datasets, and comparative performance metrics across Hindustani and Carnatic computational musicology.*

---

## Table of Contents
1. [Milestone Academic Papers & Algorithmic Evolutions](#1-milestone-academic-papers--algorithmic-evolutions)
   - [Pitch-Class Distributions & Dyads (PCD / PCDD)](#pitch-class-distributions--dyads-pcd--pcdd)
   - [Time-Delayed Melody Surfaces (TDMS)](#time-delayed-melody-surfaces-tdms)
   - [DeepSRGM: Deep Sequence Classification & Ranking](#deepsrgm-deep-sequence-classification--ranking)
   - [Tonic ($Sa$) Estimation via Multipitch Salience](#tonic-sa-estimation-via-multipitch-salience)
   - [Tala & Metrical Cycle Tracking with Dynamic Bayesian Networks](#tala--metrical-cycle-tracking-with-dynamic-bayesian-networks)
   - [Continuous-to-Discrete Swara Quantization](#continuous-to-discrete-swara-quantization)
   - [Gharana & Stylistic Lineage Classification](#gharana--stylistic-lineage-classification)
2. [Comparative Performance Benchmark Table](#2-comparative-performance-benchmark-table)
3. [Empirical Shruti Science: What Masters Actually Sing](#3-empirical-shruti-science-what-masters-actually-sing)
4. [Cross-Link Navigation](#4-cross-link-navigation)

---

## 1. Milestone Academic Papers & Algorithmic Evolutions

### Pitch-Class Distributions & Dyads (PCD / PCDD)
* **Seminal Paper:** Chordia, P., & Rae, A. (2007). *"Raag Recognition Using Pitch-Class and Pitch-Class Dyad Distributions."* In *Proceedings of the 8th International Conference on Music Information Retrieval (ISMIR 2007)*, Vienna, Austria.
* **Core Theory:**
  * **Pitch-Class Distributions (PCDs):** Measure the continuous time spent on each pitch class relative to the tonic $Sa$, collapsed into a single octave (0 to 1200 cents). While a PCD reveals the scale, it cannot distinguish between ragas with identical notes (e.g., Bhupali vs. Deshkar, or Marwa vs. Puriya).
  * **Pitch-Class Dyad Distributions (PCDDs):** Construct a first-order transition matrix (2D histogram) tracking transitions from pitch class $i$ to pitch class $j$:
    $$P(j \mid i) = \frac{\text{Transitions}(i \rightarrow j)}{\sum_k \text{Transitions}(i \rightarrow k)}$$
    This directly models *aroha* (ascending) vs. *avaroha* (descending) tendencies and preferred swara couplings (e.g., $Re \rightarrow Pa$ in Yaman).
* **Classifier:** Support Vector Machines (SVM) with radial basis function (RBF) kernels and Random Forests.

### Time-Delayed Melody Surfaces (TDMS)
* **Seminal Paper:** Gulati, S., Serrà, J., Ganguli, K. K., Şentürk, S., & Serra, X. (2016). *"Time-Delayed Melody Surfaces for Rāga Recognition."* In *Proceedings of the 17th International Society for Music Information Retrieval Conference (ISMIR 2016)*, New York, USA.
* **Core Theory:**
  * Uses non-linear time-series analysis (Takens' Delay Embedding Theorem). Given an extracted continuous fundamental frequency trajectory $f_0(t)$, a delay coordinate vector is constructed:
    $$\vec{x}(t) = [f_0(t), f_0(t - \tau)]$$
    Where $\tau$ is a characteristic delay parameter (typically 100 ms to 300 ms).
  * A 2D joint probability density surface is formed over the continuous pitch plane. This preserves microtonal inflection shapes, meend velocity, and turn geometry without explicit note segmentation.
* **Performance:** Achieved ~98% classification accuracy on a 30-raga Hindustani dataset and ~87% on a Carnatic dataset using a simple $k$-Nearest Neighbors ($k$-NN) classifier with Wasserstein metric distance.

### DeepSRGM: Deep Sequence Classification & Ranking
* **Seminal Paper:** Madhusudhan, S. T., & Chowdhary, G. (2019/2024). *"DeepSRGM: Deep Sequence Classification and Ranking in Indian Classical Music with Deep Learning."* arXiv:2402.10168.
* **Core Theory:**
  * Reconceptualizes raga analysis as a hierarchical sequence task analogous to natural language processing.
  * Continuous pitch contours are segmented into atomic ornament tokens (gamaka sequences, steady notes, and transitions).
  * Employs bidirectional Long Short-Term Memory (Bi-LSTM) networks augmented with an **Additive Attention Mechanism** that automatically learns to attend to signature *pakad* phrases while ignoring generic scalar fills.
  * **Sequence Ranking with Triplet Margin Loss:** Enables phrase search—users can hum or sing an ornament, and DeepSRGM queries a database to retrieve the closest matching classical bandishes.

### Tonic ($Sa$) Estimation via Multipitch Salience
* **Seminal Paper:** Salamon, J., Gulati, S., & Serra, X. (2012). *"A Multipitch Approach to Tonic Identification in Indian Classical Music."* In *Proceedings of the 13th International Society for Music Information Retrieval Conference (ISMIR 2012)*, Porto, Portugal.
* **Algorithm Implemented in:** Essentia `TonicIndianArtMusic`.
* **Core Mechanism:**
  1. Computes a multi-pitch continuous salience function over the audio mix.
  2. Detects stable, stationary harmonic peaks generated by the acoustic tanpura drone (which continuously sounds $Sa_1$, $Sa_2$, and $Pa$ or $Ma$).
  3. Correlates candidate drone peaks against the vocal pitch histogram to resolve fifth-octave ambiguities ($Sa$ vs. $Pa$).
* **Accuracy:** > 95% on clean classical concert recordings.

### Tala & Metrical Cycle Tracking with Dynamic Bayesian Networks
* **Seminal Papers:**
  * Srinivasamurthy, A., Holzapfel, A., Cemgil, A. T., & Serra, X. (2015). *"Particle Filters for Efficient Meter Tracking with Dynamic Bayesian Networks."* In *ISMIR 2015*.
  * Srinivasamurthy, A., & Serra, X. (2014). *"A Hierarchical Bayesian Approach to Tala Tracking in Indian Classical Music."* In *IEEE ICASSP 2014*.
* **Core Mechanism:**
  * Models rhythm hierarchically: Position inside beat ($\phi$) $\rightarrow$ Beat index inside cycle ($b$) $\rightarrow$ Instantaneous tempo ($\omega$).
  * Uses a Dynamic Bayesian Network (DBN) solved via sequential Monte Carlo (Particle Filtering) to track tempo drift and identify the *sam* (downbeat, beat 1) even across unmetered tempo transitions (e.g., accelerating from vilambit to drut).

### Continuous-to-Discrete Swara Quantization
* **Seminal Paper:** Ranjani, H. G., et al. (2014). *"Quantized Melodic Contours in Indian Art Music Perception: Application to Transcription."* In *Proceedings of ISMIR 2014*.
* **Problem Solved:** Because Indian vocalists rarely sing discrete static steps, standard note onset detectors produce unreadable fragmented scores.
* **Solution:** Identifies **critical points** (extrema in pitch acceleration $d^2C/dt^2$ and minimum pitch velocity $dC/dt \approx 0$) as perceptual anchor points (*nyasa*), categorizing connecting contours into functional ornament envelopes (meend arcs, andolan oscillations).

### Gharana & Stylistic Lineage Classification
* **Seminal Paper:** Gowriprasad, R., et al. (2021). *"Tabla Gharānā Recognition from Audio Music Recordings of Tabla Solo Performances."* In *ISMIR 2021*.
* **Finding:** While vocal gharanas share identical raga scales, they differ systematically in pitch transition velocity and time allocation. Percussion gharanas (Delhi, Banaras, Punjab, Farrukhabad) can be classified with high fidelity (> 84%) using HMM stroke sequence recognizers that identify signature *qaidas* and characteristic *bol* combinations.

---

## 2. Comparative Performance Benchmark Table

| System / Paper | Target Task | Primary Dataset | Feature Representation | Model Architecture | Reported Accuracy |
|---|---|---|---|---|---|
| **Chordia & Rae (2007)** | Raga Recognition (Hindustani) | Curated archive (20 ragas, 67 artists) | PCD + PCDD (12 pitch classes) | SVM (RBF Kernel) | ~75.4% |
| **Salamon et al. (2012)** | Tonic ($Sa$) Identification | CompMusic IAM Tonic Corpus (HMD/CMD) | Multipitch salience + Drone peaks | Peak clustering heuristic | **95.2%** |
| **Gulati et al. (2016)** | Raga Recognition | CompMusic Corpus (30 Hindustani, 40 Carnatic) | Time-Delayed Melody Surfaces (TDMS) | $k$-NN (Wasserstein metric) | **97.8% (Hind.) / 87.2% (Carn.)** |
| **Madhusudhan et al. (2019)** | Raga Recognition & Ranking | Saraga & CompMusic | Discrete gamaka-token sequences | Bi-LSTM + Attention | **89.6%** (ranking Top-5: 96%) |
| **Srinivasamurthy (2015)** | Tala & Sam Tracking | CompMusic Carnatic & Hindustani Rhythm | Percussive onset energy curves | DBN + Particle Filter | **88.4% (Sam hit rate within ±100ms)** |
| **Gowriprasad et al. (2021)** | Tabla Gharana Classification | Solo Tabla Corpus (5 Gharanas) | Stroke onset transcription & n-grams | Hidden Markov Models (HMM) | **84.3%** |

---

## 3. Empirical Shruti Science: What Masters Actually Sing

A critical discovery of Indian musicology research (AUTRIM, NCPA, and IIT Bombay studies) is that **the 22 Shrutis are not 22 rigid mathematical frequencies**.

```
                Density
                   ▲               Pure Just Ratio (315.6 cents)
                   │                       │
                   │                     ┌─┴─┐
                   │                    /     \      <--- Attraction Basin (Width ~25 cents)
                   │                   /       \
                   │      . - - - - - '         ` - - - - .
                   └─────┴─────────────────────────────────┴──────► Pitch (Cents)
                        300                               330
                      12-TET                             Darbari
                    (Flat 3rd)                        (Oscillating Ga)
```

1. **Attraction Basins, Not Rigid Lines:**
   * Research shows that swaras in performance behave as **attraction basins** with an intonational dispersion of $\pm 10$ to $\pm 18$ cents around the pure ratio.
2. **Context-Dependent Intonation:**
   * *Komal Ga* ($g$) in **Raga Todi** sits markedly lower (approx. 290–295 cents) than *Komal Ga* in **Raga Kafi** (approx. 315–320 cents).
   * In **Raga Darbari Kanada**, *Komal Ga* cannot be sung as a stationary plate; it exists almost exclusively as a slow, wide oscillation (*andolan*) swinging between 285 and 325 cents. An algorithm that marks it "flat" or "sharp" demonstrates cultural ignorance.
3. **Global Tonic Drift:**
   * Long concert recordings show that even senior maestros drift up or down by 15–35 cents over 45 minutes as vocal cords warm up. Song Lab's tonal engine must incorporate **adaptive continuous tonic tracking** to maintain microtonal calibration.

---

## 4. Cross-Link Navigation

* 📖 **[Master Documentation Hub](file:///d:/Music/INDEX.md)**: Main architecture and directory.
* 📋 **[Phase 2 Specification Plan](file:///d:/Music/plan.md)**: Core design goals and coaching roadmap.
* 🎶 **[Indian Classical MIR Ecosystem](file:///d:/Music/indian_classical_mir_ecosystem.md)**: CompMusic, Saraga, compIAM, Essentia, and commercial apps.
* 🤖 **[Generative Music AI & Suno](file:///d:/Music/generative_music_ai.md)**: Suno, Udio, YuE, MusicGen, and voice conversion.
* ⚙️ **[Audio Engineering & Signal Pipeline](file:///d:/Music/audio_pipeline_and_tooling.md)**: Separation, pitch extraction, and 22-shruti math.
* 🧠 **[AI Analyst & RAG Architecture](file:///d:/Music/ai_analyst_and_rag_architecture.md)**: Multi-agent design, knowledge graphs, and hallucination guardrails.
