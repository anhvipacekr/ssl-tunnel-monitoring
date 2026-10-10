# SSL Smart Tunnel Monitoring

[![Scope: controlled synthetic benchmark](https://img.shields.io/badge/scope-controlled%20synthetic%20benchmark-1d2a20)](docs/VALIDATION.md)
[![Runtime: Python 3.10+](https://img.shields.io/badge/runtime-Python%203.10%2B-3776ab)](examples/local_lod_demo.py)
[![Project page](https://img.shields.io/badge/project-GitHub%20Pages-c8fa5b)](https://anhvipacekr.github.io/ssl-tunnel-monitoring/)

Give this project an earlier and later 3D laser scan of a tunnel. It returns
one clear result for each area: movement found, no movement confirmed, or
rescan needed.

**Project page:** https://anhvipacekr.github.io/ssl-tunnel-monitoring/

## What it does

For each position along a tunnel, user sees one simple result:

- **Movement found**: measured movement is large enough to trust.
- **No movement confirmed**: measured difference may be normal scan variation.
- **Rescan needed**: too many points are missing to make a safe call.

The full desktop prototype also supports Excel, PDF, and IFC reporting.

## Try it first

No package install needed. Python 3.10+:

```powershell
python examples/generate_synthetic_tunnel.py
python examples/analyze_tunnel_epochs.py
python examples/test_tunnel_demo.py
```

This creates artificial 3D T0/T1 scans. The result should find:

- 25 mm roof movement at 20 m along tunnel;
- 20 mm right-wall movement at 45 m along tunnel;
- missing scan points at 40 m along tunnel, reported as `INSUFFICIENT DATA`.

Download matching public outputs:

- [Excel result](outputs/public_showcase/synthetic_tunnel_evidence.xlsx)
- [CSV result](outputs/public_showcase/section_evidence.csv)
- [Example explanation](docs/PUBLIC_DEMO.md)

## Where things are

| Path | Purpose |
| --- | --- |
| [index.html](index.html) | Project website hosted by GitHub Pages. |
| [docs/PUBLIC_DEMO.md](docs/PUBLIC_DEMO.md) | What sample scan result means. |
| [examples/generate_synthetic_tunnel.py](examples/generate_synthetic_tunnel.py) | Creates artificial tunnel scans. |
| [examples/analyze_tunnel_epochs.py](examples/analyze_tunnel_epochs.py) | Checks movement and missing data. |
| [outputs/public_showcase/](outputs/public_showcase) | Downloadable CSV, JSON, and Excel result. |
| [docs/METHOD.md](docs/METHOD.md) | Technical LoD95 method. |
| [docs/VALIDATION.md](docs/VALIDATION.md) | Technical test results and limits. |

<details>
<summary>Technical test result</summary>

Optional technical detail: 160 controlled artificial cases test point density,
missing angular segments, movement size, and tunnel zone. This is not field
validation.

| Method | False positives / 32 negative cases | Abstention | Notes |
| --- | ---: | ---: | --- |
| Fixed 10 mm rule | 4 | 43.8% | Can alert when a scan is sparse. |
| Point-only local LoD95 | 0 | 43.8% | Uses local scan variation. |
| Local LoD95 plus coverage check | 0 | 84.4% | Says more scan data is needed when support is weak. |
| M3C2 comparison | 0 | 37.5% | Supplementary technical comparison. |

Read methodology and limits in [docs/METHOD.md](docs/METHOD.md) and
[docs/VALIDATION.md](docs/VALIDATION.md).
</details>

## Why no movement may be confirmed

```powershell
python examples/local_lod_demo.py
python examples/test_local_lod_demo.py
```

Example: 16.791 mm measured movement is not called a real change when normal
scan variation at that location is 20.017 mm. This avoids treating ordinary
scan noise as tunnel movement. Technical name: local LoD95.

## Outputs in full research prototype

The maintained desktop prototype can export location-linked evidence to Excel,
PDF, and IFC workflows. This small repository does not bundle the full app or
large point-cloud files.

The public Excel file contains synthetic chainage evidence only. It has a
formula-linked decision summary and a filterable evidence table.

## Deliberate public boundary

This repository excludes raw scans, large generated point clouds, internal
archives, local paths, credentials, and unpublished research material. Full
project code and data remain under active development. No license is granted
for reuse of material in this repository; contact the author for permission.

## Citation

See [CITATION.cff](CITATION.cff) for a machine-readable project citation.

## CV wording

**SSL Smart Tunnel Monitoring - 4D LiDAR point-cloud deformation analysis**

https://anhvipacekr.github.io/ssl-tunnel-monitoring/
