"""Evaluate a German data file against the hand-annotated gold set (eval ratchet).

    python -m keine_alternative.evaluation            # print metrics
    python -m keine_alternative.evaluation --check    # exit 1 if a metric fell below threshold
    python -m keine_alternative.evaluation --update   # raise thresholds to current values

Metrics (government drafts only):

- extraction_precision: of the sections the data file has, how many match the
  gold section text exactly (after whitespace normalisation).
- classification_accuracy: how often the rule category equals the gold category.
- section_recall: share of drafts that really have section C which the data file
  finds. The gold set over-samples drafts that v0 did not find (20 of 87, against
  16 of 532 found), so the per-stratum rates are weighted by stratum size.

Only coding_1 is used for the metrics; coding_2 is for inter-coder agreement.
Labels with "confirmed": false are proposals (e.g. by a language model). They are
shown for information only; the ratchet (--check, --update) uses confirmed labels.
"""

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from keine_alternative.de.classify import classify_section
from keine_alternative.de.extract import normalise_whitespace
from keine_alternative.records import read_jsonl
from keine_alternative.stats import cohen_kappa, wilson_interval

ROOT = Path(__file__).resolve().parents[2]
GOLDSET = ROOT / "eval" / "goldset_v0.json"
THRESHOLDS = ROOT / "eval" / "thresholds.json"
DATA = ROOT / "zaehlung" / "de" / "dip-gesetzentwuerfe.jsonl"
METRICS = ("extraction_precision", "classification_accuracy", "section_recall")


@dataclass(frozen=True)
class Metric:
    name: str
    value: float | None  # None = not computable yet (missing annotations)
    low: float | None
    high: float | None
    n: int

    def line(self) -> str:
        if self.value is None:
            return f"{self.name:24} pending (n={self.n})"
        return (
            f"{self.name:24} {self.value:.3f}  95% CI [{self.low:.3f}, {self.high:.3f}]  n={self.n}"
        )


def proportion(name: str, outcomes: list[bool]) -> Metric:
    if not outcomes:
        return Metric(name, None, None, None, 0)
    low, high = wilson_interval(sum(outcomes), len(outcomes))
    return Metric(name, sum(outcomes) / len(outcomes), low, high, len(outcomes))


def labelled(items: list[dict]) -> list[dict]:
    """Items whose first coding has been filled in (by Stefan or as a proposal)."""
    return [i for i in items if i["coding_1"] and i["coding_1"]["coder"]]


def extraction_precision(items: list[dict], data: dict[str, dict]) -> Metric:
    outcomes = [
        normalise_whitespace(data[i["nr"]]["alt"])
        == normalise_whitespace(i["coding_1"]["gold_alt"])
        for i in labelled(items)
        if data[i["nr"]]["alt"] is not None and i["coding_1"]["gold_alt"] is not None
    ]
    return proportion("extraction_precision", outcomes)


def classification_accuracy(items: list[dict], data: dict[str, dict]) -> Metric:
    outcomes = [
        classify_section(data[i["nr"]]["alt"]) == i["coding_1"]["category"]
        for i in labelled(items)
        if data[i["nr"]]["alt"] is not None and i["coding_1"]["category"] is not None
    ]
    return proportion("classification_accuracy", outcomes)


def section_recall(goldset: dict, data: dict[str, dict]) -> Metric:
    """Stratified recall: sum over strata of N_s * present_s * found_s / sum of N_s * present_s.

    present_s: share of annotated drafts in stratum s that have section C.
    found_s: share of those that the data file finds.
    The interval is an approximation: it varies only present_s of the not-found
    stratum over its Wilson interval and ignores sampling error in the other
    rates, so it is narrower than a full interval.
    """
    sizes = {"found_v0": goldset["population"]["found_v0"]}
    sizes["not_found_v0"] = goldset["population"]["not_found_v0"]
    strata = {}
    for stratum in sizes:
        annotated = [
            i
            for i in labelled(goldset["items"])
            if i["stratum"] == stratum and i["coding_1"]["section_present"] is not None
        ]
        present = [i for i in annotated if i["coding_1"]["section_present"]]
        found = [i for i in present if data[i["nr"]]["alt"] is not None]
        strata[stratum] = (len(annotated), len(present), len(found))
    n_total = sum(s[0] for s in strata.values())
    if any(s[0] == 0 for s in strata.values()):
        return Metric("section_recall", None, None, None, n_total)

    def recall(present_rate_missed: float) -> float:
        weighted_present = weighted_found = 0.0
        for stratum, (annotated, present, found) in strata.items():
            present_rate = present_rate_missed if stratum == "not_found_v0" else present / annotated
            found_rate = found / present if present else 0.0
            weighted_present += sizes[stratum] * present_rate
            weighted_found += sizes[stratum] * present_rate * found_rate
        return weighted_found / weighted_present if weighted_present else 0.0

    annotated_m, present_m, _ = strata["not_found_v0"]
    low_rate, high_rate = wilson_interval(present_m, annotated_m)
    low, high = sorted((recall(low_rate), recall(high_rate)))
    return Metric("section_recall", recall(present_m / annotated_m), low, high, n_total)


