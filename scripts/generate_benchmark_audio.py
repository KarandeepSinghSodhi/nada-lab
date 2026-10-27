"""
Synthetic Benchmark Audio Generator for Song Lab.
Synthesizes acoustic audio waveforms (WAV) with known ground truth for:
1. Pure harmonic tones for Tonic (Sa) calibration.
2. Authentic Yaman phrase with portamento Meend.
3. Yaman phrase with deliberate Varjya (forbidden) notes (Tier 1 deficit).
4. Darbari Kanada with flat Komal Ga lacking Andolan (Tier 2 deficit).
5. Darbari Kanada with authentic slow 2.0 Hz Andolan.
6. Bhairav phrase with Western Vibrato flutter (Tier 3 deficit).
7. Microtonal intonation drift phrase (Tier 3 deficit).
"""

import os
import numpy as np
import soundfile as sf

OUTPUT_DIR = "data/test_audio"
SR = 22050  # 22.05 kHz standard MIR rate


def synthesize_harmonic_tone(f0_hz_array: np.ndarray, sr: int = SR) -> np.ndarray:
    """
    Synthesizes vocal-like audio with rich harmonic overtones (fundamental + 4 harmonics)
    driven by a continuous instantaneous frequency trajectory f0_hz_array.
    """
    dt = 1.0 / sr
    # Calculate phase by integrating instantaneous frequency
    phase = 2.0 * np.pi * np.cumsum(f0_hz_array) * dt
    
    # 5 Harmonics with vocal formant roll-off
    audio = (
        1.0 * np.sin(phase) +
        0.5 * np.sin(2 * phase) +
        0.25 * np.sin(3 * phase) +
        0.12 * np.sin(4 * phase) +
        0.06 * np.sin(5 * phase)
    )
    
    # Smooth attack and release envelope (20ms ramp)
    env_samples = int(0.02 * sr)
    if len(audio) > 2 * env_samples:
        ramp_up = np.linspace(0, 1, env_samples)
        ramp_down = np.linspace(1, 0, env_samples)
        audio[:env_samples] *= ramp_up
        audio[-env_samples:] *= ramp_down
        
    # Normalize peak amplitude to -3 dB
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = (audio / peak) * 0.7
        
    return audio.astype(np.float32)


