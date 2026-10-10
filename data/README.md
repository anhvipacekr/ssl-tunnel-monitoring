# Synthetic Demo Data

`examples/generate_synthetic_tunnel.py` creates these files locally:

- `generated/T0.csv`: reference epoch.
- `generated/T1.csv`: monitoring epoch.
- `generated/manifest.json`: prescribed changes and deliberate crown occlusion.

All coordinates are deterministic, artificial tunnel points. They are not
derived from field scans, client data, or internal research fixtures. Generated
files stay ignored by Git because anyone can recreate them with the public
script.
