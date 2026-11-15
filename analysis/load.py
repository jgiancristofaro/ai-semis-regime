import json, glob, os, pandas as pd
D=os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'))
def load(f):
    r=json.load(open(f))['chart']['result'][0]
    idx=pd.to_datetime(r['timestamp'],unit='s').normalize()
    q=r['indicators']['quote'][0]
    adj=r['indicators'].get('adjclose',[{}])[0].get('adjclose',q['close'])
    df=pd.DataFrame({'close':q['close'],'adj':adj,'vol':q['volume'],'high':q['high'],'low':q['low']},index=idx)
    return df[~df.index.duplicated(keep='last')].dropna(subset=['close'])
def load_tiingo(f):
    rows = json.load(open(f))
    df = pd.DataFrame(rows)
    df.index = pd.to_datetime(df['date']).dt.tz_localize(None).dt.normalize()
    out = pd.DataFrame({'close': df['close'], 'adj': df['adjClose'], 'vol': df['volume'], 'high': df['high'], 'low': df['low']})
    return out[~out.index.duplicated(keep='last')].dropna(subset=['close'])

def all_px():
    """Yahoo files for every ticker; where a Tiingo file exists and is at least as current, Tiingo replaces Yahoo."""
    P = {os.path.basename(f)[:-5]: load(f) for f in glob.glob(D + '/*.json') if not os.path.basename(f).startswith('tiingo_')}
    for f in glob.glob(D + '/tiingo_*.json'):
        k = os.path.basename(f)[7:-5]
        try:
            tg = load_tiingo(f)
            if k not in P or tg.index[-1] >= P[k].index[-1]:
                P[k] = tg
        except Exception:
            pass
    return P
def us_px(field='adj'):
    """All series aligned to the US (SPY) trading calendar; foreign/holiday-only rows dropped, gaps forward-filled."""
    P = all_px()
    cal = P['SPY'].index
    return pd.DataFrame({k: getattr(v, field) for k, v in P.items()}).sort_index().reindex(cal).ffill()

def fred(sid):
    """Daily/weekly FRED series as a float Series (missing values dropped)."""
    df = pd.read_csv(os.path.join(D, f'fred_{sid}.csv'))
    s = pd.to_numeric(df.iloc[:, 1], errors='coerce')
    s.index = pd.to_datetime(df.iloc[:, 0])
    return s.dropna()
