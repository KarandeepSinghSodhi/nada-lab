"""
End-to-End Song Lab MIR Pipeline.
Orchestrates:
1. Audio loading, Waveform Peak Extraction & F0 Pitch Tracking (via librosa pYIN).
2. Tonic (Sa) Detection & Cents Normalization.
3. Tempo & BPM Beat Tracking with Tala & Laya Inference.
4. Kinematic Derivative & Multi-Scale Wavelet Ornament Extraction.
5. Discrete Musical Transcription into Bhatkhande Sargam & Western Notations.
6. Pitch Class Distribution (PCD) & 56-Raga Identification.
7. 3-Tier Deficit Engine & Complete Diagnostic Report Generation.
"""

from dataclasses import dataclass
import os
import json
import time
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import librosa
import soundfile as sf

from src.tonal_engine import TonicEstimator, hz_to_cents, quantize_to_12_swara, quantize_to_shruti, SHRUTI_TABLE
from src.ornament_detector import KinematicOrnamentDetector, OrnamentSegment
from src.raga_matcher import RagaMatcher, RAGA_DATABASE
from src.deficit_engine import DeficitEngine, CritiqueFeedback
from src.phrase_rasa_engine import PhraseRasaEngine
from src.sheet_music_extractor import SheetMusicExtractor
from src.acoustic_sanitizer import AcousticSanitizer, StylisticPreset
from src.in_between_notes_engine import InBetweenNotesEngine


