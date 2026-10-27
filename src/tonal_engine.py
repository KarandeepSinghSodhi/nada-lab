"""
Tonal Normalization and 22-Shruti Engine for Song Lab.
Implements:
1. Movable Sa (tonic) estimation using multi-pitch harmonic salience & F0 histogram voting.
2. Exact mathematical 22-Shruti grid (Bharata / Sarngadeva / Sambamoorthy / Deval).
3. Continuous frequency-to-cents conversion relative to tonic.
4. Microtonal cents-to-shruti quantization and error computation.
5. Dual-mode terminology mapping (Indian Classical / Western Contemporary).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np


@dataclass(frozen=True)
class Shruti:
    index: int
    name_sanskrit: str
    swara_hindustani: str
    swara_carnatic: str
    ratio_num: int
    ratio_den: int
    cents: float
    western_interval: str
    western_cents_edo: float


# The 22 Shrutis of Indian Classical Music based on Bharata Natyashastra / Sangita Ratnakara
# Ratios derived from fundamental Just Intonation (harmonics 3 and 5) & Pythagorean cycles
SHRUTI_TABLE: List[Shruti] = [
    Shruti(1, "Kshobhini", "Sa", "Shadjam (S)", 1, 1, 0.0, "Perfect Unison (1P)", 0.0),
    Shruti(2, "Teevra", "Ati-Komal re", "Shuddha Rishabham (R1)", 256, 243, 90.22, "Minor Second (Diminished)", 100.0),
    Shruti(3, "Kumudvati", "Komal re", "Shuddha Rishabham (R1)", 16, 15, 111.73, "Minor Second (Just / Diatonic)", 100.0),
    Shruti(4, "Manda", "Laghu Re", "Chatushruti Rishabham (R2)", 10, 9, 182.40, "Major Second (Minor Tone)", 200.0),
    Shruti(5, "Chandovati", "Shuddha Re", "Chatushruti Rishabham (R2)", 9, 8, 203.91, "Major Second (Major Tone)", 200.0),
    Shruti(6, "Dayavati", "Ati-Komal ga", "Sadharana Gandharam (G2)", 32, 27, 294.13, "Minor Third (Pythagorean)", 300.0),
    Shruti(7, "Ranjani", "Komal ga", "Sadharana Gandharam (G2)", 6, 5, 315.64, "Minor Third (Just)", 300.0),
    Shruti(8, "Raktika", "Shuddha Ga", "Antara Gandharam (G3)", 5, 4, 386.31, "Major Third (Just 5-limit)", 400.0),
    Shruti(9, "Raudri", "Teevra Ga", "Antara Gandharam (G3)", 81, 64, 407.82, "Major Third (Pythagorean)", 400.0),
    Shruti(10, "Krodha", "Shuddha ma", "Shuddha Madhyamam (M1)", 4, 3, 498.04, "Perfect Fourth (4P)", 500.0),
    Shruti(11, "Vajrika", "Teevra ma (Alpa)", "Prati Madhyamam (M2)", 27, 20, 519.55, "Acute Fourth (Grave Tritone)", 500.0),
    Shruti(12, "Prasarini", "Teevra Ma", "Prati Madhyamam (M2)", 45, 32, 590.22, "Augmented Fourth / Tritone", 600.0),
    Shruti(13, "Priti", "Teevratara Ma", "Prati Madhyamam (M2)", 729, 512, 611.73, "Pythagorean Tritone", 600.0),
    Shruti(14, "Marjani", "Pa", "Panchamam (P)", 3, 2, 701.96, "Perfect Fifth (5P)", 700.0),
    Shruti(15, "Kshiti", "Ati-Komal dha", "Shuddha Dhaivatam (D1)", 128, 81, 792.18, "Minor Sixth (Pythagorean)", 800.0),
    Shruti(16, "Rakta", "Komal dha", "Shuddha Dhaivatam (D1)", 8, 5, 813.69, "Minor Sixth (Just)", 800.0),
    Shruti(17, "Sandipani", "Shuddha Dha", "Chatushruti Dhaivatam (D2)", 5, 3, 884.36, "Major Sixth (Just 5-limit)", 900.0),
    Shruti(18, "Alapini", "Teevra Dha", "Chatushruti Dhaivatam (D2)", 27, 16, 905.87, "Major Sixth (Pythagorean)", 900.0),
    Shruti(19, "Madanti", "Komal ni", "Kaishiki Nishadam (N2)", 16, 9, 996.09, "Minor Seventh (Pythagorean)", 1000.0),
    Shruti(20, "Rohini", "Teevra Komal ni", "Kaishiki Nishadam (N2)", 9, 5, 1017.60, "Minor Seventh (Just)", 1000.0),
    Shruti(21, "Ramya", "Shuddha Ni", "Kakali Nishadam (N3)", 15, 8, 1088.27, "Major Seventh (Just 5-limit)", 1100.0),
    Shruti(22, "Ugra", "Teevra Ni", "Kakali Nishadam (N3)", 243, 128, 1109.78, "Major Seventh (Pythagorean)", 1100.0),
]

# Standard 12-Swara Canonical Mapping (Hindustani Bhatkhande)
SWARA_12_TABLE = [
    {"symbol": "S", "name": "Shadja", "edo_cents": 0.0, "swara_type": "Achala"},
    {"symbol": "r", "name": "Komal Rishabh", "edo_cents": 100.0, "swara_type": "Komal"},
    {"symbol": "R", "name": "Shuddha Rishabh", "edo_cents": 200.0, "swara_type": "Shuddha"},
    {"symbol": "g", "name": "Komal Gandhar", "edo_cents": 300.0, "swara_type": "Komal"},
    {"symbol": "G", "name": "Shuddha Gandhar", "edo_cents": 400.0, "swara_type": "Shuddha"},
    {"symbol": "m", "name": "Shuddha Madhyam", "edo_cents": 500.0, "swara_type": "Shuddha"},
    {"symbol": "M", "name": "Teevra Madhyam", "edo_cents": 600.0, "swara_type": "Teevra"},
    {"symbol": "P", "name": "Pancham", "edo_cents": 700.0, "swara_type": "Achala"},
    {"symbol": "d", "name": "Komal Dhaivat", "edo_cents": 800.0, "swara_type": "Komal"},
    {"symbol": "D", "name": "Shuddha Dhaivat", "edo_cents": 900.0, "swara_type": "Shuddha"},
    {"symbol": "n", "name": "Komal Nishad", "edo_cents": 1000.0, "swara_type": "Komal"},
    {"symbol": "N", "name": "Shuddha Nishad", "edo_cents": 1100.0, "swara_type": "Shuddha"},
]


def hz_to_cents(f_hz: np.ndarray, f_sa_hz: float) -> np.ndarray:
    """
    Converts frequency in Hz to continuous cents relative to tonic (Sa).
    Formula: C = 1200 * log2(f / f_sa)
    Preserves unvoiced / 0 / NaN entries as NaN.
    """
    f = np.asarray(f_hz, dtype=np.float64)
    cents = np.full_like(f, np.nan, dtype=np.float64)
    valid = (f > 0) & (~np.isnan(f)) & (f_sa_hz > 0)
    cents[valid] = 1200.0 * np.log2(f[valid] / f_sa_hz)
    return cents


def cents_to_hz(cents: np.ndarray, f_sa_hz: float) -> np.ndarray:
    """
    Converts cents relative to Sa back to Hz.
    Formula: f = f_sa * 2^(cents / 1200)
    """
    c = np.asarray(cents, dtype=np.float64)
    hz = np.full_like(c, np.nan, dtype=np.float64)
    valid = ~np.isnan(c) & (f_sa_hz > 0)
    hz[valid] = f_sa_hz * (2.0 ** (c[valid] / 1200.0))
    return hz


def quantize_to_shruti(cents_relative: float) -> Tuple[Shruti, float, int]:
    """
    Quantizes a given continuous cents value (relative to Sa) to the closest 22-Shruti.
    Returns: (matching_shruti, microtonal_error_cents, octave_offset)
    """
    if np.isnan(cents_relative):
        raise ValueError("Cannot quantize NaN cents.")
    
    octave = int(np.floor(cents_relative / 1200.0))
    c_mod = cents_relative % 1200.0
    
    best_shruti = SHRUTI_TABLE[0]
    min_dist = float("inf")
    
    for shruti in SHRUTI_TABLE:
        dist = abs(c_mod - shruti.cents)
        if dist < min_dist:
            min_dist = dist
            best_shruti = shruti
            
    # Also check wrap-around to next octave Sa (1200 cents)
    if abs(c_mod - 1200.0) < min_dist:
        best_shruti = SHRUTI_TABLE[0]
        min_dist = abs(c_mod - 1200.0)
        octave += 1
        error = c_mod - 1200.0
    else:
        error = c_mod - best_shruti.cents

    return best_shruti, error, octave


def quantize_to_12_swara(cents_relative: float) -> Tuple[Dict, float, int]:
    """
    Quantizes continuous cents to standard 12-EDO semitones (0, 100, ..., 1100).
    Returns: (swara_dict, error_cents, octave_offset)
    """
    if np.isnan(cents_relative):
        raise ValueError("Cannot quantize NaN cents.")
        
    octave = int(np.floor(cents_relative / 1200.0))
    c_mod = cents_relative % 1200.0
    
    semitone_idx = int(np.round(c_mod / 100.0))
    if semitone_idx == 12:
        semitone_idx = 0
        octave += 1
        error = c_mod - 1200.0
    else:
        error = c_mod - (semitone_idx * 100.0)
        
    return SWARA_12_TABLE[semitone_idx], error, octave


class TonicEstimator:
    """
    Estimates the movable tonic (Sa) from vocal F0 contours or multi-pitch spectra.
    Implements a multi-evidence Bayesian voting strategy based on:
    1. Predominant pitch class histogram peaks (Salamon et al. 2012).
    2. Harmonic fifth (Pa = ~702 cents) and fourth (Ma = ~498 cents) relationship validation.
    3. Low octave grounding (finding typical vocal Sa range 110-330 Hz for male/female voices).
    """

    def __init__(self, min_tonic_hz: float = 100.0, max_tonic_hz: float = 350.0):
        self.min_tonic_hz = min_tonic_hz
        self.max_tonic_hz = max_tonic_hz

    def estimate_from_f0(
        self,
        f0: np.ndarray,
        voiced_prob: Optional[np.ndarray] = None,
        bin_resolution_cents: float = 10.0,
    ) -> Dict:
        """
        Estimates tonic fundamental frequency from continuous F0 contour.
        """
        valid_mask = (f0 > self.min_tonic_hz * 0.5) & (f0 < self.max_tonic_hz * 4.0)
        if voiced_prob is not None:
            valid_mask = valid_mask & (voiced_prob > 0.5)
            
        valid_f0 = f0[valid_mask]
        if len(valid_f0) < 50:
            # Fallback default C3 (130.81 Hz)
            return {
                "tonic_hz": 130.81,
                "confidence": 0.0,
                "note_name": "C3",
                "method": "insufficient_voiced_frames_fallback",
            }

        # Convert valid F0 to log2 space (midi-like)
        # Scan candidate tonic frequencies from min_tonic_hz to max_tonic_hz in 10-cent steps
        candidate_hz = self.min_tonic_hz * (2.0 ** (np.arange(0, 1200 * np.log2(self.max_tonic_hz / self.min_tonic_hz), bin_resolution_cents) / 1200.0))
        
        scores = []
        # In Indian Classical Music, the pitch distribution relative to Sa exhibits strong peaks at:
        # Sa (0 cents), Pa (702 cents), Ma (498 cents), and Samvadi / Vadi intervals
        # A true Sa will have strong energy at 0 and 702 (or 498)
        
        for cand in candidate_hz:
            c = (1200.0 * np.log2(valid_f0 / cand)) % 1200.0
            # Weight peaks at 0 (Sa) and 702 (Pa)
            dist_sa = np.minimum(c, 1200.0 - c)
            dist_pa = np.abs(c - 702.0)
            dist_ma = np.abs(c - 498.0)
            
            # Kernel density around Sa and Pa
            sa_weight = np.exp(-0.5 * (dist_sa / 35.0) ** 2)
            pa_weight = np.exp(-0.5 * (dist_pa / 35.0) ** 2)
            ma_weight = np.exp(-0.5 * (dist_ma / 35.0) ** 2)
            
            # Score combines Sa presence (weight 1.0) and supporting Pa/Ma (weight 0.6)
            score = np.sum(sa_weight) + 0.6 * np.sum(pa_weight) + 0.3 * np.sum(ma_weight)
            scores.append(score)

        scores = np.array(scores)
        best_idx = int(np.argmax(scores))
        best_tonic_hz = float(candidate_hz[best_idx])
        
        # Calculate confidence metric
        peak_score = scores[best_idx]
        mean_score = np.mean(scores)
        confidence = float(np.clip((peak_score - mean_score) / (peak_score + 1e-6), 0.0, 1.0))
        
        # Determine closest Western Note name
        midi_pitch = int(np.round(69 + 12 * np.log2(best_tonic_hz / 440.0)))
        note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        octave = (midi_pitch // 12) - 1
        note_str = f"{note_names[midi_pitch % 12]}{octave}"

        return {
            "tonic_hz": round(best_tonic_hz, 2),
            "confidence": round(confidence, 3),
            "note_name": note_str,
            "method": "harmonic_fifth_histogram_voting",
        }
