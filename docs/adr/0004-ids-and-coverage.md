# ADR 0004: Kennungen und Abdeckungssemantik

Status: angenommen · Datum: 2026-11-20

## Kontext

Einträge werden korrigiert, umbenannt und verlinkt. Und das Portal muss
zeigen, wo nichts bekannt ist, ohne dass Nichtwissen wie ein negatives Ergebnis
aussieht.

## Entscheidung

**Kennungen.** Jede Entität hat eine opake, stabile `id` aus Typ-Präfix und
Zeichenfolge (`ans_7Hk2pQ`, Muster im Schema). Die Kennung enthält keinen Inhalt,
damit eine korrigierte Überschrift nie einen Link bricht. Einmal vergebene
Kennungen werden nicht wiederverwendet. Externe Kennungen (DIP-ID, Drucksachen-
nummer, ELI, CELEX, DOI) sind Felder, nicht die Kennung selbst.

**Abdeckung.** Für jede Zelle Lösungsansatz × Ergebnis gibt es genau einen
`coverage_state`:

| Zustand | Bedeutung | angezeigtes Signal |
|---|---|---|
| `nicht_kuratiert` | Niemand hat gesucht | `offen` |
| `gesucht_ohne_befund` | Gesucht (Datum, Notiz), keine Evaluation gefunden | `ungemessen` |
| `befund` | Mindestens ein Befund verknüpft | aus Befunden abgeleitet |

- „ungemessen“ entsteht nur aus `gesucht_ohne_befund`.
- „wirkt nicht“ entsteht nur aus einem Befund mit Richtung `keine_oder_negativ`.
  Fehlende Daten erscheinen nie als „wirkt nicht“ (Test in `tests/test_schema.py`).
- „gestoppt“ ist ein Status am Fall, kein Befund.
- Das Signal wird abgeleitet, nie gespeichert (`effect_signal`).

## Folgen

- Eine leere Zelle ist ehrlich als Lücke sichtbar; das ist Teil des Produkts.
- Kurator:innen müssen eine Suche ohne Ergebnis aktiv eintragen.
