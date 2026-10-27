"""
Raga Identification, Pitch Class Distribution (PCD/PCDD), and Pakad Matcher for Song Lab.
Implements:
1. Continuous Pitch Class Distribution (PCD) and Transition Dyad Distribution (PCDD) (Chordia & Rae 2007).
2. Curated 30-Raga Knowledge Base (Arohana, Avarohana, Vadi, Samvadi, Varjya, Pakad, Mandatory Ornaments).
3. Dynamic Subsequence Phrase Matcher (Pakad DTW / Levenshtein alignment).
4. Multi-Evidence Raga Scoring and Ranking Engine.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np


@dataclass
class RagaDefinition:
    name: str
    tradition: str  # 'Hindustani' or 'Carnatic'
    thaat_or_mela: str
    arohana: List[str]      # e.g. ['S', 'R', 'G', 'P', 'D', 'S*']
    avarohana: List[str]    # e.g. ['S*', 'D', 'P', 'G', 'R', 'S']
    vadi: str
    samvadi: str
    varjya_swaras: List[str]  # Forbidden swaras
    pakad_phrases: List[List[str]]  # Canonical melodic signatures
    mandatory_ornaments: Dict[str, str]  # e.g. {'g': 'Andolan', 'd': 'Andolan'}
    allowed_swaras: List[str] = field(default_factory=list)

    def __post_init__(self):
        # Infer allowed swaras from arohana and avarohana
        swaras = set()
        for note in self.arohana + self.avarohana:
            clean = note.replace("*", "").replace(".", "")
            swaras.add(clean)
        self.allowed_swaras = sorted(list(swaras))


# Canonical 12-Swara indexing
SWARA_TO_SEMITONE = {
    "S": 0, "r": 1, "R": 2, "g": 3, "G": 4, "m": 5, "M": 6,
    "P": 7, "d": 8, "D": 9, "n": 10, "N": 11,
}
SEMITONE_TO_SWARA = {v: k for k, v in SWARA_TO_SEMITONE.items()}


# 56 Curated Foundational Ragas (Hindustani & Carnatic)
RAGA_DATABASE: List[RagaDefinition] = [
    # --- HINDUSTANI: KALYAN THAAT ---
    RagaDefinition(
        name="Yaman",
        tradition="Hindustani",
        thaat_or_mela="Kalyan",
        arohana=["N.", "R", "G", "M", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "M", "G", "R", "S"],
        vadi="G",
        samvadi="N",
        varjya_swaras=["r", "g", "m", "d", "n"],
        pakad_phrases=[["N.", "R", "G"], ["M", "R", "G", "R", "S"], ["P", "M", "D", "P", "M", "G"]],
        mandatory_ornaments={"M": "Meend to P or G", "R": "Kan of G"},
    ),
    RagaDefinition(
        name="Bhupali",
        tradition="Hindustani",
        thaat_or_mela="Kalyan",
        arohana=["S", "R", "G", "P", "D", "S*"],
        avarohana=["S*", "D", "P", "G", "R", "S"],
        vadi="G",
        samvadi="D",
        varjya_swaras=["r", "g", "m", "M", "d", "n", "N"],
        pakad_phrases=[["G", "R", "P", "G"], ["G", "R", "S", "D."], ["S", "R", "G", "P", "G", "R", "S"]],
        mandatory_ornaments={"P": "Meend to G", "D": "Meend to P"},
    ),
    RagaDefinition(
        name="Chhayanat",
        tradition="Hindustani",
        thaat_or_mela="Kalyan",
        arohana=["S", "R", "G", "m", "P", "D", "N", "S*"],
        avarohana=["S*", "D", "P", "M", "P", "R", "G", "m", "R", "S"],
        vadi="P",
        samvadi="R",
        varjya_swaras=["r", "g", "d", "n"],
        pakad_phrases=[["P", "R", "G", "m", "R", "S"], ["m", "P", "D", "P"], ["P", "M", "P", "R"]],
        mandatory_ornaments={"P": "Meend leap to R (P-R)", "M": "Teevra Ma touch in P-M-P"},
    ),
    RagaDefinition(
        name="Kedar",
        tradition="Hindustani",
        thaat_or_mela="Kalyan",
        arohana=["S", "m", "m", "P", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "M", "P", "D", "P", "m", "S", "R", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["r", "g", "d", "n"],
        pakad_phrases=[["S", "m", "m", "P"], ["M", "P", "D", "P", "m"], ["m", "P", "D", "P", "m", "S", "R", "S"]],
        mandatory_ornaments={"m": "Shuddha Madhyam repetition and Nyasa", "M": "Teevra Ma touch"},
    ),
    RagaDefinition(
        name="Kamod",
        tradition="Hindustani",
        thaat_or_mela="Kalyan",
        arohana=["S", "R", "P", "M", "P", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "M", "P", "D", "P", "G", "m", "R", "S"],
        vadi="P",
        samvadi="R",
        varjya_swaras=["r", "g", "d", "n"],
        pakad_phrases=[["R", "P", "M", "P", "D", "P"], ["G", "m", "R", "S"], ["S", "R", "P"]],
        mandatory_ornaments={"R": "Direct leap R to P", "G": "G-m-R-S vakra phrase"},
    ),
    RagaDefinition(
        name="Hameer",
        tradition="Hindustani",
        thaat_or_mela="Kalyan",
        arohana=["S", "R", "G", "m", "P", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "M", "P", "D", "P", "G", "m", "R", "S"],
        vadi="D",
        samvadi="G",
        varjya_swaras=["r", "g", "d", "n"],
        pakad_phrases=[["D", "N", "D", "P"], ["P", "M", "P", "D", "P"], ["G", "m", "D", "S*"]],
        mandatory_ornaments={"D": "Dhaivat dominant ascent", "M": "Teevra Ma transient"},
    ),
    RagaDefinition(
        name="Shuddha Sarang",
        tradition="Hindustani",
        thaat_or_mela="Kafi",
        arohana=["S", "R", "M", "P", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "M", "P", "m", "R", "S"],
        vadi="R",
        samvadi="P",
        varjya_swaras=["r", "g", "G", "d", "n"],
        pakad_phrases=[["R", "M", "P", "N", "S*"], ["P", "M", "P", "m", "R"], ["S", "R", "S"]],
        mandatory_ornaments={"M": "Teevra Ma in ascent, Shuddha Ma in descent"},
    ),

    # --- HINDUSTANI: BILAWAL THAAT ---
    RagaDefinition(
        name="Alhaiya Bilawal",
        tradition="Hindustani",
        thaat_or_mela="Bilawal",
        arohana=["S", "R", "G", "P", "D", "n", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "D", "n", "D", "P", "m", "G", "R", "S"],
        vadi="D",
        samvadi="G",
        varjya_swaras=["r", "g", "M", "d"],
        pakad_phrases=[["G", "R", "G", "P"], ["m", "G", "R", "S"], ["D", "n", "D", "P"]],
        mandatory_ornaments={"n": "Komal Nishad used vakra in descending phrases (D-n-D-P)"},
    ),
    RagaDefinition(
        name="Bihag",
        tradition="Hindustani",
        thaat_or_mela="Bilawal",
        arohana=["S", "G", "m", "P", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "M", "P", "m", "G", "R", "S"],
        vadi="G",
        samvadi="N",
        varjya_swaras=["r", "g", "d", "n"],
        pakad_phrases=[["P", "M", "P", "m", "G"], ["G", "m", "G", "R", "S"], ["S", "G", "P", "N"]],
        mandatory_ornaments={"M": "Teevra Ma only in conjunction with P (P-M-P-m-G)"},
    ),
    RagaDefinition(
        name="Shankara",
        tradition="Hindustani",
        thaat_or_mela="Bilawal",
        arohana=["S", "G", "P", "N", "D", "S*"],
        avarohana=["S*", "N", "D", "P", "G", "P", "G", "R", "S"],
        vadi="G",
        samvadi="N",
        varjya_swaras=["r", "g", "m", "M", "d", "n"],
        pakad_phrases=[["G", "P", "N", "D", "S*"], ["N", "D", "P", "G"], ["P", "G", "R", "S"]],
        mandatory_ornaments={"m": "Madhyam completely varjya", "G": "Forceful Gamak on Gandhar"},
    ),

    # --- HINDUSTANI: KHAMAJ THAAT ---
    RagaDefinition(
        name="Khamaj",
        tradition="Hindustani",
        thaat_or_mela="Khamaj",
        arohana=["S", "G", "m", "P", "D", "N", "S*"],
        avarohana=["S*", "n", "D", "P", "m", "G", "R", "S"],
        vadi="G",
        samvadi="N",
        varjya_swaras=["r", "g", "M", "d"],
        pakad_phrases=[["G", "m", "P", "D", "n", "D", "P"], ["m", "G", "R", "S"], ["D", "n", "D", "P"]],
        mandatory_ornaments={"n": "Komal Ni strictly in avaroha", "N": "Shuddha Ni in aroha"},
    ),
    RagaDefinition(
        name="Desh",
        tradition="Hindustani",
        thaat_or_mela="Khamaj",
        arohana=["S", "R", "m", "P", "N", "S*"],
        avarohana=["S*", "n", "D", "P", "m", "G", "R", "S"],
        vadi="R",
        samvadi="P",
        varjya_swaras=["r", "g", "M", "d"],
        pakad_phrases=[["R", "m", "P", "N", "S*"], ["R*", "n", "D", "P"], ["m", "G", "R", "G", "S", "N.", "S"]],
        mandatory_ornaments={"n": "Komal Ni in descent with Dhaivat", "R": "Nyasa on Rishabh"},
    ),
    RagaDefinition(
        name="Tilak Kamod",
        tradition="Hindustani",
        thaat_or_mela="Khamaj",
        arohana=["S", "R", "G", "S", "R", "m", "P", "D", "N", "S*"],
        avarohana=["S*", "P", "D", "m", "G", "S", "R", "G", "S", "N.", "S"],
        vadi="S",
        samvadi="P",
        varjya_swaras=["r", "g", "M", "d", "n"],
        pakad_phrases=[["S", "R", "G", "S"], ["R", "m", "P", "D", "P"], ["S*", "P", "D", "m", "G", "S"]],
        mandatory_ornaments={"S": "Vakra return S-R-G-S", "P": "Descent S* to P directly"},
    ),
    RagaDefinition(
        name="Rageshree",
        tradition="Hindustani",
        thaat_or_mela="Khamaj",
        arohana=["S", "G", "m", "D", "n", "S*"],
        avarohana=["S*", "n", "D", "m", "G", "R", "S"],
        vadi="G",
        samvadi="n",
        varjya_swaras=["r", "g", "M", "P", "d", "N"],
        pakad_phrases=[["S", "G", "m", "D", "n", "D"], ["m", "G", "R", "S"], ["G", "m", "D"]],
        mandatory_ornaments={"P": "Pancham completely omitted (varjya)", "G": "Antara Gandhar Nyasa"},
    ),
    RagaDefinition(
        name="Jaijaiwanti",
        tradition="Hindustani",
        thaat_or_mela="Khamaj",
        arohana=["S", "R", "G", "m", "P", "N", "S*"],
        avarohana=["S*", "n", "D", "P", "m", "G", "R", "g", "m", "R", "S"],
        vadi="R",
        samvadi="P",
        varjya_swaras=["r", "M", "d"],
        pakad_phrases=[["R", "g", "m", "R", "S"], ["D.", "n.", "R", "S"], ["m", "P", "n", "D", "P"]],
        mandatory_ornaments={"g": "Subtle Komal Ga in descent phrase (R-g-m-R-S)", "G": "Shuddha Ga in ascent"},
    ),

    # --- HINDUSTANI: KAFI THAAT ---
    RagaDefinition(
        name="Kafi",
        tradition="Hindustani",
        thaat_or_mela="Kafi",
        arohana=["S", "R", "g", "m", "P", "D", "n", "S*"],
        avarohana=["S*", "n", "D", "P", "m", "g", "R", "S"],
        vadi="P",
        samvadi="R",
        varjya_swaras=["r", "G", "M", "d", "N"],
        pakad_phrases=[["S", "R", "R", "g", "m", "P"], ["m", "P", "D", "n", "D", "P"], ["m", "g", "R", "S"]],
        mandatory_ornaments={"g": "Sadharana Gandhar touch", "R": "Nyasa swara"},
    ),
    RagaDefinition(
        name="Bageshri",
        tradition="Hindustani",
        thaat_or_mela="Kafi",
        arohana=["S", "R", "g", "m", "D", "n", "S*"],
        avarohana=["S*", "n", "D", "m", "g", "R", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["r", "G", "M", "d", "N"],
        pakad_phrases=[["D.", "n.", "S", "m"], ["m", "D", "n", "D", "m"], ["g", "m", "g", "R", "S"]],
        mandatory_ornaments={"m": "Nyasa steady with Kan", "D": "Meend to m"},
    ),
    RagaDefinition(
        name="Bhimpalasi",
        tradition="Hindustani",
        thaat_or_mela="Kafi",
        arohana=["n.", "S", "g", "m", "P", "n", "S*"],
        avarohana=["S*", "n", "D", "P", "m", "g", "R", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["r", "G", "M", "d", "N"],
        pakad_phrases=[["n.", "S", "m"], ["g", "m", "P", "g", "m", "g", "R", "S"], ["P", "n", "D", "P"]],
        mandatory_ornaments={"m": "Sthira Nyasa", "g": "Kan of m", "P": "Meend from m"},
    ),
    RagaDefinition(
        name="Miyan ki Malhar",
        tradition="Hindustani",
        thaat_or_mela="Kafi",
        arohana=["S", "R", "g", "m", "P", "N", "D", "N", "S*"],
        avarohana=["S*", "n", "P", "m", "P", "g", "m", "R", "S"],
        vadi="S",
        samvadi="P",
        varjya_swaras=["r", "G", "M", "d"],
        pakad_phrases=[["m", "R", "P"], ["m", "P", "n", "D", "N", "S*"], ["m", "P", "g", "m", "R", "S"]],
        mandatory_ornaments={"n": "Ati-Komal Nishad and Shuddha Nishad oscillation (N-D-N)", "g": "Andolan on Komal Gandhar"},
    ),
    RagaDefinition(
        name="Megh",
        tradition="Hindustani",
        thaat_or_mela="Kafi",
        arohana=["S", "R", "m", "P", "n", "S*"],
        avarohana=["S*", "n", "P", "m", "R", "S"],
        vadi="S",
        samvadi="P",
        varjya_swaras=["r", "g", "G", "M", "d", "D", "N"],
        pakad_phrases=[["S", "R", "m", "P"], ["m", "P", "n", "P", "m", "R", "S"], ["R", "n.", "S"]],
        mandatory_ornaments={"m": "Meend from P to m", "R": "Steady resting"},
    ),
    RagaDefinition(
        name="Vrindavani Sarang",
        tradition="Hindustani",
        thaat_or_mela="Kafi",
        arohana=["S", "R", "m", "P", "N", "S*"],
        avarohana=["S*", "n", "P", "m", "R", "S"],
        vadi="R",
        samvadi="P",
        varjya_swaras=["r", "g", "G", "M", "d", "D"],
        pakad_phrases=[["R", "m", "P", "N", "S*"], ["S*", "n", "P", "m", "R"], ["R", "m", "R", "S"]],
        mandatory_ornaments={"N": "Shuddha Ni in ascent", "n": "Komal Ni in descent", "R": "Nyasa"},
    ),

    # --- HINDUSTANI: ASAVARI THAAT ---
    RagaDefinition(
        name="Asavari",
        tradition="Hindustani",
        thaat_or_mela="Asavari",
        arohana=["S", "R", "m", "P", "d", "S*"],
        avarohana=["S*", "n", "d", "P", "m", "g", "R", "S"],
        vadi="d",
        samvadi="g",
        varjya_swaras=["r", "G", "M", "D", "N"],
        pakad_phrases=[["m", "P", "d", "P"], ["m", "P", "g", "R", "S"], ["R", "m", "P", "d"]],
        mandatory_ornaments={"d": "Komal Dhaivat oscillation", "g": "Meend from m to g to R"},
    ),
    RagaDefinition(
        name="Jaunpuri",
        tradition="Hindustani",
        thaat_or_mela="Asavari",
        arohana=["S", "R", "m", "P", "d", "n", "S*"],
        avarohana=["S*", "n", "d", "P", "m", "g", "R", "S"],
        vadi="d",
        samvadi="g",
        varjya_swaras=["r", "G", "M", "D", "N"],
        pakad_phrases=[["m", "P", "n", "d", "P"], ["m", "P", "g", "R", "S"], ["R", "m", "P"]],
        mandatory_ornaments={"n": "Komal Ni Nyasa", "d": "Meend to P"},
    ),
    RagaDefinition(
        name="Darbari Kanada",
        tradition="Hindustani",
        thaat_or_mela="Asavari",
        arohana=["S", "R", "g", "m", "P", "d", "n", "S*"],
        avarohana=["S*", "d", "n", "P", "m", "P", "g", "m", "R", "S"],
        vadi="R",
        samvadi="P",
        varjya_swaras=["r", "G", "M", "D", "N"],
        pakad_phrases=[["S", "R", "g", "R", "S"], ["d.", "n.", "P.", "m.", "P."], ["P", "g", "m", "R", "S"]],
        mandatory_ornaments={"g": "Heavy slow Andolan oscillating to R", "d": "Slow Andolan oscillating to P"},
    ),

    # --- HINDUSTANI: BHAIRAV THAAT ---
    RagaDefinition(
        name="Bhairav",
        tradition="Hindustani",
        thaat_or_mela="Bhairav",
        arohana=["S", "r", "G", "m", "P", "d", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "m", "G", "r", "S"],
        vadi="d",
        samvadi="r",
        varjya_swaras=["R", "g", "M", "D", "n"],
        pakad_phrases=[["G", "m", "d", "P"], ["m", "G", "r", "S"], ["S", "r", "r", "S"]],
        mandatory_ornaments={"r": "Andolan with slow touch of S", "d": "Andolan with slow touch of P"},
    ),
    RagaDefinition(
        name="Ahir Bhairav",
        tradition="Hindustani",
        thaat_or_mela="Bhairav",
        arohana=["S", "r", "G", "m", "P", "D", "n", "S*"],
        avarohana=["S*", "n", "D", "P", "m", "G", "r", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["R", "g", "M", "d", "N"],
        pakad_phrases=[["r", "S", "D.", "n.", "S"], ["G", "m", "P", "D", "n", "D", "P"], ["m", "G", "r", "S"]],
        mandatory_ornaments={"r": "Komal Re with Sa touch", "n": "Komal Ni with Dhaivat anchor"},
    ),
    RagaDefinition(
        name="Nat Bhairav",
        tradition="Hindustani",
        thaat_or_mela="Bhairav",
        arohana=["S", "R", "G", "m", "P", "d", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "m", "G", "R", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["r", "g", "M", "D", "n"],
        pakad_phrases=[["S", "R", "G", "m", "P"], ["d", "d", "P"], ["m", "G", "R", "S"]],
        mandatory_ornaments={"R": "Shuddha Rishabh in Purvanga", "d": "Komal Dhaivat in Uttaranga"},
    ),

    # --- HINDUSTANI: BHAIRAVI THAAT ---
    RagaDefinition(
        name="Bhairavi",
        tradition="Hindustani",
        thaat_or_mela="Bhairavi",
        arohana=["S", "r", "g", "m", "P", "d", "n", "S*"],
        avarohana=["S*", "n", "d", "P", "m", "g", "r", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["R", "G", "M", "D", "N"],
        pakad_phrases=[["m", "g", "S", "r", "S"], ["d.", "n.", "S", "r", "S"], ["m", "P", "d", "P", "m", "g", "r", "S"]],
        mandatory_ornaments={"r": "Komal Rishabh resting", "g": "Komal Gandhar glide", "d": "Komal Dhaivat glide"},
    ),
    RagaDefinition(
        name="Malkauns",
        tradition="Hindustani",
        thaat_or_mela="Bhairavi",
        arohana=["S", "g", "m", "d", "n", "S*"],
        avarohana=["S*", "n", "d", "m", "g", "m", "g", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["r", "R", "G", "M", "P", "D", "N"],
        pakad_phrases=[["m", "g", "m", "g", "S"], ["d", "n", "d", "m"], ["g", "m", "d", "n", "d", "m"]],
        mandatory_ornaments={"g": "Andolan / Gamak", "d": "Andolan", "m": "Sthira Nyasa"},
    ),

    # --- HINDUSTANI: TODI THAAT ---
    RagaDefinition(
        name="Todi",
        tradition="Hindustani",
        thaat_or_mela="Todi",
        arohana=["S", "r", "g", "M", "d", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "M", "d", "M", "g", "r", "g", "r", "S"],
        vadi="d",
        samvadi="g",
        varjya_swaras=["R", "G", "m", "D", "n"],
        pakad_phrases=[["r", "g", "r", "S"], ["M", "d", "N", "d", "M", "g"], ["r", "g", "r", "S"]],
        mandatory_ornaments={"r": "Ati-Komal Shruti touch", "g": "Ati-Komal Shruti touch", "M": "Teevra Ma glide to d"},
    ),
    RagaDefinition(
        name="Multani",
        tradition="Hindustani",
        thaat_or_mela="Todi",
        arohana=["N.", "S", "g", "M", "P", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "M", "g", "r", "S"],
        vadi="P",
        samvadi="S",
        varjya_swaras=["R", "G", "m", "D", "n"],
        pakad_phrases=[["N.", "S", "g", "M", "P"], ["M", "g", "M", "g", "r", "S"], ["P", "M", "g", "M"]],
        mandatory_ornaments={"P": "Strong Nyasa on Pancham", "M": "Teevra Ma glide to g"},
    ),
    RagaDefinition(
        name="Gurjari Todi",
        tradition="Hindustani",
        thaat_or_mela="Todi",
        arohana=["S", "r", "g", "M", "d", "N", "S*"],
        avarohana=["S*", "N", "d", "M", "d", "M", "g", "r", "g", "r", "S"],
        vadi="d",
        samvadi="g",
        varjya_swaras=["P", "R", "G", "m", "D", "n"],
        pakad_phrases=[["r", "g", "r", "S"], ["M", "d", "N", "d", "M", "g"], ["r", "g", "r", "S"]],
        mandatory_ornaments={"P": "Pancham completely varjya", "d": "Ati-komal Dhaivat Nyasa"},
    ),

    # --- HINDUSTANI: PURVI THAAT ---
    RagaDefinition(
        name="Purvi",
        tradition="Hindustani",
        thaat_or_mela="Purvi",
        arohana=["N.", "r", "G", "M", "P", "d", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "M", "G", "m", "G", "r", "S"],
        vadi="G",
        samvadi="N",
        varjya_swaras=["R", "g", "D", "n"],
        pakad_phrases=[["N.", "r", "G"], ["M", "P", "d", "P"], ["M", "G", "m", "G", "r", "S"]],
        mandatory_ornaments={"m": "Both Madhyams juxtaposed (M-G-m-G)", "d": "Komal Dhaivat resting"},
    ),
    RagaDefinition(
        name="Puriya Dhanashree",
        tradition="Hindustani",
        thaat_or_mela="Purvi",
        arohana=["N.", "r", "G", "M", "P", "d", "P", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "M", "G", "M", "r", "G", "r", "S"],
        vadi="P",
        samvadi="r",
        varjya_swaras=["R", "g", "m", "D", "n"],
        pakad_phrases=[["N.", "r", "G", "M", "P"], ["d", "P", "M", "G", "M", "r", "G"], ["r", "S"]],
        mandatory_ornaments={"P": "Pancham anchor", "r": "Ati-Komal Re glide to Sa"},
    ),
    RagaDefinition(
        name="Shree",
        tradition="Hindustani",
        thaat_or_mela="Purvi",
        arohana=["S", "r", "M", "P", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "M", "G", "r", "r", "S"],
        vadi="r",
        samvadi="P",
        varjya_swaras=["R", "g", "m", "D", "n"],
        pakad_phrases=[["S", "r", "r", "S"], ["P", "M", "d", "P"], ["M", "G", "r", "r", "S"]],
        mandatory_ornaments={"r": "Heavy slow Andolan on Komal Rishabh with Sa touch", "P": "Direct leap from r"},
    ),

    # --- HINDUSTANI: MARWA THAAT ---
    RagaDefinition(
        name="Marwa",
        tradition="Hindustani",
        thaat_or_mela="Marwa",
        arohana=["N.", "r", "G", "M", "D", "N", "r*"],
        avarohana=["r*", "N", "D", "M", "G", "r", "S"],
        vadi="r",
        samvadi="D",
        varjya_swaras=["P", "R", "g", "m", "d", "n"],
        pakad_phrases=[["D", "N", "r*", "N", "D"], ["M", "D", "M", "G", "r"], ["r", "N.", "D.", "S"]],
        mandatory_ornaments={"r": "Komal Re high pitch tension without Sa Nyasa", "M": "Teevra Ma glide to D"},
    ),
    RagaDefinition(
        name="Puriya",
        tradition="Hindustani",
        thaat_or_mela="Marwa",
        arohana=["N.", "r", "G", "M", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "M", "G", "M", "r", "G", "r", "S"],
        vadi="G",
        samvadi="N",
        varjya_swaras=["P", "R", "g", "m", "d", "n"],
        pakad_phrases=[["M.", "D.", "N.", "r", "S"], ["G", "M", "D", "M", "G"], ["M", "r", "G", "r", "S"]],
        mandatory_ornaments={"G": "Mandra/Madhya Gandhar dominant Nyasa", "M": "Teevra Ma glide"},
    ),
    RagaDefinition(
        name="Sohini",
        tradition="Hindustani",
        thaat_or_mela="Marwa",
        arohana=["S", "G", "M", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "M", "G", "M", "r", "S"],
        vadi="D",
        samvadi="G",
        varjya_swaras=["P", "R", "g", "m", "d", "n"],
        pakad_phrases=[["S*", "N", "D", "N", "D", "M", "G"], ["G", "M", "D", "N", "S*"], ["r*", "S*", "N", "D"]],
        mandatory_ornaments={"S*": "Tar Saptak dominant", "D": "High energy Dhaivat"},
    ),
    RagaDefinition(
        name="Lalit",
        tradition="Hindustani",
        thaat_or_mela="Purvi/Marwa",
        arohana=["S", "r", "G", "m", "M", "m", "d", "S*"],
        avarohana=["S*", "N", "d", "M", "m", "G", "r", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["P", "R", "g", "D", "n"],
        pakad_phrases=[["m", "M", "m", "G"], ["r", "G", "m", "d"], ["S*", "N", "d", "M", "m"]],
        mandatory_ornaments={"m": "Shuddha and Teevra Madhyams adjacent (m-M-m)", "P": "Pancham strictly varjya"},
    ),

    # --- CARNATIC MELAKARTAS & POPULAR JANYAS ---
    RagaDefinition(
        name="Mohanam",
        tradition="Carnatic",
        thaat_or_mela="28 Harikambhoji",
        arohana=["S", "R", "G", "P", "D", "S*"],
        avarohana=["S*", "D", "P", "G", "R", "S"],
        vadi="G",
        samvadi="D",
        varjya_swaras=["r", "g", "m", "M", "d", "n", "N"],
        pakad_phrases=[["G", "P", "D", "P", "G", "R", "S"], ["R", "G", "R", "S", "D."], ["P", "D", "S*", "D", "P"]],
        mandatory_ornaments={"G": "Kampitam oscillation", "D": "Nokku from S*"},
    ),
    RagaDefinition(
        name="Kalyani",
        tradition="Carnatic",
        thaat_or_mela="65 Mechakalyani",
        arohana=["S", "R", "G", "M", "P", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "M", "G", "R", "S"],
        vadi="G",
        samvadi="N",
        varjya_swaras=["r", "g", "m", "d", "n"],
        pakad_phrases=[["G", "M", "P", "D", "N", "S*"], ["N", "D", "P", "M", "G", "R", "S"], ["R", "G", "M", "P"]],
        mandatory_ornaments={"R": "Kampita", "G": "Kampita", "M": "Prati Madhyamam"},
    ),
    RagaDefinition(
        name="Mayamalavagowla",
        tradition="Carnatic",
        thaat_or_mela="15 Mayamalavagowla",
        arohana=["S", "r", "G", "m", "P", "d", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "m", "G", "r", "S"],
        vadi="P",
        samvadi="S",
        varjya_swaras=["R", "g", "M", "D", "n"],
        pakad_phrases=[["S", "r", "G", "m", "P"], ["P", "d", "N", "S*"], ["S*", "N", "d", "P", "m", "G", "r", "S"]],
        mandatory_ornaments={"r": "Pure Shuddha Rishabham (112c)", "d": "Pure Shuddha Dhaivatam (814c)"},
    ),
    RagaDefinition(
        name="Shankarabharanam",
        tradition="Carnatic",
        thaat_or_mela="29 Dheerasankarabharanam",
        arohana=["S", "R", "G", "m", "P", "D", "N", "S*"],
        avarohana=["S*", "N", "D", "P", "m", "G", "R", "S"],
        vadi="G",
        samvadi="D",
        varjya_swaras=["r", "g", "M", "d", "n"],
        pakad_phrases=[["S", "R", "G", "m", "P"], ["P", "D", "N", "S*"], ["S*", "N", "D", "P"]],
        mandatory_ornaments={"G": "Antara Gandharam", "N": "Kakali Nishadam"},
    ),
    RagaDefinition(
        name="Hindolam",
        tradition="Carnatic",
        thaat_or_mela="20 Natabhairavi",
        arohana=["S", "g", "m", "d", "n", "S*"],
        avarohana=["S*", "n", "d", "m", "g", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["r", "R", "G", "M", "P", "D", "N"],
        pakad_phrases=[["S", "g", "m", "d", "n"], ["S*", "n", "d", "m", "g", "S"], ["m", "d", "m", "g", "S"]],
        mandatory_ornaments={"g": "Sadharana Gandharam Kampita", "d": "Shuddha Dhaivatam Kampita"},
    ),
    RagaDefinition(
        name="Kharaharapriya",
        tradition="Carnatic",
        thaat_or_mela="22 Kharaharapriya",
        arohana=["S", "R", "g", "m", "P", "D", "n", "S*"],
        avarohana=["S*", "n", "D", "P", "m", "g", "R", "S"],
        vadi="P",
        samvadi="R",
        varjya_swaras=["r", "G", "M", "d", "N"],
        pakad_phrases=[["S", "R", "g", "m", "P"], ["P", "D", "n", "D", "P"], ["m", "g", "R", "S"]],
        mandatory_ornaments={"R": "Chatusruti Rishabham", "g": "Sadharana Gandharam Kampita"},
    ),
    RagaDefinition(
        name="Hanumatodi",
        tradition="Carnatic",
        thaat_or_mela="8 Hanumatodi",
        arohana=["S", "r", "g", "m", "P", "d", "n", "S*"],
        avarohana=["S*", "n", "d", "P", "m", "g", "r", "S"],
        vadi="d",
        samvadi="g",
        varjya_swaras=["R", "G", "M", "D", "N"],
        pakad_phrases=[["S", "r", "g", "m", "P"], ["d", "n", "d", "P"], ["m", "g", "r", "S"]],
        mandatory_ornaments={"g": "Heavy Kampitam", "d": "Heavy Kampitam", "r": "Shuddha Rishabham oscillation"},
    ),
    RagaDefinition(
        name="Harikambhoji",
        tradition="Carnatic",
        thaat_or_mela="28 Harikambhoji",
        arohana=["S", "R", "G", "m", "P", "D", "n", "S*"],
        avarohana=["S*", "n", "D", "P", "m", "G", "R", "S"],
        vadi="P",
        samvadi="S",
        varjya_swaras=["r", "g", "M", "d", "N"],
        pakad_phrases=[["S", "R", "G", "m", "P"], ["D", "n", "D", "P"], ["m", "G", "R", "S"]],
        mandatory_ornaments={"n": "Kaisiki Nishadam", "G": "Antara Gandharam"},
    ),
    RagaDefinition(
        name="Natabhairavi",
        tradition="Carnatic",
        thaat_or_mela="20 Natabhairavi",
        arohana=["S", "R", "g", "m", "P", "d", "n", "S*"],
        avarohana=["S*", "n", "d", "P", "m", "g", "R", "S"],
        vadi="P",
        samvadi="R",
        varjya_swaras=["r", "G", "M", "D", "N"],
        pakad_phrases=[["S", "R", "g", "m", "P"], ["d", "n", "d", "P"], ["m", "g", "R", "S"]],
        mandatory_ornaments={"d": "Shuddha Dhaivatam", "g": "Sadharana Gandharam"},
    ),
    RagaDefinition(
        name="Charukesi",
        tradition="Carnatic",
        thaat_or_mela="26 Charukesi",
        arohana=["S", "R", "G", "m", "P", "d", "n", "S*"],
        avarohana=["S*", "n", "d", "P", "m", "G", "R", "S"],
        vadi="P",
        samvadi="S",
        varjya_swaras=["r", "g", "M", "D", "N"],
        pakad_phrases=[["S", "R", "G", "m", "P"], ["P", "d", "n", "d", "P"], ["m", "G", "R", "S"]],
        mandatory_ornaments={"G": "Major 3rd (Antara Gandharam)", "d": "Minor 6th (Shuddha Dhaivatam)"},
    ),
    RagaDefinition(
        name="Kamavardhani",
        tradition="Carnatic",
        thaat_or_mela="51 Kamavardhani",
        arohana=["S", "r", "G", "M", "P", "d", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "M", "G", "r", "S"],
        vadi="P",
        samvadi="S",
        varjya_swaras=["R", "g", "m", "D", "n"],
        pakad_phrases=[["S", "r", "G", "M", "P"], ["d", "N", "S*"], ["S*", "N", "d", "P", "M", "G", "r", "S"]],
        mandatory_ornaments={"r": "Shuddha Rishabham Kampita", "M": "Prati Madhyamam"},
    ),
    RagaDefinition(
        name="Simhendramadhyamam",
        tradition="Carnatic",
        thaat_or_mela="57 Simhendramadhyamam",
        arohana=["S", "R", "g", "M", "P", "d", "N", "S*"],
        avarohana=["S*", "N", "d", "P", "M", "g", "R", "S"],
        vadi="P",
        samvadi="S",
        varjya_swaras=["r", "G", "m", "D", "n"],
        pakad_phrases=[["S", "R", "g", "M", "P"], ["P", "d", "N", "S*"], ["S*", "N", "d", "P", "M", "g", "R", "S"]],
        mandatory_ornaments={"M": "Prati Madhyamam Nyasa", "g": "Sadharana Gandharam"},
    ),
    RagaDefinition(
        name="Shanmukhapriya",
        tradition="Carnatic",
        thaat_or_mela="56 Shanmukhapriya",
        arohana=["S", "R", "g", "M", "P", "d", "n", "S*"],
        avarohana=["S*", "n", "d", "P", "M", "g", "R", "S"],
        vadi="P",
        samvadi="R",
        varjya_swaras=["r", "G", "m", "D", "N"],
        pakad_phrases=[["S", "R", "g", "M", "P"], ["d", "n", "d", "P"], ["M", "g", "R", "S"]],
        mandatory_ornaments={"M": "Prati Madhyamam", "n": "Kaisiki Nishadam Kampita"},
    ),
    RagaDefinition(
        name="Hamsadhwani",
        tradition="Carnatic",
        thaat_or_mela="29 Dheerasankarabharanam",
        arohana=["S", "R", "G", "P", "N", "S*"],
        avarohana=["S*", "N", "P", "G", "R", "S"],
        vadi="P",
        samvadi="S",
        varjya_swaras=["r", "g", "m", "M", "d", "D", "n"],
        pakad_phrases=[["S", "R", "G", "P", "N", "S*"], ["N", "P", "G", "R", "S"], ["G", "P", "N", "P"]],
        mandatory_ornaments={"G": "Antara Gandharam", "N": "Kakali Nishadam"},
    ),
    RagaDefinition(
        name="Abhogi",
        tradition="Carnatic",
        thaat_or_mela="22 Kharaharapriya",
        arohana=["S", "R", "g", "m", "D", "S*"],
        avarohana=["S*", "D", "m", "g", "R", "S"],
        vadi="m",
        samvadi="S",
        varjya_swaras=["r", "G", "M", "P", "d", "n", "N"],
        pakad_phrases=[["S", "R", "g", "m", "D"], ["S*", "D", "m", "g", "R", "S"], ["g", "m", "D", "m"]],
        mandatory_ornaments={"P": "Pancham varjya", "D": "Chatusruti Dhaivatam"},
    ),
    RagaDefinition(
        name="Madhyamavati",
        tradition="Carnatic",
        thaat_or_mela="22 Kharaharapriya",
        arohana=["S", "R", "m", "P", "n", "S*"],
        avarohana=["S*", "n", "P", "m", "R", "S"],
        vadi="P",
        samvadi="R",
        varjya_swaras=["r", "g", "G", "M", "d", "D", "N"],
        pakad_phrases=[["S", "R", "m", "P"], ["P", "n", "P", "m", "R", "S"], ["R", "m", "P", "n", "S*"]],
        mandatory_ornaments={"R": "Chatusruti Rishabham Kampita", "n": "Kaisiki Nishadam Kampita"},
    ),
    RagaDefinition(
        name="Saveri",
        tradition="Carnatic",
        thaat_or_mela="15 Mayamalavagowla",
        arohana=["S", "r", "m", "P", "d", "S*"],
        avarohana=["S*", "N", "d", "P", "m", "G", "r", "S"],
        vadi="d",
        samvadi="r",
        varjya_swaras=["R", "g", "M", "D", "n"],
        pakad_phrases=[["S", "r", "m", "P", "d", "S*"], ["S*", "N", "d", "P", "m", "G", "r", "S"], ["r", "m", "P", "d"]],
        mandatory_ornaments={"r": "Shuddha Rishabham", "d": "Shuddha Dhaivatam", "G": "Gandharam strictly in descent"},
    ),
]


class RagaMatcher:
    """
    Raga classifier using Pitch Class Distributions, Forbidden Swara Penalties,
    and Dynamic Phrase Alignment.
    """

    def __init__(self, raga_db: Optional[List[RagaDefinition]] = None):
        self.raga_db = raga_db if raga_db is not None else RAGA_DATABASE

    def compute_pcd(
        self,
        cents: np.ndarray,
        weights: Optional[np.ndarray] = None,
        num_bins: int = 12,
    ) -> np.ndarray:
        """
        Computes 12-dimensional Pitch Class Distribution (PCD) vector
        normalized so sum(pcd) = 1.0.
        Optionally accepts frame weights (e.g. inverse velocity weighting).
        """
        valid = ~np.isnan(cents)
        if not np.any(valid):
            return np.ones(num_bins) / float(num_bins)
            
        c_valid = cents[valid]
        w_valid = weights[valid] if weights is not None else np.ones_like(c_valid)
        w_valid = np.nan_to_num(w_valid, nan=0.0)
        
        c_mod = c_valid % 1200.0
        bin_indices = np.round(c_mod / 100.0).astype(int) % 12
        
        counts = np.bincount(bin_indices, weights=w_valid, minlength=12)
        pcd = counts.astype(np.float64)
        total = np.sum(pcd)
        if total > 0:
            pcd /= total
        return pcd

    def compute_pcdd(self, cents: np.ndarray, lag_steps: int = 25) -> np.ndarray:
        """
        Computes 12x12 Pitch Class Dyad Distribution (transition matrix) (Chordia & Rae 2007).
        lag_steps: 25 steps @ 10ms = 250ms melodic transition interval.
        """
        pcdd = np.zeros((12, 12), dtype=np.float64)
        valid = ~np.isnan(cents)
        if len(cents) <= lag_steps:
            return pcdd
            
        c_mod = cents % 1200.0
        bins = np.round(c_mod / 100.0).astype(int) % 12
        
        for t in range(len(cents) - lag_steps):
            if valid[t] and valid[t + lag_steps]:
                i = bins[t]
                j = bins[t + lag_steps]
                pcdd[i, j] += 1.0
                
        total = np.sum(pcdd)
        if total > 0:
            pcdd /= total
        return pcdd

    def align_pakad(self, sung_swaras: List[str], target_phrase: List[str]) -> float:
        """
        Calculates normalized substring alignment score between sung swaras and target pakad.
        Returns score in [0.0, 1.0].
        """
        if not sung_swaras or not target_phrase:
            return 0.0
            
        clean_sung = [s.replace("*", "").replace(".", "") for s in sung_swaras]
        clean_target = [s.replace("*", "").replace(".", "") for s in target_phrase]
        
        target_str = "".join(clean_target)
        sung_str = "".join(clean_sung)
        
        # Exact substring match
        if target_str in sung_str:
            return 1.0
            
        # Sliding-window match
        m = len(clean_target)
        best_match_ratio = 0.0
        
        for i in range(max(1, len(clean_sung) - m + 1)):
            window = clean_sung[i : i + m]
            matches = sum(1 for w, t in zip(window, clean_target) if w == t)
            ratio = matches / float(m)
            if ratio > best_match_ratio:
                best_match_ratio = ratio
                
        return best_match_ratio

    def match_raga(
        self,
        cents: np.ndarray,
        sung_swaras: Optional[List[str]] = None,
        velocity: Optional[np.ndarray] = None,
        top_k: int = 5,
    ) -> List[Dict]:
        """
        Scores candidate ragas based on:
        1. PCD profile correlation (40%)
        2. Forbidden swara penalty on steady frames (35%)
        3. Pakad phrase match (25%)
        """
        # Inverse velocity weighting: high weight for sustained notes, lower weight for fast glides
        weights = None
        if velocity is not None:
            weights = 1.0 / (1.0 + (np.abs(velocity) / 180.0) ** 2)
            
        pcd = self.compute_pcd(cents, weights=weights)
        results = []
        
        for raga in self.raga_db:
            # 1. Scale template
            allowed_indices = [SWARA_TO_SEMITONE[s] for s in raga.allowed_swaras if s in SWARA_TO_SEMITONE]
            varjya_indices = [SWARA_TO_SEMITONE[s] for s in raga.varjya_swaras if s in SWARA_TO_SEMITONE]
            
            # Energy in allowed notes vs forbidden notes
            allowed_energy = np.sum(pcd[allowed_indices])
            varjya_energy = np.sum(pcd[varjya_indices]) if varjya_indices else 0.0
            
            # Forbidden penalty is steep
            scale_score = np.clip(allowed_energy - (2.5 * varjya_energy), 0.0, 1.0)
            
            # 2. Pakad alignment score
            pakad_score = 0.0
            if sung_swaras and raga.pakad_phrases:
                phrase_scores = [self.align_pakad(sung_swaras, p) for p in raga.pakad_phrases]
                pakad_score = max(phrase_scores) if phrase_scores else 0.0
            else:
                pakad_score = 0.5  # Neutral when no discrete phrases provided
                
            # 3. Vadi & Samvadi prominence bonus
            vadi_idx = SWARA_TO_SEMITONE.get(raga.vadi)
            vadi_score = pcd[vadi_idx] if vadi_idx is not None else 0.0
            vadi_bonus = min(1.0, vadi_score * 3.0)
            
            # Combined Bayesian match score
            total_score = (
                0.40 * scale_score +
                0.35 * (1.0 - min(1.0, varjya_energy * 3.0)) +
                0.15 * pakad_score +
                0.10 * vadi_bonus
            )
            
            results.append({
                "raga": raga.name,
                "tradition": raga.tradition,
                "thaat_or_mela": raga.thaat_or_mela,
                "score": round(float(total_score), 3),
                "scale_score": round(float(scale_score), 3),
                "varjya_leak": round(float(varjya_energy), 3),
                "pakad_score": round(float(pakad_score), 3),
                "vadi": raga.vadi,
                "samvadi": raga.samvadi,
                "mandatory_ornaments": raga.mandatory_ornaments,
            })
            
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
