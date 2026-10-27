# Indian Classical Music Information Retrieval (MIR) & Raga Intelligence Ecosystem

*Comprehensive research compendium, open-source repositories, Kaggle datasets, academic frameworks, and commercial applications.*

---

## Table of Contents
1. [Core Institutional & Research Frameworks](#1-core-institutional--research-frameworks)
   - [CompMusic & Music Technology Group (MTG)](#compmusic--music-technology-group-mtg)
   - [compIAM: Common Tools for Indian Art Music](#compiam-common-tools-for-indian-art-music)
   - [AUTRIM (NCPA & University of Amsterdam)](#autrim-ncpa--university-of-amsterdam)
   - [IIT Bombay Digital Audio Processing Lab](#iit-bombay-digital-audio-processing-lab)
2. [Open-Source GitHub Repositories](#2-open-source-github-repositories)
   - [Tonic (Sa) Detection & Intonation](#tonic-sa-detection--intonation)
   - [Raga Recognition & Classification](#raga-recognition--classification)
   - [Gamaka & Ornament Modeling](#gamaka--ornament-modeling)
   - [Tala, Laya & Percussion Transcription](#tala-laya--percussion-transcription)
3. [Kaggle Datasets & Open Benchmarks](#3-kaggle-datasets--open-benchmarks)
4. [Commercial Products, Apps & Digital Portals](#4-commercial-products-apps--digital-portals)
   - [Riyaz (MusicMuni Labs)](#riyaz-musicmuni-labs)
   - [Swar Systems (SwarShala, SwarPlug, iShala)](#swar-systems-swarshala-swarplug-ishala)
   - [Sur Sadhana (Shankar Mahadevan Academy)](#sur-sadhana-shankar-mahadevan-academy)
   - [Virtual Accompaniments & Tanpura Hardware](#virtual-accompaniments--tanpura-hardware)
   - [Curated Theory Portals & Bandish Archives](#curated-theory-portals--bandish-archives)
5. [Cross-Link Navigation](#5-cross-link-navigation)

---

## 1. Core Institutional & Research Frameworks

### CompMusic & Music Technology Group (MTG)
* **Institution:** Universitat Pompeu Fabra (UPF), Barcelona, Spain. Led by Prof. Xavier Serra.
* **Overview:** CompMusic (Computational Models for the Discovery of the World's Music Traditions) was an ERC-funded research initiative that laid the modern computational groundwork for Indian Art Music (IAM), both Hindustani and Carnatic traditions.
* **Key Artifacts:**
  * **Saraga Dataset:** The canonical research dataset for Indian Classical Music. Contains multitrack audio, pitch contours, tonic annotations, time-aligned sargam transcriptions, tala cycles, and structural section annotations.
    * Hindustani Collection: 108 hours of classical recordings across diverse gharanas and ragas.
    * Carnatic Collection: 168 hours of concerts with vocal, violin, and mridangam stems.
    * Documentation & Portal: [mtg.github.io/saraga](https://mtg.github.io/saraga/)
    * GitHub: [MTG/saraga](https://github.com/MTG/saraga)
  * **Dunya Platform:** Web-based corpus exploration engine organizing Indian music recordings with aligned score, pitch, and metadata: [dunya.compmusic.upf.edu](https://dunya.compmusic.upf.edu/).

### compIAM: Common Tools for Indian Art Music
* **Repository:** [MTG/compIAM](https://github.com/MTG/compIAM)
* **What it provides:** A modular Python library specifically engineered for MIR research in Hindustani and Carnatic music:
  * **Tonic Identification:** Implementations of multi-pitch salience and tanpura drone detection algorithms.
  * **Predominant Pitch Extraction:** Specialized continuous F0 estimators calibrated for modal singing with microtonal glides.
  * **Rhythm & Tala:** Metrical cycle segmentation, downbeat (*sam*) detection, and stroke onset tracking.
  * **Dataset Loaders:** Unified API wrappers for Saraga, Dunya, and Carnatic Varnam corpora.

### AUTRIM (NCPA & University of Amsterdam)
* **Institution:** National Centre for the Performing Arts (NCPA), Mumbai & University of Amsterdam (UvA). Founded under Dr. J.J. Bhabha, led by Dr. Suvarnalata Rao and Dr. Wim van der Meer.
* **Overview:** AUTRIM (Automated Transcription for Indian Music) addresses the fundamental inadequacy of Western 5-line staff notation for Indian music by developing continuous 2D melodic curve representations (pitch over time on a microtonal grid).
* **Significance for Song Lab:**
  * Created the *Music in Motion* archive, demonstrating how raga identity resides not in discrete notes, but in continuous pitch trajectories, transitions, and ornament envelopes.
  * Established standard notation and visual rendering practices for Hindustani raga ornamentation using Praat acoustic scripting.

### IIT Bombay Digital Audio Processing Lab
* **Institution:** Department of Electrical Engineering, IIT Bombay. Led by Prof. Preeti Rao.
* **Focus Areas:**
  * Microtonal intonation analysis of *swaras* across different gharana traditions.
  * Characterization of *meend* (continuous slides) using polynomial and bezier curve fitting.
  * Automatic transcription of vocal raga performances into sargam notation.
  * Parametric voice modeling: [SubramaniKrishna/HpRNet](https://github.com/SubramaniKrishna/HpRNet) (harmonic plus residual modeling for Indian instruments and vocals).

---

## 2. Open-Source GitHub Repositories

### Tonic (Sa) Detection & Intonation
Accurate tonic detection is the non-negotiable foundation of modal music information retrieval:

| Repository / Module | Description & Architecture | Link |
|---|---|---|
| **Essentia `TonicIndianArtMusic`** | C++/Python implementation of the multipitch salience approach (Salamon, Gulati, Serra, ISMIR 2012). Detects drone peaks and singer pitch histograms. | [Essentia Docs](https://essentia.upf.edu/reference/std_TonicIndianArtMusic.html) |
| **`hari2897/shruti-monitor`** | Browser-based real-time pitch tracker for Indian Classical Music using 22-Shruti Just Intonation mathematical ratios rather than 12-TET equal temperament. Built-in shruti box. | [GitHub](https://github.com/hari2897/shruti-monitor) |
| **`rajarshi51382/microtonal-carnatic`** | Microtonal pitch extraction and state-space ornament modeling engine preserving microtonal deviations and raga grammar. | [GitHub](https://github.com/rajarshi51382/microtonal-carnatic) |

### Raga Recognition & Classification

| Repository | Approach & Model Architecture | Link |
|---|---|---|
| **`sohamm20/raag-identifier`** | Production-ready Hindustani raag classifier. Constant-Q Transform (CQT) feature extraction, Voice Activity Detection (VAD), and multi-architecture models (CNN, ResNet, CRNN). | [GitHub](https://github.com/sohamm20/raag-identifier) |
| **`ParampreetSingh97/PIM_v1_ExAI`** | Explainable AI framework for Raga Identification. Uses CNN-LSTM over combined pitch distribution and MFCC features to output interpretable phrase decisions. | [GitHub](https://github.com/ParampreetSingh97/PIM_v1_ExAI) |
| **`SuryaMajumder/Thaat-Raga-Identification`** | Two-tier hierarchical classification system: first classifies parent Thaat, then recognizes specific Ragas using Mel-spectrograms and chromagram representations. | [GitHub](https://github.com/SuryaMajumder/Thaat-Raga-Identification) |
| **`GaneshTS06/Raga-Classifier`** | Signal-processing-driven classifier. Uses DFT, Fisher-Jenks Natural Breaks Optimization to cluster swara frequencies, and relative interval ratio matching. | [GitHub](https://github.com/GaneshTS06/Raga-Classifier) |
| **`shubhlohiya/automatic-raga-reference`** | Deep learning reference models (implementing DeepSRGM architecture) for continuous sequence raga recognition. | [GitHub](https://github.com/shubhlohiya/automatic-raga-reference) |
| **`parakalan/RagaRecognition`** | Vector-space modeling using Time-Delayed Melody Surfaces (TDMS) for Carnatic raga recognition. | [GitHub](https://github.com/parakalan/RagaRecognition) |
| **`sruthiv98/RagaClassifier`** | Comparative audio analysis tool isolating characteristic interval transitions across Hindustani and Carnatic ragas. | [GitHub](https://github.com/sruthiv98/RagaClassifier) |

### Gamaka & Ornament Modeling

| Repository | Specialty | Link |
|---|---|---|
| **`naturalstupid/PyCarnatic`** | Python Carnatic music synthesis and tutor package supporting gamaka notation syntax: oscillations (`~`), glides (`/`, `\`), and microtonal adjustments. | [GitHub](https://github.com/naturalstupid/PyCarnatic) |
| **`MTG/compIAM` Melodic Module** | Continuous pitch trajectory segmenter that isolates transient transitions (meend, soot) from stationary pitch plates (nyasa swaras). | [GitHub](https://github.com/MTG/compIAM) |

### Tala, Laya & Percussion Transcription

| Repository | Focus & Architecture | Link |
|---|---|---|
| **`guruprasanth02/Mridangam-stroke-detection`** | CNN classifier predicting Carnatic mridangam strokes (*Tha, Dhi, Thom, Nam, Chapu*) from live or recorded audio. | [GitHub](https://github.com/guruprasanth02/Mridangam-stroke-detection) |
| **`pranav6670/Detection-Classification-of-Tabla-taals`** | Three-stage pipeline: Source separation (vocal vs. percussion) $\rightarrow$ onset detection $\rightarrow$ CNN-LSTM classification of Hindustani tals (Teentaal, Keherwa, Dadra, Jhaptal). | [GitHub](https://github.com/pranav6670/Detection-Classification-of-Tabla-taals) |
| **`madhavlab/2025_drumtrans_rkodag`** | Meta-learning-based percussion transcription and tala tracking on low-resource rhythmic audio datasets. | [GitHub](https://github.com/madhavlab/2025_drumtrans_rkodag) |

---

## 3. Open Benchmark Datasets (Zenodo, MTG CompMusic & Kaggle)

1. **[Saraga Carnatic Music Dataset on Zenodo (Record 4301735)](https://zenodo.org/records/4301735)**
   * Vocal and instrumental Carnatic performances with time-aligned melodic contours, tala cycle boundaries, and structural metadata. Maintained by MTG UPF.
2. **[Saraga Hindustani Music Dataset on Zenodo (Record 4301737)](https://zenodo.org/records/4301737)**
   * Hundreds of classical bandishes with expert annotations for tonic (Sa), raga name, gharana, and tempo class.
3. **[CompMusic Dunya Corpora (Carnatic & Hindustani)](https://dunya.compmusic.upf.edu/)**
   * Curated research corpora with multitrack audio, pitch tracks, metadata, and ground-truth tonic files accessible via the Dunya REST API and [compIAM](https://github.com/MTG/compIAM).
4. **[Indian Art Music Rhythm & Stroke Corpora on Zenodo (Record 1264667)](https://zenodo.org/records/1264667)**
   * Comprehensive rhythm dataset spanning Indian art music percussion recordings, stroke onsets, and meter annotations.
5. **[Kaggle Audio & Music Classification Hub](https://www.kaggle.com/datasets)**
   * Community-contributed collections including GTZAN audio benchmarks, tabla solo recordings, and Indian classical feature extractions.

---

## 4. Commercial Products, Apps & Digital Portals

### Riyaz (MusicMuni Labs)
* **Founders:** Sankalp Gulati and Prof. Xavier Serra (direct commercial spin-off from MTG UPF).
* **Platform:** iOS & Android mobile application.
* **Core Technology:**
  * **Calibra™:** Proprietary real-time pitch detection engine optimized for Indian vocal intonation. Provides instant visual feedback on a swara lane (detecting sharp, flat, or on-pitch).
  * **Voxa™:** Vocal profiling technology that measures pitch agility, vocal range, and intonation stability over time.
* **Curriculum:** Systematic exercises in Hindustani (Alankars, Paltas, Bandishes in popular ragas), Carnatic (Swaravalis, Geethams), and Bollywood vocal tracks.
* **Architectural Lessons for Song Lab:**
  * Demonstrates that learners need immediate visual swara feedback, but current versions focus on discrete pitch plates and score matching; full continuous ornament coaching (evaluating the shape of a meend or andolan) remains an open opportunity.

### Swar Systems (SwarShala, SwarPlug, iShala)
* **Developer:** Swar Systems (Gilles Snoeck, Switzerland / India).
* **Flagship Products:**
  * **SwarShala 5:** Full-featured desktop software for Indian music tutoring, practice, and composition. Features a built-in raga database, custom raga builder, microtonal Shruti tuner, and pitch-tracking practice modes (*Over Tune*, *Free Mode*, *With Support*).
  * **iShala:** The industry-standard mobile practice accompaniment app combining digital Tanpura, Tabla, Swarmandal, and Manjira with customizable Sa, tempo, and tala.
  * **SwarPlug:** VST/AU virtual instrument plugin delivering 80+ multi-sampled Indian classical instruments to DAWs.
* **Value to Song Lab:** Represents the benchmark for traditional Hindustani knowledge representation, swara ratio customization, and realistic synthetic accompaniment.

### Sur Sadhana (Shankar Mahadevan Academy)
* **Developer:** Clood On / Shankar Mahadevan Academy.
* **Platform:** Free mobile app for Android/iOS.
* **Features:** Guided swara intonation trainer. Users sing into the mic and see a real-time bouncing ball graphic showing whether their voice hits Sa, Re, Ga, Ma, Pa, Dha, Ni accurately.

### Virtual Accompaniments & Tanpura Hardware
* **iTabla Pandit / Tanpura Droid:** Ubiquitous digital riyaz tools among students and professional performers for generating pitch-stable tanpura drones and responsive tabla thekas.
* **Radel Electronic Instruments:** Hardware digital tanpuras (Milan, Saarang) and tablas (Taalmala) that established the electronic benchmark for tanpura overtones (first harmonic, fifth, octave).

### Curated Theory Portals & Bandish Archives
* **[Tanarang.com](https://www.tanarang.com):** Invaluable repository of 150+ Hindustani ragas with audio demonstrations, vadi, samvadi, aroha/avaroha, pakad, and notation of traditional bandishes.
* **[Chandrakantha.com](https://chandrakantha.com):** The most exhaustive cross-referenced index linking classical ragas to hundreds of Bollywood, Ghazal, and regional film compositions.
* **[Raga Surabhi](https://www.ragasurabhi.com):** Leading portal for Carnatic raga identification, raga characteristics, audio samples, and ear-training quizzes.
* **[Swarganga Music Foundation](https://www.swarganga.org):** Non-profit archive documenting raga genealogies, thaat classifications, bandish scores, and master artist genealogies.

---

## 5. Cross-Link Navigation

* 📖 **[Master Documentation Hub](file:///d:/Music/INDEX.md)**: Main architecture and index.
* 📋 **[Phase 2 Specification Plan](file:///d:/Music/plan.md)**: Design goals for ornament detection, raga intelligence, AI analyst.
* 🤖 **[Generative Music AI & Suno Compendium](file:///d:/Music/generative_music_ai.md)**: Suno, YuE, MusicGen, AudioCraft, and voice models.
* ⚙️ **[Audio Engineering & Signal Pipeline](file:///d:/Music/audio_pipeline_and_tooling.md)**: UVR5, Roformer, CREPE, Basic Pitch, and microtonal alignment.
