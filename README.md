# Gridloom Dispatch

Gridloom Dispatch is a small production cost model for power systems, written in Python. It solves hourly nodal dispatch with DC power flow, line losses, thermal plant fuel costs, and wind and solar profiles. Each solve is one sparse linear programme using the open-source HiGHS solver.

This is the **v0.1.0** core: a contiguous block of hours in a single LP. Unit commitment, storage, hydro budgets, full-year windowed runs and expansion live in later releases.

## Install

```
pip install -e .[test]
```

Requires Python 3.9 or later, numpy, pandas, scipy and highspy.

## Quick start

```
python -m gridloom_dispatch examples/synthetic_4node out --year 2027
```

By default this solves the first 168 hours of the year and writes hourly nodal prices, generation by unit, unserved energy and line flows. Pass `--hours 0 47` for a shorter block.

From Python:

```python
import gridloom_dispatch as gd
case = gd.Case('examples/synthetic_4node')
res = gd.dispatch(case, 2027)          # dict of DataFrames: price, gen, use, flows
res = gd.dispatch(case, 2027, range(48))
```

## Example data

`examples/synthetic_4node` is a **synthetic** four-node system made by `scripts/make_synthetic_case.py` (seed 42). The numbers are invented for testing and do not describe any real power system.

## Case format

A case is a folder of CSV files:

| File | Columns |
|---|---|
| `case.json` | `base_year`, `discount_rate`, `voll_usd_mwh`, `ref_node`, optional `line_loss_frac`, `flow_cost_usd_mwh` |
| `nodes.csv` | `node`, `name`, `peak_MW` |
| `profiles.csv` | 8760 rows: `load` and any wind or solar capacity-factor columns |
| `generators.csv` | `name`, `node`, `type` (`thermal`, `solar`, `wind`), `mw`, `heat_rate`, `fuel_usd_mmbtu`, `vom`, `profile` (for solar/wind) |
| `branches.csv` | `name`, `from`, `to`, `MVA`, `x_pu`, `loss_pct` |

## Tests

```
python -m pytest -q
```

## Licence

MIT. Copyright (c) 2026 Transition Economics Institute. See `LICENSE`. Please cite using `CITATION.cff`.
