"""Build the figures in docs/figures/ from the stored data.

The counts come from the data files in zaehlung/. Two inputs are maintained by
hand and documented where they live: the Austrian hand check (2 of the 4 pattern
hits are real alternatives) and docs/figures/data/ki-arbeit-wirkungsmessung.json,
copied from the public demo. tests/test_figures.py recomputes the numbers and
checks the committed SVG files against a fresh build.

    python -X utf8 -m open_policy_navigator.figures          # write docs/figures/*.svg
    python -X utf8 -m open_policy_navigator.figures --check  # fail if a file is stale
"""

import argparse
import json
import sys
from dataclasses import dataclass
from html import escape
from pathlib import Path

from open_policy_navigator.at.classify import ALTERNATIVE_NAMED
from open_policy_navigator.at.report import build_report as build_at_report
from open_policy_navigator.de.classify import (
    ALTERNATIVES,
    NONE_ONLY,
    NONE_WITH_REASON,
    STATUS_QUO,
)
from open_policy_navigator.de.report import build_report as build_de_report
from open_policy_navigator.records import read_jsonl

ROOT = Path(__file__).resolve().parents[2]
DE_DATA = ROOT / "zaehlung" / "de" / "dip-gesetzentwuerfe.jsonl"
AT_DATA = ROOT / "zaehlung" / "at" / "at-vorblaetter.jsonl"
FIGURES = ROOT / "docs" / "figures"
COVERAGE_DATA = FIGURES / "data" / "ki-arbeit-wirkungsmessung.json"

# Austria: the pattern finds 4 named alternatives in full WFAs; a hand check of
# all four found 2 real ones (see at/classify.py and tests/test_reproduction.py).
AT_REAL_ALTERNATIVES_BY_HAND = 2

# Colours: orange family = "no alternative", teal = real alternative (checked by
# hand), slate = "starts differently" (not the same as naming an alternative),
# grey = no data. Every segment is also named in text, so colour is never the
# only cue.
NONE_DARK = "#b9461b"
NONE_LIGHT = "#f4b183"
NAMED = "#0f766e"
OTHER_START = "#5b6b8c"
NO_DATA = "#c8c8c8"
MEASURED = "#0f766e"
NOT_MEASURED = "#d9d9d9"
INK = "#1f1f1f"
MUTED = "#555555"


@dataclass(frozen=True)
class Segment:
    label: str
    value: int
    colour: str


@dataclass(frozen=True)
class Bar:
    label: str
    segments: tuple[Segment, ...]
    note: str | None = None

    @property
    def total(self) -> int:
        return sum(s.value for s in self.segments)


def alternatives_bars() -> tuple[Bar, Bar]:
    """Section C in German government drafts and the Austrian WFA, from the data."""
    de = build_de_report(read_jsonl(DE_DATA))
    counts = {NONE_ONLY: 0, NONE_WITH_REASON: 0, ALTERNATIVES: 0, STATUS_QUO: 0}
    for (_, group), counter in de.by_period_and_group.items():
        if group == "Bundesregierung":
            for key in counts:
                counts[key] += counter[key]
    germany = Bar(
        "Deutschland: Regierungsentwürfe, Wahlperioden 20 und 21",
        (
            Segment("nur „Keine“", counts[NONE_ONLY], NONE_DARK),
            Segment("„Keine“ mit Begründung", counts[NONE_WITH_REASON], NONE_LIGHT),
            Segment(
                "beginnt nicht mit „Keine“",
                counts[ALTERNATIVES] + counts[STATUS_QUO],
                OTHER_START,
            ),
            Segment("Abschnitt vom Muster nicht erkannt", de.government_not_found, NO_DATA),
        ),
    )
    at = build_at_report(read_jsonl(AT_DATA))
    pattern_named = at.full_by_category[ALTERNATIVE_NAMED]
    if pattern_named < AT_REAL_ALTERNATIVES_BY_HAND:
        raise ValueError("hand-checked alternatives exceed the pattern result")
    austria = Bar(
        "Österreich: volle Folgenabschätzungen, XXVII. und XXVIII. GP",
        (
            Segment("keine echte Alternative", at.full - AT_REAL_ALTERNATIVES_BY_HAND, NONE_DARK),
            Segment("echte Alternative (von Hand geprüft)", AT_REAL_ALTERNATIVES_BY_HAND, NAMED),
        ),
        note=(
            f"Weitere {at.simplified_without_field} Vorlagen haben eine vereinfachte "
            "Folgenabschätzung ohne Feld für Alternativen."
        ),
    )
    return germany, austria


