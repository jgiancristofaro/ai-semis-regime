"""
Daily Finnhub snapshot for the largest US-listed semiconductor stocks (free tier):
  forward P/E, market cap, analyst recommendation counts, latest earnings surprise.
Implied consensus forward EPS = closing price / forward P/E. Saved daily to research/snapshots/estimates.csv,
so estimate revisions build up into a history (free sources don't offer historical estimates).
Needs FINNHUB_API_KEY (GitHub secret). Without it, the step is skipped and the page keeps the last snapshot.
"""
import csv, json, os, ssl, sys, time, urllib.request
import pandas as pd
from load import all_px

NAMES = ['NVDA', 'AVGO', 'TSM', 'AMD', 'ASML', 'MU', 'QCOM', 'TXN', 'AMAT', 'LRCX', 'KLAC', 'INTC',
         'ADI', 'MRVL', 'NXPI', 'MCHP', 'MPWR', 'ON']
HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, '..', 'research', 'snapshots', 'estimates.csv')
CA = '/root/.ccr/ca-bundle.crt'
ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
key = os.environ.get('FINNHUB_API_KEY')
if not key:
    print('estimates skipped: FINNHUB_API_KEY not set', file=sys.stderr); sys.exit(0)

def get(path):
    req = urllib.request.Request('https://finnhub.io/api/v1/' + path, headers={'X-Finnhub-Token': key, 'User-Agent': 'ai-semis-regime/1.0'})
    for attempt in range(3):
        try:
            return json.loads(urllib.request.urlopen(req, timeout=30, context=ctx).read())
        except Exception as e:
            if attempt == 2: raise
            time.sleep(3 * (attempt + 1))

P = all_px()
sox_last = P['SOXX'].index[-1]
asof = sox_last.strftime('%Y-%m-%d')
rows = []
for s in NAMES:
    try:
        m = get(f'stock/metric?symbol={s}&metric=all').get('metric', {})
        rec = get(f'stock/recommendation?symbol={s}')
        ern = get(f'stock/earnings?symbol={s}')
        time.sleep(1.1)  # free tier: 60 calls/minute
        fpe = m.get('forwardPE'); mcap = m.get('marketCapitalization')  # mcap in $M
        close = float(P[s].close.iloc[-1]) if s in P else None
        if s == 'TSM' and close:  # Finnhub reports TSMC's market cap in TWD; rebuild in USD: ~25,932M common shares, 5 per ADR
            mcap = close * 25932 / 5
        r0 = rec[0] if rec else {}
        e0 = ern[0] if ern else {}
        rows.append({'date': asof, 'symbol': s, 'forward_pe': fpe, 'market_cap_musd': mcap,
                     'fwd_earnings_musd': (mcap / fpe) if (mcap and fpe and fpe > 0) else None, 'close': close, 'pe_ttm': m.get('peTTM'), 'eps_growth_ttm_yoy': m.get('epsGrowthTTMYoy'),
                     'rev_growth_ttm_yoy': m.get('revenueGrowthTTMYoy'),
                     'rec_period': r0.get('period'), 'strong_buy': r0.get('strongBuy'), 'buy': r0.get('buy'), 'hold': r0.get('hold'),
                     'sell': r0.get('sell'), 'strong_sell': r0.get('strongSell'),
                     'last_q': e0.get('period'), 'eps_actual': e0.get('actual'), 'eps_estimate': e0.get('estimate'), 'surprise_pct': e0.get('surprisePercent')})
    except Exception as e:
        print(f'estimates {s} failed: {e}', file=sys.stderr)

if len(rows) < len(NAMES) * 0.7:
    print(f'estimates incomplete ({len(rows)}/{len(NAMES)}); not saved', file=sys.stderr); sys.exit(0)
old = pd.read_csv(SNAP) if os.path.exists(SNAP) else pd.DataFrame()
new = pd.DataFrame(rows)
if not old.empty:
    old = old[old['date'] != asof]  # re-runs on the same day replace that day's rows
out = pd.concat([old, new], ignore_index=True)
os.makedirs(os.path.dirname(SNAP), exist_ok=True)
out.to_csv(SNAP, index=False)
print(f'estimates ok: {len(rows)} names for {asof} ({out.date.nunique()} days on file)')
