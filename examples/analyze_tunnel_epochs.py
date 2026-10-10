"""Analyze public synthetic T0/T1 tunnel epochs by chainage and angular zone."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import median

from local_lod_demo import decision, local_lod95


BIN_DEG = 5
MIN_BIN_POINTS = 10
MIN_ZONE_COVERAGE_RATIO = 0.60
ZONES = {
    "crown": tuple(range(60, 125, BIN_DEG)),
    "right_sidewall": tuple(range(330, 360, BIN_DEG)) + tuple(range(0, 35, BIN_DEG)),
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_radius_bins(path: Path) -> dict[tuple[float, int], list[float]]:
    bins: dict[tuple[float, int], list[float]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            bins[(float(row["chainage_m"]), int(row["angle_deg"]))].append(float(row["radius_m"]))
    return dict(bins)


def _robust_sigma_mm(values_m: list[float]) -> float:
    center = median(values_m)
    return 1000.0 * 1.4826 * median(abs(value - center) for value in values_m)


def _zone_evidence(
    chainage_m: float,
    zone: str,
    t0_bins: dict[tuple[float, int], list[float]],
    t1_bins: dict[tuple[float, int], list[float]],
) -> dict[str, object]:
    expected_angles = ZONES[zone]
    common_angles = [
        angle
        for angle in expected_angles
        if len(t0_bins.get((chainage_m, angle), ())) >= MIN_BIN_POINTS
        and len(t1_bins.get((chainage_m, angle), ())) >= MIN_BIN_POINTS
    ]
    coverage_ratio = len(common_angles) / len(expected_angles)
    result: dict[str, object] = {
        "chainage_m": chainage_m,
        "zone": zone,
        "common_bins": len(common_angles),
        "expected_bins": len(expected_angles),
        "coverage_ratio": coverage_ratio,
        "measured_mm": None,
        "lod95_mm": None,
    }
    if coverage_ratio < MIN_ZONE_COVERAGE_RATIO:
        result.update(
            {
                "decision": "INSUFFICIENT DATA",
                "reason": (
                    f"Only {len(common_angles)}/{len(expected_angles)} angular bins have "
                    f"at least {MIN_BIN_POINTS} points in both epochs."
                ),
            }
        )
        return result

    deltas_mm = [
        1000.0 * (median(t1_bins[(chainage_m, angle)]) - median(t0_bins[(chainage_m, angle)]))
        for angle in common_angles
    ]
    sigma_t0_mm = median(_robust_sigma_mm(t0_bins[(chainage_m, angle)]) for angle in common_angles)
    sigma_t1_mm = median(_robust_sigma_mm(t1_bins[(chainage_m, angle)]) for angle in common_angles)
    measured_mm = median(deltas_mm)
    lod95_mm = local_lod95(sigma_t0_mm, sigma_t1_mm, len(common_angles))
    outcome = decision(measured_mm, lod95_mm)
    result.update({"measured_mm": measured_mm, "lod95_mm": lod95_mm, "decision": outcome})
    if outcome == "CONFIRMED DEFORMATION":
        result["reason"] = (
            f"Measured {measured_mm:+.3f} mm exceeds local detection limit {lod95_mm:.3f} mm."
        )
    else:
        result["reason"] = (
            f"Measured {measured_mm:+.3f} mm is within local detection limit {lod95_mm:.3f} mm."
        )
    return result


def analyze_epochs(data_dir: Path) -> list[dict[str, object]]:
    t0_bins = _load_radius_bins(data_dir / "T0.csv")
    t1_bins = _load_radius_bins(data_dir / "T1.csv")
    chainages = sorted({chainage for chainage, _ in t0_bins})
    return [_zone_evidence(chainage, zone, t0_bins, t1_bins) for chainage in chainages for zone in ZONES]


def write_public_results(rows: list[dict[str, object]], output_dir: Path) -> dict[str, int]:
    output_dir.mkdir(parents=True, exist_ok=True)
    fields = (
        "chainage_m",
        "zone",
        "measured_mm",
        "lod95_mm",
        "common_bins",
        "expected_bins",
        "coverage_ratio",
        "decision",
        "reason",
    )
    with (output_dir / "section_evidence.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    summary = {decision_name: sum(row["decision"] == decision_name for row in rows) for decision_name in (
        "CONFIRMED DEFORMATION", "NOT CONFIRMED", "INSUFFICIENT DATA"
    )}
    payload = {
        "kind": "public_synthetic_tunnel_evidence",
        "inputs": "data/generated/T0.csv and T1.csv",
        "parameters": {
            "angular_bin_deg": BIN_DEG,
            "min_bin_points": MIN_BIN_POINTS,
            "min_zone_coverage_ratio": MIN_ZONE_COVERAGE_RATIO,
        },
        "decision_counts": summary,
    }
    (output_dir / "summary.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    root = project_root()
    rows = analyze_epochs(root / "data" / "generated")
    summary = write_public_results(rows, root / "outputs" / "public_showcase")
    print("Public section evidence")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("Wrote outputs/public_showcase/section_evidence.csv and summary.json")


if __name__ == "__main__":
    main()
