# Song Lab — Phase 2 Plan: Ornaments, Raga Intelligence, AI Analyst, Knowledge Base

> **Navigation & Ecosystem Index:**
> * 🏆 **[Finalized Product Blueprint & Consensus Specs](file:///d:/Music/FINALIZED_PRODUCT_BLUEPRINT.md)**
> * 🗺️ **[Master Knowledge Hub & Architecture Index](file:///d:/Music/INDEX.md)**
> * 🏗️ **[System Architecture & Implementation Plan](file:///d:/Music/system_architecture_and_implementation_plan.md)**
> * 🎶 **[Indian Classical MIR Ecosystem & Datasets](file:///d:/Music/indian_classical_mir_ecosystem.md)**
> * 🤖 **[Generative Music AI & Suno Compendium](file:///d:/Music/generative_music_ai.md)**
> * ⚙️ **[Audio Pipeline & Tooling Specifications](file:///d:/Music/audio_pipeline_and_tooling.md)**
> * 📚 **[Academic Research Compendium & Papers](file:///d:/Music/research_compendium_and_papers.md)**
> * 🔬 **[3,257-Paper Curation & Implementation Mappings](file:///d:/Music/research_papers_curation_and_applications.md)**
> * 🧠 **[AI Analyst & RAG Knowledge Architecture](file:///d:/Music/ai_analyst_and_rag_architecture.md)**

*Extends `plan.md`. No code, only design. Phase 1 gives us stems, beat grid, pitch curve and notes. Phase 2 builds musical understanding on top of that.*

---

## 1. What Phase 2 Adds

1. **Ornament detection** with both Western and Indian classical names (vibrato, gamak, meend, kan, murki, and more)
2. **Hindustani and Carnatic tonal analysis**: tonic (Sa) detection, swara labelling, sargam notation, shruti-level (microtonal) view
3. **Raga identification** with the raga's features shown next to what the song actually does
4. **Tala and laya** detection (rhythmic cycle, not just BPM)
5. **AI Analyst**: an assistant that explains the song, the raga, your singing, and how to improve
6. **Knowledge base**: curated raga and theory data with citations from books, papers and datasets
7. **Raga-aware coaching**: scoring that knows the grammar of the raga, not just the notes

---

## 2. Reality Checks

1. **Film and pop songs are only "raga-based."** A Bollywood song may be built on Yaman or Bhairavi but uses tempered instruments, Western chords and modulations. Raga identification there is probabilistic. Always show the top 3 candidates with confidence, never a single confident verdict.
2. **Sa is not fixed.** Indian classical uses a movable tonic. Every swara label depends on first finding Sa correctly. A wrong Sa means every note and the raga guess is wrong. Tonic detection is the foundation of this phase.
3. **Swaras are not 12 equal piano keys.** Intonation is contextual (for example, komal Re in Bhairav sits differently from komal Re elsewhere) and ornaments are part of a note's identity. Work in cents relative to Sa, never snap to piano notes.
4. **Ornament labels are partly subjective.** Even gurus disagree on where a meend ends and a kan begins. Treat labels as detections with confidence, validated by a musician, not as ground truth.
5. **Raga is more than a scale.** Two ragas can share identical notes (for example Bhupali and Deshkar) and differ by emphasis, phrasing and which note you rest on. A scale matcher alone will fail. Phrase-level analysis is required.
6. **Mixed audio hurts.** Tanpura drone, tabla and harmonium leak into the vocal stem. Separation quality directly limits ornament accuracy.

---

## 3. Dual-Mode Expression, Ornament & Vocal Technique Taxonomy

To bridge global vocal techniques with traditional Indian art music, Song Lab implements a **Dual-Mode Mapping Architecture**. A single continuous pitch and acoustic performance can be inspected through two synchronized terminological lenses:
* **Mode 1: Indian Classical & Gayaki Aesthetics View** (Hindustani / Carnatic / Semi-Classical / Thumri / Ghazal)
* **Mode 2: Western Classical, Contemporary & Studio Production View** (Pop / Jazz / Opera / Modern Production)

---

### 3.1 Measurable Acoustic Features from the Signal
Everything below is calculated from the continuous fundamental frequency contour ($F_0$ in cents relative to $Sa$), energy/loudness dynamics ($RMS$ envelope), spectral harmonics, and temporal derivative dynamics ($dC/dt$, $d^2C/dt^2$):

| Raw Acoustic Feature | Measured Parameters | Underlying Vocal Phenomena |
|---|---|---|
| **Oscillatory Pitch Modulation** | Rate (Hz), Depth (Cents), Onset Delay (ms), Regularity | Vibrato, Andolan, Gamak, Kampan, Tremolo |
| **Continuous Pitch Glides** | Velocity (cents/s), Trajectory Curvature, Duration | Meend, Soot, Ghasit, Portamento, Glissando, Scoops |
| **Transient Pitch Inflexions** | Duration (20–80 ms), Peak Amplitude, Attack Angle | Kan Swar (Sparsh), Grace Notes, Acciaccatura, Khatka |
| **Multi-Note Clusters / Turns** | Directional reversals, Velocity peaks, Symmetry | Murki, Zamzama, Trill, Mordent, Turn, Cadenza |
| **Rapid Sequence Melodics** | Note rate (notes/sec), Saccadic step stability | Taan (Sapaat, Vakra, Gamak), Vocal Runs, Melisma |
| **Sustained Plateaus** | Pitch variance ($\pm \text{cents}$), Formant ratio, Harmonics | Swar Sthirata, Straight Tone, Belting, Nyas |
| **Phonation & Register Transitions**| H1-H2 harmonic ratio, Spectral tilt, Glottal onsets | Chest, Head, Mixed Voice, Falsetto, Vocal Fry |

---

### 3.2 Mode 1: Indian Classical, Semi-Classical & Gayaki Aesthetics Vocabulary

```
                                  Mode 1: Indian Gayaki Aesthetics
                                                 │
         ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
         ▼                   ▼                   ▼                   ▼                   ▼
┌──────────────────┐┌──────────────────┐┌──────────────────┐┌──────────────────┐┌──────────────────┐
│  Ornaments &     ││  Taans & Speed   ││  Alap, Vistar &  ││ Swara / Shruti   ││  Execution       │
│  Microtonality   ││  Execution       ││  Improvisation   ││ Intonation       ││  Quality Metrics │
├──────────────────┤├──────────────────┤├──────────────────┤├──────────────────┤├──────────────────┤
│ • Meend, Gamak   ││ • Sapaat, Vakra  ││ • Swar Vistar    ││ • Shruti Lagav   ││ • Taan Ki Safai  │
│ • Andolan, Murki ││ • Bol/Sargam/Aakar││ • Badhat, Laykari││ • Swar Sthirata ││ • Gamak Gahraai  │
│ • Khatka, Kan    ││ • Gamakdar Taan  ││ • Bol-Banao      ││ • Vadi-Samvadi   ││ • Meend Lambai   │
│ • Zamzama, Kampan││ • Chhoot Taan    ││ • Sthayi/Antara  ││ • Raga Bhav      ││ • Thehraav       │
└──────────────────┘└──────────────────┘└──────────────────┘└──────────────────┘└──────────────────┘
```

The system classifies Indian classical singing across seven distinct functional dimensions:

#### 1. Ornaments & Micro-Pitch Dynamics (*Alankars & Gamakas*)
* **Meend (Glissando / Portamento):** Smooth, uninterrupted glide connecting two or more swaras, revealing intermediate microtonal shades (*shrutis*).
* **Meenddaar Gayaki:** A singing style prioritizing sustained, continuous curved slides over punctuated notes.
* **Gamak:** Heavy, forceful oscillation originating from the chest/diaphragm with synchronized loudness surges.
* **Gamakdar Taan:** Rapid runs where every note is attacked with a gamak impulse.
* **Andolan:** Slow, gentle, wide swinging oscillation centered on specific microtonal swaras (e.g., *komal Ga* in Darbari Kanada, *komal Dha* in Bhairav).
* **Andolan Ki Gati:** Measured speed and regularity of the andolan oscillation.
* **Murki:** Extremely agile, delicate cluster of 2–4 notes turning rapidly around a focal pitch.
* **Murkidaar Gayaki:** Singing style rich in intricate, filigree turns (characteristic of Thumri, Dadra, and Kirana/Patiala ang).
* **Khatka:** Sharp, punchy turn; a sudden, rapid cluster of notes executed with crisp articulation.
* **Kan Swar / Sparsh Swar (Grace Note):** A brief touch note grazing an adjacent swara for a few tens of milliseconds before resolving into the primary swara.
* **Kan Ka Prayog:** The artistic placement and subtlety of grace notes.
* **Zamzama:** Rapid, sequential repeated ornamental oscillation pattern, common in Tappa and Dhrupad.
* **Krintan:** Quick hammer-on and pull-off ornament, attacking a note and rapidly catching its neighbor.
* **Kampan / Aawaz Ka Kampan:** Natural vocal flutter or fine trembling oscillation (*vibrato*).
* **Sur Ki Larzish:** Subtle, delicate quaver or shimmer on a held note.

#### 2. Taans & Rapid Melodic Runs (*Drut Phirat*)
* **Taan:** Fast melodic sequence rendered across the octave.
* **Sapaat Taan (Linear Run):** Straight, unbroken scalar run ascending or descending in strict note order ($S-R-G-M-P-D-N-S'$).
* **Vakra Taan (Zigzag Run):** Intricate, non-linear taan weaving back and forth through winding note paths.
* **Bol Taan:** Fast melodic runs executed on the lyrics (*bols*) of the bandish while preserving diction.
* **Sargam Taan:** Rapid runs vocalized using the swara names themselves (*Sa, Re, Ga, Ma...*).
* **Aakar Taan:** Runs sung entirely on the open vowel sound *"Aa"*.
* **Gamakdar Taan / Gamak Taan:** Rapid runs where every note is attacked with a heavy gamak impulse.
* **Chhoot Taan:** Spontaneous, cascading taan where the voice leaps or drops precipitously from the upper register.
* **Taan Pradhan Gayaki:** Performance style that emphasizes speed, agility, and virtuosic runs (e.g., Patiala or Gwalior drut khayal).

#### 3. Alap, Phrasing & Structural Expansion (*Vistar & Badhat*)
* **Aalap (Alap):** Slow, unmetered meditative exploration establishing the personality, mood, and grammar of the raga.
* **Aalapi:** The technique and expressive mood of alap elaboration.
* **Aakar Aalap:** Alap rendered on the pure open vowel *"Aa"*.
* **Bol Aalap:** Slow melodic phrases using the words/syllables of the poetry to color the notes.
* **Sargam Aalap:** Alap sung using swara names to emphasize raga structure.
* **Nom-Tom:** Traditional rhythmic alap syllables (*Nom, Tom, Tana, Dere, Na*) utilized in Dhrupad and Agra gharana.
* **Swar Vistar / Swar Visthar:** Systematic expansion of the raga, note by note, from lower to higher registers.
* **Badhat / Aalap Ki Badhat:** Progressive development and growth of melodic architecture.
* **Sthayi Vistar & Antara Vistar:** Melodic development focused on the lower/middle octave verse (*sthayi*) versus the upper register chorus (*antara*).
* **Bol-Banao:** Expressive emotional sculpting of poetic syllables with delicate melodic curves.
* **Layakari & Lay-Badhat:** Rhythmic play, syncopation, and tempo multiplication (*Thaah, Dugun, Tigun, Chaugun*) against the tala cycle.

#### 4. Intonation, Swara Lagav & Raga Grammar
* **Shruti & Shruti Lagav:** Precise microtonal positioning of a note within the 22-shruti spectrum; how the swara is approached and placed.
* **Komal Swar Lagav & Tivra Madhyam Lagav:** Exact microtonal shading applied to flattened and sharpened notes.
* **Swar Lagav / Sur Ka Lagav:** The aesthetic touch, entry, and intonational purity of a note.
* **Swar Shuddhata (Pitch Purity):** Intonational correctness relative to the tonic $Sa$ and raga scale.
* **Swar Sthirata / Swar Ka Thehraav:** Rock-solid stability, pitch stillness, and rest on sustained notes without pitch waver.
* **Sur Ki Pakad:** Grasp and retention of the raga's authentic pitch personality and defining phrases.
* **Vadi-Samvadi Ucharan:** Strategic acoustic emphasis and duration bestowed on the king and queen notes of the raga.
* **Nyas / Nyas Swar:** Structural resting notes where phrases conclude and pause.
* **Ansh Swar:** The principal thematic note of an ancient jati/raga.
* **Swar-Sangati & Swar-Samvad:** Consonant swara pairs and harmonically resonant melodic couplings (e.g., $Sa-Pa$ or $Re-Dha$).
* **Avirbhav & Tirobhav:** The deliberate revelation (*avirbhav*) and subtle temporary concealment (*tirobhav*) of a raga's identity through shades of an allied raga.
* **Raga Bhav, Bhava Abhivyakti & Ras Nishpatti:** Evocation of the authentic emotional essence, aesthetic mood (*rasa*), and spiritual color of the raga.
* **Swar Uchcharan:** Vocal articulation, projection, and acoustic delivery of notes.

#### 5. Gayaki Stylistic Emphases
* **Aakar Pradhan Gayaki:** Focus on open-throat vowel production and resonance.
* **Bol Pradhan Gayaki:** Focus on lyrical poetry, word articulation, and dramatic expression.
* **Lay Pradhan Gayaki:** Focus on metrical mastery, cross-rhythms, and percussion interplay.

#### 6. Artistic Execution Quality Metrics (The "Safai" & "Depth" Criteria)
* **Aakar Ki Safai:** Cleanliness, warmth, and tonal purity of the open vowel sound.
* **Taan Ki Safai:** Clarity and separation of individual notes during rapid passages (avoiding blurred pitch mush).
* **Taan Ki Barabari:** Metric uniformity, rhythmic evenness, and tempo consistency across every note in a run.
* **Taan Ki Phirat / Bol Ki Phirat / Swar Ki Phirat:** Fluidity, agility, and circular ease when maneuvering across octaves.
* **Taan Ki Gati:** Clean tempo velocity of execution.
* **Taan Ki Ladi:** Unbroken chain-like continuity of melodic phrases.
* **Murki Ki Safai:** Crisp, featherweight execution of rapid turns without pitch clumsiness.
* **Gamak Ki Gahraai:** Depth, abdominal resonance, and roundness of the gamak oscillation (not shallow shaking).
* **Meend Ki Lambai:** Sustained length, breath continuity, and tension of long slides across distant notes.
* **Andolan Ki Gati:** The slow, measured tempo and controlled breadth of the andolan oscillation.

#### 7. Vocal Technique, Phrasing & Delivery
* **Vocal Phrasing & Breath Phrasing:** The natural, expressive structuring of musical sentences around breath control and rhythmic pulse.
* **Aawaz Ka Modulation & Voice Modulation:** The dynamic, nuanced shaping of vocal volume, inflection, and tone color.
* **Note Transition & Smooth Transitions:** Fluid, seamless navigation between notes and registers without abrupt glitches.
* **Register Transition:** Navigating between mandra (chest), madhya (mixed), and taar (head) saptaks.
* **Vocal Agility & Vocal Flexibility:** Suppleness, speed, and precision in executing complex ornaments, vocal riffs, and vocal runs.
* **Vocal Ornamentation:** The collective mastery of graceful embellishments coloring the melodic line.
* **Phonation Attacks:** Employing **soft attack** (gentle onset) versus **hard attack** (glottal punch) depending on the emotional demand of the bandish.
* **Note Bending & Note Sliding:** Microtonal sliding between swara intervals without breaking vocal continuity.
* **Connected Phrasing & Detached Phrasing:** Sustaining continuous legato connection versus detached, punctuated delivery.
* **Syncopated Phrasing:** Rhythmic interplay and metric offsets against the tala cycle (*layakari*).
* **Dynamic Nuance & Emotional Inflection:** Subtle, micro-expressive shifts in volume and emotional coloring to evoke authentic *Raga Bhav*.

---

### 3.3 Mode 2: Western Classical, Contemporary & Studio Production Vocabulary

```
                               Mode 2: Western & Contemporary Production
                                                  │
         ┌───────────────────┬────────────────────┼───────────────────┬───────────────────┐
         ▼                   ▼                    ▼                   ▼                   ▼
┌──────────────────┐┌──────────────────┐ ┌──────────────────┐┌──────────────────┐┌──────────────────┐
│ Vocal Agility    ││ Articulation &   │ │ Registers &      ││ Dynamics, Timing ││ Studio & Audio   │
│ & Ornaments      ││ Pitch Bends      │ │ Phonation        ││ & Phrasing       ││ Production FX    │
├──────────────────┤├──────────────────┤ ├──────────────────┤├──────────────────┤├──────────────────┤
│ • Vibrato Types  ││ • Portamento/Gliss││ • Chest/Head/Mix ││ • Cresc./Dimin.  ││ • Reverb/Delay   │
│ • Melisma, Riffs ││ • Legato/Staccato│ │ • Belting, Fry   ││ • Sforzando      ││ • Chorus/Flanger │
│ • Runs, Trills   ││ • Pitch Scooping │ │ • Falsetto       ││ • Rubato, Syncop.││ • EQ, Harmonics  │
│ • Mordent, Grace ││ • Blue Notes     │ │ • Glottal Attack ││ • Breath Phrasing││ • Compression    │
└──────────────────┘└──────────────────┘ └──────────────────┘└──────────────────┘└──────────────────┘
```

The system classifies contemporary vocal and acoustic performances across five core pillars:

#### 1. Vocal Agility, Runs & Ornaments
* **Vibrato Types:** Periodic pitch oscillation analyzed by rate, depth, and onset delay:
  * *Sustained Vibrato:* Continuous, stable oscillation maintained through long notes.
  * *Straight Tone:* Pure, non-vibrating fundamental pitch plate (characteristic of early music and pop choruses).
  * *Subtle Vibrato:* Gentle, low-depth ($\pm 20-30\text{ cents}$) modulation.
  * *Wide Vibrato:* Deep pitch swings ($\pm 70-120\text{ cents}$) common in operatic singing.
  * *Fast Vibrato (Tremolo-like):* Oscillation rate exceeding 7.5 Hz (often caused by vocal tension).
  * *Slow Vibrato (Wobble):* Oscillation rate below 4.5 Hz (often caused by lack of diaphragmatic support).
* **Melisma:** Singing multiple distinct pitch notes across a single syllable of text.
* **Vocal Runs & Vocal Riffs (Riff & Run):** Fast, agile scalar or pentatonic flourishes characteristic of R&B, soul, and gospel singing.
* **Trill:** Rapid, continuous alternation between two adjacent scale degrees.
* **Mordent & Turn:** Short ornaments dipping once to an adjacent lower/upper note and returning instantly.
* **Grace Notes (Appoggiatura & Acciaccatura):** Crushed pre-onset notes executed before or directly on the beat.
* **Cadenza & Trillando:** An elaborate, virtuosic ornamental passage or tremulous/trilled embellishment rendered by a soloist.
* **Embellishment & Vocal Ornamentation:** The broader stylistic vocabulary of decorative expressive devices.

#### 2. Articulation, Pitch Bends & Note Transitions
* **Portamento:** A deliberate, audible continuous slide connecting two pitch targets.
* **Glissando:** A rapid slide spanning multiple scale steps.
* **Legato:** Smooth, seamless connection between notes with zero silent gaps.
* **Staccato:** Crisp, detached, punctuated notes with sharp silent cutoffs.
* **Portato, Tenuto, Marcato, Spiccato:** Varying weights, accents, and holds applied to note onsets.
* **Pitch Scooping:** Approaching a target pitch from underneath before settling on center.
* **Pitch Dropping / Fall-off:** Dropping the pitch downward at the end of a held note as vocal energy decays.
* **Note Bending & Sliding:** Microtonal manipulation stretching notes upward or downward away from 12-TET temperaments.
* **Blue Notes:** Microtonally flattened thirds, fifths, and sevenths expressive of Blues, Jazz, and Rock phrasing.
* **Ghost Notes:** Muted, swallowed, or whispered syllables providing percussive rhythmic accents.

#### 3. Vocal Registers, Phonation & Voice Placement
* **Chest Voice (Modal Voice):** Thick vocal fold mass producing rich, powerful low and mid-frequency acoustic resonance.
* **Head Voice:** Thinned vocal fold edges resonating primarily in the cranial and nasal cavities; clean, clear high notes.
* **Mixed Voice (Voix Mixte):** The seamless blend of chest and head mechanisms, essential for singing powerful high notes without strain.
* **Belting:** Carrying chest-dominant timbre and high subglottic pressure high into the vocal register.
* **Falsetto:** Incomplete vocal fold closure with airy, soft high-register timbre.
* **Vocal Fry (Pulse Register):** Low-frequency creaky rattling produced by slow, flaccid vocal cord vibration.
* **Yodeling:** Rapid, deliberate alternating flips between chest voice and falsetto registers.
* **Voice Cracking:** Involuntary register break caused by sudden laryngeal instability or tension.
* **Phonation Attacks:**
  * *Glottal Attack:* Explosive onset caused by vocal cords snapping open against high subglottic pressure.
  * *Aspirated Attack:* Breathy onset where airflow precedes vocal cord approximation.
  * *Soft Phonation / Coordinated Attack:* Perfect simultaneous alignment of breath stream and vocal fold closure.
* **Open Throat (Chiodo):** Lowered larynx and lifted soft palate expanding the pharyngeal resonating chamber.
* **Nasality:** Excessive sound transmission through the nasal cavity due to a dropped soft palate.
* **Vocal Resonance & Timbre:** The unique harmonic spectrum and formant profile (*singer's formant* around 3 kHz).

#### 4. Dynamics, Timing & Phrasing
* **Dynamic Control:** Command over volume without losing pitch stability:
  * *Crescendo:* Gradual increase in loudness.
  * *Diminuendo / Decrescendo:* Gradual decrease in loudness.
  * *Sforzando ($sfz$):* Sudden, explosive accent on a single note.
  * *Pianissimo ($pp$) & Fortissimo ($ff$):* Extreme soft and extreme loud dynamics.
* **Breath Control & Breath Support:** Managing diaphragmatic air pressure to maintain steady, unforced tone.
* **Breath Phrasing:** Structuring musical sentences around natural, silent breath inhalations.
* **Rubato:** Elastic, expressive tempo flexibility speeding up and slowing down without altering the overall metric bar.
* **Fermata:** An expressive, prolonged hold or pause on a note or rest beyond its nominal metrical value.
* **Syncopation & Rhythmic Precision:** Accenting off-beats and maintaining metric tightness against the click track.
* **Connected vs. Detached Phrasing:** Continuous emotional legato versus staccato narrative delivery.

#### 5. Extended Instrumental, Orchestral & Production Vocabulary
* **Performance Techniques:** *Arpeggio, Ostinato, Pizzicato, Sul Ponticello, Col Legno, Flutter Tonguing, Harmonization, Counterpoint, Con Sordino, A Cappella, Palm Muting, Harmonics*.
* **Audio Engineering & Production Effects:** *Wah-Wah, Feedback, Distortion, Overdrive, Chorus, Flanger, Phaser, Reverb, Delay, Echo, Sustain, Attack, Decay, Release (ADSR envelope)*.

---

### 3.4 Cross-Domain Conceptual Mapping Engine

Song Lab's translation engine allows users and teachers to view the exact same vocal phenomenon in either vocabulary:

| Indian Classical / Gayaki Concept (Mode 1) | Western / Contemporary Analog (Mode 2) | Shared Acoustic Signal Signature |
|---|---|---|
| **Meend / Soot / Ghasit** | Portamento / Continuous Pitch Glide / Slide | Monotonic continuous change in $F_0$ across $\ge 2$ intervals |
| **Kan Swar / Sparsh Swar** | Grace Note / Acciaccatura | Transient pitch blip ($< 80\text{ ms}$) adjacent to target note |
| **Gamak (Diaphragmatic)** | Heavy Pitch Modulation with Dynamic Pulse | Periodic oscillation ($3-5\text{ Hz}$) with synchronous RMS peaks |
| **Andolan** | Wide Pitch Oscillation / Slow Vibrato | Slow periodic pitch swing ($1-3\text{ Hz}$, depth $\pm 80-160\text{ cents}$) |
| **Murki** | Fast Turn / Mordent | Multi-inflection rapid turnaround ($< 250\text{ ms}$) around central note |
| **Khatka** | Staccato Turn / Sharp Articulation | Rapid direction change with explosive onset velocity |
| **Taan (Sapaat)** | Vocal Run / Fast Linear Scalar Run | Rapid continuous note events ($> 6\text{ notes/sec}$) in scale |
| **Bol Taan** | Melisma across Consonants / Articulated Run | Fast melodic runs with synchronized phoneme/syllable transitions |
| **Aakar Taan** | Pure Vowel Vocal Run | Melisma sustained entirely over open vowel formant |
| **Swar Sthirata / Swar Ka Thehraav** | Pitch Stability / Straight Tone / Sustained Hold | Pitch deviation $< \pm 8\text{ cents}$, flat variance over $\tau > 1.5\text{ s}$ |
| **Shruti Lagav** | Microtonality / Intonation Adjustment | Cent offset relative to 12-TET ($+12\text{ cents}$, $-14\text{ cents}$, etc.) |
| **Kampan / Sur Ki Larzish** | Subtle Vibrato / Vocal Shimmer | Regular pitch oscillation ($5-7\text{ Hz}$, depth $\pm 30-60\text{ cents}$) |
| **Layakari** | Syncopation / Metric Modulation / Rubato | Temporal displacement of note onsets relative to metrical grid |
| **Nom-Tom / Bol-Banao** | Phrasing / Syllabic Texturing | Expressive elongation of non-lexical or poetic vocables |
| **Aakar Ki Safai** | Tonal Clarity / Open-Throat Resonance | Balanced lower formants ($F_1, F_2$) and acoustic richness |
| **Taan Ki Barabari** | Rhythmic Uniformity / Note Equalization | Constant inter-onset intervals ($\Delta t$) across run sequence |
| **Gamak Ki Gahraai** | Diaphragmatic Depth / Amplitude Resonance | High crest-factor in energy envelope during oscillation cycle |
| **Meend Ki Lambai** | Sustained Portamento Arc | Extended duration and seamless connection of long-distance glides |

---

### 3.5 The Anti-Clutter & "What Is Missing" Feedback Principle

> [!IMPORTANT]
> **The Golden Feedback Rule:** An AI coach that tags every single line with 20 technical terms is unplayable, exhausting, and pedagogically useless. Song Lab **never overwhelms the user with line-by-line taxonomy clutter**. Instead, the system uses a **Salience Filter** to suppress expected musical events and focuses its active feedback with sharp emphasis on **what the singer is missing**.

```
                           User's Sung Vocal Line
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │    Acoustic Feature Parser    │
                     │    (Detects all ornaments)    │
                     └───────────────┬───────────────┘
                                     │
                                     ▼
                     ┌───────────────────────────────┐
                     │   3-Tier Salience Filter      │
                     └───────────────┬───────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌──────────────────┐       ┌──────────────────┐        ┌──────────────────┐
│ Tier 1: Baseline │       │ Tier 2: Milestones│       │ Tier 3: Deficit  │
│ (Normal / Plain) │       │ (Clean Badges)   │        │ ("What's Missing")│
├──────────────────┤       ├──────────────────┤        ├──────────────────┤
│ In-tune scalar   │       │ Distinct murki   │        │ **PRIMARY FOCUS** │
│ notes & standard │       │ or meend cleanly │        │ Highlights the   │
│ phrasing are     │       │ rendered; tagged │        │ crucial omitted  │
│ silent (no text).│       │ on contour hover.│        │ aesthetic nuance.│
└──────────────────┘       └──────────────────┘        └────────┬─────────┘
                                                                │
                                                                ▼
                                                   Actionable Deficit Badge
                                                   & Focused Voice Coaching
```

#### How the "What Is Missing" Engine Operates in Practice:
1. **Tier 1: Silent Baseline (Zero Noise):**
   * If a singer hits normal notes accurately within the raga or song scale, the UI displays no redundant text tags like `[Chest Voice]`, `[Straight Note]`, `[Sargam]`. Silence is respect for the performer's flow.
2. **Tier 2: Subtle Milestone Badges (On-Demand Inspection):**
   * Recognised signature techniques (e.g., a clean *Murki* or smooth *Meend*) are drawn as subtle, elegant glyphs directly above the pitch curve. Hovering reveals technical stats without generating audio popups.
3. **Tier 3: The Active Focus — The Deficit ("What You Are Missing"):**
   * The AI Analyst and Live Coach reserve active verbal and visual emphasis strictly for the **missing aesthetic component** that separates amateur singing from mastery:
     * **Missing Gamak Ki Gahraai (Indian Classical Mode):**
       > *"Your pitch on Ma is technically in tune, but **Gamak Ki Gahraai** was missing — you sang a flat Western vibrato instead of the deep, abdominal pulse required for Darbari."*
     * **Missing Meend Ki Lambai / Connection (Indian Classical Mode):**
       > *"Between Pa and Ga, you snapped directly across the gap as two disconnected notes. You missed the continuous **Meend Ki Lambai** that connects this phrase."*
     * **Missing Swar Ka Thehraav / Sthirata (Indian Classical Mode):**
       > *"On the Shadja (Sa), your voice wavered with nervous tremor. You lacked **Swar Ka Thehraav** — hold the note with calm, steady stillness."*
     * **Missing Taan Ki Barabari (Indian Classical Mode):**
       > *"In the ascending sapaat taan, your pitch accuracy was 90%, but **Taan Ki Barabari** faltered — notes 5, 6, and 7 rushed ahead of the laya."*
     * **Missing Kan Swar (Indian Classical Mode):**
       > *"You sang a bare Re $\rightarrow$ Ga; the characteristic **Kan Swar** grazing Ma from above was omitted."*
     * **Missing Mixed Voice / Breath Support (Western Mode):**
       > *"On the chorus climax (G4), you slipped into an airy, weak falsetto. You are missing **Mixed Voice resonance and diaphragmatic breath support** to anchor the belt."*
     * **Missing Legato Connection (Western Mode):**
       > *"Your vocal line was chopped into staccato fragments. Focus on **Smooth Legato transition and breath phrasing** across the bar line."*

#### Visual "Delta / Deficit" Canvas Overlay
On the visual pitch canvas, the user sees:
* **The Sung Line:** User's actual pitch contour in solid color.
* **The Ghost Reference Line:** The ideal raga or reference master take in soft translucency.
* **The Deficit Highlight Zone:** When an ornament or aesthetic quality is missing, the canvas paints a highlighted bracket with an explicit deficit callout:
  * `[⚠️ Missing Kan Swar from Pa]`
  * `[⚠️ Missing Meend Glide — Abrupt Jump Detected]`
  * `[⚠️ Lacks Gamak Depth — Oscillation Too Shallow]`
  * `[⚠️ Missing Breath Support — Unstable Straight Tone]`

---

## 4. Tonal Foundation: Sa, Swaras, Shrutis

1. **Tonic (Sa) detection**
   - Use the tanpura/drone if present (stable pitch peaks, Sa and Pa), otherwise the pitch histogram of the vocal and the recurrence of resting notes
   - Let the user confirm or override; the singer's chosen Sa is critical
2. **Pitch distribution relative to Sa:** a fine-grained histogram (bins of about 10–25 cents) showing which swaras are used and how much, including microtonal position
3. **Swara labelling:** map the curve to Sa Re Ga Ma Pa Dha Ni with komal/tivra variants, across octaves (mandra, madhya, taar)
4. **Sargam notation output:** a text/score view like *Ni Re Ga Re Sa*, with octave dots, ornament symbols, and bar/tala markers
5. **Shruti view (advanced):** show deviation from the 12-note equal grid and from the traditional 22-shruti framework, as an educational overlay rather than a strict pass/fail
6. **Western-note toggle:** switch labels between sargam, Western names and movable-Do

---

## 5. Raga Identification

### 5.1 What the system should output
For the best candidate ragas (top 3–5, with confidence):

| Field | Explanation |
|---|---|
| Raga name and aliases | Including spelling variants (Yaman / Kalyan, Bhairavi, Todi, etc.) |
| **That (Thaat)** | Parent scale in Bhatkhande's system (10 thaats); Carnatic equivalent *melakarta* where applicable |
| **Jati** | Number of notes in ascent/descent (audava 5, shadava 6, sampurna 7 and combinations) |
| **Aroha / Avaroha** | Ascending and descending patterns, including vakra (zigzag) movement |
| **Vadi / Samvadi** | The king and minister notes (most emphasised and second most) |
| **Varjya swara** | Notes omitted |
| **Pakad / chalan** | The characteristic phrase(s) that identify the raga |
| **Nyasa swara** | Notes where phrases rest |
| **Prahar / time of day** | Traditional performance time |
| **Season (if any)** and **Rasa/mood** | Traditional associations |
| Similar ragas | Easily confused ragas and how to tell them apart |
| Famous compositions | Film songs and classical bandishes in this raga |

### 5.2 How "what it has in common with the raga" is shown
A side-by-side report for the loaded song:
- **Scale match:** which notes the song uses vs. the raga's notes; any outside notes flagged (for example, a Western chord tone or a deliberate *vivadi* note)
- **Emphasis match:** the song's most-used and most-rested-on notes vs. vadi/samvadi/nyasa
- **Movement match:** does the melody follow aroha/avaroha rules and vakra patterns
- **Phrase match:** timestamps where a pakad phrase or a recognised characteristic phrase appears (highlighted on the waveform)
- **Ornament match:** ornaments typical of the raga vs. what is present
- **Deviation list:** where the song departs from the raga (crossovers, modulations into another raga, a *mishra* or mixed-raga passage)
- **Summary:** "This song is closest to Raga X (confidence Y%), mostly following its aroha-avaroha, with a touch of Raga Z in the antara"

### 5.3 Recognition approach (layered, from simple to strong)
1. **Pitch-class profile matching:** compare the song's relative-to-Sa histogram against raga templates
2. **Sequence/phrase matching:** n-gram patterns of swaras and characteristic phrase search with tolerance for ornaments and tempo
3. **Learned model:** a sequence model over the pitch contour trained on labelled raga recordings; ensemble with the rule-based layers
4. **Sectionwise analysis:** run recognition per section (mukhda, antara, alap) because songs may shift between ragas
5. **Explainability:** every prediction must come with the evidence (notes, phrases, timestamps), never just a label

Candidate data sources to evaluate (check availability, license and quality when you start): the CompMusic project's Indian art music corpora and datasets (including Saraga and raga recognition collections), published Hindustani and Carnatic raga datasets on research repositories, and any academic annotations on film songs. Commercial streaming recordings generally cannot be redistributed, so keep training data legally clean.

### 5.4 Scope control
- **Start small:** 20–30 popular Hindustani ragas (Yaman, Bhairav, Bhairavi, Bilawal, Kafi, Khamaj, Todi, Malkauns, Darbari, Bhupali, Desh, Puriya, Marwa, Asavari, Bageshree, Pilu, Jaunpuri, and so on) and expand
- **Hindustani first**, Carnatic as a separate track with its own raga database (72 melakartas plus janya ragas)
- **Be explicit when unsure:** "Low confidence: the song modulates between two ragas" is a good result

---

## 6. Tala and Laya

- Go beyond BPM: detect the **tala** (for example, Teentaal 16 beats, Jhaptaal 10, Ektaal 12, Dadra 6, Keherwa 8, Rupak 7) with **sam** (the first beat), **khali** (the empty beat) and **vibhag** (sections)
- Detect **laya** (tempo class): vilambit (slow), madhya (medium), drut (fast), and tempo drift
- Percussion-aware analysis: tabla/pakhawaj stroke recognition (dha, dhin, na, tin, ta...) as a stretch goal
- Show the tala cycle visually (circular or bar view) with the current beat
- **Practice:** a tanpura and tabla generator in your chosen scale (Sa) and tala, so users can practise without the song

---

## 7. Raga-Aware Live Coaching & The "What Is Missing" Engine (extends Phase 1 scoring)

### 7.1 The Golden Feedback Rule: What Someone Is Missing (Anti-Clutter Principle)
Traditional singing apps and naive MIR prototypes fail because they produce **line-by-line clutter**—bombarding the user with dozens of redundant badges and vocal jargon on every single phrase. 

Song Lab strictly enforces **Deficit-First Coaching**:
1. **Never tag every line with generic labels.** If a note is sung stably on-pitch without ornaments, the system stays silent. No unnecessary tags like `[Chest Voice]`, `[Straight Tone]`, `[Normal Step]`.
2. **Focus 80% of feedback on the missing artistic quality:** What did the singer omit that prevents the line from sounding authentic?
   * *Example 1 (Indian Classical Mode):* *"Your intonation on komal Ga in Darbari was on frequency, but **Gamak Ki Gahraai** was missing — you held a flat straight note instead of the required deep, resonant oscillation."*
   * *Example 2 (Indian Classical Mode):* *"Between Pa and Ga, you jumped abruptly. You missed the continuous **Meend Ki Lambai** that ties the phrase together."*
   * *Example 3 (Indian Classical Mode):* *"The taan suffered from uneven speed at beat 6 — **Taan Ki Barabari** was missing."*
   * *Example 4 (Western Contemporary Mode):* *"On the high belted note (F4), your vocal folds thinned into an airy break — **Mixed Voice resonance and diaphragmatic breath support** were missing."*
   * *Example 5 (Western Contemporary Mode):* *"Your run was pitched correctly, but **Vocal Agility and clean note separation** were missing — individual notes smeared into pitch glides."*

### 7.2 Core Coaching Modalities
- **Dual-Mode Feedback Toggle:** Switch between 🕉️ *Indian Classical (Gayaki View)* and 🌐 *Western Contemporary (Studio View)* at any moment.
- **Deficit Callout Overlays:** Visual brackets on the pitch canvas highlighting missing ornamentation (`[⚠️ Missing Kan Swar]`, `[⚠️ Missing Andolan Width]`, `[⚠️ Missing Breath Phrasing]`).
- **Grammar check:** flag any note not allowed in the chosen raga (e.g., natural Ma in Yaman instead of tivra Ma), separate from "off pitch"
- **Aroha/avaroha adherence** when singing exercises
- **Pakad drill:** the app plays a characteristic phrase and checks your reproduction, including its ornaments
- **Ornament scoring:** did you perform the meend smoothly, was the andolan too fast, was the kan too long
- **Shruti-aware tolerance:** a komal Ga in Darbari is allowed to sit lower and oscillate, so don't mark it flat
- **Tanpura mode:** sing against a drone, with feedback relative to Sa and Pa
- **Alap practice:** unmetered singing mode where timing is not scored, only pitch, ornaments and raga adherence
- **Teacher mode:** a guru can record a reference phrase, and students are scored against it

---

## 8. AI Analyst (the "AI that analyzes it")

### 8.1 Role
A conversational layer that turns the numbers into understanding. It never replaces the signal-processing pipeline; it explains and connects the pipeline's output.

### 8.2 What it can do
- **Explain the song:** structure, key, tempo, tala, raga evidence, notable ornaments, emotional character
- **Explain your singing:** "You rushed the second line, your komal Ga sat 35 cents sharp, and your meend between Pa and Dha was cut short"
- **Answer questions:** "Why is this Bhairavi and not Asavari?", "Which part uses a murki?", "Show me similar songs"
- **Make practice plans:** a weekly plan built from your weakest areas, with specific drills
- **Compare:** two versions of a song, two singers, or your takes over time
- **Teach concepts:** short lessons on raga, thaat, tala, gamak, with examples taken from the loaded song
- **Search the library:** "find songs in raga Yaman at about 90 BPM that I can sing in my range"

### 8.3 Architecture of the Analyst
1. **Structured evidence in:** the Song Package and Session results go to the AI as compact structured data (notes, ornaments, raga scores, timestamps, metrics), not as raw audio. This keeps it accurate and cheap.
2. **Retrieval in:** the AI pulls definitions and raga facts from the curated knowledge base (Section 9) and always cites them.
3. **Tools:** the AI can request more analysis from the pipeline ("re-run raga detection for the second verse only", "isolate bars 17–24") instead of guessing.
4. **Guardrails:**
   - Must separate **measured facts** (from the pipeline) from **interpretation** (its own)
   - Must show confidence and say when the evidence is weak
   - Must not invent raga facts; if the knowledge base lacks it, it says so
   - Must not claim authority a guru would have; it presents itself as a study aid
5. **Optional audio-capable models:** can be explored later for "listening" tasks, but the structured-evidence design stays the primary source of truth

### 8.4 Evaluating the Analyst
- Build a test set of questions with expert-written answers and check factual accuracy and citation correctness
- Track hallucination rate on raga facts, specifically
- Have musicians rate the helpfulness and correctness of feedback on real singing takes
- Treat this like a benchmark: fixed question set, versioned prompts and models, regression tests when anything changes

---

## 9. Knowledge Base and Books: Does It Make Sense?

**Short answer: yes for the knowledge base, no for "fetch all the books."** A well-built, curated, cited knowledge base makes the AI far more accurate. But bulk-collecting books is the wrong goal, for legal and practical reasons.

### 9.1 Why not "fetch everything"
- **Copyright:** most modern books on raga and theory are still protected. Scraping or ingesting them, especially from unofficial copies, is infringement, and putting their text in a product is risky. Do not use pirated sources.
- **Quality:** an AI reading hundreds of books can mix conflicting gharana opinions and produce a confident but muddled answer
- **Scanned books are messy:** old Devanagari and Sanskrit scans need heavy OCR cleanup and expert checking
- **Structured beats unstructured:** what the app needs most is a clean database (raga name, notes, vadi, time, pakad), not a pile of PDF text

### 9.2 The better approach, in layers

**Layer 1: Structured raga database (most valuable)**
Hand-curated entries (the Section 5.1 fields) with a source citation on every field. Start with 30 ragas and grow. A music teacher reviews entries before they go live.

**Layer 2: Glossary of terms**
Ornaments, tala names, thaats, swara names, performance sections. Each with a definition, source, and audio example.

**Layer 3: Text knowledge base (for the AI to retrieve and cite)**
Only from sources you may legally use:
- **Public domain works:** very old classical treatises and the older works of authors whose copyright has expired. Examples to investigate: Bharata's *Natyashastra*, Sharngadeva's *Sangita Ratnakara*, and V. N. Bhatkhande's works (he died in 1936, so his original works are likely in the public domain in India, but verify per work and per country, and note that *modern translations or commentaries* may have their own copyright)
- **Open-access academic research:** papers from music-information-retrieval research on Indian art music, open theses, and dataset documentation
- **Permissively licensed or openly published references:** where the license clearly permits reuse
- **Books you or your users own or license:** for personal, private study, a user can add their own legally obtained books to a personal, private library the AI can search. The app should not redistribute them.
- **Permissioned content:** invite teachers, authors and institutions to contribute material or license it, which also improves quality

**Layer 4: Bibliography without ingestion**
For copyrighted standard references, keep a *recommended reading list* with titles, authors and what each is good for, linking to where users can legally obtain them. The AI can say "see chapter on Yaman in [book]" without copying its text. Well-known modern references to consider listing (verify details before publishing): Joep Bor's *The Raga Guide*; Nazir Jairazbhoy's *The Rags of North Indian Music*; Ashok Ranade's writings on Hindustani music; Vamanrao Deshpande's *Indian Musical Traditions*; Bhatkhande's *Hindustani Sangeet Paddhati* and *Kramik Pustak Malika*.

### 9.3 Practical handling of the text
- Store every chunk with title, author, edition, page/section and license status
- Show citations in every AI answer ("Source: Bhatkhande, Kramik Pustak Malika, vol. 2") and short quotes only where the license allows
- Use a **conflict policy:** when sources disagree (gharana or author), present both views instead of picking silently
- Keep Devanagari and transliterated names indexed together so searches work for both "भैरवी" and "Bhairavi"
- Plan for expert review: a musician checks the top 100 most-queried entries first

---

## 10. Additional Features (to make it complete)

**Analysis extras**
- Raga similarity map: ragas that sound alike, with differences explained
- Detect **raga change inside a song** (ragamalika / modulation) with a timeline
- Bandish structure: *sthayi/mukhda* and *antara*, *alap*, *taan* sections
- **Song-to-raga search:** "find film songs in Yaman" using your analysed library
- Western analysis in parallel: chords, scale degrees, borrowed notes, so cross-genre songs make sense
- Instrument-specific modes: sitar, sarod, flute, harmonium, violin, and so on (different ornament vocabulary and pitch behaviour)

**Learning extras**
- Structured lessons: swara basics, alankars (practice patterns), thaats, simple ragas, then ornaments
- Alankar and **paltas** generator in any raga and tala
- Ear-training quizzes: identify the raga, the swara, the ornament
- Call-and-response with a virtual guru phrase
- Practice journal with AI feedback summaries

**Community and creation**
- Teacher accounts to assign songs, ragas and drills and review recordings
- Share annotated analyses (only metadata, not copyrighted audio)
- Export: sargam notation, MIDI with pitch-bend (for ornaments), MusicXML, and a PDF study sheet per song
- Ornament-preserving MIDI export so DAWs can reproduce meend and gamak shapes

**Language and access**
- UI and terms in English, Hindi (Devanagari), plus transliteration; later Marathi, Bengali, Tamil, Telugu, Kannada
- Voice-based interaction with the AI for hands-free practice

---

## 11. Data and Evaluation Plan

| Component | How to measure | Target idea |
|---|---|---|
| Tonic detection | Accuracy against annotated Sa (allow octave-equivalent errors separately) | Very high before anything else is trusted |
| Swara labelling | Frame and note-level accuracy vs. expert transcriptions | Report separately for clean and noisy audio |
| Ornament detection | Precision/recall per ornament type, human-agreement ceiling | Measure human agreement first |
| Raga recognition | Top-1 and top-3 accuracy, confusion matrix on similar ragas | Report on classical vs. film songs separately |
| Tala detection | Cycle length and sam accuracy | Compare with annotated sam positions |
| AI Analyst | Factual accuracy, citation correctness, user ratings | Fixed expert question set |
| End-to-end | Musician review of full reports | Qualitative panel monthly |

**Honest reporting:** publish performance per genre (classical, light classical, film, fusion), since numbers on clean classical recordings will not carry over to film songs.

**Data ethics:** use datasets under their licenses, credit sources, and never train or publish from audio you lack rights to.

---

## 12. Roadmap

**Phase 2A: Foundations (3–4 weeks)**
Tonic detection, swara labelling relative to Sa, sargam notation view, pitch-class histogram view, glossary v1.

**Phase 2B: Ornaments (3–4 weeks)**
Rule-based detection for vibrato, meend, kan, andolan, gamak, murki, khatka; tagged pitch-contour UI; first musician validation round.

**Phase 2C: Raga Recognition (4–6 weeks)**
Raga database (first 30 ragas, reviewed by a teacher), template-based identification, phrase search, evidence report; evaluate on classical and film test sets.

**Phase 2D: Tala and Raga-Aware Coaching (3–4 weeks)**
Tala/sam detection, tanpura and tabla generator, raga-grammar scoring, pakad drills.

**Phase 2E: AI Analyst (4 weeks)**
Structured-evidence interface, retrieval over the knowledge base with citations, tool calls to the pipeline, evaluation set, guardrails.

**Phase 2F: Learned models and expansion (ongoing)**
Learned ornament and raga models, Carnatic track, more ragas, instrument modes, teacher tools.

Rough total: about 4–6 months for one focused builder after Phase 1; the main bottlenecks are expert-labelled data and teacher review, not code.

---

## 13. Risks

- **Label disagreement among experts** limits achievable accuracy; budget time for a human-agreement study
- **Poor source separation on classical recordings** (tanpura, harmonium, tabla bleed)
- **AI overconfidence** about raga facts; mitigated with citations, a curated database and confidence display
- **Legal exposure** from books, recordings and datasets; mitigate with public-domain, open-access, licensed and user-owned content only
- **Cultural accuracy:** involve practising musicians early, avoid flattening gharana differences, show multiple valid views
- **Scope creep:** Carnatic, instruments and all-raga coverage can swallow the project; stage them

---

## 14. Decisions Needed

1. Hindustani only first, or Hindustani and Carnatic together?
2. Primary audience: learners and singers, musicians and teachers, or researchers?
3. Do you have access to a teacher or musician to validate raga entries and ornament labels? (This is the single biggest quality lever.)
4. Which songs should be the first test set: classical recordings, film songs, or both?
5. Should the AI Analyst run in the cloud, or locally for privacy?
6. Is the book idea for personal study (a private library users add) or for a shared product? That decides the whole legal approach.

---

## 15. Cross-Referenced Ecosystem & Technical Documentation

For in-depth technical analysis, source code references, benchmarks, and product comparisons supporting this plan, refer to:
* 🏆 **[Finalized Product Blueprint & Consensus Specs](file:///d:/Music/FINALIZED_PRODUCT_BLUEPRINT.md)**: Consensus architecture from the exhaustive design interview, defining the technical moat, core algorithms, edge-cloud split, and 6-phase engineering roadmap.
* 🗺️ **[Master Directory & Architectural Flowchart](file:///d:/Music/INDEX.md)**: Full end-to-end dataflow and comparative research matrix.
* 🏗️ **[System Architecture & Implementation Plan](file:///d:/Music/system_architecture_and_implementation_plan.md)**: Component-by-component engineering design, trade-offs (upsides, downsides, costs), service topologies, and infrastructure budget.
* 🎶 **[Indian Classical MIR Research & Industry Ecosystem](file:///d:/Music/indian_classical_mir_ecosystem.md)**: CompMusic, Saraga, compIAM, Essentia tonic identification, AUTRIM, Riyaz app (MusicMuni), SwarShala, Sur Sadhana, GitHub raga models, and Kaggle datasets.
* 🤖 **[Generative Music AI & Suno Architecture](file:///d:/Music/generative_music_ai.md)**: Suno AI (v3/v3.5/v4, Bark), Udio, Beatoven.ai (Indian AI background music), YuE (open-source lyrics-to-full-song), MusicGen, AudioCraft, RVC singing voice conversion, and Virtual Guru integration.
* ⚙️ **[Audio Pipeline, Pitch Tracking & Microtonal Calibration](file:///d:/Music/audio_pipeline_and_tooling.md)**: BS-Roformer, UVR5, torchcrepe, RMVPE, Spotify Basic Pitch, 22-Shruti mathematical ratios table, DTW pakad search, and 14-bit pitch bend MIDI export.
* 📚 **[Academic Research Compendium & Papers](file:///d:/Music/research_compendium_and_papers.md)**: Chordia & Rae (PCD/PCDD), Gulati et al. (TDMS), Madhusudhan et al. (DeepSRGM), Salamon (Tonic), Srinivasamurthy (Tala DBNs), Ranjani (Quantization), Gowriprasad (Gharanas), and empirical shruti science.
* 🔬 **[3,257-Paper Curation & Implementation Mappings](file:///d:/Music/research_papers_curation_and_applications.md)**: Automated harvest of 3,257 papers from OpenAlex, filtering 2,585 non-technical collisions, retaining 672 high-value MIR papers, and mapping top algorithms directly to Song Lab's components. Supported by machine-readable dataset: [curated_research_papers.json](file:///d:/Music/data/curated_research_papers.json).
* 🧠 **[AI Analyst & RAG Knowledge Architecture](file:///d:/Music/ai_analyst_and_rag_architecture.md)**: Multi-agent hierarchy, JSON Evidence schema, Raga Knowledge Graph, Bhatkhande RAG index, gharana conflict resolution, and anti-hallucination guardrails.
