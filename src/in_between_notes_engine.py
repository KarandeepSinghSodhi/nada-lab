"""
In-Between-The-Notes (Antar-Swara) Expressive Transition Engine for Song Lab.
Analyzes what happens BETWEEN discrete musical notes in Indian Classical and Hindi vocal music:
1. Meend Curvature Analysis (Sigmoidal S-curves, Convex scoops, Concave slides, Linear ramps).
2. Kan Swara (Micro-touch / Grace note) transient detection & identification (< 120ms).
3. Murki / Khatka (Fast circular microtonal turns and clustered embellishments).
4. Kinematic Transition Velocity (cents/sec), Acceleration, and Jerk dynamics.
5. Microtonal Shruti Drift & Intonation deviation between notes.
6. Syllabic Melisma continuity vs discrete articulation.
7. Expressive Transition Index (ETI): scoring the mastery and vocal fluidity of transitions.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
from scipy.optimize import curve_fit


class TransitionType(Enum):
    STHIRA_SUSTAIN = "Sthira Sustain / Stationary"
    MEEND_SIGMOID = "Meend / S-Curve Glide"
    MEEND_CONVEX_SCOOP = "Meend / Convex Scoop"
    MEEND_CONCAVE_SLIDE = "Meend / Concave Slide"
    MEEND_LINEAR = "Meend / Linear Ramp"
    KAN_INFLECTED = "Kan Swara / Grace Touch Transition"
    MURKI_TURN = "Murki / Rapid Microtonal Turn"
    KHATKA_CLUSTER = "Khatka / Clustered Ornament"
    GAMAK_OSCILLATION = "Gamak / Oscillatory Approach"
    DISCRETE_JUMP = "Discrete Jump / Quantized Leap"
    SILENT_REST = "Rest / Silent Gap"


# 12-TET interval names and Bhatkhande Swara symbols relative to Sa (0 cents)
SWARA_INTERVALS = [
    (0, "S", "Sa", "Tonic"),
    (100, "r", "Komal Re", "Minor Second"),
    (200, "R", "Shuddha Re", "Major Second"),
    (300, "g", "Komal Ga", "Minor Third"),
    (400, "G", "Shuddha Ga", "Major Third"),
    (500, "m", "Shuddha Ma", "Perfect Fourth"),
    (600, "M", "Tivra Ma", "Tritone / Augmented Fourth"),
    (700, "P", "Pa", "Perfect Fifth"),
    (800, "d", "Komal Dha", "Minor Sixth"),
    (900, "D", "Shuddha Dha", "Major Sixth"),
    (1000, "n", "Komal Ni", "Minor Seventh"),
    (1100, "N", "Shuddha Ni", "Major Seventh"),
    (1200, "S'", "Taar Sa", "Octave Tonic"),
]


def cents_to_swara_info(cents_val: float) -> Tuple[str, str, float]:
    """
    Finds nearest swara symbol, name, and microtonal deviation in cents.
    """
    norm_cents = cents_val % 1200
    closest = min(SWARA_INTERVALS, key=lambda x: abs(x[0] - norm_cents))
    dev = norm_cents - closest[0]
    if dev > 600:
        dev -= 1200
    elif dev < -600:
        dev += 1200
    return closest[1], closest[2], round(dev, 1)


@dataclass
class KanTouch:
    swara_symbol: str
    swara_name: str
    target_cents: float
    actual_peak_cents: float
    cents_deviation: float
    touch_duration_ms: float
    timestamp_sec: float
    direction: str  # "Upper" or "Lower" relative to base note


@dataclass
class InBetweenNoteTransition:
    from_note_idx: int
    to_note_idx: int
    from_swara: str
    to_swara: str
    from_cents: float
    to_cents: float
    total_interval_cents: float
    start_time: float
    end_time: float
    duration_ms: float
    transition_type: TransitionType
    curvature_name: str
    peak_velocity_cents_sec: float
    mean_velocity_cents_sec: float
    inflection_ratio: float  # 0.0 (early) to 1.0 (late), 0.5 = symmetrical S-curve
    kan_touch: Optional[KanTouch] = None
    murki_loops: int = 0
    gamak_rate_hz: Optional[float] = None
    expressive_transition_index: float = 85.0  # 0 to 100
    syllabic_melisma: bool = True
    contour_samples: List[float] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_note_idx": self.from_note_idx,
            "to_note_idx": self.to_note_idx,
            "from_swara": self.from_swara,
            "to_swara": self.to_swara,
            "from_cents": round(self.from_cents, 1),
            "to_cents": round(self.to_cents, 1),
            "total_interval_cents": round(self.total_interval_cents, 1),
            "start_time": round(self.start_time, 3),
            "end_time": round(self.end_time, 3),
            "duration_ms": round(self.duration_ms, 1),
            "transition_type": self.transition_type.value,
            "curvature_name": self.curvature_name,
            "peak_velocity_cents_sec": round(self.peak_velocity_cents_sec, 1),
            "mean_velocity_cents_sec": round(self.mean_velocity_cents_sec, 1),
            "inflection_ratio": round(self.inflection_ratio, 2),
            "kan_touch": {
                "swara_symbol": self.kan_touch.swara_symbol,
                "swara_name": self.kan_touch.swara_name,
                "target_cents": round(self.kan_touch.target_cents, 1),
                "actual_peak_cents": round(self.kan_touch.actual_peak_cents, 1),
                "cents_deviation": round(self.kan_touch.cents_deviation, 1),
                "touch_duration_ms": round(self.kan_touch.touch_duration_ms, 1),
                "timestamp_sec": round(self.kan_touch.timestamp_sec, 3),
                "direction": self.kan_touch.direction,
            }
            if self.kan_touch
            else None,
            "murki_loops": self.murki_loops,
            "gamak_rate_hz": round(self.gamak_rate_hz, 2) if self.gamak_rate_hz else None,
            "expressive_transition_index": round(self.expressive_transition_index, 1),
            "syllabic_melisma": self.syllabic_melisma,
            "description": self.description,
            "contour_samples": [round(c, 1) for c in self.contour_samples[:30]],
        }


class InBetweenNotesEngine:
    """
    Forensic Microtonal Transition Analyzer:
    Analyzes the continuous trajectory and expressive gestures between discrete musical notes.
    """

    def __init__(self, hop_sec: float = 0.01):
        self.hop_sec = hop_sec

    def analyze_transition(
        self,
        from_note_dict: Dict[str, Any],
        to_note_dict: Dict[str, Any],
        times: np.ndarray,
        cents: np.ndarray,
        from_idx: int,
        to_idx: int,
        from_syllable: str = "",
        to_syllable: str = "",
    ) -> InBetweenNoteTransition:
        """
        Analyzes the trajectory between from_note and to_note.
        """
        t_start = float(from_note_dict.get("end_time", from_note_dict.get("start_time", 0.0)))
        t_end = float(to_note_dict.get("start_time", to_note_dict.get("end_time", t_start + 0.2)))

        c_from = float(
            from_note_dict.get("avg_cents")
            if from_note_dict.get("avg_cents") is not None
            else from_note_dict.get("cents", from_note_dict.get("pitch_cents", 0.0))
        )
        c_to = float(
            to_note_dict.get("avg_cents")
            if to_note_dict.get("avg_cents") is not None
            else to_note_dict.get("cents", to_note_dict.get("pitch_cents", c_from))
        )

        swara_from = str(
            from_note_dict.get("symbol")
            or from_note_dict.get("sargam")
            or from_note_dict.get("swara")
            or "S"
        )
        swara_to = str(
            to_note_dict.get("symbol")
            or to_note_dict.get("sargam")
            or to_note_dict.get("swara")
            or "S"
        )

        # Allow slight padding into the notes to capture departure and arrival curvatures
        pad_t = min(0.08, max(0.02, (t_end - t_start) * 0.25))
        mask = (times >= (t_start - pad_t)) & (times <= (t_end + pad_t))
        
        t_seg = times[mask]
        c_seg = cents[mask]

        # Handle edge case of no voiced samples in between
        if len(c_seg) < 4 or np.all(np.isnan(c_seg)):
            gap_ms = max(0.0, (t_end - t_start) * 1000.0)
            tr_type = TransitionType.SILENT_REST if gap_ms > 120.0 else TransitionType.DISCRETE_JUMP
            return InBetweenNoteTransition(
                from_note_idx=from_idx,
                to_note_idx=to_idx,
                from_swara=swara_from,
                to_swara=swara_to,
                from_cents=c_from,
                to_cents=c_to,
                total_interval_cents=c_to - c_from,
                start_time=t_start,
                end_time=t_end,
                duration_ms=gap_ms,
                transition_type=tr_type,
                curvature_name="Instantaneous Step / Rest",
                peak_velocity_cents_sec=0.0,
                mean_velocity_cents_sec=0.0,
                inflection_ratio=0.5,
                expressive_transition_index=45.0,
                syllabic_melisma=False,
                contour_samples=[],
                description="Unconnected step transition or acoustic silence between swaras.",
            )

        # Interpolate NaNs
        nans = np.isnan(c_seg)
        if np.any(nans):
            indices = np.arange(len(c_seg))
            if np.all(nans):
                c_seg = np.linspace(c_from, c_to, len(c_seg))
            else:
                c_seg[nans] = np.interp(indices[nans], indices[~nans], c_seg[~nans])

        duration_ms = (t_seg[-1] - t_seg[0]) * 1000.0
        dt = np.mean(np.diff(t_seg)) if len(t_seg) > 1 else self.hop_sec
        dt = max(dt, 0.001)

        # Kinematic derivatives: velocity and acceleration
        vel = np.gradient(c_seg, dt)
        acc = np.gradient(vel, dt)

        peak_v = float(np.max(np.abs(vel)))
        mean_v = float(np.mean(np.abs(vel)))
        total_interval = c_to - c_from

        # Sub-sample contour for client visualization (up to 25 points)
        step = max(1, len(c_seg) // 25)
        contour_sub = c_seg[::step].tolist()

        # Check for Murki / Khatka (microtonal oscillations/turns)
        murki_loops, gamak_rate = self._detect_turns_and_gamak(c_seg, t_seg, vel)

        # Check for Kan Swara (Touch / Grace note) - only if not a multi-turn oscillation
        kan_touch = self._detect_kan_touch(c_seg, t_seg, c_from, c_to, vel) if murki_loops < 2 else None

        # Curvature Classification
        curv_name, tr_type, inflection_ratio, eti = self._classify_curvature(
            c_seg, t_seg, vel, acc, c_from, c_to, total_interval, kan_touch, murki_loops, gamak_rate
        )

        # Melisma detection: if vowels glide without a silent gap and lyrics share hyphen
        syllabic_melisma = bool(
            (
                kan_touch is not None
                or "Meend" in curv_name
                or (from_syllable.endswith("-") or to_syllable.startswith("-") or not to_syllable)
            )
            and (duration_ms > 60.0)
        )

        description = self._generate_description(
            swara_from, swara_to, tr_type, curv_name, kan_touch, peak_v, duration_ms, eti
        )

        return InBetweenNoteTransition(
            from_note_idx=from_idx,
            to_note_idx=to_idx,
            from_swara=swara_from,
            to_swara=swara_to,
            from_cents=c_from,
            to_cents=c_to,
            total_interval_cents=total_interval,
            start_time=float(t_seg[0]),
            end_time=float(t_seg[-1]),
            duration_ms=round(duration_ms, 1),
            transition_type=tr_type,
            curvature_name=curv_name,
            peak_velocity_cents_sec=round(peak_v, 1),
            mean_velocity_cents_sec=round(mean_v, 1),
            inflection_ratio=round(inflection_ratio, 2),
            kan_touch=kan_touch,
            murki_loops=murki_loops,
            gamak_rate_hz=gamak_rate,
            expressive_transition_index=round(eti, 1),
            syllabic_melisma=syllabic_melisma,
            contour_samples=contour_sub,
            description=description,
        )

    def _detect_kan_touch(
        self,
        c_seg: np.ndarray,
        t_seg: np.ndarray,
        c_from: float,
        c_to: float,
        vel: np.ndarray,
    ) -> Optional[KanTouch]:
        """
        Detects ephemeral micro-touch grace note (< 120ms duration) that grazes
        an upper or lower swara before landing on the target note.
        """
        if len(c_seg) < 5 or abs(c_to - c_from) < 40.0:
            return None

        # Check for overshoot beyond the min/max of [c_from, c_to]
        min_bound = min(c_from, c_to) - 35.0
        max_bound = max(c_from, c_to) + 35.0

        peak_idx = int(np.argmax(c_seg))
        trough_idx = int(np.argmin(c_seg))

        peak_val = c_seg[peak_idx]
        trough_val = c_seg[trough_idx]

        # Upper Kan touch: overshoots the higher swara by at least 45 cents
        if peak_val > max_bound + 25.0:
            # Measure duration of the overshoot excursion
            above_mask = c_seg > max_bound
            overshoot_dur_ms = np.sum(above_mask) * (self.hop_sec * 1000.0)
            if 20.0 <= overshoot_dur_ms <= 240.0:
                sym, name, dev = cents_to_swara_info(peak_val)
                return KanTouch(
                    swara_symbol=sym,
                    swara_name=name,
                    target_cents=round(peak_val - dev, 1),
                    actual_peak_cents=round(peak_val, 1),
                    cents_deviation=round(dev, 1),
                    touch_duration_ms=round(overshoot_dur_ms, 1),
                    timestamp_sec=float(t_seg[peak_idx]),
                    direction="Upper Kan Touch",
                )

        # Lower Kan touch: dips below the lower swara by at least 45 cents
        if trough_val < min_bound - 25.0:
            below_mask = c_seg < min_bound
            undershoot_dur_ms = np.sum(below_mask) * (self.hop_sec * 1000.0)
            if 20.0 <= undershoot_dur_ms <= 240.0:
                sym, name, dev = cents_to_swara_info(trough_val)
                return KanTouch(
                    swara_symbol=sym,
                    swara_name=name,
                    target_cents=round(trough_val - dev, 1),
                    actual_peak_cents=round(trough_val, 1),
                    cents_deviation=round(dev, 1),
                    touch_duration_ms=round(undershoot_dur_ms, 1),
                    timestamp_sec=float(t_seg[trough_idx]),
                    direction="Lower Kan Touch",
                )

        return None

    def _detect_turns_and_gamak(
        self, c_seg: np.ndarray, t_seg: np.ndarray, vel: np.ndarray
    ) -> Tuple[int, Optional[float]]:
        """
        Detects zero crossings in velocity that indicate directional loops (Murki/Khatka)
        or oscillatory shakes (Gamak).
        """
        if len(vel) < 6:
            return 0, None

        # Zero-crossings of velocity with sufficient amplitude
        zero_crossings = np.where(np.diff(np.signbit(vel)))[0]
        num_turns = len(zero_crossings)

        # Filter out micro-jitter: turn must have span >= 30 cents
        prominent_turns = 0
        for i in range(len(zero_crossings) - 1):
            idx1 = zero_crossings[i]
            idx2 = zero_crossings[i + 1]
            if abs(c_seg[idx2] - c_seg[idx1]) >= 28.0:
                prominent_turns += 1

        dur_sec = max(0.01, t_seg[-1] - t_seg[0])
        gamak_rate = None
        if prominent_turns >= 3 and dur_sec >= 0.2:
            gamak_rate = round(prominent_turns / (2.0 * dur_sec), 1)

        return prominent_turns, gamak_rate

    def _classify_curvature(
        self,
        c_seg: np.ndarray,
        t_seg: np.ndarray,
        vel: np.ndarray,
        acc: np.ndarray,
        c_from: float,
        c_to: float,
        total_interval: float,
        kan_touch: Optional[KanTouch],
        murki_loops: int,
        gamak_rate: Optional[float],
    ) -> Tuple[str, TransitionType, float, float]:
        """
        Classifies the mathematical curvature of the continuous pitch trajectory.
        Returns: (curvature_name, transition_type, inflection_ratio, expressive_transition_index)
        """
        dur_ms = (t_seg[-1] - t_seg[0]) * 1000.0
        abs_interval = abs(total_interval)

        # 1. Gamak or Murki loops (multi-directional turns)
        if gamak_rate and gamak_rate >= 3.0:
            return (
                f"Gamak Oscillation ({gamak_rate} Hz)",
                TransitionType.GAMAK_OSCILLATION,
                0.5,
                91.0,
            )

        if murki_loops >= 2 and dur_ms < 400.0:
            return (
                f"Murki / Khatka Rapid Turn ({murki_loops} loops)",
                TransitionType.MURKI_TURN,
                0.5,
                92.5,
            )

        # 2. Unidirectional Kan Swara inflection
        if kan_touch is not None:
            eti = 94.0 if kan_touch.touch_duration_ms < 90.0 else 88.0
            return (
                f"{kan_touch.direction} ({kan_touch.swara_symbol})",
                TransitionType.KAN_INFLECTED,
                0.5,
                eti,
            )

        # 3. Microtonal Meend Glide Curvature Analysis
        if abs_interval >= 50.0 and dur_ms >= 70.0:
            # Normalize time and cents to [0, 1]
            u = np.linspace(0.0, 1.0, len(c_seg))
            c_norm = (c_seg - c_seg[0]) / (c_seg[-1] - c_seg[0] + 1e-6)

            # Find peak velocity position (inflection ratio)
            inflection_idx = int(np.argmax(np.abs(vel)))
            inflection_ratio = float(inflection_idx / max(1, len(vel) - 1))

            # Area Under Curve (AUC) relative to linear ramp
            # Linear ramp has AUC = 0.5.
            # Convex scoop (stays low then jumps late): AUC < 0.40
            # Concave slide (jumps early then floats): AUC > 0.60
            # Symmetrical Sigmoid: AUC ~ 0.50 with inflection near 0.40-0.60 and high mid-velocity
            # Trapezoidal integration for Area Under Curve
            auc = float(np.sum((c_norm[:-1] + c_norm[1:]) * 0.5 * np.diff(u)))

            # Monotonicity check
            total_path = float(np.sum(np.abs(np.diff(c_seg))))
            monotonicity = abs_interval / (total_path + 1e-6)

            if monotonicity >= 0.70:
                if 0.35 <= inflection_ratio <= 0.65 and 0.42 <= auc <= 0.58:
                    curv_name = "Sigmoidal S-Curve Meend"
                    tr_type = TransitionType.MEEND_SIGMOID
                    # Sigmoidal transitions show highest vocal mastery (smooth C2 acceleration)
                    eti = 96.5
                elif auc < 0.40 or inflection_ratio > 0.65:
                    curv_name = "Convex Scoop Meend (Late Ascent)"
                    tr_type = TransitionType.MEEND_CONVEX_SCOOP
                    eti = 91.0
                elif auc > 0.60 or inflection_ratio < 0.35:
                    curv_name = "Concave Float Meend (Early Release)"
                    tr_type = TransitionType.MEEND_CONCAVE_SLIDE
                    eti = 90.5
                else:
                    curv_name = "Linear Meend Ramp"
                    tr_type = TransitionType.MEEND_LINEAR
                    eti = 86.0
            else:
                curv_name = "Undulating Expressive Portamento"
                tr_type = TransitionType.MEEND_SIGMOID
                eti = 88.0

            return curv_name, tr_type, inflection_ratio, eti

        # 4. Sthira Sustain vs Murki turn when interval is small
        if abs_interval < 30.0:
            c_span = float(np.max(c_seg) - np.min(c_seg))
            if c_span >= 50.0 and dur_ms < 750.0:
                return "Murki / Embellished Turn", TransitionType.MURKI_TURN, 0.5, 93.0
            return "Sthira Steady Sustain", TransitionType.STHIRA_SUSTAIN, 0.5, 95.0

        # 5. Discrete Jump (fast uncurved leap)
        return "Discrete Chromatic Leap", TransitionType.DISCRETE_JUMP, 0.5, 72.0

    def _generate_description(
        self,
        from_swara: str,
        to_swara: str,
        tr_type: TransitionType,
        curv_name: str,
        kan: Optional[KanTouch],
        peak_v: float,
        dur_ms: float,
        eti: float,
    ) -> str:
        """
        Creates a musician-first diagnostic description for the transition.
        """
        if kan:
            return (
                f"Masterful vocal inflection: {from_swara} grazes {kan.swara_symbol} ({kan.direction}) "
                f"for {kan.touch_duration_ms:.0f}ms before resolving to {to_swara} (peak velocity {peak_v:.0f} c/s, ETI {eti:.1f}%)."
            )
        elif tr_type == TransitionType.MEEND_SIGMOID:
            return (
                f"Classic Gayaki S-curve meend gliding {from_swara} → {to_swara} over {dur_ms:.0f}ms "
                f"with smooth C2 continuous acceleration (ETI {eti:.1f}%)."
            )
        elif tr_type == TransitionType.MEEND_CONVEX_SCOOP:
            return (
                f"Expressive late scoop from {from_swara} into {to_swara} over {dur_ms:.0f}ms "
                f"(peak velocity {peak_v:.0f} c/s)."
            )
        elif tr_type == TransitionType.MEEND_CONCAVE_SLIDE:
            return (
                f"Gentle early-release float connecting {from_swara} down to {to_swara} over {dur_ms:.0f}ms."
            )
        elif tr_type == TransitionType.MURKI_TURN:
            return f"Rapid circular microtonal turn embellishing the interval {from_swara} → {to_swara}."
        elif tr_type == TransitionType.GAMAK_OSCILLATION:
            return f"Heavy gamaka oscillatory shake approaching {to_swara}."
        elif tr_type == TransitionType.DISCRETE_JUMP:
            return f"Direct discrete leap from {from_swara} to {to_swara} without continuous microtonal meend."
        return f"Transition connecting {from_swara} to {to_swara} ({curv_name})."

    def analyze_phrase_transitions(
        self,
        notes: List[Dict[str, Any]],
        times: np.ndarray,
        cents: np.ndarray,
        syllables: Optional[List[str]] = None,
    ) -> List[InBetweenNoteTransition]:
        """
        Analyzes transitions between all consecutive note pairs in a transcribed phrase.
        """
        if len(notes) < 2:
            return []

        transitions: List[InBetweenNoteTransition] = []
        num_notes = len(notes)

        for i in range(num_notes - 1):
            n_curr = notes[i]
            n_next = notes[i + 1]

            syl_curr = syllables[i] if (syllables and i < len(syllables)) else ""
            syl_next = syllables[i + 1] if (syllables and (i + 1) < len(syllables)) else ""

            tr = self.analyze_transition(
                from_note_dict=n_curr,
                to_note_dict=n_next,
                times=times,
                cents=cents,
                from_idx=i,
                to_idx=i + 1,
                from_syllable=syl_curr,
                to_syllable=syl_next,
            )
            transitions.append(tr)

        return transitions
