"""Standalone local LoD95 decision example. Python standard library only."""

from __future__ import annotations

from math import isfinite, sqrt


def local_lod95(sigma_t0_mm: float, sigma_tn_mm: float, common_bins: int) -> float:
    """Return 95% local detection limit from robust scatter and shared bins."""
    if not isfinite(sigma_t0_mm) or sigma_t0_mm < 0:
        raise ValueError("sigma_t0_mm must be finite and non-negative.")
    if not isfinite(sigma_tn_mm) or sigma_tn_mm < 0:
        raise ValueError("sigma_tn_mm must be finite and non-negative.")
    if isinstance(common_bins, bool) or common_bins < 1:
        raise ValueError("common_bins must be a positive integer.")
    return 1.96 * sqrt((sigma_t0_mm ** 2 + sigma_tn_mm ** 2) / common_bins)


def decision(measured_mm: float, lod95_mm: float) -> str:
    """Classify a quality-supported local movement using the strict protocol rule."""
    if not isfinite(measured_mm):
        raise ValueError("measured_mm must be finite.")
    if not isfinite(lod95_mm) or lod95_mm < 0:
        raise ValueError("lod95_mm must be finite and non-negative.")
    return "CONFIRMED DEFORMATION" if abs(measured_mm) > lod95_mm else "NOT CONFIRMED"


def main() -> None:
    measured_mm = 16.791
    lod95_mm = local_lod95(sigma_t0_mm=45.0983, sigma_tn_mm=45.0983, common_bins=39)
    print(f"Measured movement: {measured_mm:.3f} mm")
    print(f"Local LoD95: {lod95_mm:.3f} mm")
    print(f"Decision: {decision(measured_mm, lod95_mm)}")
    print("Reason: movement must exceed local LoD95 to confirm a change.")


if __name__ == "__main__":
    main()
