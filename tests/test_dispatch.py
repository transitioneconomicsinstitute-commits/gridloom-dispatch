import os, numpy as np, pytest
import gridloom_dispatch as P
CASE=os.path.join(os.path.dirname(__file__),'..','examples','synthetic_4node')

@pytest.fixture(scope='module')
def case(): return P.Case(CASE)

def test_inputs(case):
    assert len(case.profiles)==8760 and abs(case.profiles.load.max()-1)<1e-9

def test_dispatch_balance(case):
    m=P.solve(P.build(case,np.arange(48),year=2026))
    assert m['status']=='Optimal'
    x=m['x']; gen=sum(x[g].sum() for u,g in m['units'])
    assert gen+x[m['use']].sum()>=m['L'].sum()*0.999
    r=P.extract(m); assert r['price'].shape==(48,5) and (r['price'].drop(columns='hour').values>0).all()

def test_merit_order(case):
    r=P.dispatch(case,2026,range(24),log=lambda s:None)
    g=r['gen'].set_index('name').MWh
    assert g['Gas CC A']>g['Oil engines C']

def test_case_files_are_synthetic():
    import json
    assert 'SYNTHETIC' in json.load(open(os.path.join(CASE,'case.json')))['description']

def test_demand_growth(case):
    g=case.cfg['demand_growth']; assert g>0
    np.testing.assert_allclose(case.peaks(case.cfg['base_year']),case.nodes.peak_MW.values)
    np.testing.assert_allclose(case.peaks(2030),case.nodes.peak_MW.values*(1+g)**4)
    h=np.arange(24)
    np.testing.assert_allclose(case.load(2028,h),case.load(2026,h)*(1+g)**2)
