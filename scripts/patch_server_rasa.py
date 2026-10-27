with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Import PhraseRasaEngine
old_imp = "from src.pipeline import SongLabPipeline"
new_imp = """from src.pipeline import SongLabPipeline
from src.phrase_rasa_engine import PhraseRasaEngine"""

if old_imp in text and "from src.phrase_rasa_engine import PhraseRasaEngine" not in text:
    text = text.replace(old_imp, new_imp, 1)
    print("Added import to server.py")

# Add Request Model and Endpoint
endpoint_code = """
class RasaAnalysisRequest(BaseModel):
    pitch_trajectory: List[Dict[str, float]]
    identified_raga: Optional[str] = "Yaman"
    bpm: Optional[float] = 84.0


@app.post("/api/analyze-rasa")
async def analyze_phrase_rasa_endpoint(req: RasaAnalysisRequest):
    \"\"\"
    Computes holistic piece- and phrase-level emotional aesthetic (Rasa)
    using melodic contour trajectory, Nyasa resting stability, kinematics,
    and classical musicological treatises.
    \"\"\"
    engine = PhraseRasaEngine()
    result = engine.analyze_phrase_rasa(
        pitch_trajectory=req.pitch_trajectory,
        identified_raga=req.identified_raga or "Yaman",
        bpm=req.bpm or 84.0
    )
    return result
"""

if "/api/analyze-rasa" not in text:
    idx = text.find('@app.post("/api/analyze")')
    text = text[:idx] + endpoint_code + '\n' + text[idx:]
    print("Added /api/analyze-rasa endpoint to server.py")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated server.py")
