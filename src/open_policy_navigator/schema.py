"""Data schema v0 for curated entries (Pydantic; exported as JSON Schema).

Objects and how they relate:

    Question (Frage) ──< Approach (Lösungsansatz, 1..n instruments, OECD categories)
                             ├──< Case (Fall: country, legal act, design, status)
                             ├──< Finding (Befund: direction and certainty kept apart)
                             ├──< Position (supports / opposes, actor, date)
                             └──< CoverageCell (approach × outcome: was it searched?)
    Bill (Vorhaben: one concrete draft law) links a parliament record to questions/approaches.
    Source (Quelle) is an entity of its own; every statement points to one.

Every statement (Approach, Bill, Case, Finding, Position) sits in the same
provenance envelope (`Statement`): opaque id, schema version, source, verbatim
locator, how it was extracted, and whether a human reviewed it.

Enum values are German because they are the vocabulary shown to users;
field names are English like the rest of the code.
"""

import json
from datetime import date
from enum import StrEnum
from pathlib import Path
from typing import Literal

import yaml
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

SCHEMA_VERSION = "0.1"

# Opaque, stable ids: a short type prefix plus a random/sequential part.
# The id never encodes content, so correcting a title never changes the id.
ID_PATTERN = r"^[a-z]{1,8}_[0-9A-Za-z]{4,32}$"


class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


# --- provenance envelope ------------------------------------------------------


class ExtractionMethod(StrEnum):
    RULE = "rule"  # deterministic parser (e.g. Vorblatt extractor)
    LLM = "llm"  # language model: only ever a proposal, see ADR 0002
    HUMAN = "human"


class ReviewStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


class Locator(Model):
    """Where exactly the statement is found in the source."""

    quote: str = Field(min_length=1, description="Verbatim quote from the archived source text")
    position: str = Field(
        min_length=1, description="Page, section or paragraph, e.g. 'Vorblatt, C.'"
    )


class Statement(Model):
    id: str = Field(pattern=ID_PATTERN)
    schema_version: Literal["0.1"] = SCHEMA_VERSION
    source_id: str = Field(pattern=ID_PATTERN)
    locator: Locator
    extraction_method: ExtractionMethod
    extracted_at: AwareDatetime  # with time zone, e.g. +00:00
    review_status: ReviewStatus = ReviewStatus.PENDING
    reviewed_by: str | None = None

    @model_validator(mode="after")
    def review_needs_a_reviewer(self):
        if self.review_status != ReviewStatus.PENDING and not self.reviewed_by:
            raise ValueError("a confirmed or rejected statement needs reviewed_by")
        return self


# --- entities -----------------------------------------------------------------


class SourceKind(StrEnum):
    DRUCKSACHE = "drucksache"
    GESETZ = "gesetz"
    STUDIE = "studie"
    STELLUNGNAHME = "stellungnahme"
    PRESSE = "presse"
    SONSTIGE = "sonstige"


class Source(Model):
    """A document that statements point to. Stored once, referenced by id."""

    id: str = Field(pattern=ID_PATTERN)
    kind: SourceKind
    title: str
    url: str
    license: str = Field(description="e.g. 'CC BY 4.0', 'amtliches Werk (§ 5 UrhG)', 'nur Zitat'")
    retrieved_at: AwareDatetime | None = None
    archived_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    doi: str | None = None


class Question(Model):
    id: str = Field(pattern=ID_PATTERN)
    schema_version: Literal["0.1"] = SCHEMA_VERSION
    text: str = Field(min_length=1)
    topic: str | None = None


class InstrumentCategory(StrEnum):
    """Five categories of the OECD IFCMA typology (2024)."""

    OEKONOMISCH = "oekonomisch"
    REGULATORISCH = "regulatorisch"
    INVESTITION = "investition"  # government investment and consumption
    INFORMATION = "information"
    FREIWILLIG = "freiwillig"


class Instrument(Model):
    category: InstrumentCategory
    instrument_type: str = Field(min_length=1, description="e.g. 'Steuer', 'Subvention', 'Gebot'")


class Approach(Statement):
    question_id: str = Field(pattern=ID_PATTERN)
    title: str
    description: str | None = None
    instruments: list[Instrument] = Field(min_length=1)  # packages: several instruments


class Country(StrEnum):
    DE = "DE"
    AT = "AT"


