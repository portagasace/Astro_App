from fastapi import FastAPI
from .astrology.models import (
    BirthRequest, NatalChartResponse,
    TransitRequest, TransitResponse,
    AIInterpretRequest, AIInterpretResponse
)
from .astrology.swiss import to_utc, natal_chart_full, transits_range
from .ai.hf_client import hf_generate

app = FastAPI(title="Kundali Backend (Lahiri + Nakshatra + Bhava + Transits)", version="1.0.0")

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
            "bhava_chalit": "Sripati unequal houses (houses_ex sidereal + 'S')",
            "note": "Nakshatra pada divisions use 27 equal segments; pada=navamsa size (3°20')."
        }
    }

@app.post("/api/transits", response_model=TransitResponse)
def transits(req: TransitRequest):
    days = transits_range(req.start_date_utc, req.end_date_utc, req.step_days, 
                          req.location.lat, req.location.lon)
    return {
        "days": days,
        "metadata": {
            "ayanamsa": "N.C. Lahiri",
            "node_type": "true_node",
            "step_days": req.step_days
        }
    }

@app.post("/api/ai/interpret", response_model=AIInterpretResponse)
async def ai_interpret(req: AIInterpretRequest):
    chart_dict = req.chart.model_dump()
    answer, meta = await hf_generate(chart_dict, req.question)
    return {"answer": answer, "model": meta.get("model", "unknown"), "metadata": meta}