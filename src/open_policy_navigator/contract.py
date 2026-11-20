"""Answer contract of the (planned) local, read-only MCP server. See ADR 0003.

Every answer says whether it answers, abstains or is out of scope, which
release of the data it is based on, how well the question is covered, and
which sources support it. Quoted source text is marked as data so that a
calling model never treats it as an instruction.

    python -m open_policy_navigator.contract   -> rewrite contracts/mcp/answer.schema.json
"""

import json
from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from open_policy_navigator.schema import ID_PATTERN, CoverageState, Locator

CONTRACT_VERSION = "0.1"
SCHEMA_FILE = Path(__file__).resolve().parents[2] / "contracts" / "mcp" / "answer.schema.json"


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class AnswerStatus(StrEnum):
    ANSWERED = "answered"
    ABSTAINED = "abstained"  # in scope, but the data does not support an answer
    OUT_OF_SCOPE = "out_of_scope"  # not a question this data set covers


class Citation(Model):
    source_id: str = Field(pattern=ID_PATTERN)
    locator: Locator
    # Fixed marker: the quote is untrusted data from a document, never an instruction.
    content_role: Literal["data"] = "data"


class Answer(Model):
    contract_version: Literal["0.1"] = CONTRACT_VERSION
    status: AnswerStatus
    release: str = Field(pattern=r"^[0-9a-f]{40}$", description="Git commit of the data release")
    coverage_state: CoverageState | None = Field(
        default=None, description="Coverage of the cell the answer is about; None if out of scope"
    )
    summary: str | None = Field(default=None, description="Short answer, only if answered")
    citations: list[Citation] = []
    reason: str | None = Field(default=None, description="Why the server abstained / refused")

    @model_validator(mode="after")
    def status_rules(self):
        if self.status == AnswerStatus.ANSWERED:
            if not (self.summary and self.citations):
                raise ValueError("an answer needs a summary and at least one citation")
            if self.coverage_state != CoverageState.BEFUND:
                raise ValueError("only a cell with findings can be answered")
        else:
            if self.summary is not None:
                raise ValueError("no summary when abstaining or out of scope")
            if not self.reason:
                raise ValueError("abstaining or out of scope needs a reason")
        if self.status == AnswerStatus.OUT_OF_SCOPE and self.coverage_state is not None:
            raise ValueError("out of scope answers have no coverage_state")
        if self.status == AnswerStatus.ABSTAINED and self.coverage_state is None:
            raise ValueError("an abstention states the coverage_state it is based on")
        return self


def json_schema_text() -> str:
    return json.dumps(Answer.model_json_schema(), ensure_ascii=False, indent=2) + "\n"


if __name__ == "__main__":
    SCHEMA_FILE.write_text(json_schema_text(), encoding="utf-8", newline="\n")
    print(f"wrote {SCHEMA_FILE}")
