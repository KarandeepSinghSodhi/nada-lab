import pytest
from fastapi.testclient import TestClient
from server import app
from src.phrase_rasa_engine import PhraseRasaEngine

client = TestClient(app)


def test_phrase_rasa_engine_direct():
    engine = PhraseRasaEngine()
    
    # 1. Yaman phrase trajectory (ascending to Ga, resting on Ga)
    yaman_trajectory = [
        {"t": 0.0, "cents": 0.0},
        {"t": 0.2, "cents": 204.0},
        {"t": 0.5, "cents": 386.3},
        {"t": 0.8, "cents": 386.3},
        {"t": 1.1, "cents": 386.3},
        {"t": 1.4, "cents": 498.0},
        {"t": 1.7, "cents": 590.2},
        {"t": 2.0, "cents": 702.0},
        {"t": 2.3, "cents": 702.0},
        {"t": 2.6, "cents": 702.0}
    ]

    res = engine.analyze_phrase_rasa(
        pitch_trajectory=yaman_trajectory,
        identified_raga="Yaman",
        bpm=76.0
    )

    assert "phrase_level_rasa" in res
    assert res["phrase_level_rasa"] in ["Shanta", "Shringara"]
    assert "valence" in res
    assert "arousal" in res
    assert "circumplex_quadrant" in res
    assert "musicological_critique" in res
    assert len(res["canonical_treatise_citations"]) >= 1


def test_phrase_rasa_endpoint():
    darbari_trajectory = [
        {"t": 0.0, "cents": 0.0},
        {"t": 0.3, "cents": 204.0},
        {"t": 0.6, "cents": 294.0},
        {"t": 0.9, "cents": 290.0},
        {"t": 1.2, "cents": 296.0},
        {"t": 1.5, "cents": 292.0},
        {"t": 1.8, "cents": 204.0},
        {"t": 2.1, "cents": 0.0}
    ]

    response = client.post(
        "/api/analyze-rasa",
        json={
            "pitch_trajectory": darbari_trajectory,
            "identified_raga": "Darbari Kanada",
            "bpm": 60.0
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["phrase_level_rasa"] in ["Karuna", "Shanta", "Veera"]
    assert "kinetic_profile" in data
    assert "canonical_treatise_citations" in data
