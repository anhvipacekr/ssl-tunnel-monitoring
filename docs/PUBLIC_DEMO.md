# Public Synthetic T0/T1 Demo

This demo shows three outcomes from the same deterministic point-cloud model:

| Location | Prescribed condition | Expected decision |
| --- | --- | --- |
| Ch. 20 m, crown | 25 mm inward movement | `CONFIRMED DEFORMATION` |
| Ch. 45 m, right sidewall | 20 mm inward movement | `CONFIRMED DEFORMATION` |
| Ch. 40 m, crown | T1 crown points deliberately removed | `INSUFFICIENT DATA` |
| Other supported locations | no imposed change | `NOT CONFIRMED` |

Run from repository root:

```powershell
python examples/generate_synthetic_tunnel.py
python examples/analyze_tunnel_epochs.py
python examples/test_local_lod_demo.py
python examples/test_tunnel_demo.py
```

Generated T0/T1 CSV inputs stay under `data/generated/` and are ignored by
Git. Public outputs are committed under `outputs/public_showcase/`:

- `section_evidence.csv`: chainage, zone, movement, local LoD95, coverage,
  decision, and reason.
- `synthetic_tunnel_evidence.xlsx`: formatted Excel view of the same evidence.
- `summary.json`: demo parameters and decision counts.

The synthetic data has no real tunnel geometry, scanner positions, field scans,
client data, or personal information. It demonstrates data flow and decision
behavior only. It does not validate field accuracy.
