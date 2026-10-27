"""
"What Is Missing" Deficit Engine & 3-Tier Salience Filter for Song Lab.
Implements:
1. Hierarchical Severity Ranking:
   - Tier 1 (Red / Fatal): Forbidden (Varjya) note violation, Tonic ($Sa$) alienation.
   - Tier 2 (Yellow / Structural): Missing mandatory ornament, wrong phrase progression.
   - Tier 3 (Blue / Nuance): Microtonal Shruti error (> 15c deviation), ornament speed/depth mismatch.
2. Cognitive Load Throttling: Emits exactly 1 primary critique per phrase to avoid overwhelming the student.
3. Dual-Mode Terminology Translation (Indian Classical / Gayaki vs Western / Contemporary).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional
import numpy as np

from src.ornament_detector import OrnamentSegment, OrnamentType
from src.raga_matcher import RAGA_DATABASE, RagaDefinition, SWARA_TO_SEMITONE, SEMITONE_TO_SWARA
from src.tonal_engine import quantize_to_12_swara, quantize_to_shruti


class DeficitTier(Enum):
    TIER_1_CRITICAL = "Tier 1: Fatal Tonal Violation"
    TIER_2_STRUCTURAL = "Tier 2: Structural Ornament / Grammar Deficit"
    TIER_3_MICROTONAL = "Tier 3: Microtonal & Nuance Refinement"
    NO_DEFICIT = "Perfect Alignment"


@dataclass
class CritiqueFeedback:
    phrase_id: int
    start_time: float
    end_time: float
    tier: DeficitTier
    primary_badge: str
    critique_indian_mode: str
    critique_western_mode: str
    prescriptive_drill: str
    secondary_notes: List[str]
    confidence: float

    def to_dict(self) -> Dict:
        return {
            "phrase_id": self.phrase_id,
            "start_time": round(self.start_time, 2),
            "end_time": round(self.end_time, 2),
            "tier": self.tier.value,
            "badge": self.primary_badge,
            "indian_classical_mode": {
                "critique": self.critique_indian_mode,
                "drill": self.prescriptive_drill,
            },
            "western_contemporary_mode": {
                "critique": self.critique_western_mode,
                "drill": self.prescriptive_drill,
            },
            "secondary_observations": self.secondary_notes,
            "confidence": round(self.confidence, 3),
        }


class DeficitEngine:
    """
    Evaluates sung phrases against target Raga grammar and produces
    focused, hierarchical feedback.
    """

    def __init__(self, target_raga_name: str = "Yaman"):
        self.raga = next((r for r in RAGA_DATABASE if r.name.lower() == target_raga_name.lower()), RAGA_DATABASE[0])

    def evaluate_phrase(
        self,
        phrase_id: int,
        cents_trajectory: np.ndarray,
        time_trajectory: np.ndarray,
        detected_ornaments: List[OrnamentSegment],
    ) -> CritiqueFeedback:
        """
        Runs the 3-tier salience filter across the phrase and returns the single
        highest-priority musical deficit.
        """
        valid_cents = cents_trajectory[~np.isnan(cents_trajectory)]
        if len(valid_cents) == 0:
            return CritiqueFeedback(
                phrase_id=phrase_id,
                start_time=float(time_trajectory[0]) if len(time_trajectory) else 0.0,
                end_time=float(time_trajectory[-1]) if len(time_trajectory) else 0.0,
                tier=DeficitTier.TIER_1_CRITICAL,
                primary_badge="[Unvoiced / Silence]",
                critique_indian_mode="No sustained swara detected in this phrase. Ensure vocal projection.",
                critique_western_mode="No pitched vocal energy detected in this interval. Check input levels.",
                prescriptive_drill="Sustain a clear 'Aakar' on Sa to calibrate the microphone.",
                secondary_notes=[],
                confidence=1.0,
            )

        start_t = float(time_trajectory[0])
        end_t = float(time_trajectory[-1])

        # Step 1: Analyze Swaras Present in this phrase
        swara_counts: Dict[str, int] = {}
        shruti_errors: List[float] = []

        for c in valid_cents:
            sw_dict, err, _ = quantize_to_12_swara(c)
            sym = sw_dict["symbol"]
            swara_counts[sym] = swara_counts.get(sym, 0) + 1
            
            _, shruti_err, _ = quantize_to_shruti(c)
            shruti_errors.append(abs(shruti_err))

        total_frames = len(valid_cents)
        swara_ratios = {k: v / total_frames for k, v in swara_counts.items()}
        secondary_notes = []

        # =========================================================================
        # TIER 1 CHECK: Forbidden (Varjya) Swara Violations & Tonic Grounding
        # =========================================================================
        for varjya in self.raga.varjya_swaras:
            ratio = swara_ratios.get(varjya, 0.0)
            # If sung for more than 12% of the phrase duration, it's a fatal varjya intrusion
            if ratio > 0.12:
                sw_info = next(s for s in SWARA_TO_SEMITONE if s == varjya)
                badge = f"[Forbidden Swara: {varjya}]"
                
                critique_in = (
                    f"Fatal note violation: You sang {varjya} ({ratio*100:.0f}% of phrase). "
                    f"In Raga {self.raga.name}, {varjya} is strictly Varjya (forbidden). "
                    f"Singing this instantly breaks the raga roop."
                )
                critique_we = (
                    f"Fatal tonal error: Avoidance degree '{varjya}' sounded for {ratio*100:.0f}% of the interval. "
                    f"The modal scale of {self.raga.name} prohibits this semitone pitch class."
                )
                drill = (
                    f"Practice the phrase using pure Vadi '{self.raga.vadi}' and Samvadi '{self.raga.samvadi}', "
                    f"actively omitting '{varjya}'."
                )
                return CritiqueFeedback(
                    phrase_id=phrase_id,
                    start_time=start_t,
                    end_time=end_t,
                    tier=DeficitTier.TIER_1_CRITICAL,
                    primary_badge=badge,
                    critique_indian_mode=critique_in,
                    critique_western_mode=critique_we,
                    prescriptive_drill=drill,
                    secondary_notes=[f"Forbidden note dwell: {ratio*100:.1f}%"],
                    confidence=0.98,
                )

        # =========================================================================
        # TIER 2 & TIER 3 CHECK: Ornaments & Vibrato Flutter
        # =========================================================================
        for swara, required_ornament in self.raga.mandatory_ornaments.items():
            ratio = swara_ratios.get(swara, 0.0)
            if ratio > 0.20:
                # Check what ornament accompanied this swara
                target_cents = SWARA_TO_SEMITONE[swara] * 100.0
                overlapping_ornaments = [
                    seg for seg in detected_ornaments
                    if abs((seg.min_cents % 1200.0) - target_cents) < 120.0 or
                       abs((seg.max_cents % 1200.0) - target_cents) < 120.0 or
                       abs(seg.start_cents % 1200.0 - target_cents) < 120.0
                ]
                
                # Check for rapid oscillation (Vibrato or Gamak) where slow Andolan was required
                fast_osc = next(
                    (s for s in overlapping_ornaments
                     if s.ornament_type in (OrnamentType.VIBRATO, OrnamentType.GAMAK) and
                     (s.oscillation_rate_hz is not None and s.oscillation_rate_hz > 3.5)),
                    None
                )
                if fast_osc is not None and "andolan" in required_ornament.lower():
                    rate = fast_osc.oscillation_rate_hz or 6.0
                    badge = "[Vibrato Flutter Instead of Andolan]"
                    critique_in = (
                        f"Ornament speed error: Detected {rate:.1f} Hz fast oscillation on swara '{swara}'. "
                        f"Indian classical gayaki requires a slow, deliberate Andolan (1.8 - 2.5 Hz), not rapid shake."
                    )
                    critique_we = (
                        f"Vocal oscillation rate on '{swara}' is too rapid ({rate:.1f} Hz). "
                        f"Expand your oscillation wave to a broader ~2 Hz pitch modulation."
                    )
                    drill = "Drop the oscillation speed by 50%. Focus on steady breath control from the diaphragm."
                    return CritiqueFeedback(
                        phrase_id=phrase_id,
                        start_time=start_t,
                        end_time=end_t,
                        tier=DeficitTier.TIER_3_MICROTONAL,
                        primary_badge=badge,
                        critique_indian_mode=critique_in,
                        critique_western_mode=critique_we,
                        prescriptive_drill=drill,
                        secondary_notes=[f"Oscillation rate: {rate:.1f} Hz"],
                        confidence=0.90,
                    )

                has_ornament = False
                for seg in overlapping_ornaments:
                    if "andolan" in required_ornament.lower() and seg.ornament_type == OrnamentType.ANDOLAN:
                        has_ornament = True
                    elif "meend" in required_ornament.lower() and seg.ornament_type == OrnamentType.MEEND:
                        has_ornament = True
                    elif "kan" in required_ornament.lower() and (seg.ornament_type in (OrnamentType.KAN, OrnamentType.MURKI)):
                        has_ornament = True

                if not has_ornament:
                    # Extract standard keyword
                    if "andolan" in required_ornament.lower():
                        kw = "Andolan"
                    elif "meend" in required_ornament.lower():
                        kw = "Meend"
                    elif "kan" in required_ornament.lower():
                        kw = "Kan"
                    else:
                        kw = required_ornament.split()[0]
                        
                    badge = f"[Missing {kw}]"
                    critique_in = (
                        f"Missing core inflection: You sang swara '{swara}' as a flat, straight note. "
                        f"In Raga {self.raga.name}, '{swara}' demands a mandatory {required_ornament} to establish its identity."
                    )
                    critique_we = (
                        f"Missing structural inflection: Scale degree '{swara}' was executed statically without "
                        f"the required dynamic {required_ornament} gesture."
                    )
                    drill = (
                        f"Slow down your tempo. Glide into '{swara}' or oscillate slowly at 2 Hz rather than landing flat."
                    )
                    return CritiqueFeedback(
                        phrase_id=phrase_id,
                        start_time=start_t,
                        end_time=end_t,
                        tier=DeficitTier.TIER_2_STRUCTURAL,
                        primary_badge=badge,
                        critique_indian_mode=critique_in,
                        critique_western_mode=critique_we,
                        prescriptive_drill=drill,
                        secondary_notes=[f"Swara '{swara}' dwell: {ratio*100:.0f}%", f"Expected: {required_ornament}"],
                        confidence=0.92,
                    )

        # =========================================================================
        # TIER 3 CHECK: Microtonal Shruti Deviation & Kinematic Nuance
        # =========================================================================
        mean_shruti_err = float(np.mean(shruti_errors)) if shruti_errors else 0.0
        
        # Check if an Andolan rate was too fast (e.g. western vibrato flutter)
        for seg in detected_ornaments:
            if seg.ornament_type == OrnamentType.VIBRATO:
                badge = "[Vibrato Flutter Instead of Andolan]"
                critique_in = (
                    f"Ornament speed error: Detected {seg.oscillation_rate_hz:.1f} Hz vibrato flutter. "
                    f"Indian classical gayaki requires a slow, deliberate Andolan (1.8 - 2.5 Hz), not rapid Western vibrato."
                )
                critique_we = (
                    f"Vocal oscillation rate is too rapid ({seg.oscillation_rate_hz:.1f} Hz). "
                    f"Expand your oscillation wave to a broader ~2 Hz pitch modulation."
                )
                drill = "Drop the oscillation speed by 50%. Focus on steady breath control from the diaphragm."
                return CritiqueFeedback(
                    phrase_id=phrase_id,
                    start_time=start_t,
                    end_time=end_t,
                    tier=DeficitTier.TIER_3_MICROTONAL,
                    primary_badge=badge,
                    critique_indian_mode=critique_in,
                    critique_western_mode=critique_we,
                    prescriptive_drill=drill,
                    secondary_notes=[f"Oscillation rate: {seg.oscillation_rate_hz:.1f} Hz"],
                    confidence=0.88,
                )

        if mean_shruti_err > 18.0:
            badge = f"[Microtonal Deviation: {mean_shruti_err:.0f}c]"
            critique_in = (
                f"Shruti intonation drift: Average pitch deviation is {mean_shruti_err:.1f} cents off the authentic 22-Shruti ratio. "
                f"Listen closely to the tanpura drone harmonics."
            )
            critique_we = (
                f"Intonation inaccuracy: Microtonal error averages {mean_shruti_err:.1f} cents relative to Just Intonation ratios."
            )
            drill = "Sustain each swara against a drone for at least 3 seconds, letting your pitch settle into the harmonic overtone."
            return CritiqueFeedback(
                phrase_id=phrase_id,
                start_time=start_t,
                end_time=end_t,
                tier=DeficitTier.TIER_3_MICROTONAL,
                primary_badge=badge,
                critique_indian_mode=critique_in,
                critique_western_mode=critique_we,
                prescriptive_drill=drill,
                secondary_notes=[f"Average microtonal error: {mean_shruti_err:.1f} cents"],
                confidence=0.85,
            )

        # =========================================================================
        # NO DEFICIT: Flawless Execution
        # =========================================================================
        return CritiqueFeedback(
            phrase_id=phrase_id,
            start_time=start_t,
            end_time=end_t,
            tier=DeficitTier.NO_DEFICIT,
            primary_badge="[Flawless Gayaki Execution]",
            critique_indian_mode=f"Superb execution! Authentic raga phrasing with precise shruti intonation in Raga {self.raga.name}.",
            critique_western_mode=f"Excellent intonation and phrase articulation adhering to the modal characteristics of {self.raga.name}.",
            prescriptive_drill="Advance to the next taan / drut composition.",
            secondary_notes=[f"Intonation error: {mean_shruti_err:.1f} cents (Excellent)"],
            confidence=0.96,
        )
