"""
Unit tests for SheetMusicExtractor.
"""

import pytest
from src.sheet_music_extractor import SheetMusicExtractor


def test_parse_midi_number():
    assert SheetMusicExtractor.parse_midi_number("C4") == 60
    assert SheetMusicExtractor.parse_midi_number("A4") == 69
    assert SheetMusicExtractor.parse_midi_number("D3") == 50
    assert SheetMusicExtractor.parse_midi_number("F#4") == 66


def test_guitar_tab_calculation():
    # E4 open string 1
    tab_e4 = SheetMusicExtractor.calculate_guitar_tab(64)
    assert tab_e4["string"] == 1
    assert tab_e4["fret"] == 0

    # D4 on string 2 (B3 + 3 frets)
    tab_d4 = SheetMusicExtractor.calculate_guitar_tab(62)
    assert tab_d4["string"] == 2
    assert tab_d4["fret"] == 3


def test_rhythm_symbols():
    # At 84 BPM, 1 beat is 60/84 = ~0.714 seconds
    sym_q, name_q = SheetMusicExtractor.calculate_rhythm_symbol(0.72, 84.0)
    assert sym_q == "♩"
    assert name_q == "Quarter Note"

    sym_h, name_h = SheetMusicExtractor.calculate_rhythm_symbol(1.6, 84.0)
    assert sym_h == "𝅗𝅥"
    assert name_h == "Half Note"

    sym_e, name_e = SheetMusicExtractor.calculate_rhythm_symbol(0.36, 84.0)
    assert sym_e == "♪"
    assert name_e == "Eighth Note"


def test_split_lyrics():
    text = "E-ri aa-li pi-ya bi-na sa-khi"
    syllables = SheetMusicExtractor.split_lyrics_into_syllables(text)
    assert syllables == ["E-", "ri", "aa-", "li", "pi-", "ya", "bi-", "na", "sa-", "khi"]


def test_extract_sheet_music_with_lyrics():
    mock_notations = [
        {"western_note": "D4", "symbol": "S", "frequency_hz": 293.7, "start_time": 0.0, "end_time": 0.5, "duration_ms": 500},
        {"western_note": "F#4", "symbol": "G", "frequency_hz": 370.0, "start_time": 0.5, "end_time": 1.0, "duration_ms": 500},
        {"western_note": "G4", "symbol": "M", "frequency_hz": 392.0, "start_time": 1.0, "end_time": 1.8, "duration_ms": 800},
        {"western_note": "A4", "symbol": "P", "frequency_hz": 440.0, "start_time": 1.8, "end_time": 3.0, "duration_ms": 1200},
    ]

    lyrics = "E-ri aa-li"
    sheet = SheetMusicExtractor.extract_sheet_music(
        notations=mock_notations,
        lyrics_text=lyrics,
        tempo_bpm=84.0,
        tonic_hz=146.83,
        instrument="piano"
    )

    assert sheet["tempo_bpm"] == 84.0
    assert sheet["tonic_hz"] == 146.8
    assert sheet["lyrics_aligned"] is True
    assert sheet["total_measures"] >= 1

    first_measure = sheet["measures"][0]
    assert first_measure["time_signature"] == "4/4"
    assert len(first_measure["events"]) == 4

    ev1 = first_measure["events"][0]
    assert ev1["syllable"] == "E-"
    assert ev1["note_western"] == "D4"
    assert ev1["note_sargam"] == "S"
    assert ev1["piano_key"] == 62
    assert "guitar_tab" in ev1
    assert "flute_fingering" in ev1


def test_extract_sheet_music_canonical_phrase():
    mock_notations = [
        {"western_note": "D4", "symbol": "S", "frequency_hz": 293.7, "start_time": 0.0, "end_time": 0.6},
        {"western_note": "E4", "symbol": "R", "frequency_hz": 329.6, "start_time": 0.6, "end_time": 1.2},
    ]

    sheet = SheetMusicExtractor.extract_sheet_music(
        notations=mock_notations,
        lyrics_text=None,
        phrase_key="yaman_meend"
    )

    assert sheet["lyrics_aligned"] is True
    first_ev = sheet["measures"][0]["events"][0]
    assert first_ev["syllable"] == "E-"


def test_export_musicxml_generation():
    mock_notations = [
        {"western_note": "D4", "symbol": "S", "frequency_hz": 293.7, "start_time": 0.0, "end_time": 0.5, "duration_ms": 500},
        {"western_note": "F#4", "symbol": "G", "frequency_hz": 370.0, "start_time": 0.5, "end_time": 1.0, "duration_ms": 500},
    ]
    sheet = SheetMusicExtractor.extract_sheet_music(
        notations=mock_notations,
        lyrics_text="E-ri aa-li",
        tempo_bpm=84.0,
        phrase_key="yaman_meend"
    )
    # Inject transition with meend
    sheet["measures"][0]["events"][0]["in_between_transition"] = {
        "curvature_type": "sigmoidal_s_meend",
        "duration_ms": 120.0
    }

    xml = SheetMusicExtractor.export_musicxml(sheet)
    assert '<?xml version="1.0" encoding="UTF-8"?>' in xml
    assert '<score-partwise' in xml
    assert '<work-title>' in xml
    assert '<harmony>' in xml
    assert '<root-step>D</root-step>' in xml
    assert '<note>' in xml
    assert '<step>D</step>' in xml
    assert '<step>F</step>' in xml
    assert '<alter>1</alter>' in xml
    assert '<lyric number="1">' in xml
    assert '<text>E-</text>' in xml
    assert '<glissando type="start" number="1"/>' in xml
    assert '</score-partwise>' in xml


