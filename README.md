# SSL Smart Tunnel Monitoring

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

## Run public demo

No package install needed. Python 3.10+:

```powershell
python examples/local_lod_demo.py
python examples/test_local_lod_demo.py
```

The demo recreates a human-readable local-evidence decision: a 16.791 mm
measurement does not confirm movement when its local LoD95 is 20.017 mm.

## Deliberate public boundary

This repository excludes raw scans, large generated point clouds, internal
archives, local paths, credentials, and unpublished research material. Full
project code and data remain under active development. No license is granted
for reuse of material in this repository; contact the author for permission.

## CV wording

**SSL Smart Tunnel Monitoring - 4D LiDAR point-cloud deformation analysis**

https://anhvipacekr.github.io/ssl-tunnel-monitoring/
