"""
Hyperscaler capital spending from SEC XBRL filings (cash capex: purchases of property & equipment; excludes finance leases).
Companies: Microsoft, Alphabet, Amazon, Meta, Oracle. Quarterly values are derived from the year-to-date cash-flow figures in
10-Q/10-K filings. Output: capex.json (quarterly series per company, aggregate, year-over-year growth).
The SEC requires a declared contact in the User-Agent: set SEC_USER_AGENT (GitHub secret). Without it the step is skipped
and the page keeps the last saved series (research/snapshots/capex.json).
"""
import json, os, ssl, sys, time, urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SAVED = os.path.join(HERE, '..', 'research', 'snapshots', 'capex.json')
CA = '/root/.ccr/ca-bundle.crt'
ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
CO = {'MSFT': '0000789019', 'GOOGL': '0001652044', 'AMZN': '0001018724', 'META': '0001326801', 'ORCL': '0001341439'}
CONCEPTS = ['PaymentsToAcquirePropertyPlantAndEquipment', 'PaymentsToAcquireProductiveAssets',
            'PaymentsForProceedsFromProductiveAssets', 'PaymentsToAcquireOtherPropertyPlantAndEquipment']

ua = os.environ.get('SEC_USER_AGENT', '').strip()
if not ua:
    print('capex skipped: SEC_USER_AGENT not set', file=sys.stderr)
    sys.exit(0)
if ' ' not in ua:
    ua = 'ai-semis-regime research ' + ua  # SEC asks for "name contact"

def d(s): return date.fromisoformat(s)

def quarterly(facts):
    """facts: list of {start,end,val,filed}. Returns {end: quarterly value} from direct quarters or YTD differences."""
    by = {}
    for f in facts:
        k = (f['start'], f['end'])
        if k not in by or f['filed'] > by[k]['filed']:
            by[k] = f
    q = {}
    for (st, en), f in by.items():
        days = (d(en) - d(st)).days
        if 80 <= days <= 100:
            q[en] = f['val']
    # YTD differencing: same start, consecutive ends
    starts = {}
    for (st, en), f in by.items():
        starts.setdefault(st, []).append((en, f['val']))
    for st, lst in starts.items():
        lst.sort()
        for (e0, v0), (e1, v1) in zip(lst, lst[1:]):
            gap = (d(e1) - d(e0)).days
            if 80 <= gap <= 100 and e1 not in q:
                q[e1] = v1 - v0
        # first quarter of the fiscal year
        e_first, v_first = lst[0]
        if 80 <= (d(e_first) - d(st)).days <= 100 and e_first not in q:
            q[e_first] = v_first
    return q

out = {'companies': {}, 'asof': None}
for tk, cik in CO.items():
    req = urllib.request.Request(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json',
                                 headers={'User-Agent': ua, 'Accept-Encoding': 'identity'})
    try:
        facts = json.loads(urllib.request.urlopen(req, timeout=60, context=ctx).read())['facts'].get('us-gaap', {})
    except Exception as e:
        print(f'capex {tk} failed: {e}', file=sys.stderr); continue
    time.sleep(0.3)  # SEC fair-access: well under 10 requests/second
    best = None
    for c in CONCEPTS:
        if c in facts and 'USD' in facts[c]['units']:
            fs = [f for f in facts[c]['units']['USD'] if f.get('start') and f.get('form') in ('10-Q', '10-K', '10-Q/A', '10-K/A')]
            q = quarterly(fs)
            if q and (best is None or max(q) > max(best[1])):
                best = (c, q)
    if not best:
        print(f'capex {tk}: no capex concept found', file=sys.stderr); continue
    c, q = best
    ends = sorted(q)[-16:]
    out['companies'][tk] = {'concept': c, 'quarters': [{'end': e, 'capex_busd': round(q[e] / 1e9, 3)} for e in ends]}

if len(out['companies']) < 4:
    print('capex incomplete; keeping saved series', file=sys.stderr); sys.exit(0)

# Calendar-quarter aggregate (quarter of the fiscal period end date)
def cq(e):
    dt = d(e); return f'{dt.year}Q{(dt.month - 1) // 3 + 1}'
agg = {}
for tk, v in out['companies'].items():
    for r in v['quarters']:
        agg.setdefault(cq(r['end']), {})[tk] = r['capex_busd']
qs = sorted(k for k, v in agg.items() if len(v) == len(out['companies']))
out['aggregate'] = [{'q': k, 'total_busd': round(sum(agg[k].values()), 2), **agg[k]} for k in qs]
for i, r in enumerate(out['aggregate']):
    prev = next((x for x in out['aggregate'] if x['q'] == f"{int(r['q'][:4]) - 1}{r['q'][4:]}"), None)
    r['yoy'] = round(r['total_busd'] / prev['total_busd'] - 1, 4) if prev else None
out['asof'] = max(r['end'] for v in out['companies'].values() for r in v['quarters'])
os.makedirs(os.path.dirname(SAVED), exist_ok=True)
json.dump(out, open(SAVED, 'w'), indent=1)
last = out['aggregate'][-1]
print(f"capex ok: {len(out['companies'])} companies, latest {last['q']} ${last['total_busd']:.1f}B, y/y {last['yoy']}")
