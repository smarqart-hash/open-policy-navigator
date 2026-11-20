# Datenquellen und Lizenzen

Stand: 20. November 2026. Rechtliche Einordnungen sind sorgfältig recherchiert,
aber keine Rechtsberatung; offene Punkte sind markiert.

| Quelle | Zugang | Lizenz / Bedingungen | Was im Repository liegt |
|---|---|---|---|
| **Deutscher Bundestag/Bundesrat – DIP** | DIP-API (`search.dip.bundestag.de`), Schlüssel nötig | [Nutzungsbedingungen des DIP](https://dip.bundestag.de/documents/nutzungsbedingungen_dip.pdf); Quellenangabe „Deutscher Bundestag/Bundesrat – DIP“. Drucksachen gelten verbreitet als amtliche Werke (§ 5 UrhG); im Einzelfall nicht geprüft | Metadaten (Nummer, Datum, Titel, Urheber), der Abschnitt „C. Alternativen“, DIP-Kennung, Quell-URL, Abrufzeit, SHA-256 des Volltexts |
| **Parlament Österreich – Open Data** | Filter-API und Vorblatt-PDFs auf `parlament.gv.at` | [CC BY 4.0](https://www.parlament.gv.at/recherchieren/open-data/), Namensnennung „Parlament Österreich“ | Metadaten, WFA-Merkmale, das Feld „Nullszenario und allfällige Alternativen“, Quell-URL, Abrufzeit, SHA-256 |
| **Studien und Evaluationen** | per DOI oder Verlagsseite, kein automatischer Abruf | meist urheberrechtlich geschützt; Open-Access-Texte je nach Lizenz (oft CC BY) | Bibliografische Angaben, DOI, kurze wörtliche Zitate als Beleg (Zitatrecht, § 51 UrhG). Keine Volltexte |
| **Stellungnahmen, Presse** | Webseite der Organisation | urheberrechtlich geschützt | Akteur, Datum, URL, kurzes wörtliches Zitat |
| **OECD IFCMA-Typologie 2024** | OECD-Bericht, doi:10.1787/68529f35-en | CC BY 4.0 | Nur die fünf Kategorienamen im Schema |
| **Eigene Zuordnungen, Zählungen, Goldset** | dieses Repository | CC BY 4.0 | alles unter `zaehlung/`, `eval/`, `schema/examples/` |

## Was nicht gespeichert wird

- **Volltexte** von Drucksachen und PDFs: Sie werden beim Abruf gelesen, nur ihr
  SHA-256 wird festgehalten. Ein lokales Archiv (`cache/`, per `.gitignore`
  ausgeschlossen) dient der Zitatprüfung. Ob Drucksachen-Volltexte öffentlich
  archiviert werden dürfen, ist offen (Roadmap).
- **API-Schlüssel**: nur aus der Umgebungsvariable `DIP_API_KEY`, nie in Dateien.
- **Personenbezogene Daten** über Urheberangaben (Fraktion, Ministerium) und
  öffentlich auftretende Akteure hinaus.

## Herkunft je Datensatz

Neu abgerufene Datensätze tragen `source_url`, `fetched_at`, `text_sha256` und
die Extraktor-Version. Die Datensätze der ersten Zählung (November 2026) haben
diese Felder noch nicht; sie werden beim nächsten Abruf ergänzt.
