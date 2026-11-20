"""Small statistics helpers for the evaluation (no external dependencies)."""

import math
from collections import Counter
from collections.abc import Sequence

Z_95 = 1.959963984540054  # two-sided 95 % normal quantile


def wilson_interval(successes: int, n: int, z: float = Z_95) -> tuple[float, float]:
    """Wilson score interval for a proportion.

    Better than the plain normal interval for small n and proportions near 0 or 1,
    which is exactly our situation (a few dozen annotated drafts, rates near 100 %).
    """
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denominator = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denominator
    half_width = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return (max(0.0, centre - half_width), min(1.0, centre + half_width))


def cohen_kappa(coder_a: Sequence[str], coder_b: Sequence[str]) -> float | None:
    """Agreement of two coders beyond chance. None if undefined (no items, or
    both coders always use the same single category)."""
    if len(coder_a) != len(coder_b):
        raise ValueError("both codings must have the same length")
    n = len(coder_a)
    if n == 0:
        return None
    observed = sum(a == b for a, b in zip(coder_a, coder_b, strict=True)) / n
    count_a, count_b = Counter(coder_a), Counter(coder_b)
    expected = sum(count_a[c] * count_b[c] for c in count_a.keys() | count_b.keys()) / n**2
    if expected == 1:
        return None
    return (observed - expected) / (1 - expected)
