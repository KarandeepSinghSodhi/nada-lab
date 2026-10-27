from pathlib import Path

p = Path("server.py")
text = p.read_text(encoding="utf-8")
text_norm = text.replace("\r\n", "\n")

target = """@app.post("/api/analyze")
async def analyze_audio(
    file: UploadFile = File(...),
    target_raga: Optional[str] = Query(None, description="Optional target raga for specific deficit critique"),
    manual_sa_hz: Optional[float] = Query(None, description="Optional explicit tonic frequency in Hz"),
):"""

replacement = """@app.post("/api/analyze")
async def analyze_audio(
    file: UploadFile = File(...),
    target_raga: Optional[str] = Query(None, description="Optional target raga for specific deficit critique"),
    manual_sa_hz: Optional[float] = Query(None, description="Optional explicit tonic frequency in Hz"),
    stylistic_preset: Optional[str] = Query(None, description="Optional stylistic preset: khayal_standard, khayal_kirana, khayal_gwalior, thumri_light, dhrupad, drut_taan"),
):"""

target_call = """        results = pipeline.process(
            audio_path=tmp_path,
            target_raga=target_raga,
            manual_sa_hz=manual_sa_hz,
        )"""

replacement_call = """        results = pipeline.process(
            audio_path=tmp_path,
            target_raga=target_raga,
            manual_sa_hz=manual_sa_hz,
            stylistic_preset=stylistic_preset,
        )"""

assert target in text_norm, "target not found"
assert target_call in text_norm, "target_call not found"

text_norm = text_norm.replace(target, replacement, 1)
text_norm = text_norm.replace(target_call, replacement_call, 1)

p.write_bytes(text_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Updated server.py with stylistic_preset parameter")