class Bill(Statement):
    """A concrete draft law; created by the parser with extraction_method 'rule'."""

    country: Country
    parliament_id: str | None = Field(
        default=None, description="DIP Vorgang id (DE) or history path (AT), if known"
    )
    document_number: str = Field(description="e.g. '21/8283' or '251 d.B.'")
    title: str
    question_ids: list[str] = []
    approach_ids: list[str] = []
    alternatives_text: str | None = Field(
        default=None, description="Section 'C. Alternativen' / WFA field, None if not found"
    )


class CaseStatus(StrEnum):
    VORGESCHLAGEN = "vorgeschlagen"
    BESCHLOSSEN = "beschlossen"
    IN_KRAFT = "in_kraft"
    GEAENDERT = "geaendert"
    AUFGEHOBEN = "aufgehoben"
    NICHT_BESCHLOSSEN = "nicht_beschlossen"
    GESTOPPT = "gestoppt"  # a status of the case, never a finding


class ReasonField(StrEnum):
    """McConnell's three fields: why something was stopped or failed."""

    PROZESS = "prozess"
    PROGRAMM = "programm"
    POLITIK = "politik"


class StatusReason(Model):
    field: ReasonField
    text: str = Field(min_length=1)


class LegalAct(Model):
    title: str
    identifier: str | None = Field(default=None, description="ELI, CELEX or DIP id")
    article: str | None = None


class Case(Statement):
    """One country's use of an approach."""

    approach_id: str = Field(pattern=ID_PATTERN)
    country: str = Field(pattern=r"^[A-Z]{2}$", description="ISO 3166-1 alpha-2")
    legal_act: LegalAct
    design: str | None = Field(default=None, description="Ausgestaltung, e.g. amount or scope")
    status: CaseStatus
    status_reason: StatusReason | None = None
    start: date | None = None
    end: date | None = None

    @model_validator(mode="after")
    def stopped_needs_reason(self):
        ends = (CaseStatus.GESTOPPT, CaseStatus.AUFGEHOBEN, CaseStatus.NICHT_BESCHLOSSEN)
        if self.status in ends and self.status_reason is None:
            raise ValueError(f"status '{self.status}' needs a status_reason")
        return self


class Direction(StrEnum):
    POSITIV = "positiv"
    KEINE_ODER_NEGATIV = "keine_oder_negativ"
    GEMISCHT = "gemischt"
    NICHT_SCHAETZBAR = "nicht_schaetzbar"


class Certainty(StrEnum):
    """GRADE levels."""

    HOCH = "hoch"
    MITTEL = "mittel"
    NIEDRIG = "niedrig"
    SEHR_NIEDRIG = "sehr_niedrig"


class Transferability(Model):
    rating: Literal["hoch", "mittel", "niedrig", "unklar"]
    note: str | None = None


class Finding(Statement):
    """What a study found about an approach for one outcome."""

    approach_id: str = Field(pattern=ID_PATTERN)
    case_id: str | None = Field(default=None, pattern=ID_PATTERN)
    outcome: str = Field(min_length=1, description="what was measured, e.g. 'Mietbelastung'")
    direction: Direction
    certainty: Certainty
    study_design: int | None = Field(default=None, ge=1, le=5, description="Maryland scale")
    transferability: Transferability


class Stance(StrEnum):
    STUETZT = "stuetzt"
    LEHNT_AB = "lehnt_ab"


class Position(Statement):
    approach_id: str = Field(pattern=ID_PATTERN)
    stance: Stance
    actor: str = Field(min_length=1)
    stated_on: date


class CoverageState(StrEnum):
    NICHT_KURATIERT = "nicht_kuratiert"  # nobody has looked yet
    GESUCHT_OHNE_BEFUND = "gesucht_ohne_befund"  # searched, found no evaluation
    BEFUND = "befund"  # at least one finding


class CoverageCell(Model):
    """One cell of the approach × outcome matrix."""

    approach_id: str = Field(pattern=ID_PATTERN)
    outcome: str
    state: CoverageState
    finding_ids: list[str] = []
    searched_at: date | None = None
    search_note: str | None = None

    @model_validator(mode="after")
    def state_matches_content(self):
        has_findings = bool(self.finding_ids)
        if (self.state == CoverageState.BEFUND) != has_findings:
            raise ValueError("state 'befund' if and only if finding_ids are given")
        if self.state == CoverageState.GESUCHT_OHNE_BEFUND and not (
            self.searched_at and self.search_note
        ):
            raise ValueError("'gesucht_ohne_befund' needs searched_at and search_note")
        return self


