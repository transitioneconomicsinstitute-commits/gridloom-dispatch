"""Simple contiguous-hour dispatch (no windowing or checkpoints in the core)."""
import numpy as np
from . import model as M

def dispatch(case, year, hours=None, log=print):
    """Solve one LP over `hours` (default: first 168 hours of the year). Returns extract() dict."""
    H=np.arange(168) if hours is None else np.asarray(hours)
    m=M.solve(M.build(case,H,year=year))
    if m['status']!='Optimal': raise RuntimeError(f'dispatch: {m["status"]}')
    log(f'dispatch {year} hours {int(H[0])}-{int(H[-1])} {m["status"]}')
    return M.extract(m)
