from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <--- IMPORT THIS
from .astrology.models import (
    BirthRequest, NatalChartResponse,
    TransitRequest, TransitResponse,
    AIInterpretRequest, AIInterpretResponse
)
from .astrology.swiss import to_utc, natal_chart_full, transits_range
from .ai.hf_client import hf_generate

app = FastAPI(title="Kundali Backend", version="1.0.0")

# --- VITAL FIX: ALLOW FRONTEND CONNECTION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Web, Android, iOS)
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)
# --------------------------------------------

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/api/natal-chart", response_model=NatalChartResponse)
def natal(req: BirthRequest):
    utc_dt = to_utc(req.datetime_local, req.timezone)
    chart = natal_chart_full(utc_dt, req.location.lat, req.location.lon)

    return {
        "utc_datetime": utc_dt.isoformat(),
        **chart,
        "metadata": {
            "ayanamsa": "N.C. Lahiri",
            "node_type": "true_node",
            "bhava_chalit": "Sripati",
        }
    }

@app.post("/api/transits", response_model=TransitResponse)
def transits(req: TransitRequest):
    days = transits_range(req.start_date_utc, req.end_date_utc, req.step_days, 
                          req.location.lat, req.location.lon)
    return {
        "days": days,
        "metadata": {"step_days": req.step_days}
    }

@app.post("/api/ai/interpret", response_model=AIInterpretResponse)
async def ai_interpret(req: AIInterpretRequest):
    chart_dict = req.chart.model_dump()
    answer, meta = await hf_generate(chart_dict, req.question)
    return {"answer": answer, "model": meta.get("model", "unknown"), "metadata": meta}