RASHIS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANET_ABBR = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa",
    "Rahu": "Ra", "Ketu": "Ke"
}

def norm360(x: float) -> float:
    return x % 360.0

def lon_to_rashi(lon: float) -> str:
    return RASHIS[int(norm360(lon) // 30)]

def rashi_index(lon: float) -> int:
    return int(norm360(lon) // 30)

def whole_sign_house(asc_lon: float, planet_lon: float) -> int:
    a = rashi_index(asc_lon)
    p = rashi_index(planet_lon)
    return ((p - a) % 12) + 1

def is_retrograde(speed_deg_per_day: float) -> bool:
    # Swiss Ephemeris returns speed when FLG_SPEED is used; negative longitude rate => retrograde.
    return speed_deg_per_day < 0.0