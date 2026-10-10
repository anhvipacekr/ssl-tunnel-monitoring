# Method

## Problem

Sparse or occluded point clouds can make a fixed deformation threshold report
a change where local evidence is weak. The Step 6 prototype therefore makes
three outcomes explicit:

- `CONFIRMED DEFORMATION`: measured movement exceeds local LoD95.
- `NOT CONFIRMED`: measurement exists but does not exceed local LoD95.
- `INSUFFICIENT DATA`: local angular support or coverage fails quality gates.

`NOT CONFIRMED` does not mean no movement. It means observed movement is not
large enough to distinguish from local measurement variation at 95% confidence.

## Local evidence calculation

Inputs must already be in one coordinate frame. For each one-metre chainage
slice, points are grouped into five-degree angular bins. Only bins occupied in
both T0 and Tn contribute to a local comparison.

```text
sigma = 1.4826 * median(abs(values - median(values)))
LoD95 = 1.96 * sqrt(sigma_T0^2 / common_bins + sigma_Tn^2 / common_bins)
```

For the total sidewall result:

```text
LoD95_total = sqrt(LoD95_left^2 + LoD95_right^2)
```

The code uses a strict decision rule: `abs(movement_mm) > LoD95_mm`.
Equality does not confirm a change.

## Coverage gate

Before making a result visible, each section must meet protocol settings from
the controlled benchmark:

| Parameter | Value |
| --- | ---: |
| Chainage spacing | 1.0 m |
| Axial half-window | 0.5 m |
| Angular bin width | 5 degrees |
| Minimum support | 10 points per bin |
| Minimum observed section arc | 200 degrees |
| Minimum zone coverage ratio | 0.60 |

The gate favors safety over coverage. A gray or orange outcome tells an
inspector to rescan or review local support instead of treating missing points
as deformation.

## Boundaries

This public methodology describes Step 6 deformation evidence only. It does
not validate registration, scanner calibration, or field accuracy. M3C2 is a
supplementary comparator because it measures normal distance while the primary
metric here is radial tunnel displacement.
