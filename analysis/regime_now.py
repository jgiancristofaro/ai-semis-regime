"""
Regime-model detail: each component's current value, its rule, whether it passes, the SOXX price that
would flip it on the next close (everything else held), and how those flip levels drift over the next
60 US trading days if SOXX, SPY and the 10y stay flat (the rolling windows keep moving).
"""
import json, numpy as np, pandas as pd
from load import us_px

px = us_px()
px = px[px.index <= px['SOXX'].last_valid_index()]
s, spy, tnx = px['SOXX'], px['SPY'], px['TNX']
ret = s.pct_change()
asof = s.index[-1]

# NYSE holidays in the projection window
HOL = pd.to_datetime([  # NYSE full-day holidays
    '2026-11-26', '2026-12-25',
    '2027-01-01', '2027-01-18', '2027-02-15', '2027-03-26', '2027-05-31', '2027-06-18', '2027-07-05', '2027-09-06', '2027-11-25', '2027-12-24',
    '2028-01-17', '2028-02-21', '2028-04-14', '2028-05-29', '2028-06-19', '2028-07-04', '2028-09-04', '2028-11-23', '2028-12-25'])
fut = [d for d in pd.bdate_range(asof + pd.Timedelta(days=1), periods=80) if d not in HOL][:60]

def components(S, SPY, TNX):
    s200 = S.rolling(200).mean(); r = S / SPY; rv = S.pct_change().rolling(20).std() * np.sqrt(252)
    return {
        'trend': S.iloc[-1] > s200.iloc[-1],
        'momentum': S.iloc[-1] > S.iloc[-64],
        'rel_strength': r.iloc[-1] > r.rolling(100).mean().iloc[-1],
        'calm_vol': rv.iloc[-1] < 1.5 * rv.rolling(252).median().iloc[-1],
        'rates_ok': (TNX.iloc[-1] - TNX.iloc[-64]) < 0.50,
    }

rv20 = ret.rolling(20).std() * np.sqrt(252)
rv_thr = 1.5 * rv20.rolling(252).median()
ratio = s / spy
now = {
    'asof': asof.strftime('%Y-%m-%d'),
    'soxx': float(s.iloc[-1]), 'spy': float(spy.iloc[-1]), 'tnx': float(tnx.iloc[-1]),
    'sma50': float(s.rolling(50).mean().iloc[-1]), 'sma200': float(s.rolling(200).mean().iloc[-1]),
    'anchor63': float(s.iloc[-64]), 'anchor63_date': s.index[-64].strftime('%Y-%m-%d'),
    'ret63': float(s.iloc[-1] / s.iloc[-64] - 1),
    'ratio': float(ratio.iloc[-1]), 'ratio_ma100': float(ratio.rolling(100).mean().iloc[-1]),
    'rv20': float(rv20.iloc[-1]), 'rv_thr': float(rv_thr.iloc[-1]),
    'tnx_anchor': float(tnx.iloc[-64]), 'dy63': float(tnx.iloc[-1] - tnx.iloc[-64]),
}
comp = components(s, spy, tnx)
now['components'] = {k: bool(v) for k, v in comp.items()}
now['score'] = int(sum(comp.values()))

# Exact next-close flip prices (holding SPY and the 10y flat)
c199 = s.iloc[-199:].sum(); c49 = s.iloc[-49:].sum(); r99 = ratio.iloc[-99:].sum()
now['need'] = {
    'trend': float(c199 / 199),                       # P > (sum of last 199 + P)/200
    'momentum': float(s.iloc[-63]),                   # tomorrow's 63-day-ago close
    'rel_strength': float(r99 / 99 * spy.iloc[-1]),   # P/SPY > (sum last 99 ratios + P/SPY)/100
    'sma50': float(c49 / 49),
}
now['need_tnx_max'] = float(tnx.iloc[-63] + 0.50)    # 10y must stay below this tomorrow

# Projection: flat SOXX/SPY/10y; volatility path assumes ordinary +/-2% days (about 32% annualized)
S, SP, T, V = s.copy(), spy.copy(), tnx.copy(), s.copy()
rows = []
for k, d in enumerate(fut):
    V = pd.concat([V, pd.Series([V.iloc[-1] * (1.02 if k % 2 == 0 else 1 / 1.02)], index=[d])])  # vol path only
    S = pd.concat([S, pd.Series([s.iloc[-1]], index=[d])])
    SP = pd.concat([SP, pd.Series([spy.iloc[-1]], index=[d])])
    T = pd.concat([T, pd.Series([tnx.iloc[-1]], index=[d])])
    R = S / SP
    rvv = V.pct_change().rolling(20).std().iloc[-1] * np.sqrt(252)
    rows.append({
        'date': d.strftime('%Y-%m-%d'),
        'trend': float(S.iloc[-200:-1].sum() / 199),
        'momentum': float(S.iloc[-64]),
        'rel_strength': float(R.iloc[-100:-1].sum() / 99 * spy.iloc[-1]),
        'sma50': float(S.iloc[-50:-1].sum() / 49),
        'tnx_max': float(T.iloc[-64] + 0.50),
        'sma50_val': float(S.rolling(50).mean().iloc[-1]), 'sma200_val': float(S.rolling(200).mean().iloc[-1]),
        'rv_path': float(rvv),
    })
proj = pd.DataFrame(rows)
# Date the 20-day vol window clears the Nov spike under ordinary +/-2% days (threshold held at today's value)
ok = proj[proj.rv_path < now['rv_thr']]
now['vol_clear_date'] = ok.date.iloc[0] if len(ok) else None
dc = proj[proj.sma50_val < proj.sma200_val]
now['death_cross_flat'] = dc.date.iloc[0] if len(dc) else None
now['proj'] = {c: [round(v, 2) if isinstance(v, float) else v for v in proj[c]] for c in proj.columns}
# Recent history of the score for context
hist = []
for i in range(len(s) - 260, len(s)):
    c = components(s.iloc[:i + 1], spy.iloc[:i + 1], tnx.iloc[:i + 1]); hist.append(int(sum(c.values())))
now['score_hist'] = {'dates': [d.strftime('%Y-%m-%d') for d in s.index[-260:]], 'score': hist}
json.dump(now, open('regime_now.json', 'w'))
print(json.dumps({k: v for k, v in now.items() if k not in ('proj', 'score_hist')}, indent=1, default=str))
p = proj.set_index('date')[['trend', 'momentum', 'rel_strength', 'sma50', 'tnx_max', 'rv_path']]
print(p.iloc[[0, 4, 9, 14, 19, 29, 39, 49, 59]].round(2))
