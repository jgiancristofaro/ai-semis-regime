"""One-command daily refresh: fetch prices -> rerun every analysis -> rebuild the HTML page.

Usage:  python3 update.py [--skip-fetch]
Output: ../site/index.html (override with OUT_HTML)
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
steps = ([] if '--skip-fetch' in sys.argv else ['fetch.py']) + \
        ['snapshot.py', 'backtest.py', 'deeper.py', 'grid.py', 'staged.py', 'regime_now.py', 'credit.py', 'bundle.py']
for s in steps:
    r = subprocess.run([sys.executable, s], capture_output=True, text=True)
    if r.returncode:
        print(f'{s} FAILED\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}')
        sys.exit(1)
    print('ok', s)

out = os.path.normpath(os.environ.get('OUT_HTML', os.path.join(HERE, '..', 'site', 'index.html')))
os.makedirs(os.path.dirname(out), exist_ok=True)
with open('template.html') as f:
    tpl = f.read().replace('/*__DATA__*/', open('data.js').read())
# Standalone document: everything before the page wrapper (title, metas, fonts, styles) goes in <head>.
cut = tpl.index('<div class="wrap">')
html = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="description" content="Daily-refreshed research note on SOXX, TSM and AI semiconductors: regime model, backtests, valuation and entry plan.">\n'
        + tpl[:cut] + '\n</head>\n<body>\n' + tpl[cut:] + '\n</body>\n</html>\n')
with open(out, 'w') as f:
    f.write(html)
live = json.load(open('regime_now.json'))
print(f"built {out} | as of {live['asof']} | SOXX {live['soxx']:.2f} | regime {live['score']}/5 | {live['components']}")
