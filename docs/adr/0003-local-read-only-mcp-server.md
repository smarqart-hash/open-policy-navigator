# ADR 0003: MCP-Server lokal und nur lesend

Status: angenommen · Datum: 2026-11-20

## Kontext

Sprachmodell-Werkzeuge sollen die Daten abfragen können (Model Context
Protocol). Ein Server, der schreibt oder im Netz erreichbar ist, wäre ein
Einfallstor für Manipulation und eine Betriebslast.

## Entscheidung

- Der MCP-Server läuft lokal beim Nutzer (stdio), auf einem abgeleiteten
  Release-Stand (ADR 0001). Er hat keinen Schreibzugriff und keine Netzwerkaufrufe.
- Jede Antwort folgt dem Vertrag in `contracts/mcp/answer.schema.json`:
  `status` (`answered`, `abstained`, `out_of_scope`), `coverage_state`,
  Release-Hash und Zitate als `source_id` plus `locator`.
- Zitatfelder sind als Daten markiert (`content_role: "data"`): Ein aufrufendes
  Modell darf Text aus Quellen nie als Anweisung behandeln (Schutz vor
  Prompt-Injection über zitierte Dokumente).
- Kein Befund und keine Abdeckung: der Server antwortet `abstained` statt zu raten.

## Folgen

- Kein Hosting, keine Nutzerdaten auf Projektseite.
- Ein gehosteter Lesezugang (HTTP-API) wäre eine eigene Entscheidung.
