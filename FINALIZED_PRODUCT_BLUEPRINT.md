# Song Lab — Finalized Product Blueprint & Un-Replicable Core Logic

*Finalized architectural specification derived from the exhaustive design interview. Establishes the technical moat, core algorithms, edge-cloud split, and implementation sequence.*

---

## Table of Contents
1. [The Un-Replicable Technical Moat (Why Generic Tools Fail)](#1-the-un-replicable-technical-moat-why-generic-tools-fail)
2. [The 8 Aligned Architectural Pillars](#2-the-8-aligned-architectural-pillars)
3. [Deep Core Logic & Mathematical Formulations](#3-deep-core-logic--mathematical-formulations)
   - [Kinematic-Wavelet Ornament Extraction (Tier 1 Physics)](#kinematic-wavelet-ornament-extraction-tier-1-physics)
   - [Raga-Contextual Bayesian Refiner (Tier 2 Aesthetics)](#raga-contextual-bayesian-refiner-tier-2-aesthetics)
   - [The "What Is Missing" Deficit State Machine](#the-what-is-missing-deficit-state-machine)
4. [Hybrid Edge-Cloud Service Topology](#4-hybrid-edge-cloud-service-topology)
5. [Step-by-Step Backend Implementation Roadmap](#5-step-by-step-backend-implementation-roadmap)
6. [Cross-Link Navigation](#6-cross-link-navigation)

---

## 1. The Un-Replicable Technical Moat (Why Generic Tools Fail)

Generic AI wrappers and off-the-shelf tools (like OpenAI Whisper, generic Suno/Udio APIs, standard Librosa scripts, or basic pitch tuner apps) cannot replicate or sustain this platform for four fundamental reasons:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           THE SONG LAB DEFENSIVE MOAT                                   │
├────────────────────────────┬────────────────────────────┬───────────────────────────────┤
│ Generic / Western MIR      │ Naive AI Tuner Apps        │ Song Lab Un-Replicable Moat   │
├────────────────────────────┼────────────────────────────┼───────────────────────────────┤
│ • Enforces 12-TET equal    │ • Checks static note hit   │ • Continuous sub-cent pitch   │
│   temperament (piano grid) │   (Pass/Fail on Sa or Pa)  │   curves relative to movable  │
│ • Slices notes at onsets,  │ • Blind to continuous      │   Tonic (Sa) with 22-Shruti   │
│   destroying slides        │   meends and oscillations  │   microtonal intonation grids │
├────────────────────────────┼────────────────────────────┼───────────────────────────────┤
│ • Treats vibrato as noise  │ • Redundant line-by-line   │ • Two-tier physical-wavelet   │
│   or pitch instability     │   clutter (annotates every │   ornament classification     │
│ • No concept of movable Sa │   single note with jargon) │ • Hierarchical Deficit Engine │
│   or Raga grammar          │ • Hallucinates raga theory │   (Focuses strictly on What   │
│                            │                            │   the Singer Is Missing)      │
├────────────────────────────┼────────────────────────────┼───────────────────────────────┤
│ • Black-box classification │ • Cannot demonstrate       │ • Deterministic Evidence JSON │
│   with zero musical proof  │   audio corrections at the │ • Multi-Agent RAG with zero   │
│ • No cultural grounding    │   singer's personal Sa     │   hallucination & citations   │
│                            │                            │ • Virtual Guru micro-audio    │
│                            │                            │   demonstrations at target Sa │
└────────────────────────────┴────────────────────────────┴───────────────────────────────┘
```

---

## 2. The 8 Aligned Architectural Pillars

Through the design interview, the core platform architecture was definitively aligned across eight pillars:

1. **Product Core Identity:**
   * **Dual-Faced Platform:** Combines an **Offline Song Lab** (upload and dissect polyphonic songs, stems, ragas, and master reference tracks) with an interactive **Real-Time Live Vocal Guru** (sing against a drone/accompaniment with instant feedback on missing microtonal ornaments).
2. **Ground Truth & Scoring Moat:**
   * **Hybrid Dual-Anchor Engine:** Evaluates singing against both **Mathematical Raga Grammar** (Aroha/Avaroha, Vadi/Samvadi, Nyasa, and canonical Pakad templates) AND **Master Track Comparison** (elastic frame-by-frame DTW delta against isolated master vocal stems).
3. **Ornament Detection & Classification:**
   * **Two-Tier Hierarchical Architecture:** Tier 1 extracts raw physical kinematics and wavelet oscillations (pitch velocity, acceleration, turn duration, oscillation depth); Tier 2 evaluates raga grammar and swara context to assign culturally authentic labels (*Andolan* vs. *Gamak* vs. *Vibrato*).
4. **The "What Is Missing" Deficit Engine:**
   * **Hierarchical Severity Ranking (Max 1 Primary Critique per Phrase):** Suppresses line-by-line clutter on standard notes. Prioritizes feedback by musical severity: *Forbidden Swara ($Vivadi$) > Missing Defining Ornament > Microtonal Shruti Error > Minor Timing*.
5. **Dual-Mode Terminology:**
   * **Dynamic Mode Toggle with Rosetta Stone Bridge:** A single mathematical core mapped dynamically to **Mode 1: Indian Classical / Gayaki View**, **Mode 2: Western Contemporary / Studio View**, or **Bridge View** (displaying Indian terms with Western counterparts in tooltips).
6. **Generative Audio Subsystem:**
   * **Targeted Micro-Demonstrator & Timbre Mirror:** Focuses on synthesizing instant 3-second audio corrections of the omitted nuance (e.g., demonstrating the correct *Andolan on Komal Ga* at the singer's exact $Sa$) and responsive Tanpura/Tabla accompaniment, augmented by RVC v2 voice conversion to show student potential.
7. **AI Analyst Multi-Agent Layer:**
   * **Tool-Enabled Grounded Multi-Agent System:** Operates strictly on deterministic **Structured Evidence JSON** and the **Neo4j Raga Knowledge Graph**. Enforces mandatory citations, zero hallucination, and live tool-execution capabilities.
8. **Deployment & Performance Topology:**
   * **Hybrid Edge-Cloud Architecture:** Real-time pitch tracking, 22-shruti alignment, and instant Tier 1 ornament filtering run locally on client devices (C++/ONNX/WASM) for $< 20\text{ ms}$ zero-latency practice and zero server costs. Heavy batch stem demixing (BS-Roformer), Knowledge Graph queries, and generative audio run on cloud workers.

---

## 3. Deep Core Logic & Mathematical Formulations

```
                     Continuous Pitch Trajectory C(t) [Cents relative to Sa]
                                                │
         ┌──────────────────────────────────────┴──────────────────────────────────────┐
         ▼                                                                             ▼
┌─────────────────────────────────┐                                           ┌─────────────────────────────────┐
│  Tier 1: Physical Kinematics    │                                           │  Continuous Wavelet Transform   │
│  (Velocity & Acceleration)      │                                           │  (Multi-Scale Oscillations)     │
├─────────────────────────────────┤                                           ├─────────────────────────────────┤
│ • Velocity: v(t) = dC/dt        │                                           │ • CWT(a, b) with Morlet Wavelet │
│ • Acceleration: a(t) = d²C/dt²  │                                           │ • Short-scale: Murki (8-12 Hz)  │
│ • Monotonic glide: sign(v) const│                                           │ • Mid-scale: Gamak (3-5 Hz)     │
│ • Zero-crossings: Nyasa anchors │                                           │ • Wide-scale: Andolan (1-3 Hz)  │
└────────────────┬────────────────┘                                           └────────────────┬────────────────┘
                 │                                                                             │
                 └──────────────────────────────────────┬──────────────────────────────────────┘
                                                        │
                                                        ▼
                                       ┌─────────────────────────────────┐
                                       │ Raw Kinematic Gesture Vector    │
                                       │ {ΔC, duration, v_peak, f_osc}   │
                                       └────────────────┬────────────────┘
                                                        │
                                                        ▼
                                       ┌─────────────────────────────────┐
                                       │  Tier 2: Raga Context Refiner   │
                                       │  (PCDD Matrix + Knowledge Graph)│
                                       ├─────────────────────────────────┤
                                       │ IF swara == Komal Ga &          │
                                       │    raga == Darbari &            │
                                       │    f_osc ∈ [1.0, 3.0] Hz        │
                                       │ THEN Label = "Andolan"          │
                                       └─────────────────────────────────┘
```

### Kinematic-Wavelet Ornament Extraction (Tier 1 Physics)
1. **Pitch Representation in Cents:**
   $$C(t) = 1200 \times \log_2\left(\frac{f_0(t)}{Sa(t)}\right)$$
2. **Velocity & Acceleration Derivation:**
   $$v(t) = \frac{C(t + \Delta t) - C(t - \Delta t)}{2\Delta t}, \quad a(t) = \frac{v(t + \Delta t) - v(t - \Delta t)}{2\Delta t}$$
3. **Continuous Wavelet Transform for Multi-Scale Oscillations:**
   $$W(a, b) = \frac{1}{\sqrt{a}} \int_{-\infty}^{\infty} C(t) \psi^*\left(\frac{t - b}{a}\right) dt$$
   Using a complex Morlet wavelet $\psi(t) = \pi^{-1/4} e^{i \omega_0 t} e^{-t^2/2}$ with $\omega_0 = 6$:
   * **Scale $a_1$ ($8–12\text{ Hz}$):** Isolates rapid, delicate **Murki** and Western **Trill** micro-turns.
   * **Scale $a_2$ ($3.5–5.5\text{ Hz}$):** Isolates heavy diaphragmatic **Gamak** and Western **Vibrato**.
   * **Scale $a_3$ ($1.0–2.8\text{ Hz}$):** Isolates slow, wide-swing **Andolan** and gentle **Pitch Bends**.

### Raga-Contextual Bayesian Refiner (Tier 2 Aesthetics)
Given a detected physical oscillation tuple $\mathbf{x} = (\text{rate}, \text{depth}, \text{center\_swara})$, the probability of ornament class $O_k$ is computed using Bayesian raga conditioning:

$$P(O_k \mid \mathbf{x}, R) = \frac{P(\mathbf{x} \mid O_k) \cdot P(O_k \mid \text{swara}, R)}{\sum_j P(\mathbf{x} \mid O_j) \cdot P(O_j \mid \text{swara}, R)}$$

Where:
* $P(\mathbf{x} \mid O_k)$ is the Gaussian likelihood of the physical parameters under ornament $O_k$.
* $P(O_k \mid \text{swara}, R)$ is the prior probability encoded in the **Raga Knowledge Graph** (e.g., in Raga Darbari, $P(\text{Andolan} \mid \text{Komal Ga}) = 0.92$, whereas $P(\text{Straight Tone} \mid \text{Komal Ga}) = 0.03$).

---

### The "What Is Missing" Deficit State Machine

```
                            User Sings Phrase Ph_i
                                       │
                                       ▼
                       Feature Extraction (F0, CWT, DTW)
                                       │
                                       ▼
                     ┌───────────────────────────────────┐
                     │    Compare with Raga Template     │
                     │    / Master Reference Stem        │
                     └─────────────────┬─────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌──────────────────┐         ┌──────────────────┐          ┌──────────────────┐
│ Check 1: Grammar │         │ Check 2: Ornament│          │ Check 3: Intonate│
│ Rule Violations  │         │ Defining Nuance  │          │ Shruti Alignment │
├──────────────────┤         ├──────────────────┤          ├──────────────────┤
│ Forbidden swara  │         │ Expected meend   │          │ Sustained pitch  │
│ detected?        │         │ or andolan sung  │          │ error > 20 cents?│
│ (e.g. natural Ma)│         │ as plain note?   │          │                  │
└────────┬─────────┘         └────────┬─────────┘          └────────┬─────────┘
         │ (Yes)                      │ (Yes)                       │ (Yes)
         ▼                            ▼                             ▼
   SEVERITY = 1                 SEVERITY = 2                  SEVERITY = 3
  [Forbidden Note]             [Missing Meend/Gamak]         [Intonation Error]
         │                            │                             │
         └────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                        Sort by Severity & Select Top 1
                                      │
                                      ▼
                       Emit Single Focused Deficit Badge
                       (e.g., "[⚠️ Missing Meend Ki Lambai]")
```

---

## 4. Hybrid Edge-Cloud Service Topology

To guarantee $< 20\text{ ms}$ real-time responsiveness and zero server costs during continuous live practice, the platform implements a strict **Edge-Cloud Workload Division**:

```
┌────────────────────────────────────────────────────────┐
│                   CLIENT TIER (EDGE)                   │
│         (Browser / Desktop / Mobile Local Runtime)     │
├────────────────────────────────────────────────────────┤
│ • Audio Input: 44.1kHz / 16-bit PCM Buffer             │
│ • RMVPE ONNX Model (WASM / CoreAudio / C++ Runtime)    │
│ • Instant Tonic Normalization (Cents relative to Sa)   │
│ • 22-Shruti Dynamic Grid Mapping                       │
│ • Tier 1 Kinematic Filter (Velocity, Derivatives)      │
│ • Local Canvas Renderer: Real-Time Pitch Contour       │
│ • Latency: < 18 ms glass-to-glass | Server Cost: $0    │
└───────────────────────────┬────────────────────────────┘
                            │
                            │ [WebSocket: Session Summary & Demands]
                            │ [REST: Audio Track Upload]
                            ▼
┌────────────────────────────────────────────────────────┐
│                   CLOUD BACKEND TIER                   │
│             (High-Performance Microservices)           │
├────────────────────────────────────────────────────────┤
│ 1. Asynchronous Ingestion & Stem Demixing Service      │
│    • PyTorch BS-Roformer on GPU (NVIDIA T4 / L4)       │
│    • Full Track Accompaniment & Vocal Isolation        │
│                                                        │
│ 2. Deep Raga Intelligence & Subsequence DTW Worker    │
│    • Continuous DTW search across 30+ Ragas            │
│    • Pitch-Class Dyad Transition Profiler (PCDD)       │
│                                                        │
│ 3. Neo4j Knowledge Graph & Curated Treatise RAG Hub    │
│    • 672 Peer-Reviewed MIR Papers Index                │
│    • Bhatkhande & Natyashastra Canonical Graph Nodes   │
│                                                        │
│ 4. AI Analyst Multi-Agent Engine (LangGraph)           │
│    • Consumes Structured Evidence JSON                 │
│    • Generates Factual Natural Language Explanations   │
│                                                        │
│ 5. Virtual Guru Generative Audio Synthesizer           │
│    • RVC v2 Timbre Transfer & Micro-Phrase Corrections │
│    • Dynamic Adaptive Tanpura & Tabla FluidSynth Engine│
└────────────────────────────────────────────────────────┘
```

---

## 5. Step-by-Step Backend Implementation Roadmap

### Phase 2A: Foundational Edge Engine & Tonal Calibration (Weeks 1–3)
* Compile `RMVPE` into lightweight ONNX Runtime for local execution.
* Build the C++ / Python **Cents & 22-Shruti Normalization Module** with movable $Sa$ locking.
* Deploy the local sliding buffer generating $(t, \text{cents}, V)$ at 100 Hz.

### Phase 2B: Kinematic-Wavelet Ornament Classifier (Weeks 4–6)
* Implement first/second derivative filters for instantaneous velocity and acceleration.
* Integrate Continuous Wavelet Transform (CWT) Morlet filters for multi-scale oscillation extraction.
* Benchmark on curated classical vocal clips to validate *Meend, Gamak, Andolan, Murki, Kan* physical detection.

### Phase 2C: Deficit Engine & Raga Knowledge Graph (Weeks 7–10)
* Deploy **Neo4j Property Knowledge Graph** seeded with initial 30 foundational Hindustani & Carnatic ragas.
* Implement Subsequence Dynamic Time Warping (DTW) for canonical Pakad phrase matching.
* Build the **3-Tier Salience Filter** implementing the Hierarchical Deficit State Machine.

### Phase 2D: Asynchronous Ingestion & Source Demixing Pipeline (Weeks 11–13)
* Package BS-Roformer vocal isolation worker into Celery/Redis GPU queue.
* Implement adaptive tanpura notch filtering and tabla transient suppression.
* Build the Song Package Compiler that outputs the complete **Structured Evidence JSON**.

### Phase 2E: AI Analyst & Virtual Guru Synthesizer (Weeks 14–17)
* Deploy the LangGraph Multi-Agent system with strict Pydantic JSON guardrails and citation validators.
* Integrate RVC v2 and FluidSynth for on-demand 3-second micro-demonstrations of omitted ornaments at the singer's $Sa$.
* Connect the 672-paper curated corpus for automated scholarly citation grounding.

### Phase 2F: Musician Panel Validation & Benchmark Hardening (Weeks 18–20)
* Conduct blind evaluation panel with 5 Hindustani and Carnatic gurus on 100 test takes.
* Tune kinematic thresholds and raga prior distributions based on guru inter-annotator agreement.
* Freeze API v1 and release backend for client integration.

---

## 6. Cross-Link Navigation

* 🗺️ **[Master Documentation Hub](file:///d:/Music/INDEX.md)**: Main architecture and directory.
* 📋 **[Phase 2 Specification Plan](file:///d:/Music/plan.md)**: Musical vision, dual-mode taxonomy, and coaching principles.
* 🏗️ **[System Architecture & Implementation Plan](file:///d:/Music/system_architecture_and_implementation_plan.md)**: Component engineering trade-offs (upsides, downsides, costs).
* 🔬 **[3,257-Paper Curation & Applications](file:///d:/Music/research_papers_curation_and_applications.md)**: Literature harvest and component implementation mappings.
* 📁 **[Curated Papers Dataset](file:///d:/Music/data/curated_research_papers.json)**: Machine-readable JSON corpus of 672 papers.
* 🎶 **[Indian Classical MIR Ecosystem](file:///d:/Music/indian_classical_mir_ecosystem.md)**: Institutional frameworks, datasets, and commercial apps.
* 🤖 **[Generative Music AI & Suno Compendium](file:///d:/Music/generative_music_ai.md)**: Suno, Udio, YuE, MusicGen, and singing voice conversion.
* ⚙️ **[Audio Pipeline & Tooling Specifications](file:///d:/Music/audio_pipeline_and_tooling.md)**: Separation, pitch extraction, and 22-shruti math.
* 📚 **[Academic Research Compendium & Papers](file:///d:/Music/research_compendium_and_papers.md)**: Literature benchmarks (TDMS, DeepSRGM, PCDD, DBNs).
* 🧠 **[AI Analyst & RAG Knowledge Architecture](file:///d:/Music/ai_analyst_and_rag_architecture.md)**: Multi-agent hierarchy and knowledge graph schemas.