def coverage_bars() -> tuple[Bar, ...]:
    """Cases with an impact measurement per sub-question (demo topic AI and work)."""
    data = json.loads(COVERAGE_DATA.read_text(encoding="utf-8"))
    bars = []
    for row in data["teilfragen"]:
        if not 0 <= row["mit_messung"] <= row["faelle"]:
            raise ValueError(f"inconsistent row: {row}")
        bars.append(
            Bar(
                row["frage"],
                (
                    Segment("mit Wirkungsmessung", row["mit_messung"], MEASURED),
                    Segment(
                        "ohne Wirkungsmessung", row["faelle"] - row["mit_messung"], NOT_MEASURED
                    ),
                ),
            )
        )
    return tuple(bars)


# --- SVG ----------------------------------------------------------------------

WIDTH = 760
LEFT = 24
BAR_WIDTH = WIDTH - 2 * LEFT
MIN_SEGMENT = 3  # px, so that 2 of 470 stays visible


def _text(x: float, y: float, content: str, size: int = 14, **attrs: str) -> str:
    extra = "".join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}"{extra}>{escape(content)}</text>'


def _segment_widths(bar: Bar, scale_total: int) -> list[float]:
    raw = [BAR_WIDTH * s.value / scale_total for s in bar.segments]
    widths = [
        max(w, MIN_SEGMENT) if s.value else 0.0 for w, s in zip(raw, bar.segments, strict=True)
    ]
    excess = sum(widths) - BAR_WIDTH * bar.total / scale_total
    widest = widths.index(max(widths))
    widths[widest] -= excess
    return widths


def _svg(title: str, desc: str, body: list[str], height: float, source: str) -> str:
    source_lines = source.split("\n")
    height += 16 * (len(source_lines) - 1)
    footer = [
        _text(LEFT, height - 16 - 16 * (len(source_lines) - 1 - i), line, 12, fill=MUTED)
        for i, line in enumerate(source_lines)
    ]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height:.0f}" '
        f'viewBox="0 0 {WIDTH} {height:.0f}" role="img" '
        'aria-labelledby="title desc" font-family="system-ui, -apple-system, '
        "'Segoe UI', Roboto, Arial, sans-serif\">",
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">{escape(desc)}</desc>',
        f'<rect width="{WIDTH}" height="{height:.0f}" fill="#ffffff"/>',
        _text(LEFT, 34, title, 19, font_weight="600", fill=INK),
        *body,
        *footer,
        "</svg>",
    ]
    return "\n".join(lines) + "\n"


def share_text(value: int, total: int) -> str:
    """Percent in German notation; small shares keep one decimal so they never read as 0 %."""
    share = 100 * value / total if total else 0.0
    if 0 < share < 1:
        return f"{share:.1f} %".replace(".", ",")
    return f"{round(share)} %"


def _bar_block(bar: Bar, y: float, scale_total: int) -> tuple[list[str], float]:
    out = [_text(LEFT, y, f"{bar.label} (n = {bar.total})", 15, font_weight="600", fill=INK)]
    y += 10
    x = float(LEFT)
    for segment, width in zip(bar.segments, _segment_widths(bar, scale_total), strict=True):
        if width:
            out.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="30" '
                f'fill="{segment.colour}" stroke="#ffffff" stroke-width="1"/>'
            )
        x += width
    # thin frame so that light segments stay distinguishable from the background
    out.append(
        f'<rect x="{LEFT}" y="{y:.1f}" width="{x - LEFT:.1f}" height="30" fill="none" '
        f'stroke="{MUTED}" stroke-width="1"/>'
    )
    y += 30 + 24
    for segment in bar.segments:
        out.append(
            f'<rect x="{LEFT}" y="{y - 11:.1f}" width="12" height="12" '
            f'fill="{segment.colour}" stroke="{MUTED}" stroke-width="0.5"/>'
        )
        out.append(
            _text(
                LEFT + 20,
                y,
                f"{segment.label}: {segment.value} ({share_text(segment.value, bar.total)})",
                14,
                fill=INK,
            )
        )
        y += 22
    if bar.note:
        out.append(_text(LEFT, y + 2, bar.note, 13, fill=MUTED))
        y += 24
    return out, y + 18


