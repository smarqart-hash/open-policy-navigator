"""Fetch draft laws (Gesetzentwürfe) with full text from the DIP API of the Bundestag.

The API key is read only from the environment variable DIP_API_KEY and never
written anywhere. Network access is isolated in `DipClient.get_json`, so tests
can replace it with a fake.
"""

import json
import os
import time
import urllib.parse
import urllib.request
from collections.abc import Iterator

from keine_alternative.de.extract import EXTRACTOR_VERSION, extract_alternatives
from keine_alternative.records import sha256_text, utc_now

API_BASE = "https://search.dip.bundestag.de/api/v1"
PAUSE_SECONDS = 0.4  # be polite to the API between pages


class MissingApiKeyError(RuntimeError):
    pass


def api_key_from_env() -> str:
    key = os.environ.get("DIP_API_KEY", "").strip()
    if not key:
        raise MissingApiKeyError("Set DIP_API_KEY (see README); the key is never stored.")
    return key


class DipClient:
    def __init__(self, api_key: str, timeout: float = 90, pause: float = PAUSE_SECONDS):
        self._api_key = api_key
        self._timeout = timeout
        self._pause = pause

    def get_json(self, path: str, params: dict[str, str]) -> dict:
        url = f"{API_BASE}/{path}?{urllib.parse.urlencode(params)}"
        request = urllib.request.Request(url, headers={"Authorization": "ApiKey " + self._api_key})
        with urllib.request.urlopen(request, timeout=self._timeout) as response:
            return json.load(response)

    def iter_draft_laws(self, wahlperiode: str) -> Iterator[dict]:
        """Yield all Bundestag draft laws of one electoral period, page by page.

        The DIP API pages with a cursor; it signals the end by returning the
        same cursor again or an empty page.
        """
        cursor = None
        while True:
            params = {
                "f.drucksachetyp": "Gesetzentwurf",
                "f.wahlperiode": wahlperiode,
                "f.zuordnung": "BT",
                "format": "json",
            }
            if cursor:
                params["cursor"] = cursor
            page = self.get_json("drucksache-text", params)
            documents = page.get("documents", [])
            yield from documents
            if not documents or page.get("cursor") == cursor:
                return
            cursor = page["cursor"]
            time.sleep(self._pause)


def source_url(document: dict) -> str:
    """Prefer the public PDF link; fall back to the API record."""
    pdf_url = (document.get("fundstelle") or {}).get("pdf_url")
    return pdf_url or f"{API_BASE}/drucksache-text/{document.get('id')}"


def to_record(document: dict, wahlperiode: str, fetched_at: str) -> dict:
    """Turn one DIP document into one line of the jsonl data file.

    Only metadata and the extracted section are kept; the full text is
    represented by its SHA-256 (see DATA_SOURCES.md for what may be stored).
    """
    text = document.get("text") or ""
    return {
        "wp": wahlperiode,
        "dip_id": str(document.get("id")),
        "nr": document.get("dokumentnummer"),
        "datum": document.get("datum"),
        "titel": document.get("titel"),
        "urheber": ";".join(u.get("titel", "") for u in document.get("urheber", [])),
        "alt": extract_alternatives(text),
        "source_url": source_url(document),
        "fetched_at": fetched_at,
        "text_sha256": sha256_text(text),
        "extractor": EXTRACTOR_VERSION,
    }


def fetch_records(client: DipClient, wahlperioden: list[str]) -> Iterator[dict]:
    for wahlperiode in wahlperioden:
        for document in client.iter_draft_laws(wahlperiode):
            yield to_record(document, wahlperiode, utc_now())