class SongLabPipeline:
    """
    Main analysis orchestrator for Song Lab.
    """

    def __init__(
        self,
        target_raga: str = "Yaman",
        known_tonic_hz: Optional[float] = None,
        hop_length_sec: float = 0.01,
        sr: int = 22050,
    ):
        self.target_raga = target_raga
        self.known_tonic_hz = known_tonic_hz
        self.hop_sec = hop_length_sec
        self.sr = sr
        
        self.tonic_estimator = TonicEstimator()
        self.ornament_detector = KinematicOrnamentDetector(hop_length_sec=self.hop_sec)
        self.raga_matcher = RagaMatcher()
        self.deficit_engine = DeficitEngine(target_raga_name=target_raga)
        self.in_between_engine = InBetweenNotesEngine(hop_sec=self.hop_sec)
        self.rasa_engine = PhraseRasaEngine()
        self.sanitizer = AcousticSanitizer(sr=self.sr)

    def extract_f0(self, audio: np.ndarray, sr: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Extracts continuous fundamental frequency (F0) using probabilistic YIN (pYIN).
        Returns: (f0_hz, voiced_prob, times_sec)
        """
        hop_length = int(np.round(self.hop_sec * sr))
        # Vocal pitch range 65 Hz (C2) to 1046 Hz (C6)
        f0, voiced_flag, voiced_prob = librosa.pyin(
            audio,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C6"),
            sr=sr,
            hop_length=hop_length,
        )
        times = librosa.times_like(f0, sr=sr, hop_length=hop_length)
        return f0, voiced_prob, times

    def extract_tempo_and_rhythm(self, audio: np.ndarray, sr: int) -> Dict[str, Any]:
        """
        Extracts tempo (BPM) and suggests matching classical Indian Tala and Laya.
        """
        bpm = 80.0
        try:
            onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
            t_est = librosa.feature.tempo(onset_envelope=onset_env, sr=sr)
            bpm_val = float(np.atleast_1d(t_est)[0])
            if bpm_val > 30.0 and bpm_val < 300.0:
                bpm = round(bpm_val, 1)
        except Exception:
            bpm = 80.0

        if bpm < 65.0:
            laya = "Vilambit (Slow)"
            suggested_tala = "Vilambit Teentaal (16 Matras)"
        elif bpm <= 115.0:
            laya = "Madhya (Medium)"
            suggested_tala = "Madhya Teentaal (16 Matras: 4+4+4+4)"
        else:
            laya = "Drut (Fast)"
            suggested_tala = "Drut Teentaal / Keharwa (8 Matras)"

        return {
            "bpm": bpm,
            "laya": laya,
            "suggested_tala": suggested_tala,
            "meter_signature": "4/4" if "16" in suggested_tala or "8" in suggested_tala else "7/8"
        }

    def extract_waveform_peaks(self, audio: np.ndarray, num_points: int = 160) -> List[float]:
        """
        Computes downsampled audio waveform amplitude envelope for immediate UI rendering.
        """
        if len(audio) == 0:
            return [0.0] * num_points
        hop = max(1, len(audio) // num_points)
        peaks = []
        for i in range(0, len(audio), hop):
            chunk = audio[i:i + hop]
            if len(chunk) > 0:
                peaks.append(round(float(np.max(np.abs(chunk))), 3))
        return peaks[:num_points]

    def extract_transcriptions(
        self,
        ornaments: List[OrnamentSegment],
        tonic_hz: float,
        cents: np.ndarray,
        times: np.ndarray
    ) -> List[Dict[str, Any]]:
        """
        Translates continuous kinematic pitch intervals into discrete Bhatkhande Sargam
        and Western musical notations with 22-shruti cents precision.
        """
        notations: List[Dict[str, Any]] = []

        for o in ornaments:
            if np.isnan(o.start_cents):
                continue

            c_mid = (o.start_cents + o.end_cents) / 2.0
            sw_info, _, _ = quantize_to_12_swara(c_mid)
            norm_cents = c_mid % 1200.0
            closest_shruti = min(SHRUTI_TABLE, key=lambda s: abs(norm_cents - s.cents))
            dev = norm_cents - closest_shruti.cents
            if dev > 600.0:
                dev -= 1200.0
            elif dev < -600.0:
                dev += 1200.0

            f_mid = tonic_hz * (2.0 ** (c_mid / 1200.0))
            midi_pitch = int(np.round(librosa.hz_to_midi(f_mid))) if f_mid > 20.0 else 60
            western_note = librosa.midi_to_note(midi_pitch) if midi_pitch > 0 else "N/A"

            notations.append({
                "symbol": sw_info["symbol"],
                "swara_name": sw_info["name"],
                "western_note": western_note,
                "shruti_name": f"{closest_shruti.swara_hindustani} ({closest_shruti.name_sanskrit})",
                "shruti_ratio": f"{closest_shruti.ratio_num}/{closest_shruti.ratio_den}",
                "start_time": round(float(o.start_time), 3),
                "end_time": round(float(o.end_time), 3),
                "duration_sec": round(float(o.duration_ms / 1000.0), 3),
                "avg_cents": round(float(c_mid), 1),
                "cents_deviation": round(float(dev), 1),
                "ornament_type": o.ornament_type.value,
            })

        return notations

    def analyze_audio(
        self,
        audio_path_or_array,
        sr: Optional[int] = None,
        stylistic_preset: Optional[str] = None,
    ) -> Dict:
        """
        Processes an audio file or numpy array through the full Song Lab pipeline.
        """
        t0 = time.time()
        
        # 1. Load Audio
        if isinstance(audio_path_or_array, str):
            audio, sample_rate = librosa.load(audio_path_or_array, sr=self.sr, mono=True)
            file_name = os.path.basename(audio_path_or_array)
        else:
            audio = np.asarray(audio_path_or_array, dtype=np.float32)
            sample_rate = sr if sr is not None else self.sr
            file_name = "audio_stream.wav"

        # 2. Vocal Isolation & Accompaniment Bleed Filtering (HPSS)
        isolated_audio, bleed_pct = self.sanitizer.isolate_vocal_harmonics(audio, sample_rate)

        # 3. Extract F0 on Isolated Vocal
        f0_hz, voiced_prob, times = self.extract_f0(isolated_audio, sample_rate)
        
        # 3. Extract Tempo & Rhythm
        tempo_info = self.extract_tempo_and_rhythm(audio, sample_rate)

        # 4. Extract Waveform Peaks & Stem Envelopes
        stem_info = self.sanitizer.separate_stems(audio, sample_rate, num_peak_points=160)
        waveform_peaks = stem_info["mix_peaks"]

        # 5. Process F0 Trajectory with Adaptive Thresholds & Octave Sanitization
        return self.analyze_pitch_contour(
            f0_hz,
            times,
            voiced_prob,
            total_audio_duration=len(audio) / sample_rate,
            elapsed_time=time.time() - t0,
            tempo_info=tempo_info,
            waveform_peaks=waveform_peaks,
            file_name=file_name,
            bleed_pct=bleed_pct,
            stylistic_preset=stylistic_preset,
        )

    def analyze_pitch_contour(
        self,
        f0_hz: np.ndarray,
        times: np.ndarray,
        voiced_prob: Optional[np.ndarray] = None,
        total_audio_duration: Optional[float] = None,
        elapsed_time: float = 0.0,
        tempo_info: Optional[Dict[str, Any]] = None,
        waveform_peaks: Optional[List[float]] = None,
        file_name: str = "phrase.wav",
        bleed_pct: float = 0.0,
        stylistic_preset: Optional[str] = None,
    ) -> Dict:
        """
        Processes an F0 contour directly (useful for synthetic benchmarks and pre-extracted datasets).
        """
        t_start = time.time()
        
        # Step 1: Tonic (Sa) Estimation
        if self.known_tonic_hz is not None:
            tonic_info = {
                "tonic_hz": self.known_tonic_hz,
                "confidence": 1.0,
                "note_name": "Specified by User",
                "method": "manual_or_ground_truth",
            }
        else:
            tonic_info = self.tonic_estimator.estimate_from_f0(f0_hz, voiced_prob)
            
        tonic_hz = tonic_info["tonic_hz"]
        
        # Step 2: Cents Conversion & Octave-Jump Glitch Rejection
        cents_raw = hz_to_cents(f0_hz, tonic_hz)
        cents, octave_glitches_fixed = self.sanitizer.sanitize_octave_glitches(cents_raw, hop_sec=self.hop_sec)

        # Step 2b: Tempo-Adaptive & Gharana-Aware Threshold Scaling
        bpm = float(tempo_info.get("bpm", 84.0) if tempo_info else 84.0)
        preset_enum = StylisticPreset.KHAYAL_STANDARD
        if stylistic_preset:
            for p_candidate in StylisticPreset:
                if p_candidate.name.lower() == stylistic_preset.lower() or p_candidate.value.lower() == stylistic_preset.lower():
                    preset_enum = p_candidate
                    break

        adaptive_thresh = AcousticSanitizer.get_adaptive_thresholds(bpm=bpm, preset=preset_enum)
        self.ornament_detector.configure_adaptive_thresholds(
            min_steady_duration_ms=adaptive_thresh.min_steady_duration_ms,
            steady_velocity_threshold=adaptive_thresh.steady_velocity_threshold,
            kan_max_duration_ms=adaptive_thresh.kan_max_duration_ms,
            meend_min_span_cents=adaptive_thresh.meend_min_span_cents,
        )
        
        # Step 3: Ornament Detection & Kinematic Derivatives
        voiced_mask = (voiced_prob > 0.4) if voiced_prob is not None else (~np.isnan(f0_hz))
        smoothed_cents = self.ornament_detector.smooth_contour(cents)
        v, a, j = self.ornament_detector.compute_derivatives(smoothed_cents)
        ornaments = self.ornament_detector.segment_and_classify(cents, times, voiced_mask)
        
        # Step 4: Extract discrete swara sequence for phrase alignment
        discrete_swaras: List[str] = []
        for s in ornaments:
            if not np.isnan(s.start_cents):
                sw, _, _ = quantize_to_12_swara(s.start_cents)
                discrete_swaras.append(sw["symbol"])
                
        # Step 5: Raga Matching (using steady-weighted PCD)
        raga_candidates = self.raga_matcher.match_raga(cents, discrete_swaras, velocity=v, top_k=3)
        identified_raga_name = raga_candidates[0]["raga"] if raga_candidates else "Unknown"
        match_confidence = raga_candidates[0]["score"] if raga_candidates else 0.0
        
        # Fetch raga metadata
        raga_obj = next((r for r in RAGA_DATABASE if r.name.lower() == identified_raga_name.lower()), None)

        # Step 6: Discrete Musical Transcriptions
        transcriptions = self.extract_transcriptions(ornaments, tonic_hz, cents, times)

        # Step 7: Phrase Segmentation & Deficit Engine
        unvoiced = ~voiced_mask
        runs = np.diff(np.pad(unvoiced.astype(int), (1, 1), mode="constant"))
        silence_starts = np.where(runs == 1)[0]
        silence_ends = np.where(runs == -1)[0]
        
        phrase_boundaries = [0]
        for ss, se in zip(silence_starts, silence_ends):
            silence_dur_sec = (times[min(se - 1, len(times) - 1)] - times[ss])
            if silence_dur_sec >= 0.25:
                phrase_boundaries.append(ss)
                phrase_boundaries.append(se)
        phrase_boundaries.append(len(cents))
        phrase_boundaries = sorted(list(set(phrase_boundaries)))
        
        phrase_critiques: List[CritiqueFeedback] = []
        phrase_idx = 1
        
        for i in range(len(phrase_boundaries) - 1):
            p_start = phrase_boundaries[i]
            p_end = phrase_boundaries[i + 1]
            if p_end <= p_start:
                continue
                
            sub_c = cents[p_start:p_end]
            sub_t = times[p_start:p_end]
            if np.all(np.isnan(sub_c)) or np.sum(~np.isnan(sub_c)) < 15:
                continue
                
            p_start_t = float(sub_t[0])
            p_end_t = float(sub_t[-1])
            p_ornaments = [o for o in ornaments if o.start_time >= p_start_t - 0.05 and o.end_time <= p_end_t + 0.05]
            
            critique = self.deficit_engine.evaluate_phrase(
                phrase_id=phrase_idx,
                cents_trajectory=sub_c,
                time_trajectory=sub_t,
                detected_ornaments=p_ornaments,
            )
            phrase_critiques.append(critique)
            phrase_idx += 1
            
        total_time = elapsed_time + (time.time() - t_start)
        
        # Downsampled trajectory for web UI visualization (~50 Hz)
        step = max(1, int(0.02 / self.hop_sec))
        trajectory = []
        for idx in range(0, len(cents), step):
            c_val = cents[idx]
            if not np.isnan(c_val) and voiced_mask[idx]:
                trajectory.append({
                    "t": round(float(times[idx]), 3),
                    "cents": round(float(c_val), 1),
                })

        # Calculate average pitch intonation purity
        if transcriptions:
            avg_dev = float(np.mean([abs(n["cents_deviation"]) for n in transcriptions]))
            intonation_accuracy = round(max(60.0, 100.0 - avg_dev * 1.5), 1)
        else:
            intonation_accuracy = 95.0

        if tempo_info is None:
            tempo_info = {
                "bpm": 84.0,
                "laya": "Madhya (Medium)",
                "suggested_tala": "Madhya Teentaal (16 Matras)",
                "meter_signature": "4/4"
            }

        scale_and_key = {
            "identified_raga": identified_raga_name,
            "match_confidence": round(float(match_confidence), 3),
            "thaat": raga_obj.thaat_or_mela if raga_obj else "Kalyan",
            "vadi": raga_obj.vadi if raga_obj else "Ga",
            "samvadi": raga_obj.samvadi if raga_obj else "Ni",
            "tonic_hz": round(float(tonic_hz), 2),
            "tonic_note": tonic_info.get("note_name", "D3"),
            "arohana": raga_obj.arohana if raga_obj else ["S", "R", "G", "M", "P", "D", "N", "S'"],
            "avarohana": raga_obj.avarohana if raga_obj else ["S'", "N", "D", "P", "M", "G", "R", "S"],
        }

        # In-Between-The-Notes (Antar-Swara) Expressive Transition Analysis
        in_between_transitions = self.in_between_engine.analyze_phrase_transitions(
            notes=transcriptions,
            times=times,
            cents=cents,
        )
        in_between_dicts = [t.to_dict() for t in in_between_transitions]

        # Build Structured Evidence Package
        evidence = {
            "metadata": {
                "file_name": file_name,
                "engine_version": "SongLab-Phase2-v1.0",
                "target_raga": self.target_raga,
                "analysis_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "audio_duration_sec": round(float(total_audio_duration or times[-1]), 2),
                "compute_latency_sec": round(float(total_time), 3),
            },
            "tonal_grounding": tonic_info,
            "raga_identification": {
                "top_candidates": raga_candidates,
                "identified_raga": identified_raga_name,
                "match_confidence": match_confidence,
            },
            "acoustic_hygiene": {
                "vocal_isolation_score_pct": round(max(0.0, min(100.0, 100.0 - bleed_pct)), 1),
                "accompaniment_bleed_pct": round(bleed_pct, 1),
                "octave_glitches_rectified": octave_glitches_fixed,
                "stylistic_preset": adaptive_thresh.preset_name,
                "laya_category": adaptive_thresh.laya_category,
                "adaptive_steady_duration_ms": adaptive_thresh.min_steady_duration_ms,
                "lead_vocal_quality": "Pristine Lead Vocal" if bleed_pct < 20.0 else ("Moderate Accompaniment Bleed" if bleed_pct < 45.0 else "Heavy Accompaniment Bleed (Tabla/Harmonium Filtered)")
            },
            "scale_and_key": scale_and_key,
            "tempo_and_meter": tempo_info,
            "transcribed_notations": transcriptions,
            "sheet_music_score": SheetMusicExtractor.extract_sheet_music(
                notations=transcriptions,
                tempo_bpm=float(tempo_info.get("bpm", 84.0) if tempo_info else 84.0),
                tonic_hz=float(tonic_hz),
                instrument="piano",
                in_between_transitions=in_between_dicts,
            ),
            "in_between_notes": in_between_dicts,
            "waveform_peaks": waveform_peaks or [],
            "pitch_trajectory": trajectory,
            "ornaments_detected": [o.to_dict() for o in ornaments],
            "phrase_critiques": [c.to_dict() for c in phrase_critiques],
            "phrase_rasa_profile": self.rasa_engine.analyze_phrase_rasa(
                pitch_trajectory=trajectory,
                identified_raga=identified_raga_name,
                bpm=tempo_info.get("bpm", 84.0) if tempo_info else 84.0,
                ornaments=[o.to_dict() for o in ornaments]
            ),
            "summary_scores": {
                "total_phrases": len(phrase_critiques),
                "flawless_phrases": sum(1 for c in phrase_critiques if "Flawless" in c.primary_badge),
                "structural_deficits": sum(1 for c in phrase_critiques if "Structural" in c.tier.value),
                "fatal_tonal_violations": sum(1 for c in phrase_critiques if "Fatal" in c.tier.value),
                "intonation_accuracy_pct": intonation_accuracy,
                "total_notes_transcribed": len(transcriptions),
            }
        }
        
        return evidence

    def process(
        self,
        audio_path: str,
        target_raga: Optional[str] = None,
        manual_sa_hz: Optional[float] = None,
        stylistic_preset: Optional[str] = None,
    ) -> Dict:
        """
        Convenience entry point for API bridges and batch processors.
        """
        if target_raga:
            self.target_raga = target_raga
            self.deficit_engine = DeficitEngine(target_raga_name=target_raga)
        if manual_sa_hz:
            self.known_tonic_hz = manual_sa_hz
        return self.analyze_audio(audio_path, stylistic_preset=stylistic_preset)
