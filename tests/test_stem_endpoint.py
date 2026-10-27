import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_api_separate_stems_endpoint():
    with open("data/test_audio/yaman_perfect_phrase.wav", "rb") as f:
        resp = client.post(
            "/api/separate-stems",
            files={"file": ("yaman.wav", f, "audio/wav")}
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "bleed_pct" in data
    assert "vocal_peaks" in data
    assert "accompaniment_peaks" in data
    assert "mix_peaks" in data
    assert len(data["vocal_peaks"]) == 160
    assert len(data["accompaniment_peaks"]) == 160
    assert data["vocal_audio_url"].startswith("data:audio/wav;base64,")
    assert data["accompaniment_audio_url"].startswith("data:audio/wav;base64,")
