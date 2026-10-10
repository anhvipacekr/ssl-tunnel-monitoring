# SSL Smart Tunnel Monitoring

[![Scope: controlled synthetic benchmark](https://img.shields.io/badge/scope-controlled%20synthetic%20benchmark-1d2a20)](docs/VALIDATION.md)
[![Runtime: Python 3.10+](https://img.shields.io/badge/runtime-Python%203.10%2B-3776ab)](examples/local_lod_demo.py)
[![Project page](https://img.shields.io/badge/project-GitHub%20Pages-c8fa5b)](https://anhvipacekr.github.io/ssl-tunnel-monitoring/)

Public project page for a Python desktop workflow that compares tunnel point
cloud epochs (T0/Tn), localizes deformation evidence by chainage, and reports
when evidence is too weak for a safe alert.

**Project page:** https://anhvipacekr.github.io/ssl-tunnel-monitoring/

## What it demonstrates

- Point-cloud monitoring workflow: import, clean, register, section, assess,
  and export.
- Crown settlement and bilateral sidewall convergence assessment.
- Coverage-aware local LoD95 decisions: `confirmed`, `not confirmed`, or
  `insufficient data`.
- Excel/PDF/IFC reporting paths in desktop research prototype.
- Controlled synthetic benchmark reporting false positives, recall, and
  abstentions together.

## Repository map

| Path | Purpose |
| --- | --- |
| [index.html](index.html) | Project website hosted by GitHub Pages. |
| [docs/METHOD.md](docs/METHOD.md) | Local LoD95 decision rule and support gate. |
| [docs/VALIDATION.md](docs/VALIDATION.md) | Controlled benchmark results and claim boundary. |
| [docs/PUBLIC_DEMO.md](docs/PUBLIC_DEMO.md) | Public synthetic T0/T1 demo protocol. |
| [examples/generate_synthetic_tunnel.py](examples/generate_synthetic_tunnel.py) | Creates non-sensitive T0/T1 point clouds. |
| [examples/analyze_tunnel_epochs.py](examples/analyze_tunnel_epochs.py) | Computes chainage-linked local evidence. |
| [outputs/public_showcase/](outputs/public_showcase) | Public CSV, JSON, and Excel evidence output. |

## Public evidence snapshot

The public benchmark contains 160 controlled, pre-aligned synthetic cases on
OS6-derived tunnel geometry. It varies point density, angular occlusion,
movement, and zone. It is not field validation.

| Method | False positives / 32 negative cases | Abstention | Notes |
| --- | ---: | ---: | --- |
| Fixed 10 mm rule | 4 | 43.8% | Misses small/boundary movement and can alert on sparse observations. |
| Point-only local LoD95 | 0 | 43.8% | Uses local scatter and common angular support. |
| Coverage-gated local LoD95 | 0 | 84.4% | Withholds results when support is inadequate. |
| M3C2 comparator | 0 | 37.5% | Supplementary normal-distance measure; not ranked against radial RMSE. |

Read methodology and limits in [docs/METHOD.md](docs/METHOD.md) and
[docs/VALIDATION.md](docs/VALIDATION.md).

## Run full public demo

No package install needed. Python 3.10+:

```powershell
python examples/generate_synthetic_tunnel.py
python examples/analyze_tunnel_epochs.py
python examples/test_tunnel_demo.py
```

The generator creates deterministic 3D T0/T1 tunnel points. The analyzer
confirms 25 mm crown movement at Ch. 20 m, confirms 20 mm right-sidewall
movement at Ch. 45 m, and returns `INSUFFICIENT DATA` for a deliberately
occluded crown at Ch. 40 m. It writes:

- [section_evidence.csv](outputs/public_showcase/section_evidence.csv)
- [summary.json](outputs/public_showcase/summary.json)
- [synthetic_tunnel_evidence.xlsx](outputs/public_showcase/synthetic_tunnel_evidence.xlsx)

Read the protocol in [docs/PUBLIC_DEMO.md](docs/PUBLIC_DEMO.md).

## Small LoD95 example

```powershell
python examples/local_lod_demo.py
python examples/test_local_lod_demo.py
```

The demo recreates a human-readable local-evidence decision: a 16.791 mm
measurement does not confirm movement when its local LoD95 is 20.017 mm.

## Outputs in full research prototype

The maintained desktop prototype can export chainage-linked evidence to Excel,
PDF, and IFC workflows. Those implementation paths and any generated point
cloud artifacts are not bundled here because this is a small public showcase.

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
