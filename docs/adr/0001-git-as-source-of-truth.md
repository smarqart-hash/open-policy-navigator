# ADR 0001: Git ist die Quelle der Wahrheit

Status: angenommen · Datum: 2026-11-20

## Kontext

Kuratierte Einträge (Frage, Lösungsansatz, Fall, Befund, Position) müssen
nachvollziehbar entstehen: Wer hat was wann geändert, wer hat es geprüft? Für
Abfragen (Vergleich, Graph, MCP-Server) braucht es zugleich schnelle Indizes.

## Entscheidung

- Kuratierte Daten liegen als YAML-Dateien im Repository, validiert gegen
  `schema/` (Pydantic, JSON Schema). Änderungen kommen per Pull Request.
- Jede Datenbank (SQLite, Graph, Suchindex) wird aus einem Git-Stand **abgeleitet**
  und trägt dessen Commit-Hash als Release-Kennung. Sie wird nie direkt beschrieben.
- Ein Release ist ein Tag; Antworten nennen den Release-Hash (siehe `contracts/mcp/`).

## Folgen

- Herkunft und Prüfung jeder Änderung stehen in der Git-Historie; Reviews sind
  öffentlich.
- Die abgeleitete Datenbank lässt sich jederzeit wegwerfen und neu bauen.
- Grenze: Git eignet sich für Tausende Einträge, nicht für Millionen. Rohdaten
  großer Abrufe (Volltexte) liegen nicht im Repository (siehe `DATA_SOURCES.md`).
