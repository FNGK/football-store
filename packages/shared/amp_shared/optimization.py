"""Thompson Sampling MAB, Shadow Bidding with Learning, minimum liquidity."""

import numpy as np


def thompson_sample(alphas: np.ndarray, betas: np.ndarray) -> int:
    """Select arm via Thompson Sampling for Bernoulli rewards."""
    samples = np.random.beta(alphas, betas)
    return int(np.argmax(samples))


def shadow_bid(base_bid: float, impressions: int, target_explore: int = 1000) -> float:
    """SBL: boost bids for cold-start creatives with low impressions."""
    if impressions >= target_explore:
        return base_bid
    explore_factor = 1.0 + (target_explore - impressions) / target_explore
    return base_bid * explore_factor


def enforce_minimum_liquidity(
    budget_usd: float,
    min_conversions_per_month: int = 50,
    estimated_cpa: float = 25.0,
) -> float:
    """Ensure budget supports platform learning phase (~50 conv/month)."""
    min_spend = min_conversions_per_month * estimated_cpa
    if budget_usd < min_spend:
        raise ValueError(
            f"Budget ${budget_usd:.2f} below minimum liquidity ${min_spend:.2f} "
            f"for {min_conversions_per_month} conversions/month"
        )
    return budget_usd
