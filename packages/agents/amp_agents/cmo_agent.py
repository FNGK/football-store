"""AI CMO agent — cross-channel overlap and budget reallocation."""

from dataclasses import dataclass

from amp_shared.optimization import enforce_minimum_liquidity, shadow_bid, thompson_sample

import numpy as np


@dataclass
class ChannelPerformance:
    channel: str
    alpha: float = 1.0
    beta: float = 1.0
    spend_usd: float = 0.0


class AiCmoAgent:
    def select_channel(self, channels: list[ChannelPerformance]) -> str:
        alphas = np.array([c.alpha for c in channels])
        betas = np.array([c.beta for c in channels])
        idx = thompson_sample(alphas, betas)
        return channels[idx].channel

    def allocate_budget(
        self,
        total_usd: float,
        channels: list[ChannelPerformance],
        min_per_channel: float = 1250.0,
    ) -> dict[str, float]:
        enforce_minimum_liquidity(total_usd)
        n = len(channels) or 1
        per = max(total_usd / n, min_per_channel)
        return {c.channel: per for c in channels}

    def apply_sbl(self, base_cpc: float, impressions: int) -> float:
        return shadow_bid(base_cpc, impressions)
