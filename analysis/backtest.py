"""
Backtest of pre-specified, standard regime/momentum signals on SOXX.
Rules: signal computed on close t, position taken at close t+1 (1-day lag, no look-ahead).
Cash earns 0% (conservative). Transaction cost 5 bp per side.
Parameters are textbook defaults, NOT tuned on 2026.
"""
import json, numpy as np, pandas as pd
from load import all_px, us_px

P = all_px()
px = us_px()
px = px[px.index >= '2001-07-13'].ffill()
s = px['SOXX']; spy = px['SPY']; tnx = px['TNX']; oil = px['CLF']; kospi = px['KS11']
ret = s.pct_change().fillna(0)
COST = 0.0005

def rsi(x, n=14):
    d = x.diff(); up = d.clip(lower=0).ewm(alpha=1/n).mean(); dn = (-d.clip(upper=0)).ewm(alpha=1/n).mean()
    return 100 - 100/(1+up/dn)

sma50, sma200, sma20 = s.rolling(50).mean(), s.rolling(200).mean(), s.rolling(20).mean()
ext200 = s/sma200 - 1
mom63 = s/s.shift(63) - 1
mom252_21 = s.shift(21)/s.shift(252) - 1
rs = s/spy; rs_ma = rs.rolling(100).mean()
rv20 = ret.rolling(20).std()*np.sqrt(252)
rv_med = rv20.rolling(252).median()
dy63 = (tnx - tnx.shift(63))  # 10y yield change, pct points
oil63 = oil/oil.shift(63) - 1
R = rsi(s)

sig = {}
# S1: price above 200d SMA
sig['Trend 200d'] = (s > sma200).astype(float)
# S2: golden/death cross
sig['50/200 Cross'] = (sma50 > sma200).astype(float)
# S3: dual momentum, monthly rebalance (12-1m abs > 0 and > SPY 12-1m)
spy_m = spy.shift(21)/spy.shift(252) - 1
dm = ((mom252_21 > 0) & (mom252_21 > spy_m)).astype(float)
month_end = s.index.to_series().groupby(s.index.to_period('M')).transform('max') == s.index.to_series()
sig['Dual Momentum (monthly)'] = dm.where(month_end).ffill().fillna(0)

# S4: Regime composite (5 standard components)
comp = pd.DataFrame({
    'trend': s > sma200,
    'momentum': mom63 > 0,
    'rel_strength': rs > rs_ma,
    'calm_vol': rv20 < 1.5*rv_med,
    'rates_ok': dy63 < 0.50,
}).astype(float)
score = comp.sum(axis=1)
sig['Regime Composite'] = np.select([score >= 4, score == 3], [1.0, 0.5], 0.0)
sig['Regime Composite'] = pd.Series(sig['Regime Composite'], index=s.index)

# S5: Composite + blow-off overlay.
# Overextension threshold = expanding 95th pct of ext200 using only past data.
ext_thr = ext200.expanding(500).quantile(0.95).shift(1)
was_extended = (ext200 > ext_thr).rolling(30).max().astype(bool)
crack = (s < sma50) & was_extended       # extended in last 30d, then loses 50d SMA -> blow-off top
# Once triggered, stay de-risked until full composite (score==5) re-confirms
blow = pd.Series(0.0, index=s.index); state = 0
for i, d in enumerate(s.index):
    if crack.iloc[i]: state = 1
    elif state == 1 and score.iloc[i] == 5 and s.iloc[i] > sma50.iloc[i]: state = 0
    blow.iloc[i] = state
sig['Composite + Blow-off Exit'] = sig['Regime Composite'].where(blow == 0, 0.0)

sig['Buy & Hold'] = pd.Series(1.0, index=s.index)

def run(w, start=None, end=None):
    w = w.shift(1).fillna(0)  # trade next day
    r = w*ret - w.diff().abs().fillna(0)*COST
    if start: r = r[r.index >= start]
    if end: r = r[r.index <= end]
    eq = (1+r).cumprod()
    yrs = len(r)/252
    cagr = eq.iloc[-1]**(1/yrs) - 1 if yrs > 0 else np.nan
    vol = r.std()*np.sqrt(252)
    sh = r.mean()*252/vol if vol > 0 else np.nan
    dd = (eq/eq.cummax()-1).min()
    trades = (w.diff().abs() > 0)[r.index].sum()
    tim = (w[r.index] > 0).mean()
    return eq, dict(total=eq.iloc[-1]-1, cagr=cagr, vol=vol, sharpe=sh, maxdd=dd, trades=int(trades), time_in=tim)

