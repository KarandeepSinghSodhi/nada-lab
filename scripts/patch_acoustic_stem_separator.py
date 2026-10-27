# scripts/patch_acoustic_stem_separator.py

# 1. Update src/acoustic_sanitizer.py
with open('src/acoustic_sanitizer.py', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('\r\n', '\n')

code_to_add = '''
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
'''

if 'def separate_stems' not in text:
    target = '    def get_adaptive_thresholds('
    assert target in text, 'target method not found in acoustic_sanitizer.py'
    text = text.replace(target, code_to_add + '\n' + target, 1)
    with open('src/acoustic_sanitizer.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Added separate_stems to src/acoustic_sanitizer.py.")

# 2. Update tests/test_acoustic_sanitizer.py
with open('tests/test_acoustic_sanitizer.py', 'r', encoding='utf-8') as f:
    test_text = f.read()
test_text = test_text.replace('\r\n', '\n')

new_test = '''
def test_separate_stems_and_base64():
    sanitizer = AcousticSanitizer(sr=22050)
    t = np.linspace(0.0, 0.5, 11025)
    sine = 0.4 * np.sin(2.0 * np.pi * 330.0 * t)
    noise = np.zeros_like(t)
    noise[1000:1200] = 1.0 * np.random.randn(200)
    mix = (sine + noise).astype(np.float32)

    res = sanitizer.separate_stems(mix, sr=22050, num_peak_points=40)
    assert "vocal_audio" in res
    assert "accompaniment_audio" in res
    assert "vocal_peaks" in res
    assert "accompaniment_peaks" in res
    assert len(res["vocal_peaks"]) == 40
    assert len(res["accompaniment_peaks"]) == 40

    b64_wav = AcousticSanitizer.audio_to_base64_wav(res["vocal_audio"], sr=22050)
    assert b64_wav.startswith("data:audio/wav;base64,")
'''

if 'test_separate_stems_and_base64' not in test_text:
    test_text = test_text.rstrip() + '\n' + new_test
    with open('tests/test_acoustic_sanitizer.py', 'w', encoding='utf-8') as f:
        f.write(test_text)
    print("Added test_separate_stems_and_base64 to tests/test_acoustic_sanitizer.py.")

# 3. Update src/pipeline.py to return stems telemetry
with open('src/pipeline.py', 'r', encoding='utf-8') as f:
    pipe_text = f.read()
pipe_text = pipe_text.replace('\r\n', '\n')

pipe_old = '''        # 4. Extract Waveform Peaks
        waveform_peaks = self.extract_waveform_peaks(audio, num_points=160)'''

pipe_new = '''        # 4. Extract Waveform Peaks & Stem Envelopes
        stem_info = self.sanitizer.separate_stems(audio, sample_rate, num_peak_points=160)
        waveform_peaks = stem_info["mix_peaks"]'''

if pipe_old in pipe_text and 'stem_info' not in pipe_text:
    pipe_text = pipe_text.replace(pipe_old, pipe_new, 1)

pipe_ev_old = '''            "evidence": {
                "fundamental_frequency_hz": [round(float(f), 2) for f in f0_hz if not np.isnan(f)][:50],
                "confidence_weights": [round(float(p), 2) for p in voiced_prob if p > 0.3][:50],
                "waveform_peaks": waveform_peaks,'''

pipe_ev_new = '''            "evidence": {
                "fundamental_frequency_hz": [round(float(f), 2) for f in f0_hz if not np.isnan(f)][:50],
                "confidence_weights": [round(float(p), 2) for p in voiced_prob if p > 0.3][:50],
                "waveform_peaks": waveform_peaks,
                "stems": {
                    "vocal_peaks": stem_info["vocal_peaks"],
                    "accompaniment_peaks": stem_info["accompaniment_peaks"],
                    "mix_peaks": stem_info["mix_peaks"],
                    "bleed_pct": stem_info["bleed_pct"]
                },'''

if pipe_ev_old in pipe_text and '"stems":' not in pipe_text:
    pipe_text = pipe_text.replace(pipe_ev_old, pipe_ev_new, 1)

with open('src/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(pipe_text)
print("Updated src/pipeline.py with stems telemetry.")

# 4. Update server.py with /api/separate-stems endpoint
with open('server.py', 'r', encoding='utf-8') as f:
    srv_text = f.read()
srv_text = srv_text.replace('\r\n', '\n')

srv_endpoint = '''
@app.post("/api/separate-stems")
async def separate_stems_endpoint(file: UploadFile = File(...)):
    """
    Forensic Stem Separator: splits uploaded mix into isolated Lead Vocal
    and Accompaniment / Percussion Bed stems with interactive waveform envelopes.
    """
    import librosa
    from src.acoustic_sanitizer import AcousticSanitizer
    sanitizer = AcousticSanitizer()

    suffix = Path(file.filename or "uploaded.wav").suffix or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        y, sr = librosa.load(tmp_path, sr=22050, mono=True)
        stems = sanitizer.separate_stems(y, sr=sr, num_peak_points=160)
        vocal_b64 = AcousticSanitizer.audio_to_base64_wav(stems["vocal_audio"], sr=sr)
        accomp_b64 = AcousticSanitizer.audio_to_base64_wav(stems["accompaniment_audio"], sr=sr)

        return {
            "bleed_pct": stems["bleed_pct"],
            "vocal_peaks": stems["vocal_peaks"],
            "accompaniment_peaks": stems["accompaniment_peaks"],
            "mix_peaks": stems["mix_peaks"],
            "vocal_audio_url": vocal_b64,
            "accompaniment_audio_url": accomp_b64
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
'''

if '/api/separate-stems' not in srv_text:
    srv_target = '@app.post("/api/extract-sheet-music")'
    assert srv_target in srv_text, 'target not found in server.py'
    srv_text = srv_text.replace(srv_target, srv_endpoint + '\n\n' + srv_target, 1)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(srv_text)
    print("Added /api/separate-stems endpoint to server.py.")
