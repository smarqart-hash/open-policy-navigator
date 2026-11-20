"""Golden tests for the MCP answer contract (contracts/mcp/)."""

import json
from pathlib import Path

import pytest
from conftest import ROOT
from pydantic import ValidationError

from keine_alternative import contract

GOLDEN = ROOT / "contracts" / "mcp" / "golden"
VALID = sorted((GOLDEN / "valid").glob("*.json"))
INVALID = sorted((GOLDEN / "invalid").glob("*.json"))


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", VALID, ids=[p.stem for p in VALID])
def test_valid_golden_answers_round_trip(path):
    answer = contract.Answer.model_validate(load(path))
    # Serialising again gives exactly the golden file: the contract is stable.
    assert json.loads(answer.model_dump_json()) == load(path)


@pytest.mark.parametrize("path", INVALID, ids=[p.stem for p in INVALID])
def test_invalid_golden_answers_are_rejected(path):
    with pytest.raises(ValidationError):
        contract.Answer.model_validate(load(path))


def test_every_status_has_a_golden_example():
    statuses = {load(p)["status"] for p in VALID}
    assert statuses == {s.value for s in contract.AnswerStatus}


def test_exported_contract_schema_is_up_to_date():
    # Regenerate with: python -m keine_alternative.contract
    assert load(contract.SCHEMA_FILE) == contract.Answer.model_json_schema()


def test_quotes_are_marked_as_data_in_the_schema():
    citation = contract.Answer.model_json_schema()["$defs"]["Citation"]
    assert citation["properties"]["content_role"]["const"] == "data"
