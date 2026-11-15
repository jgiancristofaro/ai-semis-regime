# AI Semis After the Peak

A daily-refreshed research note on whether SOXX, TSM and other AI semiconductor stocks are investable after the June 2026 peak.

**Live page:** https://jgiancristofaro.github.io/ai-semis-regime/

It covers:

- **2026 backtest.** A rules-based regime model (five yes/no checks plus a "blow-off" exit) held SOXX from late December 2025 and exited on July 14, 2026, three weeks after the top.
- **Current state.** Each regime check, its pass threshold, the SOXX price that flips it, and a what-if tool for future dates.
- **Momentum, breadth and macro sensitivity**, including how semis' behaviour changed in the second half of 2026.
- **Valuation and demand evidence** (agentic AI, AI-accelerated R&D, sold-out supply) with sources.
- **Entry-plan backtest** across 15 prior semiconductor drawdowns, comparing lump-sum, monthly tranches and waiting for the trend.

> Research, not investment advice. Backtests use daily adjusted closes, a one-day signal lag, 5bp per-side costs and 0% on cash.

## What refreshes daily

A GitHub Actions workflow (`.github/workflows/refresh.yml`) runs every weekday at 22:17 UTC, after the US close. It downloads prices, reruns every analysis and redeploys the page to GitHub Pages.

- **Updated each run:** prices, regime signals and flip levels, backtests, breadth, momentum state and all charts.
- **Fixed snapshot (as of Nov 15, 2026):** the written narrative, valuation figures and citations. The page says so. See `research/` for the underlying notes.

To refresh by hand, open **Actions → Daily refresh → Run workflow**.

## The regime model

At each close the model scores five checks, one point each:

| Check | Passes when |
|---|---|
| Above 200-day | SOXX closes above its 200-day moving average |
| 3-month momentum | SOXX is above its close 63 sessions earlier |
| Beats the S&P 500 | The SOXX/SPY ratio is above its 100-day average |
| Calm volatility | 20-day realized volatility is below 1.5× its 1-year median |
| Rates not spiking | The 10-year Treasury yield has risen less than 0.50 pt over 63 sessions |

Position: 4–5 = fully long, 3 = half, 0–2 = cash.

The blow-off exit triggers when SOXX's stretch above its 200-day has exceeded the 95th percentile of its own history (expanding window, past data only) within the last 30 sessions, and SOXX then closes below its 50-day. Re-entry needs 5/5 and a close above the 50-day.

## Run locally

```bash
pip install -r requirements.txt
```

```bash
python analysis/update.py
```

The page is written to `site/index.html`. Use `--skip-fetch` to rebuild from data already downloaded in `data/`.

| File | Role |
|---|---|
| `analysis/fetch.py` | Downloads daily history (Yahoo Finance chart API) into `data/` |
| `analysis/backtest.py` | Five signals on SOXX, 2026 and 2002–2025 |
| `analysis/deeper.py` | Momentum states, drawdown episodes, blow-off analogs, macro correlations, breadth |
| `analysis/grid.py` | 27-variant robustness grid for the blow-off exit |
| `analysis/staged.py` | Entry-plan backtest over 15 prior drawdowns |
| `analysis/regime_now.py` | Current regime checks, exact flip prices, 60-day projection |
| `analysis/bundle.py` | Packs all outputs into the page's data block |
| `analysis/template.html` | The page; `update.py` injects data and writes `site/index.html` |

## Data notes

Prices come from Yahoo Finance's public chart endpoint. It is unofficial, so it can rate-limit or change without notice. If a download fails, the workflow fails and the last good page stays live. Raw price files are not committed.
