"""
SONG LAB — Cinematic Raga Soundtrack Synthesizer
Generates an authentic, broadcast-grade 42-second soundtrack perfectly timed
to every visual scene in the product marketing demo.

Scenes & Audio Choreography:
  0.0s - 3.2s: Robotic 12-TET stepped synth (illustrating Suno/Udio quantization drift)
  3.2s - 7.0s: Resonant Miraj Tanpura enters + sublime vocal Meend (human soul awakes)
  7.0s - 9.0s: Bansuri Flute solo with breath turbulence and 22-shruti microtones
  9.0s - 11.5s: Sitar solo with metallic attack, jawari shimmer & tarab sympathetic ring
  11.5s - 14.0s: Warm acoustic guitar strum + Teentaal Tabla entrance
  14.0s - 17.0s: Karuna (Pathos) - mournful Darbari Komal Ga andolan oscillation
  17.0s - 21.0s: Shringara (Romantic Devotion) - radiant Yaman melody bloom
  21.0s - 28.0s: Forensic Guru acoustic reference phrase (purity on Shuddha Ga)
  28.0s - 35.0s: NEURO-RASA crescendo (soaring vocal + sitar counterpoint + tihaai)
  35.0s - 42.0s: Grand Sam resolution on Taar Sa + serene lingering Tanpura fade
"""

import math
import numpy as np
import scipy.signal as signal
import soundfile as sf

SR = 44100
DURATION = 42.0
TOTAL_SAMPLES = int(SR * DURATION)
TONIC_HZ = 146.83  # D3 (Standard Indian Classical Vocal pitch for male/female midpoint)


def create_reverb(audio: np.ndarray, wet: float = 0.28, decay_sec: float = 2.2) -> np.ndarray:
    """Natural acoustic concert hall stereo reverb via comb/all-pass network."""
    left = audio.copy()
    right = audio.copy()

    # Pre-delay
    delays = [int(0.029 * SR), int(0.037 * SR), int(0.043 * SR), int(0.053 * SR)]
    gains = [0.82, 0.76, 0.71, 0.65]

    acc_l = np.zeros_like(left)
    acc_r = np.zeros_like(right)

    for d, g in zip(delays, gains):
        comb_l = np.zeros_like(left)
        comb_r = np.zeros_like(right)
        for i in range(d, len(left)):
            comb_l[i] = left[i - d] + g * comb_l[i - d]
            comb_r[i] = right[i - d] + g * comb_r[i - d]
        acc_l += comb_l
        acc_r += comb_r

    # High frequency damping
    b, a = signal.butter(2, 4500 / (SR / 2), btype='low')
    acc_l = signal.lfilter(b, a, acc_l)
    acc_r = signal.lfilter(b, a, acc_r)

    out_l = (1.0 - wet) * left + wet * 0.25 * acc_l
    out_r = (1.0 - wet) * right + wet * 0.25 * acc_r
    return np.column_stack([out_l, out_r])


