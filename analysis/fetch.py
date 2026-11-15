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

# Tiingo (official EOD API, primary for US-listed tickers when a key is available; Yahoo stays as fallback)
TIINGO = ['SOXX', 'SMH', 'TSM', 'NVDA', 'AVGO', 'AMD', 'MU', 'ASML', 'SPY', 'QQQ', 'SOXL']
tkey = os.environ.get('TIINGO_API_KEY')
tiingo_ok = set()
if tkey:
    for t_ in TIINGO:
        for attempt in range(3):
            try:
                req = urllib.request.Request(f'https://api.tiingo.com/tiingo/daily/{t_}/prices?startDate=2000-01-01&format=json',
                                             headers={'Authorization': f'Token {tkey}', 'User-Agent': 'ai-semis-regime/1.0'})
                body = urllib.request.urlopen(req, timeout=60, context=ctx).read()
                rows = json.loads(body); assert isinstance(rows, list) and len(rows) > 1000, 'too few rows'
                with open(os.path.join(OUT, f'tiingo_{t_}.json'), 'wb') as f:
                    f.write(body)
                tiingo_ok.add(t_); break
            except Exception as e:
                if attempt == 2: print(f'tiingo {t_} failed: {e}')
                time.sleep(2 ** attempt)
    print('tiingo', len(tiingo_ok), 'of', len(TIINGO))
# A Yahoo failure only counts when Tiingo didn't cover that ticker
bad = [b for b in bad if b.split(':')[0] not in tiingo_ok]

# FRED series (public CSV endpoint, no key): Baa-10y spread, HY OAS (3y history only), 10y real yield, Chicago Fed NFCI
FRED = ['BAA10Y', 'BAMLH0A0HYM2', 'DFII10', 'NFCI']
for sid in FRED:
    for attempt in range(4):
        try:
            req = urllib.request.Request(f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}', headers={'User-Agent': 'ai-semis-regime/1.0 (+https://github.com/jgiancristofaro/ai-semis-regime)'})  # FRED stalls bare 'Mozilla/5.0'
            body = urllib.request.urlopen(req, timeout=30, context=ctx).read()
            assert body.count(b'\n') > 500, 'too few rows'
            with open(os.path.join(OUT, f'fred_{sid}.csv'), 'wb') as f:
                f.write(body)
            break
        except Exception as e:
            if attempt == 3:
                bad.append(f'FRED {sid}: {e}')
            time.sleep(2 ** attempt)

print('fetched', len(TICKERS) + len(FRED) - len(bad), 'of', len(TICKERS) + len(FRED))
if bad:
    print('FAILED:', *bad, sep='\n  ')
    sys.exit(1)
