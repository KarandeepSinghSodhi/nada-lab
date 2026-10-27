from pathlib import Path

path = Path("src/pipeline.py")
content = path.read_text(encoding="utf-8")
content_norm = content.replace("\r\n", "\n")

# 1. Add import
old_import = "from src.sheet_music_extractor import SheetMusicExtractor"
new_import = """from src.sheet_music_extractor import SheetMusicExtractor
from src.in_between_notes_engine import InBetweenNotesEngine"""

assert old_import in content_norm, "old_import not found"
content_norm = content_norm.replace(old_import, new_import, 1)

# 2. Add engine initialization in __init__
old_init = "self.deficit_engine = DeficitEngine(target_raga_name=target_raga)"
new_init = """self.deficit_engine = DeficitEngine(target_raga_name=target_raga)
        self.in_between_engine = InBetweenNotesEngine(hop_sec=self.hop_sec)"""

assert old_init in content_norm, "old_init not found"
content_norm = content_norm.replace(old_init, new_init, 1)

# 3. Analyze in-between transitions before building evidence
old_evidence_build = """        # Build Structured Evidence Package
        evidence = {"""

new_evidence_build = """        # In-Between-The-Notes (Antar-Swara) Expressive Transition Analysis
        in_between_transitions = self.in_between_engine.analyze_phrase_transitions(
            notes=transcriptions,
            times=times,
            cents=cents,
        )
        in_between_dicts = [t.to_dict() for t in in_between_transitions]

        # Build Structured Evidence Package
        evidence = {"""

assert old_evidence_build in content_norm, "old_evidence_build not found"
content_norm = content_norm.replace(old_evidence_build, new_evidence_build, 1)

# 4. Update sheet_music_score and add in_between_notes to evidence
old_sheet_call = """            "sheet_music_score": SheetMusicExtractor.extract_sheet_music(
                notations=transcriptions,
                tempo_bpm=float(tempo_info.get("bpm", 84.0) if tempo_info else 84.0),
                tonic_hz=float(tonic_hz),
                instrument="piano"
            ),"""

new_sheet_call = """            "sheet_music_score": SheetMusicExtractor.extract_sheet_music(
                notations=transcriptions,
                tempo_bpm=float(tempo_info.get("bpm", 84.0) if tempo_info else 84.0),
                tonic_hz=float(tonic_hz),
                instrument="piano",
                in_between_transitions=in_between_dicts,
            ),
            "in_between_notes": in_between_dicts,"""

assert old_sheet_call in content_norm, "old_sheet_call not found"
content_norm = content_norm.replace(old_sheet_call, new_sheet_call, 1)

path.write_bytes(content_norm.replace("\n", "\r\n").encode("utf-8"))
print("SUCCESS: Patched src/pipeline.py with In-Between-The-Notes Engine")
