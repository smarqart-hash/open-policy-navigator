"""Count categories per electoral period and originator (the README table)."""

from collections import Counter
from dataclasses import dataclass

from open_policy_navigator.de.classify import (
    NOT_FOUND,
    classify_section,
    has_eu_reference,
    is_none,
    originator_group,
)
from open_policy_navigator.records import dedupe_by

GROUPS = ("Bundesregierung", "Fraktionen", "Bundesrat")


@dataclass(frozen=True)
class NoneShare:
    """How many drafts have a section, and how many of those start with 'Keine'."""

    with_section: int
    none: int


@dataclass(frozen=True)
class DeReport:
    unique_drafts: int
    by_period_and_group: dict[tuple[str, str], Counter]
    government: NoneShare
    government_not_found: int
    government_total: int
    government_eu: NoneShare
    government_non_eu: NoneShare


def none_share(records: list[dict]) -> NoneShare:
    found = [r for r in records if r["alt"] is not None]
    return NoneShare(with_section=len(found), none=sum(is_none(r["alt"]) for r in found))


def build_report(records: list[dict]) -> DeReport:
    unique = list(dedupe_by(records, "nr"))
    table = {
        (wp, group): Counter(
            classify_section(r["alt"])
            for r in unique
            if r["wp"] == wp and originator_group(r["urheber"]) == group
        )
        for wp in sorted({r["wp"] for r in unique})
        for group in GROUPS
    }
    government = [r for r in unique if originator_group(r["urheber"]) == "Bundesregierung"]
    return DeReport(
        unique_drafts=len(unique),
        by_period_and_group=table,
        government=none_share(government),
        government_not_found=sum(classify_section(r["alt"]) == NOT_FOUND for r in government),
        government_total=len(government),
        government_eu=none_share([r for r in government if has_eu_reference(r["titel"])]),
        government_non_eu=none_share([r for r in government if not has_eu_reference(r["titel"])]),
    )


def format_report(report: DeReport) -> str:
    lines = [f"unique drafts: {report.unique_drafts}"]
    for (wp, group), counts in report.by_period_and_group.items():
        total = sum(counts.values())
        lines.append(f"WP{wp} {group:16} n={total:4} {dict(counts.most_common())}")
    g = report.government
    lines += [
        f"government with section: {g.with_section}, starting with 'Keine': {g.none}",
        f"government not found: {report.government_not_found} of {report.government_total}",
        f"government EU title: {report.government_eu}",
        f"government non-EU title: {report.government_non_eu}",
    ]
    return "\n".join(lines)
