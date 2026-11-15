"""
Read the live SOXX Regime Monitor (github.com/jgiancristofaro/soxx-regime-monitor) published state:
state machine (RISK_ON / MONITOR / EXIT / ACCUM), intraday/overnight flow streams, re-entry lines, vol and VRP.
Saved to research/snapshots/monitor_signals.json; on failure the last saved copy is used.
"""
import json, os, ssl, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'research', 'snapshots', 'monitor_signals.json')
URL = 'https://raw.githubusercontent.com/jgiancristofaro/soxx-regime-monitor/main/data/signals.json'
CA = '/root/.ccr/ca-bundle.crt'
ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else ssl.create_default_context()
try:
    s = json.loads(urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent': 'ai-semis-regime/1.0'}), timeout=30, context=ctx).read())
    keep = {k: s[k] for k in ('last_session', 'data_stale', 'state', 'today', 'trades', 'checklist', 'generated_utc') if k in s}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(keep, open(OUT, 'w'), indent=1)
    print('monitor ok', keep['last_session'], keep['state']['machine'])
except Exception as e:
    print('monitor fetch skipped (using last saved copy):', e, file=sys.stderr)
