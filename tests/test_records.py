import pytest

from keine_alternative.records import dedupe_by, read_jsonl, sha256_text, write_jsonl


def test_write_then_read_roundtrip(tmp_path):
    path = tmp_path / "out.jsonl"
    assert write_jsonl(path, [{"nr": "1", "alt": "Keine."}]) == 1
    assert read_jsonl(path) == [{"nr": "1", "alt": "Keine."}]


def test_write_never_overwrites(tmp_path):
    path = tmp_path / "out.jsonl"
    path.write_text("published data\n", encoding="utf-8")
    with pytest.raises(FileExistsError):
        write_jsonl(path, [{"nr": "1"}])
    assert path.read_text(encoding="utf-8") == "published data\n"


def test_sha256_matches_reference_value():
    # Standard test vector for SHA-256("abc")
    assert sha256_text("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert sha256_text("Keine.") != sha256_text("Keine")


def test_dedupe_keeps_last():
    rows = [{"nr": "1", "v": 1}, {"nr": "1", "v": 2}, {"nr": "2", "v": 3}]
    assert [r["v"] for r in dedupe_by(rows, "nr")] == [2, 3]