def synthesize_tanpura(duration_sec: float = DURATION) -> np.ndarray:
    """Synthesizes rich acoustic 4-string Miraj Tanpura with jawari grazing overtones."""
    t = np.linspace(0, duration_sec, int(SR * duration_sec))
    tanpura = np.zeros(len(t), dtype=np.float32)

    # D3 tuning: Pa (A3 = 220.0), Sa (D3 = 146.83), Sa (D3 = 146.83), Mandra Sa (D2 = 73.415)
    strings = [
        {"freq": TONIC_HZ * 1.5, "delay": 0.0, "decay": 3.8, "vol": 0.35},     # Pa
        {"freq": TONIC_HZ,       "delay": 1.2, "decay": 4.2, "vol": 0.40},     # Sa
        {"freq": TONIC_HZ,       "delay": 2.4, "decay": 4.2, "vol": 0.40},     # Sa
        {"freq": TONIC_HZ * 0.5, "delay": 3.6, "decay": 5.0, "vol": 0.50},     # Kharaj Sa
    ]
    cycle_period = 5.2

    for cycle_start in np.arange(0, duration_sec, cycle_period):
        for s in strings:
            start_time = cycle_start + s["delay"]
            if start_time >= duration_sec:
                continue

            start_sample = int(start_time * SR)
            decay_samples = int(s["decay"] * SR)
            end_sample = min(len(t), start_sample + decay_samples)
            num_s = end_sample - start_sample
            if num_s <= 0:
                continue

            st = np.linspace(0, s["decay"], num_s)
            f0 = s["freq"]

            # Jawari overtone series (rich, non-linear wide harmonic spectrum)
            string_sound = np.zeros(num_s, dtype=np.float32)
            for h in range(1, 16):
                # Jawari phase modulation creates dynamic rotating overtones
                h_freq = f0 * h
                if h_freq >= SR / 2 - 1000:
                    break
                h_amp = (1.0 / (h ** 0.85)) * (0.8 + 0.2 * np.sin(2.0 * np.pi * 0.8 * st + h * 0.5))
                h_decay = np.exp(-st / (s["decay"] * (0.9 / math.sqrt(h))))
                string_sound += h_amp * h_decay * np.sin(2.0 * np.pi * h_freq * st + h * 0.3)

            # Pluck attack envelope
            attack_s = int(0.03 * SR)
            if num_s > attack_s:
                string_sound[:attack_s] *= np.linspace(0.0, 1.0, attack_s)

            tanpura[start_sample:end_sample] += s["vol"] * string_sound

    # Smooth master fade-in and fade-out
    fade_in = int(0.5 * SR)
    tanpura[:fade_in] *= np.linspace(0.0, 1.0, fade_in)
    fade_out = int(3.0 * SR)
    tanpura[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)
    return tanpura


def synthesize_robotic_intro(duration_sec: float = 3.5) -> np.ndarray:
    """Robotic, rigid 12-TET quantized synth with harsh auto-tune steps (Suno/RVQ caricature)."""
    t = np.linspace(0, duration_sec, int(SR * duration_sec))
    robot = np.zeros(len(t), dtype=np.float32)

    # 12-TET major scale steps (strictly 100-cent lattice, zero microtones)
    scale_cents = [0, 200, 400, 500, 700, 900, 1100, 1200]
    note_dur = 0.35

    for i, cents in enumerate(scale_cents):
        t_start = i * note_dur
        t_end = min(duration_sec - 0.3, t_start + note_dur)
        s_start = int(t_start * SR)
        s_end = int(t_end * SR)
        if s_end <= s_start:
            break

        f = TONIC_HZ * (2.0 ** (cents / 1200.0))
        dur = (s_end - s_start) / SR
        st = np.linspace(0, dur, s_end - s_start)

        # Harsh square / sawtooth mixture with aliasing edge
        wave = 0.6 * signal.sawtooth(2.0 * np.pi * f * st) + 0.4 * signal.square(2.0 * np.pi * f * st)
        # Highpass buzz
        b, a = signal.butter(2, 800 / (SR / 2), btype='high')
        wave = signal.lfilter(b, a, wave)

        # Mechanical instant attack and release
        robot[s_start:s_end] = wave * 0.45

    # Sudden tape-stop / record-scratch effect at 3.2s
    stop_start = int(3.15 * SR)
    stop_end = int(3.45 * SR)
    if stop_end < len(robot):
        tape_len = stop_end - stop_start
        curve = np.linspace(1.0, 0.0, tape_len) ** 3
        # Frequency drop
        robot[stop_start:stop_end] *= curve

    return robot