def alternatives_svg() -> str:
    germany, austria = alternatives_bars()
    body: list[str] = [
        _text(
            LEFT,
            58,
            "Was steht unter „C. Alternativen“ im Vorblatt? Gezählt, was öffentlich steht.",
            14,
            fill=MUTED,
        )
    ]
    y = 96.0
    for bar in (germany, austria):
        block, y = _bar_block(bar, y, bar.total)
        body += block
    bare = germany.segments[0].value
    desc = (
        f"Gestapelte Balken. Deutschland, {germany.total} Regierungsentwürfe: "
        + ", ".join(f"{s.label} {s.value}" for s in germany.segments)
        + f". Österreich, {austria.total} volle Folgenabschätzungen: "
        + ", ".join(f"{s.label} {s.value}" for s in austria.segments)
        + f". {austria.note} Bei {bare} von {germany.total} deutschen Entwürfen steht nur "
        "das Wort Keine."
    )
    source = (
        "Quelle: Deutscher Bundestag/Bundesrat – DIP; Parlament Österreich, Open Data. "
        "Stand 12.11.2026.\n"
        "Eigene Zählung: DE mit Muster de-v0, AT mit Muster at-v0, AT-Treffer von Hand geprüft."
    )
    return _svg("Alternativen im Vorblatt: meist „Keine“", desc, body, y + 20, source)


def coverage_svg() -> str:
    bars = coverage_bars()
    data = json.loads(COVERAGE_DATA.read_text(encoding="utf-8"))
    cases = sum(b.total for b in bars)
    measured = sum(b.segments[0].value for b in bars)
    body = [
        _text(
            LEFT,
            58,
            f"Demo-Thema „KI und Arbeit“: {cases} Fälle, "
            f"zu {measured} gibt es eine Wirkungsmessung.",
            14,
            fill=MUTED,
        )
    ]
    widest = max(b.total for b in bars)
    y = 96.0
    for bar in bars:
        body.append(_text(LEFT, y, bar.label, 15, font_weight="600", fill=INK))
        y += 10
        x = float(LEFT)
        for i in range(bar.total):
            colour = MEASURED if i < bar.segments[0].value else NOT_MEASURED
            body.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="22" height="22" rx="3" fill="{colour}" '
                f'stroke="{MUTED if colour == NOT_MEASURED else colour}" stroke-width="1"/>'
            )
            x += 27
        body.append(
            _text(
                LEFT + 27 * widest + 8,
                y + 16,
                f"{bar.segments[0].value} von {bar.total} mit Messung",
                14,
                fill=INK,
            )
        )
        y += 22 + 30
    body.append(f'<rect x="{LEFT}" y="{y - 11:.1f}" width="12" height="12" fill="{MEASURED}"/>')
    body.append(
        _text(
            LEFT + 20,
            y,
            "Fall mit Wirkungsmessung (Vergleich, gleich welches Ergebnis)",
            14,
            fill=INK,
        )
    )
    y += 22
    body.append(
        f'<rect x="{LEFT}" y="{y - 11:.1f}" width="12" height="12" '
        f'fill="{NOT_MEASURED}" stroke="{MUTED}" stroke-width="1"/>'
    )
    body.append(_text(LEFT + 20, y, "Fall ohne Wirkungsmessung", 14, fill=INK))
    y += 30
    desc = (
        "Ein Kästchen je Fall, je Teilfrage eine Zeile. "
        + "; ".join(f"{b.label}: {b.segments[0].value} von {b.total} mit Messung" for b in bars)
        + f". Zusammen {measured} von {cases}."
    )
    source = (
        "Ein Fall ist eine Maßnahme, die ein Staat, eine Region oder eine Stadt eingeführt, "
        "erprobt oder vorgeschlagen hat.\n"
        f"Quelle: {data['quelle']}, Stand {data['stand']}."
    )
    return _svg("Wo Wirkung gemessen wurde und wo nicht", desc, body, y + 20, source)


BUILDERS = {
    "alternativen-vorblatt.svg": alternatives_svg,
    "ki-arbeit-wirkungsmessung.svg": coverage_svg,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the figures in docs/figures/ from the stored data."
    )
    parser.add_argument("--check", action="store_true", help="fail if a figure is stale")
    args = parser.parse_args(argv)
    stale = []
    for name, build in BUILDERS.items():
        path = FIGURES / name
        svg = build()
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != svg:
                stale.append(name)
        else:
            path.write_text(svg, encoding="utf-8", newline="\n")
            print(f"wrote {path.relative_to(ROOT)}")
    if stale:
        print("stale figures (run without --check): " + ", ".join(stale), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
