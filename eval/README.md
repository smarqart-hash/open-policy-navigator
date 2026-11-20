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

All 36 items are confirmed by Stefan (`"coder": "stefan"`, `"confirmed": true`) and
were cross-checked against the Drucksache PDFs: every stored `gold_alt` matches the
PDF apart from page headers and hyphenation. The cross-check corrected three labels
under codebook B: 20/12400 (budget law, "Keine." stands only in the explanatory
memorandum, so no section C), 21/2672 (`Keine`) and 20/3874 (`Status quo genannt`);
the last two still carried the v0 rule result.

A blind second coding by a language model (information only, not stored as
`coding_2`, which is reserved for a second person) agreed on 34 of 36 items. The two
differences are borderline cases and keep Stefan's label: 20/11226 (is "waiting for
the next amendment" a concrete alternative?) and 20/8654 (is "leave it to the Länder"
named as an alternative?).

Confirmed metrics, now the ratchet thresholds (`--update`, 20 November 2026):

| metric | value | 95 % Wilson interval | n |
|---|---|---|---|
| extraction_precision | 1.000 | 0.806–1.000 | 16 |
| classification_accuracy | 0.750 | 0.505–0.898 | 16 |
| section_recall | 0.884 | approx. 0.869–0.913 | 36 |

`classification_accuracy` compares the v0 rule (first word only) with codebook B, so
0.75 is the expected gap that classifier v1 should close (roadmap issue 4).

## Target (as promised in the application)

Gold set of 100 drafts, 70 of them coded independently by two people.
Agreement as Krippendorff's α per category with confidence interval, target
≥ 0.800 (Krippendorff 2004); this script still reports Cohen's κ only.
Target recall of the section detection: 95 %, with a public error report.
Roadmap issue 1.

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
