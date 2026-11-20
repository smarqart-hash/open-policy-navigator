# Eval ratchet

Checks the German data file against a hand-annotated gold set. CI runs
`python -m open_policy_navigator.evaluation --check` and fails if a metric drops
below `thresholds.json`. Thresholds only go up (`--update`), never down.
Only labels confirmed by a human count for the ratchet; proposals are shown
for information. As long as nothing is confirmed, all thresholds are `null`.

## Gold set v0 (`goldset_v0.json`)

36 government drafts (WP 20/21), sampled in two strata:

| stratum | population | in gold set | how chosen |
|---|---|---|---|
| `not_found_v0` (pattern found no section C) | 87 | 20 | random, seed 20261120 |
| `found_v0` | 532 | 16 | by v0 category, plus 21/8283 (JStG 2026), 20/12719, 20/11310 |

Because misses are over-sampled, recall is weighted by stratum size (see
`src/open_policy_navigator/evaluation.py`). Its interval is approximate (only the
share of real sections among the misses is varied), so it is too narrow.

## Annotation status (20 November 2026)

- **20 `not_found_v0` items: open.** Stefan checks the Drucksache PDF and fills
  `section_present` (is there a section "C. Alternativen"?), `gold_alt` (its text,
  whitespace does not matter) and `category`. Until then `section_recall` is *pending*.
- **16 `found_v0` items: proposals by Claude** (`"coder": "claude-proposal"`,
  `"confirmed": false`), taken from the stored text. `gold_alt` must be checked
  against the PDF (start and end of the section); `category` deviates from the
  rule result for 20/12719 and 20/11310. After checking, set `"coder": "stefan"`
  and `"confirmed": true`.

Metrics including proposals (information only, not used by the ratchet):

| metric | value | 95 % Wilson interval | n |
|---|---|---|---|
| extraction_precision | 1.000 | 0.806–1.000 | 16 |
| classification_accuracy | 0.875 | 0.640–0.965 | 16 |
| section_recall | pending | | |

`extraction_precision` is 1.0 by construction as long as `gold_alt` is a copy of
the stored text; it only becomes meaningful after checking against the PDFs.

## Double coding

Every item has `coding_2` (same fields as `coding_1`, default `null`). A second
person codes independently, without looking at `coding_1`. The run prints Cohen's
κ for `category` on all items coded twice.

## Categories (codebook B, decided by Stefan on 20 November 2026)

| category | when |
|---|---|
| `Keine` | only "Keine" or "there are no alternatives", without reasons |
| `Keine + Begründung` | no alternative, with reasons, but **no concrete alternative is named** |
| `Status quo genannt` | only keeping the current law is discussed |
| `Alternativen benannt/diskutiert` | at least one concrete alternative is named, **also if the section starts with "Keine" and rejects it** |

`section_present` refers only to section "C. Alternativen" of the Vorblatt, not to a
heading "Alternativen" in the explanatory memorandum (budget laws have the latter).

The rule classifier v0 still sorts by the first word, so it counts "Keine." followed
by a rejected alternative as `Keine + Begründung`. Under codebook B that is a miss;
the gold set measures it, classifier v1 should fix it (roadmap issue 4).
