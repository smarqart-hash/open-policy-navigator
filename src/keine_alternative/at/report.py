"""Count categories per legislative period (GP) for the Austrian bills."""

from collections import Counter
from dataclasses import dataclass

from keine_alternative.at.classify import classify_bill


@dataclass(frozen=True)
class AtReport:
    total: int
    by_period: dict[str, Counter]
    ok: int  # Vorblatt found and read
    full: int  # full WFA with a Nullszenario field
    simplified_without_field: int
    full_by_category: Counter


def build_report(records: list[dict]) -> AtReport:
    ok = [r for r in records if r["status"] == "ok"]
    full = [r for r in ok if r.get("full")]
    return AtReport(
        total=len(records),
        by_period={
            gp: Counter(classify_bill(r) for r in records if r["gp"] == gp)
            for gp in sorted({r["gp"] for r in records}, reverse=True)
        },
        ok=len(ok),
        full=len(full),
        simplified_without_field=len(ok) - len(full),
        full_by_category=Counter(classify_bill(r) for r in full),
    )


def format_report(report: AtReport) -> str:
    lines = [f"bills: {report.total}"]
    for gp, counts in report.by_period.items():
        lines.append(f"{gp} {sum(counts.values())} {dict(counts.most_common())}")
    lines += [
        f"with Vorblatt (ok): {report.ok}, full WFA: {report.full}, "
        f"simplified/no field: {report.simplified_without_field}",
        f"full WFA by category: {dict(report.full_by_category.most_common())}",
    ]
    return "\n".join(lines)
