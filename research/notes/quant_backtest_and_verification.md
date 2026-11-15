# Quant backtest results and fact verification (coordinator's own analysis)

Data: Yahoo Finance daily adjusted closes, downloaded 2026-11-15, last bar 2026-11-13. Split-adjusted (SOXX 3:1 split early Nov 2026). Scripts: analysis/backtest.py, deeper.py, grid.py. Cash earns 0% (conservative), 5bp cost per side, 1-day signal lag.

## Verified price facts (primary data — overrides any conflicting figure from research notes)
- SOXX: peak close 2026-06-22 at $218.2 (split-adj); last $149.30 (Nov 13) = -31.6% from peak; YTD +49.0% (price-only basis from Yahoo adj. close vs 2025-12-31).
- SOX index: peak 2026-06-22 ~14,630; last 10,146 (Nov 13) = -30.7%; YTD +43.2%. (Research note estimate of ~9,000-9,350 is WRONG — ignore.)
- TSM: peak 2026-10-05 $485.8; last $398.73 (-17.9%); YTD +32.2%.
- NVDA: peak 2026-10-06 $239.2; last $162.85 (-31.9%); YTD -12.5%.
- MU: YTD +172.9%, peak Jun 25, -35.8% from peak. AMD YTD +149%, peak Oct 6, -17.8%. AVGO YTD +0.8%, -27.7%. ASML YTD +40.6%, -24.6%.
- SK hynix YTD +87%, -58.3% from Jun 22 peak. KOSPI peaked Jun 22 (same day as SOX), -42%.
- SPY YTD +11.5%, only -3.2% from Oct 6 peak. QQQ -10.5% from peak.
- 10y UST: 5.15% (Nov 13); 2026 high 5.31% (Oct 5); +43bp in the last 63 trading days. WTI ~$88.6; spiked to ~$101-105 in Mar-Apr.
- SOXX Nov 5: -12.1% in one day (150.14 -> 131.90).
- Current SOXX levels: 20d SMA 156.8, 50d SMA 171.9, 200d SMA 160.3. 20d realized vol 77% vs 1y median 39%.