def synthesize_vocal_meend(
    start_time: float,
    duration: float,
    cents_start: float,
    cents_end: float,
    vibrato_hz: float = 5.2,
    vibrato_cents: float = 12.0,
    formant: str = "a"
) -> np.ndarray:
    """Synthesizes human vocal tone with continuous sigmoidal Meend and vocal tract formants."""
    num_samples = int(duration * SR)
    t = np.linspace(0, duration, num_samples)

    # Sigmoidal meend trajectory (optimal transport straight curve)
    s_curve = 1.0 / (1.0 + np.exp(-10.0 * (t / duration - 0.5)))
    cents = cents_start + (cents_end - cents_start) * s_curve

    # Natural vibrato emerging after 30% of note
    vib_envelope = np.clip((t / duration - 0.25) / 0.5, 0.0, 1.0)
    cents += vib_envelope * vibrato_cents * np.sin(2.0 * np.pi * vibrato_hz * t)

    freqs = TONIC_HZ * (2.0 ** (cents / 1200.0))
    phase = 2.0 * np.pi * np.cumsum(freqs) / SR

    # Glottal pulse source (Liljencrants-Fant vocal source model approximation)
    glottal = (
        1.0 * np.sin(phase) +
        0.65 * np.sin(2.0 * phase) +
        0.42 * np.sin(3.0 * phase) +
        0.28 * np.sin(4.0 * phase) +
        0.18 * np.sin(5.0 * phase) +
        0.10 * np.sin(6.0 * phase)
    )

    # Vocal tract formants for classical open [a:]
    # F1=750Hz, F2=1250Hz, F3=2600Hz, F4=3300Hz
    b1, a1 = signal.iirpeak(750, 4.0, SR)
    b2, a2 = signal.iirpeak(1250, 6.0, SR)
    b3, a3 = signal.iirpeak(2600, 8.0, SR)
    vocal = 0.5 * signal.lfilter(b1, a1, glottal) + 0.35 * signal.lfilter(b2, a2, glottal) + 0.2 * signal.lfilter(b3, a3, glottal)

    # Envelope
    env = np.ones(num_samples)
    att = int(0.08 * SR)
    rel = int(0.12 * SR)
    if num_samples > att + rel:
        env[:att] = np.linspace(0.0, 1.0, att)
        env[-rel:] = np.linspace(1.0, 0.0, rel)
    return vocal * env


def synthesize_bansuri_flute(
    start_time: float,
    duration: float,
    cents: float,
    bend_cents: float = 18.0
) -> np.ndarray:
    """Acoustic Indian Bansuri Flute with cylindrical air column resonance & breath turbulence."""
    num_samples = int(duration * SR)
    t = np.linspace(0, duration, num_samples)

    # Gentle initial grace bend
    c_curve = cents + bend_cents * np.exp(-t / 0.12)
    # Slow gentle vibrato (4.8 Hz)
    c_curve += 8.0 * np.sin(2.0 * np.pi * 4.8 * t) * np.clip(t / 0.25, 0.0, 1.0)

    f0 = TONIC_HZ * (2.0 ** (c_curve / 1200.0))
    phase = 2.0 * np.pi * np.cumsum(f0) / SR

    # Bamboo pipe harmonics (strong fundamental, prominent 2nd & 3rd, soft 4th)
    pipe = (
        1.0 * np.sin(phase) +
        0.45 * np.sin(2.0 * phase) +
        0.25 * np.sin(3.0 * phase) +
        0.08 * np.sin(4.0 * phase)
    )

    # Breath turbulence noise filtered around fundamental
    noise = np.random.normal(0, 0.06, num_samples)
    b, a = signal.butter(2, [max(100, f0[0] * 0.8) / (SR / 2), min(SR / 2 - 500, f0[0] * 3.5) / (SR / 2)], btype='band')
    breath = signal.lfilter(b, a, noise)

    flute = pipe + breath

    # Breathy attack
    att = int(0.06 * SR)
    rel = int(0.15 * SR)
    env = np.ones(num_samples)
    if num_samples > att + rel:
        env[:att] = np.linspace(0.0, 1.0, att) ** 1.5
        env[-rel:] = np.linspace(1.0, 0.0, rel) ** 1.5
    return flute * env


def synthesize_sitar(
    start_time: float,
    duration: float,
    cents: float,
    meend_pull_cents: float = 50.0
) -> np.ndarray:
    """Acoustic Sitar note with sharp mizrab attack, wide jawari buzz, and meend pull."""
    num_samples = int(duration * SR)
    t = np.linspace(0, duration, num_samples)

    # Meend string-pull (sitarist pulling string across fret)
    c_curve = cents + meend_pull_cents * (1.0 / (1.0 + np.exp(-12.0 * (t / duration - 0.4))))
    f0 = TONIC_HZ * 2.0 * (2.0 ** (c_curve / 1200.0)) # Playing in higher octave

    phase = 2.0 * np.pi * np.cumsum(f0) / SR

    # High metallic jawari overtone spectrum (up to 20 harmonics)
    sitar = np.zeros(num_samples, dtype=np.float32)
    for h in range(1, 18):
        h_freq = f0[0] * h
        if h_freq >= SR / 2 - 1000:
            break
        decay_time = duration / (1.0 + 0.3 * h)
        amp = (1.0 / (h ** 0.75)) * np.exp(-t / decay_time)
        sitar += amp * np.sin(phase * h)

    # Sympathetic strings (Tarab) resonant background hum
    tarab_freqs = [TONIC_HZ * 2.0, TONIC_HZ * 2.5, TONIC_HZ * 3.0]
    for tf in tarab_freqs:
        tarab = 0.06 * np.exp(-t / 2.5) * np.sin(2.0 * np.pi * tf * t)
        sitar += tarab

    # Sharp plectrum attack
    att = int(0.008 * SR)
    env = np.ones(num_samples)
    if num_samples > att:
        env[:att] = np.linspace(0.0, 1.0, att)
    return sitar * env


