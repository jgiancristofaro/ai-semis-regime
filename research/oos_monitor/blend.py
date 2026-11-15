"""Blend test: the SOXX Regime Monitor (US-session flow) vs. this repo's regime models, alone and combined.
Common window: Jan 20 - Dec 31 each year (the monitor's warm-up), positions applied with the monitor's convention.
Run oos_monitor.py first."""
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..', '..', 'analysis'))
from load import us_px
px = us_px(); px = px[px.index <= px['SOXX'].last_valid_index()]
s, spy, tnx = px['SOXX'], px['SPY'], px['TNX']; ret = s.pct_change().fillna(0)
s200, s50 = s.rolling(200).mean(), s.rolling(50).mean()
comp = pd.DataFrame({'trend': s > s200, 'mom': s / s.shift(63) > 1, 'rs': (s / spy) > (s / spy).rolling(100).mean(),
                     'vol': ret.rolling(20).std() < 1.5 * ret.rolling(20).std().rolling(252).median(),
                     'rates': (tnx - tnx.shift(63)) < 0.5}).astype(int).sum(axis=1)
W = {'Regime composite': pd.Series(np.select([comp >= 4, comp == 3], [1.0, .5], 0.0), index=s.index),
     '50/200 cross': (s50 > s200).astype(float), 'Trend 200d': (s > s200).astype(float)}
mon = pd.read_csv(os.path.join(HERE, 'monitor_positions.csv'), index_col=0, parse_dates=True)['pos']
idx = mon.index.intersection(s.index)
# My models: signal at close t applies to t+1 (shift). Monitor positions are already the held position for day t.
P = {k: v.shift(1).reindex(idx) for k, v in W.items()}
P['Monitor'] = mon.reindex(idx)
P['Buy & hold'] = pd.Series(1.0, index=idx)
P['Monitor + composite (avg)'] = (P['Monitor'] + P['Regime composite']) / 2
P['Monitor + 50/200 (avg)'] = (P['Monitor'] + P['50/200 cross']) / 2
P['Monitor AND composite>=3'] = P['Monitor'].where(P['Regime composite'] > 0, 0.0)
r = ret.reindex(idx)
def st(w, a, b):
    x = (w * r - w.diff().abs().fillna(0) * 0.0005)[a:b]; eq = (1 + x).cumprod(); n = len(x) / 252
    return dict(cagr=eq.iloc[-1] ** (1 / n) - 1, sharpe=x.mean() * 252 / (x.std() * np.sqrt(252)), maxdd=(eq / eq.cummax() - 1).min(), expo=w[a:b].mean())
rows = {}
for k, w in P.items():
    rows[k] = {f'{lab} {m}': v for lab, (a, b) in {'02-25': ('2002', '2025'), '02-09': ('2002', '2009'), '10-25': ('2010', '2025'), '2026': ('2026', '2026')}.items()
               for m, v in st(w, a, b).items() if m in ('cagr', 'sharpe', 'maxdd')}
T = pd.DataFrame(rows).T
pd.set_option('display.width', 250); print(T.round(3).to_string())
json.dump({'table': T.round(4).reset_index().rename(columns={'index': 'strategy'}).to_dict('records')}, open(os.path.join(HERE, 'blend_results.json'), 'w'), indent=1)
