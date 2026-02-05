import json
import httpx
from ..core.config import settings

def build_prompt(chart, question: str) -> str:
    planets = "\n".join([
        f"- {p['name']}({p['abbr']}): {p['lon']:.2f}° {p['rashi']} "
        f"| H(R) {p['rashi_house']} H(B) {p['bhava_house']} "
        f"| {p['nakshatra']['name']} P{p['nakshatra']['pada']} "
        f"| NakLord {p['nakshatra']['lord']} | Nav {p['navamsa']['sign']}"
        for p in chart['planets']
    ])
    return f"""Interpret this Vedic chart (Sidereal Lahiri). Bhava Chalit uses Sripati unequal houses.
Asc: {chart['asc_rashi']} ({chart['ascendant']:.2f}°) | Nak: {chart['asc_nakshatra']['name']} P{chart['asc_nakshatra']['pada']}
Planets:
{planets}

Question: {question}
Return short bullet points."""

async def hf_generate(chart_dict, question: str):
    if not settings.HF_ENDPOINT_URL or not settings.HF_TOKEN:
        return ("AI not configured. Set HF_ENDPOINT_URL and HF_TOKEN.", 
                {"configured": False, "model": settings.HF_MODEL_NAME})

    payload = {
        "inputs": build_prompt(chart_dict, question),
        "parameters": {"max_new_tokens": 350, "temperature": 0.4, "top_p": 0.9, "return_full_text": False}
    }
    headers = {"Authorization": f"Bearer {settings.HF_TOKEN}", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=90) as client:
        r = await client.post(settings.HF_ENDPOINT_URL, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()

    if isinstance(data, list) and data and isinstance(data[0], dict) and "generated_text" in data[0]:
        return (data[0]["generated_text"], {"configured": True, "model": settings.HF_MODEL_NAME})

    return (json.dumps(data)[:2000], {"configured": True, "model": settings.HF_MODEL_NAME, "note": "Unexpected response format"})