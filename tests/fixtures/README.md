# Test fixtures

`de_sections.json` (18 cases) and `at_sections.json` (8 cases) are copied verbatim
from the stored data in `zaehlung/` (Deutscher Bundestag – DIP; Parlament
Österreich, CC BY 4.0). They cover every category, the reference case of the
Jahressteuergesetz 2026 (BT-Drs. 21/8283, BR-Drs. 447/26) and known rule misses.

Fields:

- `expected_v0`: what the current rules (extractor/classifier v0) return. The tests
  pin this, so any change in behaviour is visible.
- `proposed_correct`: where a careful reader would sort the case differently, the
  category a reader would choose. **Proposed by Claude from the stored text, to be
  confirmed by Stefan.** `null` means the v0 result is considered correct.
- `note`: why the case is in the set.

The fixtures contain only the extracted section, not the full Drucksache. The
extraction tests therefore embed the section in a minimal Vorblatt frame
(see `tests/test_de_extract.py`).
