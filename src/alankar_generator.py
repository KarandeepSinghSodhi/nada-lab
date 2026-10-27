"""
Automated Alankar, Palta, and Sādhanā Drill Generator for Song Lab.
Generates structured classical vocal exercises projected through the exact
scale degrees, Arohana, and Avarohana of all 56 ragas.
"""

from typing import Dict, List, Optional, Tuple
from src.raga_matcher import RAGA_DATABASE, RagaDefinition
from src.guru_synthesizer import synthesize_guru_phrase


ALANKAR_PATTERNS = {
    "triad_step": {
        "name": "Triad Stepping (3-Note Runs)",
        "formula": [0, 1, 2],
        "description": "Progressive 3-swara ascent and descent building agile vocal transitions.",
    },
    "turn_around": {
        "name": "Symmetrical Return (Palta Turn)",
        "formula": [0, 1, 0],
        "description": "Pivot drill establishing swara sthirata (pitch stability) and quick return.",
    },
    "tetrad_cluster": {
        "name": "Tetrad Cluster (4-Note Runs)",
        "formula": [0, 1, 2, 3],
        "description": "Extended 4-swara runs training diaphragm breath support across octave registers.",
    },
    "third_leap": {
        "name": "Skips & Leaps (Chhoot Intervals)",
        "formula": [0, 2],
        "description": "Intervallic leaps training muscular vocal cord flexibility without sliding off-pitch.",
    },
    "zigzag_vakra": {
        "name": "Vakra Wave (Zigzag 4-Step)",
        "formula": [0, 2, 1, 3],
        "description": "Non-linear weaving run training cognitive raga agility and rapid pitch control.",
    },
}


class AlankarGenerator:
    """
    Constructs raga-grammatical practice drills (Paltas) for singers.
    """

    def __init__(self, raga_db: Optional[List[RagaDefinition]] = None):
        self.raga_db = raga_db or RAGA_DATABASE
        self.raga_map = {r.name.lower(): r for r in self.raga_db}

    def _get_scale_degrees(self, raga: RagaDefinition) -> Tuple[List[str], List[str]]:
        """
        Returns full extended Arohana and Avarohana note lists spanning lower, middle,
        and higher octaves.
        """
        aroha = raga.arohana or raga.allowed_swaras
        avaroha = raga.avarohana or list(reversed(raga.allowed_swaras))

        # Ensure middle octave wraps cleanly
        aroha_extended = list(aroha) + ["S'"]
        avaroha_extended = ["S'"] + list(avaroha)
        return aroha_extended, avaroha_extended

    def generate_drill(
        self,
        raga_name: str = "Yaman",
        pattern_key: str = "triad_step",
        sa_hz: float = 146.83,
        synthesize_audio: bool = False,
    ) -> Dict:
        """
        Generates full Palta exercise for given raga and pattern.
        """
        raga = self.raga_map.get(raga_name.lower())
        if not raga:
            raga = self.raga_map.get("yaman", self.raga_db[0])

        pattern_meta = ALANKAR_PATTERNS.get(pattern_key, ALANKAR_PATTERNS["triad_step"])
        offsets = pattern_meta["formula"]
        k = len(offsets)

        aroha_scale, avaroha_scale = self._get_scale_degrees(raga)

        # Build Arohana Phrases
        arohana_phrases: List[List[str]] = []
        n_a = len(aroha_scale)
        max_idx = max(offsets)
        for i in range(n_a - max_idx):
            phrase = [aroha_scale[i + off] for off in offsets]
            arohana_phrases.append(phrase)

        # Build Avarohana Phrases
        avarohana_phrases: List[List[str]] = []
        n_av = len(avaroha_scale)
        for i in range(n_av - max_idx):
            phrase = [avaroha_scale[i + off] for off in offsets]
            avarohana_phrases.append(phrase)

        # Flattened sequence for practice
        full_sung_sequence: List[str] = []
        for p in arohana_phrases:
            full_sung_sequence.extend(p)
        for p in avarohana_phrases:
            full_sung_sequence.extend(p)

        result = {
            "raga": raga.name,
            "tradition": raga.tradition,
            "thaat_or_mela": raga.thaat_or_mela,
            "vadi": raga.vadi,
            "samvadi": raga.samvadi,
            "pattern_key": pattern_key,
            "pattern_name": pattern_meta["name"],
            "description": pattern_meta["description"],
            "arohana_paltas": [" - ".join(p) for p in arohana_phrases],
            "avarohana_paltas": [" - ".join(p) for p in avarohana_phrases],
            "total_phrases": len(arohana_phrases) + len(avarohana_phrases),
            "pedagogical_focus": (
                f"Practice at medium tempo (Madhya Laya ~84 BPM). Emphasize Vadi '{raga.vadi}'. "
                f"Ensure clean separation of notes on open vowel 'Aa'."
            ),
        }

        if synthesize_audio and full_sung_sequence:
            # Synthesize representative ascending phrase
            sample_swaras = full_sung_sequence[:12]
            synth = synthesize_guru_phrase(sa_hz=sa_hz, swaras=sample_swaras, note_dur_sec=0.45, glide_sec=0.08)
            result["sample_audio_url"] = synth["data_url"]
            result["sample_duration_sec"] = synth["duration_sec"]

        return result
