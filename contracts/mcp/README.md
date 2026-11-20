# MCP answer contract v0.1

[`answer.schema.json`](answer.schema.json) is exported from
[`src/open_policy_navigator/contract.py`](../../src/open_policy_navigator/contract.py)
(`python -m open_policy_navigator.contract`). The server itself is not built yet;
the contract comes first so its behaviour can be tested (ADR 0003).

| `status` | when | rules |
|---|---|---|
| `answered` | cell has findings | `coverage_state: befund`, summary, ≥ 1 citation |
| `abstained` | in scope, but no findings | no summary, `reason`, states `coverage_state` |
| `out_of_scope` | not covered by the data | no summary, `reason`, no `coverage_state` |

Every answer names the data `release` (full Git commit hash). Citations are
`source_id` + `locator` (verbatim quote and position) and carry
`content_role: "data"`: quoted text is untrusted input, never an instruction.

`golden/valid/` must validate and round-trip unchanged; `golden/invalid/` must be
rejected (`tests/test_contract.py`).
