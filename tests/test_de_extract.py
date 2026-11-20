import pytest
from conftest import load_fixture

from keine_alternative.de.extract import MAX_SECTION_CHARS, extract_alternatives

CASES = [c for c in load_fixture("de_sections.json") if c["alt"] is not None]


def vorblatt(section: str) -> str:
    """Minimal cover sheet frame as in Anlage 3 GGO, with line breaks like in DIP texts."""
    return (
        "Gesetzentwurf\nder Bundesregierung\n"
        "A. Problem und Ziel\nEs gibt ein Problem.\n"
        "B. Lösung\nDieses Gesetz.\n"
        f"C. Alternativen\n{section}\n"
        "D. Haushaltsausgaben ohne Erfüllungsaufwand\nKeine.\n"
    )


@pytest.mark.parametrize("case", CASES, ids=[c["nr"] for c in CASES])
def test_extracts_section_text_from_frame(case):
    assert extract_alternatives(vorblatt(case["alt"])) == case["alt"]


def test_line_breaks_inside_section_are_normalised():
    assert extract_alternatives(vorblatt("Keine.\nDie Lage\n  ist klar.")) == (
        "Keine. Die Lage ist klar."
    )


def test_singular_heading_is_recognised():
    text = "C. Alternative\nKeine.\nD. Haushaltsausgaben"
    assert extract_alternatives(text) == "Keine."


def test_missing_section_returns_none():
    assert extract_alternatives("A. Problem und Ziel\nB. Lösung\nD. Haushalt") is None


def test_known_limit_long_section_is_not_found():
    # Pins the documented v0 limit: a section longer than 700 characters is missed.
    long_section = "Eine Alternative wäre ... " * (MAX_SECTION_CHARS // 20)
    assert len(long_section) > MAX_SECTION_CHARS
    assert extract_alternatives(vorblatt(long_section)) is None


def test_known_limit_section_after_search_window_is_not_found():
    assert extract_alternatives("x" * 20_000 + vorblatt("Keine.")) is None
