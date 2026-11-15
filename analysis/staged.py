# Backtest of entry plans after a deep drawdown signal: SOX >=28% off 52w high & below 200d (same de-clustered episodes)
import json, numpy as np, pandas as pd
from load import all_px, us_px
P=all_px(); d=P['SOX'].adj; d=d[d.index>='2000-01-01']
s200=d.rolling(200).mean(); s50=d.rolling(50).mean(); dd=d/d.rolling(252).max()-1
cond=(dd<=-0.28)&(d<s200)
ev=[];last=None
for t in d.index[cond.fillna(False).values]:
    if last is None or d.index.get_loc(t)-d.index.get_loc(last)>126: ev.append(t); last=t
H=252; rows=[]
for t in ev:
    i=d.index.get_loc(t)
    if i+H>=len(d): continue
    seg=d.iloc[i:i+H+1]; end=seg.iloc[-1]
    allin=end/seg.iloc[0]-1
    # wait for trend: buy at first close above 200d SMA within the 12m window, else stay cash
    above=(seg>s200.iloc[i:i+H+1])
    j=np.argmax(above.values[1:])+1 if above.values[1:].any() else None
    wait = end/seg.iloc[j]-1 if j else 0.0
    staged = (allin + 2*wait)/3   # 1/3 now, 2/3 on 200d reclaim
    worst_allin=(seg/seg.iloc[0]-1).min()
    worst_staged=min(0,(1/3)*worst_allin + (2/3)*((seg.iloc[j:]/seg.iloc[j]-1).min() if j else 0))
    rows.append(dict(date=t.strftime('%Y-%m-%d'),allin=round(allin,3),wait200=round(wait,3),staged=round(staged,3),
                     days_to_reclaim=int(j) if j else None, worstAllIn=round(worst_allin,3), worstStaged=round(worst_staged,3)))
df=pd.DataFrame(rows); print(df.to_string())
print(df[['allin','wait200','staged','worstAllIn','worstStaged']].agg(['mean','median','min','max']).round(3))
print('stdev', df[['allin','wait200','staged']].std().round(3).to_dict())
json.dump(rows,open('staged.json','w'))
print('SOX Nov5', P['SOX'].close.loc['2026-11-03':'2026-11-13'].round(0).to_dict())

# DCA over 4 tranches (0, 21, 42, 63 trading days), each held to t+252 from first tranche; and 50% now + 50% DCA
rows2=[]
for r_,t in zip(rows,[pd.Timestamp(x['date']) for x in rows]):
    i=d.index.get_loc(t); end=d.iloc[i+H]
    dca=np.mean([end/d.iloc[i+k]-1 for k in [0,21,42,63]])
    worst=np.mean([(d.iloc[i+k:i+H+1]/d.iloc[i+k]-1).min() for k in [0,21,42,63]])
    rows2.append(dict(date=r_['date'],dca4=round(dca,3),worstDca=round(worst,3)))
d2=pd.DataFrame(rows2); m=pd.DataFrame(rows).merge(d2,on='date')
print(m[['date','allin','dca4','staged','wait200']].to_string())
print(m[['allin','dca4','staged','wait200','worstAllIn','worstDca','worstStaged']].agg(['mean','median']).round(3))
print('hit>0', (m[['allin','dca4','staged','wait200']]>0).mean().round(2).to_dict())
json.dump(m.to_dict('records'),open('staged.json','w'))
