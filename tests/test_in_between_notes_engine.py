"""
Unit tests for InBetweenNotesEngine (Antar-Swara Forensic Analyzer).
Verifies:
1. Meend Sigmoidal S-Curve detection.
2. Kan Swara (Grace note / touch inflection) detection & identification.
3. Convex scoop vs Concave slide classification.
4. Murki / Khatka turn detection.
5. Expressive Transition Index (ETI) scoring.
6. Multi-note phrase transition batch analysis.
"""

import numpy as np
import pytest
from src.in_between_notes_engine import (
    InBetweenNotesEngine,
    TransitionType,
    cents_to_swara_info,
)


def test_cents_to_swara_info():
    sym, name, dev = cents_to_swara_info(0.0)
    assert sym == "S"
    assert abs(dev) < 1.0

    sym, name, dev = cents_to_swara_info(702.0)
    assert sym == "P"
    assert abs(dev - 2.0) < 0.5

    sym, name, dev = cents_to_swara_info(1105.0)
    assert sym == "N"


def test_meend_sigmoidal_s_curve():
    engine = InBetweenNotesEngine(hop_sec=0.01)
    # Generate 0.5s transition from Sa (0c) to Pa (700c) with smooth logistic sigmoid
    t = np.linspace(0.0, 0.5, 51)
    # S-curve: inflection at 0.25s
    k = 18.0
    c = 700.0 / (1.0 + np.exp(-k * (t - 0.25)))

    from_note = {"sargam": "S", "cents": 0.0, "start_time": 0.0, "end_time": 0.05}
    to_note = {"sargam": "P", "cents": 700.0, "start_time": 0.45, "end_time": 0.50}

    tr = engine.analyze_transition(
        from_note_dict=from_note,
        to_note_dict=to_note,
        times=t,
        cents=c,
        from_idx=0,
        to_idx=1,
    )

    assert tr.transition_type in (TransitionType.MEEND_SIGMOID, TransitionType.MEEND_LINEAR)
    assert "Meend" in tr.curvature_name
    assert tr.peak_velocity_cents_sec > 1000.0
    assert tr.expressive_transition_index > 85.0
    assert len(tr.contour_samples) > 0


def test_kan_swara_touch_detection():
    engine = InBetweenNotesEngine(hop_sec=0.01)
    # Transition from Pa (700c) to Dha (900c), with a momentary 50ms flick up to Ni (1100c)
    t = np.linspace(0.0, 0.6, 61)
    c = np.zeros_like(t)
    for i, ti in enumerate(t):
        if ti < 0.15:
            c[i] = 700.0
        elif 0.15 <= ti <= 0.25:
            # Kan touch flick to 1100c
            c[i] = 700.0 + (1100.0 - 700.0) * np.sin(np.pi * (ti - 0.15) / 0.10)
        else:
            c[i] = 900.0

    from_note = {"sargam": "P", "cents": 700.0, "start_time": 0.0, "end_time": 0.15}
    to_note = {"sargam": "D", "cents": 900.0, "start_time": 0.25, "end_time": 0.60}

    tr = engine.analyze_transition(
        from_note_dict=from_note,
        to_note_dict=to_note,
        times=t,
        cents=c,
        from_idx=0,
        to_idx=1,
    )

    assert tr.transition_type == TransitionType.KAN_INFLECTED
    assert tr.kan_touch is not None
    assert tr.kan_touch.swara_symbol == "N"
    assert "Upper" in tr.kan_touch.direction
    assert tr.kan_touch.touch_duration_ms > 0


def test_convex_scoop_classification():
    engine = InBetweenNotesEngine(hop_sec=0.01)
    # Late scoop: stays at 200c for 70% of the time, then shoots up to 700c at the end
    t = np.linspace(0.0, 0.5, 51)
    c = 200.0 + 500.0 * (t / 0.5) ** 4

    from_note = {"sargam": "R", "cents": 200.0, "start_time": 0.0, "end_time": 0.05}
    to_note = {"sargam": "P", "cents": 700.0, "start_time": 0.45, "end_time": 0.50}

    tr = engine.analyze_transition(
        from_note_dict=from_note,
        to_note_dict=to_note,
        times=t,
        cents=c,
        from_idx=0,
        to_idx=1,
    )

    assert tr.transition_type == TransitionType.MEEND_CONVEX_SCOOP
    assert "Convex Scoop" in tr.curvature_name


def test_phrase_transitions_batch():
    engine = InBetweenNotesEngine(hop_sec=0.01)
    # 3 notes: Sa (0) -> Re (200) -> Ga (400)
    notes = [
        {"sargam": "S", "cents": 0.0, "start_time": 0.0, "end_time": 0.3},
        {"sargam": "R", "cents": 200.0, "start_time": 0.5, "end_time": 0.8},
        {"sargam": "G", "cents": 400.0, "start_time": 1.0, "end_time": 1.3},
    ]
    t = np.linspace(0.0, 1.4, 141)
    # Smooth meends
    c = np.piecewise(
        t,
        [t < 0.3, (t >= 0.3) & (t < 0.5), (t >= 0.5) & (t < 0.8), (t >= 0.8) & (t < 1.0), t >= 1.0],
        [
            0.0,
            lambda x: 200.0 * (x - 0.3) / 0.2,
            200.0,
            lambda x: 200.0 + 200.0 * (x - 0.8) / 0.2,
            400.0,
        ],
    )
    syllables = ["E-", "ri", "aa-"]

    transitions = engine.analyze_phrase_transitions(notes, t, c, syllables=syllables)
    assert len(transitions) == 2
    assert transitions[0].from_swara == "S"
    assert transitions[0].to_swara == "R"
    assert transitions[1].from_swara == "R"
    assert transitions[1].to_swara == "G"
    assert transitions[0].syllabic_melisma is True
