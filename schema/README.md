# Schema v0

Models: [`src/keine_alternative/schema.py`](../src/keine_alternative/schema.py) (Pydantic).
Exported JSON Schema: [`dossier-v0.schema.json`](dossier-v0.schema.json), regenerate with
`python -m keine_alternative.schema` (a test fails if it is out of date).

| Object | German | Key fields |
|---|---|---|
| `Question` | Frage | text, topic |
| `Bill` | Vorhaben | country, document number, DIP/AT id, alternatives text, links to questions and approaches |
| `Approach` | Lösungsansatz | question, 1..n instruments with OECD IFCMA 2024 category |
| `Case` | Fall | country, legal act, design (Ausgestaltung), status with reason; `gestoppt` is a status |
| `Finding` | Befund | outcome, direction and certainty (GRADE) separately, study design (Maryland 1–5), transferability |
| `Position` | Position | stance `stuetzt`/`lehnt_ab`, actor, date |
| `Source` | Quelle | own entity: kind, URL, licence, SHA-256 of the archived text |
| `CoverageCell` | Abdeckung | approach × outcome: `nicht_kuratiert`, `gesucht_ohne_befund`, `befund` |

Every statement carries the provenance envelope: `id` (opaque), `schema_version`,
`source_id`, `locator` (verbatim quote + position), `extraction_method`
(`rule`/`llm`/`human`), `extracted_at`, `review_status`, `reviewed_by`.

The signal shown to users is derived, never stored (`effect_signal`):
`ungemessen` only from `gesucht_ohne_befund`, an unsearched cell is `offen`, and
`wirkt_nicht` only from a finding with direction `keine_oder_negativ`.
See [ADR 0004](../docs/adr/0004-ids-and-coverage.md).

Examples: [`vorhaben-jstg-2026.yaml`](examples/vorhaben-jstg-2026.yaml) (real, as
the parser would create it) and [`beispiel-illustrativ.yaml`](examples/beispiel-illustrativ.yaml)
(invented content, shows every object).
