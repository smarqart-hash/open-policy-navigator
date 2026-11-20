"""Find section "C. Alternativen" in the text of a German draft law.

The GGO (§ 42 Abs. 1 with Anlage 3) prescribes a cover sheet (Vorblatt) with
sections A. Problem und Ziel, B. Lösung, C. Alternativen, D. Haushaltsausgaben ...

This is extractor version "v0", the exact pattern of the first count. It is kept
unchanged so the published numbers stay reproducible. Known limits:

- The section text may be at most 700 characters. A longer section followed by
  "D. " does not match at all and the draft counts as "no section found".
  All 949 matched sections in the November 2026 data are <= 688 characters,
  which supports this as one cause of the 87 unrecognised government drafts.
- Only the first 20,000 characters are searched.
"""

import re

EXTRACTOR_VERSION = "de-v0"

SEARCH_WINDOW = 20_000
MAX_SECTION_CHARS = 700

# "C. Alternative(n)", then the shortest text up to "D. " or the end of the window.
SECTION_PATTERN = re.compile(
    rf"C\.\s*Alternative[n]?\s*(.{{0,{MAX_SECTION_CHARS}}}?)\s*(?:D\.\s|$)",
    re.S,
)


def normalise_whitespace(text: str) -> str:
    """Collapse line breaks and runs of spaces into single spaces."""
    return re.sub(r"\s+", " ", text).strip()


def extract_alternatives(full_text: str) -> str | None:
    """Return the text of section C, or None if the section was not found."""
    match = SECTION_PATTERN.search(full_text[:SEARCH_WINDOW])
    if match is None:
        return None
    return normalise_whitespace(match.group(1))
