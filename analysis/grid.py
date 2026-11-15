import json, numpy as np, pandas as pd
from load import all_px, us_px
P=all_px(); px=us_px().ffill()
s=px['SOXX'].dropna(); ret=s.pct_change().fillna(0); spy=px['SPY'].reindex(s.index); tnx=px['TNX'].reindex(s.index)
s200=s.rolling(200).mean(); ext=s/s200-1
score=((s>s200).astype(int)+(s/s.shift(63)>1).astype(int)+((s/spy)>(s/spy).rolling(100).mean()).astype(int)
       +(ret.rolling(20).std()<1.5*ret.rolling(20).std().rolling(252).median()).astype(int)+((tnx-tnx.shift(63))<0.5).astype(int))
def strat(pct, ma, base):
    thr=ext.expanding(500).quantile(pct).shift(1); sma=s.rolling(ma).mean()
    crack=((ext>thr).rolling(30).max().astype(bool))&(s<sma)
    st=0; out=np.zeros(len(s))
    for i in range(len(s)):
        if crack.iloc[i]: st=1
        elif st==1 and score.iloc[i]==5 and s.iloc[i]>sma.iloc[i]: st=0
        out[i]=st
    if base=='trend': b=(s>s200).astype(float)
    elif base=='hold': b=pd.Series(1.0,index=s.index)
    else: b=pd.Series(np.select([score>=4,score==3],[1.0,.5],0.0),index=s.index)
    return b.where(out==0,0.0)
def perf(w,a,b=None):
    w=w.shift(1).fillna(0); r=w*ret-w.diff().abs().fillna(0)*0.0005; r=r[a:b] if b else r[a:]
    eq=(1+r).cumprod(); return float(eq.iloc[-1]-1), float((eq/eq.cummax()-1).min()), float(r.mean()*252/(r.std()*np.sqrt(252)))
rows=[]
for base in ['hold','trend','composite']:
  for pct in [0.90,0.95,0.975]:
    for ma in [20,50,100]:
        w=strat(pct,ma,base)
        x=w.shift(1)['2026']; exitd=x[(x.diff()<0)]
        t26,dd26,sh26=perf(w,'2026-01-01'); tf,ddf,shf=perf(w,'2002-07-01','2025-12-31')
        exits=[d.strftime('%m-%d') for d in exitd.index]
        rows.append(dict(base=base,pct=pct,ma=ma,ret26=round(t26,3),dd26=round(dd26,3),retFull=round(tf,2),ddFull=round(ddf,3),sharpeFull=round(shf,3),exits26=exits[:6]))
df=pd.DataFrame(rows); pd.set_option('display.width',250); print(df.to_string())
json.dump(rows,open('grid.json','w'))
