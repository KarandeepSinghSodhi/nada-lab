with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

sub_block = '''    return result


@app.post("/api/export-musicxml")
def export_musicxml_endpoint(req: SheetMusicExtractRequest):
    """
    Generates standard MusicXML 3.1 file bytes from extracted lead sheet notations
    for direct import into MuseScore, Sibelius, Finale, Dorico, and Soundslice.
    """
    from src.sheet_music_extractor import SheetMusicExtractor
    lead_sheet = SheetMusicExtractor.extract_sheet_music(
        notations=req.notations,
        lyrics_text=req.lyrics,
        tempo_bpm=req.tempo_bpm or 84.0,
        tonic_hz=req.tonic_hz or 146.83,
        phrase_key=req.phrase_key,
        instrument=req.instrument or "piano"
    )
    xml_content = SheetMusicExtractor.export_musicxml(lead_sheet)
    return Response(
        content=xml_content,
        media_type="application/vnd.recordare.musicxml+xml",
        headers={"Content-Disposition": 'attachment; filename="songlab_lead_sheet.musicxml"'},
    )'''

text = text.replace(sub_block, '    return result')

target = '''    result = SheetMusicExtractor.extract_sheet_music(
        notations=req.notations,
        lyrics_text=req.lyrics,
        tempo_bpm=req.tempo_bpm or 84.0,
        tonic_hz=req.tonic_hz or 146.83,
        phrase_key=req.phrase_key,
        instrument=req.instrument or "piano"
    )
    return result'''

replacement = target + '''


@app.post("/api/export-musicxml")
def export_musicxml_endpoint(req: SheetMusicExtractRequest):
    """
    Generates standard MusicXML 3.1 file bytes from extracted lead sheet notations
    for direct import into MuseScore, Sibelius, Finale, Dorico, and Soundslice.
    """
    from src.sheet_music_extractor import SheetMusicExtractor
    lead_sheet = SheetMusicExtractor.extract_sheet_music(
        notations=req.notations,
        lyrics_text=req.lyrics,
        tempo_bpm=req.tempo_bpm or 84.0,
        tonic_hz=req.tonic_hz or 146.83,
        phrase_key=req.phrase_key,
        instrument=req.instrument or "piano"
    )
    xml_content = SheetMusicExtractor.export_musicxml(lead_sheet)
    return Response(
        content=xml_content,
        media_type="application/vnd.recordare.musicxml+xml",
        headers={"Content-Disposition": 'attachment; filename="songlab_lead_sheet.musicxml"'},
    )'''

if target in text:
    text = text.replace(target, replacement, 1)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed server.py cleanly!")
else:
    print("Target not found!")
