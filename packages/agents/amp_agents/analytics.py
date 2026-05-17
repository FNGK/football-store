"""GeoLift incrementality and Bayesian MMM calibration stubs."""

from dataclasses import dataclass


@dataclass
class GeoLiftDesign:
    holdout_regions: list[str]
    test_regions: list[str]
    holdout_spend_pct: float = 0.0


def design_geolift(
    regions: list[str],
    holdout_fraction: float = 0.2,
) -> GeoLiftDesign:
    n_holdout = max(1, int(len(regions) * holdout_fraction))
    holdout = regions[:n_holdout]
    test = regions[n_holdout:]
    return GeoLiftDesign(holdout_regions=holdout, test_regions=test)


def calibrate_mmm_prior(
    observed_lift: float,
    posterior_mean: float,
    prior_weight: float = 0.5,
) -> float:
    """Simple Bayesian update for channel incrementality."""
    return prior_weight * posterior_mean + (1 - prior_weight) * observed_lift
