"""
Out-of-sample test of the SOXX Regime Monitor (github.com/jgiancristofaro/soxx-regime-monitor) state machine,
using its own code unchanged, on SOXX 2002-2025 (it was calibrated on Jan-Jul 2026 only).

Usage: python oos_monitor.py [/path/to/soxx-regime-monitor]  (defaults to analysis/vendor/soxx_regime_monitor)
Data: Tiingo adjusted OHLCV for SOXX from ../../data/tiingo_SOXX.json (fetched by analysis/fetch.py).
Method: derived signals on full history; the state machine runs per calendar year (it resets each Jan 1, as in
production); yearly equity uses the monitor's own _run_backtest (from Jan 20, 5bp per side, cash at 0%).
"""
import json, os, sys
import numpy as np, pandas as pd

HERE0 = os.path.dirname(os.path.abspath(__file__))
# Default: the pinned copy vendored in analysis/vendor/; or pass a path to a soxx-regime-monitor checkout to test its latest code.
sm_dir = os.path.join(sys.argv[1], 'pipeline') if len(sys.argv) > 1 else os.path.join(HERE0, '..', '..', 'analysis', 'vendor', 'soxx_regime_monitor')
sys.path.insert(0, sm_dir)
import state_machine as sm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, '..', '..', 'data', 'tiingo_SOXX.json')))
df = pd.DataFrame(rows)
df.index = pd.to_datetime(df['date']).dt.tz_localize(None).dt.normalize()
df = pd.DataFrame({'open': df.adjOpen, 'high': df.adjHigh, 'low': df.adjLow, 'close': df.adjClose, 'volume': df.adjVolume})
full = sm._compute_derived(df)

years, trades_all, daily = [], [], []
for y in range(2002, 2027):
    ytd = full[full.index.year == y].copy()
    if len(ytd) < 40: continue
    states, acc, trades = sm._run_state_machine(ytd)
    eq_s, eq_bh = sm._run_backtest(ytd, states, acc, trades)
    s = pd.Series(eq_s, index=ytd.index).dropna(); b = pd.Series(eq_bh, index=ytd.index).dropna()
    pos = pd.Series([1.0 if a else sm.STATE_POS.get(st, 1.0) for st, a in zip(states, acc)], index=ytd.index)[s.index]
    years.append({'year': y, 'strategy': float(s.iloc[-1] - 1), 'buy_hold': float(b.iloc[-1] - 1),
                  'maxdd_s': float((s / s.cummax() - 1).min()), 'maxdd_bh': float((b / b.cummax() - 1).min()),
                  'trades': len(trades), 'avg_exposure': float(pos.mean())})
    trades_all += [dict(t, year=y) for t in trades]
    daily.append(pd.DataFrame({'s': s.pct_change().fillna(s.iloc[0] - 1), 'b': b.pct_change().fillna(b.iloc[0] - 1)}))
    daily[-1]['pos'] = pos
    daily[-1]['warm'] = pd.Series([st == sm.WARMUP for st in states], index=ytd.index)[s.index].astype(int)

Y = pd.DataFrame(years).set_index('year')
d = pd.concat(daily)
def stats(r):
    eq = (1 + r).cumprod(); n = len(r) / 252
    return {'total': float(eq.iloc[-1] - 1), 'cagr': float(eq.iloc[-1] ** (1 / n) - 1),
            'sharpe': float(r.mean() * 252 / (r.std() * np.sqrt(252))), 'maxdd': float((eq / eq.cummax() - 1).min())}
summary = {}
for lab, a, b_ in [('2002-2025 (out-of-sample)', '2002', '2025'), ('2002-2009', '2002', '2009'), ('2010-2019', '2010', '2019'),
                   ('2020-2025', '2020', '2025'), ('2026 (in-sample + since)', '2026', '2026')]:
    x = d[a:b_]
    summary[lab] = {'monitor': stats(x.s), 'buy_hold': stats(x.b)}
beat = int((Y.loc[:2025, 'strategy'] > Y.loc[:2025, 'buy_hold']).sum())
out = {'years': Y.reset_index().to_dict('records'), 'summary': summary, 'beat_years': beat, 'n_years': int((Y.index <= 2025).sum()),
       'trades_per_year': float(Y.loc[:2025, 'trades'].mean()), 'trades_2026': [t for t in trades_all if t['year'] == 2026],
       'last_state': states[-1], 'note': 'Equity per year from Jan 20 (monitor warm-up), chained; cash 0%, 5bp per side.'}
json.dump(out, open(os.path.join(HERE, 'oos_results.json'), 'w'), indent=1, default=str)
d[['pos', 'warm']].to_csv(os.path.join(HERE, 'monitor_positions.csv'))

pd.set_option('display.width', 200)
print(Y.round(3).to_string())
print(json.dumps(summary, indent=1))
print('beat B&H in', beat, 'of', out['n_years'], 'years; avg trades/yr', round(out['trades_per_year'], 1))
print('2026 trades:', [(t['date'], t['action']) for t in out['trades_2026']])