def test_api_export_musicxml_endpoint():
    from fastapi.testclient import TestClient
    from server import app
    client = TestClient(app)

    payload = {
        "notations": [
            {"western_note": "D4", "symbol": "S", "frequency_hz": 293.7, "start_time": 0.0, "end_time": 0.5, "duration_ms": 500},
            {"western_note": "E4", "symbol": "R", "frequency_hz": 329.6, "start_time": 0.5, "end_time": 1.0, "duration_ms": 500},
        ],
        "lyrics": "E-ri aa-li",
        "tempo_bpm": 84.0,
        "tonic_hz": 146.83,
        "instrument": "piano"
    }
    resp = client.post("/api/export-musicxml", json=payload)
    assert resp.status_code == 200
    assert "application/vnd.recordare.musicxml+xml" in resp.headers["content-type"]
    assert "songlab_lead_sheet.musicxml" in resp.headers["content-disposition"]
    xml_text = resp.text
    assert "<?xml" in xml_text
    assert "<score-partwise" in xml_text
    assert "<step>D</step>" in xml_text
    assert "<step>E</step>" in xml_text
def test_bhatkhande_sargam_sheet_export():
    lead_sheet = {
        "title": "Eri Aali Piya Bina",
        "tempo_bpm": 84.0,
        "time_signature": "4/4",
        "measures": [
            {
                "measure_number": 1,
                "chord": "Dmaj",
                "events": [
                    {"note_sargam": "S", "syllable": "E-", "note_western": "D4"},
                    {"note_sargam": "R", "syllable": "ri", "note_western": "E4", "in_between_transition": {"transition_type": "Meend / S-Curve Glide"}},
                    {"note_sargam": "G", "syllable": "aa-", "note_western": "F#4"},
                    {"note_sargam": "M", "syllable": "li", "note_western": "G4"},
                ]
            }
        ]
    }
    bk = SheetMusicExtractor.to_bhatkhande_sargam_sheet(lead_sheet)
    assert bk["title"] == "Eri Aali Piya Bina"
    assert "सा" in bk["ascii_sheet"]
    assert "E-" in bk["ascii_sheet"]
    assert "bhatkhande-score-card" in bk["html_score"]
    assert "bhatkhande-measure" in bk["html_score"]


def test_api_export_sargam_bhatkhande_endpoint():
    from fastapi.testclient import TestClient
    from server import app
    client = TestClient(app)

    payload = {
        "lead_sheet": {
            "title": "Mohe Panghat Pe",
            "tempo_bpm": 92.0,
            "measures": [
                {
                    "measure_number": 1,
                    "chord": "Gmaj",
                    "events": [
                        {"note_sargam": "G", "syllable": "Mo-"},
                        {"note_sargam": "m", "syllable": "he"},
                        {"note_sargam": "P", "syllable": "pang-"},
                        {"note_sargam": "D", "syllable": "hat"},
                    ]
                }
            ]
        }
    }
    resp = client.post("/api/export-sargam", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "bhatkhande_sheet" in data
    assert data["bhatkhande_sheet"]["title"] == "Mohe Panghat Pe"
    assert "html_score" in data["bhatkhande_sheet"]


def test_evaluate_lead_sheet_take_method():
    lead_sheet = {
        "title": "Eri Aali Piya Bina",
        "tempo_bpm": 84.0,
        "measures": [
            {
                "measure_number": 1,
                "chord": "Dmaj",
                "events": [
                    {
                        "note_sargam": "S",
                        "note_western": "D4",
                        "frequency_hz": 293.66,
                        "syllable": "E-",
                        "in_between_transition": {
                            "transition_type": "Meend / S-Curve Glide",
                            "expressive_transition_index": 96.5
                        }
                    },
                    {
                        "note_sargam": "R",
                        "note_western": "E4",
                        "frequency_hz": 330.0,
                        "syllable": "ri",
                        "in_between_transition": {
                            "transition_type": "Kan Swara / Grace Touch Transition",
                            "kan_touch": {"swara_symbol": "P", "touch_duration_ms": 55}
                        }
                    },
                    {
                        "note_sargam": "G",
                        "note_western": "F#4",
                        "frequency_hz": 370.0,
                        "syllable": "aa-"
                    }
                ]
            }
        ]
    }
    eval_res = SheetMusicExtractor.evaluate_lead_sheet_take(lead_sheet, sa_hz=146.83)
    assert eval_res["title"] == "Eri Aali Piya Bina"
    assert eval_res["intonation_accuracy_pct"] >= 90.0
    assert eval_res["meend_fluidity_pct"] >= 90.0
    assert eval_res["kan_touch_recall_pct"] == 100.0
    assert len(eval_res["measure_ribbons"]) == 1
    assert "M " in eval_res["measure_ribbons"][0]["target_path"]
    assert "M " in eval_res["measure_ribbons"][0]["sung_path"]
    assert "Guru Assessment" in eval_res["guru_assessment"] or "Intonation" in eval_res["guru_assessment"]


def test_api_evaluate_lead_sheet_take_endpoint():
    from fastapi.testclient import TestClient
    from server import app
    client = TestClient(app)

    payload = {
        "lead_sheet": {
            "title": "Jyoti Kalash Chhalke",
            "tempo_bpm": 84.0,
            "measures": [
                {
                    "measure_number": 1,
                    "chord": "Dmaj",
                    "events": [
                        {"note_sargam": "S", "note_western": "D4", "frequency_hz": 293.66, "syllable": "Jyo-"},
                        {"note_sargam": "R", "note_western": "E4", "frequency_hz": 330.0, "syllable": "ti"}
                    ]
                }
            ]
        },
        "sa_hz": 146.83
    }
    resp = client.post("/api/evaluate-lead-sheet-take", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Jyoti Kalash Chhalke"
    assert "overall_score_pct" in data
    assert "measure_ribbons" in data
    assert len(data["measure_ribbons"]) == 1

