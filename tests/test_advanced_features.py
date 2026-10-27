"""
Automated unit tests for advanced Song Lab features:
1. Raga Similarity, Contrast & Confusion Matrix Engine
2. Pedagogical Alankar & Palta Practice Generator
3. 14-Bit Pitch Bend Continuous MIDI & Sargam Exporter
4. FastAPI Endpoints for Raga Similarity, Alankars, and MIDI Export
"""

import pytest
from fastapi.testclient import TestClient

from src.raga_comparator import RagaComparator
from src.alankar_generator import AlankarGenerator
from src.midi_sargam_exporter import MidiSargamExporter
from server import app

client = TestClient(app)


def test_raga_comparator_yaman_vs_bhupali():
    """Verify detailed distinction between Yaman and its pentatonic offspring Bhupali."""
    comparator = RagaComparator()
    res = comparator.compare_pair("Yaman", "Bhupali")
    assert "metrics" in res
    assert res["metrics"]["scale_jaccard_similarity"] > 0.65
    assert "M" in res["metrics"]["r1_exclusive_swaras"]  # Tivra Ma is in Yaman, not Bhupali
    assert "N" in res["metrics"]["r1_exclusive_swaras"]  # Ni is in Yaman, not Bhupali
    assert res["metrics"]["confusion_risk"] in ["High", "Moderate"]
    assert len(res["discriminating_factors"]) > 0


def test_raga_comparator_find_allied():
    """Verify that allied ragas list includes top matching candidates."""
    comparator = RagaComparator()
    allied = comparator.find_allied_ragas("Yaman", top_k=3)
    assert len(allied) == 3
    names = [r["raga"] for r in allied]
    assert any(n in names for n in ["Bhupali", "Kalyani", "Shuddha Sarang", "Hameer"])


def test_alankar_generator_triad():
    """Verify that Alankar generation produces valid Aroha and Avaroha paltas."""
    gen = AlankarGenerator()
    res = gen.generate_drill(raga_name="Yaman", pattern_key="triad_step", synthesize_audio=True)
    assert res["raga"] == "Yaman"
    assert len(res["arohana_paltas"]) >= 3
    assert len(res["avarohana_paltas"]) >= 3
    assert "sample_audio_url" in res
    assert res["sample_audio_url"].startswith("data:audio/wav;base64,")


def test_midi_sargam_exporter():
    """Verify binary MIDI 14-bit pitch bend generation and Sargam formatting."""
    cents = [0.0, 100.0, 204.0, 386.0, 600.0, 702.0]
    midi_bytes = MidiSargamExporter.generate_pitch_bend_midi(cents, sa_midi_note=60, tempo_bpm=90)
    assert midi_bytes.startswith(b"MThd")
    assert b"MTrk" in midi_bytes
    assert len(midi_bytes) > 30

    # Test Sargam formatting
    transcript = MidiSargamExporter.trajectory_to_sargam_transcript(cents, hop_sec=0.05)
    assert len(transcript) > 0
    assert transcript[0]["swara"] == "S"
    assert "devanagari" in transcript[0]


def test_fastapi_advanced_endpoints():
    """Verify new REST API endpoints."""
    # 1. Similarity
    r_sim = client.get("/api/raga-similarity?raga1=Yaman&raga2=Bhupali")
    assert r_sim.status_code == 200
    assert "discriminating_factors" in r_sim.json()

    # 2. Allied ragas
    r_allied = client.get("/api/similar-ragas?raga=Darbari")
    assert r_allied.status_code == 200
    assert len(r_allied.json()) > 0

    # 3. Generate Alankars
    r_drill = client.post("/api/generate-alankars", json={"raga_name": "Bhairav", "pattern_key": "turn_around"})
    assert r_drill.status_code == 200
    assert r_drill.json()["raga"] == "Bhairav"

    # 4. Export MIDI
    r_midi = client.post("/api/export-midi", json={"cents_trajectory": [0.0, 200.0, 386.0, 702.0]})
    assert r_midi.status_code == 200
    assert r_midi.headers["content-type"] == "audio/midi"
    assert r_midi.content.startswith(b"MThd")

    # 5. Export Sargam
    r_sargam = client.post("/api/export-sargam", json={"cents_trajectory": [0.0, 200.0, 400.0]})
    assert r_sargam.status_code == 200
    sargam_data = r_sargam.json()
    assert "transcript" in sargam_data
    assert "bhatkhande_line" in sargam_data
    assert sargam_data["note_count"] > 0

    # 6. Autonomous Raga Identifier
    # Yaman phrase trajectory: Sa -> Re -> Ga -> Tivra Ma -> Pa
    yaman_cents = [0.0]*10 + [203.91]*15 + [386.31]*20 + [590.22]*15 + [701.95]*20
    r_id = client.post("/api/identify-raga", json={"cents_trajectory": yaman_cents, "top_k": 3})
    assert r_id.status_code == 200
    id_data = r_id.json()
    assert "candidates" in id_data
    assert len(id_data["candidates"]) > 0
    candidate_names = [c["raga"] for c in id_data["candidates"]]
    assert "Yaman" in candidate_names or "Kalyani" in candidate_names

def test_api_compare_kaggle_baseline():
    r = client.get("/api/compare-kaggle-baseline?piece_key=yaman_eri_aali")
    assert r.status_code == 200
    data = r.json()
    assert data["piece_key"] == "yaman_eri_aali"
    assert "kaggle_baseline" in data
    assert "song_lab_engine" in data
    assert "expressive_delta" in data
    assert data["kaggle_baseline"]["transition_type_accuracy_pct"] == 0.0
    assert data["song_lab_engine"]["transition_type_accuracy_pct"] > 90.0
    assert data["song_lab_engine"]["kan_grace_touch_recall_pct"] == 100.0
    assert len(data["sample_transitions"]) > 0

