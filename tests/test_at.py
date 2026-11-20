import json
import urllib.error

import pytest
from conftest import load_fixture

from open_policy_navigator.at import parlament
from open_policy_navigator.at.classify import classify_bill
from open_policy_navigator.at.extract import read_wfa

CASES = load_fixture("at_sections.json")

FULL_WFA = """Vorblatt
Wirkungsorientierte Folgenabschätzung
Nullszenario und allfällige Alternativen
Ohne Anpassung entstehen dem Bund
weiterhin Kosten.

Vorhandene Studien/Basis zur Abschätzung
"""


@pytest.mark.parametrize("case", CASES, ids=[c["nr"] for c in CASES])
def test_classification_matches_pinned_v0_result(case):
    assert classify_bill(case) == case["expected_v0"]


def test_full_wfa_primary_pattern():
    reading = read_wfa(FULL_WFA)
    assert reading.full and not reading.simplified
    assert reading.alt == "Ohne Anpassung entstehen dem Bund weiterhin Kosten."
    assert reading.alt_src == "primary"


def test_full_wfa_fallback_when_heading_is_split():
    text = "Nullszenario\nund allfällige\nAlternativen Keine.\nInterne Evaluierung"
    reading = read_wfa(text)
    assert reading.alt_src == "fallback"
    assert reading.alt == "Keine."


def test_simplified_wfa_has_no_field():
    reading = read_wfa("Vereinfachte wirkungsorientierte Folgenabschätzung\nZiele")
    assert reading.simplified and not reading.full and reading.alt is None


def fake_get(pages: dict[str, bytes]):
    def get(url, data=None):
        if url not in pages:
            raise urllib.error.URLError("not found: " + url)
        return pages[url]

    return get


HISTORY = "/gegenstand/XXVIII/I/251"
HISTORY_JSON = json.dumps(
    {
        "content": {
            "documents": [
                {"title": "Vorblatt und WFA", "documents": [{"type": "PDF", "link": "/v.pdf"}]}
            ]
        }
    }
).encode()


def test_read_bill_adds_provenance():
    get = fake_get(
        {parlament.BASE + HISTORY + "?json=true": HISTORY_JSON, parlament.BASE + "/v.pdf": b"%PDF"}
    )
    record = parlament.read_bill(get, {"his": HISTORY}, to_text=lambda pdf: FULL_WFA)
    assert record["status"] == "ok"
    assert record["source_url"] == parlament.BASE + "/v.pdf"
    assert len(record["text_sha256"]) == 64
    assert record["extractor"] == "at-v0"


def test_network_error_becomes_status_not_crash():
    record = parlament.read_bill(fake_get({}), {"his": HISTORY}, to_text=lambda pdf: "")
    assert record["status"].startswith("fehler: ")


def test_unexpected_error_is_not_swallowed():
    def broken(pdf):
        raise ValueError("bug in our code")

    get = fake_get(
        {parlament.BASE + HISTORY + "?json=true": HISTORY_JSON, parlament.BASE + "/v.pdf": b""}
    )
    with pytest.raises(ValueError):
        parlament.read_bill(get, {"his": HISTORY}, to_text=broken)


def test_refetch_only_touches_full_wfa_without_text(monkeypatch):
    calls = []
    monkeypatch.setattr(parlament, "read_bill", lambda get, r: calls.append(r["nr"]) or r)
    records = [
        {"nr": "1", "status": "ok", "full": True, "alt": None},
        {"nr": "2", "status": "ok", "full": True, "alt": "Keine"},
        {"nr": "3", "status": "ok", "full": False, "alt": None},
    ]
    assert len(list(parlament.refetch(None, records, pause=0))) == 3
    assert calls == ["1"]


def test_failed_refetch_keeps_the_original_record():
    original = {"nr": "1", "his": HISTORY, "status": "ok", "full": True, "alt": None}
    assert list(parlament.refetch(fake_get({}), [original], pause=0)) == [original]
