"""
Unit tests for AcousticSanitizer:
1. Vocal harmonic isolation & accompaniment bleed scoring.
2. Median octave-jump & vocal fry glitch unwrapping.
3. Tempo-adaptive & Gharana-aware threshold scaling.
"""

import numpy as np
import pytest
from src.acoustic_sanitizer import AcousticSanitizer, StylisticPreset


def test_vocal_harmonic_isolation():
    sanitizer = AcousticSanitizer(sr=22050)
    # Generate 1 sec of 220Hz harmonic sine wave + rhythmic percussion bursts (simulating tabla hits)
    t = np.linspace(0.0, 1.0, 22050)
    vocal_sine = 0.5 * np.sin(2.0 * np.pi * 220.0 * t)
    percussion = np.zeros_like(t)
    # Add regular percussive bursts every 2000 samples
    for hit_idx in range(1000, 20000, 2000):
        percussion[hit_idx:hit_idx + 150] = 1.2 * np.random.randn(150)

    audio = (vocal_sine + percussion).astype(np.float32)

    isolated, bleed_pct = sanitizer.isolate_vocal_harmonics(audio, sr=22050)

    assert len(isolated) == len(audio)
    assert bleed_pct > 6.0
    # Percussive spikes in isolated audio should be attenuated
    assert np.max(np.abs(isolated[1000:1050])) < np.max(np.abs(audio[1000:1050]))


def test_sanitize_octave_glitches():
    sanitizer = AcousticSanitizer()
    # Baseline steady cents contour at 400c (Shuddha Ga)
    cents = np.full(50, 400.0)
    # Inject spurious single-frame +1200c octave doubling glitch at frame 20
    cents[20] = 1600.0  # +1200c jump
    # Inject spurious 2-frame -1200c octave halving glitch at frame 35, 36
    cents[35] = -800.0
    cents[36] = -800.0

    sanitized, glitches_fixed = sanitizer.sanitize_octave_glitches(cents, hop_sec=0.01)

    assert glitches_fixed >= 2
    assert abs(sanitized[20] - 400.0) < 50.0
    assert abs(sanitized[35] - 400.0) < 50.0
    assert abs(sanitized[36] - 400.0) < 50.0


def test_adaptive_thresholds_tempo_scaling():
    # 1. Vilambit (Slow Laya, 50 BPM)
    vilambit = AcousticSanitizer.get_adaptive_thresholds(bpm=50.0, preset=StylisticPreset.KHAYAL_STANDARD)
    assert "Vilambit" in vilambit.laya_category
    assert vilambit.min_steady_duration_ms > 140.0

    # 2. Madhya (Medium Laya, 90 BPM)
    madhya = AcousticSanitizer.get_adaptive_thresholds(bpm=90.0, preset=StylisticPreset.KHAYAL_STANDARD)
    assert "Madhya" in madhya.laya_category
    assert 90.0 <= madhya.min_steady_duration_ms <= 120.0

    # 3. Drut (Fast Laya, 160 BPM)
    drut = AcousticSanitizer.get_adaptive_thresholds(bpm=160.0, preset=StylisticPreset.DRUT_TAAN)
    assert "Drut" in drut.laya_category
    assert drut.min_steady_duration_ms <= 65.0
    assert drut.steady_velocity_threshold >= 180.0

    # 4. Dhrupad
    dhrupad = AcousticSanitizer.get_adaptive_thresholds(bpm=60.0, preset=StylisticPreset.DHRUPAD)
    assert dhrupad.min_steady_duration_ms >= 180.0

def test_separate_stems_and_base64():
    sanitizer = AcousticSanitizer(sr=22050)
    t = np.linspace(0.0, 0.5, 11025)
    sine = 0.4 * np.sin(2.0 * np.pi * 330.0 * t)
    noise = np.zeros_like(t)
    noise[1000:1200] = 1.0 * np.random.randn(200)
    mix = (sine + noise).astype(np.float32)

    res = sanitizer.separate_stems(mix, sr=22050, num_peak_points=40)
    assert "vocal_audio" in res
    assert "accompaniment_audio" in res
    assert "vocal_peaks" in res
    assert "accompaniment_peaks" in res
    assert len(res["vocal_peaks"]) == 40
    assert len(res["accompaniment_peaks"]) == 40

    b64_wav = AcousticSanitizer.audio_to_base64_wav(res["vocal_audio"], sr=22050)
    assert b64_wav.startswith("data:audio/wav;base64,")
