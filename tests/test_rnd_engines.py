"""
Unit tests for R&D Chronobiology (Circadian Engine) and Expressive Meend Synthesizer
"""

import pytest
from fastapi.testclient import TestClient
from server import app
from src.circadian_engine import CircadianRagaEngine, PRAHARA_REGISTRY
from src.expressive_synthesizer import ExpressiveMeendSynthesizer

client = TestClient(app)


def test_circadian_prahara_coverage():
    """Verify all 8 Praharas correctly cover the 24-hour circadian cycle."""
    assert len(PRAHARA_REGISTRY) == 8

    test_hours = [
        (7, "Bhairav", 1),
        (10, "Todi", 2),
        (13, "Shuddha Sarang", 3),
        (16, "Bhimpalasi", 4),
        (19, "Marwa", 5),
        (22, "Yaman", 6),
        (1, "Darbari Kanada", 7),
        (4, "Bhairavi", 8),
    ]

    for hour, expected_raga, expected_prahara in test_hours:
        rec = CircadianRagaEngine.get_circadian_recommendation(hour=hour, minute=15)
        assert rec["prahara_number"] == expected_prahara
        assert rec["recommended_raga"] == expected_raga
        assert "biological_phase" in rec
        assert "neuro_correlates" in rec
        assert "drone_tuning" in rec


def test_expressive_meend_generation_yaman():
    """Verify continuous flow-spline meend trajectory for Raga Yaman."""
    res = ExpressiveMeendSynthesizer.generate_trajectory(
        notes=["Sa", "Re", "Ga", "Tivra Ma", "Pa"],
        raga="Yaman",
        tonic_hz=146.83,
        tempo_bpm=60.0,
        meend_expressiveness=0.85
    )

    assert res["raga"] == "Yaman"
    assert res["duration_sec"] > 0
    assert len(res["pitch_trajectory"]) > 100
    assert len(res["audio_wav_base64"]) > 100

    # Ensure continuous cents trajectory without NaN
    for pt in res["pitch_trajectory"]:
        assert not math_isnan(pt["cents"])
        assert not math_isnan(pt["velocity"])
        assert pt["hz"] > 100.0


def test_expressive_meend_darbari_andolan():
    """Verify authentic 2.1 Hz microtonal andolan oscillation in Darbari Kanada."""
    res = ExpressiveMeendSynthesizer.generate_trajectory(
        notes=["Sa", "Komal Ga", "Pa"],
        raga="Darbari Kanada",
        tonic_hz=146.83,
        tempo_bpm=50.0,
        meend_expressiveness=0.9
    )

    # Inspect the Komal Ga region
    ga_points = [p for p in res["pitch_trajectory"] if 0.8 < p["t"] < 2.0]
    assert len(ga_points) > 20

    cents_vals = [p["cents"] for p in ga_points]
    max_c = max(cents_vals)
    min_c = min(cents_vals)
    # Oscillation swing should be present
    assert (max_c - min_c) >= 15.0


def test_fastapi_rnd_endpoints():
    """Test REST API endpoints for circadian raga and expressive contour generation."""
    # 1. Circadian endpoint
    res = client.get("/api/circadian-raga?hour=22&minute=30")
    assert res.status_code == 200
    data = res.json()
    assert data["prahara_number"] == 6
    assert data["recommended_raga"] == "Yaman"

    # 2. Expressive contour endpoint
    res2 = client.post(
        "/api/generate-expressive-contour",
        json={
            "notes": ["Sa", "Re", "Ga"],
            "raga": "Yaman",
            "tonic_hz": 146.83,
            "tempo_bpm": 60.0,
            "meend_expressiveness": 0.85
        }
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert len(data2["pitch_trajectory"]) > 0
    assert "audio_wav_base64" in data2


def math_isnan(val):
    import math
    return math.isnan(val)
