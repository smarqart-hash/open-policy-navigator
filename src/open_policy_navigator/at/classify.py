"""Sort Austrian bills by what their impact assessment says about alternatives.

The split between "only zero scenario" and "no alternative" is pattern based
and fuzzy (see README, limits). Whether a named alternative is a real policy
alternative was checked by hand: 2 of 184 full WFAs (the pattern finds 4).
"""

import re

SIMPLIFIED = "vereinfacht: kein Alternativen-Feld"
NOT_EXTRACTED = "voll: Abschnitt nicht extrahiert"
NO_ALTERNATIVE = "voll: keine Alternative"
ALTERNATIVE_NAMED = "voll: Alternative benannt/diskutiert"
ZERO_SCENARIO_ONLY = "voll: nur Nullszenario"

NO_ALTERNATIVE_PATTERN = re.compile(
    r"keine (sinnvolle[n]? |zweckmäßige[n]? |gleichwertige[n]? |realistische[n]? )?alternativ"
    r"|alternativen? (bestehen|gibt es) nicht"
    r"|alternativen?[^.]{0,80}nicht (bekannt|ersichtlich|gegeben|vorhanden)"
    r"|keine\.?$"
    r"|^keine"
)


def classify_bill(record: dict) -> str:
    """Return a category label. Records with a fetch problem keep their status."""
    if record["status"] != "ok":
        return record["status"][:30]
    if not record.get("full"):
        return SIMPLIFIED
    text = (record.get("alt") or "").lower()
    if not text:
        return NOT_EXTRACTED
    if NO_ALTERNATIVE_PATTERN.search(text):
        return NO_ALTERNATIVE
    if "alternativ" in text:
        return ALTERNATIVE_NAMED
    return ZERO_SCENARIO_ONLY
