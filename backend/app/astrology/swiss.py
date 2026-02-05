import swisseph as swe
import pytz
from datetime import datetime, timezone, timedelta

from ..core.config import settings
from .utils import norm360, lon_to_rashi, whole_sign_house, PLANET_ABBR, is_retrograde
from .nakshatra import nakshatra_info
from .navamsa import navamsa_sign
from .bhava import bhava_boundaries_from_cusps, bhava_of_longitude, dist_from_mid
from .layout import diamond_layout

# Swiss Ephemeris setup
swe.set_ephe_path(settings.EPHE_PATH)
swe.set_sid_mode(swe.SIDM_LAHIRI) # Lahiri

PLANETS = [
    ("Sun", swe.SUN),
    ("Moon", swe.MOON),
    ("Mars", swe.MARS),
    ("Mercury", swe.MERCURY),
    ("Jupiter", swe.JUPITER),
    ("Venus", swe.VENUS),
    ("Saturn", swe.SATURN),
]

def to_utc(datetime_local_iso: str, tz_name: str) -> datetime:
    tz = pytz.timezone(tz_name)
    dt_local = datetime.fromisoformat(datetime_local_iso)
    dt_local = tz.localize(dt_local)
    return dt_local.astimezone(pytz.utc).replace(tzinfo=timezone.utc)

def julian_day_ut(utc_dt: datetime) -> float:
    ut_hours = utc_dt.hour + utc_dt.minute/60 + utc_dt.second/3600
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, ut_hours, swe.GREG_CAL)

def get_ayanamsa(jd_ut: float) -> float:
    return float(swe.get_ayanamsa_ut(jd_ut))

def calc_sidereal_body(jd_ut: float, body_id: int):
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL # sidereal + speed
    xx, _ = swe.calc_ut(jd_ut, body_id, flags)
    lon = norm360(xx[0])
    lat = float(xx[1])
    speed = float(xx[3]) # deg/day (can be negative)
    return lon, lat, speed

def calc_asc_and_cusps_sripati(jd_ut: float, lat: float, lon: float):
    cuspflag = swe.FLG_SIDEREAL # sidereal houses
    hsys = b'S' # Sripati
    
    # FIX 1: Correct Argument Order (lat, lon before hsys)
    cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, hsys, cuspflag)
    
    asc = norm360(ascmc[0])
    
    # FIX 2: Robust Length Check
    # pyswisseph sometimes returns 13 items (0-index empty) and sometimes 12 items.
    if len(cusps) == 13:
        # Standard C-style: Index 0 is dummy, Houses are 1-12
        cusps12 = [norm360(cusps[i]) for i in range(1, 13)]
    else:
        # Pythonic style: Index 0 is House 1
        cusps12 = [norm360(c) for c in cusps]
        
    return asc, cusps12

def render_planet_label(p):
    # Example: "MoR" for retrograde Moon
    ab = p["abbr"]
    return f"{ab}R" if p["retrograde"] else ab

def build_views(asc: float, planets: list, bhavas: list, cusps12: list):
    # Returns rashi and bhava views as house cells with sign + list of rendered planet labels
    
    # group labels
    by_rashi_house = {i: [] for i in range(1, 13)}
    by_bhava_house = {i: [] for i in range(1, 13)}
    for p in planets:
        by_rashi_house[p["rashi_house"]].append(render_planet_label(p))
        by_bhava_house[p["bhava_house"]].append(render_planet_label(p))
    
    # rashi signs per house (whole sign from asc)
    asc_sign_idx = int(asc // 30)
    rashi_cells = []
    for h in range(1, 13):
        sign_idx = (asc_sign_idx + (h - 1)) % 12
        sign_name = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio",
                     "Sagittarius","Capricorn","Aquarius","Pisces"][sign_idx]
        rashi_cells.append({
            "house": h,
            "sign": sign_name,
            "planets": sorted(by_rashi_house[h]),
            "details": {}
        })

    # bhava signs per house (use cusp midpoint sign as label)
    bhava_cells = []
    for h in range(1, 13):
        mid = cusps12[h-1]
        sign_name = lon_to_rashi(mid)
        bhava_cells.append({
            "house": h,
            "sign": sign_name,
            "planets": sorted(by_bhava_house[h]),
            "details": {"mid": mid}
        })
    
    return {
        "rashi": {"mode": "rashi", "cells": rashi_cells},
        "bhava": {"mode": "bhava", "cells": bhava_cells},
    }

