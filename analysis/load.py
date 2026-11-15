import json, glob, os, pandas as pd
D=os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'))
def load(f):
    r=json.load(open(f))['chart']['result'][0]
    idx=pd.to_datetime(r['timestamp'],unit='s').normalize()
    q=r['indicators']['quote'][0]
    adj=r['indicators'].get('adjclose',[{}])[0].get('adjclose',q['close'])
    df=pd.DataFrame({'close':q['close'],'adj':adj,'vol':q['volume'],'high':q['high'],'low':q['low']},index=idx)
    return df[~df.index.duplicated(keep='last')].dropna(subset=['close'])
def all_px():
    return {os.path.basename(f)[:-5]:load(f) for f in glob.glob(D+'/*.json')}
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
