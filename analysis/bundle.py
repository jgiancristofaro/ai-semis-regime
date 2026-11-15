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
D={
 'live':live,'scoreHist':rn['score_hist'],
 'd26':bt['dates2026'],'c26':{k:bt['curves2026'][k] for k in keep},'pos26':{k:bt['positions2026'][k] for k in keep},
 'stats':{k:bt['stats'][k] for k in keep},
 'ind':{k:bt['ind'][k] for k in ['soxx','sma50','sma200','ext200','ext_thr','score']},'comp':bt['components_hist'],
 'norm':dp['norm'],'macro':dp['macro'],'breadth':dp['breadth'],'states':dp['mom_states_table'],'sens':dp['macro_sens'],
 'grid':grid,'staged':st,
}
open('data.js','w').write('const D='+json.dumps(D,separators=(',',':'),default=float)+';')
print('live keys ok; score',live['score'],'breadth',above,'state',state,'bo exit',live['bo_exit'],'ytd',round(live['ytd'],3))
