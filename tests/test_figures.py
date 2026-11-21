"""Figures and the architecture page must follow from the data and the code."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from open_policy_navigator import figures

ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE = ROOT / "docs" / "architecture.md"
SVG = "{http://www.w3.org/2000/svg}"


def test_alternatives_numbers_match_published_counts():
    germany, austria = figures.alternatives_bars()
    assert germany.total == 619
    assert [s.value for s in germany.segments] == [326, 96, 110, 87]
    # Austria: share is based on the 184 full WFAs, as in the application text
    assert austria.total == 184
    assert [s.value for s in austria.segments] == [182, 2]
    assert "286" in (austria.note or "")


def test_coverage_numbers_match_demo():
    bars = figures.coverage_bars()
    assert [(b.segments[0].value, b.total) for b in bars] == [(6, 10), (1, 1), (3, 9), (1, 6)]
    assert sum(b.total for b in bars) == 26
    assert sum(b.segments[0].value for b in bars) == 11


def test_small_shares_never_read_as_zero():
    assert figures.share_text(2, 470) == "0,4 %"
    assert figures.share_text(2, 184) == "1 %"
    assert figures.share_text(326, 619) == "53 %"
    assert figures.share_text(0, 10) == "0 %"


@pytest.mark.parametrize("name", sorted(figures.BUILDERS))
def test_committed_svg_is_current(name):
    committed = (figures.FIGURES / name).read_text(encoding="utf-8")
    assert committed == figures.BUILDERS[name](), "run python -m open_policy_navigator.figures"


@pytest.mark.parametrize("name", sorted(figures.BUILDERS))
def test_svg_is_accessible(name):
    root = ET.fromstring(figures.BUILDERS[name]())
    assert root.get("role") == "img"
    title, desc = root.find(f"{SVG}title"), root.find(f"{SVG}desc")
    assert title is not None and title.text
    assert desc is not None and len(desc.text or "") > 80
    # explicit white background, so the figure also works in dark mode
    background = root.find(f"{SVG}rect")
    assert background is not None and background.get("fill") == "#ffffff"
    # every number shown as a bar is also written out as text
    texts = " ".join(t.text or "" for t in root.iter(f"{SVG}text"))
    assert re.search(r"\d+ von \d+|\d+ \(\d+(,\d)? %\)", texts)


def test_architecture_text_states_the_figure_numbers():
    """The prose next to the figures must not drift from the data."""
    text = ARCHITECTURE.read_text(encoding="utf-8")
    germany, austria = figures.alternatives_bars()
    for segment in germany.segments:
        assert str(segment.value) in text, segment.label
    assert f"Von {austria.total} vollen Folgenabschätzungen nennen 2" in text
    bars = figures.coverage_bars()
    pairs = ", ".join(f"{b.segments[0].value} von {b.total}" for b in bars)
    assert f"({pairs})" in text


def test_architecture_names_only_existing_files():
    """Backtick paths, image and link targets, and file names in built diagram nodes."""
    text = ARCHITECTURE.read_text(encoding="utf-8")
    missing = []
    for path in re.findall(r"`((?:src|eval|schema|contracts|tests|zaehlung|docs)/[^`*]+)`", text):
        if not (ROOT / path).exists():
            missing.append(path)
    for target in re.findall(r"\]\(([^)#:]+)\)", text):
        if not (ARCHITECTURE.parent / target).exists():
            missing.append(target)
    package = ROOT / "src" / "open_policy_navigator"
    for label in re.findall(r'\["([^"]+)"\]:::built', text):
        for name in re.findall(r"\b([a-z_]+(?:/[a-z_]+)?\.py)\b", label):
            if not (package / name).exists():
                missing.append(name)
    assert not missing, f"named but missing: {missing}"


def test_built_nodes_do_not_promise_planned_months():
    """A solid frame means built; a month belongs in a dashed node, unless it says 'ab Monat'."""
    text = ARCHITECTURE.read_text(encoding="utf-8")
    offenders = [
        label
        for label in re.findall(r'[\[{]"([^"]+)"[\]}]:::built', text)
        if re.search(r"Monat \d", label) and "ab Monat" not in label
    ]
    assert not offenders, offenders
