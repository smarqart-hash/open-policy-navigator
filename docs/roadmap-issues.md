# Roadmap-Issues (Entwurf, noch nicht angelegt)

Entwurf für GitHub-Issues. Anlegen erst nach Freigabe durch Stefan.

## 1. Goldset v0 annotieren und doppelt kodieren

Die 20 nicht erkannten Regierungsentwürfe in `eval/goldset_v0.json` am PDF prüfen
(`section_present`, `gold_alt`, `category`), die 16 Vorschläge bestätigen oder
korrigieren. Danach eine zweite Person unabhängig kodieren lassen (`coding_2`), Ziel etwa
70 doppelt kodierte Entwürfe (ADR 0005). **Fertig:** `section_recall` berechnet,
Krippendorff-α für `category` mit Konfidenzintervall berichtet (Ziel ≥ 0,800),
Schwellen per `--update` angehoben.

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
