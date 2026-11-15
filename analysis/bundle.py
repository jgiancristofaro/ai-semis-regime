"""Collect every analysis output into data.js (one `const D=...`) for the page."""
import json, pandas as pd, numpy as np
from load import us_px
bt=json.load(open('bt.json')); dp=json.load(open('deeper.json')); grid=json.load(open('grid.json'))
st=json.load(open('staged.json')); rn=json.load(open('regime_now.json'))
keep=['Buy & Hold','Trend 200d','50/200 Cross','Regime Composite','Composite + Blow-off Exit']

# ---- live "as of" figures used throughout the page ----
px=us_px(); px=px[px.index<=px['SOXX'].last_valid_index()]
s=px['SOXX']; y0=s[:str(s.index[-1].year-1)+'-12-31'].iloc[-1]; ys=s[str(s.index[-1].year):]
names={'NVDA':'NVDA','TSM':'TSM','AVGO':'AVGO','AMD':'AMD','MU':'MU','ASML':'ASML','000660.KS':'SK hynix','005930.KS':'Samsung'}
above=[lab for k,lab in names.items() if px[k].iloc[-1]>px[k].rolling(200).mean().iloc[-1]]
m=px['SOX'].resample('ME').last(); slow=m.iloc[-1]/m.iloc[-13]-1; fast=m.iloc[-1]/m.iloc[-2]-1
state=('Bull' if fast>0 else 'Correction') if slow>0 else ('Rebound' if fast>0 else 'Bear')
s26=bt['stats']
live=dict(rn, **{
 'ytd':float(s.iloc[-1]/y0-1),'peak':float(ys.max()),'peak_date':ys.idxmax().strftime('%Y-%m-%d'),
 'dd':float(s.iloc[-1]/ys.max()-1),'mom12_1':float(s.iloc[-22]/s.iloc[-253]-1),'mom3':float(s.iloc[-1]/s.iloc[-64]-1),
 'breadth_n':len(above),'breadth_names':above,'state':state,
 'ext_peak':bt['ext_peak2026'],'ext_peak_date':bt['ext_peak2026_date'],'ext_prior_max':max(v for k,v in bt['ext_hist_max'].items() if k!='2026'),
 'bh26':s26['Buy & Hold']['2026 YTD'],'bo26':s26['Composite + Blow-off Exit']['2026 YTD'],
 'bo_exit':[t for t in bt['transitions']['Composite + Blow-off Exit'] if t[1]==0][-1][0],
 'grid_min':min(g['ret26'] for g in grid),'grid_max':max(g['ret26'] for g in grid),'grid_beat':sum(g['ret26']>s26['Buy & Hold']['2026 YTD']['total'] for g in grid),
})
live.pop('score_hist',None)
import datetime
live['built']=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
# credit check + SOXX shares-outstanding snapshots (flows build up over time)
cr=json.load(open('credit.json'))
import csv, os
flows=[]
sp=os.path.join('..','research','snapshots','soxx_shares_outstanding.csv')
if os.path.exists(sp):
    rows=[r for r in csv.DictReader(open(sp))]
    for r in rows: r['d']=pd.to_datetime(r['as_of']).strftime('%Y-%m-%d')
    for a_,b_ in zip(rows,rows[1:]):
        px_b=float(s[:b_['d']].iloc[-1]) if len(s[:b_['d']]) else float('nan')
        flows.append({'date':b_['d'],'shares':int(b_['shares_outstanding']),'flow_usd':(int(b_['shares_outstanding'])-int(a_['shares_outstanding']))*px_b})
    live['shares_out']=int(rows[-1]['shares_outstanding']); live['shares_asof']=rows[-1]['d']; live['shares_since']=rows[0]['d']; live['flow_days']=len(flows)
    live['flow_5d']=sum(f['flow_usd'] for f in flows[-5:]) if flows else None
live['credit']=cr['dash']
# Finnhub estimate snapshots: latest table + daily aggregates (revision history builds up over time)
ep=os.path.join('..','research','snapshots','estimates.csv')
est=None
if os.path.exists(ep):
    E=pd.read_csv(ep); E=E[E.forward_pe>0]
    hist=[]
    for d_,g in E.groupby('date'):
        g=g.dropna(subset=['market_cap_musd','fwd_earnings_musd'])
        b=(g.strong_buy+g.buy).sum(); n=(g.strong_buy+g.buy+g.hold+g.sell+g.strong_sell).sum()
        hist.append({'date':d_,'pe_cw':float(g.market_cap_musd.sum()/g.fwd_earnings_musd.sum()),'pe_med':float(g.forward_pe.median()),
                     'fwd_earn_busd':float(g.fwd_earnings_musd.sum()/1e3),'buy_share':float(b/n) if n else None,'n':int(len(g))})
    last=E[E.date==E.date.max()].sort_values('market_cap_musd',ascending=False)
    names=[{'s':r.symbol,'fpe':float(r.forward_pe),'mcap_b':float(r.market_cap_musd/1e3),
            'buy':float((r.strong_buy+r.buy)/max(1,(r.strong_buy+r.buy+r.hold+r.sell+r.strong_sell))),
            'surp':None if pd.isna(r.surprise_pct) else float(r.surprise_pct),'lastq':r.last_q} for r in last.itertuples()]
    est={'hist':hist,'names':names}
    h0,h1=hist[0],hist[-1]
    live['est']={'pe_cw':h1['pe_cw'],'pe_med':h1['pe_med'],'fwd_earn_busd':h1['fwd_earn_busd'],'buy_share':h1['buy_share'],'date':h1['date'],
                 'since':h0['date'],'days':len(hist),'earn_chg':h1['fwd_earn_busd']/h0['fwd_earn_busd']-1}
# SEC capex
cp=os.path.join('..','research','snapshots','capex.json')
capex=json.load(open(cp)) if os.path.exists(cp) else None
if capex and capex.get('aggregate'):
    a_=capex['aggregate'][-1]; live['capex']={'q':a_['q'],'total':a_['total_busd'],'yoy':a_['yoy'],'asof':capex['asof']}
D={
 'live':live,'est':est,'capex':capex,'credit':{'results':cr['results'],'series':cr['series']},'flows':flows,'scoreHist':rn['score_hist'],
 'd26':bt['dates2026'],'c26':{k:bt['curves2026'][k] for k in keep},'pos26':{k:bt['positions2026'][k] for k in keep},
 'stats':{k:bt['stats'][k] for k in keep},
 'ind':{k:bt['ind'][k] for k in ['soxx','sma50','sma200','ext200','ext_thr','score']},'comp':bt['components_hist'],
 'norm':dp['norm'],'macro':dp['macro'],'breadth':dp['breadth'],'states':dp['mom_states_table'],'sens':dp['macro_sens'],
 'grid':grid,'staged':st,
}
open('data.js','w').write('const D='+json.dumps(D,separators=(',',':'),default=float)+';')
print('live keys ok; score',live['score'],'breadth',above,'state',state,'bo exit',live['bo_exit'],'ytd',round(live['ytd'],3))
