"""Thin sparse LP builder on top of HiGHS."""
import numpy as np, scipy.sparse as sp, highspy

class LP:
    """Collects variables, row bounds and coefficients, then solves with HiGHS."""
    def __init__(s):
        s.n=0; s.c=[]; s.lb=[]; s.ub=[]; s.m=0; s.rl=[]; s.ru=[]; s.I=[]; s.J=[]; s.V=[]
    def var(s,shape,cost=0.,lb=0.,ub=np.inf):
        k=int(np.prod(shape)); idx=np.arange(s.n,s.n+k).reshape(shape); s.n+=k
        for L,v in ((s.c,cost),(s.lb,lb),(s.ub,ub)): L.append(np.broadcast_to(np.asarray(v,float),shape).ravel())
        return idx
    def rows(s,shape,lo,hi):
        k=int(np.prod(shape)); idx=np.arange(s.m,s.m+k).reshape(shape); s.m+=k
        s.rl.append(np.broadcast_to(np.asarray(lo,float),shape).ravel()); s.ru.append(np.broadcast_to(np.asarray(hi,float),shape).ravel()); return idx
    def a(s,r,j,v=1.):
        r,j,v=np.broadcast_arrays(np.asarray(r),np.asarray(j),np.asarray(v,float)); s.I.append(r.ravel()); s.J.append(j.ravel()); s.V.append(v.ravel())
    def solve(s,method='ipm'):
        A=sp.csr_matrix((np.concatenate(s.V),(np.concatenate(s.I),np.concatenate(s.J))),shape=(s.m,s.n))
        lp=highspy.HighsLp(); lp.num_col_=s.n; lp.num_row_=s.m
        lp.col_cost_=np.concatenate(s.c); lp.col_lower_=np.concatenate(s.lb); lp.col_upper_=np.concatenate(s.ub)
        lp.row_lower_=np.concatenate(s.rl); lp.row_upper_=np.concatenate(s.ru)
        lp.a_matrix_.format_=highspy.MatrixFormat.kRowwise; lp.a_matrix_.start_=A.indptr; lp.a_matrix_.index_=A.indices; lp.a_matrix_.value_=A.data
        h=highspy.Highs(); h.setOptionValue('output_flag',False); h.setOptionValue('solver',method)
        h.setOptionValue('run_crossover','off' if method=='ipm' else 'on'); h.passModel(lp); h.run()
        if method=='ipm' and h.modelStatusToString(h.getModelStatus())!='Optimal':
            h.setOptionValue('run_crossover','on'); h.run()
        sol=h.getSolution()
        return h.modelStatusToString(h.getModelStatus()), np.array(sol.col_value), np.array(sol.row_dual)
