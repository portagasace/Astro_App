from .utils import norm360, rashi_index, RASHIS

NAV_LEN = 30.0 / 9.0 # 3°20'

MOVABLE = {0, 3, 6, 9}   # Aries, Cancer, Libra, Capricorn
FIXED   = {1, 4, 7, 10}  # Taurus, Leo, Scorpio, Aquarius
DUAL    = {2, 5, 8, 11}  # Gemini, Virgo, Sagittarius, Pisces

def navamsa_sign(lon: float):
    lon = norm360(lon)
    r = rashi_index(lon)
    within_sign = lon % 30.0
    nav_in_sign = int(within_sign // NAV_LEN) # 0..8

    if r in MOVABLE:
        start = r
    elif r in FIXED:
        start = (r + 8) % 12  # 9th from sign
    else:
        start = (r + 4) % 12  # 5th from sign

    nav_sign_idx = (start + nav_in_sign) % 12
    return {
        "sign": RASHIS[nav_sign_idx],
        "sign_index": nav_sign_idx + 1,
        "navamsa_index_in_sign": nav_in_sign + 1
    }