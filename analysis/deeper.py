import json, numpy as np, pandas as pd
from load import all_px, us_px
P = all_px()
px = us_px().ffill()
sox = px['SOX'][px.index >= '2000-01-01']  # longer history incl. 2000
s = px['SOXX'].dropna()
out = {}

# ---------- 1. Momentum turning-point states (Goulding, Harvey & Mazzoleni 2023) on SOX, monthly ----------
m = sox.resample('ME').last()
slow = m/m.shift(12) - 1; fast = m/m.shift(1) - 1
state = np.select([(slow > 0) & (fast > 0), (slow > 0) & (fast <= 0), (slow <= 0) & (fast <= 0), (slow <= 0) & (fast > 0)],
                  ['Bull', 'Correction', 'Bear', 'Rebound'], None)
st = pd.Series(state, index=m.index)
fwd1 = m.shift(-1)/m - 1; fwd3 = m.shift(-3)/m - 1; fwd6 = m.shift(-6)/m - 1; fwd12 = m.shift(-12)/m - 1
df = pd.DataFrame({'state': st, 'f1': fwd1, 'f3': fwd3, 'f6': fwd6, 'f12': fwd12}).dropna(subset=['state'])
pre = df[df.index < '2026-01-01']
tab = pre.groupby('state').agg(n=('f1', 'size'), f1=('f1', 'mean'), f3=('f3', 'mean'), f6=('f6', 'mean'), f12=('f12', 'mean'),
                               hit3=('f3', lambda x: (x > 0).mean()), hit12=('f12', lambda x: (x > 0).mean()))
print('Momentum states on SOX, 2001-2025 monthly:\n', tab.round(3))
out['mom_states_table'] = tab.round(4).reset_index().to_dict('records')
out['mom_states_2026'] = [(d.strftime('%Y-%m'), s_) for d, s_ in st['2025-07':].items()]
print(out['mom_states_2026'])

# ---------- 2. Conditional forward returns: SOX >= 30% below 52w high AND below 200d, with 12m mom still positive ----------
d = sox
dd = d/d.rolling(252).max() - 1
sma200 = d.rolling(200).mean()
mom12 = d/d.shift(252) - 1
fwd = {h: d.shift(-h)/d - 1 for h in [63, 126, 252]}
cond = (dd <= -0.28) & (d < sma200)
# de-cluster: first signal day per 63 trading days
ev = []; last = None
for t in d.index[cond.fillna(False).values]:
    if last is None or (d.index.get_loc(t) - d.index.get_loc(last)) > 126:
        ev.append(t); last = t
rows = []
for t in ev:
    rows.append({'date': t.strftime('%Y-%m-%d'), 'dd': round(float(dd[t]), 3), 'mom12': round(float(mom12[t]), 3),
                 'f3m': None if pd.isna(fwd[63][t]) else round(float(fwd[63][t]), 3),
                 'f6m': None if pd.isna(fwd[126][t]) else round(float(fwd[126][t]), 3),
                 'f12m': None if pd.isna(fwd[252][t]) else round(float(fwd[252][t]), 3)})
ev_df = pd.DataFrame(rows); print('\nEpisodes SOX >=28% off 52w high & <200d:\n', ev_df)
out['dd_episodes'] = rows
# all days version (unconditional vs conditional)
allf = pd.DataFrame({k: v for k, v in fwd.items()})
c_all = allf[cond & (d.index < '2025-11-01')].mean(); u_all = allf[d.index < '2025-11-01'].mean()
c_hit = (allf[cond & (d.index < '2025-11-01')] > 0).mean()
print('cond mean fwd', c_all.round(3).to_dict(), 'hit', c_hit.round(3).to_dict(), 'uncond', u_all.round(3).to_dict())
out['cond_fwd'] = {'cond_mean': c_all.round(4).to_dict(), 'cond_hit': c_hit.round(4).to_dict(), 'uncond_mean': u_all.round(4).to_dict()}

# ---------- 3. Post blow-off analogs: max extension above 200d and what followed ----------
ext = d/sma200 - 1
peaks = []
for y in range(2000, 2027):
    e = ext[str(y)]
    if len(e) and e.max() > 0.30:
        t = e.idxmax()
        nxt = d[t:]
        trough = nxt[:t + pd.Timedelta(days=550)].min()
        peaks.append({'year': y, 'date': t.strftime('%Y-%m-%d'), 'ext': round(float(e.max()), 3),
                      'max_dd_next_18m': round(float(trough/d[t] - 1), 3),
                      'ret_12m': None if t + pd.Timedelta(days=365) > d.index[-1] else round(float(d[d.index >= t + pd.Timedelta(days=365)].iloc[0]/d[t] - 1), 3)})
