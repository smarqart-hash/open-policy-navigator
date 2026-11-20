"""Sort extracted "C. Alternativen" sections into a few categories.

Rule-based on purpose: every decision can be traced to one line below.
The categories describe what the cover sheet says, not whether a ministry
actually examined alternatives.
"""

import re

NOT_FOUND = "kein Abschnitt gefunden"
NONE_ONLY = "Keine"
NONE_WITH_REASON = "Keine + Begründung"
STATUS_QUO = "Status quo genannt"
ALTERNATIVES = "Alternativen benannt/diskutiert"

# Sections that start with "Keine" and are shorter than this count as a bare "Keine."
BARE_NONE_MAX_CHARS = 25

# EU reference is only detected from keywords in the title (known limit).
EU_TITLE_PATTERN = re.compile(
    r"Richtlinie|Verordnung \(EU\)|Umsetzung|Durchführung der Verordnung|EU\)|Unionsrecht",
    re.I,
)


def originator_group(urheber: str) -> str:
    """Map the DIP 'urheber' string to one of four groups."""
    if "Bundesregierung" in urheber:
        return "Bundesregierung"
    if "Bundesrat" in urheber:
        return "Bundesrat"
    if "Fraktion" in urheber or "Gruppe" in urheber:
        return "Fraktionen"
    return "andere"


def classify_section(section: str | None) -> str:
    """Return one of the five category labels for an extracted section."""
    if section is None:
        return NOT_FOUND
    text = section.lower()
    if text.startswith("keine"):
        return NONE_ONLY if len(text) < BARE_NONE_MAX_CHARS else NONE_WITH_REASON
    if text.startswith("die ") and ("beibehaltung" in text or "rechtslage" in text):
        return STATUS_QUO
    return ALTERNATIVES


def is_none(section: str | None) -> bool:
    """True if the section starts with 'Keine' (with or without reason)."""
    return classify_section(section) in (NONE_ONLY, NONE_WITH_REASON)


def has_eu_reference(title: str | None) -> bool:
    return bool(EU_TITLE_PATTERN.search(title or ""))
