import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.morphology import KiswahiliMorphologyEngine

app = FastAPI(
    title="Kiswahili Language Intelligence API",
    description="Backend API integrating Peter's engine and Larry's sentence morphological dataset.",
    version="2.1.0"
)

# Enable CORS so Cepha's Streamlit frontend can easily communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the morphology engine
try:
    engine = KiswahiliMorphologyEngine()
    engine_loaded = True
except Exception as e:
    print(f"⚠️ Engine initialization error: {e}")
    engine_loaded = False

# Helper to load Larry's 1,500+ sentence dataset if present
def load_sentence_dataset():
    data_path = Path(__file__).parent / "data" / "sentences_data.json"
    if not data_path.exists():
        return []
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            content = json.load(f)
            return content.get("sentences", [])
    except Exception:
        return []

class WordRequest(BaseModel):
    word: str

class SentenceRequest(BaseModel):
    sentence: str

@app.get("/", tags=["Health"])
def read_root():
    dataset = load_sentence_dataset()
    return {
        "status": "online",
        "engine_loaded": engine_loaded,
        "dataset_records": len(dataset),
        "docs_url": "/docs"
    }

@app.post("/api/v1/analyze/word", tags=["Analysis"])
def analyze_single_word(request: WordRequest):
    if not engine_loaded:
        raise HTTPException(status_code=503, detail="Morphology Engine is not initialized.")
    try:
        result = engine.analyze_word(request.word)
        return {"success": True, "input": request.word, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/analyze/sentence", tags=["Analysis"])
def analyze_full_sentence(request: SentenceRequest):
    if not engine_loaded:
        raise HTTPException(status_code=503, detail="Morphology Engine is not initialized.")
    try:
        results = engine.analyze_sentence(request.sentence)
        return {"success": True, "input": request.sentence, "analysis": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/dataset/search", tags=["Dataset"])
def search_dataset(query: str):
    """Search through Larry's pre-analyzed sentence dataset."""
    sentences = load_sentence_dataset()
    matches = [s for s in sentences if query.lower() in s.get("sentence", "").lower()]
    return {"success": True, "query": query, "matches_found": len(matches), "results": matches[:10]}