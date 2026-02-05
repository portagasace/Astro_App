from .utils import norm360

def angdiff(a: float, b: float) -> float:
    return (b - a + 540.0) % 360.0 - 180.0

def mid_angle(a: float, b: float) -> float:
    return norm360(a + angdiff(a, b) / 2.0)

def in_arc(x: float, start: float, end: float) -> bool:
    x = norm360(x); start = norm360(start); end = norm360(end)
    if start <= end:
        return start <= x < end
    return x >= start or x < end

def bhava_boundaries_from_cusps(cusps12):
    cusps = [norm360(c) for c in cusps12]
    bhavas = []
    for i in range(12):
        prev_c = cusps[(i - 1) % 12]
        this_c = cusps[i]
        next_c = cusps[(i + 1) % 12]
        start = mid_angle(prev_c, this_c)
        end = mid_angle(this_c, next_c)
        bhavas.append({"house": i + 1, "start": start, "mid": this_c, "end": end})
    return bhavas

def bhava_of_longitude(lon: float, bhavas):
    lon = norm360(lon)
    for b in bhavas:
        if in_arc(lon, b["start"], b["end"]):
            return b["house"], b
    return None, None

def dist_from_mid(lon: float, bhava):
    return angdiff(bhava["mid"], norm360(lon))