import json

import pytest
from conftest import DE_DATA, ROOT

from keine_alternative import evaluation
from keine_alternative.records import read_jsonl
from keine_alternative.stats import cohen_kappa, wilson_interval


def test_wilson_reference_value():
    # 8 of 10: Wilson 95 % interval is about [0.490, 0.943]
    low, high = wilson_interval(8, 10)
    assert low == pytest.approx(0.4902, abs=1e-4)
    assert high == pytest.approx(0.9433, abs=1e-4)


def test_wilson_all_successes_stays_below_one_at_lower_end():
    low, high = wilson_interval(16, 16)
    assert high == 1.0 and 0.80 < low < 0.81


def test_kappa_reference_value():
    # Classic 2x2 example: observed 0.7, expected 0.5 -> kappa 0.4
    a = ["y"] * 20 + ["y"] * 5 + ["n"] * 10 + ["n"] * 15
    b = ["y"] * 20 + ["n"] * 5 + ["y"] * 10 + ["n"] * 15
    assert cohen_kappa(a, b) == pytest.approx(0.4)


def test_kappa_undefined_cases():
    assert cohen_kappa([], []) is None
    assert cohen_kappa(["Keine", "Keine"], ["Keine", "Keine"]) is None


def coding(present, alt=None, category=None):
    return {
        "section_present": present,
        "gold_alt": alt,
        "category": category,
        "coder": "test",
        "confirmed": True,
    }


def test_recall_is_weighted_by_stratum_size():
    # 100 found by the rule, 100 missed; half of the sampled misses have a section.
    goldset = {
        "population": {"found_v0": 100, "not_found_v0": 100},
        "items": [
            {"nr": "f1", "stratum": "found_v0", "coding_1": coding(True), "coding_2": None},
            {"nr": "m1", "stratum": "not_found_v0", "coding_1": coding(True), "coding_2": None},
            {"nr": "m2", "stratum": "not_found_v0", "coding_1": coding(False), "coding_2": None},
        ],
    }
    data = {"f1": {"alt": "Keine."}, "m1": {"alt": None}, "m2": {"alt": None}}
    metric = evaluation.section_recall(goldset, data)
    # found 100 of (100 + 100 * 0.5) drafts with a section
    assert metric.value == pytest.approx(100 / 150)
    assert metric.low < metric.value < metric.high


def test_recall_pending_without_annotated_misses():
    goldset = {
        "population": {"found_v0": 1, "not_found_v0": 1},
        "items": [{"nr": "m", "stratum": "not_found_v0", "coding_1": None, "coding_2": None}],
    }
    assert evaluation.section_recall(goldset, {"m": {"alt": None}}).value is None


def test_ratchet_only_goes_up():
    metrics = {name: evaluation.Metric(name, 0.5, 0.4, 0.6, 10) for name in evaluation.METRICS}
    new = evaluation.raised(metrics, {"extraction_precision": 0.9, "classification_accuracy": None})
    assert new["extraction_precision"] == 0.9
    assert new["classification_accuracy"] == 0.5


def test_check_fails_when_metric_drops_or_disappears():
    metrics = {
        "extraction_precision": evaluation.Metric("extraction_precision", 0.8, 0, 1, 5),
        "section_recall": evaluation.Metric("section_recall", None, None, None, 0),
    }
    thresholds = {"extraction_precision": 0.9, "section_recall": 0.95}
    assert evaluation.failures(metrics, thresholds) == ["extraction_precision", "section_recall"]


def test_committed_data_meets_committed_thresholds():
    goldset = json.loads((ROOT / "eval" / "goldset_v0.json").read_text(encoding="utf-8"))
    thresholds = json.loads((ROOT / "eval" / "thresholds.json").read_text(encoding="utf-8"))
    metrics = evaluation.evaluate(evaluation.confirmed_only(goldset), read_jsonl(DE_DATA))
    assert evaluation.failures(metrics, thresholds) == []


def test_proposals_do_not_count_for_the_ratchet():
    item = {"nr": "x", "stratum": "found_v0", "coding_2": None}
    proposal = item | {"coding_1": coding(True, "Keine.", "Keine") | {"confirmed": False}}
    confirmed = item | {"coding_1": coding(True, "Keine.", "Keine")}
    goldset = {"items": [proposal, confirmed]}
    assert evaluation.confirmed_only(goldset)["items"] == [confirmed]


def test_ratchet_never_rounds_up():
    metrics = {n: evaluation.Metric(n, 0.99996, 0, 1, 9) for n in evaluation.METRICS}
    assert evaluation.raised(metrics, {})["extraction_precision"] == 0.9999


def test_goldset_shape():
    goldset = json.loads((ROOT / "eval" / "goldset_v0.json").read_text(encoding="utf-8"))
    items = goldset["items"]
    assert 30 <= len(items) <= 40
    assert sum(i["stratum"] == "not_found_v0" for i in items) == 20
    assert all("coding_2" in i for i in items)  # prepared for double coding
    assert any(i["nr"] == "21/8283" for i in items)
