"""
Daily snapshots of data that has no free history, appended to research/snapshots/ so a history builds up.
  - SOXX shares outstanding (iShares product page). Day-over-day change x closing price approximates ETF creations/redemptions (flows).
The GitHub workflow commits the updated CSV after each run. Failures here never block the page build.
"""
import csv, html as htmllib, os, re, ssl, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SNAP = os.path.join(HERE, '..', 'research', 'snapshots')
CA = '/root/.ccr/ca-bundle.crt'
ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
os.makedirs(SNAP, exist_ok=True)

def field(html, name):
    """Pull formattedValue / formattedAsOfDate for a named data field embedded in the iShares page JSON."""
    m = re.search(r'"formattedValue":"([^"]*)"[^{}]*?"formattedAsOfDate":"([^"]*)"[^{}]*?"name":"' + name + '"', html)
    return (m.group(1), m.group(2)) if m else (None, None)

try:
    url = 'https://www.ishares.com/us/products/239705/ishares-phlx-semiconductor-etf'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    html = htmllib.unescape(urllib.request.urlopen(req, timeout=40, context=ctx).read().decode('utf-8', 'ignore'))
    so, so_date = field(html, 'sharesOutstanding')
    if not so:
        raise ValueError('shares outstanding not found on page')
    path = os.path.join(SNAP, 'soxx_shares_outstanding.csv')
    rows = list(csv.DictReader(open(path))) if os.path.exists(path) else []
    rec = {'as_of': so_date, 'shares_outstanding': so.replace(',', '')}
    if not rows or rows[-1]['as_of'] != rec['as_of']:
        rows.append(rec)
        with open(path, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rec)); w.writeheader(); w.writerows(rows)
    print('snapshot ok', rec, f'({len(rows)} rows)')
except Exception as e:  # never fail the daily build over a snapshot
    print('snapshot skipped:', e, file=sys.stderr)
