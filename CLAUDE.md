# Trainingssite "Op weg naar Hoorn"

Statische GitHub Pages-site (branch `main`, root) met een 30-weken trainingsschema richting IRONMAN 70.3 Westfriesland (Hoorn, zo 20 juni 2027).

## Bestanden
- `index.html`: de site (vanilla HTML/JS, leest `data.js`).
- `data.js`: **gegenereerd**, niet met de hand aanpassen.
- `tools/generate.py`: het schema (weekopzet, sessies, kracht A/B). Schrijft `data.js`.
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
- `goed` = volgens plan / juiste intensiteit. `aandacht` = gedaan, maar te hard, te lang of op een rustdag. `gemist` = geplande training niet gedaan (geen `gedaan`-items). `advies` = alleen voor vandaag: advies op basis van readiness/HRV (geen `gedaan`-items nodig).
- Eén entry per datum. Bestaat de datum al, vul dan aan (niet dubbel).

## Schrijfstijl
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
