"""
Raga Similarity, Contrast, and Confusion Matrix Engine for Song Lab.
Identifies:
1. Shared swara sets and Jaccard scale similarity.
2. Distinctive discriminating swaras (Bhedak Swaras).
3. Vadi/Samvadi shifts and phrase trajectory divergences.
4. Classical allied ragas (Samprakritik Ragas) and common confusion traps.
"""

from typing import Dict, List, Optional, Tuple
from src.raga_matcher import RAGA_DATABASE, RagaDefinition, SWARA_TO_SEMITONE


class RagaComparator:
    """
    Computes musicological similarity, discriminating swaras, and confusion matrices
    across all 56 curated ragas.
    """

    def __init__(self, raga_db: Optional[List[RagaDefinition]] = None):
        self.raga_db = raga_db or RAGA_DATABASE
        self.raga_map: Dict[str, RagaDefinition] = {r.name.lower(): r for r in self.raga_db}

    def get_raga(self, name: str) -> Optional[RagaDefinition]:
        clean = name.strip().lower()
        if clean in self.raga_map:
            return self.raga_map[clean]
        for k, v in self.raga_map.items():
            if clean in k or k in clean:
                return v
        return None

    def compare_pair(self, raga1_name: str, raga2_name: str) -> Dict:
        """
        Performs in-depth comparative musicological analysis between two ragas.
        """
        r1 = self.get_raga(raga1_name)
        r2 = self.get_raga(raga2_name)
        if not r1 or not r2:
            return {"error": f"One or both ragas not found: '{raga1_name}', '{raga2_name}'"}

        set1 = set(r1.allowed_swaras)
        set2 = set(r2.allowed_swaras)

        intersection = set1.intersection(set2)
        union = set1.union(set2)
        jaccard_scale = len(intersection) / float(len(union)) if union else 1.0

        r1_exclusive = sorted(list(set1 - set2))
        r2_exclusive = sorted(list(set2 - set1))

        # Check Vadi / Samvadi contrast
        same_vadi = r1.vadi == r2.vadi
        same_samvadi = r1.samvadi == r2.samvadi

        # Discriminating points (Bhedak Lakshana)
        discriminating_factors = []
        if r1_exclusive:
            discriminating_factors.append(
                f"{r1.name} includes swara(s) {', '.join(r1_exclusive)} which are strictly forbidden in {r2.name}."
            )
        if r2_exclusive:
            discriminating_factors.append(
                f"{r2.name} includes swara(s) {', '.join(r2_exclusive)} which are strictly forbidden in {r1.name}."
            )
        if not same_vadi:
            discriminating_factors.append(
                f"Vadi shift: {r1.name} centers on '{r1.vadi}', while {r2.name} centers on '{r2.vadi}'."
            )
        if not same_samvadi:
            discriminating_factors.append(
                f"Samvadi shift: {r1.name} rests on '{r1.samvadi}', while {r2.name} rests on '{r2.samvadi}'."
            )
        if r1.mandatory_ornaments != r2.mandatory_ornaments:
            discriminating_factors.append(
                f"Gayaki inflections differ: {r1.name} requires {r1.mandatory_ornaments or 'linear meends'}, whereas {r2.name} requires {r2.mandatory_ornaments or 'linear meends'}."
            )

        # Trap advice for vocalists
        confusion_risk = "High" if jaccard_scale >= 0.70 and len(intersection) >= 5 else ("Moderate" if jaccard_scale >= 0.50 else "Low")

        return {
            "raga1": {
                "name": r1.name,
                "tradition": r1.tradition,
                "thaat_or_mela": r1.thaat_or_mela,
                "vadi": r1.vadi,
                "samvadi": r1.samvadi,
                "allowed_swaras": r1.allowed_swaras,
                "varjya_swaras": r1.varjya_swaras,
            },
            "raga2": {
                "name": r2.name,
                "tradition": r2.tradition,
                "thaat_or_mela": r2.thaat_or_mela,
                "vadi": r2.vadi,
                "samvadi": r2.samvadi,
                "allowed_swaras": r2.allowed_swaras,
                "varjya_swaras": r2.varjya_swaras,
            },
            "metrics": {
                "scale_jaccard_similarity": round(jaccard_scale, 3),
                "common_swaras_count": len(intersection),
                "common_swaras": sorted(list(intersection)),
                "r1_exclusive_swaras": r1_exclusive,
                "r2_exclusive_swaras": r2_exclusive,
                "confusion_risk": confusion_risk,
            },
            "discriminating_factors": discriminating_factors,
            "vocalist_advice": (
                f"When transitioning or practicing, anchor firmly on {r1.name}'s Vadi '{r1.vadi}'. "
                f"Be cautious of {', '.join(r2_exclusive) if r2_exclusive else 'scalar crossovers'} to avoid slipping into {r2.name}."
            )
        }

    def find_allied_ragas(self, target_raga_name: str, top_k: int = 4) -> List[Dict]:
        """
        Finds the most musically similar / confusable ragas for a given target raga.
        """
        target = self.get_raga(target_raga_name)
        if not target:
            return []

        target_set = set(target.allowed_swaras)
        similarities = []

        for r in self.raga_db:
            if r.name == target.name:
                continue
            r_set = set(r.allowed_swaras)
            intersection = target_set.intersection(r_set)
            union = target_set.union(r_set)
            jaccard = len(intersection) / float(len(union)) if union else 0.0

            # Bonus if same Thaat/Mela
            thaat_bonus = 0.15 if r.thaat_or_mela == target.thaat_or_mela else 0.0
            # Bonus if same Vadi
            vadi_bonus = 0.10 if r.vadi == target.vadi else 0.0

            total_sim = min(1.0, jaccard * 0.75 + thaat_bonus + vadi_bonus)
            similarities.append((total_sim, jaccard, r))

        similarities.sort(key=lambda x: x[0], reverse=True)

        results = []
        for sim, jaccard, r in similarities[:top_k]:
            results.append({
                "raga": r.name,
                "tradition": r.tradition,
                "thaat_or_mela": r.thaat_or_mela,
                "similarity_score": round(sim, 2),
                "scale_overlap": round(jaccard, 2),
                "vadi": r.vadi,
                "samvadi": r.samvadi,
                "discriminating_note": next((s for s in r.allowed_swaras if s not in target_set), "Phrasing / Chalan"),
            })
        return results
