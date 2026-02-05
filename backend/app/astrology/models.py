from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Location(BaseModel):
    lat: float
    lon: float
    alt_m: float = 0.0

class BirthRequest(BaseModel):
    datetime_local: str
    timezone: str
    location: Location
    node_type: str = Field("true", description="Rahu/Ketu True Node")
    bhava_house_system: str = Field("sripati", description="Unequal houses via Sripati")

class NakshatraInfo(BaseModel):
    name: str
    index: int
    pada: int
    lord: str
    start_deg: float
    end_deg: float

class NavamsaInfo(BaseModel):
    sign: str
    sign_index: int
    navamsa_index_in_sign: int

class PlanetPosition(BaseModel):
    name: str
    abbr: str
    lon: float
    lat: float
    speed: Optional[float] = None
    retrograde: bool
    
    rashi: str
    rashi_house: int
    
    nakshatra: NakshatraInfo
    navamsa: NavamsaInfo
    
    bhava_house: int
    dist_from_bhava_mid_deg: float

class Bhava(BaseModel):
    house: int
    start: float
    mid: float
    end: float

class HouseCell(BaseModel):
    house: int
    sign: str
    planets: List[str] # list of rendered labels like "MoR", "Ra"
    details: Dict[str, Any] = {}

class ChartView(BaseModel):
    mode: str # "rashi" or "bhava"
    cells: List[HouseCell]

class NatalChartResponse(BaseModel):
    utc_datetime: str
    ayanamsa: float
    
    ascendant: float
    asc_rashi: str
    asc_nakshatra: NakshatraInfo
    asc_navamsa: NavamsaInfo
    
    planets: List[PlanetPosition]
    
    bhavas: List[Bhava]
    cusps: List[float]
    
    layout: Dict[str, Any]
    views: Dict[str, ChartView] # {"rashi":..., "bhava":...}
    
    metadata: Dict[str, Any]

class TransitRequest(BaseModel):
    start_date_utc: str
    end_date_utc: str
    step_days: int = Field(1, ge=1, le=7)
    location: Location

class TransitDay(BaseModel):
    date_utc: str
    ascendant: float
    asc_rashi: str
    planets: List[PlanetPosition]
    views: Dict[str, ChartView]

class TransitResponse(BaseModel):
    days: List[TransitDay]
    metadata: Dict[str, Any]

class AIInterpretRequest(BaseModel):
    chart: NatalChartResponse
    question: str = Field("Give a concise interpretation of this chart.", max_length=2000)

class AIInterpretResponse(BaseModel):
    answer: str
    model: str
    metadata: Dict[str, Any]