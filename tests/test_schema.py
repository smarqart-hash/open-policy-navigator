import json
from pathlib import Path

import pytest
import yaml
from conftest import ROOT
from pydantic import ValidationError

from keine_alternative import schema

EXAMPLES = sorted((ROOT / "schema" / "examples").glob("*.yaml"))


def raw(name: str) -> dict:
    return yaml.safe_load((ROOT / "schema" / "examples" / name).read_text(encoding="utf-8"))


def demo() -> dict:
    return raw("beispiel-illustrativ.yaml")


@pytest.mark.parametrize("path", EXAMPLES, ids=[p.name for p in EXAMPLES])
def test_examples_validate(path: Path):
    schema.load_dossier(path)


def test_two_examples_exist():
    assert len(EXAMPLES) == 2


def test_exported_json_schema_is_up_to_date():
    # Regenerate with: python -m keine_alternative.schema
    committed = json.loads(schema.SCHEMA_FILE.read_text(encoding="utf-8"))
    assert committed == schema.json_schema()


def test_bill_quote_is_verbatim_alternatives_text():
    bill = schema.load_dossier(ROOT / "schema/examples/vorhaben-jstg-2026.yaml").bills[0]
    assert bill.locator.quote == bill.alternatives_text


# --- "missing data never appears as 'wirkt nicht'" ---------------------------


def cell(state, finding_ids=()):
    extra = {}
    if state == schema.CoverageState.GESUCHT_OHNE_BEFUND:
        extra = {"searched_at": "2026-11-20", "search_note": "searched"}
    return schema.CoverageCell(
        approach_id="ans_demo01",
        outcome="x",
        state=state,
        finding_ids=list(finding_ids),
        **extra,
    )


def finding(direction, finding_id="bef_x0001"):
    data = demo()["findings"][0] | {"id": finding_id, "direction": direction}
    return schema.Finding.model_validate(data)


@pytest.mark.parametrize(
    "state", [schema.CoverageState.NICHT_KURATIERT, schema.CoverageState.GESUCHT_OHNE_BEFUND]
)
def test_missing_data_never_appears_as_not_working(state):
    # Even if unrelated negative findings exist, a cell without findings is never "wirkt_nicht".
    unrelated = [finding(schema.Direction.KEINE_ODER_NEGATIV)]
    assert schema.effect_signal(cell(state), unrelated) != "wirkt_nicht"


def test_unsearched_is_open_and_searched_is_unmeasured():
    assert schema.effect_signal(cell(schema.CoverageState.NICHT_KURATIERT), []) == "offen"
    assert schema.effect_signal(cell(schema.CoverageState.GESUCHT_OHNE_BEFUND), []) == "ungemessen"


def test_not_estimable_findings_are_not_turned_into_not_working():
    f = finding(schema.Direction.NICHT_SCHAETZBAR)
    signal = schema.effect_signal(cell(schema.CoverageState.BEFUND, [f.id]), [f])
    assert signal == "nicht_schaetzbar"


def test_only_a_negative_finding_gives_not_working():
    f = finding(schema.Direction.KEINE_ODER_NEGATIV)
    assert schema.effect_signal(cell(schema.CoverageState.BEFUND, [f.id]), [f]) == "wirkt_nicht"


def test_positive_and_negative_findings_are_mixed():
    a = finding(schema.Direction.POSITIV, "bef_a0001")
    b = finding(schema.Direction.KEINE_ODER_NEGATIV, "bef_b0001")
    signal = schema.effect_signal(cell(schema.CoverageState.BEFUND, [a.id, b.id]), [a, b])
    assert signal == "gemischt"


def test_state_befund_requires_findings_and_vice_versa():
    with pytest.raises(ValidationError):
        cell(schema.CoverageState.BEFUND)
    with pytest.raises(ValidationError):
        cell(schema.CoverageState.NICHT_KURATIERT, ["bef_x0001"])


def test_searched_without_result_needs_date_and_note():
    with pytest.raises(ValidationError):
        schema.CoverageCell(approach_id="ans_demo01", outcome="x", state="gesucht_ohne_befund")


# --- envelope and entity rules ----------------------------------------------


def test_stopped_is_a_case_status_and_needs_a_reason():
    data = demo()["cases"][0]
    assert data["status"] == "gestoppt"
    with pytest.raises(ValidationError, match="status_reason"):
        schema.Case.model_validate(data | {"status_reason": None})


def test_finding_has_no_stopped_direction():
    with pytest.raises(ValidationError):
        finding("gestoppt")


def test_confirmed_statement_needs_reviewer():
    data = demo()["approaches"][0] | {"reviewed_by": None}
    with pytest.raises(ValidationError, match="reviewed_by"):
        schema.Approach.model_validate(data)


def test_approach_needs_at_least_one_instrument():
    with pytest.raises(ValidationError):
        schema.Approach.model_validate(demo()["approaches"][0] | {"instruments": []})


def test_instrument_category_follows_oecd_typology():
    with pytest.raises(ValidationError):
        schema.Instrument(category="nudge", instrument_type="Voreinstellung")


def test_unknown_fields_are_rejected():
    with pytest.raises(ValidationError):
        schema.Question(id="q_demo01", text="?", wirkt=True)


@pytest.mark.parametrize("bad_id", ["", "Q_1", "q-1", "q_ab", "keine alternative"])
def test_ids_are_opaque_tokens(bad_id):
    with pytest.raises(ValidationError):
        schema.Question(id=bad_id, text="?")


def test_dangling_reference_is_rejected():
    data = demo()
    data["positions"][0]["approach_id"] = "ans_missing"
    with pytest.raises(ValidationError, match="unknown approach id"):
        schema.Dossier.model_validate(data)


def test_duplicate_ids_are_rejected():
    data = demo()
    data["questions"].append(dict(data["questions"][0]))
    with pytest.raises(ValidationError, match="duplicate ids"):
        schema.Dossier.model_validate(data)