out = {'stats': {}, 'curves2026': {}, 'curvesFull': {}}
windows = {
    '2026 YTD': ('2026-01-01', None),
    'Full 2002-2025 (out-of-sample)': ('2002-07-01', '2025-12-31'),
    '2000s bust 2002-2009': ('2002-07-01', '2009-12-31'),
    '2010-2019': ('2010-01-01', '2019-12-31'),
    '2020-2025': ('2020-01-01', '2025-12-31'),
}
for name, w in sig.items():
    out['stats'][name] = {}
    for wn, (a, b) in windows.items():
        eq, st = run(w, a, b)
        out['stats'][name][wn] = {k: (round(float(v), 4) if isinstance(v, (float, np.floating)) else v) for k, v in st.items()}
    eq, _ = run(w, '2025-10-01')
    out['curves2026'][name] = [round(float(x), 4) for x in eq.values]
    eq, _ = run(w, '2002-07-01')
    out['curvesFull'][name] = [round(float(x), 3) for x in eq.resample('W').last().values]
out['dates2026'] = [d.strftime('%Y-%m-%d') for d in s[s.index >= '2025-10-01'].index]
out['datesFull'] = [d.strftime('%Y-%m-%d') for d in s[s.index >= '2002-07-01'].resample('W').last().index]

# Position paths in 2026 + key transitions
pos = pd.DataFrame({k: v.shift(1) for k, v in sig.items()})
p26 = pos[pos.index >= '2025-10-01']
out['positions2026'] = {k: [float(x) for x in p26[k].values] for k in sig}
trans = {}
for k in sig:
    x = pos[k][pos.index >= '2025-11-01']; ch = x[x.diff() != 0].iloc[1:]
    trans[k] = [(d.strftime('%Y-%m-%d'), float(v)) for d, v in ch.items()]
out['transitions'] = trans

# Indicator panel (2025-10 onward)
ind = pd.DataFrame({'soxx': s, 'sma50': sma50, 'sma200': sma200, 'ext200': ext200, 'ext_thr': ext_thr,
                    'rsi': R, 'score': score, 'rs': rs/rs.loc['2025-12-31'], 'rv20': rv20, 'dy63': dy63,
                    'tnx': tnx, 'oil': oil, 'kospi': kospi, 'mom63': mom63, 'mom12_1': mom252_21})
i26 = ind[ind.index >= '2025-10-01']
out['ind'] = {c: [None if pd.isna(v) else round(float(v), 4) for v in i26[c].values] for c in i26}
out['components_now'] = {c: bool(comp[c].iloc[-1]) for c in comp}
out['components_hist'] = {c: [int(v) for v in comp[c][comp.index >= '2025-10-01'].values] for c in comp}
out['score_now'] = float(score.iloc[-1])
out['ext_now'] = float(ext200.iloc[-1]); out['ext_thr_now'] = float(ext_thr.iloc[-1])
out['ext_peak2026'] = float(ext200['2026'].max()); out['ext_peak2026_date'] = ext200['2026'].idxmax().strftime('%Y-%m-%d')
out['ext_hist_max'] = {str(y): round(float(ext200[str(y)].max()), 3) for y in [2000, 2003, 2009, 2010, 2013, 2017, 2020, 2021, 2023, 2024, 2025, 2026] if str(y) in ext200.index.year.astype(str)}
json.dump(out, open('bt.json', 'w'))

pd.set_option('display.width', 200)
for wn in windows:
    print('\n==', wn)
    print(pd.DataFrame({k: v[wn] for k, v in out['stats'].items()}).T[['total', 'cagr', 'sharpe', 'maxdd', 'trades', 'time_in']].round(3))
print('\nTransitions since Nov-2025:')
for k, v in trans.items(): print(k, v)
print('\nNow: score', out['score_now'], out['components_now'], 'ext200', round(out['ext_now'], 3), 'thr', round(out['ext_thr_now'], 3))
print('2026 ext peak', out['ext_peak2026'], out['ext_peak2026_date'], out['ext_hist_max'])
