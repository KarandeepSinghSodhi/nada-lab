"""
Kinematic and Multi-Scale Wavelet Ornament Detector for Song Lab.
Implements:
1. Savitzky-Golay / Gaussian smoothing of continuous F0 cents contour.
2. Kinematic derivative calculation: velocity v(t), acceleration a(t), jerk j(t).
3. Critical-point segmentation (Nyasa/Sthira resting points vs active transitions).
4. Continuous multi-scale oscillatory decomposition (Andolan, Gamak, Vibrato).
5. Transient & glide morphological detection (Meend, Kan, Murki, Khatka).
6. Dual-mode ornament metadata output (Indian Classical & Western Contemporary).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import numpy as np
from scipy.signal import find_peaks, savgol_filter


class OrnamentType(Enum):
    STHIRA_NOTE = "Sthira / Steady Note"
    MEEND = "Meend / Portamento Glide"
    ANDOLAN = "Andolan / Slow Wide Oscillation"
    GAMAK = "Gamak / Heavy Oscillatory Shake"
    KAN = "Kan / Grace Note / Touch Inflection"
    MURKI = "Murki / Fast Turn / Mordent"
    KHATKA = "Khatka / Clustered Ornament"
    VIBRATO = "Western Vocal Vibrato"
    UNCLASSIFIED = "Unclassified Melodic Motion"


@dataclass
class OrnamentSegment:
    start_time: float
    end_time: float
    duration_ms: float
    ornament_type: OrnamentType
    start_cents: float
    end_cents: float
    min_cents: float
    max_cents: float
    pitch_span_cents: float
    mean_velocity: float
    max_velocity: float
    oscillation_rate_hz: Optional[float] = None
    oscillation_depth_cents: Optional[float] = None
    from_swara: Optional[str] = None
    to_swara: Optional[str] = None
    confidence: float = 1.0
    properties: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "start_time": round(self.start_time, 3),
            "end_time": round(self.end_time, 3),
            "duration_ms": round(self.duration_ms, 1),
            "ornament_type": self.ornament_type.value,
            "start_cents": round(self.start_cents, 1),
            "end_cents": round(self.end_cents, 1),
            "pitch_span_cents": round(self.pitch_span_cents, 1),
            "mean_velocity_cents_sec": round(self.mean_velocity, 1),
            "max_velocity_cents_sec": round(self.max_velocity, 1),
            "oscillation_rate_hz": round(self.oscillation_rate_hz, 2) if self.oscillation_rate_hz else None,
            "oscillation_depth_cents": round(self.oscillation_depth_cents, 1) if self.oscillation_depth_cents else None,
            "from_swara": self.from_swara,
            "to_swara": self.to_swara,
            "confidence": round(self.confidence, 3),
            "properties": self.properties,
        }


class KinematicOrnamentDetector:
    """
    Tier-1 Kinematic Derivative + Tier-2 Morphological Classifier for Vocal Ornaments.
    """

    def __init__(
        self,
        hop_length_sec: float = 0.01,  # 10ms frame hop typical for F0 trackers
        min_steady_duration_ms: float = 120.0,
        steady_velocity_threshold: float = 120.0,  # cents/s
        meend_min_span_cents: float = 60.0,
        meend_min_velocity: float = 180.0,  # cents/s
        kan_max_duration_ms: float = 140.0,
        kan_min_velocity: float = 1000.0,  # cents/s
    ):
        self.hop_sec = hop_length_sec
        self.min_steady_duration_ms = min_steady_duration_ms
        self.steady_velocity_threshold = steady_velocity_threshold
        self.meend_min_span_cents = meend_min_span_cents
        self.meend_min_velocity = meend_min_velocity
        self.kan_max_duration_ms = kan_max_duration_ms
        self.kan_min_velocity = kan_min_velocity

    def configure_adaptive_thresholds(
        self,
        min_steady_duration_ms: Optional[float] = None,
        steady_velocity_threshold: Optional[float] = None,
        kan_max_duration_ms: Optional[float] = None,
        meend_min_span_cents: Optional[float] = None,
    ):
        """
        Dynamically reconfigures segmentation thresholds based on track BPM
        and stylistic Gharana presets.
        """
        if min_steady_duration_ms is not None:
            self.min_steady_duration_ms = min_steady_duration_ms
        if steady_velocity_threshold is not None:
            self.steady_velocity_threshold = steady_velocity_threshold
        if kan_max_duration_ms is not None:
            self.kan_max_duration_ms = kan_max_duration_ms
        if meend_min_span_cents is not None:
            self.meend_min_span_cents = meend_min_span_cents

    def smooth_contour(self, cents: np.ndarray, window_ms: float = 50.0) -> np.ndarray:
        """
        Applies Savitzky-Golay smoothing to continuous cents curve while preserving
        sharp inflection boundaries.
        """
        # Interpolate NaNs for filtering
        c = cents.copy()
        nans = np.isnan(c)
        if np.all(nans):
            return c
        
        # Linear fill of NaNs for smoothing filter
        indices = np.arange(len(c))
        c[nans] = np.interp(indices[nans], indices[~nans], c[~nans])
        
        window_samples = int(np.round((window_ms / 1000.0) / self.hop_sec))
        if window_samples % 2 == 0:
            window_samples += 1
        window_samples = max(window_samples, 5)
        
        if len(c) > window_samples:
            smoothed = savgol_filter(c, window_length=window_samples, polyorder=3)
        else:
            smoothed = c
            
        smoothed[nans] = np.nan
        return smoothed

    def compute_derivatives(self, cents: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes velocity v(t) = dC/dt (cents/sec),
        acceleration a(t) = d^2C/dt^2 (cents/sec^2),
        and jerk j(t) = d^3C/dt^3.
        """
        dt = self.hop_sec
        # Central difference for velocity
        v = np.gradient(cents, dt)
        # Acceleration
        a = np.gradient(v, dt)
        # Jerk
        j = np.gradient(a, dt)
        return v, a, j

    def _analyze_oscillation(
        self,
        cents_segment: np.ndarray,
        time_segment: np.ndarray
    ) -> Tuple[Optional[float], Optional[float], int]:
        """
        Detects periodic oscillation within a segment:
        Returns: (rate_hz, peak_to_peak_depth_cents, num_cycles)
        """
        if len(cents_segment) < 5:
            return None, None, 0
            
        # Detrend linear slope
        poly = np.polyfit(np.arange(len(cents_segment)), cents_segment, 1)
        detrended = cents_segment - np.polyval(poly, np.arange(len(cents_segment)))
        
        # Find positive and negative peaks with prominence threshold to reject micro-jitter
        min_prom = max(10.0, 0.15 * (np.percentile(detrended, 95) - np.percentile(detrended, 5)))
        min_dist = max(1, int(0.10 / self.hop_sec))
        pos_peaks, _ = find_peaks(detrended, distance=min_dist, prominence=min_prom)
        neg_peaks, _ = find_peaks(-detrended, distance=min_dist, prominence=min_prom)
        
        total_peaks = len(pos_peaks) + len(neg_peaks)
        if len(pos_peaks) < 2 and len(neg_peaks) < 2:
            return None, None, 0
            
        # Peak-to-peak amplitude
        depth = float(np.percentile(detrended, 95) - np.percentile(detrended, 5))
        
        # Estimate rate from interval between consecutive peaks
        peak_intervals = []
        if len(pos_peaks) >= 2:
            peak_intervals.extend(np.diff(time_segment[pos_peaks]))
        if len(neg_peaks) >= 2:
            peak_intervals.extend(np.diff(time_segment[neg_peaks]))
            
        if not peak_intervals or np.mean(peak_intervals) <= 0:
            return None, None, 0
            
        avg_period = float(np.mean(peak_intervals))
        rate_hz = float(1.0 / avg_period)
        cycles = max(len(pos_peaks), len(neg_peaks))
        
        return rate_hz, depth, cycles

    def segment_and_classify(
        self,
        cents: np.ndarray,
        times: np.ndarray,
        voiced: Optional[np.ndarray] = None,
    ) -> List[OrnamentSegment]:
        """
        Segments the continuous cents curve into contiguous ornament and steady note intervals.
        """
        if len(cents) == 0:
            return []
            
        smoothed_cents = self.smooth_contour(cents)
        v, a, j = self.compute_derivatives(smoothed_cents)
        
        if voiced is None:
            voiced = ~np.isnan(smoothed_cents)
        else:
            voiced = voiced & (~np.isnan(smoothed_cents))
            
        # Partition into contiguous voiced blocks
        voiced_diff = np.diff(np.pad(voiced.astype(int), (1, 1), mode="constant"))
        starts = np.where(voiced_diff == 1)[0]
        ends = np.where(voiced_diff == -1)[0]
        
        segments: List[OrnamentSegment] = []
        
        for s_idx, e_idx in zip(starts, ends):
            block_len = e_idx - s_idx
            if block_len < 3:
                continue
                
            block_cents = smoothed_cents[s_idx:e_idx]
            block_times = times[s_idx:e_idx]
            block_v = v[s_idx:e_idx]
            block_a = a[s_idx:e_idx]
            
            # Sub-segment this voiced block based on kinematic boundaries
            # A boundary occurs when velocity sign flips or acceleration zero-crosses with low velocity
            # Identify steady regions (abs(v) < threshold for duration >= min_steady_duration_ms)
            is_steady = np.abs(block_v) < self.steady_velocity_threshold
            
            # Find runs of steady vs dynamic
            run_diff = np.diff(np.pad(is_steady.astype(int), (1, 1), mode="constant"))
            r_starts = np.where(run_diff == 1)[0]
            r_ends = np.where(run_diff == -1)[0]
            
            # Breakpoints within the block
            breakpoints = {0, block_len}
            for rs, re in zip(r_starts, r_ends):
                r_dur_ms = (block_times[min(re - 1, block_len - 1)] - block_times[rs]) * 1000.0
                if r_dur_ms >= self.min_steady_duration_ms:
                    breakpoints.add(rs)
                    breakpoints.add(re)
                    
            sorted_breaks = sorted(list(breakpoints))
            
            for i in range(len(sorted_breaks) - 1):
                b_start = sorted_breaks[i]
                b_end = sorted_breaks[i + 1]
                if b_end <= b_start:
                    continue
                    
                sub_cents = block_cents[b_start:b_end]
                sub_times = block_times[b_start:b_end]
                sub_v = block_v[b_start:b_end]
                sub_a = block_a[b_start:b_end]
                
                start_t = float(sub_times[0])
                end_t = float(sub_times[-1])
                dur_ms = float((end_t - start_t) * 1000.0)
                
                c_start = float(sub_cents[0])
                c_end = float(sub_cents[-1])
                c_min = float(np.min(sub_cents))
                c_max = float(np.max(sub_cents))
                span = float(c_max - c_min)
                mean_v = float(np.mean(np.abs(sub_v)))
                max_v = float(np.max(np.abs(sub_v)))
                
                # Check for oscillation
                rate_hz, depth, cycles = self._analyze_oscillation(sub_cents, sub_times)
                
                ornament_type = OrnamentType.UNCLASSIFIED
                confidence = 0.8
                props = {}
                
                # 1. Steady Note (Sthira)
                if mean_v < self.steady_velocity_threshold and span < 40.0:
                    ornament_type = OrnamentType.STHIRA_NOTE
                    confidence = 0.95
                    
                # 2. Oscillatory Ornaments: Andolan vs Gamak vs Vibrato
                elif rate_hz is not None and cycles >= 2:
                    props["rate_hz"] = round(rate_hz, 2)
                    props["depth_cents"] = round(depth, 1)
                    props["cycles"] = cycles
                    
                    if 1.0 <= rate_hz <= 3.5 and depth >= 45.0:
                        ornament_type = OrnamentType.ANDOLAN
                        confidence = 0.92
                    elif 3.5 < rate_hz <= 7.5 and depth >= 70.0:
                        ornament_type = OrnamentType.GAMAK
                        confidence = 0.90
                    elif 4.5 <= rate_hz <= 8.0 and depth < 65.0:
                        ornament_type = OrnamentType.VIBRATO
                        confidence = 0.88
                    else:
                        ornament_type = OrnamentType.GAMAK
                        confidence = 0.75
                        
                # 3. Kan Swara (Grace / Touch note)
                elif dur_ms <= self.kan_max_duration_ms and (max_v >= self.kan_min_velocity or span >= 70.0):
                    ornament_type = OrnamentType.KAN
                    confidence = 0.90
                    props["inflection_span_cents"] = round(span, 1)
                    props["transient_speed"] = round(max_v, 1)
                    
                # 4. Meend (Continuous Portamento Glide)
                elif span >= self.meend_min_span_cents and mean_v >= self.meend_min_velocity and dur_ms >= 80.0:
                    # Check monotonicity (monotonic glides have high net-to-total ratio)
                    net_delta = abs(c_end - c_start)
                    total_path = np.sum(np.abs(np.diff(sub_cents)))
                    is_monotonic = (net_delta / (total_path + 1e-6)) > 0.75
                    
                    if is_monotonic:
                        ornament_type = OrnamentType.MEEND
                        confidence = 0.94
                        props["direction"] = "Ascending" if c_end > c_start else "Descending"
                    else:
                        # Non-monotonic fast motion
                        if dur_ms < 300.0:
                            ornament_type = OrnamentType.MURKI
                            confidence = 0.85
                        else:
                            ornament_type = OrnamentType.KHATKA
                            confidence = 0.80
                            
                # 5. Murki / Khatka fallback
                elif dur_ms < 300.0 and span >= 60.0:
                    ornament_type = OrnamentType.MURKI
                    confidence = 0.82
                else:
                    ornament_type = OrnamentType.STHIRA_NOTE if mean_v < 180.0 else OrnamentType.UNCLASSIFIED
                    confidence = 0.70

                seg = OrnamentSegment(
                    start_time=start_t,
                    end_time=end_t,
                    duration_ms=dur_ms,
                    ornament_type=ornament_type,
                    start_cents=c_start,
                    end_cents=c_end,
                    min_cents=c_min,
                    max_cents=c_max,
                    pitch_span_cents=span,
                    mean_velocity=mean_v,
                    max_velocity=max_v,
                    oscillation_rate_hz=rate_hz,
                    oscillation_depth_cents=depth,
                    confidence=confidence,
                    properties=props,
                )
                segments.append(seg)
                
        return segments