def natal_chart_full(utc_dt: datetime, lat: float, lon: float):
    jd_ut = julian_day_ut(utc_dt)
    ay = get_ayanamsa(jd_ut)

    asc, cusps12 = calc_asc_and_cusps_sripati(jd_ut, lat, lon)
    bhavas = bhava_boundaries_from_cusps(cusps12)

    planets_out = []

    # planets
    for name, pid in PLANETS:
        plon, plat, pspeed = calc_sidereal_body(jd_ut, pid)
        retro = is_retrograde(pspeed)
        r_house = whole_sign_house(asc, plon)
        b_house, bobj = bhava_of_longitude(plon, bhavas)

        planets_out.append({
            "name": name,
            "abbr": PLANET_ABBR[name],
            "lon": plon,
            "lat": plat,
            "speed": pspeed,
            "retrograde": retro,
            "rashi": lon_to_rashi(plon),
            "rashi_house": r_house,
            "nakshatra": nakshatra_info(plon),
            "navamsa": navamsa_sign(plon),
            "bhava_house": b_house,
            "dist_from_bhava_mid_deg": dist_from_mid(plon, bobj),
        })

    # Rahu/Ketu true node
    rahu_lon, rahu_lat, rahu_speed = calc_sidereal_body(jd_ut, swe.TRUE_NODE)
    ketu_lon = norm360(rahu_lon + 180.0)
    ketu_lat = -rahu_lat

    for nm, nlon, nlat, nspeed in [
        ("Rahu", rahu_lon, rahu_lat, rahu_speed),
        ("Ketu", ketu_lon, ketu_lat, rahu_speed),
    ]:
        retro = is_retrograde(nspeed)
        r_house = whole_sign_house(asc, nlon)
        b_house, bobj = bhava_of_longitude(nlon, bhavas)

        planets_out.append({
            "name": nm,
            "abbr": PLANET_ABBR[nm],
            "lon": nlon,
            "lat": nlat,
            "speed": nspeed,
            "retrograde": retro,
            "rashi": lon_to_rashi(nlon),
            "rashi_house": r_house,
            "nakshatra": nakshatra_info(nlon),
            "navamsa": navamsa_sign(nlon),
            "bhava_house": b_house,
            "dist_from_bhava_mid_deg": dist_from_mid(nlon, bobj),
        })

    # Asc info
    asc_rashi = lon_to_rashi(asc)
    asc_nak = nakshatra_info(asc)
    asc_nav = navamsa_sign(asc)

    views = build_views(asc, planets_out, bhavas, cusps12)

    return {
        "ayanamsa": ay,
        "ascendant": asc,
        "asc_rashi": asc_rashi,
        "asc_nakshatra": asc_nak,
        "asc_navamsa": asc_nav,
        "cusps": cusps12,
        "bhavas": bhavas,
        "planets": planets_out,
        "layout": diamond_layout(),
        "views": views
    }

def transits_range(start_date_utc: str, end_date_utc: str, step_days: int, lat: float, lon: float):
    start = datetime.fromisoformat(start_date_utc).replace(tzinfo=timezone.utc)
    end = datetime.fromisoformat(end_date_utc).replace(tzinfo=timezone.utc)
    step = timedelta(days=step_days)

    days = []
    d = start
    while d <= end:
        # use noon for stability
        dt = d.replace(hour=12, minute=0, second=0)
        chart = natal_chart_full(dt, lat, lon)
        days.append({
            "date_utc": d.date().isoformat(),
            "ascendant": chart["ascendant"],
            "asc_rashi": chart["asc_rashi"],
            "planets": chart["planets"],
            "views": chart["views"]
        })
        d += step
    
    return days