print('\nBlow-off analogs:\n', pd.DataFrame(peaks))
out['blowoffs'] = peaks

# ---------- 4. Macro sensitivity: daily SOXX returns vs 10y yield change & oil, H1 vs H2 2026 ----------
r = px[['SOXX', 'TNX', 'CLF', 'KS11', 'SPY']].copy()
dr = pd.DataFrame({'soxx': r.SOXX.pct_change(), 'dy': r.TNX.diff(), 'oil': r.CLF.pct_change(), 'kospi': r.KS11.pct_change(),
                   'spy': r.SPY.pct_change()}).dropna()
dr = dr[np.isfinite(dr).all(1)]
def beta(df, y, xs):
    X = np.column_stack([np.ones(len(df))] + [df[x].values for x in xs]); b = np.linalg.lstsq(X, df[y].values, rcond=None)[0]
    return dict(zip(['a'] + xs, b))
sens = {}
for lab, a, b in [('2025', '2025-01-01', '2025-12-31'), ('H1 2026', '2026-01-01', '2026-06-22'), ('H2 2026', '2026-06-23', '2026-12-31')]:
    x = dr[a:b]
    sens[lab] = {'corr_dy': round(float(x.soxx.corr(x.dy)), 3), 'corr_oil': round(float(x.soxx.corr(x.oil)), 3),
                 'corr_kospi_prev': round(float(x.soxx.corr(x.kospi)), 3),
                 'beta_spy': round(float(beta(x, 'soxx', ['spy'])['spy']), 2),
                 'beta_dy_per100bp': round(float(beta(x, 'soxx', ['spy', 'dy'])['dy']), 3)}
print('\nMacro sensitivity:', json.dumps(sens, indent=1))
out['macro_sens'] = sens
# rolling 63d corr soxx vs dy
rc = dr.soxx.rolling(63).corr(dr.dy)['2025-10-01':]
out['roll_corr_dy'] = {'dates': [t.strftime('%Y-%m-%d') for t in rc.index], 'v': [None if pd.isna(v) else round(float(v), 3) for v in rc.values]}

# ---------- 5. Leadership breadth among 8 AI semis ----------
names = ['NVDA', 'TSM', 'AVGO', 'AMD', 'MU', 'ASML', '000660.KS', '005930.KS']
br = pd.DataFrame({n: px[n] > px[n].rolling(200).mean() for n in names}).astype(float)
br50 = pd.DataFrame({n: px[n] > px[n].rolling(50).mean() for n in names}).astype(float)
b = br['2025-10-01':].mean(1); b5 = br50['2025-10-01':].mean(1)
out['breadth'] = {'dates': [t.strftime('%Y-%m-%d') for t in b.index], 'above200': [round(float(v), 3) for v in b], 'above50': [round(float(v), 3) for v in b5]}
print('\nBreadth now >200d', b.iloc[-1], '>50d', b5.iloc[-1])

# ---------- 6. Death cross proximity ----------
sma50 = s.rolling(50).mean(); s200 = s.rolling(200).mean()
sim = s.copy(); last = s.iloc[-1]; idx = pd.bdate_range(s.index[-1] + pd.Timedelta(days=1), periods=60)
sim = pd.concat([s, pd.Series(last, index=idx)])
gap = sim.rolling(50).mean() - sim.rolling(200).mean()
cross = gap[gap.index > s.index[-1]]; cross = cross[cross < 0]
out['death_cross_if_flat'] = cross.index[0].strftime('%Y-%m-%d') if len(cross) else None
print('Death cross if price flat:', out['death_cross_if_flat'], 'gap now', round(float(sma50.iloc[-1]/s200.iloc[-1] - 1), 3))

# ---------- 7. Name-level 2026 paths (normalized) for chart ----------
nn = ['SOXX', 'TSM', 'NVDA', 'MU', 'AMD', 'AVGO', 'ASML', '000660.KS', 'SPY']
z = px[nn]['2025-12-31':].ffill()
z = z/z.iloc[0]*100
out['norm'] = {'dates': [t.strftime('%Y-%m-%d') for t in z.index], **{n: [round(float(v), 2) for v in z[n]] for n in nn}}
# macro series
mm = px[['TNX', 'CLF', 'KS11', 'VIX']]['2025-10-01':].ffill()
out['macro'] = {'dates': [t.strftime('%Y-%m-%d') for t in mm.index], **{c: [round(float(v), 3) for v in mm[c]] for c in mm}}
json.dump(out, open('deeper.json', 'w'))
