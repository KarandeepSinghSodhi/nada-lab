"""
Acoustic Pre-Processor and Octave-Jump Sanitizer for Song Lab.
Implements:
1. Harmonic-Percussive Source Separation (HPSS) to strip tabla/percussion bleed.
2. Bandpass vocal tract formant isolation filter (65 Hz to 3800 Hz).
3. Lead Vocal Energy Ratio (LVER) & Accompaniment Bleed quality scoring.
4. Intelligent Median Octave-Jump & Vocal Fry Glitch Rejection (unwrapping +/-1200c / +/-2400c tracking artifacts).
5. Dynamic Tempo-Adaptive and Gharana-Aware threshold calculation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import librosa
import numpy as np
from scipy.signal import butter, sosfilt


class StylisticPreset(Enum):
    KHAYAL_STANDARD = "Khayal (Standard Gayaki)"
    KHAYAL_KIRANA = "Khayal (Kirana - Deep Andolan & Meend)"
    KHAYAL_GWALIOR = "Khayal (Gwalior - Crisp Sthira Swaras)"
    THUMRI_LIGHT = "Thumri / Ghazal (Brisk Kan & Murki)"
    DHRUPAD = "Dhrupad (Microtonal Shruti & Heavy Gamak)"
    DRUT_TAAN = "Drut Taan (High-Speed Virtuosic Runs)"


@dataclass
class AdaptiveThresholds:
    min_steady_duration_ms: float
    steady_velocity_threshold: float
    kan_max_duration_ms: float
    meend_min_span_cents: float
    preset_name: str
    laya_category: str


class AcousticSanitizer:
    """
    Acoustic isolation and pitch contour sanitizer for real-world un-curated audio.
    """

    def __init__(self, sr: int = 22050):
        self.sr = sr

    def isolate_vocal_harmonics(
        self, audio: np.ndarray, sr: Optional[int] = None
    ) -> Tuple[np.ndarray, float]:
        """
        Applies Harmonic-Percussive Source Separation (HPSS) and bandpass filtering
        to isolate continuous melodic vocal harmonics and strip tabla/percussion strikes.
        Returns: (isolated_audio, accompaniment_bleed_pct)
        """
        sample_rate = sr or self.sr
        if len(audio) < sample_rate * 0.1:
            return audio, 0.0

        # 1. Harmonic-Percussive Separation
        # Margin: favors extracting clean sustained tonal harmonics over percussive hits
        y_harmonic, y_percussive = librosa.effects.hpss(audio, margin=(1.2, 3.5))

        # 2. Bandpass filter for human vocal fundamental & formants (65 Hz to 3800 Hz)
        sos = butter(4, [65.0, min(3800.0, sample_rate * 0.45)], btype="bandpass", fs=sample_rate, output="sos")
        y_filtered = sosfilt(sos, y_harmonic)

        # 3. Accompaniment Bleed Calculation
        total_energy = float(np.sum(audio ** 2) + 1e-9)
        percussive_energy = float(np.sum(y_percussive ** 2))
        bleed_ratio = min(1.0, max(0.0, percussive_energy / total_energy))
        bleed_pct = round(bleed_ratio * 100.0, 1)

        # If audio is already a pristine lead vocal (< 6% percussive bleed), preserve acoustic phase
        if bleed_pct < 6.0:
            return audio.astype(np.float32), bleed_pct

        # Normalize output amplitude to match input rms
        rms_in = np.sqrt(np.mean(audio ** 2))
        rms_out = np.sqrt(np.mean(y_filtered ** 2)) + 1e-9
        y_final = y_filtered * (rms_in / rms_out)

        return y_final.astype(np.float32), bleed_pct

    def sanitize_octave_glitches(
        self,
        cents: np.ndarray,
        hop_sec: float = 0.01,
        max_glitch_duration_ms: float = 40.0,
    ) -> Tuple[np.ndarray, int]:
        """
        Detects and unwraps spurious +/-1200 cents (and +/-2400 cents) octave halving/doubling
        glitches caused by vocal fry, creaky voice, or algorithm tracking artifacts.
        
        A pitch leap of ~1200c lasting <= 40ms that returns immediately to the baseline
        is physically impossible for human vocal cords without a glottal silence.
        Returns: (sanitized_cents, num_glitches_fixed)
        """
        if len(cents) < 5:
            return cents.copy(), 0

        c = cents.copy()
        glitches_fixed = 0
        max_samples = int(np.round((max_glitch_duration_ms / 1000.0) / hop_sec))
        max_samples = max(1, max_samples)

        valid_indices = np.where(~np.isnan(c))[0]
        if len(valid_indices) < 5:
            return c, 0

        for i in range(1, len(valid_indices) - 1):
            curr_idx = valid_indices[i]
            prev_idx = valid_indices[i - 1]
            
            # Check if adjacent in time
            if curr_idx - prev_idx > 2:
                continue

            c_prev = c[prev_idx]
            c_curr = c[curr_idx]

            delta = c_curr - c_prev

            # Check for octave jump (~ +1200 or -1200 cents)
            jump_1200 = abs(abs(delta) - 1200.0) < 120.0
            jump_2400 = abs(abs(delta) - 2400.0) < 160.0

            if jump_1200 or jump_2400:
                octave_shift = 1200.0 if jump_1200 else 2400.0
                sign = 1.0 if delta > 0 else -1.0

                # Look ahead to see if it reverts within max_samples
                future_valid = [idx for idx in valid_indices if idx > curr_idx][:max_samples + 1]
                if future_valid:
                    c_future = c[future_valid[-1]]
                    # If future returns to near c_prev (within 200 cents), this was a transient octave glitch
                    if abs(c_future - c_prev) < 250.0:
                        # Fix the glitch interval
                        for fix_idx in [curr_idx] + future_valid[:-1]:
                            c[fix_idx] -= sign * octave_shift
                            glitches_fixed += 1

        # Localized 3-point median filter on isolated spikes
        for i in range(1, len(c) - 1):
            if not np.isnan(c[i - 1]) and not np.isnan(c[i]) and not np.isnan(c[i + 1]):
                window = [c[i - 1], c[i], c[i + 1]]
                med = float(np.median(window))
                if abs(c[i] - med) > 200.0 and abs(c[i - 1] - c[i + 1]) < 60.0:
                    c[i] = med
                    glitches_fixed += 1

        return c, glitches_fixed

    def separate_stems(
        self, audio: np.ndarray, sr: Optional[int] = None, num_peak_points: int = 160
    ) -> Dict[str, Any]:
        """
        Separates real-world audio into Lead Vocal and Accompaniment stems
        using high-margin HPSS and vocal formant filtering.
        """
        sample_rate = sr or self.sr
        if len(audio) < sample_rate * 0.1:
            peaks = self._compute_peaks(audio, num_peak_points)
            return {
                "vocal_audio": audio.astype(np.float32),
                "accompaniment_audio": np.zeros_like(audio, dtype=np.float32),
                "vocal_peaks": peaks,
                "accompaniment_peaks": [0.0] * len(peaks),
                "mix_peaks": peaks,
                "bleed_pct": 0.0,
            }

        y_harmonic, y_percussive = librosa.effects.hpss(audio, margin=(1.2, 3.5))
        sos = butter(4, [65.0, min(3800.0, sample_rate * 0.45)], btype="bandpass", fs=sample_rate, output="sos")
        y_vocal = sosfilt(sos, y_harmonic).astype(np.float32)
        y_accomp = y_percussive.astype(np.float32)

        total_energy = float(np.sum(audio ** 2) + 1e-9)
        percussive_energy = float(np.sum(y_accomp ** 2))
        bleed_pct = round(min(100.0, (percussive_energy / total_energy) * 100.0), 1)

        return {
            "vocal_audio": y_vocal,
            "accompaniment_audio": y_accomp,
            "vocal_peaks": self._compute_peaks(y_vocal, num_peak_points),
            "accompaniment_peaks": self._compute_peaks(y_accomp, num_peak_points),
            "mix_peaks": self._compute_peaks(audio, num_peak_points),
            "bleed_pct": bleed_pct,
        }

    @staticmethod
    def _compute_peaks(audio: np.ndarray, num_points: int = 160) -> List[float]:
        if len(audio) == 0:
            return [0.0] * num_points
        hop = max(1, len(audio) // num_points)
        peaks = []
        for i in range(0, len(audio), hop):
            chunk = audio[i:i + hop]
            if len(chunk) > 0:
                peaks.append(round(float(np.max(np.abs(chunk))), 3))
        return peaks[:num_points]

    @staticmethod
    def audio_to_base64_wav(audio: np.ndarray, sr: int = 22050) -> str:
        """Encodes float32 audio numpy array to 16-bit PCM WAV base64 string."""
        import io, base64, soundfile as sf
        buf = io.BytesIO()
        sf.write(buf, audio, sr, format="WAV", subtype="PCM_16")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:audio/wav;base64,{b64}"

    @classmethod
    def get_adaptive_thresholds(
        cls,
        bpm: float = 84.0,
        preset: StylisticPreset = StylisticPreset.KHAYAL_STANDARD,
    ) -> AdaptiveThresholds:
        """
        Dynamically adjusts kinematic segmentation thresholds based on track BPM
        and musical Gharana/stylistic genre to prevent misclassifying Drut taans as ornaments.
        """
        # Determine Laya category
        if bpm < 65.0:
            laya = "Vilambit (Slow Laya)"
            tempo_scale = 1.5
        elif bpm <= 130.0:
            laya = "Madhya (Medium Laya)"
            tempo_scale = 1.0
        else:
            laya = "Drut (Fast Virtuosic Laya)"
            tempo_scale = 0.55

        # Base parameters
        base_steady_ms = 110.0 * tempo_scale
        base_steady_vel = 120.0 / tempo_scale
        base_kan_ms = 140.0 * tempo_scale
        base_meend_span = 60.0

        if preset == StylisticPreset.KHAYAL_KIRANA:
            # Kirana favors slow deep Andolan on Komal swaras and extended meend glides
            base_steady_ms *= 1.2
            base_steady_vel *= 0.85
            base_kan_ms *= 1.3
        elif preset == StylisticPreset.KHAYAL_GWALIOR:
            # Gwalior emphasizes structural precision and firm note landing
            base_steady_ms *= 0.95
            base_steady_vel *= 1.10
        elif preset == StylisticPreset.THUMRI_LIGHT:
            # Thumri/Light Classical features brisk touch inflections and rapid khatkas
            base_steady_ms *= 0.80
            base_kan_ms = 180.0
            base_steady_vel = 150.0
        elif preset == StylisticPreset.DHRUPAD:
            # Dhrupad features extended stationary sthira swaras and heavy gamak
            base_steady_ms = max(180.0, base_steady_ms * 1.6)
            base_steady_vel = 80.0
            base_meend_span = 80.0
        elif preset == StylisticPreset.DRUT_TAAN:
            # Virtuosic 16th note taans (notes as short as 60ms)
            base_steady_ms = 55.0
            base_steady_vel = 220.0
            base_kan_ms = 70.0

        return AdaptiveThresholds(
            min_steady_duration_ms=round(base_steady_ms, 1),
            steady_velocity_threshold=round(base_steady_vel, 1),
            kan_max_duration_ms=round(base_kan_ms, 1),
            meend_min_span_cents=round(base_meend_span, 1),
            preset_name=preset.value,
            laya_category=laya,
        )
