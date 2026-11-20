import pytest

from keine_alternative.de import dip
from keine_alternative.records import sha256_text

DOCUMENT = {
    "id": 281234,
    "dokumentnummer": "21/8283",
    "datum": "2026-09-30",
    "titel": "Entwurf eines Jahressteuergesetzes 2026",
    "urheber": [{"titel": "Bundesregierung"}],
    "fundstelle": {"pdf_url": "https://dserver.bundestag.de/btd/21/082/2108283.pdf"},
    "text": "A. Problem\nB. Lösung\nC. Alternativen\nKeine.\nD. Haushalt",
}


class FakeClient(dip.DipClient):
    """Returns prepared pages instead of calling the API."""

    def __init__(self, pages):
        super().__init__(api_key="unused", pause=0)
        self.pages = list(pages)
        self.cursors_seen = []

    def get_json(self, path, params):
        self.cursors_seen.append(params.get("cursor"))
        return self.pages.pop(0)


def test_paging_stops_when_cursor_repeats():
    client = FakeClient(
        [
            {"documents": [{"id": 1}], "cursor": "a"},
            {"documents": [{"id": 2}], "cursor": "b"},
            {"documents": [{"id": 3}], "cursor": "b"},
        ]
    )
    assert [d["id"] for d in client.iter_draft_laws("21")] == [1, 2, 3]
    assert client.cursors_seen == [None, "a", "b"]


def test_record_carries_provenance():
    record = dip.to_record(DOCUMENT, "21", fetched_at="2026-11-20T10:00:00+00:00")
    assert record["dip_id"] == "281234"
    assert record["alt"] == "Keine."
    assert record["source_url"].endswith("2108283.pdf")
    assert record["fetched_at"] == "2026-11-20T10:00:00+00:00"
    assert record["text_sha256"] == sha256_text(DOCUMENT["text"])
    assert record["extractor"] == "de-v0"
    assert "text" not in record  # the full text is not stored in the data file


def test_source_url_falls_back_to_api_record():
    assert dip.source_url({"id": 7}).endswith("/drucksache-text/7")


def test_missing_api_key_is_an_error(monkeypatch):
    monkeypatch.delenv("DIP_API_KEY", raising=False)
    with pytest.raises(dip.MissingApiKeyError):
        dip.api_key_from_env()
