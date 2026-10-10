"""Runnable checks for the public LoD95 example."""

from local_lod_demo import decision, local_lod95


def main() -> None:
    lod95_mm = local_lod95(45.0983, 45.0983, 39)
    assert round(lod95_mm, 3) == 20.017
    assert decision(16.791, lod95_mm) == "NOT CONFIRMED"
    assert decision(20.018, lod95_mm) == "CONFIRMED DEFORMATION"
    print("local_lod_demo checks passed")


if __name__ == "__main__":
    main()
