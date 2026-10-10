# Controlled Validation Snapshot

## Dataset and protocol

Results come from 160 controlled synthetic cases on OS6-derived tunnel
geometry. Inputs are pre-aligned. The benchmark varies:

- point density: 100%, 50%, 25%, and 10%;
- angular occlusion: 0, 30, 60, and 90 degrees;
- imposed movement: 0, 5, 10, 20, and 40 mm;
- zones: crown and right sidewall.

All results below are provisional synthetic evidence. They are not a claim of
field accuracy or a universal scanner threshold.

## Results

| Method | Evaluated / 160 | False positives / 32 negatives | Recall on all 128 positives | RMSE |
| --- | ---: | ---: | ---: | ---: |
| Fixed 10 mm | 90 | 4 | 39.8% | 13.621 mm radial |
| Point-only local LoD95 | 90 | 0 | 23.4% | 13.621 mm radial |
| Coverage-gated local LoD95 | 25 | 0 | 11.7% | 0.312 mm radial |
| M3C2 | 100 | 0 | 38.3% | 2.188 mm normal-vs-radial |

The coverage-gated method evaluated only 25 cases because it rejected 135
cases without enough local support. This is expected behavior, not missing
accounting. It keeps unsupported observations from becoming deformation alerts.

## Interpretation

- Fixed 10 mm baseline produced four false alerts under tested sparse cases.
- Local LoD methods produced zero false alerts in this controlled matrix.
- Quality gates reduce false alerts by abstaining more often.
- M3C2 and radial displacement have different estimands. Their RMSE values are
  shown for transparency, not as a direct ranking.

## What remains

Field validation needs repeated real tunnel surveys, independent displacement
reference, held-out validation, and registration quality reporting. Raw data
and unpublished artifacts are deliberately excluded from this public project.
