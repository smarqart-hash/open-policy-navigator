# Mitmachen

Danke für das Interesse. Das Projekt ist im Aufbau; Rückmeldungen zu Daten,
Kategorien und Fehlklassifikationen sind besonders willkommen.

## Fehler in den Daten melden

Ein Issue mit Drucksachennummer (z. B. `21/8283` oder `251 d.B.`), dem Abschnitt,
wie er im Dokument steht, und der Kategorie, die du erwartest. Bestätigte Fälle
kommen ins Goldset (`eval/`) und bleiben damit dauerhaft getestet.

## Code

```bash
pip install -e ".[dev]"
ruff check . && ruff format --check .
pytest
python -m keine_alternative.evaluation --check
```

- Python 3.12, wenige Abhängigkeiten (pydantic, PyYAML; pytest und ruff für die
  Entwicklung). Neue Abhängigkeiten bitte vorher im Issue besprechen.
- Kleine, thematisch saubere Commits nach [Conventional Commits](https://www.conventionalcommits.org/).
- Verhalten ändern heißt Test ändern: Fixtures in `tests/fixtures/` halten das
  aktuelle Regelverhalten fest. Ein Parser-Umbau darf das Eval-Ratchet nicht
  verschlechtern (`eval/thresholds.json` steigt nur).
- Kein Sprachmodell in der Datenpipeline (ADR 0002). Keine Secrets committen.

## Kuratierte Einträge

Einträge folgen `schema/` (siehe `schema/README.md`). Jede Aussage braucht eine
Quelle und ein wörtliches Zitat. Eine Person prüft und bestätigt
(`review_status: confirmed`, `reviewed_by`). Gegenpositionen sind ausdrücklich
erwünscht.

## Lizenz

Beiträge zum Code stehen unter MIT, Beiträge zu Daten und Zuordnungen unter
CC BY 4.0.
