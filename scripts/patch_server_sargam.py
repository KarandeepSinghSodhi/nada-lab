target_file = r'd:\Music\server.py'

with open(target_file, 'r', encoding='utf-8') as f:
    code = f.read()

old_req = """class SargamExportRequest(BaseModel):
    cents_trajectory: List[float]
    hop_sec: Optional[float] = 0.05"""

new_req = """class SargamExportRequest(BaseModel):
    cents_trajectory: Optional[List[float]] = None
    hop_sec: Optional[float] = 0.05
    lead_sheet: Optional[Dict[str, Any]] = None
    phrase_key: Optional[str] = None"""

if old_req in code:
    code = code.replace(old_req, new_req)
    print("Updated SargamExportRequest in server.py")
else:
    print("WARNING: old_req not found in server.py")

old_endpoint = """@app.post("/api/export-sargam")
def export_sargam(req: SargamExportRequest):
    \"\"\"
    Transforms continuous cents trajectory into Bhatkhande and Devanagari Sargam notes.
    \"\"\"
    transcript = MidiSargamExporter.trajectory_to_sargam_transcript(
        cents_trajectory=req.cents_trajectory,
        hop_sec=req.hop_sec or 0.05,
    )
    bhatkhande_tokens = [item["bhatkhande"] for item in transcript]
    devanagari_tokens = [item["devanagari"] for item in transcript]
    sheet_text = " ".join(bhatkhande_tokens)
    devanagari_text = " ".join(devanagari_tokens)
    return {
        "transcript": transcript,
        "bhatkhande_line": sheet_text,
        "devanagari_line": devanagari_text,
        "note_count": len(transcript),
    }"""

new_endpoint = """@app.post("/api/export-sargam")
def export_sargam(req: SargamExportRequest):
    \"\"\"
    Transforms continuous cents trajectory into Bhatkhande and Devanagari Sargam notes,
    and generates conservatory Bhatkhande score if lead sheet requested.
    \"\"\"
    from src.sheet_music_extractor import SheetMusicExtractor

    bhatkhande_sheet = None
    if req.lead_sheet:
        bhatkhande_sheet = SheetMusicExtractor.to_bhatkhande_sargam_sheet(req.lead_sheet)

    transcript = []
    if req.cents_trajectory:
        transcript = MidiSargamExporter.trajectory_to_sargam_transcript(
            cents_trajectory=req.cents_trajectory,
            hop_sec=req.hop_sec or 0.05,
        )
    bhatkhande_tokens = [item["bhatkhande"] for item in transcript]
    devanagari_tokens = [item["devanagari"] for item in transcript]
    sheet_text = " ".join(bhatkhande_tokens)
    devanagari_text = " ".join(devanagari_tokens)
    return {
        "transcript": transcript,
        "bhatkhande_line": sheet_text,
        "devanagari_line": devanagari_text,
        "note_count": len(transcript),
        "bhatkhande_sheet": bhatkhande_sheet,
    }"""

if old_endpoint in code:
    code = code.replace(old_endpoint, new_endpoint)
    print("Updated /api/export-sargam in server.py")
else:
    print("WARNING: old_endpoint not found in server.py")

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated server.py successfully.")
