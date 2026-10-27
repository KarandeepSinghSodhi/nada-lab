# -*- coding: utf-8 -*-
"""
Script to update server.py with Circadian Samay Chakra and Expressive Meend Synthesizer endpoints
"""

with open("server.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
import_anchor = "from src.alankar_generator import AlankarGenerator"
new_imports = """from src.alankar_generator import AlankarGenerator
from src.circadian_engine import CircadianRagaEngine
from src.expressive_synthesizer import ExpressiveMeendSynthesizer"""

if import_anchor in content:
    content = content.replace(import_anchor, new_imports, 1)
    print("Imports updated in server.py.")
else:
    print("Warning: import_anchor not found!")

# 2. Pydantic request model
model_anchor = "class DtwCompareRequest(BaseModel):"
new_model = """class ExpressiveContourRequest(BaseModel):
    notes: List[str] = ["Sa", "Re", "Ga", "Pa"]
    raga: str = "Yaman"
    tonic_hz: float = 146.83
    tempo_bpm: float = 60.0
    meend_expressiveness: float = 0.85


class DtwCompareRequest(BaseModel):"""

if model_anchor in content:
    content = content.replace(model_anchor, new_model, 1)
    print("Pydantic model added to server.py.")
else:
    print("Warning: model_anchor not found!")

# 3. Endpoints
endpoint_anchor = "@app.post(\"/api/compare-dtw\")"
new_endpoints = """@app.get("/api/circadian-raga")
def get_circadian_raga(hour: Optional[int] = None, minute: Optional[int] = 0):
    \"\"\"
    Returns chronobiological circadian raga recommendation, active Prahara,
    neuro-endocrine phase, and optimal acoustic tuning parameters.
    \"\"\"
    return CircadianRagaEngine.get_circadian_recommendation(hour, minute)


@app.post("/api/generate-expressive-contour")
def generate_expressive_contour(req: ExpressiveContourRequest):
    \"\"\"
    Generates physics-informed sigmoidal meend flow splines and authentic
    andolan oscillations for humanized expressive classical trajectories.
    \"\"\"
    return ExpressiveMeendSynthesizer.generate_trajectory(
        notes=req.notes,
        raga=req.raga,
        tonic_hz=req.tonic_hz,
        tempo_bpm=req.tempo_bpm,
        meend_expressiveness=req.meend_expressiveness
    )


@app.post("/api/compare-dtw")"""

if endpoint_anchor in content:
    content = content.replace(endpoint_anchor, new_endpoints, 1)
    print("Endpoints added to server.py.")
else:
    print("Warning: endpoint_anchor not found!")

with open("server.py", "w", encoding="utf-8") as f:
    f.write(content)

print("server.py updated successfully!")
