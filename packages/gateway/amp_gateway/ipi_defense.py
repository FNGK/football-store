"""Embedding-based anomaly detection for competitive intelligence (anti-IPI)."""

import hashlib
import math
from typing import Iterable


def _char_ngram_vector(text: str, dims: int = 64) -> list[float]:
    """Lightweight bag-of-ngrams vector without external embedding API."""
    vec = [0.0] * dims
    normalized = text.lower().strip()
    for i in range(len(normalized) - 2):
        gram = normalized[i : i + 3]
        idx = int(hashlib.md5(gram.encode()).hexdigest(), 16) % dims
        vec[idx] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def detect_ipi_anomaly(
    scraped_text: str,
    baseline_corpus: Iterable[str],
    threshold: float = 0.15,
) -> bool:
    """
    Flag content whose n-gram profile diverges sharply from baseline.
    Hidden adversarial prompt injections often introduce out-of-distribution tokens.
    """
    vec = _char_ngram_vector(scraped_text)
    if not baseline_corpus:
        return False
    sims = [cosine_similarity(vec, _char_ngram_vector(b)) for b in baseline_corpus]
    max_sim = max(sims) if sims else 0.0
    return max_sim < threshold
