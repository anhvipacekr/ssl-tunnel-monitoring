"""Create deterministic, non-sensitive tunnel point-cloud epochs for the public demo."""

from __future__ import annotations

import csv
import json
from math import cos, pi, sin
from pathlib import Path


CHAINAGES_M = (0, 10, 20, 30, 40, 45, 50)
ANGLES_DEG = tuple(range(0, 360, 5))
SAMPLES_PER_BIN = 10


def public_data_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "generated"


def _is_crown(angle_deg: int) -> bool:
    return 60 <= angle_deg <= 120


def _is_right_sidewall(angle_deg: int) -> bool:
    return angle_deg >= 330 or angle_deg <= 30


def _movement_m(epoch: str, chainage_m: int, angle_deg: int) -> float:
    if epoch != "T1":
        return 0.0
    if chainage_m == 20 and _is_crown(angle_deg):
        return -0.025  # 25 mm inward crown movement.
    if chainage_m == 45 and _is_right_sidewall(angle_deg):
        return -0.020  # 20 mm inward right-sidewall movement.
    return 0.0


def _is_occluded(epoch: str, chainage_m: int, angle_deg: int) -> bool:
    return epoch == "T1" and chainage_m == 40 and _is_crown(angle_deg)


def _radius_m(epoch: str, chainage_m: int, angle_deg: int, sample: int) -> float:
    angle_rad = angle_deg * pi / 180.0
    profile_m = 3.0 + 0.012 * sin(angle_rad * 2.0) + 0.002 * sin(chainage_m / 10.0)
    centered_sample = sample - (SAMPLES_PER_BIN - 1) / 2.0
    noise_m = centered_sample * (0.0004 if epoch == "T0" else 0.0005)
    return profile_m + _movement_m(epoch, chainage_m, angle_deg) + noise_m


def _write_epoch(path: Path, epoch: str) -> int:
    count = 0
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("chainage_m", "angle_deg", "sample", "x_m", "y_m", "z_m", "radius_m"),
        )
        writer.writeheader()
        for chainage_m in CHAINAGES_M:
            for angle_deg in ANGLES_DEG:
                if _is_occluded(epoch, chainage_m, angle_deg):
                    continue
                angle_rad = angle_deg * pi / 180.0
                for sample in range(SAMPLES_PER_BIN):
                    radius_m = _radius_m(epoch, chainage_m, angle_deg, sample)
                    writer.writerow(
                        {
                            "chainage_m": chainage_m,
                            "angle_deg": angle_deg,
                            "sample": sample,
                            "x_m": f"{radius_m * cos(angle_rad):.7f}",
                            "y_m": f"{radius_m * sin(angle_rad):.7f}",
                            "z_m": f"{chainage_m + (sample - 4.5) * 0.0001:.7f}",
                            "radius_m": f"{radius_m:.7f}",
                        }
                    )
                    count += 1
    return count


def write_synthetic_dataset(output_dir: Path | None = None) -> dict[str, object]:
    """Write public T0/T1 CSV epochs and return their non-sensitive manifest."""
    output_dir = output_dir or public_data_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = {
        "T0": _write_epoch(output_dir / "T0.csv", "T0"),
        "T1": _write_epoch(output_dir / "T1.csv", "T1"),
    }
    manifest = {
        "kind": "deterministic_synthetic_public_demo",
        "units": {"coordinates": "m", "movement": "mm"},
        "epochs": ["T0", "T1"],
        "point_counts": counts,
        "prescribed_changes": [
            {"chainage_m": 20, "zone": "crown", "movement_mm": -25.0},
            {"chainage_m": 45, "zone": "right_sidewall", "movement_mm": -20.0},
        ],
        "deliberate_occlusion": {
            "epoch": "T1",
            "chainage_m": 40,
            "zone": "crown",
            "effect": "no point support; expected insufficient data",
        },
        "privacy": "No field or client point cloud data is used.",
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    manifest = write_synthetic_dataset()
    print(f"Wrote public synthetic data to {public_data_dir()}")
    print(f"T0 points: {manifest['point_counts']['T0']}")
    print(f"T1 points: {manifest['point_counts']['T1']}")


if __name__ == "__main__":
    main()