def generate_benchmark_suite():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    f_sa = 130.81  # C3 tonic (standard male vocal Sa)
    
    # -------------------------------------------------------------
    # 1. Tonic Drone Calibration Track (Sa = 130.81 Hz, Pa = 196.22 Hz)
    # -------------------------------------------------------------
    dur_sec = 3.0
    t = np.arange(0, dur_sec, 1.0 / SR)
    # Tanpura drone simulation (Sa + Pa + Sa_octave)
    drone = (
        0.4 * np.sin(2 * np.pi * f_sa * t) +
        0.3 * np.sin(2 * np.pi * (f_sa * 1.5) * t) +
        0.3 * np.sin(2 * np.pi * (f_sa * 2.0) * t)
    )
    drone_path = os.path.join(OUTPUT_DIR, "tonic_calibration_c3.wav")
    sf.write(drone_path, drone.astype(np.float32), SR)
    print(f"Generated: {drone_path}")

    # -------------------------------------------------------------
    # 2. Authentic Yaman Phrase (N. - R - G with Meend to P)
    # Notes: N. (-100c), R (200c), G (400c), M (600c), P (702c)
    # -------------------------------------------------------------
    # Timeline:
    # 0.0 - 0.6s: N. (123.47 Hz)
    # 0.6 - 1.2s: R (146.83 Hz)
    # 1.2 - 2.0s: G (164.81 Hz)
    # 2.0 - 2.4s: Meend glide G -> M -> P
    # 2.4 - 3.2s: P (196.00 Hz)
    total_samples = int(3.2 * SR)
    f0_curve = np.zeros(total_samples)
    
    s0 = int(0.0 * SR); s1 = int(0.6 * SR)
    s2 = int(1.2 * SR); s3 = int(2.0 * SR)
    s4 = int(2.4 * SR); s5 = int(3.2 * SR)
    
    f_N = f_sa * (2.0 ** (-100.0 / 1200.0))
    f_R = f_sa * (2.0 ** (204.0 / 1200.0))
    f_G = f_sa * (2.0 ** (386.0 / 1200.0))
    f_P = f_sa * (2.0 ** (702.0 / 1200.0))
    
    f0_curve[s0:s1] = f_N
    f0_curve[s1:s2] = f_R
    f0_curve[s2:s3] = f_G
    f0_curve[s3:s4] = np.linspace(f_G, f_P, s4 - s3)  # Continuous Meend glide
    f0_curve[s4:s5] = f_P
    
    audio_yaman_perfect = synthesize_harmonic_tone(f0_curve)
    p2 = os.path.join(OUTPUT_DIR, "yaman_perfect_phrase.wav")
    sf.write(p2, audio_yaman_perfect, SR)
    print(f"Generated: {p2}")

    # -------------------------------------------------------------
    # 3. Yaman with Tier 1 Varjya Violation (Singing Shuddha Ma & Komal Ga)
    # -------------------------------------------------------------
    f0_yaman_varjya = f0_curve.copy()
    # Replace the G region (1.2 to 2.0s) with Komal Ga (300c) and Shuddha Ma (500c)
    f_g = f_sa * (2.0 ** (316.0 / 1200.0))  # Komal Ga
    f_m = f_sa * (2.0 ** (498.0 / 1200.0))  # Shuddha Ma
    mid = s2 + (s3 - s2) // 2
    f0_yaman_varjya[s2:mid] = f_g
    f0_yaman_varjya[mid:s3] = f_m
    
    audio_yaman_varjya = synthesize_harmonic_tone(f0_yaman_varjya)
    p3 = os.path.join(OUTPUT_DIR, "yaman_varjya_violation.wav")
    sf.write(p3, audio_yaman_varjya, SR)
    print(f"Generated: {p3}")

    # -------------------------------------------------------------
    # 4. Darbari Kanada with Tier 2 Deficit (Flat Komal Ga, No Andolan)
    # S - R - g - R - S
    # -------------------------------------------------------------
    dur_darbari = 3.5
    f0_darbari_flat = np.zeros(int(dur_darbari * SR))
    d0 = int(0.0 * SR); d1 = int(0.7 * SR)
    d2 = int(1.4 * SR); d3 = int(2.5 * SR)
    d4 = int(3.0 * SR); d5 = int(3.5 * SR)
    
    f_S = f_sa
    f_R = f_sa * (2.0 ** (204.0 / 1200.0))
    f_komal_g = f_sa * (2.0 ** (316.0 / 1200.0))
    
    f0_darbari_flat[d0:d1] = f_S
    f0_darbari_flat[d1:d2] = f_R
    f0_darbari_flat[d2:d3] = f_komal_g  # Flat static Komal Ga without Andolan!
    f0_darbari_flat[d3:d4] = f_R
    f0_darbari_flat[d4:d5] = f_S
    
    audio_darbari_flat = synthesize_harmonic_tone(f0_darbari_flat)
    p4 = os.path.join(OUTPUT_DIR, "darbari_flat_deficit.wav")
    sf.write(p4, audio_darbari_flat, SR)
    print(f"Generated: {p4}")

    # -------------------------------------------------------------
    # 5. Darbari Kanada with Authentic Slow Andolan (2.0 Hz, 80c depth)
    # -------------------------------------------------------------
    f0_darbari_authentic = f0_darbari_flat.copy()
    t_andolan = np.arange(d3 - d2) / SR
    # Authentic Darbari Komal Ga slow andolan (2.0 Hz oscillating downward to R)
    cents_mod = 316.0 + 40.0 * np.sin(2 * np.pi * 2.0 * t_andolan)
    f0_darbari_authentic[d2:d3] = f_sa * (2.0 ** (cents_mod / 1200.0))
    
    audio_darbari_auth = synthesize_harmonic_tone(f0_darbari_authentic)
    p5 = os.path.join(OUTPUT_DIR, "darbari_authentic_andolan.wav")
    sf.write(p5, audio_darbari_auth, SR)
    print(f"Generated: {p5}")

    # -------------------------------------------------------------
    # 6. Bhairav with Western Vibrato Flutter (6.0 Hz instead of slow Andolan)
    # -------------------------------------------------------------
    dur_bhairav = 3.0
    f0_bhairav_vibrato = np.zeros(int(dur_bhairav * SR))
    b0 = int(0.0 * SR); b1 = int(0.6 * SR)
    b2 = int(2.2 * SR); b3 = int(3.0 * SR)
    
    f_komal_r = f_sa * (2.0 ** (112.0 / 1200.0))
    f0_bhairav_vibrato[b0:b1] = f_S
    
    # Komal Re sung with 6 Hz western vibrato flutter
    t_vib = np.arange(b2 - b1) / SR
    vib_cents = 112.0 + 25.0 * np.sin(2 * np.pi * 6.0 * t_vib)
    f0_bhairav_vibrato[b1:b2] = f_sa * (2.0 ** (vib_cents / 1200.0))
    f0_bhairav_vibrato[b2:b3] = f_S
    
    audio_bhairav_vib = synthesize_harmonic_tone(f0_bhairav_vibrato)
    p6 = os.path.join(OUTPUT_DIR, "bhairav_vibrato_deficit.wav")
    sf.write(p6, audio_bhairav_vib, SR)
    print(f"Generated: {p6}")

    # -------------------------------------------------------------
    # 7. Microtonal Intonation Deviation (+25 cents sharp on Shuddha Re & Ga)
    # -------------------------------------------------------------
    f0_sharp = f0_curve.copy()
    # Add +25 cents sharp error
    f0_sharp[s1:s3] *= (2.0 ** (25.0 / 1200.0))
    audio_sharp = synthesize_harmonic_tone(f0_sharp)
    p7 = os.path.join(OUTPUT_DIR, "microtonal_deviation.wav")
    sf.write(p7, audio_sharp, SR)
    print(f"Generated: {p7}")

    print("\nSuccessfully generated all 7 benchmark audio files in data/test_audio/!")


if __name__ == "__main__":
    generate_benchmark_suite()
