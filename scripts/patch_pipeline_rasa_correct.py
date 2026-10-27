with open('src/pipeline.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add import
old_imp = "from src.deficit_engine import DeficitEngine, CritiqueFeedback"
new_imp = """from src.deficit_engine import DeficitEngine, CritiqueFeedback
from src.phrase_rasa_engine import PhraseRasaEngine"""
text = text.replace(old_imp, new_imp, 1)

# 2. Add in __init__
old_init = "self.deficit_engine = DeficitEngine(target_raga_name=target_raga)"
new_init = """self.deficit_engine = DeficitEngine(target_raga_name=target_raga)
        self.rasa_engine = PhraseRasaEngine()"""
text = text.replace(old_init, new_init, 1)

with open('src/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated src/pipeline.py with PhraseRasaEngine")
