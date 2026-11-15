"""Download daily history for every ticker the analysis uses from Yahoo Finance's chart API into ../data (one JSON per ticker)."""
import json, os, ssl, sys, time, urllib.parse, urllib.request

TICKERS = ['SOXX', 'SMH', 'TSM', 'NVDA', 'AVGO', 'AMD', 'MU', 'ASML', 'SPY', 'QQQ', '^VIX', '^TNX', 'CL=F',
           '000660.KS', '005930.KS', '^KS11', 'DX-Y.NYB', 'SOXL', '^SOX']
OUT = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'))
CA = '/root/.ccr/ca-bundle.crt'  # cloud-session proxy CA; falls back to system roots elsewhere
ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
os.makedirs(OUT, exist_ok=True)

now = int(time.time())
bad = []
for t in TICKERS:
    url = (f'https://query2.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(t)}'
           f'?period1=946684800&period2={now}&interval=1d&events=div%7Csplit&includeAdjustedClose=true')
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            body = urllib.request.urlopen(req, timeout=30, context=ctx).read()
            r = json.loads(body)['chart']['result'][0]
            assert len(r['timestamp']) > 1000, 'too few rows'
            with open(os.path.join(OUT, t.replace('^', '').replace('=', '') + '.json'), 'wb') as f:
                f.write(body)
            break
        except Exception as e:  # retry with backoff, then report
            if attempt == 3:
                bad.append(f'{t}: {e}')
            time.sleep(2 ** attempt)

print('fetched', len(TICKERS) - len(bad), 'of', len(TICKERS))
if bad:
    print('FAILED:', *bad, sep='\n  ')
    sys.exit(1)
