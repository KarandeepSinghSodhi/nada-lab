from pathlib import Path

p = Path("src/pipeline.py")
content = p.read_text(encoding="utf-8")
content_norm = content.replace("\r\n", "\n")

# 1. Add import
old_import = "from src.sheet_music_extractor import SheetMusicExtractor"
new_import = """from src.sheet_music_extractor import SheetMusicExtractor
from src.acoustic_sanitizer import AcousticSanitizer, StylisticPreset"""

assert old_import in content_norm, "old_import not found"
content_norm = content_norm.replace(old_import, new_import, 1)

# 2. Add sanitizer in __init__
old_init = "self.rasa_engine = PhraseRasaEngine()"
new_init = """self.rasa_engine = PhraseRasaEngine()
        self.sanitizer = AcousticSanitizer(sr=self.sr)"""

assert old_init in content_norm, "old_init not found"
content_norm = content_norm.replace(old_init, new_init, 1)

# 3. Update analyze_audio signature and logic
old_analyze_start = "    def analyze_audio(\n        self,\n        audio_path_or_array,\n        sr: Optional[int] = None,\n    ) -> Dict:"
new_analyze_start = "    def analyze_audio(\n        self,\n        audio_path_or_array,\n        sr: Optional[int] = None,\n        stylistic_preset: Optional[str] = None,\n    ) -> Dict:"

assert old_analyze_start in content_norm, "old_analyze_start not found"
content_norm = content_norm.replace(old_analyze_start, new_analyze_start, 1)

# In analyze_audio, replace F0 extraction call with isolated vocal extraction
old_f0_call = """        # 2. Extract F0
        f0_hz, voiced_prob, times = self.extract_f0(audio, sample_rate)"""

new_f0_call = """        # 2. Vocal Isolation & Accompaniment Bleed Filtering (HPSS)
        isolated_audio, bleed_pct = self.sanitizer.isolate_vocal_harmonics(audio, sample_rate)

        # 3. Extract F0 on Isolated Vocal
        f0_hz, voiced_prob, times = self.extract_f0(isolated_audio, sample_rate)"""

assert old_f0_call in content_norm, "old_f0_call not found"
content_norm = content_norm.replace(old_f0_call, new_f0_call, 1)

old_return_call = """        # 5. Process F0 Trajectory
        return self.analyze_pitch_contour(
            f0_hz,
            times,
            voiced_prob,
            total_audio_duration=len(audio) / sample_rate,
            elapsed_time=time.time() - t0,
            tempo_info=tempo_info,
            waveform_peaks=waveform_peaks,
            file_name=file_name
        )"""

new_return_call = """        # 5. Process F0 Trajectory with Adaptive Thresholds & Octave Sanitization
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
        )"""

assert old_return_call in content_norm, "old_return_call not found"
content_norm = content_norm.replace(old_return_call, new_return_call, 1)

# 4. Update analyze_pitch_contour signature and add octave sanitization & adaptive thresholds
old_contour_sig = """    def analyze_pitch_contour(
        self,
        f0_hz: np.ndarray,
        times: np.ndarray,
        voiced_prob: Optional[np.ndarray] = None,
        total_audio_duration: Optional[float] = None,
        elapsed_time: float = 0.0,
        tempo_info: Optional[Dict[str, Any]] = None,
        waveform_peaks: Optional[List[float]] = None,
        file_name: str = "phrase.wav"
    ) -> Dict:"""

new_contour_sig = """    def analyze_pitch_contour(
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
    ) -> Dict:"""

assert old_contour_sig in content_norm, "old_contour_sig not found"
content_norm = content_norm.replace(old_contour_sig, new_contour_sig, 1)

# 5. Add octave sanitization and threshold reconfiguration in analyze_pitch_contour
old_cents_step = """        # Step 2: Cents Conversion
        cents = hz_to_cents(f0_hz, tonic_hz)
        
        # Step 3: Ornament Detection & Kinematic Derivatives"""

new_cents_step = """        # Step 2: Cents Conversion & Octave-Jump Glitch Rejection
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
        
        # Step 3: Ornament Detection & Kinematic Derivatives"""

assert old_cents_step in content_norm, "old_cents_step not found"
content_norm = content_norm.replace(old_cents_step, new_cents_step, 1)

# 6. Include acoustic_hygiene in evidence
old_evidence_scale = """            "scale_and_key": scale_and_key,"""
new_evidence_scale = """            "acoustic_hygiene": {
                "vocal_isolation_score_pct": round(max(0.0, min(100.0, 100.0 - bleed_pct)), 1),
                "accompaniment_bleed_pct": round(bleed_pct, 1),
                "octave_glitches_rectified": octave_glitches_fixed,
                "stylistic_preset": adaptive_thresh.preset_name,
                "laya_category": adaptive_thresh.laya_category,
                "adaptive_steady_duration_ms": adaptive_thresh.min_steady_duration_ms,
                "lead_vocal_quality": "Pristine Lead Vocal" if bleed_pct < 20.0 else ("Moderate Accompaniment Bleed" if bleed_pct < 45.0 else "Heavy Accompaniment Bleed (Tabla/Harmonium Filtered)")
            },
            "scale_and_key": scale_and_key,"""

assert old_evidence_scale in content_norm, "old_evidence_scale not found"
content_norm = content_norm.replace(old_evidence_scale, new_evidence_scale, 1)

# 7. Update process convenience entrypoint
old_return_process = "        return self.analyze_audio(audio_path)"
new_return_process = "        return self.analyze_audio(audio_path, stylistic_preset=stylistic_preset)"

assert old_return_process in content_norm, "old_return_process not found"
content_norm = content_norm.replace(old_return_process, new_return_process, 1)

old_process_sig = "    def process(\n        self,\n        audio_path: str,\n        target_raga: Optional[str] = None,\n        manual_sa_hz: Optional[float] = None,\n    ) -> Dict:"
new_process_sig = "    def process(\n        self,\n        audio_path: str,\n        target_raga: Optional[str] = None,\n        manual_sa_hz: Optional[float] = None,\n        stylistic_preset: Optional[str] = None,\n    ) -> Dict:"

assert old_process_sig in content_norm, "old_process_sig not found"
content_norm = content_norm.replace(old_process_sig, new_process_sig, 1)

p.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Patched src/pipeline.py with Acoustic Hygiene & Adaptive Thresholds")