# --- one YAML file ------------------------------------------------------------


class Dossier(Model):
    """Content of one curated YAML file; all references must resolve inside it."""

    schema_version: Literal["0.1"] = SCHEMA_VERSION
    sources: list[Source] = []
    questions: list[Question] = []
    approaches: list[Approach] = []
    bills: list[Bill] = []
    cases: list[Case] = []
    findings: list[Finding] = []
    positions: list[Position] = []
    coverage: list[CoverageCell] = []

    @model_validator(mode="after")
    def references_resolve(self):
        groups = [self.sources, self.questions, self.approaches, self.bills, self.cases]
        groups += [self.findings, self.positions]
        ids = [item.id for group in groups for item in group]
        duplicates = {i for i in ids if ids.count(i) > 1}
        if duplicates:
            raise ValueError(f"duplicate ids: {sorted(duplicates)}")

        def require(kind: str, wanted: str | None, existing: list) -> None:
            if wanted is not None and wanted not in {item.id for item in existing}:
                raise ValueError(f"unknown {kind} id: {wanted}")

        statements = [*self.approaches, *self.bills, *self.cases, *self.findings, *self.positions]
        for statement in statements:
            require("source", statement.source_id, self.sources)
        for approach in self.approaches:
            require("question", approach.question_id, self.questions)
        for bill in self.bills:
            for question_id in bill.question_ids:
                require("question", question_id, self.questions)
            for approach_id in bill.approach_ids:
                require("approach", approach_id, self.approaches)
        for item in [*self.cases, *self.findings, *self.positions, *self.coverage]:
            require("approach", item.approach_id, self.approaches)
        cases = {case.id: case for case in self.cases}
        for finding in self.findings:
            require("case", finding.case_id, self.cases)
            if finding.case_id and cases[finding.case_id].approach_id != finding.approach_id:
                raise ValueError(f"finding {finding.id}: case belongs to another approach")

        # A cell may only cite findings about its own approach and outcome, and
        # each approach × outcome has exactly one cell.
        findings = {finding.id: finding for finding in self.findings}
        cells = [(cell.approach_id, cell.outcome) for cell in self.coverage]
        if len(cells) != len(set(cells)):
            raise ValueError("more than one coverage cell for the same approach and outcome")
        for cell in self.coverage:
            for finding_id in cell.finding_ids:
                require("finding", finding_id, self.findings)
                cited = findings[finding_id]
                if (cited.approach_id, cited.outcome) != (cell.approach_id, cell.outcome):
                    raise ValueError(f"cell cites finding {finding_id} of another approach/outcome")
        return self


# --- derived signal -----------------------------------------------------------

Signal = Literal["wirkt", "wirkt_nicht", "gemischt", "nicht_schaetzbar", "ungemessen", "offen"]


def effect_signal(cell: CoverageCell, findings: list[Finding]) -> Signal:
    """The signal shown for one approach × outcome cell.

    Missing data never turns into "wirkt_nicht": that value can only come from a
    finding whose direction is "keine_oder_negativ". "ungemessen" only comes from
    a cell that was searched without result; a cell nobody searched is "offen".
    """
    if cell.state == CoverageState.NICHT_KURATIERT:
        return "offen"
    if cell.state == CoverageState.GESUCHT_OHNE_BEFUND:
        return "ungemessen"
    directions = {f.direction for f in findings if f.id in cell.finding_ids}
    estimable = directions - {Direction.NICHT_SCHAETZBAR}
    if not estimable:
        return "nicht_schaetzbar"
    if estimable == {Direction.POSITIV}:
        return "wirkt"
    if estimable == {Direction.KEINE_ODER_NEGATIV}:
        return "wirkt_nicht"
    return "gemischt"


# --- files ----------------------------------------------------------------------

SCHEMA_FILE = Path(__file__).resolve().parents[2] / "schema" / "dossier-v0.schema.json"


def json_schema() -> dict:
    return Dossier.model_json_schema()


def json_schema_text() -> str:
    return json.dumps(json_schema(), ensure_ascii=False, indent=2) + "\n"


def load_dossier(path: Path) -> Dossier:
    """Read and validate one curated YAML file (safe_load: no code execution)."""
    return Dossier.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    # python -m open_policy_navigator.schema  -> rewrite the exported JSON Schema
    SCHEMA_FILE.write_text(json_schema_text(), encoding="utf-8", newline="\n")
    print(f"wrote {SCHEMA_FILE}")