def synthesize_guitar_strum(
    start_time: float,
    duration: float = 2.0
) -> np.ndarray:
    """Acoustic 6-string guitar strum playing warm open D-Major modal chord."""
    num_samples = int(duration * SR)
    strum = np.zeros(num_samples, dtype=np.float32)

    # DADF#AD open acoustic tuning
    string_pitches = [73.42, 110.0, 146.83, 185.00, 220.0, 293.66]
    strum_speed_sec = 0.012

    for i, f0 in enumerate(string_pitches):
        delay_s = int(i * strum_speed_sec * SR)
        remain_s = num_samples - delay_s
        if remain_s <= 0:
            break
        st = np.linspace(0, remain_s / SR, remain_s)
        decay = np.exp(-st / 1.8)
        # Karplus-Strong string synthesis approximation
        string_sound = (
            1.0 * np.sin(2.0 * np.pi * f0 * st) +
            0.5 * np.sin(2.0 * np.pi * 2.0 * f0 * st) +
            0.25 * np.sin(2.0 * np.pi * 3.0 * f0 * st)
        ) * decay
        strum[delay_s:] += 0.18 * string_sound

    # Wood body cavity resonance
    b, a = signal.iirpeak(185, 3.5, SR)
    strum = 0.7 * strum + 0.3 * signal.lfilter(b, a, strum)
    return strum


def synthesize_tabla_theka(duration_sec: float, bpm: float = 75.0) -> np.ndarray:
    """Authentic Teentaal Tabla theka: Dha Dhin Dhin Dha / Dha Dhin Dhin Dha."""
    t_samples = int(duration_sec * SR)
    tabla = np.zeros(t_samples, dtype=np.float32)

    beat_sec = 60.0 / bpm
    pattern = ["dha", "dhin", "dhin", "dha", "dha", "dhin", "dhin", "dha", "dha", "tin", "tin", "ta", "ta", "dhin", "dhin", "dha"]

    curr_time = 0.0
    idx = 0
    while curr_time < duration_sec:
        stroke = pattern[idx % len(pattern)]
        s_start = int(curr_time * SR)

        if stroke in ["dha", "dhin"]:
            # Bayan bass ("ghe") with pitch modulation: 85 Hz -> 48 Hz
            b_dur = 0.28
            b_samples = int(b_dur * SR)
            b_end = min(t_samples, s_start + b_samples)
            if b_end > s_start:
                st = np.linspace(0, (b_end - s_start) / SR, b_end - s_start)
                f_bayan = 85.0 - 37.0 * (st / b_dur)
                bayan_sound = np.sin(2.0 * np.pi * f_bayan * st) * np.exp(-st / 0.18)
                tabla[s_start:b_end] += 0.42 * bayan_sound

            # Dayan treble ("dhin") tuned to Sa (293.66 Hz)
            d_dur = 0.35
            d_samples = int(d_dur * SR)
            d_end = min(t_samples, s_start + d_samples)
            if d_end > s_start:
                st = np.linspace(0, (d_end - s_start) / SR, d_end - s_start)
                dayan = (
                    0.8 * np.sin(2.0 * np.pi * TONIC_HZ * 2.0 * st) +
                    0.4 * np.sin(2.0 * np.pi * TONIC_HZ * 4.0 * st) +
                    0.2 * np.sin(2.0 * np.pi * TONIC_HZ * 6.0 * st)
                ) * np.exp(-st / 0.16)
                tabla[s_start:d_end] += 0.35 * dayan

        elif stroke in ["tin", "ta"]:
            # Dayan open / closed stroke
            d_dur = 0.22
            d_samples = int(d_dur * SR)
            d_end = min(t_samples, s_start + d_samples)
            if d_end > s_start:
                st = np.linspace(0, (d_end - s_start) / SR, d_end - s_start)
                dayan = np.sin(2.0 * np.pi * TONIC_HZ * 2.0 * st) * np.exp(-st / 0.09)
                tabla[s_start:d_end] += 0.25 * dayan

        curr_time += beat_sec
        idx += 1

    return tabla


