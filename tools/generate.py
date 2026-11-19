"""Schema richting IRONMAN 70.3 Westfriesland (Hoorn, 20 juni 2027).
Weekritme: Ma zwem+kracht · Di fiets (Tacx) · Wo lopen · Do rust · Vr zwem+kracht · Za fiets (+brick) · Zo lopen."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
from datetime import date, timedelta

RACE = date(2027, 6, 20)
WEEK1 = date(2026, 11, 23)

def swim_min(m):
    return round(m / 100 * 3.3 / 5) * 5

def S(sport, title, minutes, detail="", zone="", key=False):
    return {"sport": sport, "title": title, "min": minutes, "detail": detail, "zone": zone, "key": key}

REST = S("rust", "Rust", 0)

def u(m):
    return f"{m//60}u{m%60:02d}" if m >= 60 and m % 60 else (f"{m//60} uur" if m >= 60 else f"{m} min")

# ---------- sessies ----------
KRACHT_A = {
 "lichaam": "Benen, billen, heupen & buik",
 "waarom": "Sterke benen en billen geven kracht op de fiets en beschermen knieën en heupen bij het lopen.",
 "oefeningen": [
  {"naam": "Goblet squat (dumbbell voor de borst)", "spieren": "Voorkant bovenbenen, billen", "sets": "3×10"},
  {"naam": "Roemeense deadlift met dumbbells", "spieren": "Achterkant bovenbenen (hamstrings), billen, onderrug", "sets": "3×10"},
  {"naam": "Step-up op een bankje", "spieren": "Bovenbenen, billen, balans", "sets": "3×8 per been"},
  {"naam": "Bruggetje op één been", "spieren": "Billen, hamstrings", "sets": "3×10 per been"},
  {"naam": "Kuitheffen op één been (langzaam zakken)", "spieren": "Kuiten, achillespees", "sets": "3×12 per been"},
  {"naam": "Zijplank met bovenste been heffen", "spieren": "Zijkant heup/bil, schuine buikspieren", "sets": "3×8 per kant"},
  {"naam": "Dead bug", "spieren": "Diepe buikspieren", "sets": "3×8 per kant"}
 ]}
KRACHT_B = {
 "lichaam": "Rug, schouders, armen & romp",
 "waarom": "Een sterke rug en stabiele schouders geven kracht in de zwemslag en voorkomen schouderblessures. Een sterke romp houdt je houding goed op de fiets en tijdens het lopen.",
 "oefeningen": [
  {"naam": "Roeien met dumbbell (één arm, steunend op bank)", "spieren": "Brede rugspier, achterkant schouder", "sets": "3×10 per arm"},
  {"naam": "Lat pulldown of naar beneden trekken met elastiek", "spieren": "Brede rugspier: de trekfase van de zwemslag", "sets": "3×12"},
  {"naam": "Push-ups (op knieën mag)", "spieren": "Borst, triceps, voorkant schouder", "sets": "3×8–12"},
  {"naam": "Face pulls of pull-aparts met elastiek", "spieren": "Achterkant schouders, bovenrug, houding", "sets": "3×15"},
  {"naam": "Buitenwaartse rotatie met elastiek (elleboog tegen de zij)", "spieren": "Rotatorcuff: beschermt de schouder bij zwemmen", "sets": "2×15 per arm"},
  {"naam": "Plank", "spieren": "Hele romp", "sets": "3×30–45 s"},
  {"naam": "Bird dog (op handen en knieën, arm en been strekken)", "spieren": "Onderrug, billen, stabiliteit", "sets": "3×8 per kant"}
 ]}

def kracht(phase, dag, kind="opbouw"):
    if phase == "taper":
        return {**S("kracht", "Mobiliteit", 20, "Rekken en lichte core. Geen gewichten meer."), "lichaam": "Heupen, kuiten, rug"}
    base = KRACHT_A if dag == 0 else KRACHT_B
    letter = "A" if dag == 0 else "B"
    if kind in ("herstel", "test"):
        sets, minutes, tip = "2 sets per oefening, licht gewicht.", 25, "Herstelweek: "
    elif phase in ("opbouw", "specifiek"):
        sets, minutes, tip = "2 sets per oefening, iets zwaarder gewicht en wat minder herhalingen.", 25, "Onderhoud: "
    else:
        sets, minutes, tip = "Gewicht zo kiezen dat de laatste 2 herhalingen zwaar zijn, maar de techniek goed blijft.", 35, ""
    return {**S("kracht", f"Kracht {letter}: {base['lichaam']}", minutes, tip + sets + " " + base["waarom"]),
            "lichaam": base["lichaam"], "oefeningen": base["oefeningen"]}

def zwem_ma(m, kind):
    if kind in ("herstel", "test"):
        return S("zwemmen", "Zwemmen rustig", swim_min(m), f"{m} m: 300 inzwemmen · 8×50 drills · rest rustig.", "Z1–Z2")
    kern = m - 700
    return S("zwemmen", "Zwemmen techniek + duur", swim_min(m),
             f"{m} m: 300 inzwemmen · 6×50 drills · {kern} m in blokken van 100–200 m (30 s rust) · 100 uitzwemmen.", "Z2")

def zwem_vr(m, phase, kind, wk):
    if kind in ("test", "zwemtest"):
        return S("zwemmen", "Zwemtest", swim_min(1500),
                 "Inzwemmen · 400 m zo snel als gelijkmatig kan · 5 min rust · 200 m zo snel mogelijk. Druk na elk stuk op de rondeknop van je horloge; de tijden worden daarna automatisch uit je Garmin gehaald.", "Test", True)
    if kind == "herstel":
        return S("zwemmen", "Zwemmen rustig", swim_min(m), f"{m} m rustig doorzwemmen.", "Z1–Z2")
    if phase in ("reset", "basis1"):
        n = (m - 600) // 100
        return S("zwemmen", "Zwemmen duur", swim_min(m), f"{m} m: 300 in · {n}×100 m gelijkmatig (15 s rust) · 300 uit.", "Z2")
    if phase == "basis2":
        n = (m - 700) // 200
        return S("zwemmen", "Zwemmen tempo", swim_min(m), f"{m} m: 400 in · {n}×200 m stevig (20 s rust) · 300 uit.", "Z3")
    lang = 1900 if wk % 2 == 0 else 1200
    return S("zwemmen", "Zwemmen raceduur", swim_min(m),
             f"{m} m: 300 in · {lang} m aan één stuk, elke 6–8 slagen vooruit kijken · rest rustig.", "Z2–Z3")

def fiets_di(minutes, phase, kind, wk):
    if kind == "test":
        return S("fietsen", "Fietstest (Tacx)", 60, "15 min inrijden · 20 min zo hard als gelijkmatig kan · uitrijden. Druk aan het begin en eind van de 20 min op de rondeknop; de uitslag wordt automatisch uit je Garmin gehaald.", "Test", True)
    if kind == "herstel" or phase == "reset":
        return S("fietsen", "Tacx rustig", minutes, f"{minutes} min rustig, cadans 85–95.", "Z1–Z2")
    if phase == "basis1":
        n = 3 if minutes < 55 else 4
        return S("fietsen", "Tacx tempo", minutes, f"10 min inrijden · {n}×6 min tempo (3 min rustig ertussen) · rest rustig.", "Z3", True)
    if phase == "basis2":
        blok = 10 if minutes < 70 else 12
        return S("fietsen", "Tacx sweet spot", minutes, f"10 min inrijden · 3×{blok} min zwaar-maar-vol-te-houden (4 min rustig) · rest rustig.", "Z3–Z4", True)
    blok = 20 if minutes < 85 else 25
    return S("fietsen", "Tacx racetempo", minutes, f"15 min inrijden · 2×{blok} min op 70.3-tempo (5 min rustig) · rest rustig.", "Z3", True)

def loop_wo(minutes, phase, kind, wk):
    if kind == "test":
        return S("lopen", "Looptest", 50, "15 min inlopen · 20 min zo hard als gelijkmatig kan · uitlopen. Druk aan het begin en eind van de 20 min op de rondeknop; de uitslag wordt automatisch uit je Garmin gehaald.", "Test", True)
    if kind == "herstel" or phase == "reset":
        return S("lopen", "Hardlopen rustig", minutes, f"{minutes} min rustig, hartslag onder 150.", "Z1–Z2")
    if phase == "basis1":
        return S("lopen", "Hardlopen + versnellingen", minutes, f"{minutes} min rustig, aan het eind 6×20 s soepel versnellen.", "Z2", True)
    if phase == "basis2":
        if wk % 2 == 0:
            return S("lopen", "Hardlopen heuvels", minutes, "15 min inlopen · 6×1,5 min heuvel/brug op, terug wandelen · rustig uitlopen.", "Z2 + Z4", True)
        return S("lopen", "Hardlopen tempo", minutes, "15 min inlopen · 2×10 min tempo (3 min dribbel) · rustig uitlopen.", "Z3", True)
    blok = 10 if wk % 2 == 0 else 12
    if phase == "specifiek":
        return S("lopen", "Hardlopen racetempo", minutes, "15 min inlopen · 2×15 min op 70.3-tempo (3 min rustig) · uitlopen.", "Z3", True)
    return S("lopen", "Hardlopen racetempo", minutes, f"15 min inlopen · 3×{blok} min op 70.3-tempo (3 min rustig) · uitlopen.", "Z3", True)

def fiets_za(minutes, phase, kind, wk):
    if kind == "herstel" or phase == "reset":
        return S("fietsen", "Duurrit rustig", minutes, f"{u(minutes)} rustig, Tacx of buiten.", "Z2")
    if phase in ("basis1", "basis2"):
        return S("fietsen", "Duurrit", minutes, f"{u(minutes)} rustig en gelijkmatig. Tacx of buiten. Na 45 min elke 20 min eten/drinken.", "Z2", True)
    tempo = "2×20" if minutes < 200 else "3×20"
    return S("fietsen", "Lange rit", minutes, f"{u(minutes)} buiten, met {tempo} min op 70.3-tempo. Oefen racevoeding: ±60 g koolhydraten per uur.", "Z2–Z3", True)

def brick(minutes):
    return S("lopen", "Brick: direct lopen", minutes, f"Meteen na het fietsen {minutes} min lopen: eerst 5 min rustig, dan racetempo.", "Z2–Z3")

def loop_zo(minutes, phase, kind, wk):
    if kind == "herstel" or phase == "reset":
        return S("lopen", "Duurloop rustig", minutes, f"{minutes} min rustig, hartslag onder 150.", "Z1–Z2")
    if phase in ("opbouw", "specifiek") and wk % 2 == 1:
        return S("lopen", "Duurloop + racetempo", minutes, f"{u(minutes)}, laatste 20–30 min op 70.3-tempo. Oefen met een gel.", "Z2–Z3", True)
    return S("lopen", "Duurloop", minutes, f"{u(minutes)} rustig: hartslag 135–150, ongeveer 6:45–7:15/km. Liever te langzaam dan te snel.", "Z2", True)

# (fase, soort, zwemMa, zwemVr, fietsDi, loopWo, fietsZa, loopZo, brick, focus)
W = [
    ("reset",  "herstel", 1500, 1500, 45, 35, 60, 60, 0, "Rustig beginnen: de afgelopen weken waren zwaar."),
    ("basis1", "zwemtest", 1600, 1500, 50, 40, 75, 70, 0, "Aerobe basis. Vrijdag een zwemtest: daarmee bepalen we je zwemtempo's."),
    ("basis1", "opbouw",  1700, 1700, 55, 45, 90, 75, 0, ""),
    ("basis1", "opbouw",  1800, 1800, 60, 45, 105, 80, 0, ""),
    ("basis1", "herstel", 1400, 1400, 45, 35, 60, 55, 0, "Kerstweek = herstelweek. Dagen schuiven mag."),
    ("basis1", "opbouw",  1800, 1800, 60, 45, 105, 80, 0, ""),
    ("basis1", "opbouw",  1900, 1900, 60, 50, 120, 85, 0, ""),
    ("basis1", "opbouw",  2000, 2000, 65, 50, 120, 90, 0, ""),
    ("basis1", "test",    1600, 1500, 60, 50, 75, 60, 0, "Testweek: di fietsen, wo lopen, vr zwemmen."),
    ("basis2", "opbouw",  2000, 2000, 60, 50, 120, 90, 0, "Blok 2: meer tempo."),
    ("basis2", "opbouw",  2100, 2100, 70, 55, 135, 95, 0, ""),
    ("basis2", "opbouw",  2200, 2200, 75, 55, 150, 100, 0, ""),
    ("basis2", "herstel", 1700, 1600, 50, 40, 80, 60, 0, "Herstelweek."),
    ("basis2", "opbouw",  2200, 2200, 75, 55, 150, 100, 0, ""),
    ("basis2", "opbouw",  2300, 2300, 75, 60, 165, 105, 0, ""),
    ("basis2", "opbouw",  2400, 2400, 80, 60, 180, 105, 0, "Eerste rit van 3 uur."),
    ("basis2", "test",    1800, 1500, 60, 50, 90, 65, 0, "Testweek: vergelijk met week 9."),
    ("opbouw", "opbouw",  2300, 2300, 75, 60, 165, 100, 15, "Racetempo en bricks (lopen direct na het fietsen)."),
    ("opbouw", "opbouw",  2400, 2400, 80, 60, 180, 105, 20, ""),
    ("opbouw", "opbouw",  2500, 2500, 85, 65, 195, 110, 20, ""),
    ("opbouw", "herstel", 1800, 1700, 60, 45, 100, 70, 0, "Herstelweek."),
    ("opbouw", "opbouw",  2500, 2500, 85, 65, 195, 105, 25, ""),
    ("opbouw", "opbouw",  2600, 2600, 90, 65, 210, 105, 25, "Openwater zodra het water warm genoeg is (wetsuit, nooit alleen)."),
    ("opbouw", "opbouw",  2600, 2600, 90, 65, 225, 115, 30, ""),
    ("opbouw", "herstel", 1800, 1800, 60, 45, 100, 70, 0, "Herstelweek. Check of al je wedstrijdspullen er zijn en goed zitten."),
    ("specifiek", "opbouw", 2500, 2500, 85, 60, 210, 100, 30, ""),
    ("specifiek", "opbouw", 2600, 2600, 90, 60, 240, 90, 30, "Piekweek: lange rit ≈ 90 km."),
    ("specifiek", "generale", 2400, 1500, 75, 50, 0, 60, 0, "Generale repetitie op zaterdag 5 juni."),
    ("taper",  "taper",   2000, 1800, 60, 45, 120, 60, 15, "Minder volume, wel scherp blijven."),
    ("taper",  "race",    0, 0, 0, 0, 0, 0, 0, "Raceweek: rust, slapen, goed eten. Niets nieuws."),
]

PHASES = {
    "reset": {"naam": "Reset", "kleur": "#94a3b8"},
    "basis1": {"naam": "Basis 1", "kleur": "#38bdf8"},
    "basis2": {"naam": "Basis 2", "kleur": "#0284c7"},
    "opbouw": {"naam": "Opbouw", "kleur": "#f59e0b"},
    "specifiek": {"naam": "Specifiek", "kleur": "#ef4444"},
    "taper": {"naam": "Taper", "kleur": "#a855f7"},
}

def build(i, c):
    phase, kind, zma, zvr, fdi, lwo, fza, lzo, br, focus = c
    swimtest = kind == "zwemtest"
    if swimtest: kind = "opbouw"
    wk = i + 1
    d = [[] for _ in range(7)]
    if kind == "race":
        d[0] = [S("zwemmen", "Zwemmen kort", 35, "1500 m met 4×100 op racetempo.", "Z2–Z3")]
        d[1] = [S("fietsen", "Tacx kort", 45, "45 min rustig met 3×5 min racetempo.", "Z2–Z3")]
        d[2] = [S("lopen", "Hardlopen kort", 30, "30 min rustig met 3×2 min racetempo.", "Z2–Z3")]
        d[3] = [REST]
        d[4] = [S("zwemmen", "Los zwemmen", 20, "20 min heel rustig, of rust als je reist.", "Z1")]
        d[5] = [S("fietsen", "Activeren + inchecken", 30, "15 min fietsen + 10 min lopen, kort en rustig. Fiets inchecken, vroeg naar bed.", "Z1–Z2")]
        d[6] = [S("race", "IRONMAN 70.3 Hoorn", 0, "Start 07:00. 1,9 km zwemmen · 90 km fietsen · 21,1 km lopen. Zie raceplan onderaan.", "", True)]
    elif kind == "generale":
        d[0] = [zwem_ma(zma, "opbouw"), kracht("taper", 0)]
        d[1] = [fiets_di(fdi, "specifiek", "opbouw", wk)]
        d[2] = [loop_wo(lwo, "specifiek", "opbouw", wk)]
        d[3] = [REST]
        d[4] = [zwem_vr(zvr, "x", "herstel", wk)]
        d[5] = [S("race", "Generale repetitie", 210, "1500 m zwemmen (openwater) · 2 uur fietsen, waarvan 90 min racetempo · 30 min lopen. Alles zoals op racedag: kleding, ontbijt, voeding.", "Z2–Z3", True)]
        d[6] = [loop_zo(lzo, "x", "herstel", wk)]
    elif kind == "taper":
        d[0] = [zwem_ma(zma, "opbouw"), kracht("taper", 0)]
        d[1] = [S("fietsen", "Tacx racetempo kort", fdi, "15 min inrijden · 2×12 min 70.3-tempo · uitrijden.", "Z3", True)]
        d[2] = [S("lopen", "Hardlopen racetempo kort", lwo, "15 min inlopen · 3×6 min racetempo · uitlopen.", "Z3", True)]
        d[3] = [REST]
        d[4] = [zwem_vr(zvr, "opbouw", "opbouw", 2), kracht("taper", 4)]
        d[5] = [S("fietsen", "Rit kort", fza, "2 uur buiten met 20 min racetempo, op de wedstrijdfiets.", "Z2–Z3"), brick(br)]
        d[6] = [loop_zo(lzo, "x", "herstel", wk)]
    else:
        d[0] = [zwem_ma(zma, kind), kracht(phase, 0, kind)]
        d[1] = [fiets_di(fdi, phase, kind, wk)]
        d[2] = [loop_wo(lwo, phase, kind, wk)]
        d[3] = [REST]
        d[4] = [zwem_vr(zvr, phase, "zwemtest" if swimtest else kind, wk), kracht(phase, 4, kind)]
        d[5] = [fiets_za(fza, phase, kind, wk)] + ([brick(br)] if br else [])
        d[6] = [loop_zo(lzo, phase, kind, wk)]
    if kind == "zwemtest": kind = "opbouw"
    label = {"herstel": "Herstelweek", "test": "Testweek", "opbouw": "Opbouwweek",
             "generale": "Generale repetitie", "taper": "Taper", "race": "Raceweek"}[kind]
    if phase == "reset": label = "Rustig starten"
    if phase == "specifiek" and kind == "opbouw": label = "Piekweek" if wk == 27 else "Specifieke week"
    return {"nr": wk, "start": (WEEK1 + timedelta(weeks=i)).isoformat(), "fase": phase, "label": label,
            "focus": focus, "totaal": sum(s["min"] for x in d for s in x), "dagen": d}

w0 = [[] for _ in range(7)]
w0[3] = [S("rust", "Rust (na het fietsen)", 0, "Readiness vandaag 7/100: na het fietsen van vanochtend de rest van de dag rust.")]
w0[4] = [S("zwemmen", "Zwemmen rustig", 40, "1200 m rustig, geen kracht deze keer.", "Z1–Z2")]
w0[5] = [S("fietsen", "Fietsen rustig", 60, "60 min rustig, Tacx of buiten.", "Z2")]
w0[6] = [S("lopen", "Hardlopen rustig", 45, "45 min rustig, hartslag onder 150.", "Z1–Z2")]
week0 = {"nr": 0, "start": (WEEK1 - timedelta(weeks=1)).isoformat(), "fase": "reset", "label": "Startweek",
         "focus": "Even gas terug na je zware week.", "totaal": 145, "dagen": w0}

weeks = [week0] + [build(i, c) for i, c in enumerate(W)]
assert date.fromisoformat(weeks[-1]["start"]) + timedelta(days=6) == RACE

# ---------- aanpassingen (overrides per datum) ----------
ADJ_PATH = os.path.join(HERE, "aanpassingen.json")
ADJ = json.load(open(ADJ_PATH, encoding="utf-8")) if os.path.exists(ADJ_PATH) else {}

def expand(sess):
    ref = sess.get("ref")
    if ref in ("krachtA", "krachtB"):
        phase = sess.get("fase", "basis1")
        return kracht(phase, 0 if ref == "krachtA" else 4, sess.get("soort", "opbouw"))
    if ref == "rust":
        return S("rust", "Rust", 0, sess.get("detail", ""))
    return S(sess["sport"], sess["title"], int(sess.get("min", 0)), sess.get("detail", ""), sess.get("zone", ""), bool(sess.get("key", False)))

for ds, adj in ADJ.items():
    dt = date.fromisoformat(ds)
    for w in weeks:
        start = date.fromisoformat(w["start"])
        if start <= dt < start + timedelta(days=7):
            di = (dt - start).days
            w["dagen"][di] = [expand(x) for x in adj["sessies"]]
            w.setdefault("aangepast", {})[str(di)] = adj.get("reden", "")
            w["totaal"] = sum(x["min"] for d in w["dagen"] for x in d)
            break
    else:
        raise SystemExit(f"aanpassing {ds} valt buiten het schema")

LOG = json.load(open(os.path.join(HERE, "logboek.json"), encoding="utf-8"))
data = {"logboek": LOG, "race": {"naam": "IRONMAN 70.3 Westfriesland", "plaats": "Hoorn", "datum": RACE.isoformat(), "start": "07:00"},
        "fases": PHASES, "weken": weeks, "bijgewerkt": date.today().isoformat()}
with open(os.path.join(HERE, "..", "data.js"), "w", encoding="utf-8") as f:
    f.write("window.PLAN = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n")
for w in weeks:
    print(w["nr"], w["start"], w["label"], round(w["totaal"] / 60, 1))
