"""The numbers published in the README must follow from the stored data."""

from conftest import AT_DATA, DE_DATA

from keine_alternative.at.classify import ALTERNATIVE_NAMED
from keine_alternative.at.report import build_report as build_at_report
from keine_alternative.de.classify import ALTERNATIVES, NONE_ONLY, NONE_WITH_REASON, STATUS_QUO
from keine_alternative.de.report import build_report as build_de_report
from keine_alternative.records import read_jsonl


def test_germany_published_numbers():
    report = build_de_report(read_jsonl(DE_DATA))
    assert report.unique_drafts == 1083
    assert (report.government.with_section, report.government.none) == (532, 422)
    assert (report.government_not_found, report.government_total) == (87, 619)
    # "nur Keine": 187 (WP 20) + 139 (WP 21)
    bare = sum(
        report.by_period_and_group[(wp, "Bundesregierung")][NONE_ONLY] for wp in "20 21".split()
    )
    assert bare == 326


def test_germany_readme_table_row_wp20_government():
    counts = build_de_report(read_jsonl(DE_DATA)).by_period_and_group[("20", "Bundesregierung")]
    assert counts[NONE_ONLY] == 187
    assert counts[NONE_WITH_REASON] == 53
    # README column "Alternative benannt" = named alternatives + status quo
    assert counts[ALTERNATIVES] + counts[STATUS_QUO] == 58


def test_austria_published_numbers():
    report = build_at_report(read_jsonl(AT_DATA))
    assert report.total == 496
    assert report.ok == 470
    assert report.simplified_without_field == 286
    assert report.full == 184
    # The pattern finds 4; by hand 2 of them are real alternatives (see fixtures).
    assert report.full_by_category[ALTERNATIVE_NAMED] == 4
