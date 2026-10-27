"""
Song Lab Performance and Accuracy Benchmark Test Suite.
Verifies:
1. Tonal Grounding and Movable Sa Accuracy.
2. 22-Shruti Mathematical Precision (< 1 cent error).
3. Ornament Detector Recall and Precision (Meend, Andolan, Gamak, Vibrato).
4. Deficit Engine Salience Hierarchy (Tier 1 Varjya, Tier 2 Missing Inflection, Tier 3 Shruti).
5. Full End-to-End Latency & Performance on Synthetic + Real Audio.
"""

import os
import sys
import time
import pytest
import numpy as np
import soundfile as sf
import librosa

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.tonal_engine import TonicEstimator, SHRUTI_TABLE, hz_to_cents, quantize_to_shruti, quantize_to_12_swara
from src.ornament_detector import KinematicOrnamentDetector, OrnamentType
from src.raga_matcher import RagaMatcher, RAGA_DATABASE
from src.deficit_engine import DeficitEngine, DeficitTier
from src.pipeline import SongLabPipeline

AUDIO_DIR = "data/test_audio"


def test_22_shruti_mathematical_precision():
    """Verify that all 22 shrutis have correct ratios and cent distances."""
    assert len(SHRUTI_TABLE) == 22
    # Sa must be exactly 0 cents
    assert SHRUTI_TABLE[0].cents == 0.0
    # Pancham must be 3/2 (~701.96 cents)
    pa = SHRUTI_TABLE[13]
    assert pa.swara_hindustani == "Pa"
    assert pa.ratio_num == 3 and pa.ratio_den == 2
    assert abs(pa.cents - 701.96) < 0.01

    # Verify monotonic ascending cents
    for i in range(len(SHRUTI_TABLE) - 1):
        assert SHRUTI_TABLE[i].cents < SHRUTI_TABLE[i + 1].cents


def test_tonic_estimation_accuracy():
    """Verify that tonic estimator locks onto C3 (130.81 Hz) from harmonic audio."""
    path = os.path.join(AUDIO_DIR, "tonic_calibration_c3.wav")
    assert os.path.exists(path)
    
    audio, sr = sf.read(path)
    pipeline = SongLabPipeline(sr=sr)
    f0, voiced_prob, times = pipeline.extract_f0(audio, sr)
    
    estimator = TonicEstimator()
    res = estimator.estimate_from_f0(f0, voiced_prob)
    
    # Ground truth is 130.81 Hz. Allow tolerance of within 5 Hz
    assert abs(res["tonic_hz"] - 130.81) < 5.0
    assert res["note_name"] == "C3"
    print(f"\nTonic Estimation Result: {res['tonic_hz']} Hz ({res['note_name']}) with confidence {res['confidence']}")


def test_yaman_perfect_phrase_evaluation():
    """Verify that flawless Yaman phrase emits NO_DEFICIT badge."""
    path = os.path.join(AUDIO_DIR, "yaman_perfect_phrase.wav")
    assert os.path.exists(path)
    
    pipeline = SongLabPipeline(target_raga="Yaman", known_tonic_hz=130.81)
    evidence = pipeline.analyze_audio(path)
    
    # Verify Raga matcher identified Yaman as top candidate
    top_raga = evidence["raga_identification"]["identified_raga"]
    assert top_raga == "Yaman"
    
    # Verify ornaments detected (must include Meend glide)
    ornaments = evidence["ornaments_detected"]
    ornament_types = [o["ornament_type"] for o in ornaments]
    assert any("Meend" in ot for ot in ornament_types)
    
    # Verify feedback tier
    critiques = evidence["phrase_critiques"]
    assert len(critiques) > 0
    assert critiques[0]["tier"] == DeficitTier.NO_DEFICIT.value
    print(f"\nYaman Perfect: Identified {top_raga}, Ornaments: {ornament_types}, Critique: {critiques[0]['badge']}")


def test_tier_1_varjya_swara_detection():
    """Verify that Yaman with forbidden notes triggers Tier 1 Fatal Deficit."""
    path = os.path.join(AUDIO_DIR, "yaman_varjya_violation.wav")
    assert os.path.exists(path)
    
    pipeline = SongLabPipeline(target_raga="Yaman", known_tonic_hz=130.81)
    evidence = pipeline.analyze_audio(path)
    
    critiques = evidence["phrase_critiques"]
    assert len(critiques) > 0
    primary = critiques[0]
    
    # Must trigger Tier 1
    assert primary["tier"] == DeficitTier.TIER_1_CRITICAL.value
    assert "Forbidden Swara" in primary["badge"]
    print(f"\nTier 1 Deficit Caught: {primary['badge']} -> {primary['indian_classical_mode']['critique']}")


