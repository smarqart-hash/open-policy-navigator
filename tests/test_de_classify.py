import pytest
from conftest import load_fixture

from open_policy_navigator.de.classify import (
    NONE_WITH_REASON,
    classify_section,
    has_eu_reference,
    originator_group,
)

CASES = load_fixture("de_sections.json")


@pytest.mark.parametrize("case", CASES, ids=[c["nr"] for c in CASES])
def test_classification_matches_pinned_v0_result(case):
    assert classify_section(case["alt"]) == case["expected_v0"]


def test_reference_to_table_counts_as_none_with_reason():
    # JStG 2026: alternatives were examined, but the cover sheet says "Keine."
    jstg = next(c for c in CASES if c["nr"] == "21/8283")
    assert jstg["alt"].startswith("Keine. Die im Einzelnen geprüften Alternativen")
    assert classify_section(jstg["alt"]) == NONE_WITH_REASON


def test_known_rule_misses_are_documented():
    misses = [c["nr"] for c in CASES if c["proposed_correct"] not in (None, c["expected_v0"])]
    assert misses == ["20/12605", "20/12719", "20/11310"]


@pytest.mark.parametrize(
    ("urheber", "group"),
    [
        ("Bundesregierung", "Bundesregierung"),
        ("Fraktion der CDU/CSU;Fraktion der SPD", "Fraktionen"),
        ("Gruppe Die Linke", "Fraktionen"),
        ("Bundesrat", "Bundesrat"),
        ("", "andere"),
    ],
)
def test_originator_group(urheber, group):
    assert originator_group(urheber) == group


def test_eu_reference_from_title_keywords():
    assert has_eu_reference("Gesetz zur Umsetzung der Richtlinie (EU) 2024/1")
    assert not has_eu_reference("Gesetz zur Stärkung der Pflegekompetenz")
    assert not has_eu_reference(None)
