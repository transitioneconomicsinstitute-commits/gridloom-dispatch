"""Case data: a folder of CSV files plus case.json. See README for the schema."""
import os, json, numpy as np, pandas as pd

def num(v,d=0.):
    try: v=float(v)
    except (TypeError,ValueError): return d
    return d if v!=v else v

CAL=pd.date_range('2001-01-01',periods=8760,freq='h')  # non-leap reference calendar
DEFAULTS=dict(base_year=2026,discount_rate=0.08,voll_usd_mwh=1500.,ref_node=None,
              line_loss_frac=0.015,flow_cost_usd_mwh=0.01)

class Case:
    def __init__(s,path):
        s.path=path
        def r(f,req=True):
            p=os.path.join(path,f)
            if os.path.exists(p): return pd.read_csv(p)
            if req: raise FileNotFoundError(f'case is missing {f}')
            return None
        cfg=json.load(open(os.path.join(path,'case.json'))) if os.path.exists(os.path.join(path,'case.json')) else {}
        s.cfg={**DEFAULTS,**cfg}
        s.nodes=r('nodes.csv'); s.generators=r('generators.csv'); s.branches=r('branches.csv')
        s.profiles=r('profiles.csv')
        assert len(s.profiles)==8760, 'profiles.csv must have 8760 rows'
        if s.cfg['ref_node'] is None: s.cfg['ref_node']=int(s.nodes.node.iloc[0])
    def load(s,year,hours):
        """node x hour demand in MW (no demand growth in the core)."""
        sh=np.tile(s.profiles['load'].values[hours],(len(s.nodes),1))
        return s.nodes.peak_MW.values[:,None]*sh

def crf(r,n):
    return r*(1+r)**n/((1+r)**n-1)
