# Roadmap-Issues (Entwurf, noch nicht angelegt)

Entwurf für GitHub-Issues. Anlegen erst nach Freigabe durch Stefan.

## 1. Goldstandard ausbauen: 100 Entwürfe, 70 doppelt kodiert

Goldset v0 (36 Entwürfe) abschließen: Stefan bestätigt oder korrigiert die
Vorschläge. Danach auf 100 Entwürfe ausbauen, davon 70 unabhängig doppelt
kodiert (`coding_2`). Übereinstimmung als Krippendorff-α je Kategorie mit
Konfidenzintervall, Ziel ≥ 0,800 (Krippendorff 2004); das Eval-Skript rechnet
bisher nur Cohen-κ. Ziel-Trefferquote der Erkennung 95 %, mit öffentlichem
Fehlerbericht. **Fertig:** `section_recall` berechnet, α berichtet, Schwellen per
`--update` angehoben.

## 2. Extraktor de-v1: lange Abschnitte und Fundort

Muster v0 findet Abschnitte über 700 Zeichen nicht (alle 949 Treffer ≤ 688 Zeichen,
vermutlich eine Hauptursache der 87 Fehlenden). Grenze bis zur Überschrift „D.“
statt fester Länge, Suchfenster prüfen. Benötigt einen Neuabruf mit `DIP_API_KEY`
und lokalem Volltext-Archiv. **Fertig:** Neuabruf mit Provenienzfeldern,
Eval-Ratchet nicht schlechter, Zahlen im README mit Abweichungen erklärt.

## 3. Zitatprüfung in der CI

Für jede Aussage prüfen, ob `locator.quote` wörtlich im archivierten Quelltext
steht, dessen SHA-256 an der Quelle hängt (ADR 0005). Klären, wo das Archiv liegt
und was öffentlich sein darf (`DATA_SOURCES.md`).

## 4. Klassifikator v1 nach Kodierregel B

Die Regel v0 liest nur das erste Wort. Nach Kodierregel B (20.11.2026) zählt
„Keine.“ mit einer verworfenen konkreten Alternative als „Alternativen benannt“;
„Zu den vorliegenden Änderungen … bestehen keine Alternativen.“ ist ein bloßes
„Keine“ (Fixtures 20/9648, 20/3712, 20/4225, 20/12605, 20/12719). Regeln erweitern,
nur mit Goldset-Beleg; danach die Quote über alle gefundenen Abschnitte neu rechnen.

## 5. Österreich: Goldset und Trennung Nullszenario/keine Alternative

AT-Goldset analog zu DE; die 4 Treffer „Alternative benannt“ (davon 2 echt) als
Startfälle. „alternativlos“ (2204 d.B.) korrekt einordnen; abgeschnittene
Fallback-Extraktion (446 d.B.) prüfen.

## 6. Lokaler MCP-Server, nur lesend

Server nach `contracts/mcp/` auf einem abgeleiteten Release-Stand (ADR 0001,
0003). Golden-Tests als Abnahme; `abstained` bei fehlender Abdeckung.

## 7. Erste kuratierte Frage mit Gegenpositionen

Eine Frage mit 2–3 Lösungsansätzen, Fällen aus DE/AT und mindestens einer
Gegenposition je Ansatz; Review durch zwei Personen verschiedener Richtung.

## 8. Prüfstufen und Datenschichten im Schema

Der Antrag sagt vier Prüfstufen zu: automatisch erfasst → maschinell vorgeprüft
(Schema, Zitat wörtlich im archivierten Quelltext, Konsistenz, Dubletten) →
menschlich geprüft (Deckungsfrage je Fakt) → im Audit bestätigt (Zufallsstichprobe,
Fehlerquote mit Konfidenzintervall). `review_status` kennt bisher nur `proposed`,
`confirmed` und `rejected`. Vorschlag: `machine_checked` und `audited` ergänzen.
Dazu ein Feld `layer` in der Provenienz-Hülle für die drei Datenschichten
(`parsed`, `imported`, `curated`), damit die Herkunft sichtbar ist. Außerdem Modell
und Prompt-Version für `extraction_method: llm` (ADR 0005).

## 9. Importer für eine offene Instrumentendatenbank (Monat 4)

Einen Importer für eine offene Instrumentendatenbank schreiben, etwa die European
Sufficiency Policy Database (CSV). Importierte Einträge tragen `layer: imported`
und `review_status: proposed`. Zuerst die Lizenz in `DATA_SOURCES.md` klären.

## 10. Länder-Adapter, Mehrsprachigkeit, EU-Folgenabschätzungen

DE und AT als austauschbare Adapter mit gemeinsamer Schnittstelle. Schema-Texte
mehrsprachig anlegen. EU-Folgenabschätzungen als nächste Quelle (Second Stage).

## 11. Statisches Portal (WCAG 2.2 AA)

Ein statisches Portal aus dem abgeleiteten Release-Stand (ADR 0001), barrierefrei
nach WCAG 2.2 AA. Der MCP-Server bleibt lokal und folgt dem festen Antwortvertrag
(ADR 0003).
