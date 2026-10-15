"""Command line: python -m gridloom_dispatch CASE_DIR OUT_DIR --year Y [--hours START END]"""
import argparse, os
from . import Case, dispatch

def main():
    a=argparse.ArgumentParser(prog='gridloom-dispatch')
    a.add_argument('case'); a.add_argument('out'); a.add_argument('--year',type=int,required=True)
    a.add_argument('--hours',type=int,nargs=2,metavar=('START','END'),help='inclusive hour-of-year range (default 0 167)')
    A=a.parse_args(); C=Case(A.case); os.makedirs(A.out,exist_ok=True)
    H=None if A.hours is None else range(A.hours[0],A.hours[1]+1)
    r=dispatch(C,A.year,H)
    r['price'].round(2).to_csv(os.path.join(A.out,f'prices_hourly_{A.year}.csv'),index=False)
    r['gen'].groupby(['name','node','type']).MWh.sum().round(0).reset_index().to_csv(os.path.join(A.out,f'generation_{A.year}.csv'),index=False)
    r['use'].round(0).to_csv(os.path.join(A.out,f'unserved_{A.year}.csv'),index=False)
    r['flows'].round(0).to_csv(os.path.join(A.out,f'flows_{A.year}.csv'),index=False)
    print('done')

if __name__=='__main__':
    main()
