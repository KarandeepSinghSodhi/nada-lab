# scripts/patch_server_sheet_music.py

with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

target1 = '''class SargamExportRequest(BaseModel):
    cents_trajectory: List[float]
    hop_sec: Optional[float] = 0.05'''

replacement1 = '''class SargamExportRequest(BaseModel):
    cents_trajectory: List[float]
    hop_sec: Optional[float] = 0.05


class SheetMusicExtractRequest(BaseModel):
    notations: List[Dict[str, Any]]
    lyrics: Optional[str] = None
    tempo_bpm: Optional[float] = 84.0
    tonic_hz: Optional[float] = 146.83
    phrase_key: Optional[str] = None
    instrument: Optional[str] = "piano"'''

target2 = '''@app.post("/api/export-sargam")
def export_sargam(req: SargamExportRequest):'''

replacement2 = '''@app.post("/api/extract-sheet-music")
def extract_sheet_music_endpoint(req: SheetMusicExtractRequest):
    """
    Extracts structured Lead Sheet Score aligning lyrics with notes to play,
    chords, rhythm values, and multi-instrument fingering/tab guides.
    """
    from src.sheet_music_extractor import SheetMusicExtractor
    result = SheetMusicExtractor.extract_sheet_music(
        notations=req.notations,
        lyrics_text=req.lyrics,
        tempo_bpm=req.tempo_bpm or 84.0,
        tonic_hz=req.tonic_hz or 146.83,
        phrase_key=req.phrase_key,
        instrument=req.instrument or "piano"
    )
    return result


@app.post("/api/export-sargam")
def export_sargam(req: SargamExportRequest):'''

text_lf = text.replace('\r\n', '\n')
target1_lf = target1.replace('\r\n', '\n')
replacement1_lf = replacement1.replace('\r\n', '\n')
target2_lf = target2.replace('\r\n', '\n')
replacement2_lf = replacement2.replace('\r\n', '\n')

if target1_lf in text_lf and target2_lf in text_lf:
    new_text = text_lf.replace(target1_lf, replacement1_lf).replace(target2_lf, replacement2_lf).replace('\n', '\r\n')
    with open('server.py', 'wb') as f:
        f.write(new_text.encode('utf-8'))
    print('SUCCESS: Patched server.py with /api/extract-sheet-music endpoint!')
else:
    print('ERROR: Target not found in server.py')