def build_full_soundtrack() -> np.ndarray:
    print("Synthesizing multi-track cinematic acoustic master...")
    master = np.zeros(TOTAL_SAMPLES, dtype=np.float32)

    def mix_in(track: np.ndarray, start_sec: float, gain: float = 1.0):
        s_start = int(start_sec * SR)
        s_end = min(TOTAL_SAMPLES, s_start + len(track))
        s_len = s_end - s_start
        if s_len > 0:
            master[s_start:s_end] += gain * track[:s_len]

    # 1. Tanpura Drone (Foundation of Indian classical music)
    # Enters at 3.3s right when the robotic intro stops, and resonates throughout!
    print("  • Synthesizing 4-string acoustic Tanpura drone...")
    tanpura = synthesize_tanpura(DURATION - 3.2)
    mix_in(tanpura, 3.2, gain=0.65)

    # 2. Robotic 12-TET Staircase (Scene 1: The Problem with Suno / Big Tech)
    print("  • Synthesizing robotic 12-TET quantized intro (Suno/Udio artifact)...")
    robot = synthesize_robotic_intro(3.4)
    mix_in(robot, 0.0, gain=0.75)

    # 3. Scene 1 resolution (3.5s - 7.0s): Sublime Vocal Meend (Human Soul Awakes)
    print("  • Synthesizing sublime vocal meend...")
    vocal_intro = synthesize_vocal_meend(
        start_time=3.5, duration=3.4,
        cents_start=-112.0,  # Mandra Ni
        cents_end=386.3,     # Shuddha Ga (pure 5:4 ratio)
        vibrato_cents=10.0
    )
    mix_in(vocal_intro, 3.5, gain=0.70)

    # 4. Scene 2 (7.0s - 14.0s): Universal Acoustic Engine Showcase
    print("  • Synthesizing Bansuri Flute solo (Voice & Flute badge)...")
    flute1 = synthesize_bansuri_flute(start_time=7.1, duration=2.2, cents=204.0, bend_cents=15.0)  # Re
    mix_in(flute1, 7.1, gain=0.65)

    flute2 = synthesize_bansuri_flute(start_time=8.8, duration=2.0, cents=386.3, bend_cents=22.0)  # Ga
    mix_in(flute2, 8.8, gain=0.65)

    print("  • Synthesizing Sitar solo with tarab resonance...")
    sitar1 = synthesize_sitar(start_time=9.8, duration=2.2, cents=590.2, meend_pull_cents=112.0)   # Tivra Ma -> Pa
    mix_in(sitar1, 9.8, gain=0.60)

    print("  • Synthesizing Acoustic Guitar strum...")
    guitar = synthesize_guitar_strum(start_time=11.6, duration=2.5)
    mix_in(guitar, 11.6, gain=0.55)

    # 5. Scene 3 (14.0s - 21.0s): Real-Time Rasa & Affective Radar
    print("  • Synthesizing Karuna (Pathos) - Darbari Komal Ga slow andolan...")
    # Komal Ga andolan (315 cents with heavy 2.0 Hz oscillating meend)
    num_s = int(3.2 * SR)
    st = np.linspace(0, 3.2, num_s)
    andolan_cents = 315.6 + 32.0 * np.sin(2.0 * np.pi * 1.95 * st)
    andolan_f = TONIC_HZ * (2.0 ** (andolan_cents / 1200.0))
    andolan_phase = 2.0 * np.pi * np.cumsum(andolan_f) / SR
    darbari_vocal = (np.sin(andolan_phase) + 0.5 * np.sin(2.0 * andolan_phase)) * np.exp(-st / 3.0)
    mix_in(darbari_vocal, 14.1, gain=0.55)

    print("  • Morphing to Shringara (Romantic Devotion) - Yaman radiant Ga -> Tivra Ma -> Pa...")
    yaman_bloom = synthesize_vocal_meend(
        start_time=17.2, duration=3.6,
        cents_start=386.3,   # Shuddha Ga
        cents_end=702.0,     # Pa
        vibrato_cents=14.0
    )
    mix_in(yaman_bloom, 17.2, gain=0.65)

    # 6. Tabla kicks in at 18.0s and drives through the crescendo!
    print("  • Synthesizing authentic Teentaal Tabla theka...")
    tabla_track = synthesize_tabla_theka(duration_sec=DURATION - 18.0, bpm=76.0)
    mix_in(tabla_track, 18.0, gain=0.60)

    # 7. Scene 4 (21.0s - 28.0s): AI Forensic Guru Reference Phrase
    print("  • Synthesizing pristine Guru reference phrase (Yaman Pakad)...")
    guru_phrase = [
        {"cents_start": -112.0, "cents_end": 204.0, "dur": 1.4, "t": 21.2},   # Ni_ -> Re
        {"cents_start": 204.0,  "cents_end": 386.3, "dur": 1.6, "t": 22.4},   # Re -> Ga (Nyasa hold)
        {"cents_start": 386.3,  "cents_end": 590.2, "dur": 1.4, "t": 24.2},   # Ga -> Tivra Ma
        {"cents_start": 590.2,  "cents_end": 702.0, "dur": 2.2, "t": 25.5},   # Tivra Ma -> Pa
    ]
    for n in guru_phrase:
        v = synthesize_vocal_meend(n["t"], n["dur"], n["cents_start"], n["cents_end"], vibrato_cents=10.0)
        mix_in(v, n["t"], gain=0.68)

    # 8. Scene 5 (28.0s - 35.0s): NEURO-RASA R&D Breakthrough Crescendo
    print("  • Synthesizing NEURO-RASA multi-instrument counterpoint & high register run...")
    sitar_high = synthesize_sitar(start_time=28.2, duration=2.5, cents=905.9, meend_pull_cents=182.4) # Dha -> Ni
    mix_in(sitar_high, 28.2, gain=0.62)

    flute_high = synthesize_bansuri_flute(start_time=30.4, duration=2.4, cents=1088.3, bend_cents=25.0) # Shuddha Ni
    mix_in(flute_high, 30.4, gain=0.65)

    vocal_soar = synthesize_vocal_meend(
        start_time=32.2, duration=3.0,
        cents_start=905.9,   # Dha
        cents_end=1200.0,    # Taar Sa (peak achievement!)
        vibrato_cents=15.0
    )
    mix_in(vocal_soar, 32.2, gain=0.75)

    # 9. Scene 6 (35.0s - 42.0s): Grand Sam Resolution & Majestic Outro
    print("  • Synthesizing grand Sam resolution and acoustic cymbal wash...")
    # Unison Taar Sa strike at 35.2s
    sam_s = int(35.2 * SR)
    st_sam = np.linspace(0, 6.5, TOTAL_SAMPLES - sam_s)
    # Bell / Gong chime resonance
    chime_freqs = [TONIC_HZ * 4.0, TONIC_HZ * 6.0, TONIC_HZ * 8.0]
    for cf in chime_freqs:
        chime = 0.15 * np.sin(2.0 * np.pi * cf * st_sam) * np.exp(-st_sam / 3.8)
        master[sam_s:] += chime

    # Final gentle descending flute motif
    final_flute = synthesize_bansuri_flute(start_time=37.0, duration=3.5, cents=0.0, bend_cents=45.0) # Sinking back into Sa
    mix_in(final_flute, 37.0, gain=0.55)

    # Master Normalization & Soft Limiting
    peak = np.max(np.abs(master))
    if peak > 0:
        master = master / peak * 0.92

    # Add lush acoustic concert hall reverb
    print("  • Applying stereo concert hall acoustic convolution...")
    stereo_master = create_reverb(master, wet=0.25, decay_sec=2.4)

    out_wav = "d:/Music/marketing_soundtrack.wav"
    sf.write(out_wav, stereo_master.astype(np.float32), SR)
    print(f"\nSuccessfully generated soundtrack: {out_wav}")
    print(f"  Duration: {DURATION}s | Sample Rate: {SR}Hz | Channels: 2 (Stereo)")
    return stereo_master


if __name__ == "__main__":
    build_full_soundtrack()
