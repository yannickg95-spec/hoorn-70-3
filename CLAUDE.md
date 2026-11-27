# Trainingssite "Op weg naar Hoorn"

Statische GitHub Pages-site (branch `main`, root) met een 30-weken trainingsschema richting IRONMAN 70.3 Westfriesland (Hoorn, zo 20 juni 2027).

## Bestanden
- `index.html`: de site (vanilla HTML/JS, leest `data.js`).
- `data.js`: **gegenereerd**, niet met de hand aanpassen.
- `tools/generate.py`: het schema (weekopzet, sessies, kracht A/B). Schrijft `data.js`.
- `tools/aanpassingen.json`: aanpassingen op het schema per datum (zie hieronder). Hiermee worden trainingen getweakt zonder `generate.py` te wijzigen.
- `tools/logboek.json`: per datum (`YYYY-MM-DD`) wat er gedaan is plus feedback. Dit is het bestand dat de dagelijkse update bijwerkt.

Na elke wijziging: `python3 tools/generate.py`, commit en push naar `main`.

## Logboek-formaat
```json
"2026-11-19": {
  "gedaan": [{"sport": "fietsen", "tekst": "62 min · 19,2 km/u · hartslag gem. 146"}],
  "oordeel": "goed | aandacht | gemist | advies",
  "feedback": "Korte coachfeedback in de je-vorm."
}
```
- `sport`: zwemmen, fietsen, lopen, kracht, of iets anders.
- `goed` = volgens plan / juiste intensiteit. `aandacht` = gedaan, maar te hard, te lang of op een rustdag. `gemist` = geplande training niet gedaan (geen `gedaan`-items). `advies` = advies voor de volgende dag op basis van readiness/HRV/hersteltijd (geen `gedaan`-items nodig). De avondupdate van die dag vervangt de advies-entry door de gewone entry (goed/aandacht/gemist).
- Eén entry per datum. Bestaat de datum al, vul dan aan (niet dubbel).

## Trainingen aanpassen
De coach (Claude) mag en moet het schema bijsturen als de data daarom vraagt. Kleine of tijdelijke aanpassingen gaan via `tools/aanpassingen.json`. Die vervangen de sessies van één dag volledig:
```json
"2026-11-24": {
  "reden": "Korte uitleg in de je-vorm, zichtbaar op de site",
  "sessies": [
    {"sport": "fietsen", "title": "Tacx rustig", "min": 45, "detail": "45 min rustig, cadans 85–95.", "zone": "Z1–Z2", "key": false},
    {"ref": "krachtA", "fase": "basis1", "soort": "herstel"},
    {"ref": "rust", "detail": "Volledige rust."}
  ]
}
```
`ref` kan `krachtA`, `krachtB` of `rust` zijn (`fase`: reset/basis1/basis2/opbouw/specifiek/taper, `soort`: opbouw/herstel).

Wanneer aanpassen (richtlijnen):
- Readiness < 25 of hersteltijd > 48 u op een ★-dag: ★-training van vandaag/morgen omzetten naar rustig of rust.
- 2+ keer achter elkaar te hard op rustige trainingen: komende rustige sessies korter maken en de hartslaggrens herhalen.
- Gemiste trainingen: niet inhalen. Bij 3+ gemiste trainingen in een week: de volgende week ~15% lichter maken.
- Signalen van overbelasting (meerdere dagen lage readiness/HRV onder baseline, pijn): volume verlagen of een herstelweek naar voren halen.
- Gaat het structureel makkelijker dan gepland (zones goed, readiness hoog): lichte verzwaring mag (max ~10% per week).
- Testresultaten (week 2, 9, 17): zones/tempo's in teksten, `CLAUDE.md` en `index.html` bijwerken.
- Structurele wijzigingen voor meerdere weken mogen in `tools/generate.py`, maar alleen met duidelijke reden in commit en samenvatting aan Yannick.
- De racedatum, de weekindeling (ma zwem+kracht, di fiets, wo lopen, do rust, vr zwem+kracht, za fiets, zo lopen) en het verleden (data vóór vandaag) niet wijzigen.

## Schrijfstijl
- Vraag de atleet nooit om iets door te sturen: alle data komt uit Garmin Moeder.
- Nederlands, spreek de atleet aan met **je**. Kort: 1–3 zinnen. Eerlijk maar bemoedigend.
- Noem concrete cijfers (afstand, tijd, tempo, gem. hartslag).
- Geen volledige naam, geen medische claims.

## Zones (hartslag)
| | Lopen | Fietsen |
|---|---|---|
| Z1 | < 135 | < 120 |
| Z2 | 135–150 | 120–140 |
| Z3 | 151–160 | 141–152 |
| Z4 | 161–172 | 153–166 |
| Z5 | > 172 | > 166 |

Zwemmen: rustig ≈ 3:00/100 m. Bij Garmin Training Readiness < 25 of hersteltijd > 48 u: ★-training vervangen door rustig of rust.

## Garmin
Alleen de connector **Garmin Moeder** (`garmin-moeder` tools) gebruiken. De connector **Garmin** (zonder "Moeder") is van iemand anders: nooit aanroepen.