## Verified events
- Nvidia CEO Jensen Huang RESIGNED: SEC 8-K dated 2026-11-12 (https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvidiaannouncesceotransiti.htm). Kress interim CEO, Harvey Jones board chair. Board had opened an independent investigation on Nov 9 (CNBC https://www.cnbc.com/2026/11/09/nvidia-jensen-huang-chinese-spy-investigation.html). CNBC live: https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html
- Situational Awareness: Reuters reported -67% in July 2026 per investor letter; long AI infra / short software; ~4x leverage; public book sold (mostly to Citadel) Jul 30. Sources: https://www.implicator.ai/situational-awareness-fell-67-in-july-and-removed-all-leverage-letter-shows/ ; https://qz.com/situational-awareness-hedge-fund-margin-call-citadel-fire-sale-073126 . AUM figures conflict across sources.

## Backtest 1: standard signals on SOXX (parameters are textbook defaults, not tuned on 2026)
| Strategy | 2026 YTD return | 2026 maxDD | 2002-2025 total | 2002-25 CAGR | 2002-25 Sharpe | 2002-25 maxDD |
|---|---|---|---|---|---|---|
| Buy & Hold | +49.0% | -39.6% | +2194% | 13.8% | 0.57 | -66.8% |
| Trend 200d | +55.8% | -29.0% | +825% | 9.6% | 0.55 | -41.9% |
| 50/200 cross | +49.0% | -39.6% | +1713% | 12.7% | 0.66 | -34.2% |
| Dual momentum (monthly) | +49.0% | -39.6% | +369% | 6.6% | 0.41 | -53.5% |
| Regime composite (5-factor) | +44.4% | -33.7% | +584% | 8.3% | 0.49 | -50.0% |
| Composite + Blow-off exit | **+75.9%** | **-15.8%** | +545% | 8.0% | 0.49 | -50.0% |

Regime composite components: price>200d SMA; 63d momentum>0; SOXX/SPY ratio > its 100d mean; 20d realized vol < 1.5x its 1y median; 10y yield change over 63d < +50bp. Full long at 4-5, half at 3, flat <=2.
Blow-off overlay: if SOXX's % above 200d SMA exceeded the expanding (past-only) 95th percentile within the last 30 days AND price closes below 50d SMA -> exit; re-enter only when composite = 5/5 and price > 50d SMA.

Composite + Blow-off positions in 2026: long since 2025-12-22; out Mar 6 -> Apr 7 (Iran war/oil shock correction); back in Apr 7; **EXIT Jul 8, 2026**; still out today.
Peak SOXX extension above 200d SMA in 2026: +79% (Jun 3) — previous max since 2001 was +44% (2003). On SOX index incl. 2000: 2026 = +74.6%.

Honest read: in 2002-2025, no timing rule beat buy & hold on total return; they mainly reduced drawdowns (50/200 cross had best Sharpe 0.66 vs 0.57, maxDD -34% vs -67%). The blow-off overlay specifically is a tail-event tool — it paid off in 2026's unprecedented parabola, and cost return in normal regimes.

## Backtest 2: robustness grid (27 variants: base {hold, trend, composite} x extension pct {90,95,97.5} x exit MA {20,50,100})
- All 27 beat 2026 buy & hold: 2026 returns +52% to +76% vs +49%; max DD -12% to -29% vs -40%.
- 2026 exit dates by MA: 20d -> Jun 8; 50d -> Jul 8; 100d -> Jul 30. All variants were out before August.
- Percentile threshold doesn't matter in 2026 (extension so extreme all thresholds triggered).

## Current signal status (as of Nov 13, 2026)
- Regime composite: 0/5 (all components negative) -> flat. Trend-200d: flat since Nov 2 (whipsaw Oct 23-26).
- 50/200 cross still long (50d 7.2% above 200d); death cross would occur ~Dec 3, 2026 if price stays flat.
- Momentum state (Goulding-Harvey-Mazzoleni "turning points", 12m slow vs 1m fast): "Correction" (slow +, fast −) in Oct & Nov 2026. 12-1m momentum still +72%, 3m −20%.
- Historical forward returns by state on SOX 2001-2025 (monthly, n): Bull(117) 3m +3.9% / 12m +18.6%; Correction(71) 3m +2.9% / 12m +13.6% (lowest; 3m hit-rate 58%); Bear(60) 3m +4.9% / 12m +18.4%; Rebound(52) 3m +2.4% / 12m +18.8%.
- Breadth: only 1 of 8 AI semis (AMD) above its 200d SMA; 1 of 8 above 50d.
- Re-entry would need roughly: SOXX > ~160 (200d) and > ~172 (50d), vol normalizing, 10y yields stabilizing.

## Analog: drawdowns after >30% extension above 200d (SOX)
| Peak date | Extension | Max DD next 18m | 12m return |
|---|---|---|---|
| 2003-11 | +40% | -33% | -21% |
| 2004-01 | +32% | -37% | -29% |
| 2009-09 | +32% | -10% | -3% |
| 2020-12 | +38% | -4% | +41% |
| 2021-01 | +40% | -22% | +10% |
| 2023-06 | +32% | -15% | +50% |
| 2024-03 | +36% | -31% | -10% |
| 2025-10 | +38% | -13% | +57% |
| 2026-06 | +75% | -35% so far | n/a |
Median max DD after prior blow-offs ~ -22%; worst -37%. 2026 has already matched the worst, but the extension was ~2x larger.

## Episodes: SOX >=28% below 52w high and below 200d (de-clustered)
15 prior episodes since 2000. Mean forward: 3m +2.8%, 6m +7.4%, 12m +18.1% (hit-rate 60%), vs unconditional 3m +3.1%, 12m +14.6%. Bimodal: 2001-02, 2008 kept falling; 2020-03, 2022-10, 2025-04 rallied +50-114% in 12m. Unique to 2026: 12m momentum still +44% at the signal date — prior deep drawdowns almost all had negative 12m momentum.

## Macro sensitivity (daily)
| Period | corr(SOXX, Δ10y) | corr(SOXX, oil) | corr(SOXX, KOSPI) | beta to SPY |
|---|---|---|---|---|
| 2025 | +0.22 | +0.23 | 0.04 | 1.78 |
| H1 2026 | −0.29 | −0.31 | 0.13 | 2.51 |
| H2 2026 | +0.18 | −0.17 | **0.42** | **2.98** |
Interpretation: in H1, rising yields/oil hurt semis (inflation/war fears). In H2, Korea correlation tripled (leverage contagion via memory names), and beta to SPY rose to ~3x — semis became a high-beta, deleveraging-driven asset.
