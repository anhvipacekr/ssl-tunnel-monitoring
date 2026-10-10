"""Runnable regression check for public synthetic tunnel demo."""

from __future__ import annotations

from tempfile import TemporaryDirectory
from pathlib import Path

from analyze_tunnel_epochs import analyze_epochs, write_public_results
from generate_synthetic_tunnel import write_synthetic_dataset


def _row(rows: list[dict[str, object]], chainage_m: int, zone: str) -> dict[str, object]:
    return next(row for row in rows if row["chainage_m"] == chainage_m and row["zone"] == zone)


def main() -> None:
    with TemporaryDirectory() as temporary_directory:
        data_dir = Path(temporary_directory) / "data"
        output_dir = Path(temporary_directory) / "outputs"
        manifest = write_synthetic_dataset(data_dir)
        assert manifest["point_counts"] == {"T0": 5040, "T1": 4910}
        rows = analyze_epochs(data_dir)
        assert len(rows) == 14
        assert _row(rows, 20, "crown")["decision"] == "CONFIRMED DEFORMATION"
        assert round(float(_row(rows, 20, "crown")["measured_mm"]), 3) == -25.0
        assert _row(rows, 45, "right_sidewall")["decision"] == "CONFIRMED DEFORMATION"
        assert round(float(_row(rows, 45, "right_sidewall")["measured_mm"]), 3) == -20.0
        assert _row(rows, 40, "crown")["decision"] == "INSUFFICIENT DATA"
        assert _row(rows, 10, "crown")["decision"] == "NOT CONFIRMED"
        summary = write_public_results(rows, output_dir)
        assert summary == {
            "CONFIRMED DEFORMATION": 2,
            "NOT CONFIRMED": 11,
            "INSUFFICIENT DATA": 1,
        }
        assert (output_dir / "section_evidence.csv").is_file()
        assert (output_dir / "summary.json").is_file()
    print("synthetic_tunnel_demo checks passed")


if __name__ == "__main__":
    main()
