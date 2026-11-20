"""Fetch government bills and their Vorblatt PDF from the Austrian Parliament.

Data: Parlament Österreich, Open Data, CC BY 4.0. PDFs are converted with
`pdftotext` (Poppler) in a temporary file and deleted right after.
Network access is isolated in `get`, so tests can pass a fake.
"""

import http.client
import json
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterator
from pathlib import Path

from open_policy_navigator.at.extract import EXTRACTOR_VERSION, read_wfa
from open_policy_navigator.records import sha256_text, utc_now

BASE = "https://www.parlament.gv.at"
HEADERS = {
    "User-Agent": "open-policy-navigator research script",
    "Content-Type": "application/json",
}
PAUSE_SECONDS = 0.3
LIST_ENDPOINT = "/Filter/api/filter/data/101?js=eval&showAll=true"

# Column positions in the filter API rows (as observed in November 2026).
COL_DATE, COL_TITLE, COL_NUMBER, COL_HISTORY = 4, 6, 7, 14

# Problems we expect from the network or from a changed page structure. Anything
# else is a bug and should stop the run instead of being written as a status.
FETCH_ERRORS = (
    urllib.error.URLError,
    http.client.HTTPException,  # e.g. IncompleteRead, RemoteDisconnected
    ConnectionError,
    TimeoutError,
    json.JSONDecodeError,
    KeyError,
    subprocess.CalledProcessError,
)

Getter = Callable[[str, bytes | None], bytes]


def http_get(url: str, data: bytes | None = None) -> bytes:
    request = urllib.request.Request(url, data=data, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


def pdf_to_text(pdf: bytes) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "vorblatt.pdf"
        path.write_bytes(pdf)
        result = subprocess.run(
            ["pdftotext", "-enc", "UTF-8", str(path), "-"], capture_output=True, check=True
        )
    return result.stdout.decode("utf-8", "replace")


def list_government_bills(get: Getter, gp: str) -> list[list]:
    query = {"NRBR": ["NR"], "GP_CODE": [gp], "VHG": ["RV"]}
    return json.loads(get(BASE + LIST_ENDPOINT, json.dumps(query).encode()))["rows"]


def find_vorblatt_pdf(get: Getter, history_path: str) -> str | None:
    """Return the link to the Vorblatt PDF on a bill's history page, if any."""
    content = json.loads(get(BASE + history_path + "?json=true", None))["content"]
    for group in content.get("documents") or []:
        if "Vorblatt" not in group.get("title", ""):
            continue
        for document in group["documents"]:
            if document["type"] == "PDF":
                return document["link"]
    return None


def read_bill(get: Getter, record: dict, to_text: Callable[[bytes], str] = pdf_to_text) -> dict:
    """Add WFA fields, provenance and a status to a bill record (returns a new dict)."""
    record = dict(record)
    try:
        link = find_vorblatt_pdf(get, record["his"])
        if link is None:
            record["status"] = "kein Vorblatt-Dokument"
            return record
        text = to_text(get(BASE + link, None))
    except FETCH_ERRORS as error:
        record["status"] = "fehler: " + str(error)[:80]
        return record
    reading = read_wfa(text)
    record.update(
        full=reading.full,
        simplified=reading.simplified,
        alt=reading.alt,
        alt_src=reading.alt_src,
        alt_any=reading.alt_any,
        source_url=BASE + link,
        fetched_at=utc_now(),
        text_sha256=sha256_text(text),
        extractor=EXTRACTOR_VERSION,
        status="ok",
    )
    return record


def fetch_records(get: Getter, periods: list[str], pause: float = PAUSE_SECONDS) -> Iterator[dict]:
    for gp in periods:
        for row in list_government_bills(get, gp):
            base = {
                "gp": gp,
                "nr": row[COL_NUMBER],
                "datum": row[COL_DATE],
                "titel": row[COL_TITLE],
                "his": row[COL_HISTORY],
            }
            yield read_bill(get, base)
            time.sleep(pause)


def needs_refetch(record: dict) -> bool:
    """Full WFA but no field text: try again (the fallback pattern may find it)."""
    return record.get("status") == "ok" and bool(record.get("full")) and not record.get("alt")


def refetch(get: Getter, records: list[dict], pause: float = PAUSE_SECONDS) -> Iterator[dict]:
    """Yield all records; those that need it are fetched and read again.

    If the second attempt fails, the original record is kept unchanged, so a
    refetch never turns an "ok" record into an error.
    """
    for record in records:
        if not needs_refetch(record):
            yield record
            continue
        again = read_bill(get, record)
        yield again if again["status"] == "ok" else record
        time.sleep(pause)