def category_kappa(items: list[dict]) -> tuple[float | None, int]:
    pairs = [
        (i["coding_1"]["category"], i["coding_2"]["category"])
        for i in items
        if i["coding_1"]
        and i["coding_2"]
        and i["coding_1"]["category"]
        and i["coding_2"]["category"]
    ]
    return cohen_kappa([a for a, _ in pairs], [b for _, b in pairs]), len(pairs)


def confirmed_only(goldset: dict) -> dict:
    """The gold set without proposals: unconfirmed items count as not yet labelled."""
    items = [i for i in goldset["items"] if i["coding_1"] and i["coding_1"]["confirmed"]]
    return {**goldset, "items": items}


def evaluate(goldset: dict, records: list[dict]) -> dict[str, Metric]:
    data = {r["nr"]: r for r in records}
    items = goldset["items"]
    return {
        "extraction_precision": extraction_precision(items, data),
        "classification_accuracy": classification_accuracy(items, data),
        "section_recall": section_recall(goldset, data),
    }


def failures(metrics: dict[str, Metric], thresholds: dict[str, float | None]) -> list[str]:
    """Names of metrics below their threshold. A missing value with a set threshold fails too."""
    failed = []
    for name, threshold in thresholds.items():
        if threshold is None:
            continue
        value = metrics[name].value
        if value is None or value < threshold:
            failed.append(name)
    return failed


def raised(metrics: dict[str, Metric], thresholds: dict[str, float | None]) -> dict:
    """Ratchet: thresholds only go up, never down."""
    new = dict(thresholds)
    for name in METRICS:
        value = metrics[name].value
        current = new.get(name)
        if value is not None and (current is None or value > current):
            new[name] = math.floor(value * 10_000) / 10_000  # never round up
    return new


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m keine_alternative.evaluation")
    parser.add_argument("--data", type=Path, default=DATA)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--update", action="store_true")
    args = parser.parse_args(argv)

    goldset = json.loads(GOLDSET.read_text(encoding="utf-8"))
    thresholds = json.loads(THRESHOLDS.read_text(encoding="utf-8"))
    records = read_jsonl(args.data)
    metrics = evaluate(confirmed_only(goldset), records)
    with_proposals = evaluate(goldset, records)

    items = goldset["items"]
    confirmed = sum(1 for i in items if i["coding_1"] and i["coding_1"]["confirmed"])
    print(
        f"gold set {goldset['goldset']}: {len(items)} items, {len(labelled(items))} labelled, "
        f"{confirmed} confirmed by a human (the others are proposals)"
    )
    print("confirmed labels (used by the ratchet):")
    for metric in metrics.values():
        print("  " + metric.line(), f"(threshold {thresholds.get(metric.name)})")
    print("including proposals (information only):")
    for metric in with_proposals.values():
        print("  " + metric.line())
    kappa, pairs = category_kappa(items)
    print(f"{'category_kappa':24} {'pending' if kappa is None else f'{kappa:.3f}'} (pairs={pairs})")

    if args.update:
        THRESHOLDS.write_text(json.dumps(raised(metrics, thresholds), indent=2) + "\n")
        print("thresholds updated")
    if args.check:
        failed = failures(metrics, thresholds)
        if failed:
            print("FAILED (below threshold): " + ", ".join(failed))
            return 1
        print("ok: no metric below threshold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
