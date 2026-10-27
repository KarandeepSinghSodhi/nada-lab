with open('src/pipeline.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Import PhraseRasaEngine
old_import = "from src.deficit_engine import DeficitEngine, SalienceTier, DeficitFlag, CritiqueFeedback"
new_import = """from src.deficit_engine import DeficitEngine, SalienceTier, DeficitFlag, CritiqueFeedback
from src.phrase_rasa_engine import PhraseRasaEngine"""

if old_import in text and "from src.phrase_rasa_engine import PhraseRasaEngine" not in text:
    text = text.replace(old_import, new_import, 1)
    print("Imported PhraseRasaEngine in pipeline.py")

# 2. Initialize in __init__
old_init = "self.deficit_engine = DeficitEngine(sr=self.sr)"
new_init = """self.deficit_engine = DeficitEngine(sr=self.sr)
        self.rasa_engine = PhraseRasaEngine()"""

if old_init in text and "self.rasa_engine = PhraseRasaEngine()" not in text:
    text = text.replace(old_init, new_init, 1)
    print("Initialized PhraseRasaEngine in SongLabPipeline.__init__")

# 3. Compute phrase_rasa_profile and attach to evidence
old_evidence = '            "phrase_critiques": [c.to_dict() for c in phrase_critiques],'
new_evidence = """            "phrase_critiques": [c.to_dict() for c in phrase_critiques],
            "phrase_rasa_profile": self.rasa_engine.analyze_phrase_rasa(
                pitch_trajectory=trajectory,
                identified_raga=identified_raga_name,
                bpm=tempo_info.get("bpm", 84.0) if tempo_info else 84.0,
                ornaments=[o.to_dict() for o in ornaments]
            ),"""

if old_evidence in text and '"phrase_rasa_profile":' not in text:
    text = text.replace(old_evidence, new_evidence, 1)
    print("Attached phrase_rasa_profile to evidence in pipeline.py")

with open('src/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated src/pipeline.py")