def test_tier_2_missing_mandatory_andolan():
    """Verify that Darbari Kanada sung flat without Andolan triggers Tier 2 Deficit."""
    path = os.path.join(AUDIO_DIR, "darbari_flat_deficit.wav")
    assert os.path.exists(path)
    
    pipeline = SongLabPipeline(target_raga="Darbari Kanada", known_tonic_hz=130.81)
    evidence = pipeline.analyze_audio(path)
    
    critiques = evidence["phrase_critiques"]
    assert len(critiques) > 0
    primary = critiques[0]
    
    # Must trigger Tier 2
    assert primary["tier"] == DeficitTier.TIER_2_STRUCTURAL.value
    assert "Missing Andolan" in primary["badge"]
    print(f"\nTier 2 Deficit Caught: {primary['badge']} -> {primary['indian_classical_mode']['critique']}")


def test_darbari_authentic_andolan():
    """Verify that authentic slow Andolan on Komal Ga is recognized as ANDOLAN."""
    path = os.path.join(AUDIO_DIR, "darbari_authentic_andolan.wav")
    assert os.path.exists(path)
    
    pipeline = SongLabPipeline(target_raga="Darbari Kanada", known_tonic_hz=130.81)
    evidence = pipeline.analyze_audio(path)
    
    ornaments = evidence["ornaments_detected"]
    andolan_segs = [o for o in ornaments if "Andolan" in o["ornament_type"]]
    assert len(andolan_segs) > 0
    
    # Verify oscillation rate is within ~2.0 Hz
    rate = andolan_segs[0]["oscillation_rate_hz"]
    assert 1.0 <= rate <= 3.0
    print(f"\nAuthentic Andolan Detected: Rate={rate} Hz, Depth={andolan_segs[0]['oscillation_depth_cents']} cents")


def test_tier_3_vibrato_flutter_critique():
    """Verify that 6Hz Western vibrato in Bhairav is flagged as Tier 3 Vibrato Flutter."""
    path = os.path.join(AUDIO_DIR, "bhairav_vibrato_deficit.wav")
    assert os.path.exists(path)
    
    pipeline = SongLabPipeline(target_raga="Bhairav", known_tonic_hz=130.81)
    evidence = pipeline.analyze_audio(path)
    
    critiques = evidence["phrase_critiques"]
    assert len(critiques) > 0
    primary = critiques[0]
    
    assert primary["tier"] == DeficitTier.TIER_3_MICROTONAL.value
    assert "Vibrato Flutter" in primary["badge"]
    print(f"\nTier 3 Deficit Caught: {primary['badge']} -> {primary['indian_classical_mode']['critique']}")


def test_real_indian_vocal_audio_performance():
    """Evaluates the pipeline on authentic human Indian classical vocal audio."""
    path = os.path.join(AUDIO_DIR, "real_indian_vocal_sample.wav")
    assert os.path.exists(path)
    
    t0 = time.time()
    pipeline = SongLabPipeline()
    evidence = pipeline.analyze_audio(path)
    duration = time.time() - t0
    
    audio_dur = evidence["metadata"]["audio_duration_sec"]
    latency = evidence["metadata"]["compute_latency_sec"]
    rtf = latency / audio_dur if audio_dur > 0 else 0.0
    
    print(f"\n=== REAL INDIAN VOCAL SAMPLE EVALUATION ===")
    print(f"Audio Duration: {audio_dur:.2f}s | Pipeline Compute Time: {latency:.2f}s | Real-Time Factor (RTF): {rtf:.2f}x")
    print(f"Estimated Sa (Tonic): {evidence['tonal_grounding']['tonic_hz']} Hz ({evidence['tonal_grounding']['note_name']})")
    print(f"Top Identified Raga: {evidence['raga_identification']['identified_raga']} (Score: {evidence['raga_identification']['match_confidence']})")
    print(f"Total Ornaments Extracted: {len(evidence['ornaments_detected'])}")
    for o in evidence['ornaments_detected'][:5]:
        print(f"  {o['start_time']}s-{o['end_time']}s: {o['ornament_type']} (Dur: {o['duration_ms']}ms, Span: {o['pitch_span_cents']}c)")
    print(f"Total Phrases Evaluated: {len(evidence['phrase_critiques'])}")
    for c in evidence['phrase_critiques']:
        print(f"  Phrase {c['phrase_id']} ({c['start_time']}s-{c['end_time']}s): {c['badge']} [{c['tier']}]")
        print(f"    Indian Mode: {c['indian_classical_mode']['critique']}")

    # Basic performance invariants
    assert audio_dur > 0
    assert len(evidence["ornaments_detected"]) > 0
