# Keine Alternative

Offene Bausteine, mit denen sich politische Lösungsansätze, Befunde und Gegenpositionen belegt erfassen und maschinell abfragen lassen. Ausgangspunkt ist eine Zählung: Wie oft nennen Gesetzentwürfe im Vorblatt eine Alternative? Dieses Repository enthält die ersten Zählskripte für den Deutschen Bundestag und den österreichischen Nationalrat, die Rohdaten der Zählung und deren Grenzen.

Status: Vorarbeit. Die Skripte erkennen den Abschnitt über ein einzelnes Textmuster. Ein belastbarer Parser, ein offenes Datenschema für Lösungsansatz, Fall, Befund und Position, ein Prüfablauf sowie API und MCP-Server sind geplant, aber noch nicht gebaut.

## Ergebnisse (Stand 12. November 2026)

**Deutschland.** Die Gemeinsame Geschäftsordnung der Bundesministerien sieht für Gesetzentwürfe der Bundesregierung ein Vorblatt mit dem Abschnitt „C. Alternativen“ vor (§ 42 Abs. 1 GGO mit Anlage 3). Ausgewertet wurden 1.083 Gesetzentwürfe der Wahlperioden 20 und 21 über die DIP-API.

| Urheber | Abschnitt erkannt | nur „Keine“ | „Keine“ mit Begründung | Alternative benannt |
|---|---|---|---|---|
| Bundesregierung WP 20 | 298 | 187 | 53 | 58 |
| Bundesregierung WP 21 | 234 | 139 | 43 | 52 |
| Fraktionen WP 20+21 | 328 | 220 | 31 | 77 |
| Bundesrat WP 20+21 | 89 | 55 | 4 | 30 |

Bei Entwürfen der Bundesregierung beginnt der Abschnitt in 422 von 532 erkannten Fällen mit „Keine“ (79 %). 87 von 619 Regierungsentwürfen wurden nicht erkannt.

**Österreich.** Ausgewertet wurden 496 Regierungsvorlagen des Nationalrats (XXVII. und XXVIII. GP), davon 470 mit Vorblatt und Wirkungsorientierter Folgenabschätzung (WFA). 286 haben eine vereinfachte WFA ohne eigenes Feld für Alternativen. Von 184 vollen WFA nennen 2 eine inhaltliche Alternative zur vorgeschlagenen Regelung (von Hand geprüft).

## Grenzen

- Gemessen wird, was im Vorblatt steht, nicht, ob ein Ministerium Alternativen geprüft hat.
- Deutschland: Einordnung per Muster („beginnt mit Keine“). Die 87 nicht erkannten Regierungsentwürfe sind nicht von Hand geprüft. EU-Bezug nur über Stichworte im Titel.
- Österreich: Die Trennung „nur Nullszenario“ und „keine Alternative“ ist musterbasiert und unscharf. Ausgewertet wurden die ersten rund 600 bis 900 Zeichen des Abschnitts.

## Reproduktion

Python 3 mit Standardbibliothek. Für Österreich zusätzlich `pdftotext` (Poppler).

```bash
# Deutschland: API-Schlüssel nur als Umgebungsvariable, nie im Code
cd zaehlung/de
DIP_API_KEY=... python -I count.py 20,21 dip-gesetzentwuerfe.jsonl
python -I -X utf8 analyze.py dip-gesetzentwuerfe.jsonl

# Österreich
cd zaehlung/at
python -I fetch.py XXVIII,XXVII <pdf-ordner> at-vorblaetter.jsonl
python -I refetch.py at-vorblaetter.jsonl <pdf-ordner>
python -I -X utf8 analyze.py at-vorblaetter.jsonl
```

Einen API-Schlüssel für DIP gibt es beim [Deutschen Bundestag](https://dip.bundestag.de/über-dip/hilfe/api).

## Lizenzen und Quellen

- Code: [MIT](LICENSE).
- Daten in `zaehlung/de/`: Quelle Deutscher Bundestag/Bundesrat – DIP. Die Datei enthält Auszüge (Titel, Urheber, Abschnitt „C. Alternativen“), keine vollständigen Drucksachen. Es gelten die [Nutzungsbedingungen des DIP](https://dip.bundestag.de/documents/nutzungsbedingungen_dip.pdf).
- Daten in `zaehlung/at/`: Quelle Parlament Österreich, [Open Data](https://www.parlament.gv.at/recherchieren/open-data/) unter CC BY 4.0. Auszüge aus Vorblatt und WFA.
- Eigene Zuordnungen und Zählungen: CC BY 4.0.
