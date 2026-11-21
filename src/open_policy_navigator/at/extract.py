"""Read the cover sheet (Vorblatt) and impact assessment (WFA) of an Austrian bill.

A full WFA has a field "Nullszenario und allfällige Alternativen". A simplified
WFA ("Vereinfachte wirkungsorientierte Folgenabschätzung") has no such field.

Two patterns, both from the first count (November 2026):
- primary: text after the field heading, up to the next heading-like line,
- fallback: used for full WFAs where the primary pattern found nothing; takes
  up to 900 characters after the first "Nullszenario" and cuts at the next
  known heading. The fallback result is limited to 600 characters.
"""

import re
from dataclasses import dataclass

EXTRACTOR_VERSION = "at-v0"

FULL_WFA_MARKER = "Nullszenario"
SIMPLIFIED_WFA_MARKER = "Vereinfachte wirkungsorientierte"

PRIMARY_PATTERN = re.compile(
    r"Nullszenario und allfällige Alternativen\s*(.{0,600}?)"
    r"(?:\n\s*\n[A-ZÄÖÜ][^\n]{0,60}\n|Vorhandene Studien|Interne Evaluierung|Ziele\b)",
    re.S,
)
FALLBACK_WINDOW = 900
FALLBACK_MAX_CHARS = 600
FALLBACK_HEADING = re.compile(r"^Nullszenario\s*(und allfällige Alternativen)?\s*")
FALLBACK_STOP = re.compile(
    r"(Vorhandene Studien|Interne Evaluierung|Beitrag zu Wirkungsziel|Ziele Ziel 1)"
)


@dataclass(frozen=True)
class WfaReading:
    full: bool  # has the Nullszenario field
    simplified: bool
    alt: str | None  # extracted field text
    alt_src: str | None  # "primary", "fallback" or None
    alt_any: int  # how often "alternativ" occurs anywhere in the document


def normalise_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_primary(text: str) -> str | None:
    match = PRIMARY_PATTERN.search(text)
    return normalise_whitespace(match.group(1)) if match else None


def extract_fallback(text: str) -> str | None:
    start = text.find(FULL_WFA_MARKER)
    if start < 0:
        return None
    segment = normalise_whitespace(text[start : start + FALLBACK_WINDOW])
    segment = FALLBACK_HEADING.sub("", segment)
    segment = FALLBACK_STOP.split(segment)[0].strip()
    return segment[:FALLBACK_MAX_CHARS]


def read_wfa(text: str) -> WfaReading:
    full = FULL_WFA_MARKER in text
    alt, source = extract_primary(text), "primary"
    if full and not alt:
        alt, source = extract_fallback(text), "fallback"
    return WfaReading(
        full=full,
        simplified=SIMPLIFIED_WFA_MARKER in text,
        alt=alt,
        alt_src=source if alt else None,
        alt_any=len(re.findall(r"[Aa]lternativ", text)),
    )
