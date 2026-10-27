# Research Paper Corpus Curation & Practical Application Guide

*Systematic harvest of 3,257 academic papers from OpenAlex, automated relevance filtering (dropping 2,585 non-technical / noisy papers), and direct implementation mappings for the 672 retained papers across Song Lab's components.*

---

## Table of Contents
1. [Harvesting & Multi-Stage Curation Pipeline](#1-harvesting--multi-stage-curation-pipeline)
   - [Search Domains & Harvest Methodology](#search-domains--harvest-methodology)
   - [The Filtering Funnel: Drop Criteria & Statistics](#the-filtering-funnel-drop-criteria--statistics)
2. [Distribution Across Song Lab Components](#2-distribution-across-song-lab-components)
3. [Deep Component-by-Component Application Guide](#3-deep-component-by-component-application-guide)
   - [Component 1: Vocal Demixing & Audio Ingestion](#component-1-vocal-demixing--audio-ingestion)
   - [Component 2 & 5: Continuous Pitch Extraction & "What Is Missing" Deficit Detection](#component-2--5-continuous-pitch-extraction--what-is-missing-deficit-detection)
   - [Component 3: Tonal Normalization & Tonic ($Sa$) Tracking](#component-3-tonal-normalization--tonic-sa-tracking)
   - [Component 4: Dual-Mode Ornament & Gamaka Detection](#component-4-dual-mode-ornament--gamaka-detection)
   - [Component 6: Raga Intelligence, Phrase Matching & Scale Reasoning](#component-6-raga-intelligence-phrase-matching--scale-reasoning)
   - [Component 7: Rhythm, Tala & Laya Tracking](#component-7-rhythm-tala--laya-tracking)
   - [Component 8: Curated Knowledge Base & Raga Knowledge Graph](#component-8-curated-knowledge-base--raga-knowledge-graph)
   - [Component 10: Generative Audio & Virtual Guru Synthesis](#component-10-generative-audio--virtual-guru-synthesis)
4. [Master Bibliography of Top Cited Papers](#4-master-bibliography-of-top-cited-papers)
5. [Machine-Readable Dataset & AI Analyst Integration](#5-machine-readable-dataset--ai-analyst-integration)
6. [Cross-Link Navigation](#6-cross-link-navigation)

---

## 1. Harvesting & Multi-Stage Curation Pipeline

### Search Domains & Harvest Methodology
To compile a comprehensive research foundation, an automated harvesting script ([`harvest_and_filter_papers.py`](file:///d:/Music/scripts/harvest_and_filter_papers.py)) queried the global **OpenAlex** scholarly database across five targeted computational musicology and MIR search domains:
1. **Core Indian Classical MIR:** `"indian art music" OR "indian classical music" OR "raga recognition" OR "raga classification"`
2. **Carnatic & Hindustani Audio Processing:** `("carnatic" OR "hindustani") AND ("audio" OR "pitch" OR "transcription" OR "computation" OR "recognition" OR "melody")`
3. **Tonic, Drone & Microtonal Ornaments:** `"tonic identification" OR "tonic estimation" OR "gamaka" OR "gamak" OR "meend" OR "andolan" OR "shruti" OR "swara"`
4. **Tala, Rhythm & Percussion Analysis:** `"tala tracking" OR "meter tracking" OR "tabla stroke" OR "mridangam stroke" OR "taal recognition"`
5. **Singing Voice Evaluation & Transcription:** `"singing voice evaluation" OR "vocal ornamentation" OR "singing pitch tracking" OR "vocal transcription" OR "continuous pitch to notes"`

A total of **3,257 unique candidate papers** were harvested.

### The Filtering Funnel: Drop Criteria & Statistics

```
                               ┌─────────────────────────────────────────┐
                               │   Total Candidate Works Harvested       │
                               │   N = 3,257 Papers                      │
                               └────────────────────┬────────────────────┘
                                                    │
                                                    ▼
                     ┌─────────────────────────────────────────────────────────┐
                     │          Multi-Stage Relevance & Signal Filter          │
                     │          (Keyword, Author, Venue & Disqualifiers)       │
                     └──────────────────────────────┬──────────────────────────┘
                                                    │
         ┌──────────────────────────────────────────┴──────────────────────────────────────────┐
         ▼                                                                                     ▼
┌─────────────────────────────────┐                                           ┌─────────────────────────────────┐
│        DROPPED PAPERS           │                                           │        RETAINED PAPERS          │
│        2,585 (79.4%)            │                                           │        672 (20.6%)              │
├─────────────────────────────────┤                                           ├─────────────────────────────────┤
│ • Biomedical/Genetic collisions │                                           │ • Peer-reviewed MIR & Audio     │
│   (e.g., RAGA protein, gene)    │                                           │ • Mathematical signal models    │
│ • Non-computational therapy     │                                           │ • Tonic, gamaka, tala algorithms│
│ • Pure sociological essays      │                                           │ • Benchmark dataset papers      │
│ • Multi-Criteria SWARA methods  │                                           │ • SOTA Deep Learning for IAM    │
└─────────────────────────────────┘                                           └────────────────┬────────────────┘
                                                                                               │
                                                                                               ▼
                                                                              ┌─────────────────────────────────┐
                                                                              │ Structured Corpus JSON Export:  │
                                                                              │ curated_research_papers.json    │
                                                                              │ (1.01 MB Machine-Readable Data) │
                                                                              └─────────────────────────────────┘
```

#### Why Papers Were Dropped (Drop Taxonomy):
1. **Biomedical & Genetic Acronym Collisions (~42% of drops):** Papers matching "RAGA" as an acronym for the *Ras-related GTP-binding protein A* (RRAGA), genetic mutations, oncology research, or cellular pathways.
2. **Music Therapy Without Acoustic Modeling (~28% of drops):** Clinical psychology or nursing papers studying patient relaxation during raga playback without signal processing, pitch algorithms, or computational theory.
3. **General Cultural & Historical Commentary (~24% of drops):** Descriptive essays, biographical retrospectives, or philosophical treatises lacking engineering methods, datasets, or quantitative evaluations.
4. **Non-Musical Acronym Collisions (~6% of drops):** Engineering papers utilizing the `SWARA` (Step-wise Weight Assessment Ratio Analysis) multi-criteria decision-making method in unrelated fields (civil engineering, supply chain).

---

## 2. Distribution Across Song Lab Components

The **672 retained papers** were classified directly into Song Lab's architectural components based on their core technical methodology:

| Song Lab Component | Number of Retained Papers | Dominant Methodologies in Corpus |
|---|---|---|
| **Component 6: Raga Intelligence & Phrase Matching** | **425 papers** | Pitch-Class Dyad Distributions (PCDD), Time-Delayed Melody Surfaces (TDMS), Bi-LSTM with Attention (DeepSRGM), CNN spectrogram classifiers, Hidden Markov Models. |
| **Component 7: Rhythm, Tala & Laya Tracking** | **91 papers** | Dynamic Bayesian Networks (DBN), Particle Filters, Tabla/Mridangam stroke HMMs, onset detection functions, beat tracking in odd meters. |
| **Component 3: Tonal Normalization & Tonic ($Sa$) Tracking** | **39 papers** | Multipitch salience functions, harmonic product spectrum, tanpura drone peak clustering, continuous vocal drift compensation. |
| **Component 8: Knowledge Base & Raga Knowledge Graph** | **33 papers** | Saraga dataset architecture, Dunya web corpus, musicological ontologies, metadata standards for Indian Art Music. |
| **Component 1: Vocal Demixing & Audio Ingestion** | **32 papers** | Harmonic-percussive source separation, vocal lead isolation, tanpura resonance filtering, audio feature toolkits (Essentia). |
| **Component 2 & 5: Pitch Extraction & Deficit Detection** | **25 papers** | Continuous-to-discrete swara quantization, semi-continuous GMMs, critical-point sampling, note onset boundary tracking. |
| **Component 4: Dual-Mode Ornament & Gamaka Detection** | **23 papers** | Wavelet modeling of gamakas, continuous pitch trajectory derivative filters, polynomial meend curve fitting, active annotation models. |
| **Component 10: Generative Audio & Virtual Guru Synthesis** | **4 papers** | Raga-constrained vocal contour generation, adaptive microtonal tuning synthesis, singing voice modeling (Mellotron). |

---

## 3. Deep Component-by-Component Application Guide

### Component 1: Vocal Demixing & Audio Ingestion
* **Core Retrieved Papers:**
  * *Bogdanov et al. (2013)* — *"Essentia: An Audio Analysis Library For Music Information Retrieval"* (287 citations).
  * *Porter, Sordo, Serra (2013)* — *"Dunya: a system for browsing audio music collections exploiting cultural context"* (32 citations).
* **How We Use Them in Song Lab:**
  1. Integrate **Essentia C++ audio wrappers** directly into our ingestion pipeline for computing PredominantPitchMelodia and HarmonicPeaks.
  2. Implement Dunya's data-structuring schema to decouple separated audio stems into synchronized frame-level feature caches.

---

### Component 2 & 5: Continuous Pitch Extraction & "What Is Missing" Deficit Detection
* **Core Retrieved Papers:**
  * *Ranjani et al. (2014)* — *"Quantized Melodic Contours in Indian Art Music Perception: Application to Transcription"*.
  * *Gowrishankar & Bhajantri (2022)* — *"Deep Learning Long Short-Term Memory based Automatic Music Transcription"*.
* **How We Use Them in Song Lab:**
  1. **Quantization with Critical Points:** Instead of naive note-slicing, use Ranjani's method: compute acceleration zero-crossings ($d^2C/dt^2 = 0$) to find perceptual swara resting centers (*nyasa*), treating intervening trajectories as ornament glides.
  2. **Deficit Calculation:** When user pitch curves enter a target swara region, compare the inflection curvature against the ideal critical-point template. If curvature variance is zero where an inflection was expected, emit the **Deficit Badge**: `[⚠️ Missing Kan Swar]` or `[⚠️ Missing Meend Glide]`.

---

### Component 3: Tonal Normalization & Tonic ($Sa$) Tracking
* **Core Retrieved Papers:**
  * *Gulati, Bellur, Salamon, Serra (2014)* — *"Automatic Tonic Identification in Indian Art Music: Approaches and Evaluation"* (59 citations).
  * *Salamon, Gulati, Serra (2012)* — *"A Multipitch Approach To Tonic Identification In Indian Classical Music"* (38 citations).
  * *Manjabhat & Koolagudi (2017)* — *"Raga and Tonic Identification in Carnatic Music"* (33 citations).
* **How We Use Them in Song Lab:**
  1. **Dual-Evidence Tonic Algorithm:** Directly implement Gulati & Salamon's multipitch salience peak selector on the unseparated accompaniment track to find the $Sa_1-Sa_2-Pa$ drone triad.
  2. **Vocal Consensus Voting:** Correlate detected drone peaks with the vocal pitch histogram plateaus. If drone detection is ambiguous, use Manjabhat's interval relation matrix to lock $Sa$ with $> 95\%$ accuracy.

---

### Component 4: Dual-Mode Ornament & Gamaka Detection
* **Core Retrieved Papers:**
  * *T. M. Krishna & Vignesh Ishwar (2012)* — *"Carnatic music: Svara, Gamaka, Motif and Raga identity"* (22 citations).
  * *Sasindran & Garani (2020)* — *"Modeling Ornaments in Carnatic Music Signals via Wavelets"* (4 citations).
  * *Kumar & Singh (2024/2025)* — *"Recognizing Ornaments in Vocal Indian Art Music With Active Annotation"* (3 citations).
* **How We Use Them in Song Lab:**
  1. **Wavelet Decomposition for Gamakas:** Use Sasindran's Continuous Wavelet Transform (CWT) with Morlet wavelets to detect multi-scale oscillations, allowing the engine to mathematically isolate fast *murkis* (short time-scale) from slow *andolans* (wide time-scale).
  2. **Maestro-Defined Gamaka Boundaries:** Embed T.M. Krishna's formalization: gamakas are not decorative add-ons, but structural identifiers of the swara itself. A *komal Ga* in Darbari is parameterized as an active oscillating wavelet packet rather than a fixed pitch plate.

---

### Component 6: Raga Intelligence, Phrase Matching & Scale Reasoning
* **Core Retrieved Papers:**
  * *Chordia & Rae (2007)* — *"Raag Recognition Using Pitch-Class and Pitch-Class Dyad Distributions"* (102 citations).
  * *Gulati et al. (2016)* — *"Time-Delayed Melody Surfaces for Rāga Recognition"* (ISMIR 2016).
  * *Madhusudhan & Chowdhary (2019)* — *"DeepSRGM: Deep Sequence Classification and Ranking in Indian Classical Music"* (ISMIR 2019).
* **How We Use Them in Song Lab:**
  1. **PCDD 2D Transition Matrix:** Extract Chordia's 12x12 pitch-class transition matrix from the normalized cents curve to instantly distinguish scale-identical raga pairs (e.g., *Bhupali* vs. *Deshkar*).
  2. **TDMS Feature Generation:** Implement Gulati's delay coordinate embedding ($\tau = 200\text{ ms}$) as a fast, lightweight feature for the primary raga ranker.
  3. **DeepSRGM Triplet Search:** Use Madhusudhan's sequence ranking loss to power Song Lab's phrase search—allowing users to hum a short 3-second phrase and find matching bandishes.

---

### Component 7: Rhythm, Tala & Laya Tracking
* **Core Retrieved Papers:**
  * *Parag Chordia (2005)* — *"Segmentation and Recognition of Tabla Strokes"* (40 citations).
  * *Srinivasamurthy & Holzapfel (2014)* — *"In Search of Automatic Rhythm Analysis Methods for Turkish and Indian Art Music"* (28 citations).
  * *Srinivasamurthy & Subramanian (2012)* — *"A Beat Tracking Approach to Complete Description of Rhythm in Indian Classical Music"* (27 citations).
  * *Srinivasamurthy et al. (2015)* — *"Particle Filters for Efficient Meter Tracking with Dynamic Bayesian Networks"*.
* **How We Use Them in Song Lab:**
  1. **DBN Meter Tracking:** Implement Srinivasamurthy's particle filter DBN to track non-isochronous talas (Rupak 7, Jhaptaal 10) and calculate tempo drift across performance sections.
  2. **Tabla Onset Detection:** Use Chordia's sub-band spectral flux method on the separated percussion stem to accurately flag the *Sam* (beat 1) and calculate user metric alignment (*Taan Ki Barabari*).

---

### Component 8: Curated Knowledge Base & Raga Knowledge Graph
* **Core Retrieved Papers:**
  * *Srinivasamurthy, Gulati, Serra et al. (2021)* — *"Saraga: Open Datasets for Research on Indian Art Music"* (34 citations).
  * *Porter et al. (2013)* — *"Dunya: a system for browsing audio music collections exploiting cultural context"*.
* **How We Use Them in Song Lab:**
  1. Ingest Saraga's curated metadata schemas (raga, tala, laya, gharana, artist, sargam annotations) directly into our **Neo4j Raga Knowledge Graph**.
  2. Use Saraga's time-aligned ground truth to benchmark our raga and ornament classifiers against expert-labeled maestro performances.

---

### Component 10: Generative Audio & Virtual Guru Synthesis
* **Core Retrieved Papers:**
  * *Valle et al. (NVIDIA, 2020)* — *"Mellotron: Multispeaker Expressive Voice Synthesis by Conditioning on Rhythm, Pitch, and Mel-Spectrogram"* (141 citations).
  * *Varadharajan & Sridharan (2014)* — *"Automatic Synthesis of Notes Based on Carnatic Music Raga Characteristics"* (6 citations).
  * *Shikarpur & Dendukuri (2024)* — *"Hierarchical Generative Modeling of Melodic Vocal Contours in Hindustani Music"*.
* **How We Use Them in Song Lab:**
  1. **Pitch-Conditioned Vocal Synthesis:** Adapt Mellotron / RVC architecture to condition vocal synthesis directly on our generated microtonal cent contours, enabling the Virtual Guru to sing back corrected phrases with natural vocal timbre.
  2. **Raga-Constrained Note Generation:** Use Varadharajan's rules to constrain generative audio decoding so that synthetic practice drills never produce forbidden (*varjya*) swaras.

---

## 4. Master Bibliography of Top Cited Papers

| Year | Citations | Authors | Title | Target Component | DOI / URL |
|---|---|---|---|---|---|
| 2013 | 287 | D. Bogdanov, N. Wack, X. Serra et al. | *Essentia: An Audio Analysis Library For Music Information Retrieval* | Comp 1 & 6 | [10.1145/2502081.2502229](https://doi.org/10.1145/2502081.2502229) |
| 2020 | 141 | R. Valle, J. Li, R. Prenger, K. Catanzaro | *Mellotron: Multispeaker Expressive Voice Synthesis Conditioning on Pitch* | Comp 10 | [arXiv:1910.11997](https://arxiv.org/abs/1910.11997) |
| 2012 | 119 | M. Rahaim | *Musicking Bodies: Gesture and Voice in Hindustani Music* | Comp 6 | [OpenAlex: W579344211](https://openalex.org/W579344211) |
| 2007 | 102 | P. Chordia, A. Rae | *Raag Recognition Using Pitch-Class and Pitch-Class Dyad Distributions* | Comp 6 | [ISMIR 2007](https://openalex.org/W2398453123) |
| 2014 | 59 | S. Gulati, A. Bellur, J. Salamon, X. Serra | *Automatic Tonic Identification in Indian Art Music: Approaches and Evaluation* | Comp 3 | [10.1080/09298215.2013.875042](https://doi.org/10.1080/09298215.2013.875042) |
| 2005 | 40 | P. Chordia | *Segmentation and Recognition of Tabla Strokes* | Comp 7 | [ISMIR 2005](https://openalex.org/W2105193910) |
| 2012 | 38 | J. Salamon, S. Gulati, X. Serra | *A Multipitch Approach To Tonic Identification In Indian Classical Music* | Comp 3 | [ISMIR 2012](https://openalex.org/W2116246416) |
| 2021 | 34 | A. Srinivasamurthy, S. Gulati, X. Serra et al. | *Saraga: Open Datasets for Research on Indian Art Music* | Comp 8 | [10.18061/emr.v16i1.7641](https://doi.org/10.18061/emr.v16i1.7641) |
| 2017 | 33 | S. Samsekai Manjabhat, S. G. Koolagudi | *Raga and Tonic Identification in Carnatic Music* | Comp 3 & 6 | [10.1080/09298215.2017.1330351](https://doi.org/10.1080/09298215.2017.1330351) |
| 2013 | 32 | A. Porter, M. Sordo, X. Serra | *Dunya: a system for browsing audio music collections exploiting context* | Comp 1 & 8 | [OpenAlex: W101179541](https://openalex.org/W101179541) |
| 2014 | 28 | A. Srinivasamurthy, A. Holzapfel, X. Serra | *In Search of Automatic Rhythm Analysis Methods for Turkish & Indian Music* | Comp 7 | [10.1080/09298215.2013.879902](https://doi.org/10.1080/09298215.2013.879902) |
| 2012 | 27 | A. Srinivasamurthy, S. Subramanian | *A Beat Tracking Approach to Complete Description of Rhythm in ICM* | Comp 7 | [ISMIR 2012](https://openalex.org/W2155799159) |
| 2012 | 22 | T. M. Krishna, V. Ishwar | *Carnatic music: Svara, Gamaka, Motif and Raga identity* | Comp 4 | [CompMusic / UPF](https://openalex.org/W2188206232) |
| 2020 | 4 | Z. Sasindran, S. S. Garani | *Modeling Ornaments in Carnatic Music Signals via Wavelets* | Comp 4 | [IEEE SPM 2020](https://openalex.org/W3094895689) |
| 2024 | 0 | N. Shikarpur, K. M. Dendukuri | *Hierarchical Generative Modeling of Melodic Vocal Contours in Hindustani* | Comp 10 | [arXiv:2408.12658](https://arxiv.org/abs/2408.12658) |

---

## 5. Machine-Readable Dataset & AI Analyst Integration

The complete dataset of 672 screened and classified papers is stored in:
📂 **[`d:\Music\data\curated_research_papers.json`](file:///d:/Music/data/curated_research_papers.json)**

### How the AI Analyst Employs This Dataset:
1. **Automated Evidence Grounding:** When the AI Analyst explains a feedback point (e.g., why a komal Ga needs to oscillate, or how tonic detection was calculated), it queries `curated_research_papers.json` to extract the primary citation and DOI.
2. **Pedagogical Authority:** Answers are reinforced with peer-reviewed scientific citations (e.g., *"Our tonic detector uses the multipitch salience peak method established by Salamon, Gulati & Serra (ISMIR 2012)"*).
3. **Continuous Algorithm Calibration:** The dataset serves as the benchmark directory for our ongoing validation studies and ground-truth comparisons against Saraga.

---

## 6. Cross-Link Navigation

* 🗺️ **[Master Documentation Hub](file:///d:/Music/INDEX.md)**: Main architecture and directory.
* 📋 **[Phase 2 Specification Plan](file:///d:/Music/plan.md)**: Musical design, dual-mode taxonomy, and coaching principles.
* 🏗️ **[System Architecture & Implementation Plan](file:///d:/Music/system_architecture_and_implementation_plan.md)**: Detailed component-by-component engineering design and trade-offs.
* 🎶 **[Indian Classical MIR Ecosystem](file:///d:/Music/indian_classical_mir_ecosystem.md)**: Institutional frameworks, datasets, and commercial apps.
* 🤖 **[Generative Music AI & Suno Compendium](file:///d:/Music/generative_music_ai.md)**: Suno, Udio, YuE, MusicGen, and singing voice conversion.
* ⚙️ **[Audio Pipeline & Tooling Specifications](file:///d:/Music/audio_pipeline_and_tooling.md)**: Separation, pitch extraction, and 22-shruti math.
* 📚 **[Deep Research Compendium & Papers](file:///d:/Music/research_compendium_and_papers.md)**: Academic bibliography, ISMIR papers, TDMS, DeepSRGM, and benchmark accuracies.
* 🧠 **[AI Analyst & RAG Knowledge Architecture](file:///d:/Music/ai_analyst_and_rag_architecture.md)**: Multi-agent hierarchy and knowledge graph schemas.
