"""
Unit tests for new high-impact features in Song Lab:
1. Dynamic Time Warping (DTW) Alignment & Cent Delta Engine
2. Virtual Guru Audio Reference Synthesizer
3. Raga Knowledge Graph & Literature RAG Query Engine
4. FastAPI Endpoints (/api/status, /api/rag-query, /api/synthesize-guru, /api/compare-dtw)
"""

import os
import pytest
import numpy as np
from fastapi.testclient import TestClient

from src.dtw_engine import compute_pitch_dtw
from src.guru_synthesizer import synthesize_guru_phrase
from src.rag_engine import RagaRAGEngine
from server import app


client = TestClient(app)


def test_dtw_engine_perfect_alignment():
    """Verify that identical trajectories yield 100% purity and near-zero MAD."""
    curve = np.array([0.0, 100.0, 200.0, 400.0, 700.0, 702.0, 600.0, 400.0, 200.0, 0.0])
    res = compute_pitch_dtw(curve, curve)
    assert "metrics" in res
    assert res["metrics"]["mean_absolute_deviation_cents"] == 0.0
    assert res["metrics"]["intonation_purity_pct"] == 100.0
    assert res["metrics"]["alignment_score"] == 100.0
    assert len(res["alignment_stream"]) > 0
    assert res["alignment_stream"][0]["zone"] == "green"


def test_dtw_engine_severe_deviation():
    """Verify that a sharp/flat deviation is correctly flagged with amber/red zones."""
    user = np.array([50.0, 160.0, 280.0, 490.0, 780.0])
    ideal = np.array([0.0, 100.0, 200.0, 400.0, 700.0])
    res = compute_pitch_dtw(user, ideal)
    assert res["metrics"]["mean_absolute_deviation_cents"] > 40.0
    assert res["metrics"]["intonation_purity_pct"] < 50.0
    # Should contain red zones for deviations > 35 cents
    zones = [pt["zone"] for pt in res["alignment_stream"]]
    assert "red" in zones


def test_virtual_guru_synthesizer():
    """Verify synthesis of audio data URL with valid duration and trajectory."""
    res = synthesize_guru_phrase(
        sa_hz=146.83,
        swaras=["N.", "R", "G", "M", "P"],
        note_dur_sec=0.4,
        glide_sec=0.12,
    )
    assert res["data_url"].startswith("data:audio/wav;base64,")
    assert res["duration_sec"] > 1.5
    assert len(res["cents_trajectory"]) > 10
    assert res["sa_hz"] == 146.83


def test_rag_query_engine():
    """Verify RAG queries cross-reference raga grammar and peer-reviewed papers."""
    engine = RagaRAGEngine()
    assert len(engine.papers) == 672
    assert len(engine.raga_index) >= 56

    # Test literature search
    papers = engine.search_literature("pitch tracking continuous ornament", top_k=3)
    assert len(papers) > 0
    assert "title" in papers[0]
    assert "takeaway" in papers[0]

    # Test query answering for Yaman
    ans = engine.answer_query("What are the rules and forbidden notes in Yaman?", target_raga="Yaman")
    assert ans["target_raga"] == "Yaman"
    assert ans["raga_musicology"]["vadi"] == "G"
    assert "m" in ans["raga_musicology"]["varjya_swaras"]  # Shuddha Ma (m) is forbidden in Yaman
    assert len(ans["literature_citations"]) > 0
    assert "Yaman" in ans["synthesis"]


def test_fastapi_new_endpoints():
    """Verify API endpoints response codes and payloads."""
    # 1. Status
    r_status = client.get("/api/status")
    assert r_status.status_code == 200
    data = r_status.json()
    assert data["status"] == "online"
    assert data["ragas_loaded"] >= 56
    assert data["research_papers_indexed"] == 672

    # 2. RAG Query
    r_rag = client.post("/api/rag-query", json={"query": "Explain the role of Komal Gandhar in Darbari", "target_raga": "Darbari"})
    assert r_rag.status_code == 200
    rag_data = r_rag.json()
    assert rag_data["target_raga"] == "Darbari"
    assert "Darbari" in rag_data["synthesis"]

    # 3. Virtual Guru Synthesis
    r_synth = client.post("/api/synthesize-guru", json={"target_raga": "Yaman", "sa_hz": 146.83})
    assert r_synth.status_code == 200
    synth_data = r_synth.json()
    assert synth_data["data_url"].startswith("data:audio/wav;base64,")

    # 4. DTW Compare
    r_dtw = client.post("/api/compare-dtw", json={
        "user_cents": [0.0, 100.0, 204.0, 386.0, 702.0],
        "target_raga": "Yaman",
        "sa_hz": 146.83,
    })
    assert r_dtw.status_code == 200
    dtw_data = r_dtw.json()
    assert "metrics" in dtw_data
    assert "alignment_score" in dtw_data["metrics"]
