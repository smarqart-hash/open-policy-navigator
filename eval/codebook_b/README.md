# Codebook B: categories for all government drafts (proposal)

`proposals_government_v0.json` assigns a codebook-B category (see `eval/README.md`)
to each of the 532 government drafts (WP 20/21) whose section C the pattern de-v0
found. **These are proposals by a language model** (ADR 0005). It read the stored
section text. No human has confirmed them. Borderline cases are mostly legal-form
alternatives (a regulation instead of a law, a route via the MLI) and "alternatives
examined, but not named" (`examined_not_named`, 6 drafts, e.g. JStG 2026).

## Result (20 November 2026, provisional)

Found sections (532) plus an extrapolation of the 87 missed ones from the gold set
sample. Of the 20 missed drafts in the sample, 16 have a section C: 11 name an
alternative, 5 say "Keine" with reasons.

| category | found (532) | estimate incl. missed (≈ 602) |
|---|---|---|
| Keine (only the statement, no reasons) | 335 | 335 (≈ 56 %) |
| Keine + Begründung (no concrete alternative named) | 114 | ≈ 136 (≈ 23 %) |
| Status quo genannt | 29 | 29 (≈ 5 %) |
| Alternativen benannt/diskutiert | 54 | ≈ 102 (≈ 17 %, range ≈ 14–20 %) |

The range for named alternatives comes from the Wilson interval of 11/20 in the
missed stratum only. The other uncertainty (proposals instead of confirmed labels,
borderline cases) is not included.

Reading: in about **four out of five** government drafts, section C names no
concrete alternative (≈ 78 % "Keine" with or without reasons, ≈ 83 % if
status-quo-only sections are counted). Only about **one in six** names a concrete
alternative and says why it was rejected.

Next step: Stefan checks a random sample of these proposals (for example 50),
so that the error rate of the proposals can be stated (ADR 0005, point 5).
