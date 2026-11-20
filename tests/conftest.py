import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
DE_DATA = ROOT / "zaehlung" / "de" / "dip-gesetzentwuerfe.jsonl"
AT_DATA = ROOT / "zaehlung" / "at" / "at-vorblaetter.jsonl"


def load_fixture(name: str) -> list[dict]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))
