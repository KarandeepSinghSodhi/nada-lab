"""
Tests for 1-Click Track Upload, Automatic Notation Transcription,
Scale & Key Detection, Tempo & BPM Extraction, and Complete Diagnostic Report.
"""

import pytest
from fastapi.testclient import TestClient
from server import app
from src.pipeline import SongLabPipeline

client = TestClient(app)


def test_pipeline_extracts_scale_bpm_and_notations():
    pipeline = SongLabPipeline()
    res = pipeline.process("data/test_audio/yaman_perfect_phrase.wav")

    # 1. Scale & Key
    assert "scale_and_key" in res
    assert "tonic_hz" in res["scale_and_key"]
    assert "identified_raga" in res["scale_and_key"]
    assert res["scale_and_key"]["tonic_hz"] > 50.0

    # 2. Tempo & BPM
    assert "tempo_and_meter" in res
    assert "bpm" in res["tempo_and_meter"]
    assert res["tempo_and_meter"]["bpm"] > 30.0
    assert "suggested_tala" in res["tempo_and_meter"]

    # 3. Transcribed Notations
    assert "transcribed_notations" in res
    assert isinstance(res["transcribed_notations"], list)
    assert len(res["transcribed_notations"]) > 0
    first_note = res["transcribed_notations"][0]
    assert "symbol" in first_note
    assert "western_note" in first_note
    assert "start_time" in first_note
    assert "cents_deviation" in first_note

    # 4. Waveform Peaks
    assert "waveform_peaks" in res
    assert len(res["waveform_peaks"]) > 0

    # 5. Pitch trajectory
    assert "pitch_trajectory" in res
    assert len(res["pitch_trajectory"]) > 0


def test_api_analyze_endpoint_returns_complete_report():
    with open("data/test_audio/yaman_perfect_phrase.wav", "rb") as f:
        response = client.post(
            "/api/analyze?target_raga=Yaman",
            files={"file": ("yaman.wav", f, "audio/wav")}
        )

    assert response.status_code == 200
    data = response.json()

    assert "scale_and_key" in data
    assert "tempo_and_meter" in data
    assert "transcribed_notations" in data
    assert "waveform_peaks" in data
    assert "pitch_trajectory" in data
    assert "phrase_critiques" in data
    assert data["scale_and_key"]["identified_raga"] != ""
    assert data["tempo_and_meter"]["bpm"] > 0
