# Changelog

## 0.2.0 (2026-10-23)
- `LP.solve` accepts `method='hipo'` (HiGHS's parallel interior-point solver; install the optional extra `open-pcm[hipo]`, i.e. `highspy-extras`), plus `tol` (IPM optimality tolerance) and `threads`. Interior-point methods (`ipm`, `ipx`, `hipo`) run without crossover and retry with crossover if the solve is not optimal.
- Demand growth from `base_year` is applied to node load peaks.
- `crf` handles a zero discount rate and validates its inputs.
- Dispatch rejects empty or out-of-range hour ranges.
- Project renamed to OPEN-PCM (package `open_pcm`, CLI `open-pcm`).

## 0.1.0 (2026-10-15)
- First release: hourly nodal production cost model with DC power flow, losses, thermal fuel costs and wind/solar profiles, solved as one sparse LP with HiGHS.
