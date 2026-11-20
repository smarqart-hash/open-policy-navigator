"""Shared helpers for the jsonl data files: reading, safe writing and provenance.

Every record written by a fetch run carries where the text came from (source_url),
when it was fetched (fetched_at) and a fingerprint of the full text (text_sha256).
Older records from the first count (November 2026) do not have these fields; the
readers accept them anyway, so the published numbers stay reproducible.
"""

import hashlib
import json
from collections.abc import Iterable, Iterator
from datetime import UTC, datetime
from pathlib import Path


def sha256_text(text: str) -> str:
    """Hex SHA-256 of the UTF-8 encoded full text, so a later reader can check
    that an archived text is exactly the one the extraction was based on."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def utc_now() -> str:
    """Current time as ISO 8601 string in UTC, second precision."""
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def read_jsonl(path: Path) -> list[dict]:
    """Read one JSON object per line. Blank lines are skipped."""
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def write_jsonl(path: Path, records: Iterable[dict]) -> int:
    """Write records to a NEW file and return how many were written.

    Refuses to overwrite an existing file: a fetch run must never silently
    replace the data a published number is based on.
    """
    count = 0
    with path.open("x", encoding="utf-8") as fh:  # "x" fails if the file exists
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")
            fh.flush()  # keep partial results if a long run is interrupted
            count += 1
    return count


def dedupe_by(records: Iterable[dict], key: str) -> Iterator[dict]:
    """Keep the last record per key value (same behaviour as the first scripts)."""
    latest: dict[str, dict] = {}
    for record in records:
        latest[record[key]] = record
    yield from latest.values()
