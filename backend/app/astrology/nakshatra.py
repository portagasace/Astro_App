from .utils import norm360

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya", "Ashlesha",
    "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha",
    "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanistha", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]

# Vimshottari lords repeating by nakshatra:
# Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury (repeat)
NAK_LORD_CYCLE = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]
NAKSHATRA_LORDS = [NAK_LORD_CYCLE[i % 9] for i in range(27)]

NAK_LEN = 360.0 / 27.0  # 13°20'
PADA_LEN = NAK_LEN / 4.0 # 3°20'

def nakshatra_info(lon: float):
    lon = norm360(lon)
    idx0 = int(lon // NAK_LEN)        # 0..26
    within = lon - idx0 * NAK_LEN
    pada = int(within // PADA_LEN) + 1 # 1..4
    start = idx0 * NAK_LEN
    end = start + NAK_LEN
    return {
        "name": NAKSHATRA_NAMES[idx0],
        "index": idx0 + 1,
        "pada": pada,
        "lord": NAKSHATRA_LORDS[idx0],
        "start_deg": start,
        "end_deg": end
    }