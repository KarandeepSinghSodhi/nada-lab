from pathlib import Path

path = Path("server.py")
content = path.read_text(encoding="utf-8")
content_norm = content.replace("\r\n", "\n")

target_marker = """@app.post("/api/extract-sheet-music")
def extract_sheet_music_endpoint(req: SheetMusicExtractRequest):"""

new_endpoints = """class InBetweenNotesRequest(BaseModel):
    notes: List[Dict[str, Any]]
    times: List[float]
    cents: List[float]
    syllables: Optional[List[str]] = None


@app.post("/api/analyze-in-between-notes")
def analyze_in_between_notes_endpoint(req: InBetweenNotesRequest):
    \"\"\"
    Forensic Antar-Swara endpoint:
    Analyzes what happens BETWEEN discrete musical notes (Meend curvatures,
    Kan grace touches, Murki turns, Gamak shakes, and syllabic melisma).
    \"\"\"
    from src.in_between_notes_engine import InBetweenNotesEngine
    engine = InBetweenNotesEngine()
    transitions = engine.analyze_phrase_transitions(
        notes=req.notes,
        times=np.array(req.times, dtype=float),
        cents=np.array(req.cents, dtype=float),
        syllables=req.syllables,
    )
    return {
        "transitions": [t.to_dict() for t in transitions],
        "total_transitions": len(transitions),
    }


@app.get("/api/hindi-songs-benchmark")
def get_hindi_songs_benchmark():
    \"\"\"
    Serves the quantitative Hindi songs & Indian classical Antar-Swara benchmark
    comparing naive discrete note transcribers vs Song Lab's continuous expressive engine.
    \"\"\"
    from research_lab.benchmarks.benchmark_hindi_songs_in_between import run_hindi_songs_benchmark
    res_file = Path("research_lab/benchmarks/results/hindi_songs_antar_swara_benchmark_results.json")
    if res_file.exists():
        with open(res_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return run_hindi_songs_benchmark()


@app.post("/api/extract-sheet-music")
def extract_sheet_music_endpoint(req: SheetMusicExtractRequest):"""

assert target_marker in content_norm, "target_marker not found"
content_norm = content_norm.replace(target_marker, new_endpoints, 1)

path.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Patched server.py with In-Between Notes endpoints")
