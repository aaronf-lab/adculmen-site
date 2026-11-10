"""Builds v2/storms.json from NOAA SPC filtered storm report CSVs only (official NWS LSR-based data).
No other sources, no API keys. Times converted to America/Chicago; dates are local Central dates."""
import csv, io, json, sys, urllib.request
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
CT = ZoneInfo("America/Chicago")
CORE = ["MN","IA","ND","SD","WI","IL","IN","MI"]; ACTIVE = ["CO","TX","TN","FL","AZ","NM","AL"]
NAMES = {"MN":"Minnesota","IA":"Iowa","ND":"North Dakota","SD":"South Dakota","WI":"Wisconsin","IL":"Illinois","IN":"Indiana",
         "MI":"Michigan","CO":"Colorado","TX":"Texas","TN":"Tennessee","FL":"Florida","AZ":"Arizona","NM":"New Mexico","AL":"Alabama"}
DAYS, MAX_ITEMS, MAX_CORE = 60, 12, 7
def fetch(ymd):
    url = f"https://www.spc.noaa.gov/climo/reports/{ymd}_rpts_filtered.csv"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"adculmen-storms/1.0"}), timeout=30) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return ""
def tfmt(dt): return dt.strftime("%-I:%M %p ") + dt.tzname()
today = datetime.now(timezone.utc).date(); groups = {}
for back in range(DAYS, 0, -1):
    day = today - timedelta(days=back); ymd = day.strftime("%y%m%d"); sec = None
    for row in csv.reader(io.StringIO(fetch(ymd))):
        if not row: continue
        if row[0] == "Time": sec = row[1]; continue
        if len(row) < 5 or row[4] not in CORE + ACTIVE: continue
        hh, mm = int(row[0][:2]), int(row[0][2:4])
        utc = datetime(day.year, day.month, day.day, hh, mm, tzinfo=timezone.utc) + (timedelta(days=1) if hh < 12 else timedelta())
        g = groups.setdefault((ymd, row[4]), {"ymd": ymd, "st": row[4], "h": [], "w": [], "t": [], "c": set(), "times": []})
        loc, cty, lt = row[2], row[3], utc.astimezone(CT); g["c"].add(cty); g["times"].append(lt)
        if sec == "Size": g["h"].append((int(row[1]) / 100, loc, cty, lt))
        elif sec == "Speed": g["w"].append((None if row[1] == "UNK" else int(row[1]), loc, cty, lt))
        else: g["t"].append((loc, cty, lt))
items = []
for g in groups.values():
    mh = max(g["h"], key=lambda x: x[0], default=None); mw = max([w for w in g["w"] if w[0]], key=lambda x: x[0], default=None)
    lead = mh or mw or (None, *g["t"][0]) if (mh or mw or g["t"]) else None
    t0, t1 = min(g["times"]), max(g["times"]); end = tfmt(t1) + (f" ({t1:%b} {t1.day})" if t1.date() != t0.date() else "")
    it = {"date": t0.date().isoformat(), "dateLabel": f"{t0:%b} {t0.day}, {t0.year}", "state": NAMES[g["st"]], "st": g["st"],
          "timeStart": tfmt(t0), "timeEnd": end, "location": f"{lead[1]}, {lead[2]} Co." if lead else None,
          "maxHailIn": mh[0] if mh else None, "hailAt": f"{mh[1]}, {mh[2]} Co., {tfmt(mh[3])}" if mh else None,
          "maxGustMph": mw[0] if mw else None, "gustAt": f"{mw[1]}, {mw[2]} Co." if mw else None,
          "hailReports": len(g["h"]), "windReports": len(g["w"]), "tornadoReports": len(g["t"]),
          "counties": sorted(g["c"]), "countyCount": len(g["c"]), "source": "SPC storm reports (NWS LSRs)",
          "sourceUrl": f"https://www.spc.noaa.gov/climo/reports/{g['ymd']}_rpts.html", "_ymd": g["ymd"]}
    n = it["hailReports"] + it["windReports"] + it["tornadoReports"]
    if g["st"] == "MN" or n >= 3 or (it["maxHailIn"] or 0) >= 1.75 or it["tornadoReports"] or (it["maxGustMph"] or 0) >= 65:
        it["_score"] = (it["maxHailIn"] or 0) * 30 + (it["maxGustMph"] or 0) + it["tornadoReports"] * 20 + it["countyCount"] * 2
        items.append(it)
items.sort(key=lambda x: x["_ymd"], reverse=True)
core = [i for i in items if i["st"] in CORE][:MAX_CORE]
active = sorted([i for i in items if i["st"] not in CORE], key=lambda x: -x["_score"])[:MAX_ITEMS - len(core)]
pick = sorted(core + active, key=lambda x: (x["_ymd"], x["st"] == "MN"), reverse=True)
for i in pick: i.pop("_ymd"); i.pop("_score"); i.pop("st")
out = {"generated": today.isoformat(), "window": f"{(today - timedelta(days=DAYS)).isoformat()} to {today.isoformat()}",
       "note": "Territory storms from SPC filtered storm reports (NWS local storm reports). Times Central; dates are local (Central) dates.", "items": pick}
if pick: json.dump(out, open(sys.argv[1], "w"), indent=1)
print(len(pick), "items")
