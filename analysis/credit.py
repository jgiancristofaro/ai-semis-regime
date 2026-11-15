"""
Candidate 6th regime signal: broad credit stress (FRED Baa corporate minus 10y Treasury spread, daily since 1986).
Tested three ways against the 5-factor regime composite, on SOXX, 2002-2025 and 2026, with no tuning on 2026:
  A) Baseline 5-factor composite (4-5 full, 3 half, 0-2 flat)
  B) Credit veto overlay: halve the composite position when credit is stressed
  C) 6-factor composite: credit as an extra vote (5-6 full, 4 half, 0-3 flat)
"Stressed" = Baa-10y spread up more than X pt over 63 sessions; X in {0.30, 0.50} (0.50 mirrors the rates rule).
Also reports the current state of the broader credit/conditions dashboard (HY OAS, NFCI, real yield).
"""
import json, numpy as np, pandas as pd
from load import us_px, fred

px = us_px(); px = px[px.index >= '2001-07-13']
px = px[px.index <= px['SOXX'].last_valid_index()]
s, spy, tnx = px['SOXX'], px['SPY'], px['TNX']
ret = s.pct_change().fillna(0)
baa = fred('BAA10Y').reindex(px.index).ffill()
COST = 0.0005

s200 = s.rolling(200).mean()
comp = pd.DataFrame({
    'trend': s > s200, 'momentum': s / s.shift(63) > 1,
    'rel_strength': (s / spy) > (s / spy).rolling(100).mean(),
    'calm_vol': ret.rolling(20).std() < 1.5 * ret.rolling(20).std().rolling(252).median(),
    'rates_ok': (tnx - tnx.shift(63)) < 0.50}).astype(int)
score5 = comp.sum(axis=1)
w_base = pd.Series(np.select([score5 >= 4, score5 == 3], [1.0, 0.5], 0.0), index=s.index)

def run(w, a, b=None):
    w = w.shift(1).fillna(0); r = w * ret - w.diff().abs().fillna(0) * COST
    r = r[a:b] if b else r[a:]
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    return dict(total=float(eq.iloc[-1] - 1), cagr=float(eq.iloc[-1] ** (1 / yrs) - 1),
                sharpe=float(r.mean() * 252 / (r.std() * np.sqrt(252))), maxdd=float((eq / eq.cummax() - 1).min()),
                time_in=float((w[r.index] > 0).mean()))

windows = {'2026 YTD': ('2026-01-01', None), '2002-2025': ('2002-07-01', '2025-12-31'),
           '2007-2009 (GFC)': ('2007-01-01', '2009-12-31'), '2020-2025': ('2020-01-01', '2025-12-31')}
res = {'Baseline (5 signals)': {k: run(w_base, *v) for k, v in windows.items()}}
dbaa = baa - baa.shift(63)
for X in (0.30, 0.50):
    stressed = dbaa > X
    w_veto = w_base.where(~stressed, w_base * 0.5)
    sc6 = score5 + (~stressed).astype(int)
    w6 = pd.Series(np.select([sc6 >= 5, sc6 == 4], [1.0, 0.5], 0.0), index=s.index)
    res[f'Credit veto (+{X:.2f}pt)'] = {k: run(w_veto, *v) for k, v in windows.items()}
    res[f'6 signals (+{X:.2f}pt)'] = {k: run(w6, *v) for k, v in windows.items()}
res['Buy & hold'] = {k: run(pd.Series(1.0, index=s.index), *v) for k, v in windows.items()}

# Share of days credit was "stressed" in 2026, and when
st50 = (dbaa > 0.50)['2026']; st30 = (dbaa > 0.30)['2026']

# Dashboard: current readings and 2026 series
hy = fred('BAMLH0A0HYM2'); nfci = fred('NFCI'); real = fred('DFII10'); baa_raw = fred('BAA10Y')
def pctile(x, v): return float((x < v).mean())
dash = {
    'baa': {'now': float(baa_raw.iloc[-1]), 'date': baa_raw.index[-1].strftime('%Y-%m-%d'),
            'chg63': float(dbaa.dropna().iloc[-1]), 'pctile_since_1986': pctile(baa_raw, baa_raw.iloc[-1]),
            'min26': float(baa_raw['2026'].min()), 'max26': float(baa_raw['2026'].max())},
    'hy': {'now': float(hy.iloc[-1]), 'date': hy.index[-1].strftime('%Y-%m-%d'), 'chg63': float(hy.iloc[-1] - hy.iloc[-64]),
           'min26': float(hy['2026'].min()), 'max26': float(hy['2026'].max())},
    'nfci': {'now': float(nfci.iloc[-1]), 'date': nfci.index[-1].strftime('%Y-%m-%d')},
    'real10': {'now': float(real.iloc[-1]), 'date': real.index[-1].strftime('%Y-%m-%d'), 'chg63': float(real.iloc[-1] - real.iloc[-64])},
    'stressed_days_2026': {'gt050': int(st50.sum()), 'gt030': int(st30.sum()), 'days': int(len(st50))},
    'credit_ok_now': bool(dbaa.iloc[-1] <= 0.50), 'dbaa63_now': float(dbaa.iloc[-1]),
}
ser = pd.DataFrame({'baa': baa_raw, 'hy': hy}).loc['2025-10-01':].ffill().dropna(subset=['baa'])
out = {'results': res, 'dash': dash,
       'series': {'dates': [d.strftime('%Y-%m-%d') for d in ser.index], 'baa': [round(float(v), 3) for v in ser.baa],
                  'hy': [None if pd.isna(v) else round(float(v), 3) for v in ser.hy]}}
json.dump(out, open('credit.json', 'w'))

pd.set_option('display.width', 200)
for wn in windows:
    print('\n==', wn); print(pd.DataFrame({k: v[wn] for k, v in res.items()}).T.round(3))
print('\nDashboard:', json.dumps(dash, indent=1))
